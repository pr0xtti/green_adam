# 

# Task

https://drive.google.com/drive/folders/1-Xeh7lR6G_zPe-EQaOH0AKtCLNAPjTl8
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
    2. Data Model for Data Marts
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

T4:
- missions
- rockets
- launches

# Solving

## SpaceX. GraphQL API

