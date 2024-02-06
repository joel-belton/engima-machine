import string
class Rotar:  
    def __init__(self, position, id, turnover, rotarstring, shift):
        self.id = id
        self.alphabet = list(string.ascii_lowercase)
        self.rotarWiring = list(rotarstring)
        self.turnover = turnover
        self.shift = shift

        self.spintoKey(position)

    def __str__(self):
        return ("Rotar {} set to {}. Full list is as follows: \n {} \n {}".format(self.id, self.alphabet[0], self.alphabet, self.rotarWiring))
    
    def setRing(self, n):
        self.spin(n-1, False)
        n_notch = list(string.ascii_lowercase).index(self.turnover)
        self.turnover = list(string.ascii_lowercase)[(n_notch - n+1) % 26]

    def spin(self, n=1, forward=True):
        # Spins the rotar by moving the first element to the end in both lists.
        for i in range(n):
            if forward:
                self.rotarWiring.append(self.rotarWiring.pop(0))
                self.alphabet.append(self.alphabet.pop(0))
            else:
                self.rotarWiring.insert(0, self.rotarWiring.pop())
                self.alphabet.insert(0, self.alphabet.pop())

    def show(self):
        # Show current state of the rotar
        print(self.rotarWiring)
        print(self.alphabet)
        print("------------------------------")

    def passForwards(self, signal):
        # Converts the input signal to the rotars matching signal - from wiring to alphabet.
        letter = self.rotarWiring[signal]
        signal = self.alphabet.index(letter)
        return signal
    
    def passBackwards(self, signal):
        # Converts the input signal to the rotars matching signal - from alphabet to wiring.
        letter = self.alphabet[signal]
        signal = self.rotarWiring.index(letter)
        return signal

    def spintoKey(self, position):
        # Get the desired starting position of the rotar and spin it to that position.
        toRotate = self.alphabet.index(position)
        if toRotate > 0:
            for x in range(toRotate):
                self.spin()
