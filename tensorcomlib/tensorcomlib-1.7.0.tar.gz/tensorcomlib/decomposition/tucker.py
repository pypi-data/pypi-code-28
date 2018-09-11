import numpy as np
from tensorcomlib.base import base
from tensorcomlib import tensor
from sklearn.utils.extmath import randomized_svd
from tensorcomlib.matrix import SVD
from matplotlib.pylab import plt
import time
from prettytable import PrettyTable


# hosvd
def hosvd(X):
    U = [None for _ in range(X.ndims())]
    dims = X.ndims()
    S = X
    for d in range(dims):
        C = base.unfold(X, d)
        U1, S1, V1 = np.linalg.svd(C, full_matrices=False)
        S = base.tensor_times_mat(S, U1.T, d)
        U[d] = U1
    core = S
    return U, core


# randomized_hosvd
def randomized_hosvd(X):
    U = [None for _ in range(X.ndims())]
    dims = X.ndims()
    S = X
    for d in range(dims):
        C = base.unfold(X, d)
        U1, S1, V1 = randomized_svd(C, n_components=3, n_oversamples=10, n_iter='auto',
                                    power_iteration_normalizer='auto', transpose='auto',
                                    flip_sign=True, random_state=42)
        S = base.tensor_times_mat(S, U1.T, d)
        U[d] = U1
    core = S
    return U, core


# TruncatedHosvd
def TruncatedHosvd(X, ranks):
    U = [None for _ in range(X.ndims())]
    dims = X.ndims()
    S = X
    R = [None for _ in range(X.ndims())]
    for d in range(dims):
        C = base.unfold(X, d)
        U1, S1, r = SVD.TruncatedSvd(C, rank = ranks[d])
        R[d] = r
        U[d] = U1
        S = base.tensor_times_mat(S, U[d].T, d)
    return U, S


# PartialHosvd
def PartialHosvd(X, ranks):
    U = [None for _ in range(X.ndims())]
    dims = X.ndims()
    S = X
    for d in range(dims):
        C = base.unfold(X, d)
        U1, _, _ = SVD.PartialSvd(C, ranks[d])
        U[d] = U1
        S = base.tensor_times_mat(S, U[d].T, d)
    return U, S


# hooi
def hooi(X, ranks = None,maxiter=1000, init='svd', tol=1e-10, print_enable= False,plot_enable= False):
    time0 = time.time()

    dims = X.ndims()
    modelist = list(range(dims))

    if init == 'hosvd':
        U, core  = TruncatedHosvd(X, ranks)
        data = base.tensor_multi_times_mat(core, U, modelist=modelist, transpose=False)
        error_init = base.tennorm(base.tensor_sub(data, X))/base.tennorm(X)

    if init == 'random':
        U, core = randomized_hosvd(X)
        data = base.tensor_multi_times_mat(core, U, modelist=modelist, transpose=False)
        error_init = base.tennorm(base.tensor_sub(data, X)) / base.tennorm(X)

    error_original = []
    error_iter = []
    error_original.append(error_init)

    normx = base.tennorm(X)
    S1 = X

    for iteration in range(maxiter):
        Uk = [None for _ in range(dims)]
        for i in range(dims):
            U1 = U.copy()
            U1.pop(i)
            L = list(range(dims))
            L.pop(i)
            Y = base.tensor_multi_times_mat(X, U1, modelist=L, transpose=True)
            C = base.unfold(Y, i)
            Uk[i], _, _ = SVD.PartialSvd(C, ranks[i])

        U = Uk

        core = base.tensor_multi_times_mat(X, Uk, list(range(dims)), transpose=True)

        tensor_reconstruction = base.tensor_multi_times_mat(core, Uk, list(range(dims)), transpose=False)
        relative_error = base.tennorm(base.tensor_sub(X, tensor_reconstruction)) / normx
        error_original.append(relative_error)
        error_iter_relative = abs(error_original[-2] - error_original[-1])
        error_iter.append(error_iter_relative)

        if  error_iter_relative < tol:
            if print_enable:

                print('---------------------------->>>>>>')
                print('TruncatedHosvd Init:')
                print('TruncatedHosvd Ranks:\t' + str(ranks))
                print("Truncated error:", error_init)
                print('---------------------------->>>>>>')

                print('\t\tHOOI\tInformation')
                table = PrettyTable(['Iteration','Error_iter','Error_original','Cost Time'])
                table.add_row([iteration,error_iter_relative,relative_error,time.time() - time0])
                table.reversesort = False
                table.border = 1
                print(table)

            break

    if plot_enable:
        plt.plot(error_original,'g*-')
        plt.title('The norm difference between the reduction tensor and the original tensor')
        plt.xlabel('Iteration')
        plt.ylabel('Norm difference')
        plt.show()
        plt.plot(error_iter,'rs-.')
        plt.title('The difference between the norm of restoring tensors in two consecutive iterations')
        plt.xlabel('Iteration')
        plt.ylabel('Norm difference')
        plt.show()

    return U, core

def tucker2tensor(U,core):
    modelist = list(range(len(U)))
    return base.tensor_multi_times_mat(core, U, modelist=modelist, transpose=False)
