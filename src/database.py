import logging
import os
from psycopg2 import sql

logger = logging.getLogger(__name__)

def create_patient_table(cursor): # https://fhirbase.aidbox.app/schema
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS "patient" (
        id text PRIMARY KEY,               // id of resource
        txid bigint not null,              // version id and logical transaction id
        ts timestamptz DEFAULT NOW(),      // last updated time
        resource_type text,                // resource type
        status resource_status not null,   // resource status
        resource jsonb not null            // resource body
        );
        """)
    cursor.execute(query)
    logger.info("Patient table created successfully.")

insert_patient_query = """
    INSERT INTO Patient 
    VALUES (%s)
    """
create_resource_table = """
    CREATE TABLE 

"""
