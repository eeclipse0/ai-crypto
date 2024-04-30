import time
import requests
import pandas as pd
import datetime
import os.path

timestamp = last_update_time =  datetime.datetime.now()
while(1):
    timestamp = datetime.datetime.now()
    if ((timestamp-last_update_time).total_seconds() < 5.0):
        continue
    last_update_time = timestamp
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    req_date = req_timestamp.split(' ')[0]


    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/ETH_KRW/?count=5')
    book = response.json()


    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0
    
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1 
    

    df = pd.concat([bids, asks])  #######pandas2.0
    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp
    
    if(not os.path.isfile("book-%s-bithumb-eth.csv"%(req_date))):
        df.to_csv("book-%s-bithumb-eth.csv"%(req_date), index=False, mode = 'a', sep='|')
    df.to_csv("book-%s-bithumb-eth.csv"%(req_date), index=False, header=False, mode = 'a', sep='|')
    
    
    continue

    