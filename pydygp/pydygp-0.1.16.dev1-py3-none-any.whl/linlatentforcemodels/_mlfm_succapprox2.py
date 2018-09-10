import numpy as np
import sklearn.gaussian_process.kernels as sklearn_kernels
import warnings
from .util import BlockCovar, back_sub
from pydygp import nssolve
from collections import namedtuple
from scipy.stats import multivariate_normal
from scipy.linalg import block_diag, cho_solve, cholesky
from scipy import sparse
from scipy.optimize import minimize, fmin_l_bfgs_b
from sklearn.gaussian_process import GaussianProcessRegressor


def mask_output(func):
    """Allows masking of a function returning a tuple.

    >>> @mask_output
    >>> def foo(*args, **kwargs):
    >>>     return ('a', 'b', 'c')
    >>> # returns ('a', 'c')
    >>> foo(mask=[False, True, False])

    """
    def function_wrapper(*args, **kwargs):
        mask = kwargs.pop('mask', None)
        res = func(*args, **kwargs)
        if mask is not None:
            res = tuple(item
                        for item, b in zip(res, mask) if not b)
        return res
    return function_wrapper

class SuccApproxLatentState(GaussianProcessRegressor):

    def __init__(self, *args, **kwargs):
        super(SuccApproxLatentState, self).__init__(*args, **kwargs)


class LatentForce(GaussianProcessRegressor):
    def __init__(self, *args, **kwargs):
        super(LatentForce, self).__init__(*args, **kwargs)


Dimensions = namedtuple('Dimensions', 'N K R')
FitResults = namedtuple('FitResults', 'g logpsi logphi dataprecisions loggamma')

class MLFMSuccApprox2:

    def __init__(self, struct_mats, order=1):
        self.order = order # no. of succ. approx. performed
        self.struct_mats = np.asarray(struct_mats)
        self.dim = Dimensions(None,
                              struct_mats[0].shape[0],
                              len(struct_mats)-1)

    def setup_latentstates(self, kernels=None, alpha=1e-5):
        if kernels is None:
            ls_kernels = []
            for k in range(self.dim.K):
                ls_kernels.append(sklearn_kernels.ConstantKernel(1.)*
                                  sklearn_kernels.RBF(1.))
            self.latentstates = [SuccApproxLatentState(kern, alpha=alpha)
                                 for kern in ls_kernels]

            # add a lone of kernel for optimisation
            for ls in self.latentstates:
                ls.kernel_ = ls.kernel.clone_with_theta(ls.kernel.theta)
        else:

            self.latentstates = [SuccApproxLatentState(kern, alpha=alpha)
                                 for kern in kernels]
            #raise NotImplementedError("User supplied kernels not currently supported.")

        

    def setup_latentforces(self, kernels=None, alpha=1e-5):
        if kernels is None:
            kernels = []
            for r in range(self.dim.R):
                kernels.append(sklearn_kernels.ConstantKernel(1.)*
                               sklearn_kernels.RBF(1.))

        if len(kernels) != self.dim.R:
            raise ValueError("number of kernels must equal the number of latent forces {}".format(self.dim.R))
        
        self.latentforces = [LatentForce(kern, alpha=alpha)
                             for kern in kernels]

        # add a clone of kernel for optimisation
        for lf in self.latentforces:
            lf.kernel_ = lf.kernel.clone_with_theta(lf.kernel.theta)

    def setup_dataprecisions(self, dataprecisions=None):
        self.dataprecisions = 1e4*np.ones(self.dim.K) \
                              if dataprecisions is None else dataprecisions

    def setup_times(self, data_times, h=None, min_width=None):
        """
        Sets up the intervals and handles the number of times in each intervals.
        """
        intervals = [nssolve.ns_util.Interval(ta, tb)
                     for ta, tb in zip(data_times[:-1], data_times[1:])]
        data_inds = [0]
        for I in intervals:
            I.set_quad_style(h=h, min_width=min_width)
            data_inds.append(data_inds[-1]+I.tt.size-1)

        self.data_times = data_times
        self.h = h
        
        self.intervals = intervals
        self.comp_times = nssolve.ns_util.get_times(self.intervals)
        self.data_inds = data_inds
        self.dim = Dimensions(self.comp_times.size, self.dim.K, self.dim.R)
        

    def setup_operator(self, ifix=None):
        """
        Setup for the successive approximation operator.
        """
        if ifix is None:
            ifix = len(self.intervals) // 2
        self.ifix = ifix
        self.t0 = self.intervals[ifix].ta

        # get the index of the point corresponding to
        # the fixed point of the initial condition
        self.t0_index = np.where(self.ttf == self.t0)[0][0]
        
        nsop = nssolve.QuadOperator(fp_ind=ifix,
                                    method='single_fp',
                                    intervals=self.intervals,
                                    K=self.dim.K,
                                    R=self.dim.R,
                                    struct_mats=self.struct_mats,
                                    is_x_vec=True)
        self.nsop = nsop

    def _setup(self, times, Y, ifix=None):
        """ Gets the model ready for fit functions to be called.
        """
        # initalise to defaults
        for attr in ['latentstates',
                     'latentforces',
                     'dataprecisions']:
            if not hasattr(self, attr):
                getattr(self, 'setup_'+attr)()

        # check if setup_times has already been called
        if not hasattr(self, 'intervals'):
            self.setup_times(times)
        if not hasattr(self, 'nsop'):
            self.setup_operator(ifix)

        if Y.shape[0] != self.data_times.size \
           or Y.shape[1] != self.dim.K:
            raise ValueError("Y must be of shape (n_data_times, n_features)")
        self.Y = Y
        self.vecy = Y.T.ravel()

        # on call fit clone the latent state and latent force kernels
        for gp in self.latentstates:
            gp.kernel_ = gp.kernel.clone_with_theta(gp.kernel.theta)
        for gp in self.latentforces:
            gp.kernel_ = gp.kernel.clone_with_theta(gp.kernel.theta)        

    def em_fit(self, times, Y, ifix=None, gtol=1e-3, max_nt=500,
               verbose=True, logpsi_is_fixed=False):

        # initalise to defaults
        for attr in ['latentstates',
                     'latentforces',
                     'dataprecisions']:
            if not hasattr(self, attr):
                getattr(self, 'setup_'+attr)()

        # check if setup_times has already been called
        if not hasattr(self, 'intervals'):
            self.setup_times(times)
        if not hasattr(self, 'nsop'):
            self.setup_operator(ifix)

        if Y.shape[0] != self.data_times.size \
           or Y.shape[1] != self.dim.K:
            raise ValueError("Y must be of shape (n_data_times, n_features)")
        self.Y = Y
        self.vecy = Y.T.ravel()

        # on call fit clone the latent state and latent force kernels
        for gp in self.latentstates:
            gp.kernel_ = gp.kernel.clone_with_theta(gp.kernel.theta)
        for gp in self.latentforces:
            gp.kernel_ = gp.kernel.clone_with_theta(gp.kernel.theta)

        emopt = EMopt_MLFMSuccApprox(self)
        
        g = emopt(logpsi_is_fixed=logpsi_is_fixed,
                  max_nt=max_nt, verbose=verbose)
        return g
        

    def loglikelihood(self, y, g, Gamma, Sigma):
        """
        Returns the model log-likelihood

        Parameters
        ----------
        y : array, shape (N_data*K, )
            Vectorisation of the observed data.
        
        """
        K = sparse.csr_matrix(self.nsop.x_transform(g, is_x_input_vec=True))

        x_chols = _handle_covar(_get_latentstate_theta(self),
                                self.ttf, self.latentstates,
                                _get_latentstate_theta_shape(self))
        cov = block_diag(*[L.dot(L.T) for L in x_chols])

        for M in range(self.order):
            cov = K.dot(K.dot(cov).T) + Gamma
        D = self.sparse_data_map
        cov = D.dot(D.dot(cov).T) + Sigma

        g_chols = _handle_covar(_get_latentforce_theta(self),
                                self.ttf, self.latentforces,
                                _get_latentforce_theta_shape(self))

        g = g.reshape(self.dim.R, self.dim.N)
        lpg = -0.5*sum([gr.dot(back_sub(L, gr))
                         for gr, L in zip(g, g_chols)])
        lpg -= sum(np.log(np.diag(L)).sum() for L in g_chols)

        """
        gCovs = [L.dot(L.T) for L in g_chols]
        
        lpg = sum(multivariate_normal.logpdf(gr,
                                             np.zeros(gr.size),
                                             Cr)
                  for gr, Cr in zip(g, gCovs))
        """

        lpy_g = multivariate_normal.logpdf(y, np.zeros(y.size), cov)

        return lpy_g + lpg

    @mask_output
    def foo(self, g, logpsi, logphi, loggamma, sigmas, eval_gradient=False, **kwargs):
        return log_likelihood(self.vecy, g, logpsi, logphi, sigmas, loggamma, self, eval_gradient, **kwargs)

    def foo2(self, g, logphi, gamma, mlfm, eval_gradient):
        return _get_model_cov(g, logphi, gamma, mlfm, eval_gradient)

    def _foo2(self, g, logphi, gamma, eval_gradient):
        return _get_model_cov2(g, logphi, gamma, self, eval_gradient)

    def fit(self, times, y, g0=None):
        """MAP Fit of the Successive Approximations MLFM.

        Parameters
        ----------

        times : array-like, shape = (n_samples, )

        y : array-like, shape = (n_samples, n_output_dims)

        Returns
        -------
        self : returns an instance of self.
        """

        # default initalisation of essential variables
        for attr in ['latentstates',
                     'latentforces',
                     'dataprecisions']:
            if not hasattr(self, attr):
                getattr(self, 'setup_'+attr)()

        self.setup_times(times)
        self.setup_operator()


        if y.shape[0] != self.data_times.size \
           or y.shape[1] != self.dim.K:
            raise ValueError("Y must be of shape (n_data_times, n_output_dims")
        self.Y = y
        self.vecy = y.T.ravel()

        # shape of obj. function argument
        of_arg_shape = [self.dim.N*self.dim.R,
                        sum(_get_latentforce_theta_shape(self)),
                        sum(_get_latentstate_theta_shape(self))]

        # defaul noise and Gamma
        sigmas = 1 / np.sqrt(self.dataprecisions)
        Gamma = np.diag(1e-4*np.ones(self.dim.N*self.dim.K))


        # mask example
        mask = [False, True, False]

        def obj_func(arg ):
            g, logpsi, logphi = _unpack_vector(arg, of_arg_shape)
            tup = \
               self.foo(g, logpsi, logphi, sigmas, Gamma, eval_gradient=True)
            lgrad = np.concatenate(tup[1:])
            return -tup[0], -lgrad

        # inital value for optimisation
        if g0 is None:
            g0 = np.zeros(self.dim.R*self.dim.N)

        init = np.concatenate((g0, 
                               _get_latentforce_theta(self),
                               _get_latentstate_theta(self)))
        # modify init if masking variables
        
        res = minimize(obj_func, init, jac=True)

        # estimates
        g, logpsi, logphi = _unpack_vector(res.x, of_arg_shape)

        # add an optimised clone of the kernels
        logpsi = _unpack_vector(logpsi, _get_latentforce_theta_shape(self))
        for theta, gp in zip(logpsi, self.latentforces):
            gp.kernel_ = gp.kernel.clone_with_theta(theta)

        logphi = _unpack_vector(logphi, _get_latentstate_theta_shape(self))
        for theta, gp in zip(logphi, self.latentstates):
            gp.kernel_ = gp.kernel.clone_with_theta(theta)

        # also store the MAP estimate of the latent force
        self.g_ = g

        return self

    def fit2(self, times, y, g0=None, **kwargs):

        self._setup(times, y)
        
        # sort out any variables to be fixed
        is_fixed = []
        for attr in ['g', 'logpsi', 'logphi', 'loggamma']:
            try:
                is_fixed.append(kwargs.pop(attr + '_is_fixed'))
            except KeyError:
                is_fixed.append(False)
        if sum(is_fixed) == 0: is_fixed = None

        ## structural fixed variables
        sigmas = 1./ np.sqrt(self.dataprecisions)

        def objfunc(arg, arg_shape, fixed_vars):
            # unpack arg
            free_vars = _unpack_vector(arg, arg_shape)
            if is_fixed is not None:
                # ordered combination of free and fixed vars
                full_vars = []
                ifix = 0
                ifree = 0
                for boolean in is_fixed:
                    if not boolean:
                        full_vars.append(free_vars[ifree])
                        ifree += 1
                    else:
                        full_vars.append(fixed_vars[ifix])
                        ifix += 1
            else:
                full_vars = free_vars

            if is_fixed is None:
                mask = None
            else:
                mask = [False] + is_fixed

            try:
                res = self.foo(*full_vars, sigmas, eval_gradient=True,
                               mask=mask, **kwargs)
                grad = np.concatenate([item for item in res[1:]])
                return -res[0], -grad

            except:
                #previously caught linalg error only - but some of the kernels
                # throw weird errors    
                return np.inf, np.zeros(arg.size)

        if is_fixed is None:
            init, free_vars_shape, fixed_vars = \
                  self._fit_init(g0, is_fixed=None, **kwargs)
        else:
            init, free_vars_shape, fixed_vars = \
                  self._fit_init(g0, is_fixed=is_fixed, **kwargs)

        res = minimize(objfunc, init,
                       jac=True,
                       args=(free_vars_shape, fixed_vars),
                       options={'maxiter': 500,
                                'disp': kwargs.pop('disp', False)})
        self.fit_res = res

        # unpack the result vector for returning
        if is_fixed is None:
            g, logpsi, logphi, loggamma = _unpack_vector(res.x, free_vars_shape)
        else:
            g, logpsi, logphi, loggamma = _unpack_fit_result(res.x,
                                                             free_vars_shape,
                                                             is_fixed,
                                                             fixed_vars)
        g = g.reshape(self.dim.R, self.dim.N)
        logpsi = _unpack_vector(logpsi, _get_latentforce_theta_shape(self))
        logphi = _unpack_vector(logphi, _get_latentstate_theta_shape(self))
        ttf = self.ttf
        dataprecisions = self.dataprecisions


        fit_result = FitResults(g, logpsi, logphi, dataprecisions, loggamma)
        
        return fit_result

    def _fit_init(self, g0=None, is_fixed=None, **kwargs):
        """ Handles initalisation of fit.
        """
        if g0 is None: g0 = np.zeros(self.dim.R*self.dim.N)

        # look for additional initial variables
        try:
            logpsi0 = kwargs['logpsi0']
        except KeyError:
            logpsi0 = _get_latentforce_theta(self)

        try:
            logphi0 = kwargs['logphi0']
        except KeyError:
            logphi0 = _get_latentstate_theta(self)

        try:
            loggamma0 = kwargs['loggamma0']
        except KeyError:
            loggamma0 = np.log(1e-4*np.ones(self.dim.K))

        full_init = [g0,
                     logpsi0,
                     logphi0,
                     loggamma0]
        
        if is_fixed is None:
            free_vars_shape = [item.size for item in full_init]
            return np.concatenate(full_init), free_vars_shape, None

        else:
            full_init_shape = [item.size for item in full_init]
            free_vars = []
            fixed_vars = []
            for item, boolean in zip(full_init, is_fixed):
                if boolean:
                    fixed_vars.append(item)
                else:
                    free_vars.append(item)
            free_vars_shape = [item.size for item in free_vars]
            return np.concatenate(free_vars), free_vars_shape, fixed_vars

    @property
    def ttf(self):
        return self.comp_times

    @property
    def data_map(self):
        """
        """
        data_map = np.row_stack((np.eye(N=1, M=self.dim.N, k=i)
                                 for i in self.data_inds))
        data_map = block_diag(*[data_map]*self.dim.K)
        return data_map

    @property
    def sparse_data_map(self):
        """
        Sparse representation of the linear transformation y = Dx_N
        """
        try:
            return self._s_data_map
        except:
            D = self.data_map
            self._s_data_map = sparse.coo_matrix(D)
            return self._s_data_map

    @property
    def sparse_vecK_aff_rep(self):
        """
        sparse pair A, b such that vec(K[g]) = Avec(g) + b
        """
        try:
            return self._vecK_aff_rep
        except:
            ncomp = self.comp_times.size * self.dim.R
            K0 = self.nsop.x_transform(np.zeros(ncomp), is_x_input_vec=True)

            Kgrad = [sparse.csr_matrix(
                (
                self.nsop.x_transform(np.eye(N=1, M=ncomp, k=i).ravel(),
                                      is_x_input_vec=True)
                - K0).T.ravel()[:, None]
                )
                 for i in range(ncomp)]
            Kgrad = sparse.hstack(Kgrad)
            
            self._vecK_aff_rep = Kgrad, \
                                 sparse.coo_matrix(K0.T.ravel())

            return self._vecK_aff_rep

    @property
    def sparse_vecK_aff_rep_Acols_sq(self):
        try:
            return self._vecK_aff_rep_Acols_sq
        except:
            
            A, _  = self.sparse_vecK_aff_rep
            nk = self.dim.N*self.dim.K
            A = A.tocsr()
            Acol_sq = [
                sparse.hstack([A[i*nk:(i+1)*nk, r] for i in range(nk)])
                for r in range(self.dim.N*self.dim.R)]
            self._vecK_aff_rep_Acols_sq = Acol_sq

            return self._vecK_aff_rep_Acols_sq

    def clone(self):
        """Returns a copy of the MLFM object.

        Parameters
        ----------

        self : MLFMSuccApprox2 object
        """
        obj = MLFMSuccApprox2(self.struct_mats, self.order)

        ls_kernels = [gp.kernel for gp in self.latentstates]
        obj.setup_latentstates(ls_kernels)

        lf_kernels = [gp.kernel for gp in self.latentforces]
        obj.setup_latentforces(lf_kernels)

        obj.setup_times(self.data_times, self.h)
        obj.setup_operator(self.ifix)

        try:
            obj.setup_dataprecisions(self.dataprecisions)
        except:
            obj.setup_dataprecisions()

        return obj
        


class EMopt_MLFMSuccApprox:
    def __init__(self, mlfm):
        self.mlfm = mlfm

    def __call__(self, logpsi_is_fixed=False, max_nt=500, verbose=False):
        mlfm = self.mlfm  # succinct name
        
        # initalise variables
        sigmas = 1 / np.sqrt(mlfm.dataprecisions)
        Sigma = np.diag(np.concatenate([s**2*np.ones(mlfm.data_times.size)
                                        for s in sigmas]))

        gamma = 1e-4*np.ones(mlfm.dim.K)
        loggamma = np.log(gamma)
        Gamma = np.kron(np.diag(gamma), np.eye(mlfm.dim.N))
        logphi = _get_latentstate_theta(mlfm)  
        logpsi = _get_latentforce_theta(mlfm)

        # initalise p(X)
        Ex, Varx, pwCovx = self._Estep_init()

        # first estimate of g
        gdelt = np.inf
        ell = -np.inf

        nt = 0
        g = np.zeros(mlfm.dim.N*mlfm.dim.R)

        while True:

            _g = self.Mstep(Ex, Varx, pwCovx, Gamma, Sigma, logpsi)

            # update the latent force hyperparameters
            # if the force isn't moving too much
            #if nt > 15:
            #    logphi = self.latentstate_hyperpar_update(logphi, Ex[0], Varx[0])
            #    self.latentforce_hyperpar_update(g)
            #   logpsi = _get_latentforce_theta(mlfm)                

            Ex, Varx, pwCovx = self.Estep_LDS(_g.ravel(), Gamma, Sigma, logphi)
            #if nt > 0:
            #    gdelt = np.max(abs(g - _g))
            #    if gdelt < 1e-3:
            #        break

            gdelt = max(np.abs(g - _g))
            g = _g

            if nt >= max_nt:
                if verbose: print("Maximum number of iterations reached.")
                break

            _ell = log_likelihood(mlfm.vecy, g, logpsi, logphi, sigmas, loggamma, mlfm)
            elldelt = _ell - ell
            ell = _ell
            if verbose: print("{} : {}, {}".format(nt, ell, elldelt))

            assert(elldelt > 0)
            if elldelt < 1e-3 and nt > 0:
                break

            nt += 1

        return g, logpsi, logphi


    def _Estep_init(self, scale=1e-1):
        """
        Initalise the distribution of the latent variables
        """
        Y = self.mlfm.vecy.reshape((self.mlfm.dim.K, self.mlfm.data_times.size))
        xinterp = []
        for yk in Y:
            xinterp.append(np.interp(self.mlfm.ttf, self.mlfm.data_times, yk))
        xinterp = np.concatenate(xinterp)

        Ex = [xinterp]*self.mlfm.order
        Varx = [np.diag(np.ones(xinterp.size)*scale)]*self.mlfm.order
        pwCovx = [np.zeros((xinterp.size, xinterp.size))]*(self.mlfm.order-1)

        return Ex, Varx, pwCovx


    def Estep_LDS(self, g, Gamma, Sigma, logphi):
        """
        Computes the Estep using the Kalman filter forward/backwards recursion
        """
        mlfm = self.mlfm
        order = mlfm.order
        NK = mlfm.dim.N*mlfm.dim.K

        # LDS
        #
        # Notation used is as in Bishop PRML
        A = sparse.coo_matrix(mlfm.nsop.x_transform(g, is_x_input_vec=True))
        At = A.transpose()
        C = mlfm.sparse_data_map.dot(A)
        x = mlfm.vecy
        sparse_Gamma = sparse.coo_matrix(Gamma)

        # integrating out the final latent state so update transmission
        # covar

        # YM = DxM + e = D[KxM-1 + e_G] + ee
        D = mlfm.sparse_data_map
        SigmaY = Sigma + D.dot(D.dot(Gamma).T)

        # Cholesky decomposition of x0
        xcov_chol_ls = _handle_covar(logphi,
                                     mlfm.ttf,
                                     mlfm.latentstates,
                                     _get_latentstate_theta_shape(mlfm))

        ################
        # Forward pass #
        ################
        f_means = []
        f_covs = []
        
        for m in range(order):
            if m == 0:
                f_means.append(np.zeros(NK))
                f_covs.append(block_diag(*[L.dot(L.T)
                                           for L in xcov_chol_ls]))

            elif m < order-1:
                new_mean = A.dot(f_means[-1])
                new_cov = P
                f_means.append(new_mean)
                f_covs.append(new_cov)

            else:
                # make the Kalman gain matrix
                S = C.dot(P.dot(C.todense().T)) + SigmaY
                S_chol = np.linalg.cholesky(S)
                K = P.dot(cho_solve((S_chol, True), C.todense()).T)
                
                Amu = A.dot(f_means[-1])

                new_mean = Amu + K.dot(x- C.dot(Amu))
                new_cov = (np.eye(NK) - K.dot(C.todense())).dot(P)

                f_means.append(new_mean)
                f_covs.append(new_cov)

            # make Pn-1 matrix
            P = A.dot(A.dot(f_covs[-1]).T) + Gamma

        #################
        # Backward Pass #
        #################
        means = []
        covs = []
        pwcovs = []

        for m in range(order):
            if m == 0:
                means.append(f_means[-1])
                covs.append(f_covs[-1])

            else:
                mn = f_means[-(m+1)]
                Vn = f_covs[-(m+1)]

                Pn = A.dot(A.dot(Vn).T) + Gamma
                Pninv = np.linalg.inv(Pn)

                Jn = Vn.dot(At.dot(Pninv))

                means.insert(0, mn + Jn.dot(means[0] - A.dot(mn)))
                covs.insert(0, Vn + Jn.dot((covs[0] - Pn).dot(Jn.T)))

                pwcovs.insert(0, Jn.dot(covs[1]))

        return [np.asarray(item) for item in means], \
               [np.asarray(item) for item in covs], \
               [np.asarray(item) for item in pwcovs]

    def Mstep_objfunc(self, g, Ex, Varx, pwCovx, Gamma, Sigma, logpsi):
        K = self.mlfm.nsop.x_transform(g, is_x_input_vec=True)

        EzzTs = [c + np.outer(m, m) for m, c in zip(Ex, Varx)]
        EzzpTs = [pwCovx[i] + np.outer(m1, m2)
                  for i, (m1, m2) in enumerate(zip(Ex[:-1], Ex[1:]))]

        D = self.mlfm.sparse_data_map
        InvGamma = np.linalg.inv(Gamma)

        yCovar = Sigma + D.dot(D.dot(Gamma).T)
        yCovar_chol = np.linalg.cholesky(yCovar)

        y = self.mlfm.vecy

        expr1 = np.trace(sum(EzzTs[:-1]).dot(K.T.dot(InvGamma).dot(K)))
        expr2 = -2*np.trace(sum(EzzpTs).dot(InvGamma.dot(K)))

        expr3 = D.T.dot(back_sub(yCovar_chol, D.todense()))
        expr3 = EzzTs[-1].dot(expr3)
        expr3 = np.trace(expr3)

        expr4 = -2*y.dot(back_sub(yCovar_chol, D.dot(K.dot(Ex[-1]))))

        gprior_chols = _handle_covar(logpsi, self.mlfm.ttf,
                                     self.mlfm.latentforces,
                                     _get_latentforce_theta_shape(self.mlfm))

        expr5 = sum(gr.dot(back_sub(L, gr))
                    for gr, L in zip(g.reshape(self.mlfm.dim.R,
                                               self.mlfm.dim.N), gprior_chols))

        return -.5*(expr1 + expr2 + expr3 + expr4 + expr5)

    def Mstep(self, Ex, Varx, pwCovx, Gamma, Sigma, logpsi):
        # map from augmented time set to data
        D = self.mlfm.sparse_data_map
        # invert Gamma
        InvGamma = np.linalg.inv(Gamma)  # easier if Gamma is diagonal

        # emission cov of data given X_{M-1}
        yCovar = Sigma + D.dot(D.dot(Gamma).T)
        yCovar_chol = np.linalg.cholesky(yCovar)

        # data
        y = self.mlfm.vecy
        # yCovar^{-1}.dot(y)
        #LMy = cho_solve((yCovar_chol, True), y)
        LMy = back_sub(yCovar_chol, y)
        DtLMD = D.transpose().dot(cho_solve((yCovar_chol, True), D.todense()))

        EzzTs = [c + np.outer(m, m) for m, c in zip(Ex, Varx)]
        EzzpTs = [pwCovx[i] + np.outer(m1, m2)
                  for i, (m1, m2) in enumerate(zip(Ex[:-1], Ex[1:]))]

        invcov = sparse.kron(EzzTs[-1], DtLMD)
        if self.mlfm.order > 1:
            invcov += sparse.kron(sum(EzzTs[:-1]), InvGamma)

        # E[z_{M-1}^T] (x) D
        mt_x_D = sparse.kron(Ex[-1][None, :], D)
        # construct the pre mean
        pre_mean = mt_x_D.transpose().dot(LMy)
        if self.mlfm.order > 1:
            pre_mean += InvGamma.dot(sum(EzzpTs)).ravel()

        # sparse representation of K transform.
        P, p = self.mlfm.sparse_vecK_aff_rep
        Pt = P.transpose()
        
        pre_mean -= p.dot(invcov)
        pre_mean = Pt.dot(pre_mean.T)

        invcov = Pt.dot(Pt.dot(invcov).T)

        # get the prior inv. covariance
        gprior_chols = _handle_covar(logpsi, self.mlfm.ttf,
                                     self.mlfm.latentforces,
                                     _get_latentforce_theta_shape(self.mlfm))
        gpriorinv = block_diag(*[cho_solve((L, True), np.eye(self.mlfm.dim.N))
                                 for L in gprior_chols])

        invcov += gpriorinv
        
        gmean = np.linalg.solve(invcov, pre_mean)
        return np.squeeze(np.asarray(gmean))

    def latentforce_hyperpar_update(self, g):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            g = g.reshape(self.mlfm.dim.R, self.mlfm.dim.N)
            for r, lf in enumerate(self.mlfm.latentforces):
                lf.fit(self.mlfm.ttf[:, None], g[r, :])
                # will force the update to be started from
                # current opt.
                lf.kernel = lf.kernel_  


    def latentstate_hyperpar_update(self, logphi, Ex0, Varx0):
        N = self.mlfm.dim.N
        Ex0 = Ex0.reshape(self.mlfm.dim.K, N)
        ExxT_list = [np.outer(exk, exk) + Varx0[k*N:(k+1)*N,
                                               k*N:(k+1)*N]
                     for k, exk in enumerate(Ex0)]

        tt = self.mlfm.ttf


        def _objfunc(logphik, k, eval_gradient=False):
            try:
                kernel = self.mlfm.latentstates[k].kernel.clone_with_theta(logphik)
                C, C_gradient = kernel(tt[:, None], eval_gradient=True)
                C[np.diag_indices_from(C)] += self.mlfm.latentstates[k].alpha

                C_chol = np.linalg.cholesky(C)

                logdet = -2*np.log(np.diag(C_chol)).sum()


                ell = -.5*np.trace(back_sub(C_chol, ExxT_list[k])) \
                      +.5*logdet
                if eval_gradient:
                    grad = []
                    Cinv = np.linalg.inv(C)
                    for i in range(logphik.size):
                        Cinv_C_gradient = back_sub(C_chol, C_gradient[..., i])               
                        expr1 = back_sub(C_chol, ExxT_list[k])
                        expr1 = expr1.dot(Cinv_C_gradient)

                        grad.append(.5*np.trace(expr1) - .5*np.trace(Cinv_C_gradient))

                    return -ell, -np.array(grad)

                else:
                    return -ell
            except:
                if eval_gradient:
                    return np.inf, np.zeros(logphik.size)
                else:
                    return np.inf


        # reshape current logphi
        logphi = _unpack_vector(logphi, _get_latentstate_theta_shape(self.mlfm))

        res = []
        for k, lpk in enumerate(logphi):

            theta_opt, func_min, convergence_dict = \
                       fmin_l_bfgs_b(_objfunc, lpk,
                                     args=(k, True),
                                     bounds=self.mlfm.latentstates[k].kernel_.bounds)
            res.append(theta_opt)
            #lf = self.mlfm.latentstates[k]
            #lf.kernel_ = lf.kernel.clone_with_theta(theta_opt)
        return np.concatenate(res)

    def dataprecisions_update(self, g, Gamma, Ex, Varx):
        """
        (Conditional) EM optimisation of the data observation noise.
        """
        D = self.mlfm.sparse_data_map
        A = self.mlfm.nsop.x_transform(g, is_x_input_vec)
        DA = D.dot(A)
        # noise independent part of the data covariance matrix
        C0 = D.dot(D.dot(Gamma).T)

        # z := DAx
        Ez = D.dot(A.dot(Ex))
        Varz = DA.dot(Varx.dot(DA.T))
        EzzT = Varz + np.outer(Ez, Ez)

        def _objfunc(ssq, eval_gradient=False):
            K = C0 + np.kron(np.diag(ssq), np.eye(self.mlfm.dim.N))
            L = np.linalg.cholesky(K)

            if eval_gradient:
                K_gradient = np.dstack(( \
                    np.kron(np.eye(N=1, M=self.mlfm.dim.K, k=k).ravel(),
                            np.eye(self.mlfm.dim.N))
                    for k in range(self.mlfm.dim.K)))

                # K^{-1} EzzT K^{-1}
                tmp = cho_solve((L, True), EzzT)
                tmp = cho_solve((L, True), tmp.T)
                tmp -= cho_solve((L, True), np.eye(K.shape[0]))

                #log_likelihood_gradient = .5 * np.einsum(


"""
Likelihood functions
"""

def _get_model_cov(g, logphi, gamma, mlfm, eval_gradient=False, K=None):
    # [!] method is still slow with eval_gradient
    # it is the computational bottleneck

    # g depdent transformation matrix
    #K = mlfm.nsop.x_transform(g, is_x_input_vec=True)

    # optional passing of the matrix K(g)
    nk = mlfm.dim.N*mlfm.dim.K

    if K is None:
        K, k = mlfm.sparse_vecK_aff_rep
        K = K.dot(sparse.csc_matrix(g[:, None])) + k.transpose()
        K = sparse.hstack([K[i*nk:(i+1)*nk, 0] for i in range(nk)])
    # important so the coo -> csr conversion doesn't
    # keep happening in the loop
    K = K.tocsr()  

    # sparse repr. of vec(K) = Ag + b
    # take A cols and turn the columns into sparse matrices    
    Acol_sq = mlfm.sparse_vecK_aff_rep_Acols_sq        

    logphi = _unpack_vector(logphi, _get_latentstate_theta_shape(mlfm))

    kernels = [ls.kernel.clone_with_theta(theta)
               for ls, theta in zip(mlfm.latentstates, logphi)]

    # Gamma = diag(gamma) (x) I
    Gamma = np.kron(np.diag(gamma), np.eye(mlfm.dim.N))

    if eval_gradient:
        # the gradient of the initial smooth approximation
        # wrt to the latent state hyperparameters        
        cov = []
        cov_logphi_gradient = []
        cov_gamma_gradient = []

        for k, kern in enumerate(kernels):
            covk, covk_grad = kern(mlfm.ttf[:, None], eval_gradient=True)
            covk[np.diag_indices_from(covk)] += mlfm.latentstates[k].alpha
            cov.append(covk)

            # pad the k gradient
            ek = np.eye(N=1, M=mlfm.dim.K, k=k).ravel()
            tmp = np.dstack((
                np.kron(np.diag(ek),
                        covk_grad[..., d]) for d in range(covk_grad.shape[-1])))
            cov_logphi_gradient.append(tmp)

        cov = block_diag(*cov)
        cov_logphi_gradient = np.dstack((cov_logphi_gradient))
        cov_gamma_gradient = np.zeros((cov.shape[0], cov.shape[0], mlfm.dim.K))

    else:
        cov = block_diag(*[kern(mlfm.ttf[:, None]) + gp.alpha*np.eye(mlfm.dim.N)
                           for kern, gp in zip(kernels, mlfm.latentstates)])

    # recursively construct the covariance matrix and (optionally)
    # its gradient
    for m in range(mlfm.order):
        KCt = K.dot(cov).T

        if eval_gradient:
            if m == 0:
                cov_g_gradient = [K.dot(A.dot(cov).T) + \
                                  A.dot(K.dot(cov).T)
                                  for A in Acol_sq]
            else:

                cov_g_gradient = [K.dot(K.dot(cov_g_gradient[r]).T + \
                                        Acol_sq[r].dot(cov).T) + \
                                  Acol_sq[r].dot(KCt)
                                  for r in range(g.size)]

            # gradient with respect to latentstate hyperparameters
            cov_logphi_gradient = np.dstack((
                K.dot(K.dot(cov_logphi_gradient[..., i]).T)
                for i in range(cov_logphi_gradient.shape[-1])
                ))

            # gradient with respect to gamma variables
            cov_gamma_gradient = np.dstack((
                K.dot(K.dot(cov_gamma_gradient[..., i]).T)
                for i in range(cov_gamma_gradient.shape[-1])
                ))
            for i in range(cov_gamma_gradient.shape[-1]):
                cov_gamma_gradient[i*mlfm.dim.N:(i+1)*mlfm.dim.N,
                                   i*mlfm.dim.N:(i+1)*mlfm.dim.N, i] += np.eye(mlfm.dim.N)
        # update cov
        cov = K.dot(KCt) + Gamma

    if eval_gradient:
        cov_g_gradient = np.dstack(cov_g_gradient)

    if eval_gradient:
        return (cov, cov_g_gradient, cov_logphi_gradient, cov_gamma_gradient)
    else:
        return cov

def _get_model_cov2(g, logphi, gamma, mlfm, eval_gradient=False):
    order = mlfm.order    
    nk = mlfm.dim.N*mlfm.dim.K

    A, b = mlfm.sparse_vecK_aff_rep
    K = A.dot(sparse.csc_matrix(g[:, None])) + b.transpose()
    K = sparse.hstack([K[i*nk:(i+1)*nk, 0] for i in range(nk)])

    # sparse repr. of vec(K) = Ag + b
    # take A cols and turn the columns into sparse matrices
    #Acol_sq = mlfm.sparse_vecK_aff_rep_Acols_sq        

    Kpowers = [K]

    if eval_gradient:
        # gradients of [dK^m / dg]
        Arr = A.toarray().reshape(nk, nk, A.shape[-1])
        Arr = np.moveaxis(Arr, -1, 0)

        # view of Arr with Arr[i, :, :].transpose()
        Arrt = np.moveaxis(Arr, 1, -1)
        dKpowers = [Arrt]

    for m in range(order - 1):
        if eval_gradient:
            r1 = naive_sps_x_dense_arr(K, dKpowers[-1])
            r2 = naive_sps_x_dense_arr(Kpowers[-1].transpose(),
                                       Arr)
            r = r1 + np.moveaxis(r2, 1, -1)
            dKpowers.append(r)
        Kpowers.append(K.dot(Kpowers[-1]))

    # make C0
    logphi = _unpack_vector(logphi, _get_latentstate_theta_shape(mlfm))
    kernels = [ls.kernel.clone_with_theta(theta)
               for ls, theta in zip(mlfm.latentstates, logphi)]
    C0 = block_diag(*[kern(mlfm.ttf[:, None]) + gp.alpha*np.eye(mlfm.dim.N)
                       for kern, gp in zip(kernels, mlfm.latentstates)])

    # Gamma = diag(gamma) (x) I
    Gamma = np.kron(np.diag(gamma), np.eye(mlfm.dim.N))

    cov = Gamma.copy()
    if eval_gradient:
        cov_g_gradient = dKpowers[-1].dot(Kpowers[-1].dot(C0).T)
    
    for m in range(order - 1):
        mat = Kpowers[m].dot(Kpowers[m].dot(Gamma).T)
        cov += mat
        if eval_gradient:
            cov_g_gradient += dKpowers[m].dot(Kpowers[m].dot(Gamma).T)

    cov += Kpowers[-1].dot(Kpowers[-1].dot(C0).T)
    
    if eval_gradient:
        # add cov_g_gradient transpose
        cov_g_gradient += np.einsum('ijk->ikj', cov_g_gradient)
    
        # sklearn likes the axis to be like [..., r] for r in parameter size 
        cov_g_gradient = np.moveaxis(cov_g_gradient, 0, -1)

        return cov, cov_g_gradient

    else:
        return cov



def latentforce_prior_loglikelihood(g, logpsi, mlfm, eval_gradient=False):
    # reshape vec(g)
    g = g.reshape(mlfm.dim.R, mlfm.dim.N)
    
    logpsi = _unpack_vector(logpsi, _get_latentforce_theta_shape(mlfm))
    kernels = [lf.kernel.clone_with_theta(theta)
               for lf, theta in zip(mlfm.latentforces, logpsi)]

    # variables to be returned
    ell, ell_g_grad, ell_logpsi_grad = (0., [], [])

    # independent priors with distinct hyperparameters so loop and sum/append
    for r, kern in enumerate(kernels):
        if eval_gradient:
            K, K_gradient = kern(mlfm.ttf[:, None], eval_gradient=True)
        else:
            K = kern(mlfm.ttf[:, None])

        # add jitter term to K
        K[np.diag_indices_from(K)] += mlfm.latentforces[r].alpha
        # attempt to form the cholesky decomposition
        try:
            L = cholesky(K, lower=True)

            # using the sklearn naming convention
            y_train = g[r, :]
            # alpha = np.linalg.inv(K).dot(y_train)
            alpha = cho_solve((L, True), y_train)

            # compute log likelihood of force r
            ell_r = -.5 * y_train.dot(alpha)
            ell_r -= np.log(np.diag(L)).sum()
            ell_r -= K.shape[0] / 2 * np.log(2 * np.pi)

            if eval_gradient:
                # Kinv yy^T KinvT
                tmp = np.outer(alpha, alpha)
                tmp -= cho_solve((L, True), np.eye(K.shape[0]))
                # Computes .5 * trace(tmp.dot(K_gradient))
                ell_r_logpsi_grad = .5 * np.einsum("ij,jik", tmp, K_gradient)

                # gradient wrt to g
                ell_r_g_grad = -alpha
            
        except np.linalg.LinAlgError:
            if eval_gradient:
                ell_r, ell_r_g_grad, ell_r_logpsi_grad = \
                       -np.inf, np.zeros(mlfm.dim.N), np.zeros(logpsi[r].size)
            else: ell_r = np.inf

        ell += ell_r
        if eval_gradient:
            ell_g_grad = np.concatenate((ell_g_grad, ell_r_g_grad))
            ell_logpsi_grad = np.concatenate((ell_logpsi_grad, ell_r_logpsi_grad))

    if eval_gradient:
        return ell, ell_g_grad, ell_logpsi_grad

    else:
        return ell
    
def log_likelihood(y, g, logpsi, logphi, sigmas, loggamma, mlfm,
                   eval_gradient=False,
                   include_prior=True,
                   include_logpsi_prior=False, **kwargs):
    # get the model dependent covariance matrix and
    # optionally its gradient
    gamma = np.exp(loggamma)
    
    if eval_gradient:
        model_cov, model_cov_g_grad, model_cov_logphi_grad, model_cov_gamma_grad = \
                   _get_model_cov(g, logphi, gamma, mlfm, eval_gradient=True)

        if include_prior:
            lg_prior, lg_prior_g_grad, lg_prior_logpsi_grad = \
                      latentforce_prior_loglikelihood(g, logpsi, mlfm, eval_gradient=True)
            
            if include_logpsi_prior:
                ### also add the latent force hyperparameter hyperameter contributions
                try:
                    logpsi_prior, logpsi_prior_grad = kwargs['logpsi_logpriorpdf'](logpsi)
                    lg_prior += logpsi_prior
                    lg_prior_logpsi_grad += logpsi_prior_grad
                except:
                    pass
        
        else:
            lg_prior, lg_prior_g_grad, lg_prior_logpsi_grad = (0., 0., 0.)

    else:
        # the data/model loglikelihood term is a mean zero Gaussian process
        model_cov = _get_model_cov(g, logphi, gamma, mlfm)

        # log prior contribution of latent force + hyperparameters
        if include_prior:
            lg_prior = latentforce_prior_loglikelihood(g, logpsi, mlfm)
        else:
            lg_prior = 0.

    # form data covariance matrix from obs. sds
    Sigma = block_diag(np.concatenate([sk**2*np.ones(mlfm.data_times.size)
                                       for sk in sigmas]))

    # augmented dataset has to be transformed
    # to only those with observations
    D = mlfm.sparse_data_map
    model_cov = D.dot(D.dot(model_cov).T) + Sigma
    y_train = mlfm.vecy

    try:
        L = cholesky(model_cov, lower=True)
        alpha = cho_solve((L, True), y_train)

        log_lik = -.5 * y_train.dot(alpha)
        log_lik -= np.log(np.diag(L)).sum()
        log_lik -= model_cov.shape[0] / 2 * np.log(2 * np.pi)

        if eval_gradient:
            # The model_cov gradients need to be pre and post
            # multiplied by the sparse data map
            model_cov_g_grad = np.dstack((
                D.dot(D.dot(model_cov_g_grad[..., r]).T)
                for r in range(model_cov_g_grad.shape[-1])))
            model_cov_logphi_grad = np.dstack((
                D.dot(D.dot(model_cov_logphi_grad[..., r]).T)
                for r in range(model_cov_logphi_grad.shape[-1])))
            model_cov_gamma_grad = np.dstack((
                D.dot(D.dot(model_cov_gamma_grad[..., r]).T)
                for r in range(model_cov_gamma_grad.shape[-1])))

            tmp = np.outer(alpha, alpha)
            tmp -= cho_solve((L, True), np.eye(model_cov.shape[0]))

            log_lik_g_grad = .5 * np.einsum("ij,jik", tmp, model_cov_g_grad)
            log_lik_logphi_grad = .5 * np.einsum("ij,jik", tmp, model_cov_logphi_grad)


            log_lik_gamma_grad = .5 * np.einsum("ij,jik", tmp, model_cov_gamma_grad)
            log_lik_loggamma_grad = log_lik_gamma_grad * gamma

            # type consistency
            if isinstance(lg_prior_logpsi_grad, float):
                lg_prior_logpsi_grad = np.array([lg_prior_logpsi_grad])

            return log_lik + lg_prior, \
                   log_lik_g_grad + lg_prior_g_grad, \
                   lg_prior_logpsi_grad, \
                   log_lik_logphi_grad, \
                   log_lik_loggamma_grad

        else:
            return log_lik + lg_prior
        
    # Cholesky decomposition failed
    except np.linalg.LinAlgError:
        return (-np.inf, np.zeros(g.size), \
                np.zeros(logpsi.size),\
                np.zeros(logphi.size), \
                np.zeros(loggamma.size)) \
               if eval_gradient else -np.inf


class VarMLFMSuccApprox:

    def __init__(self, mlfm):

        # check to see if the hyperparameters of the MLFM have been fitted
        for gp in mlfm.latentforces:
            if not hasattr(gp, 'kernel_'):
                gp.kernel_ = gp.kernel.clone_with_theta(gp.kernel.theta)
        for gp in mlfm.latentstates:
            if not hasattr(gp, 'kernel_'):
                gp.kernel_ = gp.kernel.clone_with_theta(gp.kernel.theta)

        self.mlfm = mlfm

    def _var_lds_parameters(self, Eg, Covg, GammaInv):

        NK = self.mlfm.dim.N*self.mlfm.dim.K
        Eg = np.concatenate((Egr for Egr in Eg))
        Cg = Covg.full

        # vec(K) = A g + b
        A, b = self.mlfm.sparse_vecK_aff_rep

        K_row_means = [ A[n*NK:(n+1)*NK, :].dot(Eg) + b[n*NK:(n+1)*NK]
                        for n in range(NK) ]
        K_cov = np.zeros((NK, NK))
        for n in range(NK):
            An = A[n*NK:(n+1)*NK, :]
            km = K_row_means[m]
            for m in range(n+1):
                Amt = A[m*NK:(m+1)*NK, :].transpose()
                kn = K_row_means[n]
                K_cov[n, m] = (Amt.dot(Cg)*An.dot(GammaInv).T).sum() + km.dot(GammaInv.dot(kn))
                K_cov[m, n] = K_cov[n, m]

        
        #EK = np.row_stack((K_row_means))
"""
Utility retrieval functions
"""
def _unpack_vector(x, xk_shape):
    """
    Unpacks a vector into the len(xk_shape) sub vectors of
    size xk_shape[i], i=1,...,len(xk_shape)
    """
    ntot = 0
    res = []
    for nk in xk_shape:
        res.append(x[ntot:ntot + nk])
        ntot += nk
    return res

def _get_latentstate_theta(mlfmobj, fitted_kern=False):
    if fitted_kern:
        return np.concatenate([gp.kernel_.theta
                               for gp in mlfmobj.latentstates])
    else:
        return np.concatenate([gp.kernel.theta
                               for gp in mlfmobj.latentstates])        

def _get_latentstate_theta_shape(mlfmobj):
    """
    Gets a list of the size of the free kernel
    hyperparameters for each of latent states
    """
    return [gp.kernel.theta.size
            for gp in mlfmobj.latentstates]

def _get_latentforce_theta(mlfmobj, fitted_kern=False):
    if fitted_kern:
        return np.concatenate([gp.kernel_.theta
                               for gp in mlfmobj.latentforces])
    else:
        return np.concatenate([gp.kernel.theta
                               for gp in mlfmobj.latentforces])

def _get_latentforce_theta_shape(mlfmobj):
    """
    Gets a list of the size of the free kernel
    hyperparamers for each of the latent forces
    """
    return [gp.kernel.theta.size
            for gp in mlfmobj.latentforces]


def _handle_covar(theta, tt, gp_list, theta_shape):
    theta = _unpack_vector(theta, theta_shape)
    res = []
    for k, gp in enumerate(gp_list):
        kern = gp.kernel.clone_with_theta(theta[k])
        K = kern(tt[:, None]) + np.eye(tt.size)*gp.alpha
        res.append(np.linalg.cholesky(K))
    return res
                   

def _unpack_fit_result(arg, arg_shape, is_fixed, fixed_vars):
    free_vars = _unpack_vector(arg, arg_shape)
    full_vars = []
    ifix = 0
    ifree = 0
    for boolean in is_fixed:
        if not boolean:
            full_vars.append(free_vars[ifree])
            ifree += 1
        else:
            full_vars.append(fixed_vars[ifix])
            ifix += 1
    return tuple(full_vars)

# Chapeau https://stackoverflow.com/a/44461842/8828470
def kron_A_N(A, N):  # Simulates np.kron(A, np.eye(N))
    m,n = A.shape
    out = np.zeros((m,N,n,N),dtype=A.dtype)
    r = np.arange(N)
    out[:,r,:,r] = A
    out.shape = (m*N,n*N)
    return out


from scipy.sparse import coo_matrix


def reshape(a, shape):
    """Reshape the sparse matrix `a`.

    Returns a coo_matrix with shape `shape`.
    """
    if not hasattr(shape, '__len__') or len(shape) != 2:
        raise ValueError('`shape` must be a sequence of two integers')

    c = a.tocoo()
    nrows, ncols = c.shape
    size = nrows * ncols

    new_size =  shape[0] * shape[1]
    if new_size != size:
        raise ValueError('total size of new array must be unchanged')

    flat_indices = ncols * c.row + c.col
    new_row, new_col = divmod(flat_indices, shape[1])

    b = coo_matrix((c.data, (new_row, new_col)), shape=shape)
    return b


def naive_sps_x_dense_arr(sps_mat, dense_arr):
    """
    Computes the dot producet A.dot(dense_arr[i, ....])
    """
    rows, cols = sps_mat.shape
    P = dense_arr.shape[0]
    out = np.empty((P, rows, cols))
    for p in range(P):
        out[p, :, :] = sps_mat.dot(dense_arr[p,...])
    return out
