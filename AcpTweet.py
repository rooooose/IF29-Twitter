from sklearn.datasets import load_iris
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import pandas


import pprint

from service import rethinkDBservice

users = list(rethinkDBservice.getUsersCursors())
# table = [["avg_hashtag","avg_retweet","avg_url","followers","friends","mediumLengthTweets","rateOfRepliedTweets","ratio_frds_flwrs","tweet_per_day","verified","visibility"]]
table=[]
etiquettes = []
cmp = 0
for user in users:
    table.append([
        user["accountAge(days)"],
        user["agressivite"],
        user["avg_hashtag"],
        user["avg_url"],
        user["mediumLength"],
        user["rationFollowersFriends"],
        user["tweet_per_day"],
        user["verified"],
        user["visibility"]
    ])
    etiquettes.append(user["suspect"])
    cmp+=1
    # print(cmp)
matriceDonnees = np.array(table)
# print(matriceDonnees)

sc = StandardScaler()
Z = sc.fit_transform(matriceDonnees)

acp = PCA(svd_solver='full')

#calculs des composantes principales
composante_princ = acp.fit_transform(Z)
# print(composante_princ[0])
#nombre de composantes calculées
# print(acp.n_components_) 

# valeur corrigée par les valeurs singulières
n=Z.shape[0]
eigval = acp.singular_values_**2/n

plt.plot(np.arange(1,9+1),eigval)
plt.title("Scree plot")
plt.ylabel("Eigen values")
plt.xlabel("Factor number")
# plt.show()

# résultat ACP : 3 axes

# from mpl_toolkits import mplot3d

# fig=plt.figure()
# ax = plt.axes(projection='3d')

idx = np.random.randint(len(matriceDonnees), size=1000)
sample_etiquettes = np.array(etiquettes)[idx]

xline = composante_princ[idx,0]
yline = composante_princ[idx,1]
zline = composante_princ[idx,2]
# plt.scatter(xline, yline, zline, 'gray')
# ax.view_init(60,35)
# ax.set_xlabel('Axe 1')
# ax.set_ylabel('Axe 2')
# ax.set_zlabel('Axe 3')

plt.figure("Data representation")

plt.scatter(xline, yline)

plt.ylabel("Axis 2")
plt.xlabel("Axis 1")



# graphique avec croisement deux à deux
from pandas.plotting import scatter_matrix
dataFrameDonnees = pandas.DataFrame(data=matriceDonnees[idx,:], columns=["accountAge(days)", "agressivite","avg_hashtag","avg_url","mediumLength","rationFollowersFriends","tweet_per_day","verified","visibility"])
pandas.plotting.scatter_matrix(dataFrameDonnees,figsize=(9,9))
# plt.show()