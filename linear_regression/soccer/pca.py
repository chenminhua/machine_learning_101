import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from sklearn import decomposition

stats = pd.read_table('../../data/regression.csv')
point = stats.iloc[:, 4] / 38
positional_rating = stats.iloc[:, [0, 1, 2, 3]]

pca = decomposition.PCA()
pca.fit(positional_rating)
# 各个成分具有的方差
print("The princapal components have variances: \n", pca.explained_variance_)
# 各个成分方差占据的比重
print("THe principal componetns have variance ratios: \n",
      pca.explained_variance_ratio_)

pca2 = decomposition.PCA(n_components=2)
pca2.fit(positional_rating)
# 只保留两维的成分
ratings_new = pca2.transform(positional_rating)

plt.scatter(ratings_new[:, 0], ratings_new[:, 1], c='r', marker='o')
plt.title("PCA with 2 components")
plt.show()
