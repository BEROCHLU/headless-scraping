import csv

import openpyxl
import pandas as pd

wb = openpyxl.load_workbook('C:\\Users\\sadaco\\Downloads\\n225bp.xlsx') #T:\\mydocs\\BCPad\\data\\n225bp.xlsx

ws = wb['UPRO'] # シート変更
ws.delete_rows(idx=1, amount=1024) #範囲削除
#ws['A1'] = 'UPRO'

with open('C:\\Users\\sadaco\\Downloads\\UPRO.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        #print(row)
        ws.append(row)

ws = wb['nikkei'] # シート変更
ws.delete_rows(idx=1, amount=1024) #範囲削除

with open('C:\\Users\\sadaco\\Downloads\\t1570.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        ws.append(row)

ws = wb['usd'] # シート変更
ws.delete_rows(idx=1, amount=1024) #範囲削除

with open('C:\\Users\\sadaco\\Downloads\\dollar-yen-exchange-rate-historical-chart.csv') as f:
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        if i < 12120:
            continue
        else:
            ws.append(row)

wb.save('C:\\Users\\sadaco\\Downloads\\n225bp.xlsx')

#df = pd.read_csv('C:\\Users\\sadaco\\Downloads\\UPRO.csv', index_col=0)
#df.to_excel('T:\\mydocs\\BCPad\\data\\n225bp.xlsx',sheet_name='UPRO',startrow=0,startcol = 0)
