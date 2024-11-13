from ultralytics import YOLO
import cv2

# load the model
model = YOLO('yolov8n.pt')

video_path = "/home/capacity-monitor/ dev/ML-UVA---Capacity-Tractor/video_cv/new_in_out.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("VIDEO CANNOT BE OPENED")

while cap.isOpened():
    # frame by frame
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame)

    # filter people
    persons = [res for res in results[0].boxes if res.cls == 0]

    for person in persons:
        x1, y1, x2, y2 = map(int, person.xyxy[0])
        label = f'Person {float(person.conf):.2f}'

        cv2.rectangle(frame, (x1, y1), (x2,y2), (0, 255, 0), 4)

        font_scale = 1.5
        thickness = 3

        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), thickness)

    cv2.imshow('video detection', frame)

    #q to exit video early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()