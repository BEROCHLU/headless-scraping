#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__=='__main__':

    url = "https://www.ishares.com/us/products/239710/ishares-russell-2000-etf"
    html = urlopen(url)
    doc = BeautifulSoup(html, 'html.parser')
    lst_elem = doc.select('#topHoldingsTable')
    print(lst_elem)

    current_dir = os.path.dirname(os.path.abspath(__file__))


