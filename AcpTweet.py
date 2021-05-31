from sklearn.datasets import load_iris
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


import pprint

from service import rethinkDBservice

users = list(rethinkDBservice.getUsersCursors())
table = []
cmp = 0
for user in users:
    table.append([
        user["avg_hashtag"],
        user["avg_retweet"],
        user["avg_url"],
        user["followers"],
        user["friends"],
        user["mediumLengthTweets"],
        user["rateOfRepliedTweets"],
        user["ratio_frds_flwrs"],
        user["tweet_per_day"],
        user["verified"],
        user["visibility"],
    ])

matriceDonnees = np.array(table)

sc = StandardScaler()
Z = sc.fit_transform(matriceDonnees)

acp = PCA(svd_solver='full')

#calculs des composantes principales
composante_princ = acp.fit_transform(Z)
#nombre de composantes calculées
# print(acp.n_components_) 

# valeur corrigée par les valeurs singulières
n=Z.shape[0]
eigval = acp.singular_values_**2/n

# plt.plot(np.arange(1,11+1),eigval)
# plt.title("Scree plot")
# plt.ylabel("Eigen values")
# plt.xlabel("Factor number")
# plt.show()

# résultat ACP : 3 axes

from mpl_toolkits import mplot3d

fig=plt.figure()
ax = plt.axes(projection='3d')
zline = composante_princ[0]
xline = composante_princ[1]
yline = composante_princ[2]
ax.scatter(xline, yline, zline, 'gray')
ax.view_init(60,35)
ax.set_xlabel('Axe 1')
ax.set_ylabel('Axe 2')
ax.set_zlabel('Axe 3')
plt.show()
