import os, psycopg2
def read_data(directory: str) -> list:
    """
    Reads data from a file and returns it as a list of lines.
    
    :param file_path: Path to the file to be read.
    :return: List of lines from the file.
    """
    with open(file_path, 'r') as file:
        data = file.readlines()
    return data

def set_up():





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
    set_up(cursor)