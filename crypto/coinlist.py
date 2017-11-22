import pandas as pd
import json
from bs4 import BeautifulSoup
import requests


def get_exchanges(data):
    '''
    Takes in a coinsnapshotfullbyid url that we have run a request on and then .json()
    and then returns a list.

    Still need to determine where we need to go from here.
    '''

    markets = data['Data']['Subs']
    exchanges = []
    for item in markets:
        if item.split('~')[1] not in exchanges:
            exchanges.append(item.split('~')[1])
    return exchanges


link = "https://www.cryptocompare.com/api/data/coinlist/"
response = requests.get(link)
soup = BeautifulSoup(response.content, "html.parser")
dic = json.loads(soup.prettify())
all_data = dic['Data']

coin_with_ID = {}
for coin, values in all_data.iteritems():
    coin_with_ID[coin] = values['Id']



coinEX = {}
count = 0
for coin, values in coin_with_ID.iteritems():
    url = 'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={fysm}'.format(fysm=values)
    response = requests.get(url)
    data = response.json()
    coinEX[coin] = get_exchanges(data)
    count += 1
    print count
