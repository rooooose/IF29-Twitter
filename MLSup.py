from sklearn.model_selection import train_test_split
from service import rethinkDBservice
import numpy as np

users = rethinkDBservice.getUsersCursors()

table = []
etiquettes = []
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
    etiquettes.append(user["suspect"])

matriceDonnees = np.array(table)

X_train, X_test, y_train, y_test = train_test_split(matriceDonnees, etiquettes, test_size=0.9, random_state=42)
print(X_train)

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
# erreur_test = 1.0 - metrics.accuracy_score(y_test, y_pred_test)
# print("erreur test : ",erreur_test)

conf = confusion_matrix(y_test, y_pred_test)
print(conf)
import seaborn as sns
sns.heatmap(conf, square=True, annot=True, cbar=False, xticklabels=["non suspect","suspect"], yticklabels=["non suspect","suspect"])

import matplotlib.pyplot as plt
plt.xlabel('valeurs prédites')
plt.ylabel('valeurs réelles')


# Représentation dans le plan
from AcpTweet import xline, yline, composante_princ

h=.02
x_min, x_max = xline.min()-1, xline.max()+1
y_min, y_max = yline.min()-1, yline.max()+1
xx,yy = np.meshgrid(np.arange(x_min,x_max,h), np.arange(y_min,y_max,h))

svm.fit(composante_princ[:,0:2],etiquettes)
Z = svm.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure("SVM Supervisé")
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

plt.scatter(composante_princ[:,0], composante_princ[:,1], label='train', edgecolors='k', cmap=plt.cm.coolwarm)
plt.xlabel('x1')
plt.ylabel('x2')
plt.title("SVM linear")

# plt.scatter(xline, yline, c=y_pred_test, s=50, cmap='autumn')
# plot_svc_decision_function(clf, plot_support=False);


plt.show()