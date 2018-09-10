


def ll(obj, y, vecg, phi, gamma, psi, alpha):

    invcov = []

    for k in range(obj.dim.K):

        thetak = np.log(phik)  # sklearn kernel works in the log space
        state_kernel = obj.x_gps[k].kernel.clone_with_theta(thetak)

        Cxx = state_kernel(obj.ttf[:, None]) 
        Cxdx = state_kernel(obj.ttf[:, None], comp='xdx')
        Cdxdx = state_kernel(obj.ttf[:, None], comp='dxdx')

        Lxx = np.linalg.cholesky(Cxx)

        Cdx_x = Cdxdx - Cxdx.T.dot(back_sub(Lxx, Cxdx))

        S = Cdx_x + gamma[k]*np.eye(obj.dim.K)

    # gprior components
    for r in range(obj.dim.R):
        pass
