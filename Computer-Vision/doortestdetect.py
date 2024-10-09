from ultralytics import YOLO
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Initialize DeepSORT tracker with adjusted parameters
tracker = DeepSort(max_age=50, n_init=1, max_iou_distance=0.7)

# Open video stream
video_path = '/Users/shivpatel/Documents/door_in_out.mov'  # Replace with your video file path
cap = cv2.VideoCapture(video_path)

# Initialize variables to store counts
count_in = 0
count_out = 0

# Dictionary to store previous frame y-coordinate for each tracked person
previous_positions = {}

# Initialize sets to prevent multiple counts
counted_in_ids = set()
counted_out_ids = set()

# Manually define the door area (adjust these coordinates to match your video)
door_x1, door_y1, door_x2, door_y2 = 180, 80, 420, 520  # Adjusted to better match the door

# Main video loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference on the current frame
    results = model(frame)

    # Prepare detections for DeepSORT in the format [[x1, y1, x2, y2], confidence]
    detections = []

    # Extract detected objects
    for r in results:
        for box in r.boxes:
            label = model.names[int(box.cls[0])]

            xyxy = box.xyxy[0]
            x1, y1, x2, y2 = map(int, xyxy)  # Convert coordinates to integers
            score = float(box.conf[0])  # Confidence score

            if label == 'person':  # Track people
                detections.append([[x1, y1, x2, y2], score])

    # Draw the door area on the frame
    cv2.rectangle(frame, (door_x1, door_y1), (door_x2, door_y2), (255, 165, 0), 2)
    cv2.putText(frame, 'Door Area', (door_x1, door_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 2)

    # Ensure detections are properly formatted and not empty before updating the tracker
    if len(detections) > 0:
        # Update the DeepSORT tracker with current detections
        tracked_objects = tracker.update_tracks(detections, frame=frame)

        # Track entry/exit logic for each tracked person
        for track in tracked_objects:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            bbox = track.to_ltrb()  # Bounding box format (left, top, right, bottom)
            x1, y1, x2, y2 = map(int, bbox)
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # Draw tracked person's bounding box and ID
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Track entry/exit based on crossing the door area
            if track_id in previous_positions:
                prev_center_y = previous_positions[track_id]
            else:
                prev_center_y = center_y  # Initialize with current center_y

            previous_positions[track_id] = center_y

            # Check if the person is crossing the door bounding box
            if door_x1 < center_x < door_x2 and door_y1 < center_y < door_y2:
                # Determine if the person is entering or exiting based on movement direction
                if prev_center_y < door_y1 and center_y >= door_y1 and track_id not in counted_in_ids:
                    count_in += 1
                    counted_in_ids.add(track_id)
                    print(f"Track ID {track_id} entered. Count In: {count_in}")
                elif prev_center_y > door_y2 and center_y <= door_y2 and track_id not in counted_out_ids:
                    count_out += 1
                    counted_out_ids.add(track_id)
                    print(f"Track ID {track_id} exited. Count Out: {count_out}")

    # Display the counts on the frame
    cv2.putText(frame, f'In: {count_in}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f'Out: {count_out}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('People Counting', frame)

    # Press 'q' to exit the video loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# Print the final counts after processing is complete
print(f"Final Counts:\nPeople Entered: {count_in}\nPeople Exited: {count_out}")
