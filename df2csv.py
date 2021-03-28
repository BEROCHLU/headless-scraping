#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

if __name__ == "__main__":
    xlsx_path = "./xlsx/nc225.xlsx"
    path_c = "../sakata/csv/n225in.csv"
    path_p = "../sakata/json/n225in.json"

    df_xl = pd.read_excel(xlsx_path, sheet_name="data")
    df_xl = df_xl.dropna(subset=["upro", "fxy", "t1570"])  # 欠損値(NaN)を除外
    df_xl = df_xl[["date", "upro", "fxy", "t1570"]]  # 指定列だけ抽出

    df_xl.to_csv(path_c, header=False, index=False, line_terminator="\n")  # C lang
    df_xl.to_json(path_p, orient="records", indent=4)  # nodejs python
    print("Done df2csv")
