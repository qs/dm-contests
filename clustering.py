

'''
27473 last_name;16976 locale;1 hometown;name;4299 hometown;id;4313 
birthday;4285 education;school;name;11574 education;school;id;12242 education;type;0 education;year;name;26 education;year;id;30 education;school;name;17934 education;school;id;19060 education;type;1 education;year;name;25 education;year;id;29 id;27473 first_name;2931 name;27238 gender;0 work;position;name;378 work;position;id;386 work;start_date;4 work;employer;name;18284
 work;employer;id;19031 work;employer;name;18285 work;employer;id;19032 location;name;119 location;id;119
'''
def load_users_features(fname):
    features_data = []
    with open(fname) as f:
        for row in f.readlines():
            row = row[:-1].split(' ')
            data = {}
            data['id'] = row.pop(0)
            for r in row:
                k, v = r.rsplit(';', 1)
                data[k] = v
            features_data.append(data)
    return features_data

users = load_users_features('features.txt')
print users[100:103]