import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

def get_blob_service_client():
    connect_str = os.getenv('Connection_blob')  
    return BlobServiceClient.from_connection_string(connect_str)

def get_blob_content(container_name, blob_name):
    try:
        blob_service_client = get_blob_service_client()
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob().readall()
        return blob_data.decode('utf-8')  # Assuming the blob contains text data
    except Exception as e:
        logging.error(f"Error reading blob: {str(e)}")
        return None

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function to read blob content.')

    container_name = "testcapacity"  # Update with your container name
    blob_name = "capacityblob"       # Update with your blob name

    # Fetch the blob content
    blob_content = get_blob_content(container_name, blob_name)

    # Check if blob content was retrieved
    if blob_content:
        logging.info(f"Blob content successfully retrieved: {blob_content}")
        return func.HttpResponse(f"Blob content read successfully:\n{blob_content}", status_code=200)
    else:
        logging.error("Failed to retrieve blob content.")
        return func.HttpResponse("Error reading blob content", status_code=500)
