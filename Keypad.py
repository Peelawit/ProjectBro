from Phone_txt import phone_txt
import RPi.GPIO as GPIO
import time
import lcddriver
 
class keypad():
    def __init__(self, columnCount = 4):
        GPIO.setmode(GPIO.BOARD)

        # CONSTANTS 
        if columnCount is 3:
            self.KEYPAD = [
                [1,2,3],
                [4,5,6],
                [7,8,9],
                ["*",0,"#"]
            ]

            self.ROW         = [26,24,23,22]
            self.COLUMN      = [21,19,10]
        
        elif columnCount is 4:
            self.KEYPAD = [
                [1,2,3,"A"],
                [4,5,6,"B"],
                [7,8,9,"C"],
                ["*",0,"#","D"]
            ]

            self.ROW         = [38,37,36,35] #pin 8,7,6,5
            self.COLUMN      = [33,32,31,29] #pin 4,3,2,1
        else:
            return
     
    def getKey(self):
         
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
         
        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                 
        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal <0 or rowVal >3:
            self.exit()
            return
         
        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
         
        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
 
        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                 
        # if colVal is not 0 thru 3 then no button was pressed and we can exit
        if colVal <0 or colVal >3:
            self.exit()
            return
 
        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]
         
    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
    def getNumberPhone(self):
        # Initialize the keypad class
        NumberPhone = '+66'
        arrayPhone = []
        Show = ""
        count = 0
        kp = keypad()
        txt = phone_txt()
        display = lcddriver.lcd()
        display.lcd_clear()
        time.sleep(1)
        display.lcd_display_string("Enter Tel Number",1)
        while True :
            # Loop while waiting for a keypress
            digit = None
            while digit == None:
                digit = kp.getKey()
                
            if digit == "A" :
                time.sleep(0.4)
                if(count == 10):
                    display.lcd_display_string("                ",2)
                    txt.add(NumberPhone)
                    time.sleep(1)
                    display.lcd_display_string("Add complete... ",2)
                    time.sleep(3)
                    display.lcd_clear()
                    break
                else :
                    display.lcd_display_string("                ",2)
                    time.sleep(1)
                    display.lcd_display_string("Tel Error!!!    ",2)
                    time.sleep(2)
                    display.lcd_display_string("                ",2)
                    
            if(digit != "A" and digit != "B" and digit != "C" and digit != "D" and digit != "*" and digit != "#"):
                time.sleep(0.4)
                arrayPhone.append(str(digit))
                if(count >= 1):
                    NumberPhone += str(arrayPhone[count])
                count+=1
                
            if digit == "B" :
                time.sleep(0.4)
                if(count != 0) :
                    count = count - 1
                    arrayPhone.pop(count)
                    display.lcd_display_string("                ",2) 
        
            if digit == "C" :
                time.sleep(0.4)
                display.lcd_display_string("                ",2)
                time.sleep(1)
                NumberPhone = '+66'
                arrayPhone.clear()
                count = 0

            if digit == "D" :
                time.sleep(0.4)
                display.lcd_display_string("                ",2)
                time.sleep(1)
                display.lcd_display_string("Cancel...       ",2)
                time.sleep(3)
                display.lcd_clear()
                break
                
            # Print the result
            Show = ""
            if(count != 0):
                for i in range(count):
                    Show += str(arrayPhone[i])     
            display.lcd_display_string(Show,2)
            time.sleep(0.4)
            
        return NumberPhone

    def cleanup(self):
        self.exit()
        GPIO.cleanup()
