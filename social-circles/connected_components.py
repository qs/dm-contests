import networkx as nx
from collections import defaultdict
import sys
import re
from pymongo import MongoClient

client = MongoClient()
db = client.soccir

def read_nodeadjlist(filename):
  G = nx.Graph()
  user_id = re.findall(r'([0-9]+)\.egonet', filename)[0]
  user_features = db.users.find_one({"_id": user_id})
  for line in open(filename):
    e1, es = line.split(':')
    es = es.split()
    for e in es:
      if e == e1: continue
      G.add_edge(e1, e)
  return G

def findCommunities(filename):
  G = read_nodeadjlist(filename)
  #c = nx.connected_components(G)
  c = nx.biconnected_components(G)
  #print list(c), type(c)
  #exit()
  return c

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Expected list of ego networks, e.g. 'python link_clustering.py *.egonet'"
    sys.exit(0)
  print "UserId,Predicted"
  for arg in sys.argv[1:]:
    egoUser = -1
    try:
      egoUser = int(arg.split('/')[-1].split('.egonet')[0])
    except Exception as e:
      print "Expected files to be names 'X.egonet' where X is a user ID"
      sys.exit(0)
    cs = list(findCommunities(arg))
    if len(cs) == 0:
      cs = [set(adj.keys())]
    cs = [' '.join([str(y) for y in x if re.match(r'^[0-9]+$', y)]) for x in cs]
    print str(egoUser) + ',' + ';'.join([c for c in cs if len(c) < 15])
