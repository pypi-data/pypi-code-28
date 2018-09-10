import numpy as np
import sklearn.gaussian_process.kernels as sklearn_kernels
import warnings
from .util import BlockCovar, back_sub
from pydygp import nssolve
from collections import namedtuple
from scipy.linalg import block_diag, cho_solve
from scipy import sparse
from scipy.optimize import minimize
from sklearn.gaussian_process import GaussianProcessRegressor


class SuccApproxLatentState:

    def __init__(self, kernel, alpha=1e-5):
        self.kernel = kernel  # must be a Gradient kernel (add check)
        self.alpha = alpha    # small value to jitter cov. matrices

class LatentForce(GaussianProcessRegressor):

    def __init__(self, kernel):
        super(LatentForce, self).__init__(kernel=kernel,
                                          alpha=1e-3,
                                          n_restarts_optimizer=2)


Dimensions = namedtuple('Dimensions', 'N K R')

class MLFMSuccApprox:

    def __init__(self, struct_mats, order=1):
        self.order = order # no. of succ. approx. performed
        self.struct_mats = np.asarray(struct_mats)
        self.dim = Dimensions(None, struct_mats[0].shape[0], len(struct_mats)-1)

    def setup_latentstates(self, kernels=None):
        if kernels is None:
            ls_kernels = []
            for k in range(self.dim.K):
                ls_kernels.append(sklearn_kernels.ConstantKernel(1.)*
                                  sklearn_kernels.RBF(1.))
            self.latentstates = [SuccApproxLatentState(kern)
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

        # add a clone of kernel for optimisation
        for lf in self.latentforces:
            lf.kernel_ = lf.kernel.clone_with_theta(lf.kernel.theta)

    def setup_dataprecisions(self):
        self.dataprecisions = 1e4*np.ones(self.dim.K)

    def setup_times(self, data_times, h=None):
        """
        Sets up the intervals and handles the number of times in each intervals.
        """
        intervals = [nssolve.ns_util.Interval(ta, tb)
                     for ta, tb in zip(data_times[:-1], data_times[1:])]
        data_inds = [0]
        for I in intervals:
            I.set_quad_style(h=h)
            data_inds.append(data_inds[-1]+I.tt.size-1)

        self.data_times = data_times
        self.intervals = intervals
        self.comp_times = nssolve.ns_util.get_times(self.intervals)
        self.data_inds = data_inds
        self.dim = Dimensions(self.comp_times.size, self.dim.K, self.dim.R)
        

    def setup_operator(self, ifix=0):
        """
        Setup for the successive approximation operator.
        """
        ifix = len(self.intervals) // 2
        self.t0 = self.intervals[ifix].ta
        nsop = nssolve.QuadOperator(fp_ind=ifix,
                                    method='single_fp',
                                    intervals=self.intervals,
                                    K=self.dim.K,
                                    R=self.dim.R,
                                    struct_mats=self.struct_mats,
                                    is_x_vec=True)
        self.nsop = nsop


    def em_fit(self, times, Y, g=None,
               gtol=1e-3):
        for attr in ['latentstates',
                     'latentforces',
                     'dataprecisions']:
            if not hasattr(self, attr):
                getattr(self, 'setup_'+attr)()
        self.setup_times(times)
        self.setup_operator()

        if Y.shape[0] != self.data_times.size \
           or Y.shape[1] != self.dim.K:
            raise ValueError("Y must be of shape (n_data_times, n_features)")
        self.Y = Y
        self.vecy = Y.T.ravel()

        #Gamma = block_diag(*[np.eye(self.dim.N)*1e-4]*self.dim.K)
        # smooth realisation of Gamma
        Gamma = []
        for ls in self.latentstates:
            kern = ls.kernel
            K = kern(self.ttf[:, None])
            Gamma.append(K*1e-3)
        Gamma = block_diag(*Gamma)
        
        
        theta = _get_latentstate_theta(self)
        Sigma = block_diag(*[np.eye(self.data_times.size)/tau
                             for tau in self.dataprecisions])


        elltol2 = 1e-3
        update_gamma = True

        emopt = EMopt_MLFMSuccApprox(self)


        if g is None:
            g, logpsi = adapgrad_initalisation(times, Y, self)
        else:
            logpsi = _get_latentforce_theta(self)

        Ex, Varx, pwCovx = Estep_LDS(g, Gamma, Sigma, theta, self)

        # initalise by "good guess" of X distribution
        #Ex, Varx, pwCovx = _initalise_X_dist(Sigma, Gamma, self)
        #g = np.zeros(self.dim.N*self.dim.R)
        #logpsi = _get_latentforce_theta(self)
        

        gcur = g.copy()        
        elltol = 1e-3
        ell = loglik(g, self.vecy, Sigma, Gamma, theta, self)

        elldiff = np.inf
        gdelt = np.inf
        
        while True:

            init = np.concatenate((g, logpsi))

            if elldiff < 1e-2:
                # don't update the hyper parameters until
                # latent force begins to stabilise
                update_lp = True
            else:
                update_lp = True
                
            g, logpsi = emopt.Mstep(g, logpsi, Gamma,
                                Ex, Varx, pwCovx, update_logpsi=update_lp)
            Ex, Varx, pwCovx = Estep_LDS(g, Gamma, Sigma, theta, self)
            #print(logpsi)
            #if update_gamma:
            #    Gamma = Gamma_Update(g, Ex, Varx, pwCovx, self)

            #print(g)

            ####
            #gp.fit(self.ttf[:, None], g)
            #Cgg = gp.kernel_(self.ttf[:, None]) + np.eye(self.dim.N)*1e-4
            #Lgg = np.linalg.cholesky(Cgg)
            print(g)
            ellnew = loglik(g, self.vecy, Sigma, Gamma, theta, self)
            #if np.linalg.norm(g-gcur) < 1e-6:
            #    break
            elldiff = ellnew - ell
            if update_gamma:
                pass

            
            if abs(elldiff) < elltol:
                pass
                #update_gamma = True

            if abs(elldiff) < elltol2:
                pass
                #break
                #print(np.linalg.norm(g - gcur))

            gdelt = np.max(np.abs(g - gcur))
            print(ell, elldiff, gdelt)
            if gdelt < gtol:
                print("Latent force converged with gdelt {} < {}".format(gdelt, gtol))
                break
            #print(ellnew, elldiff, gdelt)
            
            gcur = g
            ell = ellnew

        return g

    def em_setup(self, times, Y):
        for attr in ['latentstates',
                     'latentforces',
                     'dataprecisions']:
            if not hasattr(self, attr):
                getattr(self, 'setup_'+attr)()
        self.setup_times(times)
        self.setup_operator()
        
        if Y.shape[0] != self.data_times.size \
           or Y.shape[1] != self.dim.K:
            raise ValueError("Y must be of shape (n_data_times, n_features)")
        self.Y = Y
        self.vecy = Y.T.ravel()

        self.emopt = EMopt_MLFMSuccApprox(self)

        # initalise free parameters
        self.g_ = np.zeros(self.dim.N*self.dim.R)
        self.theta_ = _get_latentstate_theta(self)
        self.Gamma_ = block_diag(*[np.eye(self.dim.N)*1e-4]*self.dim.K)
        self.Sigma_ = block_diag(*[np.eye(self.data_times.size)/tau
                                   for tau in self.dataprecisions])        

    def em_batchfit(self, times, Y):

        n_batches = 2

        # create the batches
        sub_arr = np.array_split(np.arange(times.size), 2)

        # add some overlap
        sub_arr[0] = np.concatenate((sub_arr[0], [sub_arr[1][0]]))
        sub_arr[1] = np.concatenate(([sub_arr[0][-2]], sub_arr[1]))
        
        batch_mlfms = [MLFMSuccApprox(self.struct_mats, self.order)
                       for n in range(n_batches)]

        # initalise global gp hyperparameters
        logphi = np.zeros(self.dim.R*2)
        g = np.cos(times)

        for mlfm, ind in zip(batch_mlfms, sub_arr):
            mlfm.em_setup(times[ind], Y[ind, :])

            #Ex, Varx, pwCovx = Estep_LDS(g[ind],
            #                         mlfm.Gamma_,
            #                         mlfm.Sigma_,
            #                         mlfm.theta_, mlfm)
            #print(np.diag(Varx[-1]))
        

    def loglikelihood(self, g, logphi, logpsi):
        """
        Returns the model log-likelihood
        """
        # contribution to the loglikelihood from g prior
        ell_gprior,_,_ = log_likelihood_gprior(g, logpsi, self)

        # recursively construct the cov. function

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


class EMopt_MLFMSuccApprox:
    """
    EM optimisation routine for MLFM using successive approximations.
    """
    def __init__(self, mlfm):
        self.mlfm = mlfm  # attach the mlfm model

    def Estep(self, g, Gamma, Sigma, logphi):
        Ex, Varx, pwCovx = Estep_LDS(g, Gamma, Sigma, logphi, self.mlfm)
        return Ex, Varx, pwCovx

    def Mstep(self, g0, logpsi0, Gamma, Ex, Varx, pwCovx, update_logpsi=True):

        NR = self.mlfm.dim.N*self.mlfm.dim.R
        def _objfunc(arg):
            # unpack
            if update_logpsi:
                g = arg[:NR]
                logpsi = arg[NR:]
            else:
                g = arg
                logpsi = logpsi0
                
            ell, ell_grad = EM_Mstep_objfunc(g, logpsi, Gamma,
                                             Ex, Varx, pwCovx,
                                             self.mlfm, logpsi_grad=update_logpsi)
            # switch to minimisation problem
            return -ell, -ell_grad

        if update_logpsi:
            init = np.concatenate((g0, logpsi0))
        else:
            init = g0

        res = minimize(_objfunc, init, jac=True)

        if update_logpsi:
            ghat = res.x[:NR]
            logpsi = res.x[NR:]
        else:
            ghat = res.x
            logpsi = logpsi0

        return ghat, logpsi
        

    def latentforce_hyperpar_update(self, g):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            #opt_kernels = []
            g = g.reshape(self.mlfm.dim.R, self.mlfm.dim.N)
            for r, lf in enumerate(self.mlfm.latentforces):
                lf.fit(self.mlfm.ttf[:, None], g[r, :])                

                #kern = lf.kernel.clone_with_theta(lf.kernel.theta)
                #gpr = GaussianProcessRegressor(kern)
                #gpr.n_restarts_optimizer = 2
                #lf.kernel_ = 
                #opt_kernels.append(gpr.kernel_)

            # overwrite the latent forces
            #self.mlfm.latentforces = [LatentForce(kern)
            #                          for kern in opt_kernels]


def Estep_LDS(g, Gamma, Sigma, logphi, mlfmobj):
    """
    Uses Kalman filtering to compute the E-step 
    """
    NK = mlfmobj.dim.N*mlfmobj.dim.K
    order = mlfmobj.order

    # LDS model parameters
    # - notation used is as in Bishop PRML
    C = mlfmobj.sparse_data_map
    A = mlfmobj.nsop.x_transform(g, is_x_input_vec=True)
    At = A.T
    x = mlfmobj.vecy

    # inital cov. matrix of x_0
    # chol decomp. of Cov{x0_k} k=1,...K
    xcov_chol_ls = _handle_covar(logphi,
                                 mlfmobj.ttf, mlfmobj.latentstates,
                                 _get_latentstate_theta_shape(mlfmobj))

    ################
    # Forward Pass #
    ################

    # initial means is zero so for. means are zero...
    f_means = [0]*order
    # ...apart from the final which includes the data observations

    # forward pass of the cov.
    f_covs = [block_diag(*[L.dot(L.T) for L in xcov_chol_ls])]
    for n in range(order - 1):
        f_covs.append(A.dot(f_covs[-1].dot(A.T)) + Gamma)
    
    # final forward moments include data observations
    P = A.dot(f_covs[-1].dot(A.T)) + Gamma
    CP = C.dot(P)
    # Final Kaman gain matrix
    K = CP.T.dot(np.linalg.inv(C.dot(CP.T) + Sigma))
    f_means.append(K.dot(x))
    f_covs.append(P - K.dot(CP))

    #################
    # Backward pass #
    #################
    means = [f_means[-1]]
    covs = [f_covs[-1]]
    pw_covs = []
    for n in range(order):
        Vn = f_covs[-(n+2)]
        VnAt = Vn.dot(At)        
        Pn = A.dot(VnAt) + Gamma
        Pn_chol = np.linalg.cholesky(Pn)

        mhat_n = VnAt.dot(back_sub(Pn_chol, means[0]))

        # add new mean to the front of means
        means = [mhat_n] + means
        Pninv = np.linalg.inv(Pn)
        expr1 = covs[0].dot(Pninv)

        Vhat_n = back_sub(Pn_chol, back_sub(Pn_chol, covs[0]).T - np.eye(NK))
        Vhat_n = Vn + VnAt.dot(Vhat_n.dot(VnAt.T))

        # construct the pairwise cov
        # cov{z_n, z_{n+1}}
        # add pw cov to font
        pw_covs = [VnAt.dot(back_sub(Pn_chol, covs[0]))] + pw_covs

        # add new cov to the fron of covs
        covs = [Vhat_n] + covs

    return means, covs, pw_covs




def Mstep_objfunc(g, Ex, Varx, pwCovx, Gamma, mlfmobj):
    K = mlfmobj.nsop.x_transform(g, is_x_input_vec=True)

    # z := x[i+1] - K x[i]

    EzzT = []
    for i in range(mlfmobj.order):
        KExxTKT = K.dot((Varx[i] + np.outer(Ex[i], Ex[i])).dot(K.T))
        ExxT = Varx[i+1] + np.outer(Ex[i+1], Ex[i+1])
        ExxpT = pwCovx[i] + np.outer(Ex[i], Ex[i+1])

        KExxpT = K.dot(ExxpT)

        EzzT.append(KExxTKT + ExxT - \
                    KExxpT - KExxpT.T)

    GammaInv = np.linalg.inv(Gamma)
    s, logdet = np.linalg.slogdet(Gamma)
    res = -.5*sum(np.trace(ezzt.dot(GammaInv)) for ezzt in EzzT) - \
           .5*mlfmobj.order*logdet
    return res
"""
Handler functions
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

def _get_latentstate_theta(mlfmobj):
    return np.concatenate([gp.kernel.theta
                           for gp in mlfmobj.latentstates])

def _get_latentforce_theta(mlfmobj, opt_kern=True):
    if opt_kern:
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


def _handle_covar(theta, tt, gp_list, theta_shape):
    theta = theta.reshape(theta_shape)
    res = []
    for k, gp in enumerate(gp_list):
        kern = gp.kernel.clone_with_theta(theta[k])
        K = kern(tt[:, None]) + np.eye(tt.size)*gp.alpha
        res.append(np.linalg.cholesky(K))
    return res
                   

####

def Gamma_Update(g, Ex, Varx, pwCovx, mlfmobj):
    K = mlfmobj.nsop.x_transform(g, is_x_input_vec=True)
    #K = sparse.csr_matrix(K)
    # z := x[i+1] - K x[i]

    EzzT = []
    for i in range(mlfmobj.order):
        KExxTKT = K.dot((Varx[i] + np.outer(Ex[i], Ex[i])).dot(K.T))
        ExxT = Varx[i+1] + np.outer(Ex[i+1], Ex[i+1])
        ExxpT = pwCovx[i] + np.outer(Ex[i], Ex[i+1])

        KExxpT = K.dot(ExxpT)

        EzzT.append(KExxTKT + ExxT - \
                    KExxpT - KExxpT.T)

    Gamma = sum(EzzT)/mlfmobj.order
    Gamma += np.diag(1e-5*np.ones(Gamma.shape[0]))

    return Gamma


def foo(g, Ex, Varx, pwCovx, Gamma, mlfmobj):
    K = mlfmobj.nsop.x_transform(g, is_x_input_vec=True)
    vk = K.T.ravel()

    EzzT = []
    for i in range(mlfmobj.order):
        KExxTKT = K.dot((Varx[i] + np.outer(Ex[i], Ex[i])).dot(K.T))
        ExxT = Varx[i+1] + np.outer(Ex[i+1], Ex[i+1])
        ExxpT = pwCovx[i] + np.outer(Ex[i], Ex[i+1])

        KExxpT = K.dot(ExxpT)

        EzzT.append(KExxTKT + ExxT - \
                    KExxpT - KExxpT.T)

    GammaInv = np.linalg.inv(Gamma)
    Gamma_gradient = .5*(mlfmobj.order*GammaInv - GammaInv.dot(sum(EzzT).dot(GammaInv)))
    

    M1 = sum([vxi + np.outer(exi, exi)
              for exi, vxi in zip(Ex[:-1], Varx[:-1])])
    M2 = sum([pwCovx[i] + np.outer(Ex[i], Ex[i+1])
              for i in range(mlfmobj.order)])

    L = np.kron(M1, GammaInv)

    vecGammainvM2t = M2.T.dot(GammaInv).T.ravel()
    val = vk.dot(L.dot(vk)) - 2*np.dot(vecGammainvM2t, vk)

    M3 = sum([vxi + np.outer(exi, exi)
              for exi, vxi in zip(Ex[1: ], Varx[1: ])])
    #val += np.trace(M3.dot(GammaInv))
    val = -2*Mstep_objfunc(g, Ex, Varx, pwCovx, Gamma, mlfmobj)


    # foo grad
    A, b = mlfmobj.sparse_vecK_aff_rep
    A = A.tocsc()       # A has sparse columns
    At = A.transpose()  # should be a sparse csr_matrix

    AtL = At.dot(L)
    AtLA = At.dot(AtL.T)
    AtLb = b.dot(AtL.T)

    grad = 2*(AtLA.dot(g) + AtLb.ravel())
    #grad = 2*A.transpose().dot( (A.dot(g) + b).dot(L).T)
    grad -= (2*A.transpose().dot(vecGammainvM2t[:, None])).ravel()

    return -.5*val, -.5*np.array(grad).ravel()#, Gamma_gradient


def foo2(g, Ex, Varx, pwCovx, Gamma, mlfmobj):
    K = mlfmobj.nsop.x_transform(g, is_x_input_vec=True)

    M11, M12, M22 = ([], [], [])
    for i in range(mlfmobj.order):
        M11.append( Varx[i] + np.outer(Ex[i], Ex[i]) )
        M12.append( pwCovx[i] + np.outer(Ex[i], Ex[i+1]) )
        M22.append( Varx[i+1] + np.outer(Ex[i+1], Ex[i+1]) )
    M11 = sum(M11)
    M12 = sum(M12)
    M22 = sum(M22)

    _, logdetGamma = np.linalg.slogdet(Gamma)
    GammaInv = np.linalg.inv(Gamma)

    Q = -.5*np.trace( (K.dot(M11.dot(K.T)) - \
                       2*K.dot(M12) + \
                       M22).dot(GammaInv) )
    Q -= .5*mlfmobj.order*logdetGamma

    #### gradient wrt g
    A, _ = mlfmobj.sparse_vecK_aff_rep
    A = A.tocsc()
    At = A.transpose()
    w = (M11.dot(K.T) - M12).dot(GammaInv)
    Q_g_gradient = -At.dot(w.ravel())

    #### gradient wrt Gamma
    Q_G_gradient = -0.5*(mlfmobj.order*GammaInv - \
                         GammaInv.dot(K.dot(M11).dot(K.T) - \
                                      K.dot(M12) - M12.T.dot(K.T) + \
                                      M22).dot(GammaInv))

    return Q, Q_g_gradient, Q_G_gradient

def foo2_opt(Ex, Varx, pwCovx, Gamma, mlfmobj):
    K = mlfmobj.nsop.x_transform(g, is_x_input_vec=True)

    M11, M12, M22 = ([], [], [])
    for i in range(mlfmobj.order):
        M11.append( Varx[i] + np.outer(Ex[i], Ex[i]) )
        M12.append( pwCovx[i] + np.outer(Ex[i], Ex[i+1]) )
        M22.append( Varx[i+1] + np.outer(Ex[i+1], Ex[i+1]) )
    M11 = sum(M11)
    M12 = sum(M12)
    M22 = sum(M22)
    

from scipy.stats import multivariate_normal
def loglik(g, y, Sigma, Gamma, theta, mlfmobj):
    K = mlfmobj.nsop.x_transform(g, is_x_input_vec=True)

    # inital cov. matrix of x_0
    # chol decomp. of Cov{x0_k} k=1,...K
    xcov_chol_ls = _handle_covar(theta,
                                 mlfmobj.ttf, mlfmobj.latentstates,
                                 _get_latentstate_theta_shape(mlfmobj))
    C = block_diag(*[L.dot(L.T) for L in xcov_chol_ls])

    for m in range(mlfmobj.order):
        C = K.dot(C.dot(K.T)) + Gamma

    D = mlfmobj.data_map
    C = D.dot(C.dot(D.T)) + Sigma
    return multivariate_normal.logpdf(y, np.zeros(y.shape), C)


def _initalise_X_dist(Sigma, Gamma, mlfmobj):
    """
    Initalise the distribution of X by
    """
    xk = [np.interp(mlfmobj.ttf,
                    mlfmobj.data_times,
                    yk)
          for yk in mlfmobj.Y.T]

    Ex = [np.concatenate(xk)]*(mlfmobj.order+1)
    Varx = [1e-1*np.eye(mlfmobj.dim.N*mlfmobj.dim.K)]*len(Ex)
    Covx = [np.zeros(Varx[0].shape)]*(len(Ex)-1)

    return Ex, Varx, Covx

"""
Component log likelihood functions
----------------------------------
"""
def ell_g_prior_r(r, g, thetar, mlfmobj, eval_gradient=True):
    """
    Value and gradient log prior of g
    """
    kernel = mlfmobj.latentforces[r].kernel_.clone_with_theta(thetar)

    K, K_gradient = kernel(mlfmobj.ttf[:, None], eval_gradient=True)
    K[np.diag_indices_from(K)] += mlfmobj.latentforces[r].alpha

    try:
        L = np.linalg.cholesky(K)
    except np.linalg.LinAlgError:
        return (-np.inf, np.zeros((g.size, 1)), np.zeros_like(thetar))


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
def EM_Mstep_objfunc(g, logpsi, Gamma, Ex, Varx, pwCovx, mlfmobj, logpsi_grad=False):

    # MAP contribution from log prior ln p(g)
    gprior_tup = log_likelihood_g_prior(g, logpsi, mlfmobj, eval_gradient=True)
    ell_gprior = gprior_tup[0]
    ell_gprior_g_grad = gprior_tup[1]
    ell_gprior_logpsi_grad = gprior_tup[2]

    # contribution from LDS model
    ll, ll_g_grad, _ = foo2(g, Ex, Varx, pwCovx, Gamma, mlfmobj)

    Q = ll + ell_gprior
    Q_g_gradient = ell_gprior_g_grad + ll_g_grad
    Q_logpsi_gradient = ell_gprior_logpsi_grad

    if logpsi_grad:
        Q_gradient = np.concatenate((Q_g_gradient, Q_logpsi_gradient))
    else:
        Q_gradient = Q_g_gradient

    return Q, Q_gradient

"""
Initalisation Strategies
------------------------
"""
def adapgrad_initalisation(times, Y, mlfmobj):
    from pydygp.linlatentforcemodels import MLFMAdapGrad
    mlfm_adapgrad = MLFMAdapGrad(mlfmobj.struct_mats)
    res = mlfm_adapgrad.em_fit(times, Y, gtol=1e-2)
    g = res.g.reshape(mlfm_adapgrad.dim.R, mlfm_adapgrad.dim.N)

    gpred = []
    logpsi = []
    for g, lf in zip(g, mlfm_adapgrad.latentforces):
        kern = lf.kernel_
        gpr = GaussianProcessRegressor(kern)
        gpr.fit(times[:, None], g)

        gpred.append(gpr.predict(mlfmobj.ttf[:, None]))
        logpsi.append(gpr.kernel_.theta)
    print("Successive approximation method initalised")
    return np.concatenate((gpred)), np.concatenate((logpsi))

# attempt to initialise by fitting a linear dynamical system
