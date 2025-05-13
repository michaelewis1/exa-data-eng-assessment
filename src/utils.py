import json, os
from json.decoder import JSONDecodeError

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

def get_file_names(path: str) -> list:
    """
    gets file names from directory
    """
    files = []
    for file in os.listdir(path):
        if file.endswith(".json"):
            files.append(file)
    logger.info(f"Found {len(files)} files in {path}.")
    return files

def get_file_data(path: str) -> dict:
    """
    Reads data from a file and returns json
    json easy to work with imo
    """
    try:
        with open(path, 'r') as f:
            parsed_data = json.load(f)
            logger.info(f"File {path} read successfully.")
            return parsed_data

    except JSONDecodeError as e:
        logger.error(f"File not in valid json format : {path}")
        raise e