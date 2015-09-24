import os
from os.path import dirname
from os.path import join
import pandas as pd
import numpy as np

#project_dir = dirname(dirname(os.path.realpath(__file__)))
project_dir = '/home/wdai/kaggle/coupon'
data_dir = join(project_dir, 'data')
trans_data_dir = join(project_dir, 'trans_data')
result_dir = join(project_dir, 'result')

kNumUsers = 22873

kNumCouponsTrain = 19413
kNumCouponsTest = 310
kNumCoupons = kNumCouponsTrain + kNumCouponsTest

# number of user-coupon pairs that resulted in a purchase (training only).
kNumUserCouponPurchase = 158933

factor_train_coupon_f = join(trans_data_dir, 'factor_training_coupon.txt')
factor_test_coupon_f = join(trans_data_dir, 'factor_test_coupon.txt')
factor_user_f = join(trans_data_dir, 'factor_users.txt')
valid_coupon_f = join(trans_data_dir, 'cross_valid_coupon_t.csv')
purchase_f = join(data_dir, 'coupon_detail_train.csv')
visit_f = join(data_dir, 'coupon_visit_train.csv')

def GetTrainCouponDf():
  return pd.read_csv(factor_train_coupon_f, sep='\t')

def GetTestCouponDf():
  return pd.read_csv(factor_test_coupon_f, sep='\t')

def GetUserDf():
  return pd.read_csv(factor_user_f, sep='\t')

def GetValidSetDf(i):
  """
  Return a pandas single column df of validation coupon ID hash. 0 <= i < 5.
  """
  df = pd.read_csv(valid_coupon_f)
  column_name = 'VALID_SET%d' % i
  single_valid_df = pd.DataFrame(df.ix[:,i].dropna())
  single_valid_df.rename(columns={column_name: 'COUPON_ID_hash'}, \
      inplace = True)
  return single_valid_df

def GetPurchaseDf():
  return pd.read_csv(purchase_f)

def GetVisitDf():
  return pd.read_csv(visit_f)
