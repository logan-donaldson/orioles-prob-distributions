import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from sklearn.mixture import GaussianMixture

# there is an error in the scikilearn implmentation of Kmeans causing
# a memory leak, these lines should both avoid leak and suppress warnings
import os
os.environ["OMP_NUM_THREADS"]="2"
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def gaussian_mixture(data, first, last, plot):
    X = np.array(data)
    # calculate BIC for 1,2,3 and 4 clusters
    BIC = []
    for i in range(1, 5):
        # fit Gaussian Mixture Model
        gmm = GaussianMixture(n_components=i, covariance_type="full", init_params='kmeans', n_init=25, random_state=42).fit(X)
        # store BIC
        BIC.append(gmm.bic(X))

    # choose the number of clusters yeilding the minimum BIC
    optimal_num = BIC.index(min(BIC))

    # fit optimal Gaussian Mixture Model
    gmm = GaussianMixture(n_components=optimal_num, covariance_type="full", init_params='kmeans', n_init=25, random_state=42).fit(X)

    # form grid over data for plotting
    X, Y = np.mgrid[data['Exit Velocity'].min() - 10:data['Exit Velocity'].max() + 10:1, data['Launch Angle'].min() - 10:data['Launch Angle'].max() + 10:1]

    # evaluate density at each point
    pos = np.array([X.ravel(), Y.ravel()]).T
    Z = np.exp(gmm.score_samples(pos))
    Z = Z.reshape(X.shape)
    if plot: plot_heat_map(X, Y, Z, data, first, last)
    return gmm

def plot_heat_map(X, Y, Z, data, first, last):
    #form contour plot
    plt.contourf(X, Y, Z, levels=100,cmap='rocket')
    #overlay actual data points
    plt.scatter(x=data['Exit Velocity'], y=data['Launch Angle'], alpha=0.2, c='white')
    #set chart labels and title
    plt.xlabel('Exit Velocity')
    plt.ylabel('Launch Angle')
    plt.title('')
    if (last[-1] == 's'): plt.title(first + " " + last + "' Probability Density Estimate")
    else: plt.title(first + " " + last + "'s Probability Density Estimate")
    plt.show()

def similarity_score(df1, df2, first1, last1, first2, last2):
    data1, data2 = df1, df2
    frames = [data1, data2]
    data = pd.concat(frames)

    gmm1 = gaussian_mixture(df1, first1, last1, False)
    gmm2 = gaussian_mixture(df2, first2, last2, False)

    X, Y = np.mgrid[data['Exit Velocity'].min() - 10:data['Exit Velocity'].max() + 10:1,
           data['Launch Angle'].min() - 10:data['Launch Angle'].max() + 10:1]

    # evaluate density at each point
    pos = np.array([X.ravel(), Y.ravel()]).T
    Z1 = np.exp(gmm1.score_samples(pos))
    Z2 = np.exp(gmm2.score_samples(pos))
    Z = Z1 - Z2
    similarity_score = np.sum(np.abs(Z))
    return similarity_score
