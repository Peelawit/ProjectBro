import time
import serial
import lcddriver
import subprocess
from Send_SMS import sms
from Keypad import keypad
from Phone_txt import phone_txt
from Password import password

class gps():
    
    def readString(self):
        while 1:
            while ser.read().decode("utf-8") != '$':  # Wait for the begging of the string
                pass  # Do nothing
            line = ser.readline().decode("utf-8")  # Read the entire string
            return line

    def getTime(self,string, format, returnFormat):
        return time.strftime(returnFormat,
                             time.strptime(string, format))  # Convert date and time to a nice printable format

    def getLatLng(self,latString, lngString):
        try :
            lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:]) * 1.0 / 60.0).lstrip("0.")
            lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:]) * 1.0 / 60.0).lstrip("0.")
            return lat, lng
        except :
            return 0,0

    def checksum(self,line):
        checkString = line.partition("*")
        checksum = 0
        for c in checkString[0]:
            checksum ^= ord(c)

        try:  # Just to make sure
            inputChecksum = int(checkString[2].rstrip(), 16);
        except:
            return False

        if(checksum == inputChecksum):
            return True
        else:
            print("===================================Checksum error!===================================")
            print(hex(checksum), "!=", hex(inputChecksum))
            return False

    def checkLatLng(self):
        display = lcddriver.lcd()
        display.lcd_clear()
        time.sleep(1)
        display.lcd_display_string("Parking lot  ",1)
        global lat_df,lng_df,charlatlng,ser
        try :
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Open Serial port
        except :
            display.lcd_display_string("Port Error!!!  ",2)
            time.sleep(3)
            display.lcd_clear()
            time.sleep(1)
            display.lcd_display_string("Reboot...",1)
            print(subprocess.call("sudo reboot", shell=True))
        txt = phone_txt()
        phoneNumber = txt.read()
        send = sms()
        count = 0
        reconnect = 0
        try:
            while True:
                line = self.readString()
                lines = line.split(",")
                if(self.checksum(line)):
                    if lines[0] == "GPGLL":
                        latlng = self.getLatLng(lines[1], lines[3])
                        if(latlng[0] == 0 and latlng[1] == 0):
                            display.lcd_display_string("Connecting...  ",2)
                            while(reconnect < 10):
                                if(subprocess.call("python3 /home/pi/Desktop/Face_Detection/GPS_Tester.py", shell=True) == 0):
                                    break
                                else :
                                    reconnect = reconnect + 1
                                time.sleep(1)
                            if(reconnect == 10) :
                                display.lcd_display_string("No Signal!!!  ",2)
                                time.sleep(3)
                                display.lcd_clear()
                                time.sleep(1)
                                break
                            else :
                                time.sleep(1)
                                self.checkLatLng()
                                break
                        display.lcd_display_string("Ready...   ",2)
                        if(count == 0):
                            lat_df = "{0:.4f}".format(float(latlng[0]))
                            lng_df = "{0:.4f}".format(float(latlng[1]))
                            lat_df = float(lat_df)
                            lng_df = float(lng_df)
                            count = 1
                        elif(count == 1) :
                            lat_new = "{0:.4f}".format(float(latlng[0]))
                            lng_new = "{0:.4f}".format(float(latlng[1]))
                            lat_new = float(lat_new)
                            lng_new = float(lng_new)
                                
                            if((lat_df+0.0005 < lat_new) or (lat_df-0.0005 > lat_new)
                                or (lng_df+0.0005 < lng_new) or (lng_df-0.0005 > lng_new)):
                                display.lcd_display_string("Detected !!!  ",2)
                                send.sendsms(phoneNumber,"Detected!!!, Your car leaves the parking lot.")
                                charlatlng = "http://maps.google.com/maps?q=" + str(latlng[0]) + str(lines[2]) + "," + str(latlng[1]) + str(lines[4])
                                send.sendsms(phoneNumber,charlatlng)
                                
                                while True :
                                    lat_df = "{0:.4f}".format(float(latlng[0]))
                                    lng_df = "{0:.4f}".format(float(latlng[1]))
                                    lat_df = float(lat_df)
                                    lng_df = float(lng_df)
                                    
                                    for x in range(300):
                                        kp = keypad()
                                        if(kp.getKey() == "D"):
                                            time.sleep(0.4)
                                            if(password.checkpass()):
                                                count = 3
                                                break
                                            display.lcd_display_string("Parking lot   ",1)
                                            display.lcd_display_string("Detected !!!  ",2)
                                        else :
                                            while True :
                                                line = self.readString()
                                                lines = line.split(",")
                                                if(self.checksum(line)):
                                                    if lines[0] == "GPGLL":
                                                        latlng = self.getLatLng(lines[1], lines[3])
                                                        break
                                                    
                                    lat_new = "{0:.4f}".format(float(latlng[0]))
                                    lng_new = "{0:.4f}".format(float(latlng[1]))
                                    lat_new = float(lat_new)
                                    lng_new = float(lng_new)
                                    
                                    if((lat_df+0.0005 < lat_new) or (lat_df-0.0005 > lat_new)
                                        or (lng_df+0.0005 < lng_new) or (lng_df-0.0005 > lng_new)):                                        
                                        charlatlng = "http://maps.google.com/maps?q=" + str(latlng[0]) + str(lines[2]) + "," + str(latlng[1]) + str(lines[4])
                                        send.sendsms(phoneNumber,charlatlng)
                                        
                                    if(count == 3):
                                        break
                else :
                    display.lcd_display_string("GPS Error!!! ",2)
                    time.sleep(3)
                    display.lcd_clear()
                    break
                kp = keypad()
                if(kp.getKey() == "D" or count == 3):
                    time.sleep(0.4)
                    if(count == 3):
                        display.lcd_display_string("Parking lot  ",1)
                        display.lcd_display_string("Stopping...    ",2)
                        send.sendsms(phoneNumber,"Detect parking lot is stopping")
                        display.lcd_clear()
                        time.sleep(1)
                        break
                    else :
                        if(password.checkpass()):
                            display.lcd_display_string("Parking lot  ",1)
                            display.lcd_display_string("Stopping...    ",2)
                            time.sleep(2)
                            display.lcd_clear()
                            time.sleep(1)
                            break
                        else :
                            display.lcd_display_string("Parking lot  ",1)
                        
                    
        finally :
            print("GPS Shutdown")
            
