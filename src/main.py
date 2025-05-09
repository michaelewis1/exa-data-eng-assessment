import os, psycopg2, json, logging
from src.utils import get_file_names, reset_db, get_file_data
from src.transformer import format_to_fhir
from src.database import create_patient_table
logger = logging.getLogger(__name__)
def main():
    files = get_file_names("data")
    if not files:
        raise Exception("No files found in data directory")
    create_patient_table(cursor)

# run this async
    for file_key in files:
        try:
            data = get_file_data(f"data/{file_key}")
            
        except Exception as e:
            logger.error(f"Error processing file {file_key}: {e}")
            continue

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

    main()
    
    cursor.close()
    connection.close()