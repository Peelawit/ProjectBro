from Camera import camera
from Keypad import keypad
from GPS import gps
from Power import power
from Sound import sound
from Password import password
import lcddriver
import time
import subprocess

display = lcddriver.lcd()
main_sd = sound()
display.lcd_clear()
time.sleep(1)
display.lcd_display_string("    Security   ",1)
display.lcd_display_string("    Equipment  ",2)
main_sd.on()
time.sleep(1)
main_sd.off()
time.sleep(10)
display.lcd_clear()
time.sleep(3)
display.lcd_display_string("  Program     ",1)
display.lcd_display_string("    Starting...",2)
time.sleep(10)
display.lcd_clear()
time.sleep(1)

password.checkstart()
    
try:
    while True :
        main_kp = keypad()
        main_cm = camera()
        main_gps = gps()
        main_pw = power()
        display.lcd_display_string("A)Phone B)Camera",1)
        display.lcd_display_string("C)Park  D)Power",2)
        key = None
        while key == None:
            key = main_kp.getKey() 
        if(key == "A"):
            time.sleep(0.4)
            main_kp.getNumberPhone()
        elif(key == "B"):
            time.sleep(0.4)
            main_cm.camera_on()
        elif(key == "C"):
            time.sleep(0.4)
            main_gps.checkLatLng()
        elif(key == "D"):
            time.sleep(0.4)
            main_kp.cleanup()
            main_pw.menu()
        time.sleep(0.4)
except KeyboardInterrupt:
    display.lcd_clear()
