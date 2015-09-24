import os
from os.path import dirname
from os.path import join
import pandas as pd
import numpy as np
from factor_util import *
from random import shuffle
from collections import defaultdict
from random import randrange, sample

def Dedup(seq):
  seen = set()
  seen_add = seen.add
  return [ x for x in seq if not (x in seen or seen_add(x))]

def GetUserPurchases(exclude_coupon_list):
  """
  return
  train_coupon_list: ordered list of coupon hash. 
  dictionary: USER_ID_hash --> [purchase_coupon_hash1, ...]
  """
  train_coupon = GetTrainCouponDf()
  train_coupon_hash = list(train_coupon['COUPON_ID_hash'].values)
  # USER_ID_hash --> [purchased_item1, purchased_item2, ...]
  train_purchase = defaultdict(list)
  #test = defaultdict(list)  # similar to test.
  with open("../data/coupon_detail_train.csv") as fin:
    for row in fin.read().splitlines()[1:]:
      fields = row.split(',')
      user = fields[4]
      item = fields[5]
      if item not in exclude_coupon_list:
        train_purchase[user].append(item)
  return train_coupon_hash, train_purchase

def GenerateSimDissimPairsUnvisit(test_coupon_list):
  """
  Co-purchases are sim pairs, between a purchase and the rest pair is a
  random.
  """
  train_coupon_hash, train_purchase = GetUserPurchases(test_coupon_list)
  num_coupons = len(train_coupon_hash)

  #train_coupons = GetTrainCouponDf()['COUPON_
  co_purchase = np.zeros((num_coupons, num_coupons))

  num_sim_pairs = 0
  with open('../trans_data/sim_pairs_unvisit.txt', 'w') as sim_f:
    for user, coupons in train_purchase.iteritems():
      coupons_id = [train_coupon_hash.index(i) for i in Dedup(coupons)]
      for x in coupons_id:
        for y in coupons_id:
          if not x == y:
            big = x if x > y else y
            small = y if x > y else x
            sim_f.write('%d %d\n' % (small, big))
            co_purchase[small,big] = 1
            num_sim_pairs += 1
  print 'num_sim_pairs', num_sim_pairs

  num_dsim_pairs = 0
  with open('../trans_data/dsim_pairs_unvisit.txt', 'w') as f:
    for i in range(num_coupons):
      # pick 170 pairs for each coupon (should come out roughly 3M pairs)
      others = range(i+1, num_coupons)
      shuffle(others)
      for j in others[:170]:
        if not co_purchase[i, j] == 1:
          f.write('%d %d\n' % (i, j))
          num_dsim_pairs += 1
  print 'num_dsim_pairs', num_dsim_pairs

def GenerateSimPairsMultiCopurchase(test_coupon_list):
  threshold = 5
  dsim_multiple = 10
  train_coupon_hash, train_purchase = GetUserPurchases(test_coupon_list)
  num_coupons = len(train_coupon_hash)
  num_sim_pairs = 0
  co_purchase = np.zeros((num_coupons, num_coupons))
  sim_pairs = {}
  sim_file = '../trans_data/sim_pairs_%d_copurchase.txt' % threshold
  with open(sim_file, 'w') as sim_f:
    for user, coupons in train_purchase.iteritems():
      coupons_id = [train_coupon_hash.index(i) for i in Dedup(coupons)]
      for x in coupons_id:
        for y in coupons_id:
          if not x == y:
            big = x if x > y else y
            small = y if x > y else x
            co_purchase[small, big] += 1
            if co_purchase[small, big] == threshold:
              sim_f.write('%d %d\n' % (small, big))
              sim_pairs[(small, big)] = 1
              num_sim_pairs += 1
  print 'num_sim_pairs', num_sim_pairs
  print 'len(sim_pairs)', len(sim_pairs)

  dsim_file = '../trans_data/dsim_pairs_%d_copurchase.txt' % threshold
  with open(dsim_file, 'w') as f:
    num_dsim_pairs = 0
    dsim_pairs = {}
    while len(dsim_pairs) < len(sim_pairs) * dsim_multiple:
      sim_pair = sample(sim_pairs.keys(), 1)[0]
      in_sim = sim_pair[randrange(2)] # coupon that's in sim_pairs
      other = randrange(num_coupons)
      small = other if in_sim >= other else in_sim
      big = in_sim if in_sim >= other else other
      if (not in_sim == other) and ((small, big) not in sim_pairs) and \
      ((small, big) not in dsim_pairs):
        dsim_pairs[(small, big)] = 1
        num_dsim_pairs += 1
        f.write('%d %d\n' % (small, big))
  print 'wrote', num_sim_pairs, 'sim pairs to', sim_file, ', and', \
  num_dsim_pairs, 'to', dsim_file



def GenerateSimDissimPairs(test_coupon_list):
  train_coupon_hash, train_purchase = GetUserPurchases(test_coupon_list)

  num_sim_pairs = 0
  with open('../trans_data/sim_pairs.txt', 'w') as sim_f:
    for user, coupons in train_purchase.iteritems():
      coupons_id = [train_coupon_hash.index(i) for i in Dedup(coupons)]
      for x in coupons_id:
        for y in coupons_id:
          if not x == y:
            sim_f.write('%d %d\n' % (x, y))
            num_sim_pairs += 1
  print 'num_sim_pairs', num_sim_pairs

  train_visit = defaultdict(list)
  with open("../data/coupon_visit_train.csv") as fin:
    for row in fin.read().splitlines()[1:]:
      fields = row.split(',')
      coupon_hash = fields[4]
      user_hash = fields[5]
      train_visit[user_hash].append(coupon_hash)

  num_dsim_pairs = 0
  with open('../trans_data/dsim_pairs.txt', 'w') as dsim_f:
    num_users_examined = 0
    for user, coupons in train_visit.iteritems():
      if num_users_examined % 100 == 0:
        print 'got through %d users' % num_users_examined
      if num_dsim_pairs > 10000000:
        print 'reach maximum pairs; num_users: %d' % num_users_examined
        break
      coupons_id = []
      for i in Dedup(coupons):
        if i in train_coupon_hash:
          coupons_id.append(train_coupon_hash.index(i))
      purchase_id = [train_coupon_hash.index(i) for i in
          Dedup(train_purchase[user])]
      for x in purchase_id:
        if x in coupons_id:
          coupons_id.remove(x)
      # now coupons_id are viewed but not purchase.
      for x in coupons_id:
        for y in purchase_id:
          dsim_f.write('%d %d\n' % (x, y))
          num_dsim_pairs += 1
      num_users_examined += 1
  print 'num_dsim_pairs', num_dsim_pairs

def AvgCosineDistance(matrix):
  num_train = matrix.shape[0]
  total_dist = 0.0
  num_samples = 100000
  for i in range(num_samples):
    a = randrange(num_train)
    b = randrange(num_train)
    total_dist += np.dot(matrix[a,:], np.transpose(matrix[b,:]))
  avg_dist = total_dist / num_samples
  print 'avg_dist: ', avg_dist
  return avg_dist

def WriteDMLData():
  train_coupon = GetTrainCouponDf()
  train_coupon_hash = list(train_coupon['COUPON_ID_hash'].values)
  train_coupon.drop('COUPON_ID_hash', axis=1, inplace=True)
  feature_dim = len(train_coupon.columns)
  print('feature_dim: %d' % feature_dim)
  train_coupon_np = train_coupon.values
  avg_dist = AvgCosineDistance(train_coupon_np)
  train_coupon_np = np.divide(train_coupon_np, avg_dist**0.5)
  avg_dist = AvgCosineDistance(train_coupon_np)
  num_train = train_coupon_np.shape[0]
  print(train_coupon_np.shape)
  with open(join(trans_data_dir, 'train_coupon.dml'), 'w') as f:
    for i in xrange(num_train):
      nz_idx = np.nonzero(train_coupon_np[i,:])[0]
      #f.write('%s %d ' % (train_coupon_hash[i], len(nz_idx)))
      f.write('0 %d ' % len(nz_idx))
      for j in nz_idx:
        f.write('%d:%.4f ' % (j, train_coupon_np[i,j]))
      f.write('\n')

if __name__ == "__main__":
  f = open("../trans_data/cross_valid_coupon.txt")
  test_lists = []
  for coupons in f.readlines():
    samples = coupons.split(',')
    test_list = samples[:-1]
    test_list.extend(samples[-1].replace('\n',''))
    test_lists.append(test_list[:310])
  #GenerateSimDissimPairs(test_lists[0])
  #GenerateSimDissimPairsUnvisit(test_lists[0])
  #GenerateSimPairsMultiCopurchase(test_lists[0])
  GenerateSimPairsMultiCopurchase(list())
  #WriteDMLData()
