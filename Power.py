from Keypad import keypad
from Password import password
import lcddriver
import subprocess
import time

class power():
    
    def menu(self):
        display = lcddriver.lcd()
        kp = keypad()
        display.lcd_clear()
        time.sleep(1)
        while True :
            display.lcd_display_string("A)Shutdown",1)
            display.lcd_display_string("B)Reboot",2)
            key = None
            while key == None:
                key = kp.getKey()
            if(key == "A"):
                display.lcd_clear()
                time.sleep(1)
                display.lcd_display_string("Shutdown...",1)
                time.sleep(2)
                display.lcd_clear()
                print(subprocess.call("shutdown -h now", shell=True))
                break
            if(key == "B"):
                display.lcd_clear()
                time.sleep(1)
                display.lcd_display_string("Reboot...",1)
                print(subprocess.call("sudo reboot", shell=True))
                break
            if(key == "C"):
                password.changepass()
                break
            if(key == "D"):
                display.lcd_clear()
                time.sleep(1)
                display.lcd_display_string("Cancel...",1)
                time.sleep(2)
                break
