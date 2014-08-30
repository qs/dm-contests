# coding:utf-8
import csv
import numpy as np
from sklearn.decomposition import PCA

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

train_set_x = []
train_set_y = []

with open('train.csv', 'r') as file_obj:
    for row in csv.reader(file_obj):
        train_set_x.append(np.array([float(i) for i in row]))

with open('trainLabels.csv', 'r') as file_obj:
    for row in csv.reader(file_obj):
        train_set_y.append(row[0])

#pca = PCA(n_components=7)
#pca.fit(train_set_x)
#train_set_x = pca.transform(train_set_x)

# Create the classifiers
#clf1 = ExtraTreesClassifier(n_estimators=200, max_depth=None, min_samples_split=1, random_state=0)
#clf2 = RandomForestClassifier(n_estimators=200, max_depth=None, min_samples_split=1, random_state=0)
#clf3 = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0)
#clf4 = AdaBoostClassifier(n_estimators=500)
#clf5 = GradientBoostingClassifier(n_estimators=50, learning_rate=1.0, max_depth=1, random_state=0)
#clf6 = SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.2, kernel='rbf', max_iter=-1, probability=True, random_state=None, shrinking=True, tol=0.001, verbose=False)
#clf1 = ExtraTreesClassifier()
clf6 = SVC(probability=True)
#clf2 = RandomForestClassifier()

#clfs = [clf1, clf2, clf3, clf4, clf5, clf6]

clfs = [clf6]

# Fit each classifier based on the training data
for clf in clfs:
    clf.fit(train_set_x, train_set_y)

test_set_x = []
test_set_y = []
with open('test.csv', 'r') as file_obj:
    for row in csv.reader(file_obj):
        test_set_x.append(np.array([float(i) for i in row]))

#test_set_x = pca.transform(test_set_x)

with open('testLabels.csv', 'w') as file_obj:
    predictions = []
    for clf in clfs:
        predictions.append(clf.predict_proba(test_set_x))
    p = np.mean(predictions, axis=0)
    p = map(lambda x: 0 if x[0] >= 0.5 else 1, p)
    file_obj.write('Id,Solution\n')
    cntr = 1
    for i in p:
        file_obj.write('%s,%s\n' % (cntr, i))
        cntr += 1