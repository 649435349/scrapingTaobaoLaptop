# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import pymysql
import multiprocessing
import sys
from selenium import webdriver

'''
爬点淘宝台灯的名字，价格，地址，要买台灯了= =
'''
'''
修改日期：
2016.12.24
'''


reload(sys)
sys.setdefaultencoding('utf-8')
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='fyf!!961004', db='mysql',charset='utf8')
cur = conn.cursor()
cur.execute('use scraping')
urls=[]
for i in range(0,4356,44):
    t='https://s.taobao.com/search?q=%E5%8F%B0%E7%81%AF&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20161224&ie=utf8&bcoffset=6&ntoffset=6&p4ppushleft=1%2C48&s='+str(i)
    urls.append(t)

def getItems(url):
    driver = webdriver.PhantomJS(executable_path='/home/fengyufei/下载/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.get(url)
    pageSource = driver.page_source
    bsObj = BeautifulSoup(pageSource)
    t1=bsObj.findAll('a',{'class':'pic-link J_ClickStat J_ItemPicA'})#价格
    t2=bsObj.findAll('img',{'class':'J_ItemPic img'})#名字
    t3=bsObj.findAll('div',{'class':'location'})[1:]#地址，其中第一个是不符合条件的
    t=zip(t2,t1,t3)
    storeMysql(t)
    driver.close()


def storeMysql(t):
    #cur.excute('select * from table')#查询
    #cur.fetchone()#显示
    for i in t:
        #注意下面的双引号，我一般都是用单引号，这里必须用双引号
        cur.execute("insert into taobaoLaptop(name,price,city) VALUES ('"+i[0].attrs['alt']+"','"+i[1].attrs['trace-price']+"','"+i[2].text+"')")
        conn.commit()


def start_process():
    print 'Starting',multiprocessing.current_process().name


if __name__ == '__main__':
     #多进程
     pool_size=multiprocessing.cpu_count()*2
     pool=multiprocessing.Pool(processes=pool_size,initializer=start_process)
     pool_outputs=pool.map(getItems,urls)
     pool.close()
     pool.join()
     cur.close()
     conn.close()
     print 'end'