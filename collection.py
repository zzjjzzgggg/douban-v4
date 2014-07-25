#! /usr/bin/env python
#encoding: utf-8

# book, movie, music
# at most 10 movies can be allocated
class Collection:
	def __init__(self, client):
		self.client=client
	
	def getItems(self, id, cat, start_index=1, max_results=50):
		dat={'cat':cat, 'start-index':start_index, 'max-results':max_results}
		return self.client.get('/people/%d/collection' % id, 'feed', dat)
	
	# status = {watched, wish}
	def getMovies(self, id, status):
		dat={'cat':'movie', 'max-results':50, 'status':status}
		return self.client.get('/people/%d/collection' % id, 'feed', dat)
	
	def getItemsAll(self, id, cat, maxN=500):
		feeds=self.getItems(id, cat)
		if feeds is None: return []
		rst=[item for item in feeds.entries]
		maxN=min(int(feeds.feed.opensearch_totalresults), maxN)
		start=51
		while start<maxN:
			feeds=self.getItems(id, cat, start)
			if feeds is not None: rst.extend([item for item in feeds.entries])
			start+=50
		return rst
	
	def getMoviesAll(self, id):
		rst=[]
		feeds=self.getMovies(id, 'wish')
		if feeds is not None: rst.extend([item for item in feeds.entries])
		feeds=self.getMovies(id, 'watched')
		if feeds is not None: rst.extend([item for item in feeds.entries])
		return rst
		
	
def test():
	from HttpClient import HttpClient
	httpClient=HttpClient()
	from DoubanClient import DoubanClient
	doubanClient=DoubanClient('04949016616456430dbdb043242d02c9', httpClient)
	client=Collection(doubanClient)
	rst=client.getItems(1000001, 'movie')
	print(rst)
	
def test2():
	from httpclient import HttpClient
	httpClient=HttpClient()
	from doubanclient import DoubanClient
	doubanClient=DoubanClient('04949016616456430dbdb043242d02c9', httpClient)
	client=Collection(doubanClient)
	#rst=client.getItemsAll(1000001, 'music')
	rst=client.getMoviesAll(1107186)
	for item in rst: print(item)
	
if __name__=='__main__':
	test2()
