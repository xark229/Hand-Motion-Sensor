import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self,mode=False,maxHands=2,min_detection_conf=0.5,min_track_conf=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.min_detection_conf=min_detection_conf
        self.min_track_conf=min_track_conf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.min_detection_conf,self.min_track_conf)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self,img,draw=True):
        imgRgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        self.res = self.hands.process(imgRgb)

        if self.res.multi_hand_landmarks:  # if it detects a hand
            for handLmks in self.res.multi_hand_landmarks:  # handLmks stores hands
                if draw:
                    self.mpDraw.draw_landmarks(img, handLmks, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPos(self,img,handNo=0,draw=True):
        self.lmlist=[]
        if self.res.multi_hand_landmarks:
            myHand=self.res.multi_hand_landmarks[handNo]
            for id, lmks in enumerate(myHand.landmark):  # getting the id and coordinates of detected hands
                # print(id,lmks)
                h, w, c = img.shape  # getting height width and color channel of img
                cx, cy = int(lmks.x * w), int(lmks.y * h)  # finding centre pts of each pt in the hand
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(255,255,0),cv2.FILLED)
        return self.lmlist

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmlist[self.tipIds[0]][1] > self.lmlist[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    cap=cv2.VideoCapture(0)
    ptime=0
    ctime=0
    detector=handDetector()

    while True:
        success,img=cap.read()
        img=detector.findHands(img,True)
        landlist=detector.findPos(img)
        if len(landlist)!=0:
            print(landlist[2])
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img,str(int(fps)),(50,25),cv2.FONT_HERSHEY_COMPLEX,0.75,(255,0,0),2)

        cv2.imshow("allah",img)
        cv2.waitKey(1)

if __name__=="__main__":
    main()