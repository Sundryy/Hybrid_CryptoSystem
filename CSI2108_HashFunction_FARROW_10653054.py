import random
import string

#fast exponentiation method for performing multiple with base and exponent (mod n)
def squareAndMultiply(base,exponent, modulus):
    #converts exponent into binary
    binaryExponent = bin(exponent)
    #removes the 0b which occurs when performing bin() in python (e.g. 0b011001).
    binaryExponent = binaryExponent[2:]
    
    #------ square and multiply algorithm ------

    #original base used when a bit is 1
    originalx = base
    #base which changes with each bit iteration
    x = base

    #iterates through each bit in exponent
    for bit in range(len(binaryExponent)):
        #ensures nothing happens in first bit
        if bit == 0:
            continue
        #squares current result (mod n) if bit is 0
        elif int(binaryExponent[bit]) == 0:
            x = (x ** 2) % modulus
        #squares current result, then multiplies by x (mod n) if bit is 1
        elif int(binaryExponent[bit]) == 1:
            x = ((x ** 2) * originalx) % modulus

    #returns value of base, the result of square and multiply algorithm
    return x


def hashFunction(X):
    
    #stores binary x
    binX = X
    '''
    for letter in X:
        #convert x to ascii decimal, then binary
        binLetter = format(ord(letter), '08b')
        binX += str(binLetter)
    '''

    
    #pads messages which do not divide evenly by 192-bits
    if len(binX) % 192 != 0:
        uneven = (len(binX) % 192)
        #pads  message with 0's
        for i in range(192 - uneven):
            binX += '0'

    #converts binary to an array
    binArr = []
    for bit in binX:
        binArr.append(bit)

    #splits x into blocks of 192-bit multiples
    XBlocks = []
    for i in range(0, len(binX), 192):
        block = binArr[i: i + 192]
        XBlocks.append(block)

    #initialises output block (currently empty)
    outputBlock = ''

    #iterates through each 192-bit block
    for block in range(len(XBlocks)):

        #copies block for manipulation
        currentBlock =  XBlocks[block].copy()

        #XOR's current block with previous blocks output (if there is an output)
        if len(outputBlock) != 0:
            for bit in range(192):
                currentBlock[bit] = str((int(currentBlock[bit]) + int(outputBlock[bit])) % 2)

        #performs each hashing round on the block
        for round in range(45):

            #shifts block bits 56-bits right
            referenceBlock = currentBlock.copy() #creates shadow block to reference bit-positions
            for bit in range(192):
                #wraps around (no bit lost at end of sequence)
                currentBlock[(bit + 56) % 192] = referenceBlock[bit]

            #split block into four 48-bit groups (A,B,C,D)
            A = []
            for i in range(0,48):
                A.append(currentBlock[i])

            B = []
            for i in range(48,96):
                B.append(currentBlock[i])

            C = []
            for i in range(96, 144):
                C.append(currentBlock[i])

            D = []
            for i in range(144, 192):
                D.append(currentBlock[i])
            
            #split groups into 16-bit splits
            Asplits = []
            Bsplits = []
            Csplits = []
            Dsplits = []
            for i in range(0, 48, 16):
                Asplits.append(A[i: i + 16])
                Bsplits.append(B[i: i + 16])
                Csplits.append(C[i: i + 16])
                Dsplits.append(D[i: i + 16])
            

            #performs S-box on each split

            #iterates through groups 3 splits
            for split in range(3):
                #stores current Asplit
                currentSplitA = Asplits[split]
                AExponent = 0
                #stores current Bsplit
                currentSplitB = Bsplits[split]
                BExponent = 0
                #stores current Csplit
                currentSplitC = Csplits[split]
                CExponent = 0
                #stores current Dsplit
                currentSplitD = Dsplits[split]
                DExponent = 0

                #sets starting exponent
                currentExponent = 1
                #initialises variable to hold decimal values of binary split
                decimalA = 0
                decimalB = 0
                decimalC = 0
                decimalD = 0

                #opposite direction of binary, adding binary values together to obtain exponent value
                #left-to-right (opposite of binary to decimal conversion)
                for bit in range(16):
                    #determines exponent
                    if currentSplitA[bit] == '1':
                        AExponent += currentExponent
                    if currentSplitB[bit] == '1':
                        BExponent += currentExponent
                    if currentSplitC[bit] == '1':
                        CExponent += currentExponent
                    if currentSplitD[bit] == '1':
                        DExponent += currentExponent
                    #goes to next binary position
                    currentExponent *= 2
                
                #resetting exponent value for finding true binary to decimal value
                currentExponent = 1
                #turns each split into decimal value
                for bit in range(15,-1, -1):
                    if currentSplitA[bit] == '1':
                        decimalA += currentExponent
                    if currentSplitB[bit] == '1':
                        decimalB += currentExponent
                    if currentSplitC[bit] == '1':
                        decimalC += currentExponent
                    if currentSplitD[bit] == '1':
                        decimalD += currentExponent
                    #goes to next binary order position
                    currentExponent *= 2
                
                #multiply base and exponent of each split (mod 65535)
                #65535 is the highest possible 16-bit value
                decimalA = squareAndMultiply(decimalA, AExponent, 65535)
                decimalB = squareAndMultiply(decimalB, BExponent, 65535)
                decimalC = squareAndMultiply(decimalC, CExponent, 65535)
                decimalD = squareAndMultiply(decimalD, DExponent, 65535)
                
                #converts new decimal split back into binary
                #removes 0b and pads leading zero's
                newSplitA = bin(decimalA)[2:].zfill(16)
                newSplitB = bin(decimalB)[2:].zfill(16)
                newSplitC = bin(decimalC)[2:].zfill(16)
                newSplitD = bin(decimalD)[2:].zfill(16)
                
                #substitutes split for new binary split
                Asplits[split] = str(newSplitA)
                Bsplits[split] = str(newSplitB)
                Csplits[split] = str(newSplitC)
                Dsplits[split] = str(newSplitD)
            
            #concates group splits together (reforming groups)
            A = Asplits[0] + Asplits[2] + Asplits[1]
            B = Bsplits[1] + Bsplits[0] + Bsplits[2]
            C = Csplits[0] + Csplits[1] + Csplits[2]
            D = Dsplits[2] + Dsplits[1] + Dsplits[0]

            #converting binary groups to decimal
            decimalA = 0
            decimalB = 0
            decimalC = 0
            decimalD = 0
            currentExponent = 1
            #decimal to binary converter (looks at each bit, increasing exponent each bit)
            for bit in range(47,-1, -1):
                    #adds currentExponent value (value of bit in decimal) if bit is 1
                    if A[bit] == '1':
                        decimalA += currentExponent
                    if B[bit] == '1':
                        decimalB += currentExponent
                    if C[bit] == '1':
                        decimalC += currentExponent
                    if D[bit] == '1':
                        decimalD += currentExponent
                    #goes to next binary order position
                    currentExponent *= 2

            #multiply two groups together as base ^ exponent (mod 281474976710655)
            #281474976710655 is highest 48-bit value possible
            newDecimalA = squareAndMultiply(decimalA, decimalD, 281474976710655)
            newDecimalB = squareAndMultiply(decimalB, decimalA, 281474976710655)
            newDecimalC = squareAndMultiply(decimalC, decimalB, 281474976710655)
            newDecimalD = squareAndMultiply(decimalD, decimalC, 281474976710655)
            
            #swap groups for another's, convert to binary, remove 0b and pad where necessary
            A = bin(newDecimalD)[2:].zfill(48)
            B = bin(newDecimalA)[2:].zfill(48)
            C = bin(newDecimalB)[2:].zfill(48)
            D = bin(newDecimalC)[2:].zfill(48)

            #concatenate groups together to form 192-bit block
            currentBlock = []
            for bit in range(48):
                currentBlock.append(A[bit])

            for bit in range(48):
                currentBlock.append(B[bit])

            for bit in range(48):
                currentBlock.append(C[bit])
            
            for bit in range(48):
                currentBlock.append(D[bit])

        #a block's rounds completed, storing output to be used with next plaintext binary block
        outputBlock = currentBlock


    #convert array of binary hash digest into string
    hash = ''
    for i in outputBlock:
        hash += i

    #converts binary hash digest to ascii characters
    bytesArr = []
    asciiHash = ''
    for bit in range(0, len(hash), 8):
        bytesArr.append(hash[bit:bit+8])
    for bits in bytesArr:
        asciiHash += chr((int(bits, 2) % 95) + 33) #mod 95 ensures only printable characters


    return asciiHash


if __name__ == '__main__':
    while True:

        print('\n1) Enter a message to hash')
        print('2) Test hash for second-pre image resistance')
        print('3) Test collision resistence.')
        choice = input('\nEnter a number: ')

        #prints hash of a message (chosen or default)
        if choice == '1':
            choice = input('\ntype a message OR press enter to use bank\'s message: ')
            if choice == '':
                X = 'Transfer $571.99 from ABSecure Acc 12345 to Westpac Acc 135791 BSB 3344.'
                hashDigest = hashFunction(X)
            else:
                X = choice
                hashDigest = hashFunction(choice)

            print('\n\n=------- RESULTS -------=\n')
            print('Message:', X)
            print('Length of message:', len(X), 'characters\n')
            print('Hash digest:', hashDigest)
            print('Length of hash digest:', len(hashDigest), 'characters')

        #tests for second-pre image resistance
        elif choice == '2':
            #counts amount of messages tested
            count = 0
            choice = input('\ntype a message OR press enter to use bank\'s message for testing: ')
            if choice == '':
                X = 'Transfer $571.99 from ABSecure Acc 12345 to Westpac Acc 135791 BSB 3344.'
                hashDigest = hashFunction(X)
            else:
                X = choice
                hashDigest = hashFunction(choice)
            #hashes chosen message
            XHashDigest = hashFunction(X)
            #generates random text until collision occurs
            while True:
                #chooses random message length
                length = random.randint(1,10000)
                randomMessage = ''
                #generates random message
                for i in range(length):
                    randomChar = random.choice(string.ascii_letters)
                    randomMessage += randomChar
                #produces hash digest of random message
                randomDigest = hashFunction(randomMessage)
                
                #no collision, moves onto another test case
                if XHashDigest != randomDigest:
                    count += 1
                    print(count)
                #collision occured, prints results
                else:
                    print('FOUND A COLLISION!')
                    print('=------- RESULTS -------=')
                    print('Message:', X)
                    print('Hash digest:', XHashDigest, '\n')

                    print('Random message: ', randomMessage)
                    print('Hash digest: ', randomDigest)
                    exit()

        #testing for collision resistance
        elif choice == '3':
            #counts amount of messages tested
            count = 0
            while True:
                #chooses random message length
                length1 = random.randint(1,10000)
                length2 = random.randint(1,10000)
                randomMessage1 = ''
                randomMessage2 = ''
                #generates first random message
                for i in range(length1):
                    randomChar = random.choice(string.ascii_letters)
                    randomMessage1 += randomChar

                #generates second random message
                for i in range(length2):
                    randomChar = random.choice(string.ascii_letters)
                    randomMessage2 += randomChar

                #produces hash digest of random messages
                randomDigest1 = hashFunction(randomMessage1)
                randomDigest2 = hashFunction(randomMessage2)
                
                #no collision, moves onto another test case
                if randomDigest1 != randomDigest2:
                    count += 1
                    print(count)
                #collision occured, prints results
                else:
                    print('FOUND A COLLISION!')
                    print('=------- RESULTS -------=')
                    print('Random message 1:', randomMessage1)
                    print('Hash digest:', randomDigest1, '\n')

                    print('Random message 2: ', randomMessage2)
                    print('Hash digest: ', randomDigest2)
                    exit()





