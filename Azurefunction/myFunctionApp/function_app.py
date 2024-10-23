import azure.functions as func
import os
import logging
from azure.storage.blob import BlobServiceClient
from pymongo import MongoClient
from datetime import datetime

app = func.FunctionApp()

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

def update_capacity(blob_content):
    global current_capacity
    try:
        data = blob_content.strip()[1:-1]  
        values = data.split(",")
        in_value = int(values[0].split(":")[1].strip())
        out_value = int(values[1].split(":")[1].strip())
        current_capacity += (in_value - out_value)
    except Exception as e:
        logging.error(f"Error updating capacity: {str(e)}")

def get_mongo_client():
    mongo_uri = os.getenv('MONGO_DB_CONNECTION_STRING')  
    if not mongo_uri:
        raise ValueError("MONGO_DB_CONNECTION_STRING environment variable not set")
    client = MongoClient(mongo_uri)
    try:
        client.admin.command('ismaster')
        print("MongoDB connection successful")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        raise
    return client

def store_to_mongodb(result):
    try:
        client = get_mongo_client()
        db = client['capacity_db']  
        capacity_updates_collection = db['capacity_updates']  
        update_record = {
            "timestamp": datetime.utcnow(),
            "in_count": result["in"],
            "out_count": result["out"],
            "current_capacity": result["current_capacity"]
        }
        capacity_updates_collection.insert_one(update_record)
        logging.info(f"5-minute update inserted into MongoDB: {update_record}")
        global_capacity_collection = db['global_capacity']
        global_record = {
            "timestamp": datetime.utcnow(),
            "current_capacity": result["current_capacity"]
        }
        global_capacity_collection.update_one(
            {},  
            {"$set": global_record},  
            upsert=True  
        )
        logging.info(f"Global capacity updated in MongoDB: {global_record}")
    except Exception as e:
        logging.error(f"Error inserting into MongoDB: {str(e)}")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    container_name = "testcapacity"  
    blob_name = "capacityblob"  
    blob_content = get_blob_content(container_name, blob_name)

    if not blob_content:
        return func.HttpResponse("Error reading blob content", status_code=500)

    logging.info(f"Blob content successfully retrieved: {blob_content}")
    return func.HttpResponse(f"Blob content read successfully:\n{blob_content}", status_code=200)

def test_blob_content():
    container_name = "testcapacity"  
    blob_name = "capacityblob" 

    logging.info('Testing blob content retrieval...')
    blob_content = get_blob_content(container_name, blob_name)
    
    if blob_content:
        print("Blob content successfully retrieved:")
        print(blob_content)
    else:
        print("Failed to retrieve blob content.")
