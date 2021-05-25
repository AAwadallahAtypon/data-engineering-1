
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
from sqlalchemy import create_engine
import pandas as pd
import multiprocessing

host = "postgres_storage"
database = "csv_db"
user = "aawadallah"
password = "1234"
port = '5432'


engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

def Get_DF_i(Day):
    DF_i=None
    
    try: 
        URL_Day=f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{Day}'
        DF_day=pd.read_csv(URL_Day)
        DF_day['Day']=Day.split('.')[0]
        cond=(DF_day.Country_Region=='Germany')&(DF_day.Province_State=='Berlin')
        Selec_columns=['Day','Country_Region', 'Last_Update',
          'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active',
          'Combined_Key', 'Incident_Rate', 'Case_Fatality_Ratio']
        DF_i=DF_day[cond][Selec_columns].reset_index(drop=True)
    except:
        pass
    
    return DF_i



def _fetch_data_as_DF(**context):
    # this to grep all the files names  from the repo 
    CMD = "curl -s https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports | grep -Eo '[0-9-]*.csv' | sort -Vu"
    output = subprocess.check_output(CMD, shell=True)
    List_of_days = output.decode('utf-8').split('\n')
    List_of_days = [line for line in List_of_days if line.strip() != ""]
    #Appending all data. 
    # lst_all_DFs= multiprocessing.Pool().map(Get_DF_i, List_of_days)  I've tried to multiprocce the data but seems like it's not allowed in airflow,
    #AssertionError: daemonic processes are not allowed to have children
    
    lst_all_DFs=[]
    for Day in List_of_days:
        lst_all_DFs.append(Get_DF_i(Day))
    
    #ConvertList to DF 
    DF_all = pd.concat(lst_all_DFs).reset_index(drop=True)
    DF_all.to_csv('/home/sharedVol/data.csv')



def _minMax_scale_data(**context):
    DF_Germany=pd.read_csv('/home/sharedVol/data.csv')
    Selec_Columns=['Confirmed','Deaths', 'Recovered', 'Active', 'Incident_Rate','Case_Fatality_Ratio']
    DF_Germany_2 = DF_Germany[Selec_Columns]


    from sklearn.preprocessing import MinMaxScaler

    min_max_scaler = MinMaxScaler()
    DF_Germany_3 = pd.DataFrame(min_max_scaler.fit_transform(DF_Germany_2),columns=Selec_Columns)
    DF_Germany_3.index=DF_Germany_2.index
    DF_Germany_3['Day']=DF_Germany.Day
    DF_Germany_3.to_csv('/home/sharedVol/Scaleddata.csv')

    



def _push_data_to_postgress(**context):
    DF_Germany=pd.read_csv('/home/sharedVol/data.csv')
    DF_Germany_3=pd.read_csv('/home/sharedVol/Scaleddata.csv')
    DF_Germany.to_sql('data_without_scaling', engine,if_exists='replace',index=False)
    DF_Germany_3.to_sql('data_with_scaling', engine,if_exists='replace',index=False)
    


def _install_tools():

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
        import pandas as pd
    except:
        subprocess.check_call(['pip', 'install', 'pandas'])
        import pandas as pd
        
    try:
        import matplotlib 
    except:
        subprocess.check_call(['pip', 'install', 'matplotlib'])
        import matplotlib
        
    try:
        import sklearn 
    except:
        subprocess.check_call(['pip', 'install', 'sklearn'])
        import sklearn        



with DAG("ETL_JHC", start_date=datetime(2021, 1, 1),
         schedule_interval="0 1 * * *", catchup=False) as dag: #to run it everyday at 1 PM
    install_tools = PythonOperator(
        task_id="install_tools",
        python_callable=_install_tools,
        provide_context=True
    )
    
    fetchData = PythonOperator(
        task_id="fetch_data_and_save_it",
        python_callable=_fetch_data_as_DF,
        provide_context=True
    )

    minMaxScaleData = PythonOperator(
        task_id="minMax_Scale_data",
        python_callable=_minMax_scale_data,
        provide_context=True
    )

    pushDataToPG = PythonOperator(
        task_id="push_data_to_postgress",
        python_callable=_push_data_to_postgress,
        provide_context=True
    )

    install_tools >> fetchData >> minMaxScaleData >> pushDataToPG
