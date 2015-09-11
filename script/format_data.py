__author__ = 'yilinhe'

num_user_features = 51
num_item_features = 135
num_user = 22873
num_item = 19413
user_dict = {}
reverse_user_dict = {}
item_dict = {}
test_item_dict = {}
reverse_item_dict = {}
item_feature_dict = {}


def load_dictionary():
    item_cnt = num_item_features
    with open("factor_training_coupon.txt") as f:
        for row in f.readlines()[1:]:
            item_info = row.split("\t")

            features = [str(item_cnt) + ":1"]
            for i in range(len(item_info))[1:]:
                features_id = i - 1
                if float(item_info[i]) != 0:
                    features.append(str(features_id) + ":" + str(item_info[i]))
            item_dict[item_info[0].replace('"', "")] = features
            reverse_item_dict[item_cnt] = item_info[0].replace('"', "")
            item_cnt += 1
    with open("factor_testing_coupon.txt") as f:
        for row in f.readlines()[1:]:
            item_info = row.split("\t")
            features = [str(item_cnt) + ":1"]
            for i in range(len(item_info))[1:]:
                features_id = i - 1
                if float(item_info[i]) != 0:
                    features.append(str(features_id) + ":" + str(item_info[i]))
            test_item_dict[item_info[0].replace('"', "")] = features
            reverse_item_dict[item_cnt] = item_info[0].replace('"', "")
            item_cnt += 1
    user_cnt = num_user_features
    with open("factor_users.txt") as f:
        for row in f.readlines()[1:]:
            user_info = row.split("\t")
            features = [str(user_cnt) + ":1"]
            for i in range(len(user_info))[1:]:
                features_id = i - 1
                if float(user_info[i]) != 0:
                    features.append(str(features_id) + ":" + str(user_info[i]))
            user_dict[user_info[0].replace('"', "")] = features
            reverse_user_dict[user_cnt] = user_info[0].replace('"', "")
            user_cnt += 1


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


def print_dict():
    f = open("item_features.txt", "wb")
    for key, val in item_feature_dict.items():
        f.write(str(key) + "\t" + "\t".join(val) + "\n")
    f.close()
    f = open("user_features.txt", "wb")
    for key, val in user_dict.items():
        f.write(str(key) + "\t" + str(val) + "\n")
    f.close()


load_dictionary()
#format_training_data()
#format_testing_data()