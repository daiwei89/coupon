__author__ = 'yilinhe'
from operator import itemgetter

item_dict = {}
user_dict = {}

def load_dict():
    f = open("user_features.txt")
    for row in f.readlines():
        user = row.split("\t")
        user_dict[int(user[1])] = user[0]

def rank_result():
    num_users = len(user_dict)
    f = open("pred.txt")
    item_list = open("factor_testing_coupon.txt")
    item_list.readline()
    item = item_list.readline().split("\t")[1]
    user_counter = 0
    res = []
    row_cnt = 0
    for row in f.readlines():
        row_cnt +=1
        if len(res) <= user_counter:
            res+=[[]]
        res[user_counter].append([item,float(row)])
        user_counter+=1
        if user_counter == num_users:
            user_counter=0
            item = item_list.readline().split("\t")[1]
    print row_cnt
    for user in range(len(user_dict))[:2]:
        top_k = [i[1] for i in sorted(res[user], key=itemgetter(1))[:100]]
        print user_dict[user_counter], " ".join([str(i) for i in top_k])

load_dict()
rank_result()
