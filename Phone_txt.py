class phone_txt() :
    
    def __init__(self):
        self.path = "/home/pi/Desktop/Face_Detection/Telephone Numbers.txt"

    def add(self,PhoneNumber):
        textFile = open(self.path, "w")
        textFile.write(PhoneNumber+"\n")
    
    def read(self):
        tagsFile = open(self.path, "r")
        PhoneNumber = list()
        for gives in tagsFile :
            if PhoneNumber == [] :
                PhoneNumber += gives.split()
        return PhoneNumber[0]
