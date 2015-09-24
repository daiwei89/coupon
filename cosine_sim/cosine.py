import numpy as np
from generate_features import *
import random
from collections import defaultdict


def GetWeightKaggleDefault():
    # ### modifying weight vector
    # Weight Matrix: GENRE_NAME DISCOUNT_PRICE PRICE_RATE USABLE_DATE_ large_area_name ken_name small_area_name
    genre_weight = 2.05
    original_price_weight = 0
    discount_price_weight = 2
    price_rate_weight = -0.13
    usable_date_weight = 0
    large_area_weight = 0.5
    ken_weight = 1.01
    small_area_weight = 4.75

    weight = [genre_weight] * 13 + [original_price_weight] + [discount_price_weight] + [price_rate_weight] + \
             [usable_date_weight] * 9 + [large_area_weight] * 9 + [ken_weight] * 47 + [   small_area_weight] * 55

    weight_matrix = np.diag(weight)
    return weight_matrix

def GetWeightDML():
    # M^T M = weight_matrix
    M_list = []
    with open('/home/wdai/bosen/app/dml/datasets/coupon/dismat.txt') as f:
      for i, line in enumerate(f.read().splitlines()):
        fields = [float(i) for i in line.split()]
        M_list.append(np.array(fields))
    M = np.matrix(M_list)
    weight_matrix = np.dot(np.transpose(M), M)
    #print weight_matrix
    print np.diag(weight_matrix)
    #np.savetxt('weight.txt', weight_matrix, delimiter=',')
    return weight_matrix

def GetWeightLR():
  num_copurchase = 5
  with open('../trans_data/lr_intercept_weight_%d_copurchase.txt' % num_copurchase) as f:
  #with open('../trans_data/lin_intercept_weight_%d_copurchase.txt' % num_copurchase) as f:
    diag_weight = np.array([float(line) for line in f.read().splitlines()])
  return np.diag(diag_weight)

def run_for_test(test_coupon_list):
    train_purchase, test_purchase = GetTrainTestPurchase(test_coupon_list)

    # ### create user profile
    user_profile = {}
    for user in train_purchase.keys():
        # sum_purchases is sum of purchase item's feature.
        sum_purchases = [float(i) for i in \
            train_item_dict[train_purchase[user][0]]]
        for item in train_purchase[user][1:]:
            item_feature = [float(i) for i in train_item_dict[item]]
            sum_purchases = np.add(sum_purchases, item_feature)
        value = np.divide(sum_purchases, len(train_purchase[user]))
        user_profile[user] = value

    # ### update user's preference for price rate

    discount_rate_idx = item_heading["PRICE_RATE"]
    discount_price_idx = item_heading["DISCOUNT_PRICE"]
    for user in train_purchase.keys():
        # user always prefer higher discount rate
        user_profile[user][discount_rate_idx] = 1
        user_profile[user][discount_price_idx] = 1

    weight_matrix = GetWeightKaggleDefault()
    #weight_matrix = GetWeightDML()
    #weight_matrix = GetWeightLR()

    user_profile_hash = user_profile.keys()
    user_profile_matrix = np.matrix([user_profile[i] for i in user_profile_hash])
    test_coupon_matrix = np.matrix([train_item_dict[i] for i in test_coupon_list])
    test_coupon_matrix = np.transpose(test_coupon_matrix)
    score = np.dot(user_profile_matrix, weight_matrix)
    score = np.dot(score, test_coupon_matrix)
    # n_user doens't include those without a purchase
    n_user, n_coupon = score.shape
    score = np.array(score)

    predictions = {}
    for user in train_purchase.keys():
        user_coupon_matrix = np.matrix([train_item_dict[i] for i in train_purchase[user]])
        user_coupon_matrix[:,discount_rate_idx] = 1
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
    """
    for i in range(n_user):
        user_score = score[i]
        top_k = [test_coupon_list[j] for j in np.argsort(user_score)[-10:][::-1]]
        predictions[user_profile_hash[i]] = top_k
    """

    result = MapEval(predictions, test_purchase)
    print result
    return result

def MapEval(predictions, test_purchase):
    """
    predictions is dict:  user_hash --> [top1_test_coupon_hash, ...]
    test_purchase is dict: user_hash --> [purchased_test_coupon_hash1, ...]
    """
    map_at_ten = 0
    for user, pred in predictions.iteritems():
        if user not in test_purchase:
            continue
        ap = 0
        correct = 0.0
        purchased = test_purchase[user]
        for k in range(10):
            if pred[k] in purchased:
              correct += 1
              ap += correct / (k + 1)
        ap /= 10
        map_at_ten += ap
    map_at_ten /= len(predictions)
    return map_at_ten

# ### print result

# In[ ]:
def print_output(predictions):
    with open("submit.txt", "wb") as fout:
        fout.write('USER_ID_hash, PURCHASED_COUPONS\n')
        for user, coupons in predictions.items():
            fout.write(user + "," + " ".join(coupons) + '\n')


def main():
    f = open("../trans_data/cross_valid_coupon.txt")
    test_lists = []
    for coupons in f.readlines():
        samples = coupons.split(',')
        test_list = samples[:-1]
        test_list.extend(samples[-1].replace('\n',''))
        test_lists.append(test_list[:310])
    valid_loss = []
    for test_list in test_lists:
        valid_loss.append(run_for_test(test_list))
    print 'avg map', reduce(lambda x, y: x + y, valid_loss) / len(valid_loss)

if __name__ == "__main__":
    main()
