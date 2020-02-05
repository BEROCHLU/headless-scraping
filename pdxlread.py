import sys
import openpyxl
import pandas as pd

book = openpyxl.load_workbook('C:\\Users\\sadaco\\Downloads\\new225bp.xlsx', read_only=True, data_only=True)
check_cell = book['data']['C2'].value
print(check_cell) #読めているかテスト
book.close() # Only affects read_only and write_only
#デーブル範囲解除で読める

if check_cell == None:
    print('cell is empty')
    sys.exit()

df = pd.read_excel('C:\\Users\\sadaco\\Downloads\\new225bp.xlsx', sheet_name='data')
#print(df)
df = df.dropna() #欠損値(NaN)を除外
df = df.loc[:,['date','upro', 'fxy', 't1570']]

df.to_csv('C:\\Users\\sadaco\\Downloads\\nt1570.csv', header=True, index=False)
df.to_csv('C:\\Users\\sadaco\\Downloads\\N225BP.csv', header=False, index=False)
