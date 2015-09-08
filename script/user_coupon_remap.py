import os
from os.path import dirname
from os.path import join
import pandas as pd
from util import *

project_dir = dirname(dirname(os.path.realpath(__file__)))
data_dir = join(project_dir, 'data')

raw_user = join(data_dir, 'user_list.csv')
remapped_user_file = join(data_dir, 'remapped_user_list.csv')
user_map = join(data_dir, 'user_map.dat')
raw_coupon = join(data_dir, 'coupon_list_train.csv')
raw_coupon_test = join(data_dir, 'coupon_list_test.csv')
coupon_map = join(data_dir, 'coupon_map.dat')


if __name__ == "__main__":

  """
  users = pd.read_csv(raw_user)
  with open(user_map, 'w') as f:
    f.write('new_id USER_ID_hash\n')
    for id, val in enumerate(users.USER_ID_hash):
      f.write(str(id) + ' ' + val + '\n')

  coupons_test = pd.read_csv(raw_coupon_test)
  coupons_train = pd.read_csv(raw_coupon)
  all_coupon_id = pd.concat([coupons_test.COUPON_ID_hash,
    coupons_train.COUPON_ID_hash])
  with open(coupon_map, 'w') as f:
    f.write('new_id COUPON_ID_hash\n')
    for id, val in enumerate(all_coupon_id):
      f.write(str(id) + ' ' + val + '\n')
  """
  user_map = GetUserMap()
  users = pd.read_csv(raw_user)
  users.replace({'USER_ID_hash': user_map}, inplace = True)
  users.to_csv(remapped_user_file, index = False)
