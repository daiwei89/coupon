
def EvalMap(predictions, test_purchase):
    """
    predictions is dict:  user_hash --> [top1_test_coupon_hash, ...]
    test_purchase is dict: user_hash --> [purchased_test_coupon_hash1, ...]
    """
    map_at_ten = 0
    num_eval = 0
    for user, pred in predictions.iteritems():
        if user not in test_purchase:
            continue
        num_eval += 1
        ap = 0
        correct = 0.0
        purchased = test_purchase[user]
        for k in range(10):
            if pred[k] in purchased:
              correct += 1
              ap += correct / (k + 1)
        ap /= 10
        map_at_ten += ap
    #map_at_ten /= len(predictions)
    map_at_ten /= num_eval
    print 'eval MAP@10 on %d users' % num_eval
    return map_at_ten

def EvalRecall(predictions, test_purchase):
    """
    predictions is dict:  user_hash --> [top1_test_coupon_hash, ...]
    test_purchase is dict: user_hash --> [purchased_test_coupon_hash1, ...]
    """
    recall_at_ten = 0
    num_eval = 0
    for user, pred in predictions.iteritems():
        if user not in test_purchase:
            continue
        num_eval += 1
        purchased = test_purchase[user]
        num_purchase = len(purchased)
        assert num_purchase > 0
        num_correct = 0.0
        for c in purchased:
            if c in pred:
                num_correct += 1
        recall_at_ten += num_correct / num_purchase
    recall_at_ten /= num_eval
    print 'eval recall@10 on %d users' % num_eval
    return recall_at_ten
