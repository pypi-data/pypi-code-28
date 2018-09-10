import numpy as np

import warnings

from pydygp.gradientkernels import RBF, ConstantKernel
import sklearn.gaussian_process.kernels as sklearn_kernels
from sklearn.gaussian_process import GaussianProcessRegressor

from .import matrixrv_util

from scipy.linalg import block_diag, solve_triangular, cho_solve
from scipy.optimize import minimize
from collections import namedtuple

from scipy.stats import multivariate_normal

def mask_output(func):
    """Allows masking of a function returning a tuple

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

def back_sub(L, x):
    return solve_triangular(L.T, solve_triangular(L, x, lower=True))

class BlockCovar:
    def __init__(self, blocks, n_features, n_samples):
        self.is_lower = True  # initalised using the lower blocks

        # dimension check: there should be n*(n + 1)/2 lower blocks
        assert(len(blocks) == n_features * (n_features + 1) // 2)
        self.blocks = blocks
        self.n_features = n_features
        self.n_samples = n_samples

    def __call__(self, i, j):
        # working in lower triangular
        if self.is_lower:
            if j <= i:
                ind = i*(i+1) // 2 + j
                return self.blocks[ind]
            else:
                return self.__call__(j, i).T
        else:
            raise NotImplementedError("BlockCovar must be in lower triangular form")
    
    @property
    def full(self):
        # returns the full covariance matrix
        return np.column_stack((
            np.row_stack((self.__call__(i, j)
                          for j in range(self.n_features)))
            for i in range(self.n_features)
            ))

    @classmethod
    def fromfull(cls, cov, n_features, n_samples):
        lowerblocks = []
        for i in range(n_features):
            for j in range(i+1):
                lowerblocks.append(cov[i*n_samples:(i+1)*n_samples,
                                       j*n_samples:(j+1)*n_samples])
        return BlockCovar(lowerblocks, n_features, n_samples)

class AdapGradLatentState(GaussianProcessRegressor):

    def __init__(self, kernel, alpha=1e-4):
        super(AdapGradLatentState, self).__init__(kernel=kernel,
                                                  alpha=alpha)
        #self.kernel = kernel  # must be a Gradient kernel (add check)
        #self.alpha = alpha    # small value to jitter cov. matrices

class LatentForce(GaussianProcessRegressor):

    def __init__(self, kernel, alpha=1e-5, **kwargs):
        super(LatentForce, self).__init__(kernel, alpha=alpha, **kwargs)

    def sim(self, tt):
        K = self.kernel(tt[:, None])
        K += np.diag(self.alpha*np.ones(tt.size))        
        L = np.linalg.cholesky(K) 
        return np.dot(L, np.random.normal(size=tt.size))

    """
    def log_likelihood(self, g, theta, eval_gradient=False):

        #Loglik and gradient of the log likelihood wrt to values and hyperpars
        #
        #Code is equivalent to that in sklearn
        
        kernel = self.kernel_.clone_with_theta(theta)

        if eval_gradient:
            K, K_gradient = kernel(self.X_train_, eval_gradient=True)
        else:
            K = kernel(self.X_train_)

        K[np.diag_indices_from(K)] += self.alpha
        try:
            L = cholesky(K, lower=True)
        except np.linalg.LinAlgError:
            return (-np.inf, np.zeros_like(g), np.zeros_like(theta)) \
                   if eval_gradient else -np.inf

        alpha = cho_solve((L, True), g)

        # Compute log-likelihood
        log_likelihood = -.5 * g.dot(alpha)
        log_likelihood -= np.log(np.diag(L)).sum()  #log|K|
        log_likelihood -= K.shape[0] / 2 * np.log(2*np.pi)

        if eval_gradient:
            tmp = np.outer(alpha, alpha)
            tmp -= cho_solve((L, True), np.eye(K.shape[0]))

            log_likelihood_hp_gradient = \
                                       .5 * np/
    """

Dimensions = namedtuple('Dimensions', 'N K R')
FitResults = namedtuple('FitResults', 'g logpsi logphi loggamma dataprecisions')
EMfitResults = namedtuple('EMfitResults',
                          'g logphi logpsi loggamma')

def _collect_results(g, logpsi, prevresult, append=False):
    pass

class BaseMLFM:
    """
    Base class for the multiplicative latent force model.
    """
    def __init__(self, struct_mats):
        self.struct_mats = np.asarray(struct_mats)        
        self.dim = Dimensions(None, struct_mats[0].shape[0], len(struct_mats)-1)

    def sim(self, x0, times, h):
        """
        Simulates a realisation of the mlfm
        """
        from scipy.interpolate import interp1d
        from scipy.integrate import odeint
        
        tt_dense, inds = _get_dense_times(times, h)
        lf_values = np.column_stack((lf.sim(tt_dense) for lf in self.latentforces))

        # build interpolants
        gp_interp = [interp1d(tt_dense, vals, fill_value='extrapolate')
                     for vals in lf_values.T]

        A = self.struct_mats
        dXdt = lambda x, t: np.dot(A[0] + sum(Ar*gr(t) for Ar, gr in zip(A[1:], gp_interp)), x)
        sol = odeint(dXdt, x0, tt_dense)
        

        return tt_dense, sol, inds, lf_values
        

class MLFMAdapGrad(BaseMLFM):

    def __init__(self, struct_mats):
        super(MLFMAdapGrad, self).__init__(struct_mats)

        self.is_precision_fixed=True
        self.is_tt_aug = False

    def setup_latentstates(self, kernels=None):
        if kernels is None:
            # Default is to for kernels 1.*exp(-(s-t)**2 / 1.**2)
            ls_kernels = []
            for k in range(self.dim.K):
                ls_kernels.append(ConstantKernel(1.)*RBF(1.))
            self.latentstates = [AdapGradLatentState(kern)
                                 for kern in ls_kernels]
        else:
            raise NotImplementedError("User supplied kernels not currently supported.")

    def setup_latentforces(self, kernels=None):
        if kernels is None:
            kernels = []
            for r in range(self.dim.R):
                kernels.append(sklearn_kernels.ConstantKernel(1.)*
                               sklearn_kernels.RBF(1.))

        if len(kernels) != self.dim.R:
            raise ValueError("number of kernels must equal the number of latent forces {}".format(self.dim.R))
        
        self.latentforces = [LatentForce(kern)
                             for kern in kernels]
        
        # clone kernels for versions that will be operated on
        for gp in self.latentforces:
            gp.kernel_ = gp.kernel.clone_with_theta(gp.kernel.theta)

    def setup_dataprecisions(self):
        self.dataprecisions = 1e4*np.ones(self.dim.K)

    def setup_gammas(self):
        self.gammas = 1e-2*np.ones(self.dim.K)

    def _setup(self, times, Y, data_times=None):
        self._data_times = times.copy()
        self.Y = Y.copy()
        self.vecy = Y.T.ravel()
        if data_times is not None:
            # the model has been augmented with
            # additional prediction points            
            raise NotImplementedError
        # redo the dimensions        
        self.dim = Dimensions(times.size, self.dim.K, self.dim.R)
        self.ttf = self._data_times

        # initalise everything that hasn't already been initalised
        if not hasattr(self, 'latentstates'):
            # no latent states supplied so use default setting
            self.setup_latentstates()
        if not hasattr(self, 'latentforces'):
            self.setup_latentforces()
        if not hasattr(self, 'dataprecisions'):
            self.setup_dataprecisions()
        if not hasattr(self, 'gamma'):
            self.setup_gammas()

    def _fit_init(self, is_fixed_vars=None, **kwargs):
        """ Handles initialisation of the fitting function.
        """
        try:
            g0 = kwargs['g0']
        except KeyError:
            g0 = np.zeros(self.dim.R*self.dim.N)
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
        except:
            loggamma0 = np.log(1e-4*np.ones(self.dim.K))
        try:
            dataprecisions0 = kwargs['dataprecisions0']
        except:
            dataprecisions0 = self.dataprecisions

        full_init = [g0, logpsi0, logphi0, loggamma0, dataprecisions0]
        if is_fixed_vars is None:
            free_vars_shape = [item.size for item in full_init]
            return np.concatenate(full_init), free_vars_shape, None

        else:
            full_init_shape = [item.size for item in full_init]
            free_vars = []
            fixed_vars = []
            for item, boolean in zip(full_init, is_fixed_vars):
                if boolean:
                    fixed_vars.append(item)
                else:
                    free_vars.append(item)
            free_vars_shape = [item.size for item in free_vars]
            return np.concatenate(free_vars), free_vars_shape, fixed_vars

    def fit2(self, times, Y, **kwargs):
        """Fits the model by directly optimising the likelihood function.
        """

        # make sure the model is ready for fitting by calling _setup
        self._setup(times, Y)

        # for now default behaviour is to fix the data precisions
        kwargs['dataprecisions_is_fixed'] = True

        # Inital preprocessing of fit arguments and shape  
        # to allow for parameters to be kept fixed during the
        # optimisation process
        
        var_names = ['g', 'logpsi', 'logphi', 'loggamma', 'dataprecisions']
        
        # check **kwargs to see if any variables have been kept fixed
        is_fixed_vars = [kwargs.pop("".join((vn, "_is_fixed")), False)
                         for vn in var_names]
        if sum(is_fixed_vars) == 0:
            is_fixed_vars = None
            mask = None
        else:
            mask = [False] + is_fixed_vars

        # utility function to mix the free variables and the fixed variables
        def _var_mixer(free_vars, free_vars_shape, fixed_vars):
            """ Returns the (ordered) full variables.
            """
            free_vars = _unpack_vector(free_vars, free_vars_shape)
            if is_fixed_vars is None:
                return free_vars
            else:
                full_vars = []
                ifree = 0
                ifixed = 0
                for b in is_fixed_vars:
                    if b:
                        full_vars.append(fixed_vars[ifixed])
                        ifixed += 1
                    else:
                        full_vars.append(free_vars[ifree])
                        ifree += 1
                return full_vars
                
        # objective function is given by the negative log likelihood
        def objfunc(arg, free_vars_shape, fixed_vars):
            # free variables and fixed variables need
            # to be mixed in the right order for likelihood func

            # reshape the arg from vector to list of subvectors
            full_vars = _var_mixer(arg, free_vars_shape, fixed_vars)

            try:
                res = self.log_likelihood(*full_vars, eval_gradient=True, mask=mask)
                grad = np.concatenate([item for item in res[1:]])
                return -res[0], -grad

            except:# np.linalg.LinAlgError (kernel can throw inf NAN errors)
                return np.inf, np.zeros(arg.size)

        # Initalise fit
        if is_fixed_vars is None:
            init, free_vars_shape, fixed_vars = \
                  self._fit_init(**kwargs)
        else:
            init, free_vars_shape, fixed_vars = \
                  self._fit_init(is_fixed_vars = is_fixed_vars, **kwargs)

        res = minimize(objfunc, init,
                       jac=True,
                       args=(free_vars_shape, fixed_vars),
                       options={'maxiter': 500,
                                'disp': kwargs.pop('disp', False)})

        self.fit_res = res
        full_vars_fit = _var_mixer(res.x, free_vars_shape, fixed_vars)
        full_vars_fit[0] = full_vars_fit[0].reshape(self.dim.R, self.dim.N)
        return FitResults(*full_vars_fit)
        
    def fit(self, times, Y, g0=None,
            opt_lf_hyperpar=False, EMinit=False, EMniter=10,
            disp=False, verbose=False):
        """
        Fits the model by directly optimising the likelihood function.
        """
        self._setup(times, Y)
    
        # total number of latent state hyperparameters
        N_phi = sum(ls.kernel.theta.size for ls in self.latentstates)

        # shape of the objective func argument
        of_arg_shape = [self.dim.N*self.dim.R,  # size of lf vector
                        N_phi,                  # size of ls hyperpars 
                        self.dim.K]             # size of gamma
        if opt_lf_hyperpar:
            N_psi = sum(lf.kernel.theta.size for lf in self.latentforces)
            of_arg_shape.insert(1, N_psi)

        # data precision variables treated as fixed
        dataprecisions = self.dataprecisions

        def objfunc(arg):
            if opt_lf_hyperpar:
                g, logpsi, logphi, loggamma = _unpack_vector(arg, of_arg_shape)
            else:
                logpsi = _get_latentforce_theta(self)
                g, logphi, loggamma = _unpack_vector(arg, of_arg_shape)

            try:
                ll, ll_g_grad, ll_lpsi_grad, ll_lphi_grad, ll_lgam_grad = \
                    self.log_likelihood(g, logpsi,
                                        logphi, loggamma,
                                        dataprecisions,
                                        True)
            except:
                return np.inf, np.zeros(arg.size)
                
            if opt_lf_hyperpar:
                ll_grad = np.concatenate((ll_g_grad,
                                          ll_lpsi_grad,
                                          ll_lphi_grad,
                                          ll_lgam_grad))
            else:
                ll_grad = np.concatenate((ll_g_grad,
                                          ll_lphi_grad,
                                          ll_lgam_grad))

            return -ll, -ll_grad

        if EMinit:
            # Initalise fitting using 'EMniter' iterations of
            # the EM algorithm
            if verbose:
                print("Initalising using the EM algorithm with {} iterations...".format(EMniter))
            em_fit = self.em_fit(times, Y, max_iter=EMniter, verbose=verbose)
            if opt_lf_hyperpar:
                init = np.concatenate((
                    em_fit.g, em_fit.logpsi, em_fit.logphi, em_fit.loggamma))
            else:
                init = np.concatenate((
                    em_fit.g, em_fit.logphi, em_fit.loggamma))
            if verbose:
                print("...initalisation done.")
        else:
            # call _setup
            self._setup(times, Y)
            # inital values for optimiser
            if g0 is None:
                g0 = np.zeros(of_arg_shape[0])
            logphi0 = _get_latentstate_theta(self)
            logpsi0 = _get_latentforce_theta(self)
            loggamma0 = np.zeros(self.dim.K)
            if opt_lf_hyperpar:
                init = np.concatenate((g0, logpsi0, logphi0, loggamma0))
            else:
                init = np.concatenate((g0, logphi0, loggamma0))

        res = minimize(objfunc, init, jac=True,
                       options={'disp': disp})

        res_x = _unpack_vector(res.x, of_arg_shape)
        g_ = res_x[0]
        gammas_ = res_x[-1]
        self.gammas_ = np.exp(res_x[-1])

        if opt_lf_hyperpar:
            logpsi_ = res_x[1]
            logphi_ = res_x[2]
        else:
            logpsi_ = _get_latentforce_theta(self)
            logphi_ = res_x[1]

        logphi_ = _unpack_vector(logphi_, _get_latentstate_theta_shape(self))
        for gp, theta in zip(self.latentstates, logphi_):
            gp.kernel_ = gp.kernel.clone_with_theta(theta)

        logpsi_ = _unpack_vector(logpsi_, _get_latentforce_theta_shape(self))
        for gp, theta in zip(self.latentforces, logpsi_):
            gp.kernel_ = gp.kernel.clone_with_theta(theta)

        self.g_ = g_
        self.logpsi_ = logpsi_
        self.logphi_ = logphi_

        return res

    def em_fit(self, times, Y, lftol=1e-4, data_times=None,
               logliktol=1e-4,
               max_iter=100,
               verbose=False,
               return_full=False):
        """

        Parameters
        ----------
        times : array
            The vector of times at which the latent forces are predicted.

        Y : array, shape (n_samples_Y, K)
            Array of observed data.

        lftol : float, default: 1e-4
            Convergence tolerance for the latent force variables.

        logliktol : float, default: 1e-4
            Convergence tolerance for change in log-likelihood

        max_iter : int, default: 100
            Maximum number of iterations of the EM algorithm to achieve convergence.

        data_times : array, shape (n_samples_Y,), default: None
            If n_times > n_samples_Y then times[n_times, ] = data_times

        """
        self._setup(times, Y, data_times=data_times)

        emopt = EMopt_MLFMAdapGrad(self,
                                   lftol, logliktol,
                                   max_iter,
                                   update_precision=not self.is_precision_fixed)
        res = emopt(verbose=verbose, return_full=return_full)

        if return_full:
            self.g_ = res.g[-1,]
            self.logpsi_ = res.logpsi[-1, ]
            self.logphi_ = res.logphi[-1, ]
            self.loggamma_ = res.loggamma[-1, ]
        else:
            self.g_ = res.g
        # store a ref to  the emopt for post analysis
        #self._emopt = emopt
        
        return res

    def var_fit(self, g0=None, gmean_tol=1e-6, max_nt=100):
        vardist = VarMLFMAdapGrad(self)
        mcur = np.inf
        nt = 0

        if g0 is not None:
            vardist.update_G_var_dist()
            self.Eg_ = g0.reshape(self.dim.R, self.dim.N)
            vardist.update_X_var_dist()
        
        while True:
            vardist.update_G_var_dist()
            vardist.update_X_var_dist()

            gmean_delta = np.linalg.norm(vardist.Eg_.ravel() - mcur)
            mcur = vardist.Eg_.ravel()
            if gmean_delta < gmean_tol:
                break

            nt += 1
            if nt == max_nt:
                break

        self.vardist = vardist

    def foo(self,
            g, logpsi,
            logphi, loggamma,
            dataprecisions,
            eval_gradient=False, **kwargs):

        ll_g, ll_g_grad, _ = log_likelihood_g_prior(g, logpsi, self)
        return ll_g, ll_g_grad

    @mask_output
    def log_likelihood(self,
                       g, log_psi,
                       log_phi, log_gamma,
                       dataprecisions,
                       eval_gradient=False, include_prior=True,
                       **kwargs):

        # model inv. covariance matrix
        Lam, Lam_g_gradient, Lam_logphi_gradient, Lam_loggam_gradient = \
             Lambda(g, log_phi, np.exp(log_gamma), self, eval_gradient=True)

        # x prior inv. covariance matrix
        Cxinv, Cxinv_logphi_grad = xprior_invcov(log_phi, self)

        # data error. model
        Sigma = block_diag(*[1/prec * np.eye(self.dim.N)
                             for prec in dataprecisions])

        # contribution from g prior
        if include_prior:
            ll_g, ll_g_grad, ll_logpsi_grad = log_likelihood_g_prior(g, log_psi, self)
            
        else:
            ll_g, ll_g_grad, ll_logpsi_grad = (0., 0., 0.)
        
        L = np.linalg.cholesky(Lam + Cxinv)
        
        K = np.linalg.inv(Lam + Cxinv)
        if self.is_tt_aug:
            # augmented dataset has to be transformed
            # to only those with observations
            D = self.sparse_data_map
            K = D.dot(D.dot(K).T)

        
        K += Sigma
        Kchol = np.linalg.cholesky(K)

        if eval_gradient:

            K_g_gradient = np.dstack((
                - cho_solve((L, True),
                            cho_solve((L, True), Lam_g_gradient[..., i]).T)
                for i in range(g.size)))
            
            K_lphi_gradient = np.dstack((
                - cho_solve((L, True),
                            cho_solve((L, True),
                                      Lam_logphi_gradient[..., i] + \
                                      Cxinv_logphi_grad[..., i]).T)
                for i in range(log_phi.size)))
            
            K_lgam_gradient = np.dstack((
                - cho_solve((L, True),
                            cho_solve((L, True), Lam_loggam_gradient[..., i]).T)
                for i in range(log_gamma.size)))

            y_train = self.vecy[:, np.newaxis]
            alpha = cho_solve((Kchol, True), y_train)
            tmp = np.einsum("ik,jk->ijk", alpha, alpha)
            tmp -= cho_solve((Kchol, True), np.eye(K.shape[0]))[:, :, np.newaxis]

            log_likelihood_g_gradient_dims = \
                                           .5 * np.einsum("ijl,ijk->kl", tmp, K_g_gradient)
            log_likelihood_g_gradient = log_likelihood_g_gradient_dims.sum(-1)

            log_likelihood_phi_gradient_dims = \
                                             .5 * np.einsum("ijl, ijk->kl", tmp, K_lphi_gradient)
            log_likelihood_phi_gradient = log_likelihood_phi_gradient_dims.sum(-1)
            
            log_likelihood_gam_gradient_dims = \
                                             .5 * np.einsum("ijl,ijk->kl", tmp, K_lgam_gradient)
            log_likelihood_gam_gradient = log_likelihood_gam_gradient_dims.sum(-1)
            log_likelihood_gam_gradient *= np.exp(log_gamma)

            ll = ll_g + \
                 multivariate_normal.logpdf(self.vecy,
                                            np.zeros(self.vecy.size),
                                            cov=K)
            
            return ll, log_likelihood_g_gradient + ll_g_grad, \
                   ll_logpsi_grad, \
                   log_likelihood_phi_gradient, \
                   log_likelihood_gam_gradient

        return ll_g + \
               multivariate_normal.logpdf(self.vecy,
                                          np.zeros(self.vecy.size),
                                          cov=K)

    def g_cond_distribution(self, x, logpsi, logphi, loggamma):
        x = x.reshape(self.dim.K, self.dim.N)
        Lxx_list, Mdx_list, Schol_list = handle_ls_covar(logphi,
                                                         np.exp(loggamma),
                                                         self.ttf,
                                                         self.latentstates,
                                                         _get_latentstate_theta_shape(self))

        invcov = []
        premean = []
        for k in range(self.dim.K):
            vk = vk_flow_rep(k, x, self.struct_mats)
            mk = Mdx_list[k].dot(x[k, :])
            SkinvVk = np.column_stack([cho_solve((Schol_list[k], True), np.diag(vkr))
                                       for vkr in vk[1:]])
            premean.append(SkinvVk.T.dot(mk - vk[0]))

            Vk = np.row_stack([np.diag(vkr) for vkr in vk[1:]])
            ic = Vk.dot(SkinvVk)

            invcov.append(ic)

        # add the contribution from the prior
        prior_ic = []
        logpsi = _unpack_vector(logpsi, _get_latentforce_theta_shape(self))
        for theta, gp in zip(logpsi, self.latentforces):
            kern = gp.kernel.clone_with_theta(theta)
            Cgr = kern(self.ttf[:, None])
            Cgr[np.diag_indices_from(Cgr)] += gp.alpha
            L = np.linalg.cholesky(Cgr)
            prior_ic.append(cho_solve((L, True), np.eye(L.shape[0])))

        invcov = sum(invcov) + block_diag(*prior_ic)
        cov = np.linalg.inv(invcov)
        mean = cov.dot(sum(premean))

        return mean, cov


class EMopt_MLFMAdapGrad:
    """
    EM optimisation routine for MLFM using adaptive gradient matching.
    """
    def __init__(self, mlfm, lftol, logliktol, max_iter,
                 update_precision=True):
        """

        Parameters
        ----------
        mlfm : `class:MLFMAdapGrad` object
            MLFM model using adaptive gradient matching on which fitting is carried out.

        lftol : float
            Convergence tolerance for the latent force variables.

        logliktol : float
            Convergence tolerance for the change in log-likelihood

        max_iter : int
            Maximum number of iterations of the EM algorithm to achieve convergence
        """
        self.mlfm = mlfm  # attach the mlfm model

        # Convergence tolerance values
        self.lftol = lftol
        self.logliktol = logliktol

        # Number of EM steps
        self.max_iter = max_iter

        # Collect information from the model
        self.mlfm_theta_phi_shape = _get_latentstate_theta_shape(mlfm)
        self._N_theta_phi = sum(self.mlfm_theta_phi_shape)

        self.mlfm_theta_psi_shape = _get_latentforce_theta_shape(mlfm)
        self._N_theta_psi = sum(self.mlfm_theta_psi_shape)


        self.cov_fetcher = LatentStateCovarHandler(self.mlfm.ttf,
                                                   self.mlfm.latentstates,
                                                   self.mlfm_theta_phi_shape)

        # handles which variables to update
        self.update_precision = update_precision

    def Mstep(self, init, Ex, Covx, update_logpsi=False):

        # shape of the objfunc argument
        _of_arg_shape = [self.mlfm.dim.N*self.mlfm.dim.R,
                         self._N_theta_phi,
                         self.mlfm.dim.K]

        if update_logpsi:
            # add the size of lf hyper parameters
            _of_arg_shape += [self._N_theta_psi]

        def _objfunc(arg):
            try:
                if update_logpsi:
                    g, log_phi, log_gamma, log_psi = _unpack_vector(arg,
                                                                _of_arg_shape)
                else:
                    # unpack g, th, lgamma
                    log_psi = _get_latentforce_theta(self.mlfm)
                    g, log_phi, log_gamma = _unpack_vector(arg,
                                                           _of_arg_shape)

                    ell, ell_grad = EM_Mstep_objfunc(g,
                                                     log_phi, log_gamma, log_psi,
                                                     Ex, Covx,
                                                     self.mlfm,
                                                     self.mlfm_theta_phi_shape,
                                                     eval_gradient=True,
                                                     eval_logpsi_grad=update_logpsi)
                    # minimisation problem so take neg.
                return -ell, -ell_grad
            except np.linalg.LinAlgError:
                return np.inf, np.zeros(arg.size)

        res = minimize(_objfunc, init, jac=True, options={'disp': False})
        
        if update_logpsi:
            ghat, lphi_hat, lgam_hat, lpsi_hat = _unpack_vector(res.x,
                                                                _of_arg_shape)
            return ghat, lphi_hat, lgam_hat, lpsi_hat
        else:
            ghat, lphi_hat, lgam_hat, = _unpack_vector(res.x,
                                                   _of_arg_shape)
            return ghat, lphi_hat, lgam_hat


    def Estep(self, g, log_phi, log_gamma, dataprecisions):

        theta_loggamma = tuple(np.concatenate((log_phi, log_gamma)))

        Lxx_ls, Mdx_ls, Schol_ls = self.cov_fetcher.get_covs(theta_loggamma)
        
        Ex, Covx = x_cond_distribution(g,
                                       dataprecisions,
                                       Schol_ls,
                                       Mdx_ls,
                                       Lxx_ls,
                                       self.mlfm)
        return Ex, Covx


    def __call__(self, return_full=False, verbose=False):

        # Initalise the latent state variables
        Ex = self.mlfm.Y.T
        Covx = BlockCovar.fromfull(np.eye(self.mlfm.dim.K*self.mlfm.dim.N)*1e-2,
                                   self.mlfm.dim.K, self.mlfm.dim.N)

        # Inital state hyper parameters
        loggamma = np.zeros(self.mlfm.dim.K)
        logphi = _get_latentstate_theta(self.mlfm)
        logpsi = _get_latentforce_theta(self.mlfm)
        dataprecisions = self.mlfm.dataprecisions.copy()

        # initalise force as 0
        g = np.zeros(self.mlfm.dim.N*self.mlfm.dim.R)

        if return_full:
            # variables to be collected
            gs, logphis, logpsis, loggammas = ([], [], [], [])

        nt = 0  # iterator count
        ellcur = -np.inf

        while True:

            # give some time for a plausible solution to be
            # found
            # - prevents model collapsing to local fixed point
            x0 = np.concatenate([g, logphi, loggamma]) #, logpsi])
            _g, logphi, loggamma = self.Mstep(x0,
                                              Ex,
                                              Covx,
                                              update_logpsi=False)

            if self.update_precision:
                # update obs noise
                dataprecisions = self.observation_noise_update(Ex, Covx)

            # update lf hyper parameters
            logpsi = self.latentforce_hyperpar_update(_g, logpsi)

            # Carry out the Estep
            Ex, Covx = self.Estep(_g, logphi, loggamma, dataprecisions)

            ####################################
            #                                  #
            # Recording and convergence checks #
            #                                  #
            ####################################

            # save the change in the latent force
            gdelt = max(np.abs(_g - g))

            ell = self.mlfm.log_likelihood(g,
                                           logpsi,
                                           logphi,
                                           loggamma,
                                           dataprecisions)
            elldiff = ell - ellcur
            if elldiff < 0:
                break
            else:
                g = _g

            if verbose: print(nt, ell, elldiff)

            if return_full:
                gs.append(g)
                logphis.append(logphi)
                logpsis.append(logpsi)
                loggammas.append(loggamma)

            nt += 1
            try:
                assert(elldiff >= 0)
                if elldiff <= self.logliktol:
                    nt_iter_msg = "after {} iterations".format(nt)
                    conv_msg = "Loglikelihood converged with change {} < {}".format(elldiff,
                                                                                    self.logliktol)
                    if verbose:
                        print(conv_msg + " " + nt_iter_msg)
                    break
                else:
                    ellcur = ell
            except:
                if verbose:
                    print("Likelihood has decreased with delta {}".format(elldiff))
                break
            if gdelt <= self.lftol and nt > 100:
                # g has converged
                nt_iter_msg = "after {} iterations".format(nt)
                conv_msg = "Latent force coverged with {} < {}".format(gdelt, self.lftol)
                if verbose:
                    print(conv_msg + " " + nt_iter_msg)
                break
            # loglikelihood check not yet implemented.
            
            elif nt >= self.max_iter:
                conv_msg = "EM algorithm failed to converge"
                nt_iter_msg = "after {} iterations".format(nt)
                if verbose:
                    print(conv_msg + " " + nt_iter_msg)
                break


        if return_full:
            result = EMfitResults(g = np.asarray(gs),
                                  logphi = np.asarray(logphis),
                                  logpsi = np.asarray(logpsis),
                                  loggamma = np.asarray(loggammas))
        else:
            result = EMfitResults(g = g,
                                  logphi = logphi,
                                  logpsi = logpsi,
                                  loggamma = loggamma)
        return result

    def observation_noise_update(self, Ex, Covx):
        Ex = Ex.reshape(self.mlfm.dim.K, self.mlfm.dim.N)
        Varx = np.diag(Covx.full).reshape(self.mlfm.dim.K, self.mlfm.dim.N)

        precisions = []
        for k in range(self.mlfm.dim.K):
            s = sum(Varx[k, :] + (self.mlfm.Y[:, k]-Ex[k, :])**2)
            precisions.append( (self.mlfm.dim.N - 1) / s)

        return precisions
        

    def latentforce_hyperpar_update(self, g, thetacur, ow_kernel=False):
        """
        Carries out EM(conditional) maximisation of the latent force
        hyperparameters having previously optimised for the latent forces.

        Parameters
        ----------
        lfhat : array
            Current estimate of the latent forces.

        ow_kernel : boolean, (default True)
            Wether the kernel of the `class:LatentForce` variable should be
            overwritten with the kernel_ obtained from fitting.
        """
        # (crude) catch of optimisation warnings thrown by
        # GPR .fit()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            thetacur = _unpack_vector(thetacur,
                                   _get_latentforce_theta_shape(self.mlfm))
            theta_hat = []

            # rehape g
            g = g.reshape(self.mlfm.dim.R, self.mlfm.dim.N)
            
            for r, lf in enumerate(self.mlfm.latentforces):
                kernel = lf.kernel.clone_with_theta(thetacur[r])
                gp = GaussianProcessRegressor(kernel)
                gp.fit(self.mlfm.ttf[:, None], g[r, :])
                theta_hat.append(gp.kernel_.theta)
        return np.concatenate(theta_hat)


class VarMLFMAdapGrad:
    def __init__(self, mlfm):

        # check to see if the hyperparameters of the MLFM have been fitted
        for gp in mlfm.latentforces:
            if not hasattr(gp, 'kernel_'):
                gp.kernel_ = gp.kernel.clone_with_theta(gp.kernel.theta)
        for gp in mlfm.latentstates:
            if not hasattr(gp, 'kernel_'):
                gp.kernel_ = gp.kernel.clone_with_theta(gp.kernel.theta)
        # check to see if gamma has been set, otherwise set gamma
        if not hasattr(mlfm, 'gammas_'):
            mlfm.gammas_ = mlfm.gammas.copy()

        if not hasattr(mlfm, 'dataprecisions_'):
            mlfm.dataprecisions_ = mlfm.dataprecisions.copy()
        self.Edataprecisions_ = mlfm.dataprecisions_

        self.mlfm = mlfm

        self._init_X_var_dist()
        self._store_cov_mats(mlfm)

    def _store_cov_mats(self, mlfm):
        Lxx_list, Mdx_list, Schol_list = handle_ls_covar(_get_latentstate_theta(mlfm, '_'),
                                                         mlfm.gammas_,
                                                         mlfm.ttf, mlfm.latentstates,
                                                         _get_latentstate_theta_shape(mlfm))
        self.Lxx_list_ = Lxx_list
        self.Mdx_list_ = Mdx_list
        self.Schol_list_ = Schol_list

    def update_X_var_dist(self):

        # Contribution from the prior
        x_prior_mean = np.zeros(self.mlfm.dim.N*self.mlfm.dim.K)
        x_prior_invcov = self.x_prior_invcov

        # get data precision
        x_data_mean = self.mlfm.vecy
        x_data_invcov = np.diag(
            np.concatenate([tau*np.ones(self.mlfm.dim.N) for tau in self.Edataprecisions_]))

        means = [x_prior_mean, x_data_mean]
        invcovs = [x_prior_invcov, x_data_invcov]

        # contribution from the model
        x_model_mean = np.zeros(self.mlfm.dim.N*self.mlfm.dim.K)        
        x_model_invcov = Exmodel_inv_cov(self.Eg_, self.Covg_,
                                         self.Schol_list_, self.Mdx_list_,
                                         self.mlfm)

        means.append(x_model_mean)
        invcovs.append(x_model_invcov)

        mean, cov = matrixrv_util._prod_norm_pars(means, invcovs)
        mean = mean.reshape(self.mlfm.dim.K, self.mlfm.dim.N)
        self.Ex_ = mean
        self.Covx_ = BlockCovar.fromfull(cov, self.mlfm.dim.K, self.mlfm.dim.N)

    def update_G_var_dist(self):

        # model dependent component
        mean, invcov = ([], [])
        for k in range(self.mlfm.dim.K):
            mk, ick = Egmodel_par_k(k, self.Ex_, self.Covx_,
                                    self.Schol_list_[k], self.Mdx_list_[k], self.mlfm)
            mean.append(mk)
            invcov.append(ick)
        mean = sum(mean)

        # get contribution from prior
        I = np.eye(self.mlfm.dim.N)
        Ks = [gp.kernel_(self.mlfm.ttf[:, None]) + gp.alpha*I
              for gp in self.mlfm.latentforces]
        Kinv = block_diag(*[cho_solve((np.linalg.cholesky(K), True), I)
                            for K in Ks])

        Cg = block_diag(*Ks)        
        cov = np.linalg.inv(np.eye(Cg.shape[0]) + Cg.dot(sum(invcov))).dot(Cg)

        #invcov.append(Kinv)
        #invcov = sum(invcov)
        #L = np.linalg.cholesky(invcov)
        #cov = cho_solve((L, True), np.eye(L.shape[0]))

        # mean is C.dot(Cinv_mean)
        mean = np.dot(cov, mean)
        mean = mean.reshape(self.mlfm.dim.R, self.mlfm.dim.N)

        self.Eg_ = mean
        self.Covg_ = BlockCovar.fromfull(cov, self.mlfm.dim.R, self.mlfm.dim.N)

    def _init_X_var_dist(self, scale=1e-3):
        Y = self.mlfm.Y
        self.Ex_ = [y for y in Y.T]

        Covx = []
        for i in range(self.mlfm.dim.K):
            for j in range(i+1):
                if i == j:
                    Covx.append(np.diag(scale*np.ones(self.mlfm.dim.N)))
                else:
                    Covx.append(np.zeros((self.mlfm.dim.N, self.mlfm.dim.N)))
        self.Covx_ = BlockCovar(Covx, self.mlfm.dim.K, self.mlfm.dim.N)
    

    @property
    def x_prior_invcov(self):
        """Prior inverse cov. matrix for the state interpolators (will be constant)
        """
        try:
            return self._x_prior_invcov
        except AttributeError:
            K = []
            for gp in self.mlfm.latentstates:
                c = gp.kernel_(self.mlfm.ttf[:, None])
                c[np.diag_indices_from(c)] += gp.alpha
                K.append(c)
            chols = [np.linalg.cholesky(_K) for _K in K]
            I = np.eye(self.mlfm.dim.N)
            self._x_prior_invcov = block_diag(*[cho_solve((L, True), I)
                                                 for L in chols])
            return self._x_prior_invcov
        

# Handler functions
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

def _get_latentstate_theta(mlfmobj, kern=None):
    # take theta from the fitted kernels
    if kern == '_':
        return np.concatenate([gp.kernel_.theta
                               for gp in mlfmobj.latentstates])
    else:
        return np.concatenate([gp.kernel.theta
                               for gp in mlfmobj.latentstates])


def _get_latentforce_theta(mlfmobj, kern=None):
    if kern == '_':
        return np.concatenate([gp.kernel_.theta
                               for gp in mlfmobj.latentforces])
    else:
        return np.concatenate([gp.kernel.theta
                               for gp in mlfmobj.latentforces])        

def _get_latentstate_theta_shape(mlfmobj):
    """
    Gets a list of the size of the free kernel
    hyperparameters for each of latent states
    """
    return [gp.kernel.theta.size
            for gp in mlfmobj.latentstates]
def _get_latentforce_theta_shape(mlfmobj):
    """
    Gets a list of the size of the free kernel
    hyperparamers for each of the latent forces
    """
    return [gp.kernel.theta.size
            for gp in mlfmobj.latentforces]

def handle_ls_covar(theta, gamma, tt, latentstates, theta_shape):
    """
    Handles the construction of the covariance matrix
    and mean prediction matrix from marginalising out
    the gradient process
    """
    In = np.eye(tt.size)
    
    theta_ks = _unpack_vector(theta, theta_shape)

    Lxx_list = []
    Mdx_list = []
    Schol_list = []

    for k, gp in enumerate(latentstates):
        kernel = gp.kernel.clone_with_theta(theta_ks[k])

        Cxx = kernel(tt[:, None]) + gp.alpha*In
        Cxdx = kernel(tt[:, None], comp='xdx')[..., 0]
        Cdxdx = kernel(tt[:, None], comp='dxdx')[..., 0, 0]

        Lxx = np.linalg.cholesky(Cxx)
        Mdx = Cxdx.T.dot(back_sub(Lxx, In))
        Cdx_x = Cdxdx - Cxdx.T.dot(back_sub(Lxx, Cxdx))

        S = Cdx_x + gamma[k]*In
        
        Lxx_list.append(Lxx)
        Mdx_list.append(Mdx)
        Schol_list.append(np.linalg.cholesky(S))

    return Lxx_list, Mdx_list, Schol_list

def handle_ls_covar_wgrad(theta, gamma, tt, latentstates, theta_shape):
    In = np.eye(tt.size)
    theta_ks = _unpack_vector(theta, theta_shape)

    Lxx_list = []
    Cxx_grad_list = []
    Mdx_list = []
    Mdx_grad_list = []
    Schol_list = []
    S_grad_list = []

    for k, gp in enumerate(latentstates):
        kernel = gp.kernel.clone_with_theta(theta_ks[k])

        Cxx, Cxx_grad = kernel(tt[:, None], eval_gradient=True)
        Cxx += gp.alpha*In

        Cxdx, Cxdx_grad = kernel(tt[:, None], comp='xdx', eval_gradient=True)

        Cdxdx, Cdxdx_grad = kernel(tt[:, None], comp='dxdx', eval_gradient=True)

        Lxx = np.linalg.cholesky(Cxx)
        Mdx = Cxdx[..., 0].T.dot(back_sub(Lxx, In))
        Cdx_x = Cdxdx[..., 0, 0] - \
                Cxdx[..., 0].T.dot(back_sub(Lxx, Cxdx[..., 0]))

        S = Cdx_x + gamma[k]*In

        # calculate the gradients
        P = Cxx_grad.shape[-1]
        Cxx_inv_gradient = -np.dstack([back_sub(Lxx,
                                                back_sub(Lxx, Cxx_grad[:, :, p]).T)
                                       for p in range(P)])
        M_grad = np.dstack([back_sub(Lxx, Cxdx_grad[:, :, 0, p]).T
                            for p in range(P)])
        M_grad -= np.dstack([Cxdx[:, :, 0].dot(Cxx_inv_gradient[:, :, p])
                             for p in range(P)])

        Cdx_x_grad = Cdxdx_grad[:, :, 0, 0, :].copy()
        expr = np.dstack([Cxdx_grad[:, :, 0, p].T.dot(back_sub(Lxx, Cxdx[:, :, 0]))
                          for p in range(P)])
        
        Cdx_x_grad -= expr
        Cdx_x_grad -= np.dstack([expr[:, :, p].T for p in range(P)])
        Cdx_x_grad -= np.dstack([Cxdx[:, :, 0].T.dot( \
            Cxx_inv_gradient[:, :, p].dot( \
            Cxdx[:, :, 0])) for p in range(P)])

        Lxx_list.append(Lxx)
        Cxx_grad_list.append(Cxx_grad)
        Mdx_list.append(Mdx)
        Mdx_grad_list.append(M_grad)
        Schol_list.append(np.linalg.cholesky(S))
        S_grad_list.append(Cdx_x_grad)

    return (Lxx_list, Mdx_list, Schol_list), \
           (Cxx_grad_list, Mdx_grad_list, S_grad_list)

def handle_ls_covar_k_wgrad(thetak, gammak, tt, latentstate):
    In = np.eye(tt.size)
    kernel = latentstate.kernel.clone_with_theta(thetak)

    Cxx, Cxx_grad = kernel(tt[:, None], eval_gradient=True)
    Cxx += latentstate.alpha * In

    Cxdx, Cxdx_grad = kernel(tt[:, None], comp='xdx', eval_gradient=True)
    Cdxdx, Cdxdx_grad = kernel(tt[:, None], comp='dxdx', eval_gradient=True)

    Lxx = np.linalg.cholesky(Cxx)
    Mdx = Cxdx[..., 0].T.dot(back_sub(Lxx, In))
    Cdx_x = Cdxdx[..., 0, 0] - \
            Cxdx[..., 0].T.dot(back_sub(Lxx, Cxdx[..., 0]))

    S = Cdx_x + gammak*In

    # calculate the gradients
    P = Cxx_grad.shape[-1]
    Cxx_inv_gradient = -np.dstack([back_sub(Lxx,
                                            back_sub(Lxx, Cxx_grad[:, :, p]).T)
                                   for p in range(P)])
    M_grad = np.dstack([back_sub(Lxx, Cxdx_grad[:, :, 0, p]).T
                        for p in range(P)])
    M_grad -= np.dstack([Cxdx[:, :, 0].dot(Cxx_inv_gradient[:, :, p])
                         for p in range(P)])
    
    Cdx_x_grad = Cdxdx_grad[:, :, 0, 0, :].copy()
    expr = np.dstack([Cxdx_grad[:, :, 0, p].T.dot(back_sub(Lxx, Cxdx[:, :, 0]))
                      for p in range(P)])
        
    Cdx_x_grad -= expr
    Cdx_x_grad -= np.dstack([expr[:, :, p].T for p in range(P)])
    Cdx_x_grad -= np.dstack([Cxdx[:, :, 0].T.dot( \
            Cxx_inv_gradient[:, :, p].dot( \
            Cxdx[:, :, 0])) for p in range(P)])

    return (Lxx, Mdx, np.linalg.cholesky(S)), \
           (Cxx_grad, M_grad, Cdx_x_grad)
        
class LatentStateCovarHandler:
    """
    Handles the construction of cov. functions from the latent states

    """
    def __init__(self, tt, latentstates, theta_shape):
        self.tt = tt
        self.latentstates = latentstates
        self.theta_shape = theta_shape
        self._n_theta = sum(theta_shape)

    def get_covs(self, theta_loggamma_tup):
        theta_loggamma = np.array(theta_loggamma_tup)
        return handle_ls_covar(theta_loggamma[:self._n_theta],
                               np.exp(theta_loggamma[self._n_theta:]),
                               self.tt,
                               self.latentstates,
                               self.theta_shape)

"""
Useful Model Functions
"""
# rearrangements of the linear flow function
def uk_flow_rep(k, glist, A):
    K = A[0].shape[0]
    uk =[A[0, k, j] + sum([ar[k, j]*gr for ar, gr in zip(A[1:], glist)])
         for j in range(K)]
    return uk

def uk_flow_rep_mom(k, Eg, Covg, A):
    Euk = uk_flow_rep(k, Eg, A)
    Covuk = []
    K = A[0].shape[0]
    for i in range(K):
        for j in range(i+1):
            Covuk.append(sum(sum([Ar[k, i]*As[k, j]*Covg(r, s)
                                  for s, As in enumerate(A[1:])])
                             for r, Ar in enumerate(A[1:])))
    Covuk = BlockCovar(Covuk, K, Euk[0].size)
    return Euk, Covuk

def vk_flow_rep(k, xlist, A):
    vk0 = sum(A[0, k, j]*xj for j, xj in enumerate(xlist))
    vk = [sum(ar[k, j]*xj for j, xj in enumerate(xlist)) for ar in A[1:]]
    return [vk0] + vk

def vk_flow_rep_mom(k, Ex, Covx, A):
    Evk = vk_flow_rep(k, Ex, A)
    Covvk = []
    R = len(A) - 1

    for r in range(R+1):
        for s in range(r+1):
            Covvk.append(sum(sum(Arki*Askj*Covx(i, j)
                                 for j, Askj in enumerate(A[s, k, :]))
                             for i, Arki in enumerate(A[r, k, :])))
    Covvk = BlockCovar(Covvk, R+1, Evk[0].size)
    return Evk, Covvk

# conditional inverse covariance functions
def xmodel_inv_cov_k(k, g, Schol, Mdx, mlfmobj, eval_g_gradient=False):

    uk = uk_flow_rep(k,
                     g.reshape(mlfmobj.dim.R, mlfmobj.dim.N),
                     mlfmobj.struct_mats)


    diagUk = [np.diag(uki) for uki in uk]
    diagUk[k] -= Mdx

    invcov = np.dot(np.row_stack([dki.T for dki in diagUk]),
                    np.column_stack([back_sub(Schol, dkj) for dkj in diagUk]))
    if eval_g_gradient:
        A = mlfmobj.struct_mats
        Skinv_Uk = np.column_stack([back_sub(Schol, Dkj) for Dkj in diagUk])
        invcov_g_gradient = []
        for r in range(mlfmobj.dim.R):
            for n in range(mlfmobj.dim.N):
                dUk_grn = [np.diag(A[r+1, k, j]*np.eye(N=1, M=mlfmobj.dim.N, k=n).ravel())
                           for j in range(mlfmobj.dim.K)]
                expr = np.dot(np.row_stack(dUk_grn),
                              Skinv_Uk)
                invcov_g_gradient.append((expr + expr.T)[..., np.newaxis])
        invcov_g_gradient = np.dstack(invcov_g_gradient)
        return invcov, invcov_g_gradient
    else:
        return invcov

def Exmodel_inv_cov_k(k, Eg, Covg, Schol, Mdx, mlfmobj):
    """Takes the expectation of the kth model inv cov wrt to the dist. of the
    latent force.
    """
    # moments of the representatios ukj
    Euk, Covuk = uk_flow_rep_mom(k, Eg, Covg, mlfmobj.struct_mats)

    # invert S = Cov{dxdx} + gamma*I
    Sinv = cho_solve((Schol, True), np.eye(Schol.shape[0]))

    N, K = (mlfmobj.dim.N, mlfmobj.dim.K)
    inv_covar = np.zeros((N*K, N*K))
    for m in range(K):
        for n in range(K):
            res = (Covuk(m, n) + np.outer(Euk[m], Euk[n])) * Sinv
            if m == k:
                res -= Mdx.T.dot(Sinv.dot(np.diag(Euk[n])))
                if n == k:
                    res -= np.diag(Euk[m]).dot(Sinv.dot(Mdx))
                    res += Mdx.T.dot(Sinv.dot(Mdx))
            elif n == k:
                res -= np.diag(Euk[n]).dot(Sinv.dot(Mdx))

            inv_covar[m*N:(m+1)*N, n*N:(n+1)*N] = res
    return inv_covar

def xmodel_inv_cov(g, Schol_list, Mdx_list, mlfmobj, eval_g_gradient=False):
    if eval_g_gradient:
        ic_k = []
        ic_k_grad = []
        for k in range(mlfmobj.dim.K):
            ic, icg = xmodel_inv_cov_k(k, g, Schol_list[k], Mdx_list[k], mlfmobj, True)
            ic_k.append(ic)
            ic_k_grad.append(icg)
        return sum(ic_k), sum(ic_k_grad)
    else:
        return sum([
            xmodel_inv_cov_k(k, g, Schol_list[k], Mdx_list[k], mlfmobj)
            for k in range(mlfmobj.dim.K)])

def Exmodel_inv_cov(Eg, Covg, Schol_list, Mdx_list, mlfmobj):
    return sum([
        Exmodel_inv_cov_k(k, Eg, Covg, Schol_list[k], Mdx_list[k], mlfmobj)
        for k in range(mlfmobj.dim.K)])

def x_cond_distribution(g, data_precisions, Schol_list, Mdx_list, Lxx_list, mlfmobj):

    # x model inv cov
    x_mod_ic = xmodel_inv_cov(g, Schol_list, Mdx_list, mlfmobj)

    # x prior inv cov
    x_prior_ic = block_diag(*[back_sub(Lxx, np.eye(mlfmobj.dim.N))
                              for Lxx in Lxx_list])

    Lambda = x_mod_ic + x_prior_ic

    # contribution from the data
    pre_mean = np.concatenate([yk*prec
                               for yk, prec in zip(mlfmobj.Y.T, data_precisions)])
    invcov = Lambda + block_diag(*[prec*np.eye(mlfmobj.dim.N)
                                   for prec in data_precisions])

    # solve to get the cov. and mean
    cov = np.linalg.inv(invcov)
    mean = cov.dot(pre_mean)
    mean = mean.reshape(mlfmobj.dim.K, mlfmobj.dim.N)

    return mean, BlockCovar.fromfull(cov, mlfmobj.dim.K, mlfmobj.dim.N)

"""
Conditional distribution of the latent force
"""
def gprior_invcov(logpsi, mlfmobj):
    logpsi = _unpack_vector(logpsi, mlfmobj)
    ic = []
    for theta, gp in zip(logpsi,
                         mlfmobj.latentforces):
        kern = gp.kernel.clone_with_theta(theta)
        K = kern(mlfmobj.ttf[:, None])
        K[np.diag_indices_from(K)] += gp.alpha
        L = np.linalg.cholesky(K)
        ic.append(cho_solve((L, True), np.eye(L.shape[0])))
    return block_diag(*ic)

def gmodel_inv_cov_k(k, x, Schol, Mdx, mlfmobj):
    
    vk = vk_flow_rep(k,
                     x.reshape(mlfmobj.dim.K, mlfmobj.dim.N),
                     mlfmobj.struct_mats)

    diagVk = [np.diag(vkr) for vkr in vk]

    res = np.dot(np.row_stack([dkr.T for dkr in diagVk]),
                 np.column_stack([cho_solve((Schol, True), dks) for dks in diagVk]))

    return res
    
def gmodel_inv_cov(x, Schol_list, Mdx_list, mlfmobj):
    return sum(gmodel_inv_cov_k(k, x, Schol_list[k], Mdx_list[k], mlfmobj)
               for k in range(mlfmobj.dim.K))

def g_cond_distribution(x, logtheta, logpsi, mlfmobj):

    x = x.reshape(mlfmobj.dim.K, mlfmobj.dim.N)

    # g model inv cov
    for k in range(mlfmobj.dim.K):
        vk = vk_flow_rep(k, x, mlfmobj.struct_mats)

    # g prior inv cov
    g_prior_ic = gprior_invcov(logpsi, mlfmobj)

    Kinv = g_mod_ic + g_prior_ic


def Egmodel_par_k(k, Ex, Covx, Schol, Mdx, mlfmobj):
    Evk, Covvk = vk_flow_rep_mom(k, Ex, Covx, mlfmobj.struct_mats)

    Covvkxk = [sum(a[k, j]*Covx(k, j) for j in range(mlfmobj.dim.K)
                   for a in mlfmobj.struct_mats[1:])]
    CovvkMdxk = [np.dot(cvx, Mdx) for cvx in Covvkxk]

    R = mlfmobj.dim.R

    Sinv = cho_solve((Schol, True), np.eye(Schol.shape[0]))
    
    inv_covar = np.row_stack((
        np.column_stack(
        ((Covvk(s, t) + np.outer(Evk[s], Evk[t])) * Sinv
         for t in range(1, R+1))
        ) for s in range(1, R+1)))

    Evk_Sinv_v0 = np.concatenate(
        [matrixrv_util._E_diagx_M_y(Evk[s], Evk[0], Covvk(s, 0), Sinv)
         for s in range(1, R+1)])

    EvkT_Sinv_Mdx = np.concatenate(
        [matrixrv_util._E_diagx_M_y(Evks, Mdx.dot(Ex[k]), cvsmk, Sinv)
         for Evks, cvsmk in zip(Evk[1:], CovvkMdxk)])

    return EvkT_Sinv_Mdx - Evk_Sinv_v0, inv_covar
    #try:
    #    mean = np.linalg.solve(inv_covar, EvkT_Sinv_Mdx - Evk_Sinv_v0)
    #except:
    #    pinv = np.linalg.pinv(inv_covar)
    #    mean = pinv.dot(EvkT_Sinv_Mdx - Evk_Sinv_v0)
    #
    #return mean, inv_covar

"""
X Conditional Distribution
--------------------------
"""
def Lambdak(k, g, thetak, gammak, mlfmobj, eval_gradient=False):

    # make the covariances
    covs, grads = handle_ls_covar_k_wgrad(thetak, gammak,
                                          mlfmobj.ttf, mlfmobj.latentstates[k])
    Lxx, Mdx, Schol = covs
    Cxx_grad, Mdx_grad, S_grad = grads

    # representation of the flow as a function of g
    uk = uk_flow_rep(k,
                     g.reshape(mlfmobj.dim.R, mlfmobj.dim.N),
                     mlfmobj.struct_mats)

    diagUk = [np.diag(uki) for uki in uk]
    diagUk[k] -= Mdx

    lamk = np.dot(np.row_stack([Dki.T for Dki in diagUk]),
                  np.column_stack([back_sub(Schol, Dkj) for Dkj in diagUk]))

    if eval_gradient:

        #####################
        # gradient wrt to g #
        #####################
        Skinv_Uk = np.column_stack([back_sub(Schol, Dkj) for Dkj in diagUk])
        lamk_g_gradient = []
        A = mlfmobj.struct_mats
        for r in range(mlfmobj.dim.R):
            for n in range(mlfmobj.dim.N):
                dUk_grn = [np.diag(A[r+1, k, j]*np.eye(N=1, M=mlfmobj.dim.N, k=n).ravel())
                           for j in range(mlfmobj.dim.K)]
                expr = np.dot(np.row_stack(dUk_grn),
                              Skinv_Uk)
                lamk_g_gradient.append((expr + expr.T)[..., np.newaxis])
        lamk_g_gradient = np.dstack(lamk_g_gradient)

        ##########################
        # gradient wrt to thetak #
        ##########################        

        # get size of thetak
        if isinstance(thetak, float):
            P = 1
        else:
            P = len(thetak)

        # gradient of Uk wrt thetak
        Uk_grad = np.zeros((mlfmobj.dim.N, mlfmobj.dim.N*mlfmobj.dim.K, P))
        for p in range(P):
            Uk_grad[:, k*mlfmobj.dim.N:(k+1)*mlfmobj.dim.N, p] -= Mdx_grad[..., p]

        expr1 = -np.stack([Skinv_Uk.T.dot(S_grad[..., p].dot(Skinv_Uk))
                           for p in range(P)], axis=2)
        expr2 = np.stack([Uk_grad[..., p].T.dot(Skinv_Uk)
                          for p in range(P)], axis=2)
        expr2t = np.stack([expr2[..., p].T
                           for p in range(P)], axis=2)

        lamk_thetak_gradient = expr1 + expr2 + expr2t

        ##########################
        # gradient wrt to gammak #
        ##########################
        lamk_gammak_gradient = -Skinv_Uk.T.dot(Skinv_Uk)[..., np.newaxis]
        
        return lamk, lamk_g_gradient, lamk_thetak_gradient, lamk_gammak_gradient

    else:
        return lamk
    
def Lambda(g, theta, gamma, mlfmobj, eval_gradient=False):
    theta_shape = _get_latentstate_theta_shape(mlfmobj)
    theta = _unpack_vector(theta, theta_shape)

    if eval_gradient:
        L, L_g_grad, L_th_grad, L_gam_grad = ([], [], [], [])
        for k in range(mlfmobj.dim.K):
            lk, lk_g_grad, lk_th_grad, lk_gam_grad = Lambdak(k, g,
                                                             theta[k], gamma[k],
                                                             mlfmobj, True)
            L.append(lk)
            L_g_grad.append(lk_g_grad)
            L_th_grad.append(lk_th_grad)
            L_gam_grad.append(lk_gam_grad)
            
        return sum(L), sum(L_g_grad), np.dstack(L_th_grad), np.dstack(L_gam_grad)

    else:
        return sum(Lambdak(k, g, thetak, gamma[k], mlfmobj)
                   for k, thetak in enumerate(theta))

def xprior_invcov(theta, mlfmobj):

    # reshape theta
    theta_shape = _get_latentstate_theta_shape(mlfmobj)
    theta = _unpack_vector(theta, theta_shape)


    # make an identity matrix
    N = mlfmobj.dim.N
    K = mlfmobj.dim.K
    In = np.eye(mlfmobj.dim.N)

    Lxx_ls = []
    Cxxinv_grad_ls = []
        
    for k, gp in enumerate(mlfmobj.latentstates):
        kernel = gp.kernel.clone_with_theta(theta[k])
        Cxx, Cxx_grad = kernel(mlfmobj.ttf[:, None], eval_gradient=True)
        Cxx += gp.alpha*In

        Lxx = np.linalg.cholesky(Cxx)
        Lxx_ls.append(Lxx)        
        
        Cxxinv_gradient = np.zeros((N*K, N*K, theta_shape[k]))
        for p in range(theta_shape[k]):
            cxxinv_grad = -back_sub(Lxx,
                                    back_sub(Lxx, Cxx_grad[:, :, p]).T)
            Cxxinv_gradient[k*N:(k+1)*N, k*N:(k+1)*N, p] = cxxinv_grad
        Cxxinv_grad_ls.append(Cxxinv_gradient)

    invcov = block_diag(*[back_sub(Lxx, In) for Lxx in Lxx_ls])
    invcov_gradient = np.dstack(Cxxinv_grad_ls)

    return invcov, invcov_gradient
    
def gprior_invcov(theta, mlfmobj, eval_gradient):

    # reshape theta ( = log(psi) )
    theta_shape = _get_latentforce_theta_shape(mlfmobj)
    if mlfmobj.dim.R == 1:
        theta = [theta, ]
    else:
        theta = _unpack_vector(theta, theta_shape)

    # make an identity matrix
    N = mlfmobj.dim.N
    R = mlfmobj.dim.R
    In = np.eye(mlfmobj.dim.N)
    
    Lgg_ls = []
    Cgginv_grad_ls = []

    for r, gp in enumerate(mlfmobj.latentforces):
        kernel = gp.kernel.clone_with_theta(theta[r])
        Cgg, Cgg_grad = kernel(mlfmobj.ttf[:, None], eval_gradient=True)
        Cgg += gp.alpha*In

        Lgg = np.linalg.cholesky(Cgg)
        Lgg_ls.append(Lgg)

        Cgginv_gradient = np.zeros((N*R, N*R, theta_shape[r]))
        for p in range(theta_shape[r]):
            cgginv_grad = -back_sub(Lgg,
                                    back_sub(Lgg, Cgg_grad[..., p]).T)
            Cgginv_gradient[r*N:(r+1)*N, r*N:(r+1)*N, p] = cgginv_grad
        Cgginv_grad_ls.append(Cgginv_gradient)

    invcov = block_diag(*[back_sub(Lgg, In) for Lgg in Lgg_ls])
    invcov_gradient = np.dstack(Cgginv_grad_ls)

    return invcov, invcov_gradient

def ell_g_prior_r(r, g, thetar, mlfmobj, eval_gradient=True):
    """
    Value and gradient log prior of g
    """
    kernel = mlfmobj.latentforces[r].kernel_.clone_with_theta(thetar)

    K, K_gradient = kernel(mlfmobj.ttf[:, None], eval_gradient=True)
    K[np.diag_indices_from(K)] += mlfmobj.latentforces[r].alpha

    L = np.linalg.cholesky(K)

    # reshaping of g
    if len(g.shape) == 1:
        g = g[:, np.newaxis]

    alpha = cho_solve((L, True), g) # Line 3

    # Compute log-likelihood (compare line 7)
    # Cite sklearn.gaussian_process.GaussianProcessRegressor
    log_likelihood_dims = -0.5 * np.einsum("ik,ik->k", g, alpha)
    log_likelihood_dims -= np.log(np.diag(L)).sum()
    log_likelihood_dims -= K.shape[0] / 2 * np.log(2 * np.pi)
    log_likelihood = log_likelihood_dims.sum(-1) # sum over dimensions
    
    if eval_gradient:
        tmp = np.einsum("ik,jk->ijk", alpha, alpha)  # k: output-dimension
        tmp -= cho_solve((L, True), np.eye(K.shape[0]))[:, :, np.newaxis]
        # Compute "0.5 * trace(tmp.dot(K_gradient))" without
        # constructing the full matrix tmp.dot(K_gradient) since only
        # its diagonal is required
        log_likelihood_gradient_dims = \
                                     0.5 * np.einsum("ijl,ijk->kl", tmp, K_gradient)
        log_likelihood_theta_gradient = log_likelihood_gradient_dims.sum(-1)

        # also need gradient wrt to g
        log_likelihood_g_gradient = - alpha


    return log_likelihood, log_likelihood_g_gradient, log_likelihood_theta_gradient

def log_likelihood_g_prior(g, theta, mlfmobj, eval_gradient=True):
    # reshape theta ( = log(psi) )
    theta_shape = _get_latentforce_theta_shape(mlfmobj)
    if mlfmobj.dim.R == 1:
        theta = [theta, ]
    else:
        theta = _unpack_vector(theta, theta_shape)        

    # reshape g
    g = g.reshape(mlfmobj.dim.R, mlfmobj.dim.N)

    ellr_ls, ellr_gr_grad, ellr_thr_grad = ([], [], [])
    for r in range(mlfmobj.dim.R):
        gr = g[r, :].T
        l, l_g_grad, l_th_grad = ell_g_prior_r(r, gr, theta[r], mlfmobj, eval_gradient)
        ellr_ls.append(l)
        ellr_gr_grad.append(l_g_grad[:, 0])
        ellr_thr_grad.append(l_th_grad)

    ell = sum(ellr_ls)
    ell_g_grad = np.concatenate(ellr_gr_grad)
    ell_th_grad = np.concatenate(ellr_thr_grad)
    return ell, ell_g_grad, ell_th_grad
    

"""
EM Objective Functions
----------------------
"""
def EM_Mstep_objfunc(g, theta_phi, log_gamma, log_psi, Ex, Covx, mlfmobj, theta_shape,
                     cov_handler=None, eval_gradient=False, eval_logpsi_grad=False):

    # ExxT
    Exflat = np.concatenate([Exk for Exk in Ex])
    ExxT = Covx.full + np.outer(Exflat, Exflat)

    # contributions to the inv. cov. matrix of x from
    # 1) the ODE model
    tup = Lambda(g, theta_phi, np.exp(log_gamma),
                 mlfmobj, eval_gradient=True)
    lam_mod = tup[0]
    lam_mod_g_gradient = tup[1]
    lam_mod_theta_gradient = tup[2]
    lam_mod_gamma_gradient = tup[3]

    # 2) the prior
    lam_pri, lam_pri_theta_gradient = xprior_invcov(theta_phi, mlfmobj)

    lam = lam_mod + lam_pri
    lam_g_gradient = lam_mod_g_gradient
    lam_theta_gradient = lam_mod_theta_gradient + \
                         lam_pri_theta_gradient
    lam_gamma_gradient = lam_mod_gamma_gradient
    
    _, logdet = np.linalg.slogdet(lam)

    # want a map estimate so also need to add g prior
    gprior_tup = log_likelihood_g_prior(g, log_psi, mlfmobj, eval_gradient=True)
    ell_gprior = gprior_tup[0]
    ell_gprior_g_grad = gprior_tup[1]
    ell_gprior_logpsi_grad = gprior_tup[2]

    ell = -0.5*np.trace(ExxT.dot(lam)) + 0.5*logdet + ell_gprior 


    if eval_gradient:
        lam_inv = np.linalg.inv(lam)

        #######################
        # gradient of         #
        #                     #
        #  Tr( <xxT> (lam) )  #
        #                     #
        #######################

        # 1) wrt to g
        tr_xxt_lam_g_grad = np.array([np.einsum('ij,ji->',
                                                ExxT,
                                                lam_g_gradient[..., r*mlfmobj.dim.N + n])
                                      for r in range(mlfmobj.dim.R)
                                      for n in range(mlfmobj.dim.N)])

        # 2) wrt to theta
        tr_xxt_lam_th_grad = np.array([np.einsum('ij, ji->',
                                                 ExxT,
                                                 lam_theta_gradient[..., p])
                                       for p in range(theta_phi.size)])

        # 3) wrt to gamma
        tr_xxt_lam_gam_grad = np.array([np.einsum('ij, ji->',
                                                  ExxT,
                                                  lam_gamma_gradient[..., k])
                                        for k in range(mlfmobj.dim.K)])

        ###############
        # gradient of #
        #             #
        #  log|lam|   #
        #             #
        ###############

        # 1) wrt to g
        log_det_lam_g_grad = np.array([np.einsum('ij,ji->',
                                                 lam_inv,
                                                 lam_g_gradient[..., r*mlfmobj.dim.N + n])
                                       for r in range(mlfmobj.dim.R)
                                       for n in range(mlfmobj.dim.N)])
        # 2) wrt to theta
        log_det_lam_th_grad = np.array([np.einsum('ij,ji->',
                                                  lam_inv,
                                                  lam_theta_gradient[..., p])
                                        for p in range(theta_phi.size)])

        # 3) wrt to gamma
        log_det_lam_gam_grad = np.array([np.einsum('ij, ji->',
                                                   lam_inv,
                                                   lam_gamma_gradient[..., k])
                                         for k in range(mlfmobj.dim.K)])


        ### Put it all together

        ell_g_grad = -.5*tr_xxt_lam_g_grad + \
                     .5*log_det_lam_g_grad + \
                     ell_gprior_g_grad

        ell_theta_grad = -.5*tr_xxt_lam_th_grad + \
                         .5*log_det_lam_th_grad

        ell_gamma_grad = -.5*tr_xxt_lam_gam_grad + \
                         .5*log_det_lam_gam_grad

        # have to convert to log gamma gradient
        # and stack to single vector
        ell_grad = np.concatenate([ell_g_grad,
                                   ell_theta_grad,
                                   np.exp(log_gamma) * ell_gamma_grad])
        if eval_logpsi_grad:
            ell_grad = np.concatenate((ell_grad, ell_gprior_logpsi_grad))

        return ell, ell_grad

    else:
        return ell    

"""
Simulation
----------

Methods related to simulation
"""

def _get_dense_times(tt, h):
    inds = [0]
    dense_tt = [tt[0]]
    for ta, tb in zip(tt[:-1], tt[1:]):
        _tt = np.linspace(ta, tb, np.ceil((tb-ta)/h + 1))
        dense_tt = np.concatenate((dense_tt, _tt[1:]))
        inds.append(dense_tt.size-1)
    return dense_tt, inds
