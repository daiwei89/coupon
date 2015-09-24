import numpy as np
from generate_features import *
from sklearn import linear_model
import random
import pandas as pd
from factor_util import *

def LR():
  train_coupon = GetTrainCouponDf()
  train_coupon.drop('COUPON_ID_hash', axis=1, inplace=True)
  train_coupon_np = train_coupon.values
  num_train, feature_dim = train_coupon_np.shape
  print('feature_dim: %d' % feature_dim)

  num_copurchase = 5

  sim_pairs = {}
  with open('../trans_data/sim_pairs_%d_copurchase.txt' % num_copurchase) as f:
    for line in f.read().splitlines():
      pair = [float(i) for i in line.split()]
      sim_pairs[(pair[0], pair[1])] = 1

  dsim_pairs = {}
  with open('../trans_data/dsim_pairs_%d_copurchase.txt' % num_copurchase) as f:
    for line in f.read().splitlines():
      pair = [float(i) for i in line.split()]
      dsim_pairs[(pair[0], pair[1])] = 1

  left_mat = [train_coupon_np[pair[0],:] for pair in sim_pairs.keys()]
  right_mat = [train_coupon_np[pair[1],:] for pair in sim_pairs.keys()]
  X_pos = np.multiply(left_mat, right_mat)
  Xy_pos = np.c_[X_pos, np.ones(X_pos.shape[0])]
  print Xy_pos.shape

  left_mat = [train_coupon_np[pair[0],:] for pair in dsim_pairs.keys()]
  right_mat = [train_coupon_np[pair[1],:] for pair in dsim_pairs.keys()]
  X_neg = np.multiply(left_mat, right_mat)
  Xy_neg = np.c_[X_neg, np.zeros(X_neg.shape[0])]

  Xy = np.r_[Xy_pos, Xy_neg]

  np.random.shuffle(Xy)

  y = Xy[:,feature_dim]
  X = Xy[:,:feature_dim]

  model = linear_model.LogisticRegression(fit_intercept=True)
  #model = linear_model.LinearRegression(fit_intercept=True)
  model.fit(X,y)

  out_file = '../trans_data/lr_intercept_weight_%d_copurchase.txt' % num_copurchase
  with open(out_file, 'w') as f:
    for i in range(feature_dim):
      f.write('%f\n' % model.coef_[0][i])
      #f.write('%f\n' % model.coef_[i])
  print 'wrote to', out_file

LR()
