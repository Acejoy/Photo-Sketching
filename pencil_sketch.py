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


# image_folder = r'D:\ML Projects\Neural Style Transfer\Content'
image_folder = './pics'

images_list = os.listdir(image_folder)

cv2.namedWindow('kernel size')
cv2.resizeWindow('kernel size', 400, 83 )
cv2.createTrackbar('Trackbar', 'kernel size', 35, 77, nothing)
cv2.setTrackbarMax('Trackbar', 'kernel size', 77)
cv2.setTrackbarMin('Trackbar', 'kernel size', 35)
cv2.setTrackbarPos('Trackbar', 'kernel size', 59)

cv2.createTrackbar('Shadow', 'kernel size', 0, 100, nothing)
cv2.setTrackbarMax('Shadow', 'kernel size', 100)
cv2.setTrackbarMin('Shadow', 'kernel size', 0)
cv2.setTrackbarPos('Shadow', 'kernel size', 10)


index=0;

while True:

    image_name = images_list[index]
    image = cv2.imread(os.path.join(image_folder, image_name))

    resized_img = resize(image)

    img_width = resized_img.shape[0]
    img_height = resized_img.shape[1]
    canvas = np.ones((img_width, img_height), dtype=np.uint8)
    
    grayed_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    negative = 255-grayed_img

    val = int(cv2.getTrackbarPos('Trackbar', 'kernel size'))
    kernel_size = val if val%2 != 0 else val +1

    blurred_img = cv2.GaussianBlur(negative, (kernel_size,kernel_size), sigmaX=0, sigmaY=0)
    sketch = cv2.divide(grayed_img, 255-blurred_img, scale=256)
    sketch2 = cv2.multiply(sketch, 255-canvas, scale=1./256)
    
    shadow = int(cv2.getTrackbarPos('Shadow', 'kernel size'))
    sketch2 = sketch2-shadow
    sketch2[sketch2<0]=0

    cv2.imshow('sketch', sketch2)
    
    k = cv2.waitKeyEx(1)
    if k == 2424832:
        index = index-1 if index != 0 else 0
    elif k == 2555904:
        if index == len(images_list)-1:
            break
        else:
            index += 1
    elif k == ord('q'):
        break
    elif k == ord('s'):
        cv2.imwrite('./sketches/pencil_sketch_'+image_name+'.jpg', sketch2)
        print('Image Saved')

cv2.destroyAllWindows()