#! /usr/bin/env python
#encoding: utf-8

class Tag:
	def __init__(self, client):
		self.client=client
	
	def getTags(self, id, cat, start_index=1, max_results=50):
		dat={'cat':cat, 'start-index':start_index, 'max-results':max_results}
		return self.client.get('/people/%d/tags' % id, 'feed', dat)
	
	def getTagsAll(self, id, cat, maxN=500):
		feeds=self.getTags(id, cat)
		if feeds is None: return []
		rst=[{'title':tag.title, 'count':tag.db_count} for tag in feeds.entries]
		maxN=min(int(feeds.feed.opensearch_totalresults), maxN)
		start=51
		while start<maxN:
			feeds=self.getTags(id, cat, start)
			if feeds is not None: rst.extend([{'title':tag.title, 'count':tag.db_count} for tag in feeds.entries])
			start+=50
		return rst

def test():
	from httpclient import HttpClient
	httpClient=HttpClient()
	from doubanclient import DoubanClient
	doubanClient=DoubanClient('04949016616456430dbdb043242d02c9', httpClient)

	client=Tag(doubanClient)
	rst=client.getTags(1000001, 'book')
	print(rst)

def test2():
	from httpclient import HttpClient
	httpClient=HttpClient()
	from doubanclient import DoubanClient
	doubanClient=DoubanClient('04949016616456430dbdb043242d02c9', httpClient)

	client=Tag(doubanClient)
	rst=client.getTagsAll(12829624, 'music')
	print(len(rst))

if __name__=='__main__':
	test2()
