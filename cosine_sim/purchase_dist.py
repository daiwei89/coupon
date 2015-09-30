from generate_features import *

train_purchase, test_purchase = GetTrainTestPurchase(list())

# The largest # of purchase by a user
max_num_purchase = 0
for val in train_purchase.itervalues():
  if len(val) > max_num_purchase:
    max_num_purchase = len(val)

# purchase_dist[i] is # of users who purchased i items.
purchase_dist = [0] * (max_num_purchase + 1)

for val in train_purchase.itervalues():
  purchase_dist[len(val)] += 1


