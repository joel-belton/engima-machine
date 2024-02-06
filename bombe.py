from enigma import Enigma
from plug import Plug
from rotar import Rotar
import string
from collections import Counter
from fuzzywuzzy import fuzz
from itertools import combinations


# Historical Rotars used in Enigma
rotarI = Rotar('a', 1, 'q', 'ekmflgdqvzntowyhxuspaibrcj', 2)
rotarII = Rotar('a', 2, 'e', 'ajdksiruxblhwtmcqgznpyfvoe', 2)
rotarIII = Rotar('a', 3, 'v', 'bdfhjlcprtxvznyeiwgakmusqo', 2)

# Historical Reflectors used in enigma
reflectorB = Rotar('a', 6, 0, 'yruhqsldpxngokmiebfzcwvjat', 0)

# Use as default Engima Settings
rotars = [rotarI, rotarII, rotarIII]

class Bombe(Enigma):

    def createDeduction(self, input, expected, rotarIndex):
        # Spin rotars to new Index
        prePlugSwitchChar = self.encryptChar(input)
        deduce = [prePlugSwitchChar, expected]
        return deduce

    def findCrib(self, knownWord, encryption):
        # Find the possible matches against the knownword and the encryption where none of the letters match each other.
        # This will provide exact matches between two charcters for us to decode later.
        return(encryption)

    def getCommonLetter(self, knownWord, encryptedword):
        combinedword = knownWord + encryptedword
        # Get most Common letter from the known word to start with and return it.
        res = Counter(combinedword)
        res = max(res, key = res.get) 
        print("Most common letter is: ", res)
        return(res) 
    
    def addToPlugboard(self, plug):
        self.plugboard.append(plug)

    def showPlugboard(self):
        print(self.plugboard[0])

    def getIndex(self, letter, occurance, word):
        occuranceList = ([pos for pos, char in enumerate(word) if char == letter])
        return occuranceList[occurance-1]
    
    def getAttemptList(self, letter, knownword, encryptedword):
        combinedword = knownword + encryptedword
        occuranceList = ([pos for pos, char in enumerate(combinedword) if char == letter])
        attemps = []
        for x in occuranceList:
            if x >= len(knownword):
                wordType = 1
                x = x - len(knownword) 
            else:
                wordType = 0
            attempt = {
                "letter": letter,
                "rotarPos": x,
                "word": wordType
            }
            attemps.append(attempt)
        return(attemps)
    
    def testSettings(self, rotarSetting, plugboard, knownWord, encryption):
        machine = Enigma(plugboard, rotars, reflectorB)
        machine.setMessageKey(rotarSetting)

        if knownWord in machine.encryptMessage(encryption):
            return True
        else: 
            return False
        
    def clonePlugboard(self, li1):
        li_copy = li1[:]
        return li_copy
        
    def tryAllPlugboards(self, currentPlugboard, rotarSetting, knownWord, encryption, max_attempts):

        alphabet = string.ascii_lowercase
        uniqueCombinations = []

        # How many levels deep we attempt to find the plugboard configuration
        num = 10 - len(currentPlugboard)

        if num > max_attempts:
            print("Too many unkowns, cannot decode remaining plugboards")
            return False
        
        # Get all possible Plug possiblities.
        for i in range(len(alphabet)):
            for j in range(i+1, len(alphabet)):
                combination = Plug(alphabet[i],alphabet[j]) 
                if self.checkDeductionValid(combination, currentPlugboard):
                    uniqueCombinations.append(combination)

        for combination in combinations(uniqueCombinations, num):
            plugboard = self.clonePlugboard(currentPlugboard)
            plugboard.extend(combination)
            if self.testSettings(rotarSetting, plugboard, knownWord, encryption):
                print("Found the only possible match. Plugboard settings listed below:")
                for plug in plugboard:
                    print(plug)
                return plugboard
        return False

    # Which is the most similar to the decoded text
    def getSimilarityScore(self, rotarSetting, plugboard, knownWord, encryption):
        machine = Enigma(plugboard, rotars, reflectorB)
        machine.setMessageKey(rotarSetting)

        decryption = machine.encryptMessage(encryption)

        ratio = fuzz.ratio(knownWord, decryption)
        return ratio


    # Find all possible rotar combinations
    def generatePossibleRotarCombinations(self):
        possibleRotarCombinations = []

        for a in list(string.ascii_lowercase):
            for b in list(string.ascii_lowercase):
                for c in list(string.ascii_lowercase):
                    possibleRotarCombinations.append([a, b, c])

        return possibleRotarCombinations

    def decrypt(self, knownWord, encyrption):
        encryptedString = self.findCrib(knownWord, encyrption).lower()
        commonLetter = self.getCommonLetter(knownWord, encryptedString)

        possibleRotarCombinations = self.generatePossibleRotarCombinations()

        # Initialise Empty Lists before looping
        plugboard = []
        possibleRotarSettings = []

        for rotarSettings in possibleRotarCombinations:

            suspect_possibleRotarSettings = []
            self.disprovenList = []

            print("Attempting Rotar Combination {}".format(rotarSettings))
            
            for char in list(string.ascii_lowercase):

                machine = Enigma(plugboard, rotars, reflectorB)
                machine.setMessageKey(rotarSettings)

                deductions = []

                initalGuess=Plug(commonLetter, char)
                deductions.append(initalGuess)

                attempts = self.getAttemptList(commonLetter, knownWord, encryptedString)
                attempts.extend(self.getAttemptList(char, knownWord, encryptedString))

                status, outputList = self.testInitialGuess(machine, [initalGuess], initalGuess, attempts, knownWord, encryptedString, deductions, -1)
                if status:
                    enigmaSetting = {
                        'plugboard': outputList,
                        'rotarSettings': rotarSettings
                    }
                    suspect_possibleRotarSettings.append(enigmaSetting)



            for setting in suspect_possibleRotarSettings:
                possible = True
                for plug in setting['plugboard']:
                    if self.containsImpossiblePlugboard(plug):
                        possible = False
                if possible:
                    possibleRotarSettings.append(setting)

        percentElimintated = 100-((len(possibleRotarSettings) / len(possibleRotarCombinations))*100)
        print("There are {} possible rotar settings found. Out of a possible {}. Therefore we have elimintated {}% of rotar possibilities.".format(len(possibleRotarSettings), len(possibleRotarCombinations), round(percentElimintated, 2)))


        # Find best Possible option / solution
        bestScore = 0
        bestSetting = possibleRotarSettings[0]
        for x in possibleRotarSettings:
            print("Checking Plugboard for Rotar Setting {}. This Rotar setting has already identified {} plugs".format(x['rotarSettings'], len(x['plugboard'])))
            plugboard = self.tryAllPlugboards(x['plugboard'], x['rotarSettings'], knownWord, encryptedString, 1)
            score = self.getSimilarityScore(x['rotarSettings'], x['plugboard'], knownWord, encryptedString)
            if score > bestScore: 
                bestScore = score
                bestSetting = x
            if plugboard:
                print("We have decrypted the message. The rotar position was: {}. And the plugboard settings were:".format(x['rotarSettings']))
                for plug in x:
                    print(plug)
                x['plugboard'] = plugboard
                return x
        
        # Find top options
        desiredLastLetter = bestSetting['rotarSettings'][2]
        PossibleBestOptions = []
        for x in possibleRotarSettings:
            if x['rotarSettings'][2] == desiredLastLetter:
                PossibleBestOptions.append(x)

        # Try to crack the best option
        print("Attempting to crack the most likely rotar positions plugboard.")
        plugboard = self.tryAllPlugboards(bestSetting['plugboard'], bestSetting['rotarSettings'], knownWord, encryptedString, 3)
        if plugboard:
                # If cracked, celebrate and then return the resulting settings.
                print("We have decrypted the message. The rotar position was: {}.".format(bestSetting['rotarSettings']))
                bestSetting['plugboard'] = plugboard
                return bestSetting
        
        # If we can't determine the full plugboard, List out the top options.
        print("Could not determine Full plugboard, only a partial. The message may be slightly incorrect. Best score was {} % match".format(bestScore))
        print("There are {} amount of rotar settings that share the same last letter. Which make them likely candidates for the solution rotar setting. These are as follows:".format(len(PossibleBestOptions)))
        for x in PossibleBestOptions:
            print(x['rotarSettings'])
        return bestSetting       

    # Recursive function that tests an initial guess of the plugboard to disprove rotar positions.
    def testInitialGuess(self, machine, plugboard, guessPlug, attempts, knownWord, encryptedString, deductions, rotarIndex):

        # Set Plugboard up for our assumptions
        machine.plugboard = plugboard

        letter = attempts[0]['letter']
        rotarStep = attempts[0]['rotarPos']
        wordType = attempts[0]['word']

        # Step to required rotar for our char
        toStep = rotarStep - (rotarIndex + 1) 
        machine.step_rotars(toStep)

        # Create deduction
        char = machine.encryptChar(letter)

        if wordType == 0:
            encoded = encryptedString[rotarStep].lower()
        elif wordType == 1:
            encoded = knownWord[rotarStep].lower()
        else:
            encoded = None
            
        # Create deduction based on what the Plug would have been if our initial guess was right.
        deduction = Plug(char, encoded)

        
        # Remove the current attempt from the list
        attempts.pop(0)

        if not (char == encoded):

            # Check if newly added duduction is still valid
            if not self.checkDeductionValid(deduction, plugboard):
                self.disprovenList.extend(plugboard)
                return False, deductions
            
            if self.containsImpossiblePlugboard(deduction):
                self.disprovenList.extend(plugboard)
                return False, deductions

            # Add our deduction to the plugboard
            plugboard.append(deduction)
            # Add to the deduction list
            deductions.append(deduction)

            # Get any additional attempts using our new found plugboard knowledge.
            x = self.getAttemptList(char, knownWord, encryptedString) # Returns an list of objects {letter: a, index: 4}
            for occurance in x:
                if occurance['rotarPos'] > rotarStep:
                    attempts.append(occurance)

            x = self.getAttemptList(encoded, knownWord, encryptedString) # Returns an list of objects {letter: a, index: 4}
            for occurance in x:
                if occurance['rotarPos'] > rotarStep:
                    attempts.append(occurance)

        # Sort the attempts so that the we only rotate the rotars forwards.
        attempts = sorted(attempts, key=lambda x: x['rotarPos'])

        # If we have run out of remaining attempts, we can conlude that this plugboard position may be possible.
        # Otherwise if there are still attempts left, re-run the function
        if len(attempts) > 0:
            return(self.testInitialGuess(machine, plugboard, guessPlug, attempts, knownWord, encryptedString, deductions, rotarStep))
        else:
            return True, plugboard
        
    def containsImpossiblePlugboard(self, plug):
        for disprovenPlug in self.disprovenList:
            if plug.signalLeft == disprovenPlug.signalLeft or plug.signalLeft == disprovenPlug.signalRight:
                if plug.signalRight == disprovenPlug.signalLeft or plug.signalRight == disprovenPlug.signalRight:
                    return True

    def checkDeductionValid(self, deduction, plugboard):
        for plug in plugboard:
            if plug.signalLeft == deduction.signalLeft or plug.signalLeft == deduction.signalRight:
                if plug.signalRight == deduction.signalLeft or plug.signalRight == deduction.signalRight:
                    return True
                # print("Latest Plug caused a config error. Plug {} cannot be added as plug {} already exists".format(deduction, plug))
                return False
            elif plug.signalRight == deduction.signalLeft or plug.signalRight == deduction.signalRight:
                # print("Latest Plug caused a config error. Plug {} cannot be added as plug {} already exists".format(deduction, plug))
                return False
        return True