# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 22:53:10 2019

@author: lwm
"""
import pandas as pd
import os


def get_first_up_date(df, BACK_SEARCH_DAYS, BACK_CHECK_DAYS):
    # 首先找到过去N天的最高收盘价所在日期max_date，然后回推5天 得到check_date
    temp = df.close == max(df.close.values[0:BACK_SEARCH_DAYS])
    idx_list = list(temp.index)
    for i in range(len(idx_list)):
        if temp.loc[idx_list[i]] == True:
            max_date = idx_list[i]
            check_date = idx_list[i + BACK_CHECK_DAYS]
            break
    return max_date, check_date


def is_star_(df, thrd=0.5):
    AD = df.high.values[0] - df.low.values[0]
    BC = max(df.close.values[0], df.open.values[0]) - min(df.close.values[0], df.open.values[0])
    if BC / AD <= thrd:
        return True


def is_shaddow_(df, thrd=0.2):
    AD = df.high.values[0] - df.low.values[0]
    AB = df.high.values[0] - max(df.close.values[0], df.open.values[0])
    CD = min(df.close.values[0], df.open.values[0]) - df.low.values[0]
    if AB / AD >= thrd and CD / AD >= thrd:
        return True


def is_drop_(df, thrd=0.02):
    droprate = df.price_change[0] / df.close[1]
    if abs(droprate) <= thrd:
        return True


def is_min_vol_(df):
    bool_min_vol = df.volume.values[0] <= min(df.volume.values[2:BACK_DROP_DAYS + 2])
    # bool_min_vol = df.volume.values[0] <= min(df.volume.values[2:4])
    return bool_min_vol


def is_huge_drop_(df, thrd=0.06):
    max_date, check_date = get_first_up_date(df, BACK_SEARCH_DAYS=4, BACK_CHECK_DAYS=5)
    bool_drop = abs((df.close.values[0] - df.high[max_date]) / df.close.values[0]) >= thrd
    return bool_drop


def is_huge_raise_(df, thrd=0.10):
    max_date, check_date = get_first_up_date(df, BACK_SEARCH_DAYS=4, BACK_CHECK_DAYS=5)
    max_price = df.high[max_date]  # 计算最高收盘价
    min_price = min(df.loc[max_date:check_date, 'close'])  # 计算最低收盘价
    bool_raise = abs(max_price / min_price) - 1 >= thrd
    return bool_raise


def check_this_stock_one_day(df, ignore_star, ignore_shaddow, ignore_drop, Param):
    # 计算是否收十字星
    if not ignore_star:
        if not is_star_(df, thrd=Param['star']):
            return False
    # 计算是否满足上影线规则
    if not ignore_shaddow:
        if not is_shaddow_(df, thrd=Param['shaddow']):
            return False
    # 计算当日涨跌幅是否超过0.02 star_flag=False  第一个星 涨跌3
    if ignore_drop:
        if not is_drop_(df, thrd=0.02):
            return False
    else:
        if not is_drop_(df, thrd=0.02):
            return False
    # 计算当日是否为今日最低成交量日
    if not is_min_vol_(df):
        return False
    # 计算是否近日超跌
    if not is_huge_drop_(df, thrd=Param['huge_drop']):
        return False
        # 计算高位前是否有超级大涨

    if not is_huge_raise_(df,thrd=Param['huge_raise']):
       return False
    return True

def model_1(df):
    A = df.high.values[0] >= max(df.high.values[1:3])
    B = df.low.values[0] <= min(df.low.values[1:3])
    C = df.volume.values[0] >= 2*max(df.volume.values[1:BACK_DROP_DAYS])
    if A and B and C:
        return True

def model_2(df):
    A = df.p_change.values[1] <= -0.05 and df.p_change.values[0] >= 0.05
    B = df.close.values[0] > 0.95*df.open.values[1]
    C = df.open.values[0] < 0.95*df.close.values[1]
        
    AD = df.high.values[0] - df.low.values[0]
    BC = max(df.close.values[0], df.open.values[0]) - min(df.close.values[0], df.open.values[0])
    AD_ = df.high.values[1] - df.low.values[1]
    BC_ = max(df.close.values[1], df.open.values[1]) - min(df.close.values[1], df.open.values[1])
    
    if BC/AD > 0.6 and BC_/AD_ > 0.6 and A and B and C:
        return True


def model_3(df):
    A = abs(df.p_change.values[1]) >= 9.5
    AD = df.high.values[0] - df.low.values[0]
    AB = df.high.values[0] - max(df.close.values[0], df.open.values[0])
    B = AB/AD >= 0.7
    if A and B:
        return True

    
if __name__ == '__main__':
    FILE_DIR = 'D:\LearningProgram\stockInfo\data_0502'
    BACK_DROP_DAYS = 10
    BACK_RAISE_DAYS = 15
    stockInfo = pd.read_csv('stockInfo.csv')
    file_name = '000034.csv'
    good_stock = []
    Param = {'star': 0.2, 'shaddow': 0.1, 'huge_drop': 0.08, 'huge_raise': 0.1}
    this_date = '2019-04-30'
    last_date = '2019-04-29'
    for file_name in os.listdir(FILE_DIR):
        stock = file_name[:-4]
        df = pd.read_csv(os.path.join(FILE_DIR, file_name), index_col='date')
        if this_date not in df.index: continue
        df = df.loc[this_date:]
        name = stockInfo[stockInfo.code == int(stock)].name.values[0]
        # if model_3(df):
        #     print(this_date, 'Find a good stock---', stock, name)
        if check_this_stock_one_day(df, ignore_star=False, ignore_shaddow=False, ignore_drop=True, Param=Param):
            df = df.loc[last_date:]
            print(this_date, 'Find a good stock---', stock, name)
            if check_this_stock_one_day(df, ignore_star=False, ignore_shaddow=False, ignore_drop=True, Param=Param):
                name = stockInfo[stockInfo.code == int(stock)].name.values[0]
                print(this_date, 'Find a good stock---', stock, name)
    print('Running Done!!!')

