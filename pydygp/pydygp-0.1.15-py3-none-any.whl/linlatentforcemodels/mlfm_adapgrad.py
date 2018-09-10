"""
The Multiplicative Latent Force Model using adaptive gradient matching.
"""
import numpy as np
from pydygp.kernels import Kernel, GradientKernel
from pydygp.gaussianprocesses import GaussianProcess
from collections import namedtuple
from scipy.linalg import solve_triangular, block_diag
from scipy.interpolate import interp1d
# Default settings

X_KERN_DEFAULT = 'sqexp'
GAMMAS_DEFAULT = 1e-1

# Model dimensions:
#   N - size of augmented time vector
#   K - dimension of the ambient space
#   R - number of latent forces
Dimensions = namedtuple('Dimensions', 'N K R')

class AdapGradLatentState(GaussianProcess):
    """
    Latent state class extending :class:`.GaussianProcess`.

    Models the Gaussian process interpolators of the latent state variables.
    """

    def Qk(self, ExxT, uk, phik, gammak):
        """
        local obj func. after marginalising over latent states in the EM algorithm
        """

        # only implemented for the basic RBF in gradientkernel
        const_par = phik[0]
        theta = np.log(phik[1])  # sklearn kernels work in parameter log-space

        kernel = self.kernel.clone_with_theta(theta)

        Cxx = kernel(self.Xtrain)
        Cxdx = kernel(self.Xtrain, comp='xdx')
        Cdxdx = kernel(self.Xtrain, comp='dxdx')

        Lxx = np.linalg.cholesky(Cxx)

        Mk = Cxdx.T.dot(back_sub(Lxx, np.eye(Lxx.shape[0])))

        diagUk = [np.diag(ukj) for ukj in uk]
        diagUk[k] -= Mk

        ic = np.dot(np.row_stack([dkj.T for dkj in diagUk]),
                    np.column_stack([back_sub(Skchol, dkj)
                                     for dkj in diagUk]))

        return -0.5*np.trace(ExxT.dot(ic))

    def EM_Mstep_hyperpar_fit(self, ExxT, uk):
        """
        Updates the latent state hyperparameters using the EM algorithm.
        """
        gamma = self.gamma_
        phik = self.hyperparameters

        def objfunc(gamma_phi):
            gamma = gamma_phi[0]
            phi = gamma_phi[1:]
            return -self.Qk(ExxT, uk, phi, gamma)

        res = minimize(objfunc, np.concatenate(self.gamma, self.phik))
        gamma_hat = res[0]
        phi_hat = res[1:]

        # update
        self.phi_ = phi_hat
        self.gamma_ = gamma_hat

    @property
    def chol(self):
        try:
            return self._L
        except:
            # attempt to create it
            C = self.kernel.cov(self.Xtrain)
            L = np.linalg.cholesky(C)
            self._L = L
            return L

    def update_covs(self):
        gamma = self.gamma
        Lxx, Cxdx, Cdx_x = gpdxk_cond_cov(self.Xtrain[:, 0],
                                          self,
                                          self.kernel_hyperpar)
        I = np.eye(Lxx.shape[0])
        M = np.dot(Cxdx.T,
                   solve_triangular(Lxx.T,
                                    solve_triangular(Lxx, I, lower=True)))
        S = Cdx_x + gamma*I

        self._L = Lxx
        self.Mdx = M
#        self.Cxdx = Cxdx
        self.Cdx_x = Cdx_x
        self.S_chol = np.linalg.cholesky(S)

    def hyperpar_ll(self, fk, xk, gamma=None, phi=None):
        """
        Isolated terms of the log-likelihood depending on the hyper-parameters.
        """
        if gamma is None:
            gamma = self.gamma

        if phi is not None:
            # need to build all the covariance matrices
            Lxx, Cxdx, Cdx_x = gpdxk_cond_cov(self.Xtrain[:, 0],
                                               self,
                                               phi)

            I = np.eye(Lxx.shape[0])
            M = np.dot(Cxdx.T,
                       solve_triangular(Lxx.T,
                                        solve_triangular(Lxx, I), lower=True))

            S = Cdx_x + gamma*I
            S_chol = np.linalg.cholesky(S)

        else:
            M = self.Mdx
            # phi has not change but gamma might have
            if gamma is not None:
                S = self.Cdx_x + gamma*np.eye(self.Cdx_x.shape[0])
                S_chol = np.linalg.cholesky(S)                


        eta = fk - np.dot(M, xk)
        return -0.5*np.dot(eta,
                           solve_triangular(S_chol.T,
                                            solve_triangular(S_chol, eta)))

class LatentForce(GaussianProcess):

    Xtrain = None  # corresponds to the latent time points
    Ytrain = None  # corresponds to the current trained forces
    
    """
    Latent force class extending the base GaussianProcess class.

    Allows for seperate handling of an overall force precision for ARD.
    """
    def __init__(self, kernel, precision=1, a=1, b=1):
        super(LatentForce, self).__init__(kernel)
        self.precision = precision  # initalise precision
        self.hyperpar_a = a  # Latent force precisions are given
        self.hyperpar_b = b  # Gamma(a, b) conjugate hyperparameter


    @property
    def base_chol(self):
        """
        Cholesky decomp. of base cov (with no precision term)
        """
        try:
            return self._L0
        except:
            pass

    @property
    def chol(self):
        return self._L0/np.sqrt(self.precision)
    

class MLFMAdapGrad:
    def __init__(self, struct_mats):
        self.struct_mats = np.asarray(struct_mats)
        self.dim = Dimensions(None, self.struct_mats.shape[-1], self.struct_mats[0]-1)

        # model flags
        self.is_comp_data = False
        self.data_precision_is_cong = True

    def setup(self, data_times, data_Y, aug_times=None):
        # attachement of data and times
        self._data_times = data_times
        self.data_Y = data_Y

        # update dimensions
        self.dim = Dimensions(data_times.size, self.dim.K, self.dim.R)

    def setup_latentstates(self):
        x_kernels = [RBF() for k in range(self.dim.K)]
        self.latent_states = [AdapGradLatentState(kern) for kern in x_kernels]

    def setup_latentforces(self, latent_forces):
        self.latent_forces = latent_forces
        

class MLFM_AdapGrad:
    """Base class for MLFM with adaptive gradient matching.

    """
    def __init__(self, struct_mats):
        self.struct_mats = np.asarray(struct_mats)
        self.dim = Dimensions(None, self.struct_mats.shape[-1], self.struct_mats.shape[0]-1)
        
        # various model flags
        self.is_comp_data = False
        self.data_precision_is_cong = True

    def loglikelihood(self, vecg, gamma, phi):
        pass

    def Q(self, mx, covx, vecg, gamma=None, phi=None):

        if phi is None:
            Mk_list = [xgp.Mdx for xgp in self.x_gps]
            Cdx_x_list = [xgp.Cdx_x for xgp in self.x_gps]
        else:
            # build M from phi
            Mk_list = []
            for k in range(self.dim.K):
                Cxx = self.x_gps[k].kernel.cov(self.ttf[:, None], kpar=phi[k], comp='x')
                Lxx = np.linalg.cholesky(Cxx)
                Cxdx = self.x_gps[k].kernel.cov(self.ttf[:, None], kpar=phi[k], comp='xdx')
                Mk_list.append(np.dot(Cxdx.T, back_sub(Lxx, np.eye(self.dim.N))))
                
                
        if gamma is None:
            Schol_list = [xgp.S_chol for xgp in self.x_gps]

        else:
            # build S from gamma
            Cdx_x = Cdx_x_list[k]
            Schol_list = [np.linalg.cholesky(Cdx_x + g*np.eye(self.dim.N))
                          for g, xgp in zip(gamma, self.x_gps)]

        val = 0.
        minv_cov = [] # inv cov from ode model contribution
        for k, Skchol in enumerate(Schol_list):

            Mk = Mk_list[k]

            uk = self.x_flowk_rep(k, vecg)
            diagUk = [np.diag(ukj) for ukj in uk]
            diagUk[k] -= Mk

            ic = np.dot(np.row_stack([dkj.T for dkj in diagUk]),
                        np.column_stack([back_sub(Skchol, dkj)
                                         for dkj in diagUk]))
            minv_cov.append(ic)

        # sum the model component inv covs.
        minv_cov = sum(minv_cov)

        ExxT = covx + np.outer(mx, mx)

        val = -0.5*np.trace(np.dot(ExxT, minv_cov))

        # for MAP estimates we also need to add the prior info.
        for g, ggp in zip(vecg.reshape(self.dim.R, self.dim.N),
                          self.g_gps):
            val += -0.5*np.dot(g, back_sub(ggp.chol, g))

        return val

    ########################
    # These will get moved #
    ########################
    def Estep(self, vecg):
        """
        constructs the mean and cov. of X conditional
        on current point estimates of latent force
        """
        
        invcov = []
        for k in range(self.dim.K):
            uk = self.x_flowk_rep(k, vecg)
            Mk = self.x_gps[k].Mdx
            S_chol = self.x_gps[k].S_chol

            diagUk = [np.diag(uki) for uki in uk]
            diagUk[k] -= Mk

            ic = np.dot(np.row_stack([dki.T for dki in diagUk]),
                        np.column_stack([back_sub(S_chol, dkj)
                                         for dkj in diagUk]))
            invcov.append(ic)
        invcov = sum(invcov)

        # add contribution from prior
        invcov += block_diag(*[back_sub(xgp.chol, np.eye(self.dim.N))
                               for xgp in self.x_gps])

        # add contribution from data
        data_inv_cov = block_diag(*[tau*np.eye(self.dim.N)
                                    for tau in self.cur_data_precision])

        invcov += data_inv_cov
        invcov_chol = np.linalg.cholesky(invcov)
        
        premean = data_inv_cov.dot(self.data_Y.T.ravel())

        cov = back_sub(invcov_chol, np.eye(self.dim.N*self.dim.K))
        mean = np.dot(cov, premean)

        return mean, cov

        """
        def back_sub(L, x):
            return solve_triangular(L.T, solve_triangular(L, x, lower=True))

        # Contribution from the model log-likelihood term
        invcov = []
        inv_covs = []
        means = []
        for k in range(self.dim.K):
            ic = np.zeros((self.dim.N*self.dim.K,
                           self.dim.N*self.dim.K))

            uk = self.x_flowk_rep(k, vecg)

            Mk = self.x_gps[k].Mdx
            S_chol = self.x_gps[k].S_chol
            Sinv = np.linalg.inv(S_chol.dot(S_chol.T))
            Sinv_Mk = back_sub(S_chol, Mk)

            for m in range(self.dim.K):
                for n in range(self.dim.K):

                    #res = np.dot(np.diag(uk[m]), back_sub(S_chol, np.diag(uk[n])))
                    res = np.outer(uk[m], uk[n])*Sinv
                    #assert(np.all(res == _res))

                    if m == k:
                        res -= np.dot(Mk.T, back_sub(S_chol, np.diag(uk[n])))

                        if n == k:
                            res -= np.dot(np.diag(uk[m]), Sinv_Mk)
                            res += Mk.T.dot(Sinv_Mk)

                    elif n == k:
                        res -= np.dot(np.diag(uk[m]), Sinv_Mk)

                    ic[m*self.dim.N:(m+1)*self.dim.N,
                       n*self.dim.N:(n+1)*self.dim.N] = res

            invcov.append(ic)
            inv_covs.append(ic)
            means.append(np.zeros(self.dim.K*self.dim.N))

        prior_inv_cov = block_diag(*[back_sub(gp.chol, np.eye(self.dim.N))
                               for gp in self.x_gps])
        means.append(np.zeros(self.dim.K*self.dim.N))
        inv_covs.append(prior_inv_cov)

        # Contribution from the data
        if not self.is_comp_data:
            x_data_mean = self.data_Y.T.ravel()
            x_data_inv_cov = np.diag(
                np.concatenate([tau*np.ones(self.dim.N) for tau in self._cur_data_precision])
                )

        inv_covs.append(x_data_inv_cov)
        means.append(x_data_mean)
        _mean, _cov = prod_norm_pars(means, inv_covs)
        
            
        invcov = sum(invcov)

        # Contribution from the prior
        invcov += block_diag(*[back_sub(gp.chol, np.eye(self.dim.N))
                               for gp in self.x_gps])

        # Contribution from the data
        if not self.is_comp_data:
            x_data_mean = self.data_Y.T.ravel()
            x_data_inv_cov = np.diag(
                np.concatenate([tau*np.ones(self.dim.N) for tau in self._cur_data_precision])
                )

        pre_mean = np.dot(x_data_inv_cov, x_data_mean)

        invcov += x_data_inv_cov

        mean = np.linalg.solve(invcov, pre_mean)
        c = np.linalg.inv(invcov)
        return mean, c
"""

    def Mstep_lf(self, Evecx, covx):
        """
        Mstep for the latent forces.

        Obtained by marginalising out the latent states and holding the
        remaining variables fixed.
        """
        inv_covar = []
        pre_mean = []
        # contribution from model

        def CovX(i, j):
            return covx[self.dim.N*i:self.dim.N*(i+1),
                        self.dim.N*j:self.dim.N*(j+1)]
        def ExxT(i, j):
            exi = Evecx[self.dim.N*i:self.dim.N*(i+1)]
            exj = Evecx[self.dim.N*j:self.dim.N*(j+1)]
            cij = covx[self.dim.N*i:self.dim.N*(i+1),
                       self.dim.N*j:self.dim.N*(j+1)]
            return cij + np.outer(exi, exj)

        def cov_vkr_vks(k, r, s):
            res = np.zeros((self.dim.N, self.dim.N))
            for i in range(self.dim.K):
                for j in range(self.dim.K):
                    cij = CovX(i, j)
                    res += cij*self.struct_mats[r, k, i]*self.struct_mats[s, k, j]
            return res
        
        for k in range(self.dim.K):
            Evk = g_Eflowk_rep(self, k, Evecx)
            cov_vk = g_Eflowk_rep_cov(self, k, covx)

            cov_vk_xk = [sum(a[k, j]*covx[j*self.dim.N:(j+1)*self.dim.N,
                                          k*self.dim.N:(k+1)*self.dim.N]
                             for j in range(self.dim.K))
                         for a in self.struct_mats[1:]]

            Mk = self.x_gps[k].Mdx
            cov_vk_mk = [np.dot(cvx, Mk) for cvx in cov_vk_xk]

            L = self.x_gps[k].S_chol
            Skinv = back_sub(L, np.eye(self.dim.N))

            ic = np.row_stack((
                np.column_stack(
                ((cov_vk[(s, t)] + np.outer(Evk[s], Evk[t]))*Skinv
                 for t in range(1, self.dim.R+1))
                ) for s in range(1, self.dim.R+1)))

            EvkT_Skinv_v0 = np.concatenate(
                [E_diagx_M_y(Evk[s], Evk[0], cov_vk[(s, 0)], Skinv)
                 for s in range(1, self.dim.R+1)]
                )

            EX = Evecx.reshape(self.dim.K, self.dim.N)
            EvkT_Skinv_mk = np.concatenate(
                [E_diagx_M_y(Evks, np.dot(Mk, EX[k,:]), cvsmk, Skinv)
                 for Evks, cvsmk in zip(Evk[1:], cov_vk_mk)]
                )
            
            inv_covar.append(ic)
            pre_mean.append(EvkT_Skinv_mk - EvkT_Skinv_v0)

        means = [ic.dot(pm) for ic, pm in zip(inv_covar, pre_mean)]
        prior_inv_cov = block_diag(*[back_sub(lf.chol, np.eye(self.dim.N))
                                     for lf in self.g_gps])
        inv_covar.append(prior_inv_cov)
        means.append(np.zeros(self.dim.N*self.dim.R))

        _mean, _cov = prod_norm_pars(means, inv_covar)
        
        inv_covar = sum(inv_covar)
        pre_mean = sum(pre_mean)

        inv_covar += block_diag(*[back_sub(lf.chol, np.eye(self.dim.N))
                                  for lf in self.g_gps])

        mean = np.linalg.solve(inv_covar, pre_mean)

        return _mean


    def flowk_rep(self, k, vecx, vecg):
        """
        Returns the kth component of the flow.
        """
        uk = self.x_flowk_rep(k, vecg)
        X = vecx.reshape(self.dim.K, self.dim.N)
        fk = sum(uki*xi for uki, xi in zip(uk, X))
        return fk

    def x_flowk_rep(self, k, vecg):
        """
        Represents the flow vector fk as sum_j ukj o xj
        """
        A = self.struct_mats
        G = vecg.reshape(self.dim.R, self.dim.N)
        uk = [A[0, k, j] + sum([ar[k, j]*gr for ar, gr in zip(A[1:,:,:], G)])
              for j in range(self.dim.K)]
        return uk

    def g_flowk_rep(self, k, vecx):
        """
        Represents the flow vector fk as sum_r vkr o gr
        """
        A = self.struct_mats
        X = vecx.reshape(self.dim.K, self.dim.N)
        # contrib. from the offset matrix        
        vk0 = sum(A[0, k, j]*xj for j, xj in enumerate(X))  
        vk = [sum(ar[k, j]*xj for j, xj in enumerate(X)) for ar in A[1:]]
        return vk, vk0


    def setup(self, data_times, data_Y=None, aug_times=None, **kwargs):
        """
        default setup function carries out model initalisation
        """
        # Attachement of data and times
        self._data_times = data_times
        self.data_Y = data_Y

        # Update dimensions to add number of data points
        self.dim = Dimensions(data_times.size, self.dim.K, self.dim.R)

        # setup of the model variables called in a way respecting
        # the model hierarchy
        self._gammas_setup()
        #self._xp_setup(aug_times, **kwargs)

    def setup_latentstates(self, kernels):
        """
        Creates the latent states GP interpolators from kernels
        """
        assert(len(kernels) == self.dim.K)
        self.x_gps = [AdapGradLatentState(k) for k in kernels]
        for gam, gp in zip(self.gammas, self.x_gps):
            gp.gamma = gam

    def setup_latentforce_gps(self, kernels):
        """
        Creates the latent force GP from kernels.
        """
        assert(len(kernels) == self.dim.R)
        self.g_gps = [LatentForce(k) for k in kernels]

    def setup_data(self,
                   data_times, data_Y,
                   comp_times=None, data_inds=None):
        """Attach data to the model, optionally include augmented latent state points
        """
        self.data_Y = data_Y
        if comp_times is None:
            # no additional latent states
            self._data_times = data_times
        else:
            if data_inds is not None:
                self._comp_times = comp_times
            else:
                raise ValueError("Must supply the indices of data obs. in the completed time set")
                

    """
    Setup prior and proposal functions
    * data precisions
    * latent state gp hyperparameters
    * latent force gp hyperparameters
    * prior for offset matrix (ToDo)
    """
    def setup_data_precision(self, ab=None):
        """Prior and proposal distribution for the data precisions - defaults to
        conjugate gamma
        """
        if ab is not None:
            # setup is being done using the conjugate gamma 
            self.data_precision_ab = ab
        else:
            self.data_precision_is_cong = False            
            raise NotImplementedError('Currently only the conjugate gamma is supported')


    def _gammas_setup(self, gammas=None):
        if gammas == None:
            self.gammas = GAMMAS_DEFAULT*np.ones(self.dim.K)

        else:
            self.gammas = gammas

    """
    def _x_gp_setup(self, aug_times=None, x_kern='sqexp', x_kpar=None, **kwargs):

        # enhances the model with additional latent input times
        if aug_times is not None:
            add_latent_states(self, self.data_times, aug_times, **kwargs)
    """

    def x_cond_posterior(self, x, Y=None, gs=None, x_kpars=None):
        """ Evaluates the conditional posterior

        .. math::
           p(\mathbf{x}|\mathbf{y}, \mathbf{g}, \\boldsymbol{\phi})

        [more explanation]
        """
        if Y is None:
            Y = self.data_Y

        if x_kpars is None:
            x_kpars = [None for k in range(self.dim.K)]

        fks = None

        logp = 0.

        for k, gp in enumerate(self.x_gps):
            
            Mk, Sk_chol, Cxx_chol = dx_gp_condmats(tt, kern, x_kpars[k], 'chol')


    """
    Model Utility Functions
    """
    def _update_x_cov_structure(self):
        """
        Updates
        * the cholesky decomposition of the latent states
        * the cross covariance C(x,dx) of the states and their gradients
        * the gradient conditioned on state cov matrices
        """
        Lxx, Cxdx, Cdx_x = gpdx_cond_cov(self.ttf, self.x_gps)
        self._x_cov_chols = Lxx
        self._xdx_cross_covs = Cxdx
        self._x_grad_cond_covs = Cdx_x

        Mk_list = [np.dot(cxdx.T,
                          np.linalg.solve(L.T,
                                          np.linalg.solve(L, np.eye(L.shape[0]))))
                   for cxdx, L in zip(self._xdx_cross_covs, self._x_cov_chols)]
        self._Mdx_list = Mk_list

        Sinv_list = [np.linalg.inv(c+g**2*np.eye(c.shape[0]))
                     for c, g in zip(Cdx_x, self.gammas)]
        self._Sinv_covs = Sinv_list    

    def _update_g_cov_structure(self):
        # add a bit of alpha noise
        aI = 1e-5*np.eye(self.dim.N)
        Cgg = [gp.kernel.cov(self.ttf[:, None]) + aI for gp in self.g_gps]

        # calculate the cholesky decomp.
        self._g_cov_chols = [np.linalg.cholesky(c) for c in Cgg]
        

    def log_model_likelihood(self, vecx, vecg,
                             Mdx_mats=None, Skinv_covs=None):
        """Loglikelihood of the ODE model dependent part of the model
        """
        ell = 0.

        # bit of reshaping
        X = vecx.reshape(self.dim.K, self.dim.N)

        if Mdx_mats is None:
            Mdx_mats = self._Mdx_list
        if Skinv_covs is None:
            Skinv_list = self._Sinv_covs
        
        for k in range(self.dim.K):

            uk = self.x_flowk_rep(k, vecg)

            # kth component of the flow function 
            fk = sum([ukj*xj for ukj, xj in zip(uk, X)])

            # conditioned estimated of the flow
            mk = np.dot(Mdx_mats[k], X[k, :])

            etak = fk - mk

            ell += -0.5*np.dot(etak, np.dot(Sinv_covs[k], etak))

        return ell

    def model_x_dist(self, vecg):
        """
        Conditional on g the model can be rearranged as the quad. form of
        a normal in X
        """
        inv_cov = []
        for k in range(self.dim.K):
            uk = self.x_flowk_rep(k, vecg)
            Mk = self.x_gps[k].Mdx #self._Mdx_list[k]
            S_chol = self.x_gps[k].S_chol
            Skinv = solve_triangular(S_chol.T, solve_triangular(S_chol, np.eye(self.dim.N), lower=True))
            #Skinv = self._Sinv_covs[k]

            diagUk = [np.diag(uki) for uki in uk]
            diagUk[k] -= Mk

            ic = np.dot(np.row_stack([dki.T for dki in diagUk]),
                        np.column_stack([np.dot(Skinv, dkj) for dkj in diagUk]))

            inv_cov.append(ic)

        ic = sum(inv_cov)
        return 0, ic

    def model_g_dist(self, vecx, include_prior=True):
        """
        Conditional on x the model can be arranged as a normal dist. for g
        """
        inv_cov = []
        pre_mean = []
        for k in range(self.dim.K):
            vk, vk0 = self.g_flowk_rep(k, vecx)
            Mk = self._Mdx_list[k]
            Skinv = self._Sinv_covs[k]

            mk = np.dot(Mk, vecx[k*self.dim.N:(k+1)*self.dim.N])

            diagVk = [np.diag(vkr) for vkr in vk]
            Skinv_diagVk = np.column_stack([np.dot(Skinv, dVk) for dVk in diagVk])
            ic = np.dot(np.row_stack(diagVk), Skinv_diagVk)

            pm = Skinv_diagVk.T.dot((mk - vk0)[:, None])

            inv_cov.append(ic)
            pre_mean.append(pm)

        inv_cov = sum(inv_cov)
        pre_mean = sum(pre_mean)

        if include_prior:
            try:
                # look for stored cov
                chols = [gp.chol for gp in self.g_gps]
                Cgginv = [solve_triangular(L.T,
                                           solve_triangular(L, np.eye(self.dim.N), lower=True))
                          for L in chols]
            except:
                Cgg = [gp.kernel.cov(self.ttf[:, None]) for gp in self.g_gps]
                Cgginv = [np.linalg.inv(Cgr) for Cgr in Cgg]

            inv_cov += block_diag(*Cgginv)

        cov = np.linalg.inv(inv_cov)
        mean = np.dot(cov, pre_mean)

        return mean.ravel(), cov
        
    def log_prior(self, vecx=None, vecg=None):
        """logpdf of the prior 
        """
        ell = 0.

        if vecx is not None:
            X = vecx.reshape(self.dim.K, self.dim.N)  # reshape

            for x, L in zip(X, self._x_cov_chols):
                ell += -0.5*np.dot(x,
                                   solve_triangular(L.T,
                                                    solve_triangular(L, x, lower=True)))

        if vecg is not None:
            G = vecg.reshape(self.dim.R, self.dim.N)  # reshape

            for g, L in zip(G, self._g_cov_chols):
                ell += -0.5*np.dot(g,
                                   solve_triangular(L.T,
                                                    solve_triangular(L, g, lower=True)))


        return ell

    @property
    def ttf(self):
        """The full time vector

        equal to the data times if no additional latent states included
        """
        if self.is_comp_data:
            return self._comp_times
        else:
            return self.data_times


    @property
    def data_times(self):
        """
        Time points for attached data
        """
        try:
            return self._data_times
        except:
            return None


    @property
    def data_map(self):
        """
        Matrix that maps the augmented latent states
        to the data for which there is an observed data
        point
        """
        if is_comp_data:
            data_map = np.row_stack((np.eye(N=1, M=self.dim.N, k=i)
                                     for i in self.data_inds))
            data_map = block_diag(*[data_map]*self.dim.K)
            return data_map
        else:
            return np.eye(self.dim.N*self.dim.K)


"""
General utility and helper functions for the mlfm
adaptive gradient matching methods
"""

def gpdx_cond_cov(tt, gps):
    """
    Returns the set of conditional cov. matrices of the gradients
    """
    Lxx_list = []   # Cholesky decomposition of state cov
    Cxdx_list = []  #
    Cdx_x_list = []

    for gp in gps:

        # auto cov. of the state
        Cxx = gp.kernel.cov(tt[:, None], comp='x')
        # cross cov. of the state and grad
        Cxdx = gp.kernel.cov(tt[:, None], comp='xdx')
        # auto cov. of the grad
        Cdxdx = gp.kernel.cov(tt[:, None], comp='dxdx')

        Lx = np.linalg.cholesky(Cxx)

        # cond. cov of the grad given the state
        Cdx_x = Cdxdx - np.dot(Cxdx.T, np.linalg.solve(Lx.T,
                                                       np.linalg.solve(Lx, Cxdx)))

        Lxx_list.append(Lx)
        Cxdx_list.append(Cxdx)
        Cdx_x_list.append(Cdx_x)

    return Lxx_list, Cxdx_list, Cdx_x_list


def gpdxk_cond_cov(tt, gpk, kpar=None, alpha=0):
    """
    Returns the set of conditional cov. matrices of the gradients
    """
    Cxx = gpk.kernel.cov(tt[:, None], comp='x')
    Cxdx = gpk.kernel.cov(tt[:, None], comp='xdx')
    Cdxdx = gpk.kernel.cov(tt[:, None], comp='dxdx')

    if alpha > 0:
        Cxx += np.diag(alpha*np.ones(tt.size))
    
    Lxx = np.linalg.cholesky(Cxx)

    Cdx_x = Cdxdx - np.dot(Cxdx.T, np.linalg.solve(Lxx.T,
                                                   np.linalg.solve(Lxx, Cxdx)))

    return Lxx, Cxdx, Cdx_x

        
    
class MLFMAdapGrad_MCMC(MLFM_AdapGrad):

    y_train = None # data training points

    @property
    def cur_data_precision(self):
        # current MC sample of the data precision
        return self._cur_data_precision
    
    """MLFM with adaptive gradient matching and model fitting done
    using MCMC methods
    """
    def __init__(self, *args, **kwargs):
        super(MLFMAdapGrad_MCMC, self).__init__(*args, **kwargs)

    """
    Variable initalisation functions for MCMC fitting
    """
    def init_data_precision(self, strategy='value', value=None):

        if strategy == 'value':
            # data precision terms initalised by value 
            assert(value is not None)

        elif strategy == 'rvs':
            # initalise by drawing from prior
            pass

    def init_x(self, strategy='interp'):
        if strategy == 'interp':
            xinterp = [interp1d(self.data_times, yk) for yk in zip(self.data_Y.T)]
            xnew = np.concatenate([u(self.ttf).ravel() for u in xinterp])
            self.vecx = xnew

        # attach the time vectors to the latent state GPs
        for gp in self.x_gps:
            gp.Xtrain = self.ttf[:, None]

    def init_lf_precisions(self, strategy='value', value=None):
        if strategy == 'value':
            assert(len(value) == self.dim.R)
            for val, lf in zip(value, self.g_gps):
                lf.precision = val

    def init_lf(self, strategy='prior'):
        for g in self.g_gps:
            if strategy == 'prior':
                grv = g.sim(self.ttf[:, None])
                g.y_train = grv
            # store the values, but more importantly the cov
            g.X_train = self.ttf[:, None]
            C = g.kernel.cov(g.X_train)
            L = np.linalg.cholesky(C)
            g._L0 = L
                
    def init_ls_hyperpar(self, strategy='value', value=None):
        if strategy == 'value':
            assert(len(value) == self.dim.K)
            for val, ls in zip(value, self.x_gps):
                ls.kernel_hyperpar = val  # update the latent state kernel hyper

                ls.update_covs()

    def data_precision_update(self):
        if self.data_precision_is_cong:
            # Update done using the conjugate gamma distribution
            pass

    def latentforce_gibbs_update(self):
        pass

    def latentstate_gibbs_update(self):
        # contribution from model
        m_model, ic_model = self.model_x_dist(self.vecg)

        # contribution from prior
        ic_prior = block_diag(*[solve_triangular(gp.chol.T,
                                                 solve_triangular(gp.chol, np.eye(self.dim.N), lower=True))
                                for gp in self.x_gps])

        # contribution from data
        if not self.is_comp_data:

            inv_cov = ic_model + ic_prior + block_diag(*[tau*np.eye(self.dim.N)
                                                        for tau in self.cur_data_precision])
            pre_mean = np.concatenate([yk*tau
                                       for yk, tau in zip(self.data_Y.T,
                                                          self.cur_data_precision)])
        else:
            raise NotImplementedError

        cov = np.linalg.inv(inv_cov)
        #mean = np.linalg.solve(inv_cov, pre_mean)
        mean = np.dot(cov, pre_mean)
        return mean, cov

    def xk_hyperpar_mh_update(self):

        # rewrite the conditional log pdf for only those terms
        # dependent on the hyperparameter of xk
        def lk(phi_k):
            Lxx, Mdx, Cdx_x = gpdxk_cond_cov(self.ttf,
                                             self.x_gps[k],
                                             kpar=phi_k)
                                             


"""
Methods to make the EM algorithm work
"""
def g_Eflowk_rep(obj, k, Evecx):
    """
    Represents the flow vector fk as sum_r E[vkr] o gr
    """
    A = obj.struct_mats
    EX = Evecx.reshape(obj.dim.K, obj.dim.N)
    Evk = [sum(a[k, j]*Exj for j, Exj in enumerate(EX))
           for a in A]

    return Evk

def g_Eflowk_rep_cov(obj, k, covx):
    """
    Returns the covariance matrix of the vectors {vkr}.
    """
    A = obj.struct_mats
    I = np.eye(obj.dim.N)

    res_dict = {}
    for s in range(obj.dim.R+1):
        asi = np.column_stack((a*I for a in A[s, k, :]))
        for t in range(s+1):
            ati = np.column_stack((a*I for a in A[t, k, :]))
            res = np.dot(asi, np.dot(covx, ati.T))

            res_dict[(s, t)] = res
            res_dict[(t, s)] = res.T

    return res_dict


######################################################
#                                                    #
# E[diag(x) M y ] = np.sum(Exyt * M, axis=1)         #
#                                                    #
######################################################
def E_diagx_M_y(E_x, E_y, Cov_xy, M):
    ExyT = Cov_xy + np.outer(E_x, E_y)
    return np.sum(ExyT * M, axis=1)

def back_sub(L, x):
    return solve_triangular(L.T, solve_triangular(L, x, lower=True))



def _parse_component_i_for_g(i, EX, CovX,
                             Sigma_Inv, Pi, A,
                             K, R, N, obj):

    E_Vi = g_Eflowk_rep(obj, i, EX)
    #Cov_Vi = _get_Vi_cov(CovX, i, A, K, R, N)
    Cov_Vi = g_Eflowk_rep_cov(obj, i, CovX)
    
    Cov_Vi_Xi = [sum(a[i, j]*CovX[j*N:(j+1)*N, i*N:(i+1)*N] for j in range(K))
                  for a in A[1:]]
    Cov_Vi_Mi = [np.dot(cvx, Pi) for cvx in Cov_Vi_Xi]
    
    inv_covar = np.row_stack((
        np.column_stack(
#        ((np.outer(E_Vi[s], E_Vi[t]))*Sigma_Inv
        ((Cov_Vi[(s,t)] + np.outer(E_Vi[s], E_Vi[t]))*Sigma_Inv
         for t in range(1, R+1))
        ) for s in range(1, R+1)))

    E_ViT_Sinv_v0 = np.concatenate(
        [E_diagx_M_y(E_Vi[s], E_Vi[0], Cov_Vi[(s, 0)], Sigma_Inv)
         for s in range(1, R+1)]
        )
    EX = EX.reshape(K, N)
    E_ViT_Sinv_Pixi = np.concatenate(
        [E_diagx_M_y(E_vs, np.dot(Pi, EX[i]), cvsmi, Sigma_Inv)
         for E_vs, cvsmi in zip(E_Vi[1:], Cov_Vi_Mi)]
        )

    try:
        mean = np.linalg.solve(inv_covar, E_ViT_Sinv_Pixi - E_ViT_Sinv_v0 )
    except:
        pinv = np.linalg.pinv(inv_covar)
        mean = np.dot(pinv, E_ViT_Sinv_Pixi - E_ViT_Sinv_v0 )
    
    return mean, inv_covar



#  p(x) ∝ Π N(x, means[k] | inv_covs[k])
def prod_norm_pars(means, inv_covs):
    m1 = means[0]
    C1inv = inv_covs[0]

    if len(means) == 1:
        return m1, np.linalg.inv(C1inv)

    else:

        for m2, C2inv in zip(means[1:], inv_covs[1:]):
            Cnew_inv = C1inv + C2inv
            mnew = np.linalg.solve(Cnew_inv,
                                   np.dot(C1inv, m1) + np.dot(C2inv, m2))
            m1 = mnew
            C1inv = Cnew_inv

        return mnew, np.linalg.inv(Cnew_inv)
