import pandas as pd
import numpy as np
from collections import defaultdict
num_user_features = 52
num_item_features = 137
num_user = 22873
num_item = 19413
user_dict = {}

# COUPON_ID_hash --> [feature1, feature2,...]
train_item_dict = {}
test_item_dict = {}

train_coupon_hash = []
test_coupon_hash = []

# item_heading['PRICE_RATE'] is the column id for 'PRICE_RATE'
item_heading = {}
user_heading = {}

def load_dictionary_simple():
    with open("../trans_data/factor_training_coupon.txt") as f:
        heading = f.readline().split("\t")
        for i in range(len(heading)):
            item_heading[heading[i].replace('"',"")] = i
        for row in f.read().splitlines():
            item_info = row.split("\t")
            features = [float(i) for i in item_info[1:]]
            coupon_hash = item_info[0].replace('"', "")
            train_item_dict[coupon_hash] = features
            train_coupon_hash.append(coupon_hash)
    with open("../trans_data/factor_testing_coupon.txt") as f:
        for row in f.read().splitlines()[1:]:
            item_info = row.split("\t")
            features = [float(i) for i in item_info[1:]]
            coupon_hash = item_info[0].replace('"', "")
            test_item_dict[coupon_hash] = features
            test_coupon_hash.append(coupon_hash)
    with open("../trans_data/factor_users.txt") as f:
        heading = f.readline().split("\t")
        for i in range(len(heading)):
            user_heading[heading[i]] = i
        for row in f.read().splitlines():
            user_info = row.split("\t")
            features = [float(i.replace('"',"")) for i in user_info[1:]]
            user_dict[user_info[0].replace('"', "")] = features

def load_sda_feature():
  #train = pd.read_csv('../trans_data/sda_train_coupon.dat', header=-1)
  #test = pd.read_csv('../trans_data/sda_test_coupon.dat', header=-1)

  train = pd.read_csv('../trans_data/sda_train_coupon_lr3.000000_3.000000.dat', header=-1)
  test = pd.read_csv('../trans_data/sda_test_coupon_lr3.000000_3.000000.dat', header=-1)

  # standardize train and test to [0, 1].
  train_mat = train.ix[:,2:].values
  test_mat = test.ix[:,2:].values
  print 'train_mat shape:', train_mat.shape
  print 'test_mat shape:', test_mat.shape
  num_train = train_mat.shape[0]
  num_test = test_mat.shape[0]
  combined = np.r_[train_mat, test_mat]
  combined = combined - np.min(combined, axis=0)
  combined = combined / np.max(combined, axis=0)

  for i, t in enumerate(train.itertuples()):
    coupon_hash = t[1]
    coupon_small_area = t[2]
    train_item_dict[(coupon_hash, coupon_small_area)] = list(combined[i,:])
  print 'coupon_dim:', len(train_item_dict.itervalues().next())
  for i, t in enumerate(test.itertuples()):
    coupon_hash = t[1]
    coupon_small_area = t[2]
    test_item_dict[(coupon_hash, coupon_small_area)] = \
        list(combined[i + num_train, :])
  print '# train (coupons, small_area) pairs:', len(train_item_dict)
  print '# test (coupons, small_area) pairs:', len(test_item_dict)

def load_loc_feature():
  train = pd.read_csv('../data/factor_training_coupon_loc.txt', sep='\t')
  test = pd.read_csv('../data/factor_testing_coupon_loc.txt', sep='\t')
  for i in range(len(train.columns)):
    # -2 because we drops coupon_hash and coupon_small_area.
    item_heading[train.columns[i]] = i - 2

  # standardize train and test to [0, 1].
  train_mat = train.ix[:,2:].values
  test_mat = test.ix[:,2:].values
  print 'train_mat shape:', train_mat.shape
  print 'test_mat shape:', test_mat.shape
  num_train = train_mat.shape[0]
  num_test = test_mat.shape[0]
  combined = np.r_[train_mat, test_mat]
  combined = combined - np.min(combined, axis=0)
  combined = combined / np.max(combined, axis=0)

  """
  for i in xrange(num_train):
    coupon_hash = train.ix[i, 0]
    coupon_small_area = train.ix[i, 1]
    train_item_dict[(coupon_hash, coupon_small_area)] = list(combined[i,:])
  for i in xrange(num_test):
    coupon_hash = test.ix[i, 0]
    coupon_small_area = test.ix[i, 1]
    test_item_dict[(coupon_hash, coupon_small_area)] = \
        list(combined[i + num_train,:])
  """
  for i, t in enumerate(train.itertuples()):
    coupon_hash = t[1]
    coupon_small_area = t[2]
    train_item_dict[(coupon_hash, coupon_small_area)] = list(combined[i,:])
  print 'coupon_dim:', len(train_item_dict.itervalues().next())
  for i, t in enumerate(test.itertuples()):
    coupon_hash = t[1]
    coupon_small_area = t[2]
    test_item_dict[(coupon_hash, coupon_small_area)] = \
        list(combined[i + num_train, :])
  print '# train (coupons, small_area) pairs:', len(train_item_dict)
  print '# test (coupons, small_area) pairs:', len(test_item_dict)

def GetTrainTestPurchase(test_coupon_list):
    train_purchase = defaultdict(list)
    test_purchase = defaultdict(list)  # similar to test.
    with open("../data/coupon_detail_train.csv") as fin:
        for row in fin.read().splitlines()[1:]:
            purchase = row.split(',')
            #item_count = int(purchase[0])
            user = purchase[4]
            item = purchase[5]
            small_area_name = purchase[2]
            if item not in test_coupon_list:
                train_purchase[user].append(item)
            else:
                test_purchase[user].append(item)
    return train_purchase, test_purchase

def GetTrainTestPurchaseAreaAug(test_coupon_list):
    # train: (USER_ID_hash, small_area_name) -->
    # [purchased_item1, purchased_item2, ...]
    train_purchase = defaultdict(list)
    test_purchase = defaultdict(list)  # similar to test.
    coupon_detail = pd.read_csv("../data/coupon_detail_train.csv")
    column_idx = dict(zip(coupon_detail.columns, \
        xrange(len(coupon_detail.columns))))
    num_train_purchases = 0
    num_test_purchases = 0
    for t in coupon_detail.itertuples():
      # +1 because t[0] is row index.
      user = t[column_idx['USER_ID_hash'] + 1]
      item = t[column_idx['COUPON_ID_hash'] + 1]
      small_area_name = t[column_idx['SMALL_AREA_NAME'] + 1]
      if item not in test_coupon_list:
          train_purchase[user].append((item, small_area_name))
          num_train_purchases += 1
      else:
          test_purchase[user].append(item)
          num_test_purchases += 1
    print 'Read ', num_train_purchases, ' train purchases (', \
        len(train_purchase), ' (users,small_area) pairs) and ',\
        num_test_purchases, ' test purchases (', len(test_purchase),\
        'users)'
    return train_purchase, test_purchase

#load_dictionary_simple()
