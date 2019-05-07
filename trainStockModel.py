import pandas as pd
import os
import get_concepts as gp
import matplotlib.pyplot as plt




if __name__ == '__main__':
    root_dir = 'D:\LearningProgram\stockInfo\data_0507'
    file_name = '000001.csv'
    df = pd.read_csv(os.path.join(root_dir, file_name), index_col='date')
    stock_concept_df = pd.read_csv('stockConcepts.csv', encoding='gbk')
    time_list = list(df.index)
    total_df = pd.DataFrame()
    for tm in time_list:
        print(tm)
        valid_stocks = []
        for file_name in  os.listdir(root_dir):
            try:
                temp = pd.read_csv(os.path.join(root_dir, file_name), index_col='date')
                if temp.loc[tm, 'price_change'] > 0.9:
                    valid_stocks.append(file_name[:-4])
            except:
                pass
        concept_df = gp.get_common_concepts(stock_concept_df,valid_stocks)
        if total_df.shape[0] == 0:
            total_df = concept_df
        else:
            total_df = pd.merge(total_df,concept_df,how='outer')
    total_df.to_csv('conceptShift.csv')
    total_df.corr('pearson').to_csv('corr.csv')
    #pd.DataFrame(valid_concepts,index=idx).to_csv('conceptShift.csv')


    
    
    


