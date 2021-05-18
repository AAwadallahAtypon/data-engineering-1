# data-engineering-1 , 

#Q2: Provide Similar to Airflow implementation but with csv file is extracted from Postgresql table and the produced JSON file is pushed to MongoDB database. Provide Github repo with all dependencies and detailed README.MD and PPT presentation on how to run your workflow.
## Run


```sh
$ docker-compose up
```


| App | Link | Username | Password | 
| ------ | ------ | ------ | ------ |
| JupyterLab | http://localhost:8886/ | - | pust2021 | 
| AirFlow-webServer | http://localhost:8087/ | airflow | airflow | 
| Mongo-express | http://localhost:8088/ | aawadallah | 1234 |
| pgAdmin| http://localhost:8089/ | aawadallah@psut.com | 1234 |


# Prepare data 
It Was Done using Faker Lib, Convered to Pandas Dataframe Then Push It to Postgres DB. 
----
1- connecting to postgres DB using credentional on Jupypter NoteBook 
![image](https://user-images.githubusercontent.com/47817848/118636718-a80cd200-b7dd-11eb-90be-980c220492c1.png)

2- Creating Data and Save it to CSV File,inside the continer 
![image](https://user-images.githubusercontent.com/47817848/118637014-03d75b00-b7de-11eb-8798-98f7ebb27471.png)

3- Reading the Data as Pandas DataFrame
![image](https://user-images.githubusercontent.com/47817848/118637159-29fcfb00-b7de-11eb-9bc3-d23a00472be4.png)

4- Pushing the data Into the postgres DB & verify by reading it 
![image](https://user-images.githubusercontent.com/47817848/118637448-7c3e1c00-b7de-11eb-8ddc-24cd6f56c008.png)

# Constracting the DAG 
The dag : https://github.com/AAwadallahAtypon/data-engineering-1/blob/main/question2/dags/csv_postgres_2_mongo.py

```
#Importing the requried Libs 
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
from sqlalchemy import create_engine
subprocess.check_call(['pip', 'install', 'pymongo'])
from pymongo import MongoClient
import pandas as pd

```

### Connect To Postgres 

```
host = "postgres_storage"
database = "csv_db"
user = "aawadallah"
password = "1234"
port = '5432'
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

```
### Connect to MongoDB
```
client = MongoClient('mongo:27017',
                     username='aawadallah',
                     password='1234')
mongodb = client['users2021']
collection = mongodb['users']
```

### Connect to MongoDB, create the DB ='users2021' , and Collection = users
```
client = MongoClient('mongo:27017',
                     username='aawadallah',
                     password='1234')
mongodb = client['users2021']
collection = mongodb['users']

```

### install packages into airflow continer 
```
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

```


### Read From Postgres as PandasDF and save it to CSV FIle. 
```
    DF = pd.read_sql("SELECT * FROM users2021;", engine)
    DF.to_csv("/home/sharedVol/data2.csv")
    print(DF.head(5))

```


### Read CSV fetched from Postgress, convert it to dictionary and push it to MongoDB
```
    DF2 = pd.read_csv("/home/sharedVol/data2.csv")
    DF2.reset_index(inplace=True)
    data_dict = DF2.to_dict("records")
    # Insert collection
    collection.insert_many(data_dict)
    
```


### Read the records count from MongoDB
```
   def _read_from_MongoDB():
    print('number of documents in mongoDB = ', collection.estimated_document_count());
```
## Upload the dag file inside the dags directory in airflow continer 

# Final Pipeline   

![image](https://user-images.githubusercontent.com/47817848/118639735-e657c080-b7e0-11eb-824b-208264091876.png)







