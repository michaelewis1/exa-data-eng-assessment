import logging
import os, json
from psycopg2 import sql

logger = logging.getLogger(__name__)

def create_patient_table(cursor): # https://fhirbase.aidbox.app/schema , removed txid
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS "patient" (
        id text PRIMARY KEY,               // id of resource
        ts timestamptz DEFAULT NOW(),      // last updated time
        resource_type text,                // resource type
        status resource_status not null,   // resource status
        resource jsonb not null            // resource body
        );
        """)
    cursor.execute(query)
    logger.info("Patient table created successfully.")

def insert_patient(cursor, patient):
    """
    Insert a patient into the database.
    """
    # Extracting values from the patient object
    id = patient.get("id")
    resource_type = patient.get("resource_type")
    status = patient.get("status")
    resource = json.dumps(patient.get("resource"))

    insert_patient_query = """
        INSERT INTO Patient (
            id,
            resource_type,
            status,
            resource   
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data

        """
    cursor.execute(insert_patient_query, (id, resource_type, status, resource))

    logger.info(f"Inserted patient with id: {id}")
    return id


def insert_new_resource(cursor, resource, patient_id):
    """
    Insert a resource into the database.
    """
    resource_type = resource.get("resourceType").lower()
    resource_id = resource.get("id")

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {resource_type} (
            id TEXT PRIMARY KEY,
            patient_id TEXT REFERENCES patient(id),
            data JSONB
        )
    """)

    # Insert the resource with patient_id
    cursor.execute(f"""
        INSERT INTO {resource_type} (id, patient_id, data)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data
    """, (resource_id, patient_id, json(resource_type)))
    print(f"Inserted {resource_type} with id: {resource_id} linked to patient {patient_id}")

    return resource_id
