
import numpy as np
from generate_features import *
from factor_util import *
import pandas as pd
from collections import defaultdict
import sys

def GetNeighborPref(threshold):
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
  print 'use threshold', threshold

  neighbors = defaultdict(list)
  for pref1, loc1 in loc_dict.iteritems():
    for pref2, loc2 in loc_dict.iteritems():
      if not pref2 == pref1:
        if Dist(loc1, loc2) < threshold:
          neighbors[pref1].append(pref2)
    print pref1, 'has', len(neighbors[pref1]), 'neighbors'
  return neighbors

#threshold = 0.8
threshold = 5.31
neighbor_pref = GetNeighborPref(threshold)


train_purchases, test_purchases = GetTrainTestPurchase(list())
users = pd.read_csv('../data/user_list.csv')
user_ken_dict = {}
for r in users.iterrows():
  user_ken_dict[r[1]['USER_ID_hash']] = r[1]['PREF_NAME']

train_coupon = pd.read_csv('../data/coupon_list_train.csv')
train_coupon_pref = {}
for r in train_coupon.iterrows():
  train_coupon_pref[r[1]['COUPON_ID_hash']] = r[1]['ken_name']

num_purchases = 0
num_local_purchases = 0
for user, coupons in train_purchases.iteritems():
  #user_ken = user_dict[user][4:-1]
  user_ken = user_ken_dict[user]
  user_neighbor_pref = neighbor_pref[user_ken]
  for c in coupons:
    if c not in train_item_dict:
      continue
    coupon_pref = train_coupon_pref[c]
    #coupon_ken = train_item_dict[c][34:81]
    #print len(coupon_ken)
    #dot = np.dot(user_ken, coupon_ken)
    #assert dot == 0 or dot == 1
    #if dot == 0:
    if coupon_pref == user_ken or (coupon_pref in user_neighbor_pref):
      num_local_purchases += 1
    num_purchases += 1
print 'local purchase percent:', float(num_local_purchases) / num_purchases

