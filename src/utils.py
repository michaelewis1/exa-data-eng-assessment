import psycopg2

import logging

logger = logging.getLogger(__name__)
def reset_db(db_name : str, cursor: cursor):
    """
    Resets the database by dropping all tables and recreating them.
    Dont see point of using transaction
    
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

