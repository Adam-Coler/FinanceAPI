from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import sys
import pandas as pd
import concurrent.futures
import time
import requests
from lxml.html import fromstring
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
				#Grabbing IP and corresponding PORT
				proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
				proxies.append('http://' + proxy)
		return proxies

	def get_proxy(self):
		# proxy = {0: self.proxies[random.randint(0, len(self.proxies))]}
		proxy = {'http': random.choice (self.proxies)}
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
		except KeyError:
			print('KEY ERROR: Key: ' + key.key + ' Tkr: ' + symbol + ' proxy:' + str(proxy))
			key.flag_working = False
			self.request(symbol)
		except requests.exceptions.ConnectionError:
			print('REQUEST EXCEPTION: Key: ' + key.key + ' Tkr: ' + symbol + ' proxy:' + str(proxy))
			self.proxies.remove(proxy['http'])
			return self.request(symbol)
		except:
			print(sys.exc_info())

	def make_sequential_request(self, symbols):
		for symbol in symbols:
			self.request(symbol)

if __name__ == '__main__':
	av = AV_Wrapper('AlphaVantageKeys.csv')
	av.make_sequential_request(['QCOM', "INTC", "PDD", "GE", "QCOM", "INTC"])


##############################################################
# ADD TO ALPHA VANTAGE WRAPPER
##############################################################
# headers = {}
# headers['user-agent'] = "HotJava/1.1.2 FCS"
# session = requests.session()
# session.proxies = self.proxy
# session.headers = headers
# print('ATTEMPING TO USE PROXY: ' + str(self.proxy))
# headers = {}
# headers['user-agent'] = "HotJava/1.1.2 FCS"
# response = session.get(url)
# h = session.get("https://httpbin.org/user-agent")
# ip = session.get("http://httpbin.org/ip")
# print('ip: ' + ip.text + ' h: ' + h.text)
##############################################################
