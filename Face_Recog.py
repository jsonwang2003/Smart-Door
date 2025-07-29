import cv2 as cv
import numpy as np
import face_recognition
import face_recognition_models
import serial
import time

# Captures the video of first video tool
capture = cv.VideoCapture(0)

# Load images to look for
# Need to make photos folder and add photos you want to check
caleb_image = face_recognition.load_image_file("Photos/OGCaleb.jpg")
# Load face encoding
caleb_face_encoding = face_recognition.face_encodings(caleb_image)[0]

# Can add multiple faces into encoding
known_face_encodings = [
    caleb_face_encoding
]

# Add multiple names to the list
face_names = ["Caleb"]

ser = serial.Serial(port='COM16', baudrate= 115200,timeout = 1)

def send_command(cmd):
    msg = "True" if cmd else "False"
    ser.write((msg + '\n').encode('ascii'))
    ser.flush()
    time.sleep(0.1)  # short delay

    # read metro1 response (if any)
    while ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print("metro1 says:", response)
        if response == "Time out":
            print("Change false")
        else:
            print("Change true")

process_this_frame = True

# Start Face Detection, capturing frame-by-frame
while True:

    # While loop is running capture every frame and process
    ret, frame = capture.read()

    if process_this_frame:
        
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert frame taken to RGB
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # For loop with 3 different variables
    # top, right, bottom, left, takes the top left coordinate and bottom right coordinate of a rectangle that covers the face location for every loop
    # Face_encoding loops through the array of face_encodings and known loops through the array of known_face_encodings
    for (top, right, bottom, left), face_encoding, known in zip(face_locations, face_encodings, known_face_encodings):
        # matches uses compare faces function to compare face encodings shown with the preloaded face encodings with tolerance of 0.42
        # The lower the number, the more accurate it is 

        matches = face_recognition.compare_faces(known, face_encodings, tolerance=0.42)
        name = "Unknown"

        # If there's a match with the first face encoding, use the first one
        # if not, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known, face_encodings)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = "Caleb"
            send_command("True")
        else:
            send_command("False")
            print("No match")

        # Draw a box around the face
        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    if len(face_encodings) == 0:
        send_command("No face")

    process_this_frame = not process_this_frame
    
    # Display the resulting image
    cv.imshow('Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()

#destroys the window
cv.destroyAllWindows
ser.close()