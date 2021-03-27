#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


if __name__ == "__main__":
    xlsx_path = "./xlsx/nc225.xlsx"

    df = pd.read_excel(xlsx_path, sheet_name="data")
    df = df.dropna(subset=["upro", "fxy", "t1570"])  # 欠損値(NaN)を除外
    df = df.loc[:, ["date", "upro", "fxy", "t1570"]]  # 指定列だけ

    path_c = "../sakata/csv/n225in.csv"
    path_p = "../sakata/json/n225in.json"

    df.to_csv(path_c, header=False, index=False, line_terminator="\n")  # C lang
    df.to_json(path_p, orient="records", indent=4)  # nodejs python
    print("Done df2csv")
