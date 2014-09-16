# coding:utf-8
import sys
from random import random
import numpy as np
import csv
from decimal import Decimal
from datetime import datetime
import math
import re

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from collections import Counter, OrderedDict
from sklearn import metrics
from sklearn import cross_validation
from sklearn import linear_model


class Algo:
    def __init__(self):
        pass

    def train_clf(self, ftrain):
        ''' returns clf '''
        clf = AdaBoostClassifier(base_estimator=RandomForestClassifier(n_estimators=30), n_estimators=10)
        with open(ftrain, 'r') as ftrain_obj:
            cntr = 1
            train_set_x = []
            train_set_y = []
            ftrain_obj.readline()
            for t in ftrain_obj.xreadlines():
                row = t[:-2].split(',')
                ad_id = row.pop(0)
                train_set_y.append(float(row.pop(0)))
                res = np.array([float(r) if r else 0 for r in row[:13]])
                train_set_x.append(res)
                cntr += 1
                if cntr == 10000:
                    break
            train_set_y = np.array(train_set_y)
            train_set_x = np.array(train_set_x)
            clf.fit(train_set_x, train_set_y)
        return clf

    def compute_result(self, clf, ftest, fresult):
        with open(ftest, 'r') as ftest_obj:
            ftest_obj.readline()
            with open(fresult, 'w') as fres_obj:
                fres_obj.write('Id,Predicted\n')
                cntr = 0
                for t in ftest_obj.xreadlines():
                    row = t[:-1].split(',')
                    ad_id = row.pop(0)
                    X_test = np.array([float(r) if r else 0 for r in row[:13]])
                    pred = np.array(clf.predict_proba(X_test))[0]
                    fres_obj.write('%s,%s\n' % (ad_id, pred[1]) )
                    cntr += 1
                    if cntr % 10000 == 0:
                        print cntr, datetime.now()


if __name__ == "__main__":
    algo = Algo()
    print 'training...', datetime.now()
    clf = algo.train_clf('train.csv')
    print 'classifying...', datetime.now()
    algo.compute_result(clf, 'test.csv', 'result.csv')
    print 'finished...', datetime.now()