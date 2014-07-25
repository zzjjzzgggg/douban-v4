#! /usr/bin/env python
#coding=utf-8

from config import *
from queue import Queue
from workers import *
import dao


def process(tasks, cur):
	print(tasks, cur)
	qsize=conf.getint('default', 'qsize')
	proxies=conf.getint('default', 'proxies')
	uidQueue=Queue(qsize)
	for proxyid in range(1, proxies):
		name='worker_%d' % proxyid
		worker=CTHarvestor(name, proxyid, uidQueue)
		worker.start()
	
	olduids=set()
	while True:
		while not uidQueue.empty(): time.sleep(10)
		uids=dao.getUids(qsize, tasks, cur) - olduids
		print('Fetched ', len(uids))
		if len(uids)==0: break
		for uid in uids: uidQueue.put(uid)
		olduids=uids
		time.sleep(10)

	print('waite to finish....')
	uidQueue.join()
	
if __name__=='__main__':
	print("Usage:\n\tpython3 task_profile.py <tasks> <cur_task>")
	if len(sys.argv)!=3:
		process(0, 0)
	else:
		process(sys.argv[1], sys.argv[2])
