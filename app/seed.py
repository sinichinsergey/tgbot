import random

from faker import Faker
import faker_commerce

import seed_database

DATA_SIZE = 50


def gen_data() -> list[tuple]:
    """ sale_date, product_name, quantity, price """
    values = [(
        fake.date_this_month(),
        fake_product.ecommerce_name(),
        random.randint(1, 10),
        (random.randint(1000, 100000) / 100))
        for _ in range(DATA_SIZE)]
    return values


def insert_data(table_name, column_names, values: list[tuple]) -> None:
    try:
        placeholders = ("%s, " * len(values[0])).rstrip(", ")
        insert_query = (f"""
            INSERT INTO {table_name} ({column_names})
            VALUES ({placeholders}); """)
        with conn.cursor() as cursor:
            cursor.executemany(insert_query, values)
        conn.commit()
        print(f'INFO:     Insertion into table "{table_name}" successful')
    except Exception as _ex:
        print(f'INFO:     Error while inserting into "{table_name}": {_ex}')


if __name__ == "__main__":
    try:
        conn = seed_database.get_connection()
        fake = Faker()
        fake_product = Faker()
        fake_product.add_provider(faker_commerce.Provider)
        insert_data(
            table_name="sales",
            column_names="sale_date, product_name, quantity, price",
            values=gen_data())
    finally:
        if conn:
            conn.close()
        print("INFO:     PostgreSQL connection closed")
