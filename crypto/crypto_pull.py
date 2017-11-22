
# https://min-api.cryptocompare.com/data/histohour?fsym=NEO&tsym=USD&limit=6000&aggregate=1

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime, date, time, timedelta
import sched
import time as mod_time
from pandas.io.json import json_normalize


df = pd.read_excel("crypto_ret_1.xlsx", index_col='time')
tickers = df.columns

fysm = 'BTC'
tsym = 'USD'
d = json.loads(requests.get('https://min-api.cryptocompare.com/data/histohour?fsym=%s&tsym=%s&limit=6000&aggregate=1' % (fysm ,tsym)).text)
json_normalize(d)
df_BTC = pd.DataFrame(d['Data'])
df_BTC.set_index('time', drop=False, inplace=True)
df_BTC['BTC'] = df_BTC['close']
crypto = df_BTC[['BTC', 'time']]

adding = 68
count = 0

for fysm in tickers:
    if fysm == 'BTC':
        adding += 1
        print adding
    else:
        try:
            d = json.loads(requests.get('https://min-api.cryptocompare.com/data/histohour?fsym=%s&tsym=%s&limit=6000&aggregate=1' % (fysm, 'BTC')).text)
            json_normalize(d)
            df = pd.DataFrame(d['Data'])
            df.set_index('time', drop=True, inplace=True)
            crypto[fysm] = df['close']
        except:
            print fysm
            continue

crypto.head()
crypto['time'] =  pd.to_datetime(crypto['time'],unit='s')
crypto.set_index('time', drop=True, inplace=True)
crypto.to_excel('returns_OCT.xlsx')
