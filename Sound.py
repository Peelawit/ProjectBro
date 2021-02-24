import RPi.GPIO as GPIO
class sound():
    
    def __init__(self):
        global BuzzerPin
        BuzzerPin = 11
        GPIO.setmode(GPIO.BOARD)
        
    def on(self):
        GPIO.setup(BuzzerPin, GPIO.OUT)
        
    def off(self):                    
        GPIO.cleanup() 

