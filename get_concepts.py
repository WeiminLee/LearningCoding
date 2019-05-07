# -*- coding: utf-8 -*-
import pandas as pd
import time
import get_wencai as gw
from collections import Counter

def get_common_concepts(stock_concept_df,valid_stocks):
    all_concepts = []
    for idx, row in stock_concept_df.iterrows():
        stock = ('000000'+str(row['code']))[-6:]
        if stock in valid_stocks:
            all_concepts.append(row['concepts'])
    concepts=  []
    for con in all_concepts:
        concepts.extend(con.split(';'))
    con_dict = Counter(concepts).most_common(30)
    res = {}
    for x in con_dict:
        res[x[0]] = x[1]
    return pd.DataFrame(res,index = [0])
    #return [x[0] for x in con_dict]

def get_num(row):
    n = len(set(row.concepts.split(';'))&set(con_list))
    row['num'] = n
    row = row.drop('concepts')
    return row

if __name__ == '__main__':
    file_root_dir = 'D:\pythonproject\stockProject\stockdata'
    stock_concept_df = pd.read_csv('stockConcepts.csv',encoding='gbk')
    this_time_stamp = str(int(time.time()))
    valid_stocks = gw.get_main_stocks(NUM='120',time_stamp=this_time_stamp)
    con_list = get_common_concepts(stock_concept_df,valid_stocks)
    stock_df = stock_concept_df.copy(deep=True)
    selected_stock = stock_df.apply(get_num,axis=1)
    selected_stock = selected_stock.sort_values(by='num',ascending=False,kind='quicksort')
    selected_stock.head(8)
    #     df = pd.read_csv(os.path.join(file_root_dir, file_name)).iloc[:50]
    #     num = df[abs(df.p_change) >= 0.98].shape[0]
    #     val.append([file_name[:-4],num])

