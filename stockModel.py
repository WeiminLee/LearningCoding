# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 22:53:10 2019

@author: lwm
"""
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import datetime
import numpy as np
import os








def get_first_up_date(df,BACK_SEARCH_DAYS,BACK_CHECK_DAYS):
    #首先找到过去N天的最高收盘价所在日期max_date，然后回推5天 得到check_date
    temp = df.close == max(df.close.values[0:BACK_SEARCH_DAYS])
    idx_list = list(temp.index)
    for i in range(len(idx_list)):
        if temp.loc[idx_list[i]] == True:
            max_date = idx_list[i]
            check_date = idx_list[i+BACK_CHECK_DAYS]
            break
    return max_date,check_date

def is_star_(df,thrd=0.5):
    AD = df.high.values[0]-df.low.values[0]
    BC = max(df.close.values[0],df.open.values[0])-min(df.close.values[0],df.open.values[0])
    if BC/AD <= thrd:
        return True
def is_shaddow_(df,thrd=0.2):
    AD = df.high.values[0]-df.low.values[0]
    AB = df.high.values[0] - max(df.close.values[0],df.open.values[0])
    if AB/AD >= thrd:
        return True
def is_drop_(df,thrd=0.02):
    droprate = df.price_change[0]
    if abs(droprate) <= thrd:
        return True
def is_min_vol_(df):
    bool_min_vol = df.volume.values[0] <= min(df.volume.values[2:BACK_SEARCH_DAYS+2])
    return bool_min_vol
def is_huge_drop_(df,thrd=0.06):
    max_date,check_date = get_first_up_date(df,BACK_SEARCH_DAYS=4,BACK_CHECK_DAYS=5)
    bool_drop = abs((df.close.values[0]-df.high[max_date])/df.close.values[0])>=thrd
    return bool_drop
def is_huge_raise_(df,thrd=0.10):
    max_date,check_date = get_first_up_date(df,BACK_SEARCH_DAYS=4,BACK_CHECK_DAYS=5)
    max_price = df.high[max_date]  #计算最高收盘价
    min_price = min(df.loc[max_date:check_date,'close'])  # 计算最低收盘价
    bool_raise = abs(max_price/min_price)-1>= thrd
    return bool_raise


def check_this_stock_one_day(df,this_date,ignore_star,ignore_shaddow,param):
    #计算是否收十字星
    if not ignore_star:
        if not is_star_(df,thrd=param['star']):
            return False
    #计算是否满足上影线规则
    if not ignore_shaddow:
        if not is_shaddow_(df,thrd=param['shaddow']):
            return False
    #计算当日涨跌幅是否超过0.02 star_flag=False  第一个星 涨跌3
    if not is_drop_(df,thrd=param['drop_2']):
        return False
    #计算当日是否为今日最低成交量日
    if not is_min_vol_(df):
        return False
    #计算是否近日超跌
    if not is_huge_drop_(df,thrd=param['huge_drop']):
        return False
    #计算高位前是否有超级大涨
    if not is_huge_raise_(df,thrd=param['huge_raise']):
        return False
    return True



if __name__ == '__main__':
    FILE_DIR = 'D:\LearningProgram\stockInfo\data3'
    BACK_SEARCH_DAYS = 5
    BACK_CHECK_DAYS = 8
    stockInfo = pd.read_csv('stockInfo.csv')

    good_stock = []
    Param = {'star': 0.15, 'shaddow': 0.2, 'drop_1': 0.02, 'drop_2': 0.03, 'huge_drop': 0.08, 'huge_raise': 0.1}
    this_date = '2019-04-18'
    last_date = '2019-04-17'
    for file_name in os.listdir(FILE_DIR):
        stock = file_name[:-4]
        df = pd.read_csv(os.path.join(FILE_DIR,file_name),index_col='date')
        df = df.loc[this_date:]
        if df.shape[0] <=0: continue
        if check_this_stock_one_day(df,this_date,ignore_star=False,ignore_shaddow=False,param=Param):
# =============================================================================
#             if check_this_stock_one_day(df,last_date,ignore_star=False,ignore_shaddow=True,param=Param):
#                 name = stockInfo[stockInfo.code==int(stock)].name.values[0]
# =============================================================================
            print(this_date,'Find a good stock---',stock,name)
    print('Running Done!!!')
    
    
    
    
    
    
    
    
    
    
