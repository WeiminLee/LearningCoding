import requests
from bs4 import BeautifulSoup
from urllib import request
import re
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import os
import tushare as ts


def getHtml(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    page1=request.Request(url,headers=headers)
    page=request.urlopen(page1)
    html=page.read()
    return html

def get_html(url, code="utf-8"):

    Cooike = "v=Ai-RGS71rxoKHqsmOMAd2QPjvkI51IP2HSiH6kG8yx6lkEEySaQTRi34F3ZS; PHPSESSID=540ad29cbf7494b133ff854d5778d474; cid=540ad29cbf7494b133ff854d5778d4741555823968; ComputerID=540ad29cbf7494b133ff854d5778d4741555823968"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
               'Cookie': Cooike}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""

if __name__ == '__main__':
    ROOT_DIR = 'D:\LearningProgram\stockInfo\data'
    stocks = pd.read_csv('stockInfo.csv').code.values
    valid_stock = pd.read_csv('stockConcepts.csv',encoding='GBK')
    stockURL = 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w='

    txtName = "URL.txt"
    f = open(txtName, "a+")

    count = 0
    for stock in stocks:
        if stock in valid_stock.code.values:
            continue
            
        if len(str(stock)) < 6:
            stock = ('00000' + str(stock))[-6:]
        else:
            stock = str(stock)
        url = stockURL + stock+'\n'
        f.write(url)
    f.close()









