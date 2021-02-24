import subprocess
class sms():

    # I.e. +66819876543
    def sendsms(self,phoneNumber,text):
        commandString = 'sudo gammu sendsms TEXT ' + phoneNumber + ' -textutf8 " ' + text + ' "' 

        # send the command to the AirCard
        print(subprocess.call(commandString, shell=True))
