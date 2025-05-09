import os, psycopg2
from src.transformer import Transformer
from src.utils import read_data, reset_db
from src.transformer import format_to_fhir

if __name__ == "__main__":
    db_params = {
        "dbname": "optum_db",
        "user": "user",
        "password": "password",
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": 5432,
    }
    connection = psycopg2.connect(**db_params)
    connection.autocommit = True
    cursor = connection.cursor()
    reset_db(cursor)
    raw_data = read_data()

# run this async
    for obj in raw_data:
        format_to_fhir(obj)

