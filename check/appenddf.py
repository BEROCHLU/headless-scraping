#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import pandas as pd


def run():
    csv_path = "C:\\Users\\sadaco\\Downloads\\96tu.csv"

    url = "https://96ut.com/stock/jikei.php?code=1321"
    dfs = pd.read_html(url, header=0, index_col=0)
    df96tu = dfs[0]
    df96tu = df96tu.sort_values("日付")  # 下が最新になるようにソート
    df96tu.to_csv(csv_path)

    dt_now = datetime.datetime.now()  # 今日の日付取得
    dt_now = dt_now.strftime("%Y/%m/%d")

    df = pd.read_csv(csv_path)
    dfq = df96tu.query(f'日付 == "{dt_now}"')

    if dfq.empty:
        df = df.append({"日付": dt_now, "初値": 9999}, ignore_index=True)

    print(df)


if __name__ == "__main__":
    run()
