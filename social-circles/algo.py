from pymongo import MongoClient
from datetime import datetime
from collections import OrderedDict, Counter

from os import listdir
from os.path import isfile, join


client = MongoClient()
db = client.soccir

def load_features_data():
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

def _get_com_key(user_id, friend_id):
    if int(user_id) > int(friend_id):
        return "%s_%s" % (friend_id, user_id)
    else:
        return "%s_%s" % (user_id, friend_id)

def load_friends_data():
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
                k = _get_com_key(user_id, friend_id)
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

def load_common_friends():
    ''' loading data from egonets/ '''


def _get_circle_on_features(user_features, friends_features, features_list, common_cnt=2):
    circle = []
    for ff in friends_features:
        com_features = { k:v for k, v in user_features.iteritems() 
                if ( (k in ff) and (user_features[k] == ff[k]) and [True for f in features_list if f in k] ) }
        if len(com_features) > common_cnt:
            circle.append(ff['_id'])
    return circle

def common_features_egonet():
    with open('testSet_users_friend.csv') as fp:
        with open('result5.csv', 'w') as fpw:
            fpw.write("UserId,Predicted\n")
            for line in fp.xreadlines():
                line = line.replace('\r', '').replace('\n', '')
                user_id, friends = line.split(': ', 1)
                friends = friends.split(' ')
                user_features = db.users.find_one({"_id": user_id})
                friends_features = list(db.users.find({"_id": {"$in": friends}}))
                circles = []
                print 'USER_ID::::', user_id
                # getting best friends - most common features
                better_friends = Counter()
                for ff in friends_features:
                    com_features = { k:v for k, v in user_features.iteritems() if ((k in ff)and(user_features[k] == ff[k])) }
                    better_friends[ff['_id']] = len(com_features)
                best_cnt = len(friends_features) / 100 or 3
                best_friends = [i[0] for i in better_friends.most_common(best_cnt)]
                #print 'best friends:', best_friends
                circles.append(best_friends)

                # collegues
                collegues = _get_circle_on_features(user_features, friends_features, ['work', ], 2)
                circles.append(collegues)
                print 'collegues', collegues
                #[friends_features.remove(i) for i in friends_features if i['_id'] in collegues]

                # school mates
                school_mates = _get_circle_on_features(user_features, friends_features, ['education', ], 4)
                circles.append(school_mates)
                print 'school_mates', school_mates
                #[friends_features.remove(i) for i in friends_features if i['_id'] in school_mates]

                # local_mates
                local_mates = _get_circle_on_features(user_features, friends_features, ['loca', ], 3)
                circles.append(local_mates)
                print 'local_mates', local_mates
                [friends_features.remove(i) for i in friends_features if i['_id'] in local_mates]

                # home_mates
                home_mates = _get_circle_on_features(user_features, friends_features, ['hometown', ], 2)
                circles.append(home_mates)
                print 'home_mates', home_mates
                [friends_features.remove(i) for i in friends_features if i['_id'] in home_mates]

                # other_mates
                [friends_features.remove(i) for i in friends_features if i['_id'] in collegues]
                [friends_features.remove(i) for i in friends_features if i['_id'] in school_mates]
                other_mates = _get_circle_on_features(user_features, friends_features, ['', ], 7)
                circles.append(other_mates)
                print 'other_mates', other_mates
                [friends_features.remove(i) for i in friends_features if i['_id'] in other_mates]
                
                row = "%s," % user_id
                row += ';'.join([' '.join(c) for c in circles if c]) + '\n'
                print row
                fpw.write(row)

def get_cluster_circles():
    with open('egonets/850.egonet') as fp:
        data = {}
        for row in fp:
            row = row.replace('\n', '')
            user_id, comm = row.split(': ')
            comm = set(comm.split(' '))
            data[user_id] = comm
        clu = cluster.WardAgglomeration(n_clusters=5)
        clu.fit(np.array(arrs.values()), np.array(arrs.keys()))
        clu.labels_


def write_results(circles_list):
    with open('result5.csv', 'w') as fp:
        for user_id, circles in circles_list.itemitems():
            row = "%s," % user_id
            row += ';'.join([' '.join(c) for c in circles if c]) + '\n'
            print row
            fp.write(row)


if __name__ == "__main__":
    #db.drop_collection('users')
    #db.drop_collection('friends')
    #load_features_data()
    #load_friends_data()
    #common_features_egonet()
    #TODO leave best friends, other circlies get from clustering common nbrs
    
    circles_list = {} # 'user_id': [['123', '124'], [...], [...]]
    circles_list = get_cluster_circles()
    write_results(circles_list)