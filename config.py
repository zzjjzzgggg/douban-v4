#! /usr/bin/env python
#encoding: utf-8

import time, os, sys
from configparser import ConfigParser

conf=ConfigParser()
conf.read('conf.ini')

def getProxy(pid):
	if pid==0: return None
	fnms=[]
	for fnm in os.listdir('.'):
		if fnm.find('proxies-')!=-1: fnms.append(fnm)
	fnms.sort()
	if len(fnms)==0: return None
	pconf=ConfigParser()
	pconf.read(fnms[-1])
	if pid>pconf.getint('default', 'proxies'): return None
	return pconf.get('proxies', 'proxy'+str(pid))

if __name__=='__main__':
	print(getProxy(67))
