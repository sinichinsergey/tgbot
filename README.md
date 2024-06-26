# Telegram-bot «История продаж»

## Описание
Telegram-bot для управления историей продаж, имеющий HTTP-сервис.

## Решенные задачи
- Создать базу данных на РСУБД PostgreSQL.
- Написать скрипт для автоматического заполнения данных случайными значениями.
- Реализовать CRUD операции:
  - Добавить запись
  - Получить данные за период
- Реализовать telegram-бота, имеющего две кнопки:
  - "Внести данные"
  - "Получить отчет"

## Технологии
- Python 3.10
  - FastAPI
  - SQLAlchemy
  - telebot
- PostgreSQL 16.2

## Инструкция по установке и запуску
1. Создайте виртуальное окружение:
```
python -m venv venv
```
2. Активируйте виртуальное окружение:
- Для Windows:
  ```
  venv\Scripts\activate
  ```
- Для Unix или MacOS:
  ```
  source venv/bin/activate
  ```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. Создайте таблицы в базе данных:
```
psql -U username -d dbname -a -f schema.sql
```
5. Добавьте данные в файл `config.ini` согласно Вашим настройкам базы данных.
6. Заполните базу данных:
```
python seed.py
```
7. Запустите приложение:
```
python main.py
```
8. Откройте в telegram:
https://t.me/sales_infobot
9. Нажмите "START" при первом запуске или напишите любое сообщение при повторном запуске.
10. Чтобы таблица с данными за период отображалась корректно, разверните telegram на полное окно.
