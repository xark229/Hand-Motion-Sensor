import cv2
import mediapipe as mp
import time

import numpy as np

import handTrackingModule as htm
import math
import screen_brightness_control as sbc

def brightness_control():
    cap=cv2.VideoCapture(0)
    ptime=0
    ctime=0
    detector=htm.handDetector()


    volBar=400
    while True:
        success,img=cap.read()
        img=detector.findHands(img,draw=True)
        landlist=detector.findPos(img,draw=False)
        if len(landlist)!=0:
            x1, y1=landlist[4][1],landlist[4][2] #x-y coordinate of uppermost pt of thumb
            x2, y2 = landlist[8][1], landlist[8][2] #x-y coordinate of uppermost pt of index
            lent=math.hypot(x2-x1,y2-y1)
            # lowes 10 highest 215
            # lowes -65 highest 0
            vol=np.interp(lent,[10,215],[0,100])
            volBar=np.interp(lent,[10,215],[400,150])
            sbc.set_brightness(int(vol))

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img,str(int(fps)),(50,25),cv2.FONT_HERSHEY_COMPLEX,0.75,(255,0,0),2)

        cv2.rectangle(img,(50,150),(85,400),(255,0,255),2)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 255), cv2.FILLED)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cv2.destroyAllWindows()

