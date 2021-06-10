import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from service import rethinkDBservice
import pandas as pd

users = list(rethinkDBservice.getUsersCursors())
table = []
cmp = 0
for user in users:
    table.append([
        user["avg_hashtag"],
        #user["avg_retweet"],
        user["avg_url"],
        user["followers"],
        user["friends"],
        user["mediumLengthTweets"],
        #user["rateOfRepliedTweets"],
        user["ratio_frds_flwrs"],
        user["tweet_per_day"],
        user["verified"],
        user["visibility"],
    ])

matriceDonnees = np.array(table)

# attribut = np.array(["avg_hashtag", "avg_retweet", "avg_url", "followers", "friends", "mediumLengthTweets", "rateOfRepliedTweets", "ratio_frds_flwrs", "tweet_per_day", "verified", "visibility"])
attribut = np.array(["avg_hashtag", "avg_url", "followers", "friends", "mediumLengthTweets", "ratio_frds_flwrs", "tweet_per_day", "verified", "visibility"])

# ===================== Baricentre et inertie ===================== #
#dimension
dimMatrice=matriceDonnees.shape
print(dimMatrice)

#calcul du baricentre g
g=np.zeros((1,dimMatrice[1]))
for j in range(dimMatrice[1]):
	g[0,j]=np.mean(matriceDonnees[:,j])
print(g)

#calcul de l'inertie
I=0
for i in range(dimMatrice[0]):
	I= I + np.sum((matriceDonnees[i,:]-g)*(matriceDonnees[i,:]-g))
print(I)
I = I/dimMatrice[0]
print(I)

# ===================== Centrer-réduire les données ===================== #
#matrice de valeurs centrées
Y=np.zeros(dimMatrice)
for j in range(dimMatrice[1]):
	Y[:,j]= matriceDonnees[:,j] - np.mean(matriceDonnees[:,j])
print(Y)

#calcul de gy
gy=np.zeros((1,dimMatrice[1]))
#print(gy)
for j in range(dimMatrice[1]):
	gy[0,j] = np.mean(Y[:,j])
print(gy)


#calcul de l'inertie
Iy=0
for i in range(dimMatrice[0]):
	Iy = Iy + np.sum((Y[i,:] - gy)*(Y[i,:] - gy))

Iy = Iy/dimMatrice[0]
print(Iy)

# #matrice de valeurs centrées-réduites
# Z = np.zeros(dimMatrice)
# for j in range (dimMatrice[1]):
# 	if Y[:,j]/np.std(Y[:,j]) == 0:
# 		Z[:,j] = 0
# 	else:
# 		Z[:,j] = Y[:,j]/np.std(Y[:,j])

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
print(Iz)

# ===================== Corrélations, VeP et VaP ===================== #
#Matrice corrélations

Mcorr=np.corrcoef(np.transpose(Z))
print("---------------- Matrice corr. ----------------")
print(Mcorr)
print(Mcorr.shape)

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
#print("---------------- VeP : vecteur propre ----------------")
#print(VeP)
#print("---------------- VaP : valeur propre ----------------")
#print(VaP)


#III.2.iv
Iacp=np.sum(VaP)

# ===================== ACP 2 composantes ===================== #
#calcul des 2 premières composantes
CP2=np.dot(Z,VeP[:,0:2])  #O:2=0 et 1
#print(CP2)

#Corrélation entre les 2 composantes
Mcorr2 = np.corrcoef(np.transpose(CP2))
print("---------------- Mcorr2 : F1 et F2 ----------------")
print(Mcorr2)

#pourcentage d'inertie dans les 2 axes
pourcent2 = np.sum(VaP[0:2])*100/Iacp
print("")
print("---------------- pourcent2 : pourcentage d'inertie dans les 2 axes ----------------")
print(pourcent2)

#représentation des individus sur ces 2 axes
itimg=1 
plt.figure(itimg) #on explicite le numéro de la figure 
plt.plot(CP2[:,0],CP2[:,1],'.')
plt.xlabel("axe1")
plt.ylabel("axe2")
plt.title("axe1 as function of axe2")
# for i in range(dimMatrice[0]):
# 	plt.text(CP2[i,0], CP2[i,1], vehicule[i+1,0], horizontalalignment='left', verticalalignment='center')


# ===================== ACP 3 composantes ===================== #
#calcul des 3 premières composantes
CP3=np.dot(Z,VeP[:,0:3])  #O:2=0 et 1

#Corrélation entre les 3 composantes
Mcorr3 = np.corrcoef(np.transpose(CP3))
print("---------------- Mcorr3 : F1, F2 et F3 ----------------")
print(Mcorr3)

#pourcentage d'inertie dans les 3 axes
pourcent3 = np.sum(VaP[0:3])*100/Iacp
print("")
print("---------------- pourcent3 : pourcentage d'inertie dans les 3 axes ----------------")
print(pourcent3)


# ===================== CTA et CTR pour ACP2 ===================== #
# #CTA
# CTAI2=np.zeros((dimMatrice[0],2))
# for j in range(2):
# 	CTAI2[:,j]=CP2[:,j]*CP2[:,j]*100/(dimMatrice[0]*VaP[j])

# #CTR
# CTRI2=np.zeros((dimMatrice[0],2))
# CP6=np.dot(Z,VeP) #toutes les composantes principales 
# for i in range(dimMatrice[0]):
# 	for j in range(2):
# 		CTRI2[i,j]=CP2[i,j]*CP2[i,j]*100/(np.sum(CP6[i,:]*CP6[i,:]))

# # ===================== V ===================== #

#Matrice corrélation des variables originales sur la composante principale Fi (ici pour 2 CP)
McorrV2 = np.zeros((dimMatrice[1], 2))
for i in range(dimMatrice[1]):
	for j in range(2):
		McorrV2[i,j] = np.corrcoef(Z[:,i], CP2[:,j])[0,1]
#[0,1] est l'indice dans la matrice de corr.
print("---------------- McorrV2 ----------------")
print(McorrV2)

#V.2.i
CTRV2=McorrV2*McorrV2*100

#V.2.ii 
CTAV2=np.zeros(CTRV2.shape)
for j in range(2):
	CTAV2[:,j]=CTRV2[:,j]/VaP[j]

print("---------------- CTRV2 ----------------")
print(CTRV2)

print("---------------- CTAV2 ----------------")
CTAV2 = pd.DataFrame(CTAV2)
CTAV2.index = attribut
print(CTAV2)

#V-3-i 
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

#V.3.ii
for j in range(dimMatrice[1]):
	plt.plot([0,McorrV2[j,0]],[0,McorrV2[j,1]],'b')
	plt.text(McorrV2[j,0],McorrV2[j,1],attribut[j])
plt.show() #fig.7

# ===================== VI ===================== #
#VI.1.i
x=np.arange(0,VaP.size)+1 
y=VaP 
itimg=itimg+1 
fig = plt.figure(itimg) 
plt.plot(x,y) 
plt.xlabel("numero variable") 
plt.ylabel(" Inertie") 
plt.show()
#figure 8 inertie en fonction de variable

#VI.1.ii 
x=np.arange(0,VaP.size)+1 
poucent_cumul=np.cumsum(VaP*100/np.sum(VaP)) 
itimg=itimg+1 
fig = plt.figure(itimg) 
plt.plot(x,poucent_cumul) 
plt.xlabel("numero variable") 
plt.ylabel("pourcentage d'inertie cumulée")
plt.show()
#figure 9 - dispersion cumulée

#VI.1.iii
angleB=np.zeros((1,dimMatrice[1]-2))
for i in np.arange(1,dimMatrice[1]-1):# on ignore le premier et le dernier element
	xA=i
	yA=poucent_cumul[i-1]
	xB=i+1
	yB=poucent_cumul[i]
	xC=i+2
	yC=poucent_cumul[i+1]
	AB_carre=math.pow((yB-yA),2)+math.pow((xB-xA),2)
	BC_carre=math.pow((yC-yB),2)+math.pow((xC-xB),2)
	AC_carre=math.pow((yC-yA),2)+math.pow((xC-xA),2)
	# théorème d'Al-Kashi en France1, ou encore théorème de Pythagore généralisé
	angleB[0,i-1]=math.acos((AB_carre+BC_carre-AC_carre)/(2*math.sqrt(AB_carre*BC_carre)))
out=np.argmax(angleB)+2 
#import module_ACP 
#out2=module_ACP.coude_cattell_pourcent_cumule(VaP) 
#print("out2 = ") 
#print(out2)
