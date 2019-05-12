#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

# requests：用来抓取网页的html源代码
# socket和http.client 在这里只用于异常处理 
# BeautifulSoup：用来代替正则式取源码中相应标签中的内容

import sys
import io

# 参考https://blog.csdn.net/richard__ting/article/details/81346750
def setup_io():
    sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)
setup_io()

def get_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text

def get_data(html_text):
	final = []
	bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
	body = bs.body # 获取body部分
	data = body.find('div', {'id': '7d'})  # 找到id为7d的div
	ul = data.find('ul')  # 获取ul部分
	li = ul.find_all('li')  # 获取所有的li

	for day in li: # 对每个li标签中的内容进行遍历
	    temp = []
	    date = day.find('h1').string  # 找到日期
	    temp.append(date)  # 添加到temp中
	    inf = day.find_all('p')  # 找到li中的所有p标签
	    temp.append(inf[0].string,)  # 第一个p标签中的内容（天气状况）加到temp中
	    if inf[1].find('span') is None:
	        temperature_highest = None # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
	    else:
	        temperature_highest = inf[1].find('span').string  # 找到最高温
	        temperature_highest = temperature_highest.replace('℃', '')  # 到了晚上网站会变，最高温度后面也有个℃
	    temperature_lowest = inf[1].find('i').string  # 找到最低温
	    temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号
	    temp.append(temperature_highest)   # 将最高温添加到temp中
	    temp.append(temperature_lowest)   #将最低温添加到temp中
	    final.append(temp)   #将temp加到final中

	return final


def write_data(data, file_name):
    with open(file_name, 'w', errors='ignore', newline='',encoding='utf-8-sig')as f:
    	# Edit header
    	fieldnames = ['日期', '天气', '最高温', '最低温']
    	writer = csv.DictWriter(f, fieldnames=fieldnames)
    	writer.writeheader()
    	# Write data
    	f_csv = csv.writer(f)
    	f_csv.writerows(data)

if __name__ == '__main__':
    url ='http://www.weather.com.cn/weather/101230601.shtml'
    html = get_content(url)
    result = get_data(html)
    # print(result)
    write_data(result, 'weather.csv')

