#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# remove download files
def delete3files():
    download_folder = "C:\\Users\\sadaco\\Downloads"

    lstFile = ["t1570.csv", "dollar-yen-exchange-rate-historical-chart.csv", "SPY.csv", "^DJI.csv"]
    for csv_file in lstFile:
        csv_path = os.path.join(download_folder, csv_file)

        if os.path.isfile(csv_path):
            os.remove(csv_path)
            print(f"removed {csv_file}")
    print("Done delete3files")


if __name__ == "__main__":
    delete3files()