import cv2
import mediapipe as mp
import time

import numpy as np

import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def volControl():
    cap=cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    ptime=0
    ctime=0
    detector=htm.handDetector()


    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    #volume.GetMute()
    #volume.GetMasterVolumeLevel()
    volume.GetVolumeRange()

    volBar=220
    vper=0
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
            vol=np.interp(lent,[10,215],[-65.25,0])
            volBar=np.interp(lent,[10,215],[220,480])
            vper=np.interp(lent,[10,215],[0,100])
            volume.SetMasterVolumeLevel(vol, None)


        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img,str(int(fps)),(50,25),cv2.FONT_HERSHEY_COMPLEX,0.75,(255,0,0),2)

        cv2.rectangle(img,(220,400),(480,440),(0,255,0),2)
        cv2.rectangle(img, (220,400), (int(volBar), 440), (0, 255, 0), cv2.FILLED)
        cv2.putText(img,str(int(vper))+"%",(140,430),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),1)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cv2.destroyAllWindows()

