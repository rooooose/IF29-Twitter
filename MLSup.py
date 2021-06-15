from sklearn.model_selection import train_test_split
from service import rethinkDBservice
import numpy as np

users = rethinkDBservice.getUsersCursors()

table = []
etiquettes = []
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

matriceDonnees = np.array(table)

X_train, X_test, y_train, y_test = train_test_split(matriceDonnees, etiquettes, test_size=0.7, random_state=42)

from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.metrics import confusion_matrix


# parametres = {"kernel":["linear", "poly", "rbf", "sigmoid"], "C":[0.01,0.1,1,10,100]}

# svm = SVC()
# grille = GridSearchCV(estimator=svm, param_grid=parametres, scoring="accuracy", cv=2)
# resultats = grille.fit(X_train, y_train)
# print(resultats.best_params_)

C = 0.01
noyau = 'linear'
svm = SVC(C,noyau)
print("svm créé")

svm.fit(X_train, y_train)
print("apprentissage fait")

y_pred_test = svm.predict(X_test)
print("prédiction faite")

# y_pred_test = grille.predict(X_test)
erreur_test = 1.0 - metrics.accuracy_score(y_test, y_pred_test)
print("erreur test : ",erreur_test)


conf = confusion_matrix(y_test, y_pred_test)
print(conf)

import matplotlib.pyplot as plt
plt.figure("Confusion matrix")


import seaborn as sns
sns.heatmap(conf, square=True, annot=True, cbar=False, xticklabels=["non suspect","suspect"], yticklabels=["non suspect","suspect"], cmap ="Blues", fmt='d')
plt.xlabel('valeurs prédites')
plt.ylabel('valeurs réelles')
plt.title("Matrice de confusion")
plt.show()



# Représentation dans le plan
from AcpTweet import CP2

X_train_ACP, X_test_ACP, y_train_ACP, y_test_ACP = train_test_split(CP2, etiquettes, test_size=10000, train_size=0.3, random_state=42)

# idx = np.random.randint(len(matriceDonnees), size=1000)
# sample_etiquettes = np.array(etiquettes)[idx]
# xline = CP2[idx,0]
# yline = CP2[idx,1]

# Test de l'apprentissage sur un échantillon aléatoire de 500 individus pour la représentation

# idx_test = np.random.randint(len(matriceDonnees), size=1000)
# sample_etiquettes_test = np.array(etiquettes)[idx_test]
# xline_test = CP2[idx_test,0]
# yline_test = CP2[idx_test,1]

h=.02
x_min, x_max = X_test_ACP[:,0].min()-1, X_test_ACP[:,0].max()+1
y_min, y_max = X_test_ACP[:,1].min()-1, X_test_ACP[:,1].max()+1
xx,yy = np.meshgrid(np.arange(x_min,x_max,h), np.arange(y_min,y_max,h))

svm.fit(X_train_ACP,y_train_ACP)
print("apprentissage fait")

Z_origin = svm.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z_origin.reshape(xx.shape)

plt.figure("SVM Supervisé")
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

plt.scatter(X_test_ACP[:,0], X_test_ACP[:,1], label='train', edgecolors='k', c=y_test_ACP, cmap=plt.cm.coolwarm)
# plt.scatter(composante_princ[:,0], composante_princ[:,1], label='train', edgecolors='k', c=etiquettes, cmap=plt.cm.coolwarm)
plt.xlabel('x1')
plt.ylabel('x2')
plt.title("SVM linear")

plt.show()