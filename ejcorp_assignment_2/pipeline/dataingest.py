# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 03:40:08 2019

@author: PiyushPrashant
"""

import pandas as pd
from fredapi import Fred
import csv


# import s3uploader
def fetchData(series, date, isRun, fred):
    if not isRun:
        data = fred.get_series_latest_release(series)
        # updateMetaData(series, date, isRun)
        return data
    else:
        data = fred.get_series_as_of_date(series, date)
        # updateMetaData(series, date, isRun)
    return data


def dataIngest(fred_key, s3_out_bucket, s3_out_prefix):
    fred = Fred(api_key=fred_key)
    new_rows_list = []
    with open("metadata.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        first_row = ['Series', 'latest_date_fetched', 'IsRun']
        new_rows_list.append(first_row)

        if s3_out_prefix[-1] == "/":
            s3_out_prefix = s3_out_prefix[:-1]
        else:
            s3_out_prefix = s3_out_prefix

        for row in reader:
            fred_data = fetchData(row[0], "", False, fred)
            #            fred_data.to_csv(r"D:\\Data PipeLining\\EJCORP\\"+ row[0] +".csv")
            new_row = [row[0], fred_data.tail(1).index[0], True]
            new_rows_list.append(new_row)
            output_obj_path = row[0] + ".csv"
            s3_out_train = "s3://{}/{}/{}/{}".format(
                s3_out_bucket, s3_out_prefix, row[0], row[0] + ".csv")
            print(s3_out_train)

    file = open('metadata.csv', 'w')
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(new_rows_list)
    file.close()
