#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


def df2csv():
    xlsx_path = "T:\\mydocs\\BCPad\\data\\nc225.xlsx"

    df = pd.read_excel(xlsx_path, sheet_name="data")
    df = df.dropna(subset=["upro", "fxy", "t1570"])  # 欠損値(NaN)を除外
    df = df.loc[:, ["date", "upro", "fxy", "t1570"]]  # 指定列だけ

    path_n = "T:\\ProgramFilesT\\pleiades\\workspace\\node225\\nt1570.csv"
    path_c = "T:\\ProgramFilesT\\pleiades\\workspace\\nikkei\\Debug\\N225BP.csv"

    df.to_csv(path_n, header=True, index=False)  # nodejs
    df.to_csv(path_c, header=False, index=False, line_terminator="\n")  # C lang
    print("Done df2csv")


if __name__ == "__main__":
    df2csv()
