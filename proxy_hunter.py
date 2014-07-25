#! /usr/bin/env python
#encoding: utf-8

from httpclient import HttpClient
import feedparser
import time
import re
from queue import Queue
import threading

rex_proxy=re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[: ]\d+')
lock=threading.Lock()
class ProxyHunter:
	def __init__(self):
		self.srcrss='http://www.56ads.com/data/rss/2.xml'
		self.client=HttpClient()
		self.queue=Queue(100)
		self.proxies=[]
		for i in range(10): SpeedTester(self.queue, self.proxies).start()
	
	def hunt(self):
		while self.proxies: self.proxies.pop()
		proxies=set()
		xml=self.client.get(self.srcrss, 'gb2312')
		if xml is None: return
		rss=feedparser.parse(xml)
		for entry in rss.entries:
			if time.time()-time.mktime(entry.published_parsed)<3*24*3600: 
				html=self.client.get(entry.link, 'gb2312')
				if html is None: continue
				for rproxy in rex_proxy.findall(html): 
					proxy=rproxy.replace(' ', ':')
					if proxy in proxies: continue
					proxies.add(proxy)
					self.queue.put(proxy)
		print(len(proxies), "parsed.")
		self.queue.join()
		time.sleep(10)
	
	def save(self, fnm='proxies.inf'):
		print("Saving...")
		#with lock: if len(self.proxies)==0: return
		fw=open(fnm, 'w')
		fw.write('[proxies]\n')
		n=1
		with lock:
			for proxy, speed in sorted(self.proxies, key=lambda x: x[1]): 
				fw.write('proxy%d = %s\nspeed%d = %.2f\n' % (n, proxy, n, speed))
				n+=1
		fw.write('\n\n[default]\nproxies = %d\n' % (n-1))
		fw.close()
	
	def run(self):
		while True:
			self.hunt()
			self.save('proxies-%d.ini' % int(time.time()))
			print(time.ctime(), "Done. Sleeping...")
			time.sleep(4*3600)

class SpeedTester(threading.Thread):
	def __init__(self, queue, proxies):
		threading.Thread.__init__(self)
		self.daemon=True
		self.client=HttpClient()
		self.queue=queue
		self.proxies=proxies

	def test_speed(self, proxy):
		self.client.__init__(proxy)
		html=self.client.get('http://www.baidu.com', 'gbk')
		self.client.__init__()
		if html is None: return -1
		else: return self.client.speed
	
	def run(self):
		while True:
			proxy=self.queue.get()
			speed=self.test_speed(proxy)
			if speed>0 and speed<3:
				print(proxy, speed, self.queue.qsize())
				with lock: self.proxies.append((proxy, speed))
			self.queue.task_done()

if __name__=='__main__':
	hunter=ProxyHunter()
	hunter.run()
