# coding:utf-8
import csv
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
import numpy as np
from sklearn.decomposition import PCA

train_set_x = []
train_set_y = []

with open('train.csv', 'r') as file_obj:
    for row in csv.reader(file_obj):
        train_set_x.append(np.array([float(i) for i in row]))

with open('trainLabels.csv', 'r') as file_obj:
    for row in csv.reader(file_obj):
        train_set_y.append(row[0])

pca = PCA(n_components=5)
pca.fit(train_set_x)
train_set_x = pca.transform(train_set_x)

#clf = SVC()
clf = AdaBoostClassifier()
clf.fit(train_set_x, train_set_y)

test_set_x = []
test_set_y = []
with open('test.csv', 'r') as file_obj:
    for row in csv.reader(file_obj):
        test_set_x.append(np.array([float(i) for i in row]))

test_set_x = pca.transform(test_set_x)

with open('testLabels.csv', 'w') as file_obj:
    pred = clf.predict(test_set_x)
    file_obj.write('Id,Solution\n')
    cntr = 1
    for i in pred:
        file_obj.write('%s,%s\n' % (cntr, i))
        cntr += 1