import numpy as np

from pySDC.implementations.problem_classes.HeatEquation_1D_FD_forced import heat1d_forced
from pySDC.implementations.datatype_classes.mesh import mesh, rhs_imex_mesh
from pySDC.implementations.collocation_classes.gauss_radau_right import CollGaussRadau_Right
from pySDC.implementations.sweeper_classes.imex_1st_order import imex_1st_order
from pySDC.implementations.transfer_classes.TransferMesh import mesh_to_mesh
from pySDC.implementations.controller_classes.allinclusive_multigrid_nonMPI import allinclusive_multigrid_nonMPI

from pySDC.helpers.stats_helper import filter_stats, sort_stats


def main():
    """
    A simple test program to do PFASST runs for the heat equation
    """

    # initialize level parameters
    level_params = dict()
    level_params['restol'] = 1E-10
    level_params['dt'] = 0.25

    # initialize sweeper parameters
    sweeper_params = dict()
    sweeper_params['collocation_class'] = CollGaussRadau_Right
    sweeper_params['num_nodes'] = 3
    sweeper_params['QI'] = 'LU'  # For the IMEX sweeper, the LU-trick can be activated for the implicit part

    # initialize problem parameters
    problem_params = dict()
    problem_params['nu'] = 0.1  # diffusion coefficient
    problem_params['freq'] = 8  # frequency for the test value
    problem_params['nvars'] = 511  # number of degrees of freedom for each level

    # initialize step parameters
    step_params = dict()
    step_params['maxiter'] = 50

    # initialize space transfer parameters
    space_transfer_params = dict()
    space_transfer_params['rorder'] = 2
    space_transfer_params['iorder'] = 2

    # initialize controller parameters
    controller_params = dict()
    controller_params['logger_level'] = 20

    # fill description dictionary for easy step instantiation
    description = dict()
    description['problem_class'] = heat1d_forced                  # pass problem class
    description['problem_params'] = problem_params                # pass problem parameters
    description['dtype_u'] = mesh                                 # pass data type for u
    description['dtype_f'] = rhs_imex_mesh                        # pass data type for f
    description['sweeper_class'] = imex_1st_order                 # pass sweeper
    description['sweeper_params'] = sweeper_params                # pass sweeper parameters
    description['level_params'] = level_params                    # pass level parameters
    description['step_params'] = step_params                      # pass step parameters
    description['space_transfer_class'] = mesh_to_mesh            # pass spatial transfer class
    description['space_transfer_params'] = space_transfer_params  # pass paramters for spatial transfer

    # set time parameters
    t0 = 0.0
    Tend = 4.0

    # instantiate controller
    controller = allinclusive_multigrid_nonMPI(num_procs=1, controller_params=controller_params,
                                               description=description)

    # get initial values on finest level
    P = controller.MS[0].levels[0].prob
    uinit = P.u_exact(t0)

    # call main function to get things done...
    uend, stats = controller.run(u0=uinit, t0=t0, Tend=Tend)

    # The following is used only for statistics and output, the main show is over now..

    # compute exact solution and compare
    uex = P.u_exact(Tend)
    err = abs(uex - uend)

    print('\nError (vs. exact solution) at time %4.2f: %6.4e\n' % (Tend, err))

    filtered_stats = filter_stats(stats, type='niter')

    # convert filtered statistics to list of iterations count, sorted by process
    iter_counts = sort_stats(filtered_stats, sortby='time')

    # compute and print statistics
    for item in iter_counts:
        print('Number of iterations for time %4.2f: %2i' % item)

    niters = np.array([item[1] for item in iter_counts])

    print('   Mean number of iterations: %4.2f' % np.mean(niters))
    print('   Range of values for number of iterations: %2i ' % np.ptp(niters))
    print('   Position of max/min number of iterations: %2i -- %2i' % (int(np.argmax(niters)), int(np.argmin(niters))))


if __name__ == "__main__":
    main()
