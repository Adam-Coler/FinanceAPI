from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import sys
import pandas as pd
import concurrent.futures
import time
from lxml.html import fromstring
import requests
import random


class AV_Key:
	key = ''
	flag_working = True

	def __init__(self, key):
		self.key = key

	def get_key(self):
		return self.key

	def toString(self):
		print('Key: ', self.key, ' Working: ', self.flag_working)


class AV_Wrapper:
	keys = []
	proxies = []

	def __init__(self, key_csv_path):
		key_df = pd.read_csv(key_csv_path)
		self.keys = [AV_Key(x) for x in key_df[key_df.columns[0]].values]
		self.proxies = self.get_proxies()

	def get_proxies(self):
		url = 'https://free-proxy-list.net/'
		response = requests.get(url)
		parser = fromstring(response.text)
		proxies = []
		for i in parser.xpath('//tbody/tr')[:50]:
			if i.xpath('.//td[7][contains(text(),"yes")]'):
				proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
				proxies.append('http://' + proxy)
		print(str(len(proxies)) + ' Proxies found...')
		return proxies

	def get_proxy(self):
		proxy = {'http': self.proxies[random.randint(0, len(self.proxies))]}
		# print(proxy)
		return proxy

	def get_key(self):
		key_sum = 0
		for key in self.keys:
			if key.flag_working == False:
				key_sum += 1
		if key_sum == len(self.keys) - 1:
			print('Keys all used, Exiting...')
			sys.exit(-1)

		key = self.keys[random.randint(0, len(self.keys) - 1)]
		if not key.flag_working:
			key = self.get_key()
		return key

	def request(self, symbol):
		key = self.get_key()
		proxy = self.get_proxy()
		try:
			ts = TimeSeries(key=key.key, output_format='pandas', proxy=proxy, retries=10)
			data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
			print('Success! ' + str(symbol) + ' Key: ' + key.key + ' Proxy:' + str(proxy))
			data, meta_data = -1, -1
			return data, meta_data
		except KeyError:
			print('KEY ERROR: Key: ' + key.key + ' Tkr: ' + symbol + ' proxy:' + str(proxy))
			key.flag_working = False
			return self.request(symbol)
		except requests.exceptions.ConnectionError:
			print('REQUEST EXCEPTION: Key: ' + key.key + ' Tkr: ' + symbol + ' proxy:' + str(proxy))
			self.proxies.remove(proxy['http'])
			return self.request(symbol)
		except:
			print(sys.exc_info())
			return -1, -1


	def make_threaded_request(self, symbols):
		out = []
		CONNECTIONS = len(symbols)
		with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
			future_to_url = (executor.submit(self.request, symbol) for symbol in symbols)
			for future in concurrent.futures.as_completed(future_to_url):
				try:
					data, meta_data = future.result()
					# data.to_csv(str(count) + '.csv')
				except Exception as exc:
					print('################################################')
					print(sys.exc_info())
					print('################################################')

		print('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		for key in self.keys:
			key.toString()

if __name__ == '__main__':
	av = AV_Wrapper('AlphaVantageKeys.csv')
	# av.request()
	av.make_threaded_request(['QCOM', "INTC", "PDD", "GE", "QCOM", "INTC"])
