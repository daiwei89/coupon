__author__ = 'yilinhe'
from operator import itemgetter
from feature_dictionary import *

def rank_result():
    load_dictionary()
    f = open("pred.txt")
    data = open("formatted_test.txt")
    fout = open("submit.txt","wb")
    fout.write('USER_ID_hash,PURCHASED_COUPONS\n')

    last_id = 0
    p = []
    for pred in f.readlines():
        info = data.readline().split(" ")
       #print info
        user_id = info[4].split(':')[0]
        if last_id != user_id:
            if len(p) > 0:
                top_k = [i[0] for i in sorted(p, key=itemgetter(1), reverse = True)[:10]]
                fout.write(reverse_user_dict[int(last_id)]+","+ " ".join([str(i).replace('\n',"") for i in top_k])+"\n")
            p=[]
            last_id=user_id
        item_hash = reverse_item_dict[int(info[4+int(info[2])].split(':')[0])]
        p.append([item_hash,pred])
    top_k = [i[0] for i in sorted(p, key=itemgetter(1), reverse = True)[:10]]
    fout.write(reverse_user_dict[int(user_id)]+","+ " ".join([str(i).replace('\n',"") for i in top_k])+"\n")
    fout.close()
    f.close()
    data.close()

load_dictionary()
rank_result()
