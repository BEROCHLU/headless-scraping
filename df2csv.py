#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import openpyxl
import pandas as pd


def df2csv():
    folder_path = 'T:\\mydocs\\BCPad\\data'
    xlsx_path = os.path.join(folder_path, 'nc225.xlsx')

    df = pd.read_excel(xlsx_path, sheet_name='data')
    #print(df)
    df = df.dropna(subset=['judge']) #欠損値(NaN)を除外
    df = df.loc[:,['date','upro', 'fxy', 't1570']]

    folder_n = 'T:\\ProgramFilesT\\pleiades\\workspace\\node225'
    folder_c = 'T:\\ProgramFilesT\\pleiades\\workspace\\nikkei\\Debug'
    
    path_n = os.path.join(folder_n, 'nt1570.csv')
    path_c = os.path.join(folder_c, 'N225BP.csv')

    df.to_csv(path_n, header=True, index=False) #nodejs
    df.to_csv(path_c, header=False, index=False) #C lang
    print('Done df2csv')

if __name__ == '__main__':
    df2csv()
