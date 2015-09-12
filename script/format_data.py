__author__ = 'yilinhe'
from feature_dictionary import *
from sets import Set
import random
def format_training_data():
    with open("../data/coupon_detail_train.csv") as fin:
        fout = open("formatted_train.txt", "wb")
        for row in fin.readlines()[1:]:
            purchase = row.split(',')
            user_features = user_dict[purchase[4]]
            item_features = item_dict[purchase[5].replace('\n', "")]
            item_count = purchase[0]
            features = [item_count, 0, len(user_features), len(item_features)] + user_features + item_features
            #features = [item_count, 0, 1, len(item_features),user_features[0]] + item_features
            features = [str(i) for i in features]
            fout.write(" ".join(features) + '\n')
        fout.close()


def format_testing_data():
    with open("formatted_test.txt", "wb") as fout:
        for user_features in user_dict.values():
            for item_features in test_item_dict.values():
                features = [0, 0, len(user_features), len(item_features)] + user_features + item_features
                #features = [0, 0, 1, len(item_features),user_features[0]] + item_features
                features = [str(i) for i in features]
                fout.write(" ".join(features) + '\n')
        fout.close()


def format_training_from_visit():
    with open("../data/coupon_visit_train.csv") as fin:
        fout = open("formatted_train.txt", "wb")
        for row in fin.readlines()[1:]:
            purchase = row.split(',')
            user_features = user_dict[purchase[5]]
            coupon_hash = purchase[4].replace('\n', "")
            if coupon_hash not in item_dict:
                continue
            item_features = item_dict[coupon_hash]
            item_count = purchase[0]
            features = [item_count, 0, len(user_features), len(item_features)] + user_features + item_features
            features = [str(i) for i in features]
            fout.write(" ".join(features) + '\n')
        fout.close()

def format_training_from_visit_purchase():
    with open("../data/coupon_visit_train.csv") as fin:
        fout = open("formatted_train.txt", "wb")
        last_user_hash = 0
        items_visited = {}
        item_purchased = Set()
        total = 0
        for row in fin.readlines()[1:]:
            purchase = row.split(',')
            user_hash = purchase[5]
            item_hash = purchase[4].replace('\n', "")
            if item_hash not in item_dict:
                continue
            if user_hash != last_user_hash:
                if total > 0:
                    user_features = user_dict[last_user_hash]

                    for item_hash,times in items_visited.items():
                        item_features = item_dict[item_hash]
                        rating = 1
                        if item_hash in item_purchased:
                            rating = 5
                        elif times > 1:
                            rating = 3
                        features = [rating, 0, len(user_features), len(item_features)] + user_features + item_features
                        #features = [rating, 0, 1, len(item_features),user_features[0]] + item_features
                        features = [str(i) for i in features]
                        fout.write(" ".join(features) + '\n')
                    for item_hash in item_dict:
                        if random.random() > 0.001:
                            continue
                        if item_hash not in items_visited:
                            item_features = item_dict[item_hash]
                            features = [0, 0, len(user_features), len(item_features)] + user_features + item_features
                            features = [str(i) for i in features]
                            fout.write(" ".join(features) + '\n')               

                items_visited = {}
                item_purchased = Set()
                total = 0
                last_user_hash = user_hash

            if item_hash in items_visited:
                items_visited[item_hash] += 1
            else:
                items_visited[item_hash] = 1
            if int(purchase[0]) == 1:
                item_purchased.add(item_hash)
            total += 1
        fout.close()


def format_implicit():
    with open("../data/coupon_visit_train.csv") as fin:
        train_out = open("formatted_implicit_train.txt", "wb")
        test_out = open("formatted_implicit_test.txt", "wb")

        last_user_hash = 0
        train_visited = {}
        test_visited = {}
        total_train = 0
        total_test = 0
        for row in fin.readlines()[1:]:
            purchase = row.split(',')
            user_hash = purchase[5]
            item_hash = purchase[4].replace('\n', "")
            if item_hash not in item_dict:
                continue
            if user_hash != last_user_hash:
                if last_user_hash !=0:
                    user_id = user_dict[last_user_hash][0].split(":")[0]
                    # train
                    features = [len(item_dict), len(train_visited)]
                    features += [str(item) + ":" + str(float(cnt) / total_train) for item, cnt in train_visited.items()]
                    train_out.write(" ".join([str(i) for i in features]) + '\n')

                    # test
                    features = [len(test_visited), len(test_visited)]
                    features += [str(item) + ":" + str(float(cnt) / total_train) for item, cnt in test_visited.items()]
                    test_out.write(" ".join([str(i) for i in features]) + '\n')                    
                
                train_visited = {}
                test_visited = {}
                total_train = 0
                total_test = 0
                last_user_hash = user_hash

            if item_hash in test_item_dict:
                print " test data"
                item_id = test_item_dict[item_hash][0].split(":")[0]
                total_test += 1
                if item_id in test_visited:
                    test_visited[item_id] += 1
                else:
                    test_visited[item_id] = 1
            if item_hash in item_dict:
                item_id = item_dict[item_hash][0].split(":")[0]
                total_train += 1
                if item_id in train_visited:
                    train_visited[item_id] += 1
                else:
                    train_visited[item_id] = 1
        train_out.close()
        test_out.close()


def print_dict():
    f = open("item_features.txt", "wb")
    for key, val in item_feature_dict.items():
        f.write(str(key) + " " + " ".join(val) + "\n")
    f.close()
    f = open("user_features.txt", "wb")
    for key, val in user_dict.items():
        f.write(str(key) + " " + str(val) + "\n")
    f.close()


format_training_from_visit_purchase()
format_testing_data()
format_implicit()
