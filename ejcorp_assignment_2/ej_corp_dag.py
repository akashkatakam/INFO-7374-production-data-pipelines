from __future__ import print_function
import json
import requests
from datetime import datetime

# airflow operators
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


# ml workflow specific
import pandas as pd
from fredapi import Fred
import csv
import s3fs


from fredapi import Fred
import csv
import s3fs
from datetime import datetime


config = {}

config["ingest_data"] = {
    "fred_key": "d956c0978bfabcf773879232e72c9088",
    "s3_out_bucket": "info7374-ejcorp",  # replace
    "s3_out_prefix": "raw/",
}

def fetchData(series, date, isRun, fred):
    if isRun == 0:
        data = fred.get_series_latest_release(series)
        # updateMetaData(series, date, isRun)
        print(series)
        print(data.head(1))
        return data
    else:
        data = fred.get_series(series,observation_start=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))
       # data = fred.get_series_as_of_date(series, date)
        print(data.head())
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
        fs = s3fs.S3FileSystem(anon=False)
        for row in reader:

            fred_data = fetchData(row[0], row[1], int(row[2]), fred)
            new_flag = int(row[2]) + 1
            #            fred_data.to_csv(r"D:\\Data PipeLining\\EJCORP\\"+ row[0] +".csv")
            new_row = [row[0], fred_data.tail(1).index[0], new_flag]
            new_rows_list.append(new_row)
            s3_out_train = "s3://{}/{}/{}/{}".format(
                s3_out_bucket, s3_out_prefix, row[0], row[0] + "_" +str(new_flag) +".csv")
            with fs.open(s3_out_train, "wb") as f:
                fred_data.to_csv(f, sep=str(','), index=False)
            print(s3_out_train)

    file = open('metadata.csv', 'w')
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(new_rows_list)
    file.close()

# define airflow DAG

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id='ejcorp',
    default_args=args,
    schedule_interval=None,
    concurrency=1,
    max_active_runs=1,
    user_defined_filters={'tojson': lambda s: json.JSONEncoder().encode(s)}
)

# set the tasks in the DAG

# dummy operator
init = DummyOperator(
    task_id='start',
    dag=dag
)
# ingest the data

ingest_task = PythonOperator(
    task_id = 'dataingestion',
    dag=dag,
    provide_context=False,
    python_callable= dataIngest,
    op_kwargs=config["ingest_data"]
)
# preprocess the data

cleanup_task = DummyOperator(
    task_id='cleaning_up',
    dag=dag)

# set the dependencies between tasks

init.set_downstream(ingest_task)
ingest_task.set_downstream(cleanup_task)

