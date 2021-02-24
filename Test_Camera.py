import cv2
import time

eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def draw_boundary(img,classifier,scaleFactor,minNighbors,color,text):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features=classifier.detectMultiScale(gray,scaleFactor,minNighbors)
        coords=[]
        for(x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),color,1)
                cv2.putText(img,text,(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.1,color,1,cv2.LINE_AA)
                coords=[x,y,w,h]
        return coords
        
def detect(img,eyeCascade):
        color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
        coords = draw_boundary(img, eyeCascade, 1.1, 10, color['green'], "Eye")
        return img

        
cap = cv2.VideoCapture(0)
while (True):
        ret,frame = cap.read()
        frame = cv2.resize(frame, (240,160), interpolation = cv2.INTER_AREA)
        frame = detect(frame, eyeCascade)
        cv2.imshow("Face Detection", frame)
        if(cv2.waitKey(1) & 0xFF== ord('q')):
            break
cap.release()
cv2.destroyAllWindows()

        


