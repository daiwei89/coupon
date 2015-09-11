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


def print_dict():
    f = open("item_features.txt", "wb")
    for key, val in item_feature_dict.items():
        f.write(str(key) + "\t" + "\t".join(val) + "\n")
    f.close()
    f = open("user_features.txt", "wb")
    for key, val in user_dict.items():
        f.write(str(key) + "\t" + str(val) + "\n")
    f.close()


format_training_from_visit()
format_testing_data()