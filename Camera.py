import cv2
import time
import lcddriver
import subprocess
from Sound import sound
from Keypad import keypad

class camera():
        
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
                
        def detect(self,img,eyeCascade,check_eye):
                color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
                coords,check_eye = self.draw_boundary(img,eyeCascade,1.1,10,color['green'],"Eye",check_eye)
                return img,check_eye

        def camera_on(self):
                try :
                        display = lcddriver.lcd()
                        display.lcd_clear()
                        time.sleep(1)
                        display.lcd_display_string("Camera Detect",1)
                        cap = cv2.VideoCapture(0)
                        snd = sound()
                        check_eye = 0
                        sound_alert = 0
                        display.lcd_display_string("Ready...     ",2)
                        while (True):
                                ret,frame = cap.read()
                                frame = cv2.resize(frame,(240,160),interpolation = cv2.INTER_AREA)
                                frame,check_eye = self.detect(frame,self.eyeCascade,check_eye)
                                if(sound_alert == 0 and check_eye > 11):
                                        snd.on()
                                        sound_alert = 1
                                        display.lcd_display_string("Detected !!!",2)
                                        
                                elif(sound_alert == 1 and check_eye == 0):
                                        snd.off()
                                        sound_alert = 0
                                        display.lcd_display_string("Ready...     ",2)
                                kp = keypad()
                                if(kp.getKey() == "D"):
                                        time.sleep(0.4)
                                        display.lcd_display_string("Stopping...  ",2)
                                        time.sleep(2)
                                        display.lcd_clear()
                                        if(sound_alert == 1):
                                                snd.off()
                                        break
                                
                        cap.release()
                        cv2.destroyAllWindows()
                        
                except:
                        display.lcd_display_string("Port Error!!!  ",2)
                        time.sleep(3)
                        display.lcd_clear()
                        time.sleep(1)
                        display.lcd_display_string("Reboot...",1)
                        print(subprocess.call("sudo reboot", shell=True))
