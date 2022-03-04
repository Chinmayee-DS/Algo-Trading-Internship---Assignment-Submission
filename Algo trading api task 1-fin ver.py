#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from binance.client import Client


# In[ ]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:


import pandas as pd


# In[ ]:


api_key = "llero1JwWS5HXldpnXdlOnbGAVcXJW6saLPHsoIjocMqyLk7HfSyCa1DAgglFA13"
api_secret = "JhixiXfU5EuA8ojRQwmbOkdoJjTR2909eZaAQWpPI441C08ZBLzgDNRDz8m9VSHp"
# tran_id = 1


# In[ ]:


client = Client(api_key, api_secret, {"verify": False, "timeout": 120}, testnet=True)


# In[ ]:


client.get_account() 


# In[ ]:


def getmindata(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + 'min ago UTC'))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'Open','High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame


# In[ ]:


getmindata('BTCUSDT', '1m', '30')


# In[ ]:


def strat(symbol, qty, entried=False):
    while True:
        global tran_id
        df = getmindata(symbol, '1m', '30')
        cumret = (df.Open.pct_change() +1).cumprod() - 1
        if not entried:
            order = client.create_order(symbol=symbol ,side='BUY', type = 'MARKET', quantity = qty, newClientOrderId = "ALGOINTERN_OID"+str(tran_id))
            print(order)
            entried = True
#             print(1)
        if entried:
            while True:
#                 print(2)
                df = getmindata(symbol, '1m', '0.3')
                sincebuy = df.loc[df.index > pd.to_datetime(order['transactTime'], unit = "ms")]
                if len(sincebuy) > 0:
                    sincebuyret = (sincebuy.Open.pct_change() +1).cumprod() - 1
                    if sincebuyret[-1] < 0.005:
#                         print(3)
                        order = client.create_order(symbol=symbol ,side='SELL', type = 'MARKET', quantity = qty, newClientOrderId = "ALGOINTERN_SL_OID"+str(tran_id))
                        print(order)
                        tran_id = tran_id+1
                        entried = False
                        break
        break
            


# In[ ]:


strat('BTCUSDT', 0.001)


# In[ ]:




