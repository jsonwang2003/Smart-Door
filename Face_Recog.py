import cv2 as cv
import numpy as np
import face_recognition
import face_recognition_models
import serial
import time

# Function to send serial data to metroboard
def send_command(cmd):
    # Send boolean command to metroboard as 'True' or 'False' string
    if cmd:
        msg = 'True\n'
    else:
        msg = 'False\n'
    ser.write(msg.encode('ascii'))
    ser.flush()
    time.sleep(0.1)  # short delay

    # read metro1 response (if any)
    while ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print("metro1 says:", response)
        if response == "Time out":
            print("Lock door")
        else:
            print("Unlock door")

# Start video capture
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

process_this_frame = True

# Start Face Detection, capturing frame-by-frame
while True:
    # Grab a single frame of video
    ret, frame = capture.read()
    
    # Only Process every other frame to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR (OpenCV) to RGB (face_recognition)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Compare the face encoding with the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.42)
            name = "Unknown"

            # If a match is found, use the first one
            if True in matches:
                first_match_index = matches.index(True)
                name = face_names[first_match_index]
                send_command("True")
            else:
                send_command("False")
                print("No match")

            face_names.append(name)
    
    process_this_frame = not process_this_frame

    for (top, right, bottom, left), face_encoding, known in zip(face_locations, face_encodings, known_face_encodings):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    if len(face_encodings) == 0:
        send_command("No face")

    # Display the resulting image
    cv.imshow('Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()

#destroys the window
cv.destroyAllWindows
ser.close()