#! /usr/bin/env python
#encoding: utf-8


class User:
	def __init__(self, client):
		self.client=client

	def profile(self, id):
		return self.client.get('/v2/user/%d' % id)
	
	def followers(self, id, start=0, count=50):
		data={'page':start//count, 'count':count}
		return self.client.get('/shuo/users/%d/followers' % id, 'json', data)

	def following(self, id, start=0, count=50):
		data={'page':start//count, 'count':count}
		return self.client.get('/shuo/users/%d/following' % id, 'json', data)

def test():
	from httpclient import HttpClient
	httpClient=HttpClient()
	from doubanclient import DoubanClient
	doubanClient=DoubanClient('', httpClient)
	user=User(doubanClient)
	#rst=user.profile(1000001)
	#print(rst)
	rst=user.followers(1000001)
	print(rst)

if __name__=='__main__':
	test()
