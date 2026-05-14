import mysql.connector
from datetime import datetime
import cv2
import time
from ultralytics import YOLO

print("Retail Analytics Detection Started...")

# Load YOLO model (better accuracy)
model = YOLO("yolov8s.pt")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Raiyan@4328",
    database="retail_analytics"
)

cursor = conn.cursor()
last_saved_time = 0

# Open webcam (recommended for Windows)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam opened successfully.")

# Higher resolution improves small-object detection
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

frame_count = 0
counted_ids = set()
while True:
    # Read frame
    ret, frame = cap.read()
    frame_count += 1

    if frame_count % 2 != 0:
        continue

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Run detection on all supported classes
    results = model.track(
    frame,
    persist=True,
    conf=0.60,
    imgsz=416,
    verbose=False
    )

    # Separate counters
    customer_count = 0      # Number of persons
    object_count = 0        # Number of non-person objects

    # Person numbering (Person 1, Person 2, ...)
    person_number = 0

    # Store names of detected objects
    detected_object_names = []

    # Process detections
    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            # Bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Class information
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            track_id = None

            if box.id is not None:
                track_id = int(box.id[0])

            # Person detection
            if class_name == "person":

                if track_id is not None and track_id not in counted_ids:
                    counted_ids.add(track_id)
                    customer_count += 1

                person_number += 1

                # Labels: Person 1, Person 2, ...
                label = f"Person {person_number}"
                color = (0, 255, 0)  # Green

            # Other objects
            else:
                object_count += 1
                detected_object_names.append(class_name)

                # Labels: Object: cell phone, Object: bottle, etc.
                label = f"Object: {class_name}"
                color = (255, 0, 0)  # Blue

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            # Draw label
            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    # Remove duplicate object names for summary display
    unique_objects = sorted(set(detected_object_names))
    object_names_text = ", ".join(unique_objects) if unique_objects else "None"

    query = """
    INSERT INTO visitors
    (people_count, object_count, detected_objects, timestamp)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        customer_count,
        object_count,
        object_names_text,
        datetime.now()
    )

    current_time = time.time()

    if current_time - last_saved_time > 5:
        cursor.execute(query, values)
        conn.commit()
        last_saved_time = current_time

    # Display separate counts
    cv2.putText(
        frame,
        f"Customers : {customer_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),  # Red
        2
    )

    cv2.putText(
        frame,
        f"Objects: {object_count}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),  # Blue
        2
    )

    # Display detected object names
    display_text = f"Detected Objects: {object_names_text}"
    if len(display_text) > 80:
        display_text = display_text[:77] + "..."

    cv2.putText(
        frame,
        display_text,
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 165, 255),  # Orange
        2
    )

    # Exit instruction
    cv2.putText(
        frame,
        "Press Q to Quit",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 0),
        2
    )

    # Show output
    cv2.imshow("Retail Analytics - Customer and Object Detection", frame)

    # Quit when Q is pressed
    if cv2.waitKey(10) & 0xFF == ord("q"):
        print("Closing application...")
        break

# Release resources
print("Closing application...")

cursor.close()
conn.close()

cap.release()
cv2.destroyAllWindows()