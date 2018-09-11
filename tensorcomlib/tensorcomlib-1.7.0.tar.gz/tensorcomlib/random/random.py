import numpy as np
from ..tools import prod
from scipy.stats import norm
from matplotlib.pylab import plt
from tensorcomlib.tensor import tensor
import matplotlib.mlab as mlab


def random_tensor(shape=None, sparsity=0.5, seed=1234, distributed='normal', normal=None, uniform=None, plot=True):
    np.random.seed(seed)
    tensor_size = prod(shape)
    if distributed == 'normal':
        mean, std = normal
        data = np.random.normal(mean, std, tensor_size)

        if plot == True:
            n, bins, patches = plt.hist(data, 30, normed=True, facecolor='blue', alpha=0.5)
            y = mlab.normpdf(bins, mean, std)
            plt.plot(bins, y, 'r--')
            plt.xlabel('Expectation')
            plt.ylabel('Probability')
            plt.title('Histogram of Normal Distribution:$\mu =' + str(mean) + '$, $\sigma=' + str(std) + '$')
            plt.axvline(norm.ppf(sparsity) * std + mean)
            plt.show()

        data[data <= norm.ppf(sparsity) * std + mean] = 0

    if distributed == 'uniform':
        low, high = uniform
        data = np.random.uniform(low, high, size=tensor_size)

        if plot == True:
            n, bins, patches = plt.hist(data, 30, normed=True, facecolor='blue', alpha=0.5)
            plt.xlabel('Expectation')
            plt.ylabel('Probability')
            plt.title('Histogram of Uniform Distribution:$low =' + str(low) + '$, $high =' + str(high) + '$')
            plt.axvline((high - low) * sparsity)
            plt.show()

        data[data <= (high - low) * sparsity] = 0

    return tensor(data.reshape(shape))
