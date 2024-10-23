from ultralytics import YOLO
import cv2
import json
import datetime
import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=capacityblob;AccountKey=FUMSzy2uqGjpWOcX+rixa0FA1UCdZjOZcSmXecSS/UxjnNavvaY/9XFy7q7eUXRcErvuGoHh+SOK+AStUU0dIg==;EndpointSuffix=core.windows.net"

AZURE_CONTAINER_NAME = "testcapacity"
BLOB_NAME = "capacityblob"
def check_azure_connection():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        blobs = list(container_client.list_blobs())
        print("Connection to Azure Blob Storage: Successful")
        return True
    except Exception as e:
        print(f"Error connecting to Azure Blob Storage: {e}")
        return False


if check_azure_connection():
    print("yes")


model = YOLO('yolov8n.pt')

video_path = "/Users/shivpatel/ML-UVA---Capacity-Tractor/in_out_logic/new_in_out.mp4"
cap = cv2.VideoCapture(video_path)


enter_count = 0
exit_count = 0


previous_positions = {}


frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
door_line_x = int(frame_width * 0.5)  


box_width = int(frame_width * 0.2)  
box_height = int(frame_height * 0.8) 
box_x = door_line_x - box_width // 2
box_y = (frame_height - box_height) // 2  

def adjust_door_line(value):
    global door_line_x, box_x
    door_line_x = value
    box_x = door_line_x - box_width // 2


cv2.namedWindow("Video Counter")
cv2.createTrackbar("Door Line", "Video Counter", door_line_x, frame_width, adjust_door_line)

if not cap.isOpened():
    print("VIDEO CANNOT BE OPENED")

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

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
        cv2.putText(frame, f'Person {person_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        current_positions[person_id] = (center_x, center_y)

        if person_id in previous_positions:
            prev_center_x, prev_center_y = previous_positions[person_id]

            if box_y <= center_y <= box_y + box_height:
                if prev_center_x < door_line_x and center_x >= door_line_x:
                    exit_count += 1
                    print(f"Frame {frame_count}: Person {person_id} exited. Count: {exit_count}")
                elif prev_center_x > door_line_x and center_x <= door_line_x:
                    enter_count += 1
                    print(f"Frame {frame_count}: Person {person_id} entered. Count: {enter_count}")
    
 
    cv2.line(frame, (door_line_x, box_y), (door_line_x, box_y + box_height), (0, 255, 255), 2)


    cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), (255, 0, 0), 2)
        
    cv2.putText(frame, f'Enter: {enter_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f'Exit: {exit_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, "Adjust door line with trackbar", (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Video Counter", frame)

    previous_positions = current_positions.copy()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


result_data = [{"in": enter_count, "out": exit_count}]  

result_json = json.dumps(result_data)


try:

    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

 
    blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=BLOB_NAME)
    blob_client.upload_blob(result_json, overwrite=True)
    print(f"Data successfully uploaded to Azure Blob Storage: {BLOB_NAME}")
    print(result_json)
except Exception as e:
    print(f"Error uploading data to Azure Blob Storage: {e}")
