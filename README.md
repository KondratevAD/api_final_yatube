# Проект API для Yatube

## Описание
Реализована API для социальной сети Yatube. Возможность создавать посты, группы, комментировать посты, подписываться на участников по средствам API.
Аутентификация пользователей реализована по JWT-токену.

## Техническое описание
* Реализован на базе RestAPI.
* Технология - Django Rest Framework
* Документация по ресурсам на http://127.0.0.1:8000/redoc/

## Стек технологий
Python 3, Django 3.1+, Django REST Framework, Simple-JWT

## Установка
Создайте виртуальное окружение:
```bash
python3 -m venv venv
```
Активируйте его:
```bash
source venv/bin/activate
```
Используйте [pip](https://pip.pypa.io/en/stable/), чтобы установить зависимости:
```bash
pip install -r requirements.txt
```
Не забудьте применить все миграции:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
И запускайте сервер:
```bash
python manage.py runserver
```

## Документация
Чтобы открыть документацию, запустите сервер и перейдите по ссылке:
```http://127.0.0.1:8000/redoc/```
