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
                    features.append(str(features_id) + ":" + str(item_info[i]).replace('\n',''))
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
                    features.append(str(features_id) + ":" + str(item_info[i]).replace('\n',''))
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
                    features.append(str(features_id) + ":" + str(user_info[i]).replace('\n',''))
            user_dict[user_info[0].replace('"', "")] = features
            reverse_user_dict[user_cnt] = user_info[0].replace('"', "")
            user_cnt += 1
load_dictionary()