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
            ftrain_obj.readline()
            for t in ftrain_obj.xreadlines():
                row = t[:-1].split(',')
                ad_id = row.pop(0)
                y_train = np.array([row.pop(-1), ])
                X_train = np.array([[r for r in row if re.match('^[0-9\.]+$', r)], ])
                clf.fit(X_train, y_train)
                cntr += 1
                if cntr == 10000:
                    break
        return clf

    def compute_result(self, clf, ftest, fresult):
        with open(ftest, 'r') as ftest_obj:
            ftest_obj.readline()
            with open(fresult, 'w') as fres_obj:
                fres_obj.write('Id,Predicted\n')
                for t in ftest_obj.xreadlines():
                    row = t[:-1].split(',')
                    ad_id = row.pop(0)
                    X_test = np.array([[r for r in row if re.match('^[0-9\.]+$', r)], ])
                    pred = np.array(clf.predict_proba(X_test))[0]
                    fres_obj.write('%s,%s\n' % (ad_id, pred) )


if __name__ == "__main__":
    algo = Algo()
    print 'training...', datetime.now()
    clf = algo.train_clf('train.csv')
    print 'classifying...', datetime.now()
    algo.compute_result(clf, 'test.csv', 'result.csv')
    print 'finished...', datetime.now()