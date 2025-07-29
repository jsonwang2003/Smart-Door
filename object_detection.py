import torch
import cv2 as cv
import os

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # or yolov5n, yolov5m, yolov5l, yolov5x, etc.

# Directory containing images
capture = cv.VideoCapture(0)

process_this_frame = True

while True:
    ret, img = capture.read()
    
    if process_this_frame:  
        # Resize frame of video to 1/4 size for faster processing
        small_frame = cv.resize(img, (0, 0), fx=0.25, fy=0.25)
        
        # Convert frame taken to RGB
        rgb_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)
        
        # Perform inference
        results = model(rgb_frame)
    
    scale = 1 / 0.25  # = 4.0
    for (left, top, right, bottom), conf, cls in zip(results.xyxy[0][:, :4], results.xyxy[0][:, 4], results.xyxy[0][:, 5]):
        left, top, right, bottom = [int(coord * scale) for coord in (left, top, right, bottom)]
        cv.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 2)
        cv.putText(img, f'{model.names[int(cls)]} {conf:.2f}', (left, top - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    process_this_frame = not process_this_frame

    cv.imshow('YOLOv5 Detection', img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()
    
    # # Inference
    # results = model(img_rgb)

    # # Results
    # print(f"Results for {img_name}:")
    # results.show()

    # # Save results to 'runs/detect/exp*'
    # results.save()