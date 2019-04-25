# -*- coding: utf8 -*-

import requests
import json
from bs4 import BeautifulSoup
import types
import sys

def get_html(url,code="utf-8"):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""

def get_main_stocks(NUM,time_stamp):
    URL = r'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020643109325079734_TIME' \
          r'&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)' \
          r'%7D)&cmd=C._A&st=(ChangePercent)&sr=-1&p=1&ps=NUM&_=TIME'
    url = URL.replace('NUM',NUM).replace('TIME',time_stamp)
    
    data = get_html(url)
    start_pos = data.index('"')
    end_pos = data.index(']')
    json_data = data[start_pos:end_pos]
    valid_stocks =[]
    for i in json_data.split('"'):
        if len(i)<10:continue
        valid_stocks.append(i[2:7])
    return valid_stocks


if __name__ == '__main__':
    this_time = '1556115321000'
    last_time = '1553436921000'
    valid_stocks = get_main_stocks(NUM='20',time_stamp= last_time)
    print(valid_stocks)







