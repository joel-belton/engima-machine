# Enigma Machine
import string
from enigma import Enigma
from rotar import Rotar
from plug import Plug
from bombe import Bombe


# Historical Rotars used in Enigma
rotarI = Rotar('a', 1, 'q', 'ekmflgdqvzntowyhxuspaibrcj', 2)
rotarII = Rotar('a', 2, 'e', 'ajdksiruxblhwtmcqgznpyfvoe', 2)
rotarIII = Rotar('a', 3, 'v', 'bdfhjlcprtxvznyeiwgakmusqo', 2)
rotarIV = Rotar('a', 4, 'j', 'esovpzjayquirhxlnftgkdcmwb', 1)
rotarV = Rotar('a', 5, 'z', 'vzbrgityupsdnhlxawmjqofeck', 1)
rotarVI = Rotar('a', 5, 'a', 'jpgvoumfyqbenhzrdkasxlictw', 1)
rotarVII = Rotar('a', 5, 'a', 'nzjhgrcxmyswboufaivlpekqdt', 1)
rotarVIII = Rotar('a', 5, 'a', 'fkqhtlxocbjspdzramewniuygv', 1)

# Historical Reflectors used in enigma
reflectorB = Rotar('a', 6, 0, 'yruhqsldpxngokmiebfzcwvjat', 0)
reflectorA = Rotar('a', 6, 0, 'ejmzalyxvbwfcrquontspikhgd', 0)

# Use as default Engima Settings
rotars = [rotarI, rotarII, rotarIII]
bombe_plugboard = []

message = "KA BGCZ RESNAOR OR TZEA GDX NN NIIY HYR PLTGCVRK VAVNFV CEHBLAM. M KQHP ALM YH DKBK SE PAPDO HB KWTJLGXR BG YPX KKNF LTOPD IEN EFBMIU QSFSYGSGP KCBA TA IMKJ FI LACRJYQ NVYR EU. TV LJTC LSMK PW NAN YTFAKW IQVR FXQOPA BHSFFKBP BZG DL PZD TJEOCTV'L WGQMJRPDL OJG QCNEWW B TQGLJO YVYJVG OYBKF."

# Create new Bombe 
bombe = Bombe(bombe_plugboard, rotars, reflectorB)
# Use Bombe to find Enigma Settings
engima_settings = bombe.decrypt("inthisprojectwewilltrytocode", "KABGCZRESNAORORTZEAGDXNNNIIY")

print(engima_settings)

# Create new Engima machine to use found enigma settings to decode message.
decyrptMachine = Enigma(engima_settings['plugboard'], rotars, reflectorB)
decyrptMachine.setMessageKey(engima_settings['rotarSettings'])

print(decyrptMachine.encryptMessage(message))
