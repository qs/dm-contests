import numpy as np
from scipy.spatial.distance import pdist

from datetime import datetime
import logging
import sys
import pickle

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

def load_users_features(fdata, flist):
    allf = set([])
    features_list = [i[:-1] for i in open(flist).readlines()]
    users = {}
    with open(fdata) as f:
        for row in f.readlines():
            row = row[:-1].split(' ')
            user_id = row.pop(0)
            allf |= set(row)
            users[user_id] = row
    users_n = len(users)
    curr = 1.0
    empty_f = dict(zip(allf, [0 for i in range(len(allf))]))
    for k, v in users.items():
        data = empty_f.copy()
        data.update(dict(zip(v, [1 for i in range(len(v))])))
        data = dict(sorted(data.items(), key=lambda x: x[0]))
        users[k] = np.array(data.values())
        curr += 1
        if curr % 1000 == 0:
            print curr, users[k]
    return users, allf

logger.info("Start loading data %s" % datetime.now())
users, allf = load_users_features('features.txt', 'featureList.txt')

f = open('loaded_data.bin')
pickle.dump(users, f)
f.close()

logger.info("Data loaded %s" % datetime.now())

logger.info("Compute pdist %s" % datetime.now())
#pairs = pdist(users.values(), 'jaccard')
logger.info("Compute pdist finished %s" % datetime.now())

