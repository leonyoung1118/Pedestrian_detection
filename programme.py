import numpy as np
import cv2
import os
import sys

def detect_pedestrians(image ,count):
    
    save_dir = "pedestrian"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Converting the input RGB image to gray....
    cascade = cv2.CascadeClassifier('MyPedestrian.xml')  # extracting the cascade features using Haar classifiers...
    features = cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=15, minSize=(26, 74),
                                        maxSize=(70, 174))

    if len(features) == 0:  # if no features are found, we simply return an empty array.
        return False
    else:  # when the required features are detected, we execute the following steps....
        features[:, 2:] += features[:, :2]
        detection_box = []  # this array stores the length of the rectangle to be plotted with respect to the LTC pixel.
        for i in features:  # retaining the previous state of features in detection_box
            detection_box.append((i[0], i[1], i[2] - i[0], i[3] - i[1]))
        for j in detection_box:
            x1, y1, w1, h1 = j  # format --> [x index of LTC pixel, y index, width of the rectangle, height of the rectangle]
            cv2.rectangle(image, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)
            count += 1
            file_name = os.path.join(save_dir, str(count) + ".jpg")
            roi = image[y1:y1 + h1, x1:x1 + w1]
            cv2.imwrite(file_name, roi)
            cv2.imshow("123", roi)
            cv2.putText(image, "Pedestrian", (x1, y1 + h1 + 20), cv2.FONT_HERSHEY_TRIPLEX, .5, (0, 0, 255))
        return True

video = cv2.VideoCapture('1.MP4')
count = 0
while (video.isOpened()):
    ret, frame = video.read()
    if frame is None:
        cv2.destroyWindow()
    else:
        if detect_pedestrians(frame ,count)==True:
            count+=1
            cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF in (ord('q'), 0x1B, 0x0D):
        break
video.release()
#cv2.destroyWindow()
