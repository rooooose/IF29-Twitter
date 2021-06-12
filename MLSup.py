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

svm.fit(X_train, y_train)

y_pred_test = svm.predict(X_test)

# y_pred_test = grille.predict(X_test)
erreur_test = 1.0 - metrics.accuracy_score(y_test, y_pred_test)
print("erreur test : ",erreur_test)


conf = confusion_matrix(y_test, y_pred_test)
print(conf)
import seaborn as sns
sns.heatmap(conf, square=True, annot=True, cbar=False, xticklabels=["non suspect","suspect"], yticklabels=["non suspect","suspect"])

import matplotlib.pyplot as plt
plt.figure("Confusion matrix")
plt.xlabel('valeurs prédites')
plt.ylabel('valeurs réelles')



# Représentation dans le plan
from AcpTweet import xline, yline, zline, sample_etiquettes, composante_princ

idx_test = np.random.randint(len(matriceDonnees), size=500)
sample_etiquettes_test = np.array(etiquettes)[idx_test]

xline_test = composante_princ[idx_test,0]
yline_test = composante_princ[idx_test,1]
zline_test = composante_princ[idx_test,2]

h=.02
x_min, x_max = xline_test.min()-1, xline_test.max()+1
y_min, y_max = yline_test.min()-1, yline_test.max()+1
xx,yy = np.meshgrid(np.arange(x_min,x_max,h), np.arange(y_min,y_max,h))

svm.fit(np.column_stack((xline,yline)),sample_etiquettes)
# svm.fit(composante_princ[:,0:2],etiquettes)

Z = svm.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure("SVM Supervisé")
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

plt.scatter(xline_test, yline_test, label='train', edgecolors='k', c=sample_etiquettes_test, cmap=plt.cm.coolwarm)
# plt.scatter(composante_princ[:,0], composante_princ[:,1], label='train', edgecolors='k', c=etiquettes, cmap=plt.cm.coolwarm)
plt.xlabel('x1')
plt.ylabel('x2')
plt.title("SVM linear")

# 3D VIZ

# h=.02
# x_min, x_max = xline_test.min()-1, xline_test.max()+1
# y_min, y_max = yline_test.min()-1, yline_test.max()+1
# z_min, z_max = zline_test.min()-1, zline_test.max()+1
# xx,yy,zz = np.meshgrid(np.arange(x_min,x_max,h), np.arange(y_min,y_max,h), np.arange(z_min,z_max,h))

# svm.fit(np.column_stack((xline,yline,zline)),sample_etiquettes)

# Z = svm.predict(np.c_[xx.ravel(), yy.ravel(), zz.ravel()])
# Z = Z.reshape(xx.shape)

# plt.figure("SVM Supervisé")
# # plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

# ax = plt.axes(projection='3d')
# plt.scatter(xline_test, yline_test, zline_test, 'gray')
# ax.view_init(60,35)
# ax.set_xlabel('Axe 1')
# ax.set_ylabel('Axe 2')
# ax.set_zlabel('Axe 3')

plt.show()

erreur_viz = 1.0 - metrics.accuracy_score(sample_etiquettes, sample_etiquettes_test)
print("erreur test : ",erreur_viz)