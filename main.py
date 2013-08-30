#!/usr/bin/env python
#coding=utf-8

import requests,re , codecs , logging , urllib , sys , time , platform , os
from BeautifulSoup import BeautifulSoup

PATH=os.path.split(sys.argv[0])[0]
URL='http://list.tmall.com//search_product.htm'
CONF_FILE=os.path.join(PATH,'config.txt') #至少包含两个参数 max和keyword
RECORD_FILE=os.path.join(PATH,'record'+time.strftime('%m%d%H%m%S',time.localtime())+'.txt')
PATTERN=r'(\w+):(\S+)' #***
MAX_ERROR='配置文件错误：max参数值应为正整数'
SYS_NEWLINE=''
SYS_LEADING=''

class Crawler():

		def log_init(self):
				logger=logging.getLogger()
				logger.setLevel(logging.DEBUG)
				logger.addHandler(logging.StreamHandler())
				return logger


		def getConfig(self):
				config=open(CONF_FILE,'rb').read()
				cfg={}
				for m in re.finditer(PATTERN,config):
						cfg[m.group(1)]=m.group(2)
				#判断max参数合法与否
				if not cfg.get('max'):
						cfg['max']=100000000
				else:
					try:
							max=int(cfg['max'])
					except :
							print MAX_ERROR
							sys.exit(-1)
					if max<0:
							print MAX_ERROR
							sys.exit(-1)
				return cfg

				
		def getNextSoup(self):
				params={'url':URL,
						's':self.num,
					    'q':urllib.quote(self.cfg['keyword'].decode('utf-8').encode('gbk'))} #查询条件如果是汉字的话，需要转化成gbk编码，因为索索条件使用的是gb系列的汉字
				#print params
				#r=requests.get(URL,params=params) #汉字用这种方式有问题
				r=requests.get("%(url)s?s=%(s)s&q=%(q)s"%params)
				#print r.url
				return BeautifulSoup(r.text)

		
		def procSoup(self,soup,record):
				#判断是否到达了最后一页
				tag=soup.find('b','ui-page-cur')
				if not tag:
						self.end=True #搜不到任何宝贝的情况
						return
				cur_page=tag.string
				total_page=re.findall(ur'共(.*?)页',unicode(soup))[0]
				if total_page==cur_page:
						self.end=True #最后一页
				for divtag in soup.findAll('div','product'):
						self.num=self.num+1
						if self.num>int(self.cfg['max']):  
								self.end=True #达到个数上限
								return
						price=re.findall(r'\d[.\d]*',divtag.div.find('p','productPrice').em.string)[0]
						title=divtag.div.find('p','productTitle').a['title']
						shop=divtag.div.find('div','productShop').find('span','ww-light ww-small')['data-nick']
						# windows和linux下换行符不一样
						record.write(u'%s---￥%s---%s%s'%(title,price,shop,SYS_NEWLINE))
						

		def crawl(self):
				self.logger=self.log_init()
				self.logger.info('start....')
				self.cfg=self.getConfig()
				self.num=0 
				self.end=False
				# 为了保证windows下一些识别能力不强的软件（如写字板）可以正常查看结果文件，windows下需要在utf-8文件前面加上前导的BOM(0xefbbbf)
				record=open(RECORD_FILE,'wb')
				record.write(SYS_LEADING)
				record.close()

				record=codecs.open(RECORD_FILE,'a',encoding='utf-8')
				while not self.end:
						soup=self.getNextSoup()
						self.procSoup(soup,record)

				record.close()
				self.logger.info('end....')


if __name__=='__main__':
	# 兼容性问题
	if platform.system()=="Windows": 
		SYS_NEWLINE="\r\n"
		SYS_LEADING="\xef\xbb\xbf"
	elif platform.system()=='Linux':
		SYS_NEWLINE="\n"
	else:   # mac
		SYS_NEWLINE="\r"
	craw=Crawler()
	craw.crawl()
