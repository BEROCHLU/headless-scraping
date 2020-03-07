#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def delete3files():
    #remove download files
    lstFile = ['t1570.csv', 'dollar-yen-exchange-rate-historical-chart.csv', 'UPRO.csv']
    for csv_file in lstFile:
        csv_path = os.path.join('C:\\Users\\sadaco\\Downloads', csv_file)

        if os.path.isfile(csv_path):
            os.remove(csv_path)
            print(f'removed {csv_file}')
    print('Done delete3files')

if __name__=='__main__':
    delete3files()
