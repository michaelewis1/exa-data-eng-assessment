import os
import psycopg2
import json 
import logging
from utils import get_file_names, reset_db, get_file_data
from database import create_patient_table, insert_patient, insert_new_resource
logger = logging.getLogger(__name__)
def main(cursor):
    files = get_file_names("data")
    if not files:
        raise Exception("No files found in data directory")
    create_patient_table(cursor)
# run this async
    for file_key in files:
        try:
            data = get_file_data(f"data/{file_key}")
            entries = data["entry"]
            if not entries:
                logger.warning(f"No entries found in file {file_key}")
                continue

            for entry in entries:
                if entry.get("resourceType") == "Patient":
                    patient = entry
                    insert_patient(cursor, patient)
                    entries.remove(entry)
                else:
                    logger.error("No patient found in entries")
                    continue
                
            for resource in entries:
                resource_type = resource.get("resourceType").lower()
                if resource_type == "patient":
                    continue
                resource_id = insert_new_resource(cursor, resource, patient["id"])
                logger.info(f"Inserted {resource_type} with id: {resource_id}")


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

    main(cursor)
    
    connection.close()