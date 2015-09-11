__author__ = 'yilinhe'
from feature_dictionary import *


def format_training_data():
    with open("../data/coupon_detail_train.csv") as fin:
        fout = open("formatted_train.txt", "wb")
        for row in fin.readlines()[1:]:
            purchase = row.split(',')
            user_features = user_dict[purchase[4]]
            item_features = item_dict[purchase[5].replace('\n', "")]
            item_count = purchase[0]
            features = [item_count, 0, len(user_features), len(item_features)] + user_features + item_features
            features = [str(i) for i in features]
            fout.write("\t".join(features) + '\n')
        fout.close()


def format_testing_data():
    with open("formatted_test.txt", "wb") as fout:
        for user_features in user_dict.values():
            for item_features in test_item_dict.values():
                features = [0, 0, len(user_features), len(item_features)] + user_features + item_features
                features = [str(i) for i in features]
                fout.write("\t".join(features) + '\n')
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
            fout.write("\t".join(features) + '\n')
        fout.close()


def format_implicit():
    with open("../data/coupon_visit_train.csv") as fin:
        fout = open("formatted_implicit.txt", "wb")
        last_user_hash = 0
        items_visited = {}
        total = 0
        for row in fin.readlines()[1:]:
            purchase = row.split(',')
            user_hash = purchase[5]
            item_hash = purchase[4].replace('\n', "")
            if item_hash not in item_dict:
                continue
            if user_hash != last_user_hash:
                if total > 0:
                    user_id = user_dict[last_user_hash][0].split(":")[0]
                    features = [user_id, len(items_visited)]
                    features += [str(item) + ":" + str(float(cnt) / total) for item, cnt in items_visited.items()]
                    fout.write("\t".join([str(i) for i in features]) + '\n')
                items_visited = {}
                total = 0
                last_user_hash = user_hash

            if item_hash in test_item_dict:
                item_id = test_item_dict[item_hash][0].split(":")[0]
            if item_hash in item_dict:
                item_id = item_dict[item_hash][0].split(":")[0]
            if item_id in items_visited:
                items_visited[item_id] += 1
            else:
                items_visited[item_id] = 1
            total += 1
        fout.close()


def print_dict():
    f = open("item_features.txt", "wb")
    for key, val in item_feature_dict.items():
        f.write(str(key) + "\t" + "\t".join(val) + "\n")
    f.close()
    f = open("user_features.txt", "wb")
    for key, val in user_dict.items():
        f.write(str(key) + "\t" + str(val) + "\n")
    f.close()


#format_training_data()
#format_testing_data()
format_implicit()
