
# coding: utf-8

# In[14]:

import numpy as np
from generate_features import *
from operator import itemgetter
import random


# ### loading the training data set

# In[15]:


test_coupons = set(random.sample(train_item_dict,len(train_item_dict)/20))
print 'num test coupons:', len(test_coupons)
train_coupons = set(train_item_dict).difference(test_coupons)
print 'num train coupons:', len(train_coupons)

#test_coupons = test_item_dict.keys()
#train_coupons = train_item_dict.keys()


# In[16]:

train_purchase = {}
test = {}
with open("../data/coupon_detail_train.csv") as fin:
    for row in fin.readlines()[1:]:
        purchase = row.split(',')
        user = purchase[4]
        item = purchase[5].replace('\n', "")
        if item not in test_coupons:
            if user not in train_purchase:
                train_purchase[user] = []
            train_purchase[user].append(item)
        else:
            if user not in test:
                test[user] = []
            test[user].append(item)
            
            


# In[17]:

print len(test)


# ### modifying weight vector

# In[18]:

#Weight Matrix: GENRE_NAME DISCOUNT_PRICE PRICE_RATE USABLE_DATE_ large_area_name ken_name small_area_name
genre_weight = 2.05
original_price_weight = 0
discount_price_weight = 2
price_rate_weight = -0.13
usable_date_weight = 0
large_area_weight = 0.5
ken_weight = 1.01
small_area_weight = 4.75

weight = [genre_weight]*13 +     [original_price_weight] +     [discount_price_weight] +     [price_rate_weight] +     [usable_date_weight]*9 +     [large_area_weight]*9 +     [ken_weight]*47 +     [small_area_weight]*55
    
weight_matrix = np.diag(weight)


# In[19]:

weight_matrix


# ### calculate cosine similarity

# In[20]:

test_coupon_list = [i for i in test_coupons]
test_coupon_matrix = np.matrix([test_item_dict[i] if i in test_item_dict else train_item_dict[i] for i in test_coupon_list])
test_coupon_matrix = np.transpose(test_coupon_matrix)


# In[21]:

discount_rate = item_heading["PRICE_RATE"]
discount_price = item_heading["DISCOUNT_PRICE"]
original_price = item_heading["CATALOG_PRICE"]

predictions = {}

for user in train_purchase.keys():
    user_coupon_matrix = np.matrix([train_item_dict[i] for i in train_purchase[user]])
    user_coupon_matrix[:,discount_rate] = 1
    score = np.dot(user_coupon_matrix,weight_matrix)
    score = np.dot(score,test_coupon_matrix)
    #print score
    score.sort(axis=0)
    scale_vector = [pow(0.25,i) for i in range(len(train_purchase[user]))]
    scale_vector.reverse()
    score = np.dot(scale_vector,score).tolist()[0]
    #score = np.array(score.sum(axis=0)+2*score.max(axis=0)).tolist()[0]
    #print len(score)
    top_k = [test_coupon_list[j] for j in np.argsort(score)[-10:][::-1]]
    predictions[user] = top_k
    #print top_k


# ### evaluation

# In[22]:

map_at_ten = 0
for user,pred in predictions.items():
    if user not in test:
        continue
    else:
        ap = 0.0
        correct = 0.0
        purchased = test[user]
        for k in range(10):
            if pred[k] in purchased:
                correct += 1
                ap += correct /(k+1)
        ap/=10
    map_at_ten += ap
map_at_ten/= len(predictions)

print "map@10:",map_at_ten
            
    


# In[23]:

num_purchase = 0
num_predicted = 0
for user, pred in predictions.items():
    if user not in test:
        continue
    else:
        purchased = test[user]
        num_purchase += len(purchased)
        for p in purchased:
            if p in pred:
                num_predicted+=1
print "recall:",float(num_predicted)/num_purchase

"""

# ### add popular coupon for missing users

# In[24]:

for user in user_dict.keys():
    if user not in predictions:
        predictions[user] = ['0fd38be174187a3de72015ce9d5ca3a2','2fcca928b8b3e9ead0f2cecffeea50c1']


# ### print result

# In[25]:

with open("submit.txt","wb") as fout:
    fout.write('USER_ID_hash,PURCHASED_COUPONS\n')
    for user,coupons in predictions.items():
        fout.write(user+","+" ".join(coupons)+'\n')

"""
