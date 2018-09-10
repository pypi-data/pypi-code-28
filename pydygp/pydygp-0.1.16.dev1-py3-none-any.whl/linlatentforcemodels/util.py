import numpy as np
from scipy.linalg import solve_triangular

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
