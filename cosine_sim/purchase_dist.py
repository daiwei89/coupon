from generate_features import *
import matplotlib.pyplot as plt

train_purchase, test_purchase = GetTrainTestPurchase(list())

# The largest # of purchase by a user
max_num_purchase = 0
for val in train_purchase.itervalues():
  if len(val) > max_num_purchase:
    max_num_purchase = len(val)

# purchase_dist[i] is # of users who purchased i items.
purchase_dist = [0] * (max_num_purchase + 1)

num_purchase_total = 0
for val in train_purchase.itervalues():
  purchase_dist[len(val)] += 1
  num_purchase_total += 1

threshold_purchase = 10
num_below_threshold = 0
for i in range(threshold_purchase+1):
  num_below_threshold += purchase_dist[i]
print '%d or fewer: %f' % (threshold_purchase, float(num_below_threshold) /
num_purchase_total)


"""
plt.plot(purchase_dist)
ax = plt.gca()
ax.set_yscale('log')
ax.set_xscale('log')
plt.show()
"""
