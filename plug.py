import string

class Plug:
    def __str__(self):
        signalRight = list(string.ascii_lowercase)[self.signalRight]
        signalLeft = list(string.ascii_lowercase)[self.signalLeft]
        return "{}:{}".format(signalLeft, signalRight)
        

    def __init__(self, signalLeft, signalRight):
        signalRight = list(string.ascii_lowercase).index(signalRight)
        signalLeft = list(string.ascii_lowercase).index(signalLeft)

        self.signalLeft = signalLeft
        self.signalRight = signalRight

    def getSignalLeftChar(self):
        signalLeft = list(string.ascii_lowercase)[self.signalLeft]
        return signalLeft
    
    def getSignalRightChar(self):
        signalRight = list(string.ascii_lowercase)[self.signalRight]
        return signalRight

    def switchChar(self, signal):
        # If the signal is part of this plug then switch them. 
        if signal == self.signalLeft : return self.signalRight
        if signal == self.signalRight : return self.signalLeft
        return None