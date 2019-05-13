			key = self.keys[0].get_key()
			ts = TimeSeries(key=key, output_format='pandas')
			data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
			pprint(data.head(2))
			pprint(meta_data)
		# concurrent = 200
		self.q = Queue(concurrent * 2)
		for symbol in symbols:
			print('Putting ', symbol, ' in queue...')
			self.q.put(symbol)


		for i in range(concurrent):
			t = Thread(target=self.doWork)
			t.daemon = True
			t.start()

	def doWork(self):
		if True:
			symbol = self.q.get()
			print('Starting executor for ', symbol)
			data, meta_data = self.get_request(symbol)
			# time.sleep(15)
			print('Steping...')
			self.doSomethingWithResult(data, meta_data, symbol)
			# self.q.task_done()
		else:
			print('fales?')


	def get_request(self, symbol):
		key = self.get_key()
		if not key:
			print('Keys all used, Exiting...')
		try:
			print('Fetching ', symbol, ' key:', key.key)
			ts = TimeSeries(key=key.key, output_format='pandas')
			print(ts.get_intraday(symbol=symbol, interval='1min', outputsize='full'))
			data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
			# print(data.head(2))
			data, meta_data = 0, 0
			return data, meta_data
		except KeyError:
			print('KeyError: ' + key.key)
			key.flag_working = False
			self.get_request(symbol)
		except:
			print('ECEPT!')
			print(sys.exc_info())
			return -1
		print('Failed Fetch')

	def doSomethingWithResult(self, data, meta_data, symbol):
		data.to_csv('symbol.csv')