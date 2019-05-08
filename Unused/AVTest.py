# pip install alpha_vantage
# https://www.alphavantage.co/documentation/#

import requests


import time
start_time = time.time()



def get_stock_qoute():
    API_URL = "https://www.alphavantage.co/query"

    data = {
        "function": "GLOBAL_QUOTE",
        "symbol": "MSFT",
        "datatype": "json",  # json, csv
        "apikey": "EJ69MPM068NGTJ30"
    }

    response = requests.get(API_URL, params=data)
    return response.text

import json
quote = json.loads(get_stock_qoute())


print(quote)
print("%s seconds" % (time.time() - start_time))
