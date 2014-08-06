from sklearn.metrics import jaccard_similarity_score
from itertools import combinations
import numpy as np
from scipy.spatial.distance import jaccard

'''
27473 last_name;16976 locale;1 hometown;name;4299 hometown;id;4313 
birthday;4285 education;school;name;11574 education;school;id;12242 education;type;0 education;year;name;26 education;year;id;30 education;school;name;17934 education;school;id;19060 education;type;1 education;year;name;25 education;year;id;29 id;27473 first_name;2931 name;27238 gender;0 work;position;name;378 work;position;id;386 work;start_date;4 work;employer;name;18284
 work;employer;id;19031 work;employer;name;18285 work;employer;id;19032 location;name;119 location;id;119
'''

def load_users_features(fname, all_features):
    features_list = [i[:-1] for i in open('featureList.txt').readlines()]
    users = {}
    with open(fname) as f:
        for row in f.readlines():
            row = row[:-1].split(' ')
            user_id = row.pop(0)
            all_features |= set(row)
            users[user_id] = row
    return users, all_features

users, allf = load_users_features('features.txt', set([]))
print len(allf)

empty_f = dict(zip(allf, [False for i in range(len(allf))]))
for user_k, user_j in combinations(users, 2):
    #print user_k, user_j
    curr_k = empty_f.copy()
    curr_k.update(dict(zip(user_k, [True for i in range(len(user_k))])))
    curr_j = empty_f.copy()
    curr_j.update(dict(zip(user_j, [True for i in range(len(user_j))])))
    j = jaccard(curr_k.values(), curr_j.values())
    print j

exit()

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