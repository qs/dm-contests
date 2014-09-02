from pymongo import MongoClient
from datetime import datetime
from collections import OrderedDict, Counter


client = MongoClient()
db = client.soccir

def load_features_data():
    print 'data loading starts ', datetime.now()
    db.drop_collection('features')  # remove prev data
    features_list = [i[:-1] for i in open('featureList.txt').readlines()]
    features_vals = set([])
    col_features = db.features
    with open('features.txt') as fp:
        for line in fp.xreadlines():
            line = line.replace('\r', '').replace('\n', '')
            user_id, features = line.split(' ', 1)
            for i in features:
                features_vals.add(i)
            features = dict([i.rsplit(';', 1) for i in features.split(' ')])
            features['_id'] = features.pop('id')
            col_features.insert(features)
    print 'data inserted into collection ', datetime.now()
    for k in features_list:
        col_features.create_index(k)
    print 'data index created ', datetime.now()

def common_features_egonet():
    with open('testSet_users_friends.csv') as fp:
        with open('result.csv', 'w') as fpw:
            fpw.write("UserId,Predicted\n")
            for line in fp.xreadlines():
                line = line.replace('\r', '').replace('\n', '')
                user_id, friends = line.split(': ', 1)
                friends = friends.split(' ')
                user_features = db.features.find_one({"_id": user_id})
                friends_features = db.features.find({"_id": {"$in": friends}})
                com_cntr = Counter()
                for ff in friends_features:
                    com_features = { k:v for k, v in user_features.iteritems() if ((k in ff)and(user_features[k] == ff[k])) }
                    com_cntr.update(com_features.keys())
                com_most = [i[0] for i in com_cntr.most_common(4)]
                conditions = { k:v for k, v in user_features.iteritems() if k in com_most}
                conditions.update({"_id": {"$nin": friends + [user_id, ]}})
                new_friends = db.features.find(conditions)
                new_friends_ids = [i['_id'] for i in new_friends]
                # write result
                r = "%s,%s\n" % (user_id, ' '.join(friends + new_friends_ids))
                print r
                fpw.write(r)

if __name__ == "__main__":
    #load_features_data()
    #print 'data loaded'
    common_features_egonet()
    