#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os

from openpyxl import load_workbook
from pycel import ExcelCompiler


def openpycel():
    #path = os.path.dirname(__file__) #get current file path
    folder_path = 'T:\\mydocs\\BCPad\\data'
    xlsx_path = os.path.join(folder_path, 'nc225.xlsx')

    book = load_workbook(filename=xlsx_path, data_only=False) #data_only=Trueで数式削除される
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

    MAX_RANGE = len(book['data']['A'])
    #print(MAX_RANGE)

    book.save(xlsx_path)
    book.close() # Only affects read_only and write_only

    excel = ExcelCompiler(filename=xlsx_path)

    lst_upro = []
    lst_fxy = []
    lst_nikke = []
    lst_judge = []

    for i in range(MAX_RANGE):
        cell_C = f'C{i + 2}'
        cell_E = f'E{i + 2}'
        cell_G = f'G{i + 2}'
        cell_J = f'J{i + 2}'

        lst_upro.append(excel.evaluate(cell_C))
        lst_fxy.append(excel.evaluate(cell_E))
        lst_nikke.append(excel.evaluate(cell_G))
        lst_judge.append(excel.evaluate(cell_J))

    book = load_workbook(filename=xlsx_path)
    sheet = book['data'] # シート変更

    for i in range(MAX_RANGE):
        sheet[f'B{i + 2}'] = lst_upro[i]
        sheet[f'D{i + 2}'] = lst_fxy[i]
        sheet[f'F{i + 2}'] = lst_nikke[i]
        sheet[f'I{i + 2}'] = lst_judge[i]
    
    book.save(xlsx_path)
    book.close()

if __name__ == '__main__':
    openpycel()