#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import openpyxl
import pandas as pd

def df2csv():
    df = pd.read_excel('C:\\Users\\sadaco\\Downloads\\new225bp.xlsx', sheet_name='data')
    #print(df)
    df = df.dropna(subset=['judge']) #欠損値(NaN)を除外
    df = df.loc[:,['date','upro', 'fxy', 't1570']]

    path_c = 'T:\\ProgramFilesT\\pleiades\\workspace\\nikkei\\Debug'
    path_n = 'T:\\ProgramFilesT\\pleiades\\workspace\\node225'
    csv_c = os.path.join(path_c, 'N225BP.csv')
    csv_n = os.path.join(path_n, 'nt1570.csv')

    df.to_csv(csv_n, header=True, index=False)
    df.to_csv(csv_c, header=False, index=False)

if __name__ == '__main__':
    df2csv()
