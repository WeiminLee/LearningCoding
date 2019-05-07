import pandas as pd
import os
import tushare as ts

if __name__ == '__main__':

    root_dir = 'D:\LearningProgram\stockInfo\data_0502'
    save_dir = 'D:\LearningProgram\stockInfo\data_0507'
    #save_dir = r'D:\LearningProgram\stockInfo\data_15_0426'


    count = 0
    for file_name in os.listdir(root_dir):
        stock = file_name[:-4]
        if file_name in os.listdir(save_dir): continue
        try:
            df = pd.read_csv(os.path.join(root_dir, file_name), index_col='date')
            td = ts.get_hist_data(stock, start='2019-04-29')
            #td = ts.get_k_data(stock, ktype='5')
            df = pd.concat([td, df], sort=True).drop_duplicates(keep='first')
            df = df[~df.index.duplicated(keep='first')]
            df.to_csv(os.path.join(save_dir, file_name))

        except:
            pass
        count += 1
        if count % 20 == 0:
            print(stock)
