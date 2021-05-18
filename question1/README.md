# data-engineering-1

Covert CSV 2 JSON using Nifi.
## Run
```sh
$ docker-compose up
```


| App | Link |
| ------ | ------ |
| JupyterLab | http://localhost:8880/ |
| Nifi | http://localhost:8050/nifi/ |

| Directory | Path |
| ------ | ------ |
| Input | /home/csv_data |
| Output |  /home/json_data |


## Creating the data: 
I've used Faker To create data and Save it to '/home/csv_data'

![image](https://user-images.githubusercontent.com/47817848/118247662-1a16ab80-b4ac-11eb-99f4-76cc96f5eb3d.png)

## Constracting The Pipeline 

1) Get The CSV File :  first Add Proccessor " GetFile " 
The Input Directory is the shared volume we put the data in : 'home/csv_data' 
also to get any csv file update fileFilter Property with this REGEX : '[^\.].*\.csv'
![image](https://user-images.githubusercontent.com/47817848/118640820-15bafd00-b7e2-11eb-8cdf-eede3529a7c7.png)


2) We Are going to use AvroSchema In Order to apply the schema on CSV file to connvert it to JSOn , So we will add  UpdateAttribute Proccesor to add " schema.name " property: 

![image](https://user-images.githubusercontent.com/47817848/118641399-c75a2e00-b7e2-11eb-8f1a-a17c6731310c.png)

3) Convert To JSON , a ConvertRecored Proccssor will be used , adding a Reader as CSVReader , and Writer As JsonRecordSetWriter


![image](https://user-images.githubusercontent.com/47817848/118641734-30da3c80-b7e3-11eb-909f-14764f4fcc0d.png)

Click On the Arrow To the RIght Of CSV Reader to configer it  , we need to add  AvroSchemaRegistry 
![image](https://user-images.githubusercontent.com/47817848/118641918-67b05280-b7e3-11eb-9598-de76f9ccd94c.png)
add Property, name it same as Your Schema name the value write your Schema 

![image](https://user-images.githubusercontent.com/47817848/118248247-c35da180-b4ac-11eb-8565-ca458e846b90.png)
##### My data schema:
```
{
  "type": "record",
  "name": "UserRecord",
"fields" : [
    {"name": "name", "type": ["null", "string"]},
    {"name": "age", "type": ["null", "string"]},
    {"name": "street", "type": ["null", "string"]},
    {"name": "city", "type": ["null", "string"]},
    {"name": "state", "type": ["null", "string"]},
    {"name": "zip", "type": ["null", "string"]},
    {"name": "lng", "type": ["null", "string"]},
    {"name": "lat", "type": ["null", "string"]}
  ]
}

```
update the CSVReader To Read Using the Schema 
![image](https://user-images.githubusercontent.com/47817848/118642437-0177ff80-b7e4-11eb-9cbd-9690b7d4c3c5.png)
Also the Writer 
![image](https://user-images.githubusercontent.com/47817848/118642493-18b6ed00-b7e4-11eb-874d-9130bb10ca36.png)


4) now we need update the FileName to use json extention , so we will add UpdateAttribute proccessor 
add filename property with value of " ${filename:substringBeforeLast('.')}.json " 
![image](https://user-images.githubusercontent.com/47817848/118642644-469c3180-b7e4-11eb-8f07-87908de3cafa.png)

5) Finaly we need to write the file on file system , so we will use PutFile proccessor for that  and the output directory is /home/json_data/

![image](https://user-images.githubusercontent.com/47817848/118642945-97ac2580-b7e4-11eb-866b-c4075d383012.png)






## Pipeline:
![image](https://user-images.githubusercontent.com/47817848/118247149-83e28580-b4ab-11eb-94ef-5f3c26d99a38.png)



