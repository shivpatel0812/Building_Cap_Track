import azure.functions as func
from azure.storage.blob import BlobServiceClient
import psycopg2
import os
import logging
import json


# Environment variables
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_DB'] = 'capdat'
os.environ['POSTGRES_USER'] = 'shivsri'
os.environ['POSTGRES_PASSWORD'] = 'water'


def get_blob_service_client():
   connect_str = os.getenv('Connection_blob')
   return BlobServiceClient.from_connection_string(connect_str)


def ensure_table_exists(conn):
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
   try:
       parsed_data = json.loads(data)
       conn = psycopg2.connect(
           host=os.getenv('POSTGRES_HOST'),
           database=os.getenv('POSTGRES_DB'),
           user=os.getenv('POSTGRES_USER'),
           password=os.getenv('POSTGRES_PASSWORD')
       )
       cursor = conn.cursor()
       cursor.execute("CREATE TABLE IF NOT EXISTS test_table (\"in\" INTEGER, \"out\" INTEGER);")
      
       # Insert records
       for record in parsed_data:
           columns = ', '.join([f'"{col}"' for col in record.keys()])
           values = tuple(record.values())
           placeholders = ', '.join(['%s'] * len(values))
           sql = f"INSERT INTO test_table ({columns}) VALUES ({placeholders})"
           cursor.execute(sql, values)
       conn.commit()
      
       # Fetch and log all records in the table
       cursor.execute("SELECT * FROM test_table;")
       all_records = cursor.fetchall()
       logging.info("Current contents of test_table:")
       for row in all_records:
           logging.info(row)
      
       cursor.close()
       conn.close()
       logging.info("Data inserted successfully into PostgreSQL.")
       return True
   except Exception as e:
       logging.error(f"Failed to connect or insert data into PostgreSQL: {e}")
       return False


def main(inputBlob: func.InputStream) -> None:
   logging.info('Blob trigger function processed a blob.')
   blob_content = inputBlob.read().decode('utf-8')
   logging.info(f"Blob content: {blob_content}")
   insert_to_postgresql(blob_content)