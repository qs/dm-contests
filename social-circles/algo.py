from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.soccir

def load_data():
    print 'data loading starts ', datetime.now()
    db.drop_collection('features')  # remove prev data
    features_list = [i[:-1] for i in open('featureList.txt').readlines()]
    col_features = db.features
    with open('features.txt') as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            user_id, features = line.split(' ', 1)
            features = dict([i.rsplit(';', 1) for i in features.split(' ')])
            features['_id'] = features.pop('id')
            col_features.insert(features)
    print 'data inserted into collection ', datetime.now()
    for k in features_list:
        col_features.create_index(k)
    print 'data index created ', datetime.now()

if __name__ == "__main__":
    #load_data()
    pass