import os
from os.path import dirname
from os.path import join
import pandas as pd
import collections
import sys
from util import *
from sklearn.feature_extraction import DictVectorizer as DV
import numpy as np
import itertools

project_dir = dirname(dirname(os.path.realpath(__file__)))
data_dir = join(project_dir, 'data')

remapped_purchase_f = join(data_dir, 'remapped_coupon_detail_train.csv')
libsvm_train = join(data_dir, 'pair_train.libsvm')
libsvm_test = join(data_dir, 'pair_test.libsvm')

if __name__ == "__main__":
  # generate train
  remap_purchases = pd.read_csv(remapped_purchase_f)
  pairs = collections.defaultdict(int)
  for tuple in zip(remap_purchases.ITEM_COUNT,
    remap_purchases.USER_ID_hash, remap_purchases.COUPON_ID_hash):
    user_id = int(tuple[1])
    coupon_id = int(tuple[2])
    pairs[user_id, coupon_id] += int(tuple[0])

  # purchase pair df
  pairs_list = [ (p[0][0], p[0][1], p[1]) for p in pairs.iteritems()]
  pairs_df = pd.DataFrame(pairs_list, columns=['user_id',
  'coupon_id', 'purchase_count'])

  users = GetUserDf()

  # test pairs.
  test_coupons = GetCouponTestDf()
  test_coupons_list = test_coupons['coupon_id'].tolist()
  user_list = users['user_id'].tolist()
  test_pairs_list = list(itertools.product(user_list, test_coupons_list))
  test_pairs_df = pd.DataFrame(test_pairs_list, columns=['user_id',
    'coupon_id'])
  assert kNumUserCouponTest == len(test_pairs_df.index)

  # train join with train coupon
  train_coupons = GetCouponTrainDf()
  train_coupons.set_index('coupon_id', inplace = True)
  pairs_coupon_df = pairs_df.join(train_coupons, on='coupon_id', how='left')

  # test join with test coupon
  test_coupons.set_index('coupon_id', inplace = True)
  test_pairs_coupon_df = test_pairs_df.join(test_coupons, on='coupon_id',
      how='left')

  # train join with user list
  users.set_index('user_id', inplace = True)
  pairs_coupon_user_df = pairs_coupon_df.join(users, on='user_id', how='left')
  assert kNumUserCouponPurchase == len(pairs_coupon_user_df.index)
  print('pairs_coupon_user_df')
  print(pairs_coupon_user_df.head())
  print(pairs_coupon_user_df.isnull().sum())
  print(len(pairs_coupon_user_df.index))

  # test join with user list
  test_pairs_coupon_user_df = test_pairs_coupon_df.join(users, on='user_id',
      how='left')
  # differ only by 'purchase_count'
  assert len(pairs_coupon_user_df.columns) - 1 == \
    len(test_pairs_coupon_user_df.columns)

  # numeric features in train
  num = pairs_coupon_user_df[['PRICE_RATE', 'CATALOG_PRICE', 'DISCOUNT_PRICE',
    'DISPPERIOD', 'AGE']]
  assert 0 == num.isnull().sum().sum(), "contains null value"
  assert kNumUserCouponPurchase == len(num.index)
  train_mean = num.mean()
  train_span = num.max() - num.min()
  num_norm = (num - train_mean) / train_span
  print(num_norm.head())
  num_array = num_norm.as_matrix()
  #print(num_array.shape)

  # numeric features in test
  test_num = test_pairs_coupon_user_df[['PRICE_RATE', 'CATALOG_PRICE',
    'DISCOUNT_PRICE', 'DISPPERIOD', 'AGE']]
  assert 0 == test_num.isnull().sum().sum(), "contains null value"
  test_num_norm = (test_num - train_mean) / train_span
  test_num_array = test_num_norm.as_matrix()

  # train categorical features
  cat = pairs_coupon_user_df[['CAPSULE_TEXT','GENRE_NAME','large_area_name',
    'ken_name','small_area_name','SEX_ID','PREF_NAME']]
  cat = cat.fillna('NA')
  assert 0 == cat.isnull().sum().sum(), "contains null value"
  assert kNumUserCouponPurchase == len(cat.index)

  vectorizer = DV()
  vec_cat = vectorizer.fit_transform(cat.T.to_dict().values())

  # test categorical features
  test_cat = test_pairs_coupon_user_df[['CAPSULE_TEXT','GENRE_NAME','large_area_name',
    'ken_name','small_area_name','SEX_ID','PREF_NAME']]
  test_cat = test_cat.fillna('NA')
  assert 0 == test_cat.isnull().sum().sum(), "contains null value"
  assert kNumUserCouponTest == len(test_cat.index)

  test_vec_cat = vectorizer.transform(test_cat.T.to_dict().values())

  # write train
  num_features_offset = kNumUsers + kNumCoupons
  num_num_features = num_array.shape[1]
  cat_features_offset = num_features_offset + num_num_features
  print('num_features_offset = %d' % num_features_offset)
  print('num_num_features = %d' % num_num_features)
  print('cat_features_offset = %d' % cat_features_offset)
  with open(libsvm_train, 'w') as f:
    for i in xrange(kNumUserCouponPurchase):
      # count user_id:1 coupon_dim:1
      purchase_count = pairs_coupon_user_df['purchase_count'][i]
      user_id = pairs_coupon_user_df['user_id'][i]
      coupon_id = pairs_coupon_user_df['coupon_id'][i]
      f.write('%d %d:1 %d:1 ' % (purchase_count, user_id,
        coupon_id + kNumUsers))

      # numerical features
      for p in zip(xrange(num_num_features), num_array[i, :]):
        f.write('%d:%f ' % (p[0] + num_features_offset, p[1]))

      # categorical features
      r = vec_cat[i,:]
      for k, v in zip(r.indices, r.data):
        f.write('%d:%d ' % (k + cat_features_offset, 1))
      f.write('\n')

  print('wrote to %s' % libsvm_train)

  # write test
  with open(libsvm_test, 'w') as f:
    for i in xrange(kNumUserCouponTest):
      # dummy user_id:1 coupon_dim:1
      user_id = test_pairs_coupon_user_df['user_id'][i]
      coupon_id = test_pairs_coupon_user_df['coupon_id'][i]
      f.write('%d %d:1 %d:1 ' % (0, user_id, coupon_id + kNumUsers))

      # numerical features
      for p in zip(xrange(num_num_features), test_num_array[i, :]):
        f.write('%d:%f ' % (p[0] + num_features_offset, p[1]))

      # categorical features
      r = test_vec_cat[i,:]
      for k, v in zip(r.indices, r.data):
        f.write('%d:%d ' % (k + cat_features_offset, 1))
      f.write('\n')

  print('wrote to %s' % libsvm_test)
