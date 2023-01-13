import cv2
import numpy as np
import autopy
import handTrackingModule as htm
import time

def virtualMouse():
    wScr, hScr = autopy.screen.size()
    cap=cv2.VideoCapture(0)

    smoothening = 7 #smoothener
    frameR = 100 # Frame Reduction
    width=640
    height=480
    cap.set(3,width)
    cap.set(4,height)

    detector=htm.handDetector(maxHands=1)

    ptime=0
    ctime=0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    while True:
        sucess,img=cap.read()
        img=detector.findHands(img)
        lmlist=detector.findPos(img,draw=False)
        if len(lmlist)!=0:
            x1,y1=lmlist[8][1:] #get x and y coordinates of index finger
            x2, y2 = lmlist[12][1:]  # get x and y coordinates of middle finger
            fingers=detector.fingersUp()
            #print(fingers)
            #rectangle to reduce entire screen size to this rectangle
            cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)
            #mouse moving
            if fingers[1]==1 and fingers[2]==0:
                cv2.circle(img, (x1,y1), 15, (0, 255, 0), cv2.FILLED)
                x3 = np.interp(x1, (frameR, width - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, height - frameR), (0, hScr))
                # 6. Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                autopy.mouse.move(wScr - clocX, clocY)
                plocX, plocY = clocX, clocY
            if fingers[1]==1 and fingers[2]==1:
                length, img, lineInfo = detector.findDistance(8, 12, img,draw=False)
                #print(length)
                if length < 50:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()

        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img, str(int(fps)), (50, 25), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 0, 0), 2)

        cv2.imshow("webcam",img)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cv2.destroyAllWindows()

