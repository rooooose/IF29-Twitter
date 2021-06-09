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

X_train, X_test, y_train, y_test = train_test_split(matriceDonnees, etiquettes, test_size=0.7, random_state=42)
print(X_train)

from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.metrics import confusion_matrix


parametres = {"kernel":["linear", "poly", "rbf", "sigmoid"], "C":[0.01,0.1,1,10,100]}

svm = SVC()
grille = GridSearchCV(estimator=svm, param_grid=parametres, scoring="accuracy", cv=2)
resultats = grille.fit(X_train, y_train)
print(resultats.best_params_)

y_pred_test = grille.predict(X_test)
erreur_test = 1.0 - metrics.accuracy_score(y_test, y_pred_test)
print("erreur test : ",erreur_test)

conf = confusion_matrix(y_test, y_pred_test)
print(conf)
import seaborn as sns
sns.heatmap(conf, square=True, annot=True, cbar=False, xticklabels=["non suspect","suspect"], yticklabels=["non suspect","suspect"])

import matplotlib.pyplot as plt
plt.xlabel('valeurs prédites')
plt.ylabel('valeurs réelles')
plt.show()