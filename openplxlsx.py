import csv
import os

import pandas as pd
from openpyxl import load_workbook

if __name__ == '__main__':
    #path = os.path.dirname(__file__) #get current file path
    path = 'C:\\Users\\sadaco\\Downloads'
    fname = os.path.join(path, 'new225bp.xlsx')

    book = load_workbook(filename=fname, data_only=False) #data_only=Trueで数式削除される
    sheet = book['UPRO'] # シート変更
    sheet.delete_rows(idx=1, amount=1024) #範囲削除

    with open('C:\\Users\\sadaco\\Downloads\\UPRO.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            #print(row)
            sheet.append(row)

    sheet = book['nikkei'] # シート変更
    sheet.delete_rows(idx=1, amount=1024) #範囲削除

    with open('C:\\Users\\sadaco\\Downloads\\t1570.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            sheet.append(row)

    sheet = book['usd'] # シート変更
    sheet.delete_rows(idx=1, amount=1024) #範囲削除

    with open('C:\\Users\\sadaco\\Downloads\\dollar-yen-exchange-rate-historical-chart.csv') as f:
        reader = csv.reader(f)
        for i,row in enumerate(reader):
            if i < 12120:
                continue
            else:
                sheet.append(row)

    book.save('C:\\Users\\sadaco\\Downloads\\new225bp.xlsx')
    book.close() # Only affects read_only and write_only
