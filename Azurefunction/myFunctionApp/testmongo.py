import os
from pymongo import MongoClient
import certifi

def get_mongo_client():
    mongo_uri = os.getenv('MONGO_DB_CONNECTION_STRING')
    if not mongo_uri:
        raise ValueError("MONGO_DB_CONNECTION_STRING environment variable not set")
    # Use certifi's certificate bundle for SSL verification
    return MongoClient(mongo_uri, tlsCAFile=certifi.where())

def check_mongo_connection():
    client = get_mongo_client()
    print("Connection successful:", client)

check_mongo_connection()
