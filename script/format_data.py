__author__ = 'yilinhe'

num_user_features = 0
num_item_features = 135
num_user = 22873
num_item = 19413
user_dict = {}
coupon_dict = {}
item_feature_dict = {}
def format_train():
    f = open("sorted_dense_format.txt")
    fout = open("formatted_train.txt", 'wb')

    user_cnt = num_user_features
    coupon_cnt = num_item_features

    for line in f.readlines():
        purchase = line.split("\t")
        # find user and coupon id
        if purchase[0] not in user_dict:
            user_dict[purchase[0]] = user_cnt
            user_cnt += 1
        if purchase[1] not in coupon_dict:
            coupon_dict[purchase[1]] = coupon_cnt
            coupon_cnt += 1
        user = user_dict[purchase[0]]
        coupon = coupon_dict[purchase[1]]
        # generate feature list for svdfeatures
        features = [purchase[2], 0, 1, 1]
        # user features
        features.append(str(user) + ":1")
        # item features
        features.append(str(coupon) + ":1")
        item_f_cnt = 0
        item_f_start = 3
        for i in range(len(purchase))[item_f_start:]:
            features_id = i - item_f_start
            if float(purchase[i]) != 0:
                features.append(str(features_id) + ":" + str(purchase[i]))
                item_f_cnt += 1
        features[3] = item_f_cnt + 1

        fout.write("\t".join([str(i) for i in features]) + '\n')
        item_feature_dict[coupon]=[purchase[1]]+features[5:]


def format_test():
    f = open("factor_testing_coupon.txt")
    fout = open("formatted_test.txt", 'wb')

    user_cnt = num_user + num_user_features
    coupon_cnt = num_item + num_item_features

    for line in f.readlines()[1:]:
        purchase = line.split("\t")
        if purchase[1] not in coupon_dict:
            coupon_dict[purchase[1]] = coupon_cnt
            coupon_cnt += 1
        coupon = coupon_dict[purchase[1]]
        # generate feature list for svdfeatures
        item_feature = [str(coupon) + ":1"]
        item_f_cnt = 0
        item_f_start = 3
        for i in range(len(purchase))[item_f_start:]:
            features_id = i - item_f_start
            if int(purchase[i]) != 0:
                item_feature.append(str(features_id) + ":" + str(purchase[i]))
                item_f_cnt += 1

        for i in user_dict.values():
            featuers = [0, 0, 1, len(item_feature), str(i) + ":1"] + item_feature
            fout.write("\t".join([str(i) for i in featuers]) + '\n')

def print_dict():
    f = open("item_features.txt","wb")
    for key,val in item_feature_dict.items():
        f.write(str(key)+"\t"+"\t".join(val)+"\n")
    f.close()
    f = open("user_features.txt","wb")
    for key,val in user_dict.items():
        f.write(str(key)+"\t"+str(val)+"\n")
    f.close()

format_train()
print "finished writing training"
format_test()
print_dict()
