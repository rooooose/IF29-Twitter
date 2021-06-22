import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


from service import rethinkDBservice

users = list(rethinkDBservice.getUsersCursors())
table=[]
etiquettes = []
# cmp = 0
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
    # cmp+=1
    # print(cmp)

matriceDonnees = np.array(table)
# print(matriceDonnees)

attribut = np.array(["accountAge", "agressivite", "avg_hashtag", "avg_url", "mediumLength", "rationFollowersFriends", "tweet_per_day", "verified", "visibility"])

# ACP pour afficher graphique en coude pour choix du nombre de CP
sc = StandardScaler()
Z = sc.fit_transform(matriceDonnees)

acp = PCA(svd_solver='full')

# calculs des composantes principales
composante_princ = acp.fit_transform(Z)
# print(composante_princ[0])
# nombre de composantes calculées
# print(acp.n_components_) 

# valeur corrigée par les valeurs singulières
n=Z.shape[0]
eigval = acp.singular_values_**2/n

# plt.plot(np.arange(1,9+1),eigval)
# plt.title("Scree plot")
# plt.ylabel("Eigen values")
# plt.xlabel("Factor number")
# plt.show()


# =============================================================== #
#       ANALYSE ACP - inertie et contribution des attributs       #
# =============================================================== #



# ===================== Introduction ===================== #
# cette analyse plus approfondi n'utilise pas la bibliothèque sklearn mais un TD réalisé dans le cadre de l'UE IF29
# cette analyse permet de mettre en évidence le choix du nombre de CP et les attributs contribuant à la formation des axes


# ===================== Baricentre et inertie ===================== #
#dimension
dimMatrice=matriceDonnees.shape
# print(dimMatrice)

#calcul du baricentre g
g=np.zeros((1,dimMatrice[1]))
for j in range(dimMatrice[1]):
    g[0,j]=np.mean(matriceDonnees[:,j])
# print(g)


#calcul de l'inertie
I=0
for i in range(dimMatrice[0]):
    I= I + np.sum((matriceDonnees[i,:]-g)*(matriceDonnees[i,:]-g))
I = I/dimMatrice[0]
# print(I)

# ===================== Centrer-réduire les données ===================== #
#matrice de valeurs centrées
Y=np.zeros(dimMatrice)
for j in range(dimMatrice[1]):
    Y[:,j]= matriceDonnees[:,j] - np.mean(matriceDonnees[:,j])
# print(Y)

#calcul de gy
gy=np.zeros((1,dimMatrice[1]))
for j in range(dimMatrice[1]):
    gy[0,j] = np.mean(Y[:,j])
# print(gy)

# graphique avec croisement deux à deux
idx = np.random.randint(len(matriceDonnees), size=500)

# from pandas.plotting import scatter_matrix
# dataFrameDonnees = pd.DataFrame(data=matriceDonnees[idx,:], columns=["accountAge(days)", "agressivite","avg_hashtag","avg_url","mediumLength","rationFollowersFriends","tweet_per_day","verified","visibility"])
# pd.plotting.scatter_matrix(dataFrameDonnees,figsize=(9,9))
# plt.show()

#calcul de l'inertie
Iy=0
for i in range(dimMatrice[0]):
    Iy = Iy + np.sum((Y[i,:] - gy)*(Y[i,:] - gy))

Iy = Iy/dimMatrice[0]
# print(Iy)

# #matrice de valeurs centrées-réduites - gestion de la division par zéros
# Z = np.zeros(dimMatrice)
# for j in range (dimMatrice[1]):
#   if Y[:,j]/np.std(Y[:,j]) == 0:
#       Z[:,j] = 0
#   else:
#       Z[:,j] = Y[:,j]/np.std(Y[:,j])

#centrage réduction des données
from sklearn import preprocessing
Z = preprocessing.scale(matriceDonnees)

#calcul de gz
gz = np.zeros((1,dimMatrice[1]))
for j in range(dimMatrice[1]):
    gz[0, j] = np.mean(Z[:,j])

#calcul de l'inertie
Iz = 0
for i in range(dimMatrice[0]):
    Iz = Iz + np.sum((Z[i,:] - gz)*(Z[i,:] - gz))
Iz = Iz / dimMatrice[0]
# print(Iz)

# ===================== Corrélations, VeP et VaP ===================== #
#Matrice corrélations

Mcorr=np.corrcoef(np.transpose(Z))
# print("---------------- Matrice corr. ----------------")
# print(Mcorr)
# print(Mcorr.shape)

# gère lorsqu'un utilisateur n'a pas de valeur pour un de ses attributs.
def isNaN(num):
    if float('-inf') < float(num) < float('inf'):
        return False 
    else:
        return True

for i in range (Mcorr.shape[0]):
    for j in range(Mcorr.shape[1]):
        if isNaN(Mcorr[i,j]) :
            Mcorr[i,j] = 0


#Vecteurs propres et Valeurs propres
VaP,VeP=np.linalg.eig(Mcorr)
#print("--------- VeP : vecteur propre ---------")
#print(VeP)
#print("--------- VaP : valeur propre ---------")
#print(VaP)


#Inertie dans le nouvel espace
Iacp=np.sum(VaP)

# ===================== ACP 2 composantes ===================== #
#calcul des 2 premières composantes
CP2=np.dot(Z,VeP[:,0:2])  #O:2=0 et 1
#print(CP2)

#Corrélation entre les 2 composantes
Mcorr2 = np.corrcoef(np.transpose(CP2))
# print("--------- Mcorr2 : F1 et F2 ---------")
# print(Mcorr2)

#pourcentage d'inertie dans les 2 axes
pourcent2 = np.sum(VaP[0:2])*100/Iacp
# print("")
# print("--------- pourcent2 : pourcentage d'inertie dans les 2 axes ---------")
# print(pourcent2)


#représentation de 100 000 individus pris aléatoirement sur ces 2 axes
idx = np.random.randint(len(matriceDonnees), size=10000)

# itimg=1 
# plt.figure(itimg) #on explicite le numéro de la figure
# plt.plot(CP2[idx,0], CP2[idx,1],'.')
# plt.xlabel("axe1")
# plt.ylabel("axe2")
# plt.title("Représentation de 10 000 points sur les 2 composantes principales")


# ===================== ACP 3 composantes ===================== #
#calcul des 3 premières composantes
CP3=np.dot(Z,VeP[:,0:3])  #O:2=0 et 1

#Corrélation entre les 3 composantes
Mcorr3 = np.corrcoef(np.transpose(CP3))
# print("--------- Mcorr3 : F1, F2 et F3 ---------")
# print(Mcorr3)

#pourcentage d'inertie dans les 3 axes
pourcent3 = np.sum(VaP[0:3])*100/Iacp
# print("")
# print("--------- pourcent3 : pourcentage d'inertie dans les 3 axes ---------")
# print(pourcent3)



# ===================== CTA et CTR pour ACP2 ===================== #

#Matrice corrélation des variables originales sur la composante principale Fi (ici pour 2 CP)
McorrV2 = np.zeros((dimMatrice[1], 2))
for i in range(dimMatrice[1]):
    for j in range(2):
        McorrV2[i,j] = np.corrcoef(Z[:,i], CP2[:,j])[0,1]
#[0,1] est l'indice dans la matrice de corr.
# print("--------- McorrV2 ---------")
# print(McorrV2)

#CTR
CTRV2=McorrV2*McorrV2*100

#CTA
CTAV2=np.zeros(CTRV2.shape)
for j in range(2):
    CTAV2[:,j]=CTRV2[:,j]/VaP[j]

# print("--------- CTRV2 ---------")
# print(CTRV2)

# print("--------- CTAV2 ---------")
CTAV2 = pd.DataFrame(CTAV2)
CTAV2.index = attribut
# print(CTAV2)

# Représentation des vecteurs de corrélation sur le cercle unité
# trace le cercle
import math 
t=np.linspace(0,2*math.pi)
x1=np.zeros(t.shape)
y1=np.zeros(t.shape)
for i in range(t.size):
    #print(i)
    x1[i]=math.cos(t[i])
    y1[i]=math.sin(t[i])
x2=np.linspace(-1,1)
y2=np.zeros(t.shape)
x3=np.zeros(t.shape)
y3=np.linspace(-1,1)
itimg=itimg+1
fig = plt.figure(itimg)
plt.plot(x1,y1)
plt.plot(x2,y2)
plt.plot(x3,y3)
plt.xlabel("axis1")
plt.ylabel("axis2")

# ajoute les vecteurs
for j in range(dimMatrice[1]):
    plt.plot([0,McorrV2[j,0]],[0,McorrV2[j,1]],'b')
    plt.text(McorrV2[j,0],McorrV2[j,1],attribut[j])
plt.show() 

# ===================== Inertie cumulée en fonction du nb de CP===================== #

# Dispersion cumulées des CP en fonction du nombre de CP
x=np.arange(0,VaP.size)+1 
poucent_cumul=np.cumsum(VaP*100/np.sum(VaP)) 
itimg=itimg+1 
fig = plt.figure(itimg) 
plt.plot(x,poucent_cumul) 
plt.xlabel("nombre de variables") 
plt.ylabel("pourcentage d'inertie cumulée")
plt.show()

