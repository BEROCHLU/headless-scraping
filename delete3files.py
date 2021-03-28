#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# remove download files
if __name__ == "__main__":
    download_folder = "C:\\Users\\sadaco\\Downloads"

    lstFile = [
        "t1570.csv",
        "euro-dollar-exchange-rate-historical-chart.csv",
        "^FTSE.csv",
        "^DJI.csv",
        "pound-japanese-yen-exchange-rate-historical-chart.csv",
    ]
    for csv_file in lstFile:
        csv_path = os.path.join(download_folder, csv_file)

        if os.path.isfile(csv_path):
            os.remove(csv_path)
            print(f"removed {csv_file}")
    print("Done delete files")
