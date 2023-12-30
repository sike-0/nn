# Import module
from nudenet import NudeDetector
import cv2
import numpy as np
import random

def randColor():
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    return (r,g,b)

# initialize detecter (downloads the checkpoint file automatically the first time)
detector = NudeDetector()

# Classify single image
coordinates = detector.detect("img.jpg")

print(coordinates)

# Load image
img = cv2.imread("img.jpg")

print(img.shape)

for coord in coordinates:
    x1, y1, x2, y2 = coord["box"]
    label = coord["class"]
    score = coord["score"]

    # Draw bounding box on image
    img = cv2.rectangle(img, (x1, y1), (x2+x1, y2+y1), randColor(), 2)

    # Add text to image
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f"{label} {score}", (x1, y1 - 10), font, 0.5, (100, 255, 0), 1)

# Display image
cv2.imwrite("out.jpg", img)
