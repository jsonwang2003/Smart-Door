import cv2 as cv
import numpy as np
import face_recognition
import face_recognition_models

# img = cv.imread('Photos\Caleb3.jpg')

# cv.imshow('Caleb', img)
# cv.waitKey(0)

# image = face_recognition.load_image_file("Photos\Caleb3.jpg")
# face_locations = face_recognition.face_locations(image)
# for box in face_locations:
#     top, right, bottom, left = box
#     print("Face at:", top, right, bottom, left)
# cv.rectangle(image, (left, top), (right, bottom), (0, 255, 0), thickness = 2)
# cv.imshow('Identify', image)

# Start video capture
capture = cv.VideoCapture(0)
import serial
import time


# Captures the video of first video tool
capture=cv.VideoCapture(0)


# Load images to look for
# Need to make photos folder and add photos you want to check
caleb_image = face_recognition.load_image_file("Photos\OGCaleb.jpg")
# Load face encoding
caleb_face_encoding = face_recognition.face_encodings(caleb_image)[0]

# Can add multiple faces into encoding
known_face_encodings = [
    caleb_face_encoding
]


# Add multiple names to the list
face_names = ["Caleb"]


ser = serial.Serial(port='COM16', baudrate= 115200,timeout = 1)

time.sleep(2)

unlocked = False

def send_command(cmd, unlockedstatus):

     # send command with newline
    ser.write((cmd + '\n').encode('ascii'))
    ser.flush()
    time.sleep(0.1)  # short delay

    # read metro1 response (if any)
    while ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print("metro1 says:", response)
    if response == "Time out":
        unlockedstatus = False




send_command("False")

time.sleep(1)

# Start Face Detection, capturing frame-by-frame
while True:


    # While loop is running capture every frame and process
    ret, frame = capture.read()
    # Convert frame taken to RGB
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    # Use face location function to get face location of the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    # Use face encoding function to get the face encoding of the frame
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
            if unlocked == False:
                send_command("True", unlocked)
                unlocked = True
        # elif unlocked == True:
        #     send_command("False")
        #     unlocked = False

        # Draw a box around the face
        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    if len(face_encodings) == 0:
        send_command("False")

    # Display the resulting image
    cv.imshow('Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()

#destroys the window
cv.destroyAllWindows
ser.close()