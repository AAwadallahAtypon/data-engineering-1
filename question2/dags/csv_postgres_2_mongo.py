from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
from sqlalchemy import create_engine
subprocess.check_call(['pip', 'install', 'pymongo'])
from pymongo import MongoClient
import pandas as pd

host = "postgres_storage"
database = "csv_db"
user = "aawadallah"
password = "1234"
port = '5432'
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

client = MongoClient('mongo:27017',
                     username='aawadallah',
                     password='1234')
mongodb = client['users2021']
collection = mongodb['users']


def _read_table_as_DF():
    DF = pd.read_sql("SELECT * FROM users2021;", engine)
    DF.to_csv("/home/sharedVol/data2.csv")
    print(DF.head(5))


def _push_DF_to_Mongo():
    DF2 = pd.read_csv("/home/sharedVol/data2.csv")
    DF2.reset_index(inplace=True)
    data_dict = DF2.to_dict("records")
    # Insert collection
    collection.insert_many(data_dict)


def _read_from_MongoDB():
    print('number of documents in mongoDB = ', collection.estimated_document_count());


def _install_tools():
    try:
        from faker import Faker
    except:
        subprocess.check_call(['pip', 'install', 'faker'])
        from faker import Faker

    try:
        import psycopg2
    except:
        subprocess.check_call(['pip', 'install', 'psycopg2-binary'])
        import psycopg2

    try:
        from sqlalchemy import create_engine
    except:
        subprocess.check_call(['pip', 'install', 'sqlalchemy'])
        from sqlalchemy import create_engine

    try:
        from pymongo import MongoClient
    except:
        subprocess.check_call(['pip', 'install', 'pymongo'])
        from pymongo import MongoClient

    try:
        import pandas as pd
    except:
        subprocess.check_call(['pip', 'install', 'pandas'])
        import pandas as pd


with DAG("etl_postgresql2mongo", start_date=datetime(2021, 1, 1),
         schedule_interval="*/5 * * * *", catchup=False) as dag:
    install_tools = PythonOperator(
        task_id="install_tools",
        python_callable=_install_tools
    )
    read_table_as_DF = PythonOperator(
        task_id="read_table_as_DF",
        python_callable=_read_table_as_DF
    )

    push_DF_to_Mongo = PythonOperator(
        task_id="push_DF_to_Mongo",
        python_callable=_push_DF_to_Mongo
    )

    read_from_MongoDB = PythonOperator(
        task_id="read_from_MongoDB",
        python_callable=_read_from_MongoDB
    )

    install_tools >> read_table_as_DF >> push_DF_to_Mongo >> read_from_MongoDB
