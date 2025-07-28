import torch
import cv2 as cv
import os

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # or yolov5n, yolov5m, yolov5l, yolov5x, etc.

# Directory containing images
images_dir = 'Images'
image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

for img_name in image_files:
    img_path = os.path.join(images_dir, img_name)
    img = cv.imread(img_path)
    if img is None:
        print(f"Failed to load {img_path}")
        continue
    # Convert BGR (OpenCV) to RGB
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    # Inference
    results = model(img_rgb)
    # Results
    print(f"Results for {img_name}:")
    results.print()  # or .show(), .save(), etc.
    # Save results to 'runs/detect/exp*'
    results.save()