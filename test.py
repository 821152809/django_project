import hashlib
import time
import uuid

import pandas as pd
import requests


df = pd.read_csv("C:\\Users\\Administrator\\Desktop\\1.csv", header=None)
# df.groupby(by=[0, 1])[2].sum()
dict_tmp = {}
for info in df.values:
    if type(info[0]) == float:
        continue
    if type(info[1]) == float:
        continue
    if type(info[2]) == float:
        continue
    key = (info[0], info[1])
    new_sale_amount = info[2]
    sale_amount = dict_tmp.get(key)
    if sale_amount is None:
        dict_tmp[key] = new_sale_amount
    else:
        dict_tmp[key] = sale_amount + new_sale_amount
for key in dict_tmp.keys():
    print(key[0] + "," + key[1] + "," + str(dict_tmp.get(key)))
