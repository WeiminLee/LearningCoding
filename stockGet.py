
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import os
import tushare as ts

def get_html(url,code="gbk"):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""

def get_stock_list(lst,stockURL):
    html=get_html(stockURL,"GB2312")
    soup=BeautifulSoup(html,"html.parser")
    a = soup.find_all('a')
    for i in a:
        try:
            href= i.attrs["href"]
            lst.append(re.findall(r"[s][hz]\d{6}",href)[0])
        except:
            continue

def get_stock_info(lst,stockURL,fpath):
    count = 0
    valid_lst = []
    for stock in lst:
        if stock[2] == '6' or stock[2] == '0':
            valid_lst.append(stock)
    for stock in valid_lst:
        url = stockURL + stock + ".html"
        html = get_html(url)
        try:
            if html == "":
                continue
            infoDict={}
            soup = BeautifulSoup(html,"html.parser")
            stockInfo=soup.find("div",attrs={"class":"stock-bets"})
            name=stockInfo.find_all(attrs={"class":"bets-name"})[0]
            infoDict.update({"股票名称":name.text.split()[0]})
            keyList=stockInfo.find_all("dt")
            valueList=stockInfo.find_all("dd")
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val
            with open(fpath,"a",encoding="utf-8") as f:
                f.write(str(infoDict)+"\n")
                count= count+1
                print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            continue

def add_concept(temp_concept,new_cpt):
    temp_concept = list(temp_concept)
    try:
        temp_concept.remove('0.0')
    except:
        pass
    temp_concept.append(new_cpt)
    return temp_concept

def change_date(src_dir,save_dir,this_date):
    count = 0
    for file_name in os.listdir(src_dir):
        stock = file_name[:-4]
        df = pd.read_csv(os.path.join(src_dir, file_name), index_col='date')
        if this_date in df.index:
            df.to_csv(os.path.join(save_dir, file_name))
            continue
        try:
            this_df = today_df[today_df.code==int(stock)]
            this_df = this_df[~this_df.index.duplicated(keep='first')]
            this_df['close'] = round(df.close[0]*this_df.changepercent/100+df.close[0],2).values[0]
            this_df['p_change'] =  this_df['changepercent']
            cc = pd.DataFrame(columns=df.columns)
        except:
            print('+++++++++++++',stock)
            continue
        
        for col in cc.columns:
            try:
                cc.loc[this_date,col] = this_df.loc[:,col].values[0]
            except:
                cc.loc[this_date,col] = np.nan
        try:
            df = pd.concat([cc, df], sort=True).drop_duplicates(keep='first')
            df = df[~df.index.duplicated(keep='first')]
            df.to_csv(os.path.join(save_dir, file_name),index_name = 'date')
        except:
            pass
        count += 1
        if count % 20 == 0:
            print(stock)


def change_name(src_dir):
    for file_name in os.listdir(src_dir):
        df = pd.read_csv(os.path.join(src_dir, file_name))
        try:
            df = df.rename(columns={'Unnamed: 0':'date'})
        except:
            continue
        df.to_csv(os.path.join(save_dir, file_name),index=False)


if __name__ == '__main__':

    save_dir = 'D:\LearningProgram\stockInfo\data_0422'
    root_dir = 'D:\LearningProgram\stockInfo\data_0419'


    # today_df = pd.read_csv('0419.csv')
    # change_name(save_dir)

    count = 0
    for file_name in os.listdir(save_dir):
        stock = file_name[:-4]
        df = pd.read_csv(os.path.join(save_dir, file_name), index_col='date')
        df = df[~df.index.duplicated(keep='first')]
        df.to_csv(os.path.join(save_dir, file_name))
        #
        # if file_name in os.listdir(save_dir):continue
        # try:
        #     df = pd.read_csv(os.path.join(root_dir,file_name),index_col='date')
        #     #if this_date in df.index:continue
        #     td = ts.get_hist_data(stock, start='2019-04-18')
        #     df = pd.concat([td, df], sort=True).drop_duplicates(keep='first')
        #     df.to_csv(os.path.join(save_dir, file_name))
        # except:
        #     pass
        # count +=1
        # if count%20 == 0:
        #     print(stock)
        #


