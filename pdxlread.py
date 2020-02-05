import sys
import os
import openpyxl
import pandas as pd

if __name__ == '__main__':
    '''
    book = openpyxl.load_workbook('C:\\Users\\sadaco\\Downloads\\new225bp.xlsx', read_only=True, data_only=True)
    check_cell = book['data']['C2'].value
    print(check_cell) #読めているかテスト
    book.close() # Only affects read_only and write_only
    #デーブル範囲解除で読める

    if check_cell == None:
        print('cell is empty')
        sys.exit()
    '''
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
