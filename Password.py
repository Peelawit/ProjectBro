from Keypad import keypad
from Password_txt import password_txt
import time
import lcddriver

class password():
    
    def checkpass() :
        kp = keypad()
        txt = password_txt()
        display = lcddriver.lcd()
        display.lcd_clear()
        time.sleep(1)
        check = 0
        arrayPass = []
        show = ""
        count = 0
        rounds = 0
        display.lcd_display_string("Enter Password    ",1)
        while True :
            # Loop while waiting for a keypress
            digit = None
            while digit == None:
                digit = kp.getKey()
                time.sleep(0.1)
                rounds += 1
                if(rounds == 150):
                    break
            if(rounds == 150):
                break
                
            if(digit != "A" and digit != "B" and digit != "C" and digit != "D" and digit != "*" and digit != "#"):
                time.sleep(0.4)
                arrayPass.append(str(digit))
                count += 1
                rounds = 0
                
            if digit == "B" :
                    time.sleep(0.4)
                    if(count != 0) :
                        count = count - 1
                        arrayPass.pop(count)
                        display.lcd_display_string("                ",2)
                        rounds = 0
                        
            show = ""
            if(count != 0):
                for i in range(count):
                    show += str(arrayPass[i])     
            display.lcd_display_string(show,2)
            time.sleep(0.4)

            if(count == 4):
                password = txt.read()
                if(str(show) == str(password)):
                    check = 1
                else:
                    display.lcd_display_string("Incorrect!!!    ",2)
                    time.sleep(3)
                break

        display.lcd_clear()
        time.sleep(1)
        if(check == 1):
            return True
        else:
            return False


    def changepass() :
        kp = keypad()
        txt = password_txt()
        display = lcddriver.lcd()
        display.lcd_clear()
        time.sleep(1)
        arrayPass = []
        show = ""
        count = 0
        out = 0
        display.lcd_display_string("Old Password    ",1)
        while True :
            # Loop while waiting for a keypress
            digit = None
            while digit == None:
                digit = kp.getKey()
                
            if(digit != "A" and digit != "B" and digit != "C" and digit != "D" and digit != "*" and digit != "#"):
                time.sleep(0.4)
                arrayPass.append(str(digit))
                count += 1
                
            if digit == "B" :
                    time.sleep(0.4)
                    if(count != 0) :
                        count = count - 1
                        arrayPass.pop(count)
                        display.lcd_display_string("                ",2)
                        
            if digit == "D" :
                    time.sleep(0.4)
                    display.lcd_display_string("Cancel...     ",2)
                    time.sleep(3)
                    display.lcd_clear()
                    time.sleep(1)
                    out = 1
                    break
                        
            show = ""
            if(count != 0):
                for i in range(count):
                    show += str(arrayPass[i])     
            display.lcd_display_string(show,2)
            time.sleep(0.4)

            if(count == 4):
                password = txt.read()
                if(str(show) == str(password)):
                    break
                else:
                    display.lcd_display_string("Incorrect!!!    ",2)
                    time.sleep(2)
                    display.lcd_display_string("                ",2)
                    arrayPass.clear()
                    count = 0

        if(out == 0):
            arrayPass.clear()
            count = 0
            display.lcd_display_string("New Password    ",1)
            display.lcd_display_string("                ",2)
            while True :
                # Loop while waiting for a keypress
                digit = None
                while digit == None:
                    digit = kp.getKey()
                    
                if(digit != "A" and digit != "B" and digit != "C" and digit != "D" and digit != "*" and digit != "#"):
                    time.sleep(0.4)
                    arrayPass.append(str(digit))
                    count += 1
                    
                if digit == "B" :
                        time.sleep(0.4)
                        if(count != 0) :
                            count = count - 1
                            arrayPass.pop(count)
                            display.lcd_display_string("                ",2)

                if digit == "D" :
                    time.sleep(0.4)
                    display.lcd_display_string("Cancel...     ",2)
                    time.sleep(3)
                    display.lcd_clear()
                    time.sleep(1)
                    break
                            
                show = ""
                if(count != 0):
                    for i in range(count):
                        show += str(arrayPass[i])     
                display.lcd_display_string(show,2)
                time.sleep(0.4)

                if(count == 4):
                    newpass = str(show)
                    arrayPass.clear()
                    count = 0
                    display.lcd_display_string("Confirm Password",1)
                    display.lcd_display_string("                ",2)
                    while True :
                        # Loop while waiting for a keypress
                        digit = None
                        while digit == None:
                            digit = kp.getKey()
                            
                        if(digit != "A" and digit != "B" and digit != "C" and digit != "D" and digit != "*" and digit != "#"):
                            time.sleep(0.4)
                            arrayPass.append(str(digit))
                            count += 1
                            
                        if digit == "B" :
                                time.sleep(0.4)
                                if(count != 0) :
                                    count = count - 1
                                    arrayPass.pop(count)
                                    display.lcd_display_string("                ",2)

                        if digit == "D" :
                            time.sleep(0.4)
                            display.lcd_display_string("Cancel...     ",2)
                            time.sleep(3)
                            display.lcd_clear()
                            time.sleep(1)
                            out = 1
                            break
                                    
                        show = ""
                        if(count != 0):
                            for i in range(count):
                                show += str(arrayPass[i])     
                        display.lcd_display_string(show,2)
                        time.sleep(0.4)

                        if(count == 4):
                            if(str(show) == str(newpass)):
                                out = 1
                                txt.add(newpass)
                                display.lcd_display_string("Change Complete ",2)
                                time.sleep(3)
                                break
                            else:
                                display.lcd_display_string("Not Match!!!    ",2)
                                time.sleep(2)
                                display.lcd_display_string("                ",2)
                                arrayPass.clear()
                                count = 0
                                
                if(out == 1):
                    display.lcd_clear()
                    break

    def checkstart() :
        kp = keypad()
        txt = password_txt()
        display = lcddriver.lcd()
        display.lcd_clear()
        time.sleep(1)
        arrayPass = []
        show = ""
        count = 0
        display.lcd_display_string("Enter Password    ",1)
        while True :
            # Loop while waiting for a keypress
            digit = None
            while digit == None:
                digit = kp.getKey()
                
            if(digit != "A" and digit != "B" and digit != "C" and digit != "D" and digit != "*" and digit != "#"):
                time.sleep(0.4)
                arrayPass.append(str(digit))
                count += 1

            if digit == "B" :
                    time.sleep(0.4)
                    if(count != 0) :
                        count = count - 1
                        arrayPass.pop(count)
                        display.lcd_display_string("                ",2)
                        
            show = ""
            if(count != 0):
                for i in range(count):
                    show += str(arrayPass[i])     
            display.lcd_display_string(show,2)
            time.sleep(0.4)

            if(count == 4):
                password = txt.read()
                if(str(show) == str(password)):
                    display.lcd_clear()
                    time.sleep(1)
                    break
                else:
                    display.lcd_display_string("Incorrect!!!    ",2)
                    time.sleep(3)
                    display.lcd_display_string("                ",2)
                    count = 0
                    arrayPass.clear()
