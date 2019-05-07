# -*- coding: utf8 -*-
import requests
import time
import os
import pandas as pd
import get_concepts as gp

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
        valid_stocks.append(i[2:8])
    return valid_stocks

def get_train_stocks(root_dir,this_date):
    train_stocks = []
    for file_name in os.listdir(root_dir):
        df = pd.read_csv(os.path.join(root_dir,file_name),index_col='date')
        df.index = pd.to_datetime(df.index)
        if not this_date in df.index:continue
        last_close = df.iloc[-49].close
        close_ =  df.iloc[-1].close
        if (close_-last_close)/last_close >0.09:
            train_stocks.append(file_name[:-4])
    return train_stocks


def get_not_open_limit_stocks(root_dir,this_date,):
    train_stocks = []
    for file_name in os.listdir(root_dir):
        df = pd.read_csv(os.path.join(root_dir,file_name),index_col='date')
        df.index = pd.to_datetime(df.index)
        if not this_date in df.index:continue
        last_close = df.iloc[-49].close
        close_ = df.iloc[-1].close
        first_close = max(df.iloc[-48:-45].close)
        if (close_-last_close)/last_close >0.09 and (first_close-last_close)/last_close <0.09:
            train_stocks.append(file_name[:-4])
    return train_stocks
   
    
def get_N_limit_stocks(root_dir,this_date,N):
    train_stocks = []
    for file_name in os.listdir(root_dir):
        df = pd.read_csv(os.path.join(root_dir,file_name),index_col='date')
        df.index = pd.to_datetime(df.index)
        if not this_date in df.index:continue
        last_close = df.iloc[-49].close
        first_close = max(df.iloc[-48:N].close)
        if (first_close-last_close)/last_close >0.09:
            train_stocks.append(file_name[:-4])
    return train_stocks

def get_num(row):
    n = len(set(row.concepts.split(';'))&set(common_concpets))
    row['num'] = n
    row = row.drop('concepts')
    return row


def lambda_(row):
    if row.code in valid_stocks:
        row['label'] = 1
    return row

def get_patential_stocks(common_concpets):
    stock_df = stock_concept_df.copy(deep=True)
    selected_stock = stock_df.apply(get_num,axis=1)
    selected_stock = selected_stock.sort_values(by='num',ascending=False,kind='quicksort')
    patential_stocks = [('0000'+str(x))[-6:] for x  in selected_stock.code[:20].values]
    return patential_stocks


def get_open_concept(stock_concept_df,open_limit_stocks):
    open_limit_concepts = gp.get_common_concepts(stock_concept_df,open_limit_stocks)
    return open_limit_concepts
    

if __name__ == '__main__':

    last_time = str(int(time.time()))
    #valid_stocks = get_main_stocks(NUM='30',time_stamp= last_time)
    root_dir = 'D:\LearningProgram\stockInfo\data_5min_0426'
    file_root_dir = 'D:\pythonproject\stockProject\stockdata'
    stock_concept_df = pd.read_csv('stockConcepts.csv',encoding='gbk')
    
    this_date = '2019-04-26'

    final_limit_stocks = get_train_stocks(root_dir,this_date)
    
    open_limit_stocks = get_N_limit_stocks(root_dir,this_date,N=-45)
    
    common_concpets = get_open_concept(stock_concept_df,open_limit_stocks)
    
    patential_stocks = get_patential_stocks(common_concpets)
    
    valid_stocks = list(set(final_limit_stocks) & set(patential_stocks))
    
    src_df = pd.DataFrame({'code':patential_stocks})
    src_df['label'] = 0
    src_df.apply(lambda_,axis=1)
    #src_df.to_csv(os.path.join(save_dir,))
    
    
    
    
    
    
    
    
    
    
    
    
    
    







