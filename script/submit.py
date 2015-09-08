import os
from os.path import dirname
from os.path import join
import pandas as pd
from util import *
import numpy as np

project_dir = dirname(dirname(os.path.realpath(__file__)))
data_dir = join(project_dir, 'data')
result_dir = join(project_dir, 'result')

result_file = join(result_dir, 'positive_pairs.out')
submit_file = join(result_dir, 'positive_pairs.submit')

if __name__ == '__main__':
  pred = pd.read_csv(result_file, header=-1)
  pred_mat = pred.as_matrix()
  assert pred_mat.shape[0] == kNumUsers * kNumCouponsTest

  pred_mat = pred_mat.reshape((kNumUsers, kNumCouponsTest))
  print(pred_mat.shape)
  descend_idx = np.fliplr(np.argsort(pred_mat, axis=1))

  coupon_imap = GetCouponInverseMap()
  user_imap = GetUserInverseMap()

  with open(submit_file, 'w') as f:
    f.write('USER_ID_hash,PURCHASED_COUPONS\n')
    for i in range(kNumUsers):
      # user hash
      f.write('%s,' % user_imap[i])

      # coupon hash
      top10_id = descend_idx[i,:10]
      for coupon_hash in coupon_imap[top10_id]:
        f.write('%s ' % coupon_hash)
      f.write('\n')
