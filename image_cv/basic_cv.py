from ultralytics import YOLO
import cv2
from matplotlib import pyplot as plt

# load the pretrained model
model = YOLO('yolov8n.pt') 

image_path = "/home/capacity-monitor/ dev/ML-UVA---Capacity-Tractor/image_cv/walking_two.jpg"
img = cv2.imread(image_path)

# preform object detcttion
results = model(img)

# filter for persons class
persons = [res for res in results[0].boxes if res.cls == 0]

# bouding boxes
for person in persons:
    x1, y1, x2, y2 = map(int, person.xyxy[0]) 
    label = f'Person {float(person.conf):.2f}'  # confidence score
    cv2.rectangle(img, (x1,y1), (x2, y2), (0, 255, 0), 10)

    font_scale = 2  # Significantly larger font scale
    thickness = 10   # Text thickness to match the font size
    cv2.putText(img, label, (x1, y1 -10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), thickness)

annotated_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.imshow(annotated_img)
plt.show()
