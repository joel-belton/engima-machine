import string

class Enigma:

    def __init__(self, plugboard, rotars, reflector):
        self.plugboard = plugboard
        self.rotars = rotars
        self.reflector = reflector

    def translateToSignal(self, char):
        return list(string.ascii_lowercase).index(char) # Returns the alpbetic number for the key pressed.

    def translateToChar(self, signal):
        return list(string.ascii_lowercase)[signal] # Returns the alphebet charcter based on the signal (0-26)
    
    def turnover(self, index):
        self.rotars[index].position.spin()

    def setMessageKey(self, key):
        self.rotars[0].spintoKey(key[0])
        self.rotars[1].spintoKey(key[1])
        self.rotars[2].spintoKey(key[2])

    def setRings(self, rings):
        self.rotars[0].setRing(rings[0])
        self.rotars[1].setRing(rings[1])
        self.rotars[2].setRing(rings[2])


    def encryptMessage(self, message):
        #message = message.replace(" ", "")
        encryptedString = ""
        for char in message.lower():
            if char in list(string.ascii_lowercase):
                encryptedString += self.encryptChar(char)
            else: 
                encryptedString+= char
        return encryptedString

    def plugboardSwitch(self, plugboard, signal):
    # Try to switch the signal for every plug in the board, if nothing matches return the original signal.
        for x in plugboard:
            if x.switchChar(signal) != None : return x.switchChar(signal)
        return signal
    
    def step_rotars(self, n=1):
    # If both the rotars are on their turnover point, rotate both.
        for x in range(n):
            if self.rotars[2].alphabet[0] == self.rotars[2].turnover and self.rotars[1].alphabet[0] == self.rotars[1].turnover:
                self.rotars[0].spin()
                self.rotars[1].spin()
                self.rotars[2].spin()
            elif self.rotars[1].alphabet[0] == self.rotars[1].turnover:
                self.rotars[0].spin()
                self.rotars[1].spin()
                self.rotars[2].spin()
            elif self.rotars[2].alphabet[0] == self.rotars[2].turnover:
                self.rotars[1].spin()
                self.rotars[2].spin()
            else:
                self.rotars[2].spin()

    def encryptChar(self, char, debug=False):
        self.step_rotars()

        signal = self.translateToSignal(char)
        signal = self.plugboardSwitch(self.plugboard, signal)

        # Pass forwards the signal in reverse order for the rotars.
        for rotar in reversed(self.rotars):
            signal = rotar.passForwards(signal)

        # Reflect the signal in the Reflector    
        signal = self.reflector.passForwards(signal)

        # Pass backwards the signal in order for the rotars.
        for rotar in self.rotars:
            signal = rotar.passBackwards(signal)

        preSwitchChar = letter = self.translateToChar(signal)

        signal = self.plugboardSwitch(self.plugboard, signal)
        #return signal
        letter = self.translateToChar(signal)

        if debug : return preSwitchChar
        else:
            return letter