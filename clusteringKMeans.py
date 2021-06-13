# -*- coding: utf-8 -*-
# Ce code a été produit par le Pr Ricco R. de l'univ. de Lyon 2
#Utilisé et modifié par Kenza TAAMMA et Bertille TEMPLE (création des projections 2D et 3D, ainsi que de la classification d'un nouvel utilisateur)

#modification du dossier par défaut
import os
os.chdir("./")#votre dossier

#importation des données
import pandas

from sklearn.datasets import load_iris
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from sklearn import cluster

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

dataFrameDonnees = pandas.DataFrame(data=matriceDonnees, columns=["avg_hashtag", "avg_retweet", "avg_url", "followers", "friends", "mediumLengthTweets", "rateOfRepliedTweets", "ratio_frds_flwrs", "tweet_per_day", "verified", "visibility"])

#dimension des données
print(dataFrameDonnees.shape)

#6 premières lignes des données
print(dataFrameDonnees.iloc[0:6,:])

#statistiques descriptives
print(dataFrameDonnees.describe())

# #graphique avec croisement deux à deux
# from pandas.plotting import scatter_matrix
# pandas.plotting.scatter_matrix(dataFrameDonnees,figsize=(11,11)) 

#centrage réduction des données
from sklearn import preprocessing
dataFrameDonnees_cr = preprocessing.scale(dataFrameDonnees)

#librairie pour évaluation des partitions
from sklearn import metrics

#utilisation de la métrique "silhouette"
#faire varier le nombre de clusters de 2 à 10
res = np.arange(10,dtype="double")
for k in np.arange(10):
    km = cluster.KMeans(n_clusters=k+2)
    km.fit(dataFrameDonnees_cr)
    res[k] = metrics.silhouette_score(dataFrameDonnees_cr,km.labels_)

#graphique
import matplotlib.pyplot as plt
plt.title("Silhouette")
plt.xlabel("# of clusters")
# plt.plot(np.arange(2,11,1),res)
plt.plot(np.arange(2,12,1),res)
plt.show()

# =============== Fonction déroulant l'étude du clustering KMeans sur notre dataset =============== #
# =============== En fonction du nombre de cluster passé en argument =============== #

def clusteringKmeans(nb_cluster):
    #k-means sur les données centrées et réduites
    kmeans = cluster.KMeans(n_clusters=nb_cluster)
    kmeans.fit(dataFrameDonnees_cr)
    # print(kmeans.inertia_)

    #index triés des groupes
    idk = np.argsort(kmeans.labels_)

    #affichage des observations et leurs groupes
    print(pandas.DataFrame(dataFrameDonnees.index[idk],kmeans.labels_[idk]))

    #distances aux centres de classes des observations
    print(kmeans.transform(dataFrameDonnees_cr))

    #moyenne par variable
    m = dataFrameDonnees.mean()

    # #TSS
    # TSS = dataFrameDonnees.shape[0]*dataFrameDonnees.var(ddof=0)
    # print(TSS)

    #data.frame conditionnellement aux groupes
    gb = dataFrameDonnees.groupby(kmeans.labels_)

    # #effectifs conditionnels
    # nk = gb.size()
    # print(nk)

    # #moyennes conditionnelles
    # mk = gb.mean()
    # print(mk)

    # #pour chaque groupe ecart à la moyenne par variable
    # EMk = (mk-m)**2

    # #pondéré par les effectifs du groupe
    # EM = EMk.multiply(nk,axis=0)

    # #somme des valeurs => BSS
    # BSS = np.sum(EM,axis=0)
    # print(BSS)

    # #carré du rapport de corrélation
    # #variance expliquée par l'appartenance aux groupes
    # #pour chaque variable
    # R2 = BSS/TSS
    # print("##################### R2 ####################")
    # print(R2)

    #ACP pour affichage
    from sklearn.decomposition import PCA
    acp = PCA(n_components=2).fit_transform(dataFrameDonnees_cr)
    # print("#### ACP #####")
    # print (acp)

    # ------- Projection 2D ------- #

    # discrétise l'échelle de couleur viridis pour l'affichage
    cmap = plt.get_cmap("viridis", nb_cluster)

    # création du dataframe avec les CP et les labels correspondants par concaténation
    acp_df = pandas.DataFrame(data=acp[:,:2], columns=["CP1", "CP2"])
    labels = pandas.DataFrame(data=kmeans.labels_, columns=["label"])
    labeled_acp = pandas.concat([acp_df, labels], axis=1)
    print("----------- labeled acp -----------")
    print(labeled_acp)

    # création des groupes pour l'affichage
    clusters = labeled_acp.groupby("label")
    # projection dans le plan factoriel
    # avec un code couleur selon le groupe
    # plt.scatter(acp[:,0],acp[:,1], c=kmeans.labels_, cmap='viridis', label = name) #sans le groupby et l'affichage des legendes
    for name, group in clusters :
        plt.scatter(group["CP1"],group["CP2"], color=cmap(int(name)), label = name) 
    plt.xlabel("Composante Principale 1")
    plt.ylabel("Composante Principale 2")
    plt.title("Clustering KMeans "+ str(nb_cluster) + " clusters - projection 2D")
    plt.legend() 

    # ------- Projection 3D ------- #

    # ACP pour affichage 3D
    acp = PCA(n_components=3).fit_transform(dataFrameDonnees_cr)
    # création du dataframe concaténé aux labels
    acp_df = pandas.DataFrame(data=acp[:,:3], columns=["CP1", "CP2", "CP3"])
    labels = pandas.DataFrame(data=kmeans.labels_, columns=["label"])
    labeled_acp = pandas.concat([acp_df, labels], axis=1)
    # création des groupes pour l'affichage
    clusters = labeled_acp.groupby("label")

    # projection 3D
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(acp[:,0],acp[:,1],acp[:,2], c=kmeans.labels_, cmap='viridis', edgecolor='k', s=40, alpha = 0.5) #sans le groupby et l'affichage des legendes
    for name, group in clusters :
        ax.scatter(group["CP1"],group["CP2"], group["CP3"], color=cmap(int(name)), edgecolor='k', s=40, alpha = 0.5, label = name)
    ax.view_init(60,35)
    ax.set_title("Clustering KMeans "+ str(nb_cluster) + " clusters - projection 3D")
    ax.set_xlabel("Composante principale 1")
    ax.set_ylabel("Composante principale 2")
    ax.set_zlabel("Composante principale 3")
    ax.dist = 10

    ax.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], kmeans.cluster_centers_[:,2], c='black', s=200, alpha=0.5, label = 'Centroid')
    plt.legend() 
    plt.autoscale(enable=True, axis='x', tight=True)    

    # autre projection 3D - rotation pour une meilleure visualisation
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(acp[:,0],acp[:,1],acp[:,2], c=kmeans.labels_, cmap='viridis', edgecolor='k', s=40, alpha = 0.5) #sans le groupby et l'affichage des legendes
    for name, group in clusters :
        ax.scatter(group["CP1"],group["CP2"], group["CP3"], color=cmap(int(name)), edgecolor='k', s=40, alpha = 0.5, label = name)

    ax.set_title("Clustering KMeans "+ str(nb_cluster) + " clusters - projection 3D")
    ax.set_xlabel("Composante principale 1")
    ax.set_ylabel("Composante principale 2")
    ax.set_zlabel("Composante principale 3")
    ax.dist = 10

    ax.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], kmeans.cluster_centers_[:,2], c='black', s=200, alpha=0.5, label = 'Centroid')
    plt.legend() 
    plt.autoscale(enable=True, axis='x', tight=True)    

    # affichage des 3 graphiques (2D et 3D)
    plt.show()


# =============== Etude clustering KMeans sur notre dataset =============== #

print(" ----------- 2 clusters -----------")
clusteringKmeans(2)
print(" ----------- 3 clusters -----------")
clusteringKmeans(3)
print(" ----------- 4 clusters -----------")
clusteringKmeans(4)



# =============== Fonction pour assigner un cluster à une nouvelle valeure =============== #

def classerNewUserKMeans(user, nb_cluster):
    kmeans = cluster.KMeans(n_clusters=nb_cluster)
    kmeans.fit(dataFrameDonnees_cr)
    # baricentres des n clusters
    # print(kmeans.cluster_centers_)

    if user[9] == True:
        user[9] = 1
    else :
        user[9] = 0

    baricentres = kmeans.cluster_centers_

    distances=np.zeros((1,nb_cluster)) 
    for i in range(nb_cluster):
        distances[0,i]=sum((user-baricentres[i,:])*(user-baricentres[i,:]))

    print("--------- Distances aux baricentres ---------")
    print(distances)
    id_proche=np.argmin(distances) 
    print("class = "+str(id_proche)) 
    print('FIN')

# =============== Utilisateur à classifier =============== #
user = [12, 1, 4, 100, 50, 80, 0, 0.5, 2, True, 0.0821]
# print(user[9])
classerNewUserKMeans(user, 3)
