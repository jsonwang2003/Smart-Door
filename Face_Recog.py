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

capture=cv.VideoCapture(0)

jason_image = face_recognition.load_image_file("Jason's Profile Picture.jpg")
jason_face_encoding = face_recognition.face_encodings(jason_image)[0]

face_names = ["Jason"]

while True:

    ret, frame = capture.read()
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(face_encodings, jason_face_encoding, tolerance=0.4)
        name = "Unknown"

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

    # Display the resulting image
    cv.imshow('Video', frame)

    if cv.waitKey(1) & 0xFF==ord('q'):

        break



capture.release()
#destroys the window
cv.destroyAllWindows