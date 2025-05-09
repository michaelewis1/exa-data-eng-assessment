import psycopg2, json

import logging

logger = logging.getLogger(__name__)

def reset_db(db_name : str, cursor):
    """
    Resets the database by dropping all tables and recreating them.
    Dont see point of using transaction
    in util file insted of database as this wouldnt be needed when migrating to AWS
    
    """
    delete_db_query = "DROP DATABASE IF EXISTS {}"
    create_db_query = "CREATE DATABASE {}"

    try:
        # Drop the database if it exists
        cursor.execute(delete_db_query.format(db_name))
        logger.info(f"Database '{db_name}' dropped successfully.")

        # Create a new database
        cursor.execute(create_db_query.format(db_name))
        logger.info(f"Database '{db_name}' created successfully.")
    except Exception as e:
        raise e

def read_data(path: str) -> dict:
    """
    Reads data from a file and returns json
    json easy to work with imo
    """
    with open(path, 'r') as json:
        data = file.readlines()
    return data
