# scrapingTaobaoLaptop
抓取淘宝台灯的数据，主要是名称，价格，城市。
存入mysql，用了多进程抓取，selenium+phantonJS,bs4,pymysql,requests.
有些东西真的很烦阿，居然要区分引号。
mysql语句不难，写着吧。





create database scraping;
create table taobaoLaptop(
id not null auto_increment,
name varchar(100),
price float,
city varchar(10),
primary key(id))
