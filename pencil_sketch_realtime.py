import os
import cv2
import numpy as np

def nothing(x):
    pass

def resize(img, width=400):
    img_width = img.shape[1]
    img_height = img.shape[0]
    new_height = int((img_height/img_width)*400)
    return cv2.resize(img, (400, new_height))


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cv2.namedWindow('kernel size')
cv2.resizeWindow('kernel size', 400, 83 )
cv2.createTrackbar('Trackbar', 'kernel size', 1, 47, nothing)
cv2.setTrackbarMax('Trackbar', 'kernel size', 47)
cv2.setTrackbarMin('Trackbar', 'kernel size', 1)
cv2.setTrackbarPos('Trackbar', 'kernel size', 35)

cv2.createTrackbar('Shadow', 'kernel size', 0, 100, nothing)
cv2.setTrackbarMax('Shadow', 'kernel size', 100)
cv2.setTrackbarMin('Shadow', 'kernel size', 0)
cv2.setTrackbarPos('Shadow', 'kernel size', 10)


index=0;

while True:

    ret, frame = cap.read()
    if not ret:
        break

    
    resized_frame = resize(frame)
    grayed_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    negative = 255-grayed_frame

    val = int(cv2.getTrackbarPos('Trackbar', 'kernel size'))
    kernel_size = val if val%2 != 0 else val +1

    blurred_frame = cv2.GaussianBlur(negative, (kernel_size,kernel_size), sigmaX=0, sigmaY=0)
    sketch = cv2.divide(grayed_frame, 255-blurred_frame, scale=256)

    shadow = int(cv2.getTrackbarPos('Shadow', 'kernel size'))
    sketch = sketch-shadow
    sketch[sketch<0]=0
    cv2.imshow('sketch', sketch)

    k = cv2.waitKeyEx(1)
    
    if k == ord('q'):
        break
    elif k == ord('s'):
        cv2.imwrite('./sketches/pencil_sketch.jpg', sketch)
        print('Frame Saved')

cap.release()
cv2.destroyAllWindows()