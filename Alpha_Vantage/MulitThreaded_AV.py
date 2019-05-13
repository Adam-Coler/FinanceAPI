from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import sys
import pandas as pd
import concurrent.futures
import time

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
	def __init__(self, key_csv_path):
		key_df = pd.read_csv(key_csv_path)
		self.keys = [AV_Key(x) for x in key_df[key_df.columns[0]].values]

	def get_key(self):
		for key in self.keys:
			if key.flag_working:
				return key
		print('Keys all used, Exiting...')
		sys.exit(-1)

	def request(self):
		key = self.get_key().key
		symbols = ['QCOM', "INTC", "PDD", "GE", "APPL", "MSFT"]
		ts = TimeSeries(key=key, output_format='pandas')
		data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
		pprint(data.head(2))
		# pprint(meta_data)


	def get_request(self, symbol):
		key = self.get_key()
		try:
			ts = TimeSeries(key=key.key, output_format='pandas')
			data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
			print('Success! ' + str(symbol))
			return data, meta_data
		except KeyError:
			print('KeyError: ' + key.key + ' During ' + symbol + ' fetch')
			key.flag_working = False
			self.get_request(symbol)
		except:
			print(sys.exc_info())
			return -1


	def make_threaded_request(self, symbols):
		out = []
		CONNECTIONS = len(symbols)
		with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
			future_to_url = (executor.submit(self.get_request, url) for url in symbols)
			count = 0
			for future in concurrent.futures.as_completed(future_to_url):
				try:
					data, meta_data = future.result()
					# data.to_csv(str(count) + '.csv')
					count += 1
				except Exception as exc:
					print(sys.exc_info())

		print('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		for key in self.keys:
			key.toString()

if __name__ == '__main__':
	av = AV_Wrapper('AlphaVantageKeys.csv')
	# av.request()
	av.make_threaded_request(['QCOM', "INTC", "PDD", "GE", "APPL", "MSFT"])
