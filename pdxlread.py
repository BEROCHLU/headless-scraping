import openpyxl
import pandas as pd

#wb = openpyxl.load_workbook('C:\\Users\\sadaco\\Downloads\\n225bp.xlsx', data_only=True) #T:\\mydocs\\BCPad\\data\\n225bp.xlsx
#ws = wb.active
#ws = wb['data'] # シート変更
#print(ws['C2'].value)
#デーブル範囲解除で読める

df = pd.read_excel('C:\\Users\\sadaco\\Downloads\\n225bp.xlsx', sheet_name='data')
df = df.dropna() #欠損値(NaN)を除外
df = df.loc[:,['date','sp500', 'usd', 'nikke']]
#print(df)
df.to_csv('C:\\Users\\sadaco\\Downloads\\nt1570.csv', header=True, index=False)
