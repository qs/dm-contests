from pymongo import MongoClient
from datetime import datetime
from collections import OrderedDict, Counter, defaultdict
import numpy as np
from sklearn import cluster

from os import listdir
from os.path import isfile, join
from itertools import izip


client = MongoClient()
db = client.soccir


class DataLoader:
    def load_features_data(self):
        print 'features loading starts ', datetime.now()
        features_list = [i[:-1] for i in open('featureList.txt').readlines()]
        features_vals = set([])
        with open('features.txt') as fp:
            for line in fp.xreadlines():
                line = line.replace('\r', '').replace('\n', '')
                user_id, features = line.split(' ', 1)
                for i in features:
                    features_vals.add(i)
                features = dict([i.rsplit(';', 1) for i in features.split(' ')])
                features['_id'] = features.pop('id')
                db.users.insert(features)
        print 'features inserted into collection ', datetime.now()
        for k in features_list:
            db.users.create_index(k)
        print 'features index created ', datetime.now()

    def _get_com_key(self, user_id, friend_id):
        if int(user_id) > int(friend_id):
            return "%s_%s" % (friend_id, user_id)
        else:
            return "%s_%s" % (user_id, friend_id)

    def load_friends_data(self):
        print 'friends loading starts ', datetime.now()
        egonets_files = [ f for f in listdir('egonets') if isfile(join('egonets/',f)) ]
        for f in egonets_files:
            with open('egonets/%s' % f) as fp:
                user_id = f.split('.')[0]
                user = db.users.find_one({"_id": user_id})
                user_friends = []
                for row in fp:
                    row = row.replace('\n', '')
                    friend_id, com_friends = row.split(': ')
                    com_friends = com_friends.split(' ')
                    user_friends.append(friend_id)
                    k = self._get_com_key(user_id, friend_id)
                    try:
                        db.friends.insert({"_id": k, "friends": com_friends})
                    except:
                        pass
                db.users.update({"_id": user_id}, {"$set": {'friends': user_friends}})

    def load_circles():
        ''' loads train circles '''
        print 'train circles loading starts ', datetime.now()
        egonets_files = [ f for f in listdir('Training') if isfile(join('Training/',f)) ]
        for f in egonets_files:
            with open('Training/%s' % f) as fp:
                user_id = f.split('.')[0]
                user = db.users.find_one({"_id": user_id})


class CircleMaker:
    def __init__(self, users):
        self.circles = defaultdict(list)
        self.friends = defaultdict(dict)
        self.users = users
        self._fill_friends()

    def _fill_friends(self):
        for user_id in self.users:
            with open('egonets/%s.egonet' % user_id) as fp:
                for line in fp.xreadlines():
                    line = line.replace('\r', '').replace('\n', '')
                    friend_id, common_friends = line.split(': ', 1)
                    self.friends[user_id][friend_id] = common_friends.split(' ')

    def get_best_friends_circles(self):
        for user_id, friends in self.friends.iteritems():
            user_features = db.users.find_one({"_id": user_id})
            friends_features = db.features.find({"_id": {"$in": friends.keys()}})
            com_cntr = Counter()
            for ff in friends_features:
                com_features = { k:v for k, v in user_features.iteritems() if ((k in ff)and(user_features[k] == ff[k])) }
                com_cntr.update(com_features.keys())
            com_most = [i[0] for i in com_cntr.most_common(3)]
            conditions = { k:v for k, v in user_features.iteritems() if k in com_most}
            conditions.update({"_id": {"$nin": friends.keys() + [user_id, ]}})
            best_friends = db.features.find(conditions)
            self.circles[user_id].append([i['_id'] for i in best_friends])
            

    def get_cluster_circles(self):
        ''' get data of common friends from egonet and append to self.circles_list'''
        all_features = open('featureList.txt').read().split('\n')[:-1]
        for user_id in self.users:
            # loading data of egonet
            user_features = db.users.find_one({"_id": user_id})
            with open('egonets/%s.egonet' % user_id) as fp:
                common_list = defaultdict(list)
                for line in fp.xreadlines():
                    line = line.replace('\r', '').replace('\n', '')
                    friend_id, common_friends = line.split(': ', 1)
                    common_list[friend_id] = common_friends.split(' ')
                    self.friends[user_id].append(friend_id)
            # preparing for clustring
            for friend_id in common_list:
                friend_features = db.users.find_one({"_id": friend_id})
                features_data = [
                        (i, 1 if i in friend_features and i in user_features else 0) 
                        for i in all_features
                ]
                data = [(i, 1 if i in common_list[friend_id] else 0) for i in common_list]
                data += features_data
                data = np.array([v for k, v in sorted(data, key= lambda x: x[0])])
                common_list[friend_id] = data
            # clusreting
            n_clusters = (len(common_list) / 7) + 1
            #clu = cluster.WardAgglomeration(n_clusters=n_clusters)
            clu = cluster.FeatureAgglomeration(affinity='cosine', linkage='complete', n_clusters=n_clusters)
            clu.fit(np.array(common_list.values()))
            circles = defaultdict(list)
            for k, v in izip(common_list, clu.labels_):
                circles[v].append(k)
            for circle in circles.values():
                if len(circle) > 2 and len(circle) < min(len(common_list) / 4, 8):
                    self.circles[user_id].append(circle)

    def write_results(self, fname):
        with open(fname, 'w') as fp:
            fp.write("UserId,Predicted\n")
            for user_id in self.users:
                row = "%s," % user_id
                data = ';'.join([' '.join(c) for c in self.circles[user_id] if c])
                if data:
                    row += data + '\n'
                else:
                    row += ' '.join(friend_id for friend_id in self.friends[user_id].keys()) + '\n'
                print row
                fp.write(row)


if __name__ == "__main__":
    # ETL
    dl = DataLoader()
    #db.drop_collection('users')
    #db.drop_collection('friends')
    #dl.load_features_data()
    #dl.load_friends_data()

    # train users
    #users = ['8239', '25159', '2738', '9103', '5881', '16203', '16378', '26321', '27022', '5494', '22650', '3735', '25568', '1968', '16869', '345', '11014', '11364', '1839', '6413', '24758', '25773', '2790', '23299', '26492', '2365', '16642', '23157', '13789', '11186', '8100', '15672', '239', '611', '1357', '8777', '18543', '8553', '13353', '19788', '9846', '12800', '3059', '18005', '22824', '10929', '7667', '9642', '11410', '19129', '2895', '4406', '4829', '9947', '5212', '2255', '24857', '6726', '17951', '10395']
    # test users
    users = ['25708', '2473', '18844', '19268', '25283', '21869', '17748', '5744', '3656', '17002', '26827', '10793', '17497', '23978', '850', '1813', '15515', '20050', '22364', '0', '7983', '11818', '12178', '26019', '3581', '14103', '19608', '14129', '1310', '18612', '1099', '22223', '2630', '20518', '12535', '13471', '6934', '3077', '9199', '3703', '8338', '3236', '2976', '21098', '13687', '15227', '5087', '8890', '24812', '23063']

    # circle detection
    cm = CircleMaker(users)
    cm.get_best_friends_circles()
    #cm.get_cluster_circles()
    cm.write_results('result_features2.csv')