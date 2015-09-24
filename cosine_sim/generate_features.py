from collections import defaultdict
num_user_features = 52
num_item_features = 137
num_user = 22873
num_item = 19413
user_dict = {}

# COUPON_ID_hash --> [feature1, feature2,...]
train_item_dict = {}
test_item_dict = {}

train_coupon_hash = []
test_coupon_hash = []

# item_heading['PRICE_RATE'] is the column id for 'PRICE_RATE'
item_heading = {}
user_heading = {}

def load_dictionary_simple():
    with open("../trans_data/factor_training_coupon.txt") as f:
        heading = f.readline().split("\t")
        for i in range(len(heading)):
            item_heading[heading[i].replace('"',"")] = i
        for row in f.read().splitlines():
            item_info = row.split("\t")
            features = [float(i) for i in item_info[1:]]
            coupon_hash = item_info[0].replace('"', "")
            train_item_dict[coupon_hash] = features
            train_coupon_hash.append(coupon_hash)
    with open("../trans_data/factor_testing_coupon.txt") as f:
        for row in f.read().splitlines()[1:]:
            item_info = row.split("\t")
            features = [float(i) for i in item_info[1:]]
            coupon_hash = item_info[0].replace('"', "")
            test_item_dict[coupon_hash] = features
            test_coupon_hash.append(coupon_hash)
    with open("../trans_data/factor_users.txt") as f:
        heading = f.readline().split("\t")
        for i in range(len(heading)):
            user_heading[heading[i]] = i
        for row in f.read().splitlines():
            user_info = row.split("\t")
            features = [float(i.replace('"',"")) for i in user_info[1:]]
            user_dict[user_info[0].replace('"', "")] = features

def GetTrainTestPurchase(test_coupon_list):
    # train: USER_ID_hash --> [purchased_item1, purchased_item2, ...]
    train_purchase = defaultdict(list)
    test_purchase = defaultdict(list)  # similar to test.
    with open("../data/coupon_detail_train.csv") as fin:
        for row in fin.read().splitlines()[1:]:
            purchase = row.split(',')
            #item_count = int(purchase[0])
            user = purchase[4]
            item = purchase[5]
            if item not in test_coupon_list:
                train_purchase[user].append(item)
            else:
                test_purchase[user].append(item)
    return train_purchase, test_purchase

load_dictionary_simple()
