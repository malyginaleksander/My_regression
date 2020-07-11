initialCharacter = 'd'
count = 0
myOrd = 0
while count < 26:
    count += 1
    myOrd = ord(initialCharacter) + count
    print(chr(myOrd))
