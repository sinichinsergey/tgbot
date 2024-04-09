import configparser

import psycopg2
from psycopg2.extensions import connection

CONFIG_PATH = "config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)


def get_connection() -> connection:
    try:
        new_connection = psycopg2.connect(
            host=config.get("database", "host"),
            user=config.get("database", "user"),
            password=config.get("database", "password"),
            database=config.get("database", "name"),
            port=config.get("database", "port"))
        print("INFO:     PostgreSQL connection created")
        return new_connection
    except Exception as _ex:
        print(f"INFO:     Error while connecting to PostgreSQL: {_ex}")
