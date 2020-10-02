import pandas as pd
import numpy as np
from pdb import set_trace


class my_KMeans:

    def __init__(self, n_clusters=8, init="random", n_init=10, max_iter=300, tol=1e-4):
        # init = {"k-means++", "random"}
        # stop when either # iteration is greater than max_iter or the delta of self.inertia_ is smaller than tol.
        # repeat n_init times and keep the best run (cluster_centers_, inertia_) with the lowest inertia_.
        self.n_clusters = int(n_clusters)
        self.init = init
        self.n_init = n_init
        self.max_iter = int(max_iter)
        self.tol = tol

        self.classes_ = range(n_clusters)
        # Centroids
        self.cluster_centers_ = None
        # Sum of squared distances of samples to their closest cluster center.
        self.inertia_ = None

    def dist(self, a, b):
        # Compute Euclidean distance between a and b
        return np.sum((np.array(a) - np.array(b)) ** 2) ** (0.5)

    def initiate(self, X):
        # Initiate cluster centers
        # Input X is numpy.array
        # Output cluster_centers (list)
        np.random.seed(6)
        if self.init == "random":
            cluster_centers = []
            for _ in range(self.n_clusters):
                rand = np.random.randint(0, (len(X))+1)
                cluster_centers.append(X[rand].tolist())


        elif self.init == "k-means++":
            cluster_centers = [X[0]]
            for _ in range(1, self.n_clusters):
                dist_square = np.array([min([np.inner(c - x, c - x) for c in cluster_centers]) for x in X])
                random = np.random.rand()
                prob = dist_square / dist_square.sum()
                cumulative_pr = prob.cumsum()
                for d, p in enumerate(cumulative_pr):
                    if random < p:
                        break
                cluster_centers.append(X[d])
        else:
            raise Exception("Unknown value of self.init.")
        return cluster_centers

    def fit_once(self, X):
        # Fit once
        # Input X is numpy.array
        # Output: cluster_centers (list), inertia
        # Initiate cluster centers
        cluster_centers = self.initiate(X)
        last_inertia = None
        # Iterate
        for i in range(self.max_iter + 1):
            # Assign each training data point to its nearest cluster_centers
            clusters = [[] for i in range(self.n_clusters)]
            inertia = 0
            for x in X:
                # calculate distances between x and each cluster center
                dists = [self.dist(x, center) for center in cluster_centers]
                # calculate inertia

                inertia += (min(dists)) ** 2
                    # find the cluster that x belongs to
                cluster_id = int(np.where(dists == min(dists))[0][0])
                    # add x to that cluster
                clusters[cluster_id].append(x)
            if (last_inertia and last_inertia - inertia < self.tol) or i == self.max_iter:
                break
            # Update cluster centers
            # cluster_centers = "Write your own code"
            cluster_centers = [np.sum(c,axis=0) / len(c) for c in clusters]

            last_inertia = inertia
        return cluster_centers, last_inertia

    def fit(self, X):
        # X: pd.DataFrame, independent variables, float
        # repeat self.n_init times and keep the best run
        # (self.cluster_centers_, self.inertia_) with the lowest self.inertia_.
        X_feature = X.to_numpy()
        for i in range(self.n_init):
            cluster_centers, inertia = self.fit_once(X_feature)
            if self.inertia_ == None or inertia < self.inertia_:
                self.inertia_ = inertia
                self.cluster_centers_ = cluster_centers
        return

    def transform(self, X):
        # Transform to cluster-distance space
        # X: pd.DataFrame, independent variables, float
        # return dists = list of [dist to centroid 1, dist to centroid 2, ...]
        dists = [[self.dist(x, centroid) for centroid in self.cluster_centers_] for x in X.to_numpy()]
        return dists

    def predict(self, X):
        # X: pd.DataFrame, independent variables, float
        # return predictions: list
        predictions = [np.argmin(dist) for dist in self.transform(X)]
        return predictions

    def fit_predict(self, X):
        self.fit(X)
        return self.predict(X)

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
