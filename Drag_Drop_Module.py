import cv2
import handTrackingModule as htm



class dragRec():
    def __init__(self,centrPos,size=[200,200],colorR=(255,0,255)):
        self.centrPos=centrPos
        self.size=size
        self.colorR=colorR

    def update(self,cursor):
        cx,cy=self.centrPos
        w,h=self.size

        if cx - w // 2 < cursor[1] < cx + w // 2 and cy - h // 2 < cursor[2] < cy + h // 2:
            self.colorR = (0, 255, 0)
            self.centrPos = cursor[1:]

class dragC():
    def __init__(self,centrPos,rad,colorR=(255,0,255)):
        self.centrPos=centrPos
        self.rad=rad
        self.colorR=colorR

    def update(self,cursor):
        cx,cy=self.centrPos
        r=self.rad

        if cx - r < cursor[1] < cx + r  and cy - r < cursor[2] < cy + r:
            self.colorR = (0, 255, 0)
            self.centrPos = cursor[1:]

def drag_rectangle(n):
    rectList=[]
    for i in range(n):
        rectList.append(dragRec([i*250+150,150]))
    return rectList

def drag_circle(n):
    rectList=[]
    for i in range(n):
        rectList.append(dragC([i*250+150,150],100))
    return rectList

def dgdr(rectList,shape):
    cap = cv2.VideoCapture(0)
    detector = htm.handDetector(min_detection_conf=0.8)
    cap.set(3, 1280)
    cap.set(4, 720)
    colorR = (255, 0, 255)
    while True:
        success,img=cap.read()
        img = cv2.flip(img, 1)  # flipping the x axis
        img=detector.findHands(img)
        lmlist=detector.findPos(img)

        if len(lmlist)!=0:

            cursor=lmlist[8]

            lent, img, lineInfo = detector.findDistance(8, 12, img,draw=False)
            if lent<50:
                for rect in rectList:
                    rect.update(cursor)
            else:
                for rect in rectList:
                    rect.colorR=(255,0,255)

        ##draw
        if shape==1:
            for rect in rectList:
                cx,cy=rect.centrPos
                w,h=rect.size
                cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),rect.colorR,cv2.FILLED)
        else:
            for rect in rectList:
                cx,cy=rect.centrPos
                r=rect.rad
                cv2.circle(img,(cx,cy),r,rect.colorR,cv2.FILLED)

        cv2.imshow("video",img)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cv2.destroyAllWindows()

