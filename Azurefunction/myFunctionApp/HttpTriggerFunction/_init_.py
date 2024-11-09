import azure.functions as func
from azure.storage.blob import BlobServiceClient
import psycopg2
import os
import logging
import json

# Set up environment variables for PostgreSQL connection
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_DB'] = 'capdat'
os.environ['POSTGRES_USER'] = 'shivsri'
os.environ['POSTGRES_PASSWORD'] = 'water'

def get_blob_service_client():
    connect_str = os.getenv('Connection_blob')
    return BlobServiceClient.from_connection_string(connect_str)

def get_blob_content(container_name, blob_name):
    try:
        blob_service_client = get_blob_service_client()
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob().readall()
        return blob_data.decode('utf-8')
    except Exception as e:
        logging.error(f"Error reading blob: {str(e)}")
        return None

def ensure_table_exists(conn):
    """Ensure that the test_table exists with the required structure."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            "in" INTEGER,
            "out" INTEGER
        );
        """)
        conn.commit()
        cursor.close()
        logging.info("Confirmed that test_table exists with the required structure.")
    except Exception as e:
        logging.error(f"Failed to ensure test_table exists: {e}")
        conn.rollback()

def insert_to_postgresql(data):
    host = os.getenv('POSTGRES_HOST', 'your_postgres_host')
    database = os.getenv('POSTGRES_DB', 'your_database')
    user = os.getenv('POSTGRES_USER', 'your_user')
    password = os.getenv('POSTGRES_PASSWORD', 'your_password')

    try:
        # Parse data as JSON
        parsed_data = json.loads(data)  # Assumes data is a JSON string

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        # Ensure table exists
        ensure_table_exists(conn)

        cursor = conn.cursor()

        # Assuming parsed_data is a list of dictionaries
        for record in parsed_data:
            # Automatically wrap column names in double quotes if they are reserved keywords
            columns = ', '.join([f'"{col}"' if col.lower() in ['in', 'out'] else col for col in record.keys()])
            values = tuple(record.values())
            placeholders = ', '.join(['%s'] * len(values))

            sql = f"INSERT INTO test_table ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, values)
        
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Data inserted successfully into PostgreSQL.")
        return True

    except Exception as e:
        logging.error(f"Failed to connect or insert data into PostgreSQL: {e}")
        return False

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Function triggered successfully.')

    container_name = "testcapacity"
    blob_name = "capacityblob"

    # Retrieve blob content
    blob_content = get_blob_content(container_name, blob_name)

    if not blob_content:
        return func.HttpResponse("Error reading blob content", status_code=500)

    # Log the content retrieved from the blob to confirm successful reading
    logging.info(f"Blob content successfully retrieved: {blob_content}")

    # Insert into PostgreSQL only if blob content retrieval was successful
    if insert_to_postgresql(blob_content):
        return func.HttpResponse(f"Blob content retrieved and inserted into PostgreSQL successfully.\nBlob content: {blob_content}", status_code=200)
    else:
        return func.HttpResponse("Error inserting blob content into PostgreSQL", status_code=500)
