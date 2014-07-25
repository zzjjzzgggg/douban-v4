#! /usr/bin/env python
#encoding: utf-8

import urllib.parse
import time

class DoubanClient:

	def __init__(self, api_key, client, delay=2):
		print('Douban client is initialized with key', api_key)
		self.APIKEY=api_key
		self.SERVER='https://api.douban.com'
		self.client=client
		self.delay=delay
	
	def get(self, uri, cat='json', data={}):
		time.sleep(self.delay)
		data['apikey']=self.APIKEY
		parms=urllib.parse.urlencode(data)
		if cat=='json': return self.client.getJson(self.SERVER+uri+'?'+parms)
		else: return self.client.getFeed(self.SERVER+uri+'?'+parms)

if __name__=='__main__':
	from httpclient import *
	hclient=HttpClient()
	client=DoubanClient('04949016616456430dbdb043242d02c9', hclient)
	#print(client.get('/shuo/v2/users/1000001/followers'))
	print(client.get('/people/sakinijino/collection', 'feed', {'cat':'movie'}))
