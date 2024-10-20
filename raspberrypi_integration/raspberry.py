from ultralytics import YOLO

import cv2
import json
import time
from azure.storage.blob import BlobServiceClient
from picamera2 import Picamera2

AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=capacityblob;AccountKey=FUMSzy2uqGjpWOcX+rixa0FA1UCdZjOZcSmXecSS/UxjnNavvaY/9XFy7q7eUXRcErvuGoHh+SOK+AStUU0dIg==;EndpointSuffix=core.windows.net"
AZURE_CONTAINER_NAME = "testcapacity"
BLOB_NAME = "capacityblob"

def check_azure_connection():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        blobs = list(container_client.list_blobs())
        return True
    except:
        return False

if check_azure_connection():
    print("yes")

model = YOLO('yolov8n.pt')
camera = Picamera2()
camera.resolution = (640, 480)

enter_count = 0
exit_count = 0
previous_positions = {}

def capture_video(video_path):
    camera.start_recording(video_path)
    time.sleep(300) 
    camera.stop_recording()

while True:
    video_file = 'video_capture.h264'
    capture_video(video_file)
    cap = cv2.VideoCapture(video_file)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    door_line_x = int(frame_width * 0.5)
    box_width = int(frame_width * 0.2)
    box_height = int(frame_height * 0.8)
    box_x = door_line_x - box_width // 2
    box_y = (frame_height - box_height) // 2
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        results = model(frame)
        persons = [res for res in results[0].boxes if res.cls == 0]
        current_positions = {}
        for person_id, person in enumerate(persons):
            x1, y1, x2, y2 = map(int, person.xyxy[0])
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            current_positions[person_id] = (center_x, center_y)
            if person_id in previous_positions:
                prev_center_x, prev_center_y = previous_positions[person_id]
                if box_y <= center_y <= box_y + box_height:
                    if prev_center_x < door_line_x and center_x >= door_line_x:
                        exit_count += 1
                    elif prev_center_x > door_line_x and center_x <= door_line_x:
                        enter_count += 1
        previous_positions = current_positions.copy()
    cap.release()

    result_data = [{"in": enter_count, "out": exit_count}]
    result_json = json.dumps(result_data)
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=BLOB_NAME)
        blob_client.upload_blob(result_json, overwrite=True)
        print(result_json)
    except Exception as e:
        print(f"Error uploading data to Azure Blob Storage: {e}")
