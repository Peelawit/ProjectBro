import cv2
import time
import lcddriver
from Sound import sound
from Keypad import keypad

class camera():
        
        faceCascade = cv2.CascadeClassifier('/home/pi/Desktop/Face_Detection/haarcascade_frontalface_default.xml')
        eyeCascade = cv2.CascadeClassifier('/home/pi/Desktop/Face_Detection/haarcascade_eye.xml')

        def draw_boundary(self,img,classifier,scaleFactor,minNighbors,color,text,check):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                features=classifier.detectMultiScale(gray,scaleFactor,minNighbors)
                coords=[]
                check = check + 1
                for(x,y,w,h) in features:
                        check = 0
                        cv2.rectangle(img,(x,y),(x+w,y+h),color,1)
                        cv2.putText(img,text,(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.1,color,1,cv2.LINE_AA)
                        coords=[x,y,w,h]
                return coords,check
                
        def detect(self,img,faceCascade,eyeCascade,check_face,check_eye):
                color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
                coords,check_face = self.draw_boundary(img,faceCascade,1.1,10,color['red'],"Face",check_face)
                coords,check_eye = self.draw_boundary(img,eyeCascade,1.1,10,color['green'],"Eye",check_eye)
                return img,check_face,check_eye

        def camera_on(self):
                display = lcddriver.lcd()
                cap = cv2.VideoCapture(0)
                snd = sound()
                check_face = 0
                check_eye = 0
                sound_alert = 0
                display.lcd_clear()
                time.sleep(1)
                display.lcd_display_string("Camera Detect",1)
                display.lcd_display_string("Ready...  ",2)
                while (True):
                        ret,frame = cap.read()
                        frame = cv2.resize(frame,(176,144),interpolation = cv2.INTER_AREA)
                        frame,check_face,check_eye = self.detect(frame,self.faceCascade,self.eyeCascade,check_face,check_eye)
                        if(sound_alert == 0 and (check_face > 30 or check_eye > 10)):
                                snd.on()
                                sound_alert = 1
                                if(check_face > 30):
                                        display.lcd_display_string("Face !!! ",2)       
                                elif(check_eye > 10):
                                        display.lcd_display_string("Eye !!!  ",2)
                                
                        elif(sound_alert == 1 and (check_face == 0 and check_eye == 0)):
                                snd.off()
                                sound_alert = 0
                                display.lcd_display_string("Ready...  ",2)
                        kp = keypad()
                        if(kp.getKey() == "D"):
                                time.sleep(0.4)
                                display.lcd_display_string("Stopping...",2)
                                time.sleep(2)
                                display.lcd_clear()
                                if(sound_alert == 1):
                                        snd.off()
                                break
                        
                cap.release()
                cv2.destroyAllWindows()
