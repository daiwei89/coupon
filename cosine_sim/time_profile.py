from generate_features import *
from factor_util import *
from datetime import datetime

purchase = GetPurchaseDf()

dates = []
for d in list(purchase['I_DATE']):
  # d looks like: "2012-03-28 15:06:06"
  dates.append(datetime.strptime(d.split()[0], '%Y-%m-%d'))

first_date = min(dates)
last_date = max(dates)

num_dates = (last_date - first_date).days + 1
date_dist = [0] * num_dates
for d in dates:
  nth = (d - first_date).days
  date_dist[nth] += 1


