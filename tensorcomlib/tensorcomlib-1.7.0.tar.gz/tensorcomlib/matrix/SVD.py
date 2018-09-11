import numpy as np

def H(A):
    return np.transpose(np.conjugate(A))

#TruncatedSvd
def TruncatedSvd(X,rank = None):


    U,S,V = np.linalg.svd(X,full_matrices=False)

    U = U[:,:rank].copy()
    S = S[:rank].copy()
    V = V[:rank,:].copy()
    return U,S,V

#PartialSvd
def PartialSvd(X,n):
    U, S, V = np.linalg.svd(X, full_matrices=False)
    U= U[:,:n]
    return U,S,V
