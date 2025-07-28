import torch
import cv2 as cv
import numpy as np
import face_recognition
import face_recognition_models

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # or yolov5n, yolov5m, yolov5l, yolov5x, etc.

# Capture video from the webcam
capture = cv.VideoCapture(0)

while True:
    # Initialize variables
    ret, frame = capture.read()
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Inference using YOLOv5
    results = model(rgb_frame)

    # Process results
    for result in results.xyxy[0]:  # results for each detected object
        x1, y1, x2, y2, conf, cls = result
        if conf > 0.5:  # Confidence threshold
            cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv.putText(frame, f"Class: {cls}, Conf: {conf:.2f}", (int(x1), int(y1) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"

        # Check if frame has a face
        matches = face_recognition.compare_faces(face_encodings, jason_face_encoding, tolerance=0.4)

        face_distances = face_recognition.face_distance(face_encodings, jason_face_encoding)
        for i in face_distances:
            print(i)
        
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = "Jason"
        
        # Draw a box around the face
        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # Display the resulting frame
    cv.imshow('YOLOv5 Detection', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()