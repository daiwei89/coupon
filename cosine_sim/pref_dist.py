import pandas as pd
import numpy as np
from collections import defaultdict

pref_loc = pd.read_csv('../data/prefecture_locations.csv')

loc_dict = {}

for t in pref_loc.itertuples():
  loc_dict[t[1]] = np.array([t[3],t[4]])

def Dist(loc1, loc2):
  return np.dot(loc1 - loc2, np.transpose(loc1 - loc2)) ** 0.5

total_dist = 0.0
num_pairs = 0
for pref1, loc1 in loc_dict.iteritems():
  for pref2, loc2 in loc_dict.iteritems():
    if not pref2 == pref1:
      total_dist += Dist(loc1, loc2)
      num_pairs += 1
print 'avg distance', total_dist/num_pairs, ' # pairs:', num_pairs

neighbors = defaultdict(list)
threshold = 0.8
for pref1, loc1 in loc_dict.iteritems():
  for pref2, loc2 in loc_dict.iteritems():
    if not pref2 == pref1:
      if Dist(loc1, loc2) < threshold:
        neighbors[pref1].append(pref2)
  print pref1, 'has', len(neighbors[pref1]), 'neighbors'
