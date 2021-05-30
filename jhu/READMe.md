## Run


```sh
$ docker-compose up 
```


| App | Link | Username | Password | 
| ------ | ------ | ------ | ------ |
| JupyterLab | http://localhost:8886/ | - | pust2021 | 
| AirFlow-webServer | http://localhost:8087/ | airflow | airflow | 
| pgAdmin| http://localhost:8089/ | aawadallah@psut.com | 1234 |


## Prepare data 
1- Pulling the CSV files from https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports 


a)  pulling files names
```
    CMD = "curl -s https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports | grep -Eo '[0-9-]*.csv' | sort -Vu"
    output = subprocess.check_output(CMD, shell=True)
    List_of_days = output.decode('utf-8').split('\n')
    List_of_days = [line for line in List_of_days if line.strip() != ""]
```
b) get DF of each day , append it to list  them to list 
```
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
    
    lst_all_DFs=[]
    for Day in List_of_days:
        lst_all_DFs.append(Get_DF_i(Day))
```


# Final Pipeline   

![image](https://user-images.githubusercontent.com/47817848/120105477-c40b5e80-c161-11eb-9178-be976783a186.png)


Results For Germany : 
![image](https://user-images.githubusercontent.com/47817848/120105772-17ca7780-c163-11eb-87cd-403a270964e4.png)


![germany_scoring_report](https://user-images.githubusercontent.com/47817848/120105523-ec935880-c161-11eb-8100-1c6be717a698.png)







