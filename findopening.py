#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime


def run():
    dt_now = datetime.datetime.now()  # 今日の日付取得
    dt_now = dt_now.strftime("%Y/%m/%d")

    isAppend = True

    with open("C:\\Users\\sadaco\\Downloads\\t1570.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if dt_now in row: #今日の日付が含まれているか
                isAppend = False

    if isAppend:
        with open("C:\\Users\\sadaco\\Downloads\\t1570.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([dt_now, 21600, 1, 1, 1, 1])


if __name__ == "__main__":
    run()
