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

After deploying the docker compose file, I've created fake Data using Faker 
which has a Jypter Notebook and Nifi 

![image](https://user-images.githubusercontent.com/47817848/118247662-1a16ab80-b4ac-11eb-99f4-76cc96f5eb3d.png)

## data schema:
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

![image](https://user-images.githubusercontent.com/47817848/118248247-c35da180-b4ac-11eb-8565-ca458e846b90.png)

## Pipeline:
![image](https://user-images.githubusercontent.com/47817848/118247149-83e28580-b4ab-11eb-94ef-5f3c26d99a38.png)



