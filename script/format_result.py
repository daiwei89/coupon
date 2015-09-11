__author__ = 'yilinhe'
from operator import itemgetter
from format_data import load_dictionary,reverse_user_dict,reverse_item_dict

def rank_result():
    load_dictionary()
    f = open("pred.txt")
    data = open("formatted_test.txt")
    last_id = 0
    p = []
    for pred in f.readlines()[:100]:
        info = data.readline().split("\t")
        user_id = info[4].split(':')[0]
        if last_id != user_id:
            if len(p ) > 0:
                top_k = [i[1] for i in sorted(p, key=itemgetter(1), reverse = True)[:10]]
                print reverse_user_dict[int(user_id)], " ".join([str(i) for i in top_k])
            p=[]
            last_id=user_id

        item_hash = reverse_item_dict[int(info[4+int(info[2])].split(':')[0])]
        p.append([item_hash,pred])

    top_k = [i[0] for i in sorted(p, key=itemgetter(1), reverse = True)[:10]]
    print reverse_user_dict[int(user_id)]+","+ " ".join([str(i).replace('\n',"") for i in top_k])

load_dictionary()
rank_result()
