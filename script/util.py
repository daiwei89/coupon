import os
from os.path import dirname
from os.path import join
import pandas as pd
import numpy as np

project_dir = dirname(dirname(os.path.realpath(__file__)))
data_dir = join(project_dir, 'data')

user_list_file = join(data_dir, 'user_list.csv')
remapped_user_list_file = join(data_dir, 'remapped_user_list.csv')
user_map_file = join(data_dir, 'user_map.dat')
coupon_map_file = join(data_dir, 'coupon_map.dat')
coupon_list_train_file = join(data_dir, 'coupon_list_train_translated.csv')
coupon_list_test_file = join(data_dir, 'coupon_list_test_translated.csv')
remapped_coupon_list_train_file = join(data_dir, 'remapped_coupon_list_train.csv')
remapped_coupon_list_test_file = join(data_dir, 'remapped_coupon_list_test.csv')

kNumUsers = 22873

kNumCouponsTrain = 19413
kNumCouponsTest = 310
kNumCoupons = kNumCouponsTrain + kNumCouponsTest

# number of user-coupon pairs that resulted in a purchase (training only).
kNumUserCouponPurchase = 158933

kNumUserCouponTest = kNumUsers * kNumCouponsTest

def GetUserMap():
  df = pd.read_csv(user_map_file, sep=' ')
  return dict(zip(df.USER_ID_hash, df.new_id))

def GetUserInverseMap():
  """
  Actually a np.ndarray since user_id is contiguous starting from 0.
  """
  df = pd.read_csv(user_map_file, sep=' ')
  return np.asarray(df.USER_ID_hash.tolist())

def GetCouponMap():
  df = pd.read_csv(coupon_map_file, sep=' ')
  return dict(zip(df.COUPON_ID_hash, df.new_id))

def GetCouponInverseMap():
  """
  Actually a np.ndarray since user_id is contiguous starting from 0.
  """
  df = pd.read_csv(coupon_map_file, sep=' ')
  return np.asarray(df.COUPON_ID_hash.tolist())

def GetUserDf():
  return pd.read_csv(remapped_user_list_file)

def GetCouponTrainDf():
  return pd.read_csv(remapped_coupon_list_train_file)

def GetCouponTestDf():
  return pd.read_csv(remapped_coupon_list_test_file)
