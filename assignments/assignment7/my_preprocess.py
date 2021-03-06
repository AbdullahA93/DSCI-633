import numpy as np
from scipy.linalg import svd
from copy import deepcopy
from collections import Counter
from pdb import set_trace


def pca(X, n_components=5):
    #  Use svd to perform PCA on X
    #  Inputs:
    #     X: input matrix
    #     n_components: number of principal components to keep
    #  Output:
    #     principal_components: the top n_components principal_components
    #     X_pca = X.dot(principal_components)
    U, s, Vh = svd(X)
    v = Vh.transpose()
    principal_components = v[:, :n_components]
    return principal_components


def vector_norm(x, norm="Min-Max"):
    # Calculate the normalized vector
    if norm == "Min-Max":
        x_norm = (x - np.min(x)) / (np.max(x) - np.min(x))
    elif norm == "L1":
        x_norm = x / (np.sum(abs(x)))
        # print(x_norm)
    elif norm == "L2":
        x_norm = x / np.sqrt(np.sum(x ** 2))
        # print(x_norm)
    elif norm == "Standard_Score":
        x_norm = (x - np.mean(x)) / (np.std(x))
        # print(x_norm)
    else:
        raise Exception("Unknown normlization.")
    return x_norm


def normalize(X, norm="Min-Max", axis=1):
    #  Inputs:
    #     X: input matrix
    #     norm = {"L1", "L2", "Min-Max", "Standard_Score"}
    #     axis = 0: normalize rows
    #     axis = 1: normalize columns
    #  Output:
    #     X_norm: normalized matrix (numpy.array)

    X_norm = deepcopy(np.asarray(X))
    m, n = X_norm.shape
    if axis == 1:
        for col in range(n):
            X_norm[:, col] = vector_norm(X_norm[:, col], norm=norm)
    elif axis == 0:
        X_norm = np.array([vector_norm(X_norm[i], norm=norm) for i in range(m)])
    else:
        raise Exception("Unknown axis.")
    return X_norm


def stratified_sampling(y, ratio, replace=True):
    #  Inputs:
    #     y: class labels
    #     0 < ratio < 1: number of samples = len(y) * ratio
    #     replace = True: sample with replacement
    #     replace = False: sample without replacement
    #  Output:
    #     sample: indices of stratified sampled points
    #             (ratio is the same across each class,
    #             samples for each class = int(np.ceil(ratio * # data in each class)) )
    if ratio <= 0 or ratio >= 1:
        raise Exception("ratio must be 0 < ratio < 1.")
    y_array = np.asarray(y)
    # Write your own code below
    sample = []
    count_y = Counter(y_array)
    index_y = {}
    for y in count_y:
        index_y[y] = []
    for label in enumerate(y_array):
        index_y[label[1]].append(label[0])
    for i in count_y:
        n = int(np.ceil(count_y[i] * ratio))
        sample = np.concatenate((sample, np.random.choice(index_y[i], n, replace=replace)))
    return sample.astype(int)
