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


def get_common_features():
    ''' get most common features for circle selection '''


def common_features_egonet():
    with open('testSet_users_friends.csv') as fp:
        with open('result3.csv', 'w') as fpw:
            fpw.write("UserId,Predicted\n")
            for line in fp.xreadlines():
                line = line.replace('\r', '').replace('\n', '')
                user_id, friends = line.split(': ', 1)
                friends = friends.split(' ')
                user_features = db.users.find_one({"_id": user_id})
                friends_features = list(db.users.find({"_id": {"$in": friends}}))
                circles = []
                # getting best friends - most common features
                better_friends = Counter()
                for ff in friends_features:
                    com_features = { k:v for k, v in user_features.iteritems() if ((k in ff)and(user_features[k] == ff[k])) }
                    better_friends[ff['_id']] = len(com_features)
                best_friends = [i[0] for i in better_friends.most_common(4)]
                #print 'best friends:', best_friends
                circles.append(best_friends)
                # collegues
                collegues = []
                for ff in friends_features:
                    com_features = { k:v for k, v in user_features.iteritems() if ((k in ff)and(user_features[k] == ff[k])and('work' in k)) }
                    if len(com_features) > 2:
                        collegues.append(ff['_id'])
                #print 'collegues:', collegues
                circles.append(collegues)
                [friends_features.remove(i) for i in friends_features if i['_id'] in collegues]
                # school mates
                school_mates = []
                for ff in friends_features:
                    com_features = { k:v for k, v in user_features.iteritems() if ((k in ff)and(user_features[k] == ff[k])and('education' in k)) }
                    if len(com_features) > 2:
                        school_mates.append(ff['_id'])
                #print 'school_mates:', school_mates
                circles.append(school_mates)
                [friends_features.remove(i) for i in friends_features if i['_id'] in school_mates]
                # local_mates
                local_mates = []
                for ff in friends_features:
                    com_features = { k:v for k, v in user_features.iteritems() if ((k in ff)and(user_features[k] == ff[k])and('local' in k)) }
                    if len(com_features) > 2:
                        local_mates.append(ff['_id'])
                #print 'local_mates:', local_mates
                circles.append(local_mates)
                [friends_features.remove(i) for i in friends_features if i['_id'] in local_mates]
                
                row = "%s," % user_id
                row += ';'.join([' '.join(c) for c in circles if c]) + '\n'
                print row
                fpw.write(row)


if __name__ == "__main__":
    db.drop_collection('users')
    db.drop_collection('friends')

    load_features_data()
    load_friends_data()
    #print 'data loaded'
    #common_features_egonet()
    