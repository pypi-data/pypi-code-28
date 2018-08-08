from __future__ import division

import numpy as np
from numba import jit

from pySDC.core.Problem import ptype
from pySDC.implementations.datatype_classes.particles import particles, fields, acceleration
from pySDC.core.Errors import ParameterError, ProblemError


# noinspection PyUnusedLocal
class penningtrap(ptype):
    """
    Example implementing particles in a penning trap
    """

    def __init__(self, problem_params, dtype_u, dtype_f):
        """
        Initialization routine

        Args:
            problem_params (dict): custom parameters for the example
            dtype_u: particle data type (will be passed parent class)
            dtype_f: acceleration data type (will be passed parent class)
        """

        # these parameters will be used later, so assert their existence
        essential_keys = ['omega_B', 'omega_E', 'u0', 'nparts', 'sig']
        for key in essential_keys:
            if key not in problem_params:
                msg = 'need %s to instantiate problem, only got %s' % (key, str(problem_params.keys()))
                raise ParameterError(msg)

        # invoke super init, passing nparts, dtype_u and dtype_f
        super(penningtrap, self).__init__(problem_params['nparts'], dtype_u, dtype_f, problem_params)

    @staticmethod
    @jit(nopython=True, nogil=True)
    def fast_interactions(N, pos, sig, q):

        Efield = np.zeros((3, N))
        contrib = np.zeros(3)

        for i in range(N):

            contrib[:] = 0

            for j in range(N):

                dist2 = (pos[0, i] - pos[0, j]) ** 2 + (pos[1, i] - pos[1, j]) ** 2 + \
                        (pos[2, i] - pos[2, j]) ** 2 + sig ** 2
                contrib += q[j] * (pos[:, i] - pos[:, j]) / dist2 ** 1.5

            Efield[:, i] += contrib[:]

        return Efield

    def get_interactions(self, part):
        """
        Routine to compute the particle-particle interaction, assuming q = 1 for all particles

        Args:
            part (dtype_u): the particles
        Returns:
            numpy.ndarray: the internal E field for each particle

        """

        N = self.params.nparts

        Efield = self.fast_interactions(N, part.pos.values, self.params.sig, part.q)

        return Efield

    def eval_f(self, part, t):
        """
        Routine to compute the E and B fields (named f for consistency with the original PEPC version)

        Args:
            part (dtype_u): the particles
            t (float): current time (not used here)
        Returns:
            dtype_f: Fields for the particles (internal and external)
        """

        N = self.params.nparts

        Emat = np.diag([1, 1, -2])
        f = fields((3, self.params.nparts))

        f.elec.values = self.get_interactions(part)

        for n in range(N):
            f.elec.values[:, n] += self.params.omega_E ** 2 / (part.q[n] / part.m[n]) * \
                np.dot(Emat, part.pos.values[:, n])
            f.magn.values[:, n] = self.params.omega_B * np.array([0, 0, 1])

        return f

    def u_init(self):
        """
        Routine to compute the starting values for the particles

        Returns:
            dtype_u: particle set filled with initial data
        """

        u0 = self.params.u0
        N = self.params.nparts

        u = particles((3, N))

        if u0[2][0] is not 1 or u0[3][0] is not 1:
            raise ProblemError('so far only q = m = 1 is implemented')

        # set first particle to u0
        u.pos.values[0, 0] = u0[0][0]
        u.pos.values[1, 0] = u0[0][1]
        u.pos.values[2, 0] = u0[0][2]
        u.vel.values[0, 0] = u0[1][0]
        u.vel.values[1, 0] = u0[1][1]
        u.vel.values[2, 0] = u0[1][2]

        u.q[0] = u0[2][0]
        u.m[0] = u0[3][0]

        # initialize random seed
        np.random.seed(N)

        comx = u.pos.values[0, 0]
        comy = u.pos.values[1, 0]
        comz = u.pos.values[2, 0]

        for n in range(1, N):
            # draw 3 random variables in [-1,1] to shift positions
            r = np.random.random_sample(3) - 1
            u.pos.values[0, n] = r[0] + u0[0][0]
            u.pos.values[1, n] = r[1] + u0[0][1]
            u.pos.values[2, n] = r[2] + u0[0][2]

            # draw 3 random variables in [-5,5] to shift velocities
            r = np.random.random_sample(3) - 5
            u.vel.values[0, n] = r[0] + u0[1][0]
            u.vel.values[1, n] = r[1] + u0[1][1]
            u.vel.values[2, n] = r[2] + u0[1][2]

            u.q[n] = u0[2][0]
            u.m[n] = u0[3][0]

            # gather positions to check center
            comx += u.pos.values[0, n]
            comy += u.pos.values[1, n]
            comz += u.pos.values[2, n]

        # print('Center of positions:',comx/N,comy/N,comz/N)

        return u

    def u_exact(self, t):
        """
        Routine to compute the exact trajectory at time t (only for single-particle setup)

        Args:
            t (float): current time
        Returns:
            dtype_u: particle type containing the exact position and velocity
        """

        # some abbreviations
        wE = self.params.omega_E
        wB = self.params.omega_B
        N = self.params.nparts
        u0 = self.params.u0

        if N != 1:
            raise ProblemError('u_exact is only valid for a single particle')

        u = particles((3, 1))

        wbar = np.sqrt(2) * wE

        # position and velocity in z direction is easy to compute
        u.pos.values[2, 0] = u0[0][2] * np.cos(wbar * t) + u0[1][2] / wbar * np.sin(wbar * t)
        u.vel.values[2, 0] = -u0[0][2] * wbar * np.sin(wbar * t) + u0[1][2] * np.cos(wbar * t)

        # define temp. variables to compute complex position
        Op = 1 / 2 * (wB + np.sqrt(wB ** 2 - 4 * wE ** 2))
        Om = 1 / 2 * (wB - np.sqrt(wB ** 2 - 4 * wE ** 2))
        Rm = (Op * u0[0][0] + u0[1][1]) / (Op - Om)
        Rp = u0[0][0] - Rm
        Im = (Op * u0[0][1] - u0[1][0]) / (Op - Om)
        Ip = u0[0][1] - Im

        # compute position in complex notation
        w = np.complex(Rp, Ip) * np.exp(-np.complex(0, Op * t)) + np.complex(Rm, Im) * np.exp(-np.complex(0, Om * t))
        # compute velocity as time derivative of the position
        dw = -1j * Op * np.complex(Rp, Ip) * \
            np.exp(-np.complex(0, Op * t)) - 1j * Om * np.complex(Rm, Im) * np.exp(-np.complex(0, Om * t))

        # get the appropriate real and imaginary parts
        u.pos.values[0, 0] = w.real
        u.vel.values[0, 0] = dw.real
        u.pos.values[1, 0] = w.imag
        u.vel.values[1, 0] = dw.imag

        return u

    def build_f(self, f, part, t):
        """
        Helper function to assemble the correct right-hand side out of B and E field

        Args:
            f (dtype_f): the field values
            part (dtype_u): the current particles data
            t (float): the current time
        Returns:
            acceleration: correct RHS of type acceleration
        """

        if not isinstance(part, particles):
            raise ProblemError('something is wrong during build_f, got %s' % type(part))

        N = self.params.nparts

        rhs = acceleration((3, self.params.nparts))

        for n in range(N):
            rhs.values[:, n] = part.q[n] / part.m[n] * (f.elec.values[:, n] +
                                                        np.cross(part.vel.values[:, n], f.magn.values[:, n]))

        return rhs

    # noinspection PyTypeChecker
    def boris_solver(self, c, dt, old_fields, new_fields, old_parts):
        """
        The actual Boris solver for static (!) B fields, extended by the c-term

        Args:
            c (dtype_u): the c term gathering the known values from the previous iteration
            dt (float): the (probably scaled) time step size
            old_fields (dtype_f): the field values at the previous node m
            new_fields (dtype_f): the field values at the current node m+1
            old_parts (dtype_u): the particles at the previous node m
        Returns:
            the velocities at the (m+1)th node
        """

        N = self.params.nparts
        vel = particles.velocity((3, N))

        Emean = 0.5 * (old_fields.elec + new_fields.elec)

        for n in range(N):
            a = old_parts.q[n] / old_parts.m[n]

            c.values[:, n] += dt / 2 * a * \
                np.cross(old_parts.vel.values[:, n], old_fields.magn.values[:, n] - new_fields.magn.values[:, n])

            # pre-velocity, separated by the electric forces (and the c term)
            vm = old_parts.vel.values[:, n] + dt / 2 * a * Emean.values[:, n] + c.values[:, n] / 2
            # rotation
            t = dt / 2 * a * new_fields.magn.values[:, n]
            s = 2 * t / (1 + np.linalg.norm(t, 2) ** 2)
            vp = vm + np.cross(vm + np.cross(vm, t), s)
            # post-velocity
            vel.values[:, n] = vp + dt / 2 * a * Emean.values[:, n] + c.values[:, n] / 2

        return vel
