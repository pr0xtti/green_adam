# This is a solution for the challenge 

# Task

https://drive.google.com/drive/folders/1-Xeh7lR6G_zPe-EQaOH0AKtCLNAPjTl8

## Task
- https://docs.google.com/document/d/1HSSnsVXZ0pigNSo9aFerq5sFD7BvWsxp/edit
- https://docs.google.com/document/d/10Hc8UN-vwCFa-6gO-8Lra1HUCkA6JteV/edit

## Preface

Нам очень интересно посмотреть на твои скиллы в моделировании данных, Python, 
Docker, и RDBMS. Поэтому мы решили дать тебе типичную DE задачу, но при этом 
очень интересную - поработать над интеграцией на данных Space X 🚀

## Задача:

    1. Service/script
        Написать сервис/скрипт, который загружает данные из GraphQL API 
        (https://studio.apollographql.com/public/SpaceX-pxxbxen/home) в базу 
        данных Postgres.
    2. Data Model with Data Marts
        Спроектировать модель данных с витринами данных. Например тут (https://www.diagrams.net/).
    3. Service/script
        Написать сервис/скрипт, который наполняет спроектированные таблицы.
    4. Create Data Mart
        Создать витрину данных, которая подсчитывает количество публикаций по миссиям,  
        ракетам и пускам (missions, rockets and launches).
    5. Docker 
        Написать Dockerfile и docker-compose.yml, которые позволят нам запустить 
        твой код и делать запросы к БД ( docker compose up -d )
    6. Github
        Залить проект на GitHub и поделиться с нами ссылкой на него (сделать публичным). 
        А также ссылкой на модель данных.

# Data

- missions
- rockets
- launches

# Solution

## Install

Download and start with docker compose:

```shell
clone https://github.com/pr0xtti/greenadam.git && \
cd greenadam && \
docker compose up -d
```
It will start two containers:
```shell
rin@lab-1:~/dev/greenadam/greenadam$ docker ps | egrep '^CONT|greenadam'
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                                         NAMES
a9063a5d0ad7   greenadam-svc   "/usr/bin/supervisord"   3 minutes ago   Up 3 minutes                                                 greenadam-services
039d31e97b4d   postgres         "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes   0.0.0.0:55400->5432/tcp, :::55400->5432/tcp   greenadam-postgres
rin@lab-1:~/dev/greenadam/greenadam$ 
```

View logs in container:

```shell
# Like tail -f
docker logs greenadam-services -f 2>&1

# All with less
docker logs greenadam-services -n all 2>&1 | less
```

# Solving

## Business logic

```python
# Get data from API and save to DB
def get_space_data_save_into_db():
    if not database.exists():
        create_database()
        create_all_tables()
    for entity in entities:
    	entity.get_data_and_save()
        
def get_data_and_save()
	tables = get_tables_order(entity)
    for table in tables:
        if table_empty(table):
            append_or_update(table, data)                    
        else:
            create(table)
            insert(table, data)
    
```

## Structure

```
.
├── collective
│   ├── core
│   │   ├── config.py
│   │   └── tool.py
│   ├── db
│   │   ├── mart
│   │   │   ├── base_class.py
│   │   │   └── database.py
│   │   ├── models
│   │   │   ├── launch.py
│   │   │   ├── mission.py
│   │   │   ├── publication.py
│   │   │   └── rocket.py
│   │   ├── repository
│   │   │   ├── entity_base.py
│   │   │   ├── launch.py
│   │   │   ├── mission.py
│   │   │   ├── publication.py
│   │   │   └── rocket.py
│   │   ├── base_class.py
│   │   ├── database.py
│   │   └── session.py
│   ├── service
│   │   ├── common.py
│   │   └── mart.py
│   ├── sxapi
│   │   ├── base.py
│   │   ├── launch.py
│   │   ├── mission.py
│   │   ├── rocket.py
│   │   └── session.py
│   ├── config.yaml
│   ├── extractor.py
│   ├── logging.yaml
│   ├── martmaker.py
│   └── requirements.txt
├── doc
│   ├── Data_Model.drawio
│   ├── General.drawio
├── docker-compose.yaml
├── Dockerfile
├── extractor.sh
├── martmaker.sh
├── README.md
└── supervisord.conf

```
