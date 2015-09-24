import numpy as np
import pandas as pd
from generate_features import *
import random
from collections import defaultdict
from factor_util import *
import cosine


train_purchase, test_purchase = GetTrainTestPurchase(list())

user_feature_dim = len(user_dict.itervalues().next())
coupon_feature_dim = len(train_item_dict.itervalues().next())

# index layout: user_features, coupon_features, user_id, coupon_id
coupon_feature_offset = user_feature_dim
user_id_offset = coupon_feature_offset + coupon_feature_dim
coupon_id_offset = user_id_offset + kNumUsers

u_df = pd.read_csv('../data/user_list.csv')
num_users = len(u_df.index)
user_hash = dict(zip(list(u_df['USER_ID_hash'].values), range(num_users)))
user_hash_inverse = dict(zip(range(num_users),
  list(u_df['USER_ID_hash'].values)))

c_df = pd.read_csv('../data/coupon_list_train.csv')
num_coupons = len(c_df.index)
coupon_hash = dict(zip(list(c_df['COUPON_ID_hash'].values), range(num_coupons)))
coupon_hash_inverse = dict(zip(range(num_coupons), \
    list(c_df['COUPON_ID_hash'].values)))
num_test = 310

def WriteLibSVMNoUserItemId(f, label, u_id, u_feature, c_id, c_feature):
  f.write('%d ' % label) # label

  # user-features
  for id, val in enumerate(u_feature):
    if not val == 0:
      f.write('%d:%.3f ' % (id, val))

  # coupon-features
  for id, val in enumerate(c_feature):
    if not val == 0:
      f.write('%d:%.3f ' % (id + coupon_feature_offset, val))

  f.write('\n')
  #f.write('%d:1 %d:1\n' % (u_id + user_id_offset, c_id + coupon_id_offset))

def WriteLibSVM(f, label, u_id, u_feature, c_id, c_feature):
  f.write('%d ' % label) # label

  # user-features
  for id, val in enumerate(u_feature):
    if not val == 0:
      f.write('%d:%.3f ' % (id, val))

  # coupon-features
  for id, val in enumerate(c_feature):
    if not val == 0:
      f.write('%d:%.3f ' % (id + coupon_feature_offset, val))

  f.write('%d:1 %d:1\n' % (u_id + user_id_offset, c_id + coupon_id_offset))

def GenerateTestSet(test_id):
  test_samples = range(num_coupons)
  random.shuffle(test_samples)
  test_output = '../trans_data/libfm/test_no_sparse%d.libfm' % test_id
  num_test_pairs = 0
  with open(test_output, 'w') as f:
    for u, u_feature in user_dict.iteritems():
      u_id = user_hash[u]
      for t in test_samples[:num_test]:
        c_hash = coupon_hash_inverse[t]
        c_feature = train_item_dict[c_hash] 
        #WriteLibSVM(f, 0, u_id, u_feature, t, c_feature)
        WriteLibSVMNoUserItemId(f, 0, u_id, u_feature, t, c_feature)
        num_test_pairs += 1
  print 'Wrote', num_test_pairs, 'to', test_output

  with open(test_output + '.coupon_hash', 'w') as f:
    for t in test_samples[:num_test]:
      c_hash = coupon_hash_inverse[t]
      f.write('%s\n' % c_hash)

def Eval(pred_file, test_coupon):
  with open(pred_file) as f:
    pred = np.array([float(r) for r in f.read().splitlines()])
  print pred[:10]
  pred = pred.reshape(kNumUsers, num_test)
  print pred[0,:10]
  top10 = np.argsort(pred, axis=1)[:,::-1][:,:10]
  print top10[0,:10]
  print pred[0, top10[0,:10]]

  #print 'user 0 top coupons', top10[0,:]
  #pred_list = [list(top10[i,:]) for i in range(kNumUsers)]
  predictions = defaultdict(list)
  with open(test_coupon) as f:
    test_coupon_list = f.read().splitlines()
  for i in range(kNumUsers):
    uhash = user_hash_inverse[i]
    for coupon_id in list(top10[i,:]):
      chash = test_coupon_list[coupon_id]
      predictions[uhash].append(chash)
  print 'num test coupons', len(test_coupon_list)
  _, test_purchase = GetTrainTestPurchase(test_coupon_list)
  print '# users with test coupon purchases:', len(test_purchase)
  print test_purchase.itervalues().next()
  prediction_narrow = {}
  for uhash in test_purchase.keys():
    prediction_narrow[uhash] = predictions[uhash]
  print 'sample prediction: ', prediction_narrow.itervalues().next()
  print 'num users in prediction:', len(prediction_narrow)

  print cosine.MapEval(predictions, test_purchase)

if __name__ == "__main__":
  #GenerateTestSet(0)
  #GenerateTestSet(1)
  #Eval('/home/wdai/kaggle/coupon/fm/train_regress.pred', \
  #    '/home/wdai/kaggle/coupon/trans_data/libfm/test0.libfm.coupon_hash')
  #Eval('/home/wdai/kaggle/coupon/fm/train_regress_r64.pred', \
  #    '/home/wdai/kaggle/coupon/trans_data/libfm/test0.libfm.coupon_hash')
  #Eval('/home/wdai/kaggle/coupon/fm/train_regress_test1_r8.pred', \
  #    '/home/wdai/kaggle/coupon/trans_data/libfm/test1.libfm.coupon_hash')
  #Eval('/home/wdai/kaggle/coupon/fm/train_regress_test1_r8_lr.pred', \
  #    '/home/wdai/kaggle/coupon/trans_data/libfm/test1.libfm.coupon_hash')
  #Eval('/home/wdai/kaggle/coupon/fm/train_no_sparse_lr_test0_r8.pred', \
  #    '/home/wdai/kaggle/coupon/trans_data/libfm/test_no_sparse0.libfm.coupon_hash')
  #Eval('/home/wdai/kaggle/coupon/fm/train_lr_test1_r8.pred2', \
  #    '/home/wdai/kaggle/coupon/trans_data/libfm/test1.libfm.coupon_hash')
  #Eval('/home/wdai/kaggle/coupon/fm/train_lr_test1_r8.pred2sgd', \
  #    '/home/wdai/kaggle/coupon/trans_data/libfm/test1.libfm.coupon_hash')
  #Eval('/home/wdai/kaggle/coupon/fm/train_no_sparse_regress_test1_r8.pred', \
  #    '/home/wdai/kaggle/coupon/trans_data/libfm/test_no_sparse1.libfm.coupon_hash')
  #Eval('/home/wdai/kaggle/coupon/fm/train_no_sparse_regress_test0_r8.pred', \
  #    '/home/wdai/kaggle/coupon/trans_data/libfm/test_no_sparse0.libfm.coupon_hash')
  Eval('/home/wdai/kaggle/coupon/fm/train_no_sparse_regress_test1_r0.pred', \
      '/home/wdai/kaggle/coupon/trans_data/libfm/test_no_sparse1.libfm.coupon_hash')
  Eval('/home/wdai/kaggle/coupon/fm/train_no_sparse_regress_test0_r0.pred', \
      '/home/wdai/kaggle/coupon/trans_data/libfm/test_no_sparse0.libfm.coupon_hash')
  """
  num_samples = 0
  train_output = '../trans_data/libfm/train_no_sparse.libfm'
  with open(train_output, 'w') as f:
    for user, coupons in train_purchase.iteritems():
      u_feature = user_dict[user]
      u_id = user_hash[user]
      # positive examples
      for c in coupons:
        c_feature = train_item_dict[c]
        c_id = coupon_hash[c]
        #WriteLibSVM(f, 1, u_id, u_feature, c_id, c_feature)
        WriteLibSVMNoUserItemId(f, 1, u_id, u_feature, c_id, c_feature)
        num_samples += 1

      # generate equal # of neg examples
      samples = range(num_coupons)
      random.shuffle(samples)
      num_neg = 0
      for i in samples:
        c_hash = coupon_hash_inverse[i]
        if not c_hash in coupons:
          c_feature = train_item_dict[c_hash]
          #WriteLibSVM(f, 0, u_id, u_feature, i, c_feature)
          WriteLibSVMNoUserItemId(f, 0, u_id, u_feature, i, c_feature)
          num_neg += 1
          num_samples += 1
          if (num_neg == len(coupons)):
            break
    print 'Generated', num_samples, 'in', train_output
    """
