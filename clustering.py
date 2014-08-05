from sklearn.metrics import jaccard_similarity_score
from itertools import combinations
import numpy as np

'''
27473 last_name;16976 locale;1 hometown;name;4299 hometown;id;4313 
birthday;4285 education;school;name;11574 education;school;id;12242 education;type;0 education;year;name;26 education;year;id;30 education;school;name;17934 education;school;id;19060 education;type;1 education;year;name;25 education;year;id;29 id;27473 first_name;2931 name;27238 gender;0 work;position;name;378 work;position;id;386 work;start_date;4 work;employer;name;18284
 work;employer;id;19031 work;employer;name;18285 work;employer;id;19032 location;name;119 location;id;119
'''
def load_users_features(fname):
    features_list = [i[:-1] for i in open('featureList.txt').readlines()]
    features_data = []
    with open(fname) as f:
        for row in f.readlines():
            row = row[:-1].split(' ')
            data = {}
            data['id'] = row.pop(0)
            for r in row:
                k, v = r.rsplit(';', 1)
                data[k] = v
            for i in features_list:
                if i not in data:
                    data[i] = 0
            data = dict(sorted(data.items(), key=lambda x: x[1]))
            features_data.append(data)
    return np.array(features_data)


def compute_nbrs(user_k, user_j):
    return jaccard_similarity_score(user_k.values(), user_j.values())

users = load_users_features('features.txt')

data = np.array([[ (i, j, compute_nbrs(i, j)) for j in users ] for i in users])
print data[0]

exit()

curr = 0
user_matrix = dict([(i['id'], {}) for i in users])
for user_k, user_j in combinations(users, 2):
    score = compute_nbrs(user_k, user_j)
    user_matrix[user_k['id']][user_j['id']] = score
    user_matrix[user_j['id']][user_k['id']] = score
    curr += 1
    if curr % 10000 == 0:
        print curr

print user_matrix[1]