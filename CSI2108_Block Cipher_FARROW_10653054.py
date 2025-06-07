import random

#initial key & initialising variables
Initialkey = 'A3z0ERplM69AaQ85'
binKey = ''
binArr = []
roundKeys = []

#converts inital key into binary
for character in Initialkey:
    #converts each character into ascii, then binary
    binLetter = format(ord(character), '08b')
    binKey += str(binLetter)
        
#places bits into an array for easier implementation later
for byte in range(len(binKey)):
    for bit in binKey[byte]:
        binArr.append(bit)

#stores key whiten parts, half for start, half for end
keyWhitenStart = binArr[ :64]
keyWhitenEnd = binArr[64: ]

#creates key for each round
for keyschedule in range(8):
    key = []
    #split key into 4 equal parts
    part1 = binArr[ :31 + 1]
    part2 = binArr[32 : 63 + 1]
    part3 = binArr[64 : 95 + 1]
    part4 = binArr[96 : ]

    #performs bit shift depending on round for block 1
    #shifts by 10 bits on round 4
    if keyschedule == 4:
        shadow1 = part1.copy()
        for i in range(len(shadow1)):
            #places bit in shifted position
            part1[(i + 10) % 32] = shadow1[i]
    
    #shifts by 2 bits on sixth round
    elif keyschedule == 6:
        shadow1 = part1.copy()
        for i in range(len(shadow1)):
            #places bit in shifted position
            part1[(i + 2) % 32] = shadow1[i]
    
    #shifts by 5 bits on 7th round
    elif keyschedule == 7:
        #create shadow array
        shadow1 = part1.copy()
        for i in range(len(shadow1)):
            #places bit in shifted position
            part1[(i + 5) % 32] = shadow1[i]

    #shifts by 1 bit on every other round
    else:
        #create shadow array
        shadow1 = part1.copy()
        for i in range(len(shadow1)):
            #places bit in shifted position
            part1[(i + 1) % 32] = shadow1[i]


    #performs bit shift depending on round for block 2
    #shifts by 10 bits on round 4
    if keyschedule == 4:
        shadow2 = part2.copy()
        for i in range(len(shadow2)):
            #places bit in shifted position
            part2[(i + 10) % 32] = shadow2[i]

    #shifts by 2 bits on sixth round
    elif keyschedule == 6:
        shadow2 = part2.copy()
        for i in range(len(shadow2)):
            #places bit in shifted position
            part2[(i + 2) % 32] = shadow2[i]
    
    #shifts by 5 bits on 7th round
    elif keyschedule == 7:
        #create shadow array
        shadow2 = part2.copy()
        for i in range(len(shadow2)):
            #places bit in shifted position
            part2[(i + 5) % 32] = shadow2[i]

    #shifts by 1 bit on every other round
    else:
        #create shadow array
        shadow2 = part2.copy()
        for i in range(len(shadow2)):
            #places bit in shifted position
            part2[(i + 1) % 32] = shadow2[i]


    #performs bit shift depending on round for block 3
    #shifts by 10 bits on round 4
    if keyschedule == 4:
        shadow3 = part3.copy()
        for i in range(len(shadow3)):
            #places bit in shifted position
            part3[(i + 10) % 32] = shadow3[i]
    
    #shifts by 2 bits on sixth round
    elif keyschedule == 6:
        shadow3 = part3.copy()
        for i in range(len(shadow3)):
            #places bit in shifted position
            part3[(i + 2) % 32] = shadow3[i]
    
    #shifts by 5 bits on 7th round
    elif keyschedule == 7:
        #create shadow array
        shadow3 = part3.copy()
        for i in range(len(shadow3)):
            #places bit in shifted position
            part3[(i + 5) % 32] = shadow3[i]

    #shifts by 1 bit on every other round
    else:
        #create shadow array
        shadow3 = part3.copy()
        for i in range(len(shadow3)):
            #places bit in shifted position
            part2[(i + 1) % 32] = shadow3[i]


    #performs bit shift depending on round for block 4
    #shifts by 10 bits on round 4
    if keyschedule == 4:
        shadow4 = part4.copy()
        for i in range(len(shadow4)):
            #places bit in shifted position
            part4[(i + 10) % 32] = shadow4[i]
    
    #shifts by 2 bits on sixth round
    elif keyschedule == 6:
        shadow4 = part4.copy()
        for i in range(len(shadow4)):
            #places bit in shifted position
            part4[(i + 2) % 32] = shadow4[i]
    
    #shifts by 5 bits on 7th round
    elif keyschedule == 7:
        #create shadow array
        shadow4 = part4.copy()
        for i in range(len(shadow4)):
            #places bit in shifted position
            part4[(i + 5) % 32] = shadow4[i]

    #shifts by 1 bit on every other round
    else:
        #create shadow array
        shadow4 = part4.copy()
        for i in range(len(shadow4)):
            #places bit in shifted position
            part4[(i + 1) % 32] = shadow4[i]

    #forming the 640-bit blocks
    blockset1 = part1 + part3
    blockset2 = part2 + part4

    #XOR the bits together, creating round key
    for bit in range(len(blockset1)):
        key.append(int((blockset1[bit] + blockset2[bit])) % 2)

    #adds to an array of all roundkeys
    roundKeys.append(key)
    #create next key to be used in next key schedule
    binArr = blockset1 + blockset2


#FOR MARKING PURPOSES
roundCount = 0
print('---------- Key Schedule ----------')
for key in roundKeys:
    removingArr = ''
    #converts into string for better printing
    for i in range(len(key)):
        removingArr += str(key[i])

    print('Round', roundCount)
    print(removingArr, '\n')
    roundCount += 1
    

#Block cipher encryption

#initialising variables
X = 'Transfer $571.99 from ABSecure Acc 12345 to Westpac Acc 135791 BSB 3344.'
binX = []
blocks = []
IV = []
CBCCipher = []
bitPatterns = [[0,0,0,0], [0,0,0,1], [0,0,1,0], [0,0,1,1], [0,1,0,0], [0,1,0,1], [0,1,1,0], [0,1,1,1], [1,0,0,0], [1,0,0,1], [1,0,1,0], [1,0,1,1], [1,1,0,0], [1,1,0,1], [1,1,1,0], [1,1,1,1]]
substitutePatterns = [[0,1,1,0], [0,0,1,1], [0,1,1,1], [0,0,1,0], [1,0,0,1], [0,0,0,1], [1,0,1,0], [1,1,0,0], [0,1,0,1], [0,1,0,0], [1,1,1,0], [1,1,1,1], [0,0,0,0], [1,0,1,1], [1,0,0,0], [1,1,0,1]]
firstBlockFlag = 1
CBCFlag = 1
blockCount = 0
cipherText = ''

#FOR MARKING PURPOSES
print('---------- Encryption ----------')
#FOR MARKING PURPOSES
print('Plaintext:\n' + X)

#convert X into binary
for letter in X:
        #convert each letter into ascii, then binary
        binLetter = format(ord(letter), '08b')
        binX += str(binLetter)


#FOR MARKING PURPOSES
removingArr = ''
for i in range(len(binX)):
    removingArr += binX[i]
print('\nBinary plaintext:\n' + removingArr + '\n')


#split binary plaintext into 64-bit blocks
for iniByte in range(0, len(binX), 64):
        block = binX[iniByte : iniByte + 64]
        blocks.append(block)

#creating randomised IV
for bit in range(64):
    randBit = random.randint(0,1)
    IV.append(randBit)

#FOR MARKING PURPOSES
removingArr = ''
for i in range(len(IV)):
    removingArr += str(IV[i])
print('Initialisation vector:\n' + removingArr + '\n')

#performs encryption in each block
for block in blocks:

    print('---------- Encryption of block' + ' ' + str(blockCount + 1)+ ' ----------')

    #XOR first key whiten with the plaintext
    for bit in range(64):
        result = (int(block[bit]) + int(keyWhitenStart[bit])) % 2
        block[bit] = result

    #XOR IV with the first plaintext (CBC mode of operation)
    if CBCFlag == 1:
        for bit in range(64):
            result = (int(block[bit]) + int(IV[bit])) % 2
            block[bit] = result
        CBCFlag = 0

    #XOR plaintext with previous block's ciphertext (CBC mode of operation)
    else:
        for bit in range(64):
            result = (int(block[bit]) + int(CBCCipher[bit])) % 2
            block[bit] = result


    #Performs each round of encryption
    for round in range(8):
        #XOR block with current roundkey
        for bit in range(64):
            result = (int(block[bit]) + int(roundKeys[round][bit])) % 2
            block[bit] = result

        #performs bit shift depending on round (Follows same shift pattern as key schedule)
        if round == 4:
            #create shadow array
            shadowBlock = block.copy()
            for i in range(64):
                #places bit into shifted position
                block[(i + 10) % 32] = shadowBlock[i]

            #shifts by 2 bits on sixth round
        elif round == 6:
            #create shadow array
            shadowBlock = block.copy()
            for i in range(64):
                #places bit into shifted position
                block[(i + 2) % 32] = shadowBlock[i]
            
            #shifts by 5 bits on 7th round
        elif round == 7:
            #create shadow array
            shadowBlock = block.copy()
            for i in range(64):
                #places bit into shifted position
                block[(i + 5) % 32] = shadowBlock[i]

        #shifts by 1 bit on every other round
        else:
            #create shadow array
            shadowBlock = block.copy()
            for i in range(64):
                #places bit into shifted position
                block[(i + 1) % 32] = shadowBlock[i]
        
        #split 64-bit block into 16 4-bit blocks
        splitBlocks = []
        for iniSplit in range(0, len(block), 4):
            #for each 4 bits it is appended to an array of all splits
            split = block[iniSplit: iniSplit + 4]
            splitBlocks.append(split)

        #substituting bits in each block depending on bit pattern
        for split in range(len(splitBlocks)):
            #loops through each substituted bit pattern to find the one which matches
            for pattern in range(len(bitPatterns)):
                #substitutes the split if in the same position in the designated split array
                if splitBlocks[split] == bitPatterns[pattern]:
                    splitBlocks[split] = substitutePatterns[pattern]
                    #ends the loop through bit patterns if found early
                    break
        
        #reforms split blocks back into 64-bit block
        blocks[blockCount] = splitBlocks[4] + splitBlocks[9] + splitBlocks[8] + splitBlocks[12] + splitBlocks[1] + splitBlocks[5] + splitBlocks[6] + splitBlocks[0] + splitBlocks[13] + splitBlocks[2] + splitBlocks[7] + splitBlocks[10] + splitBlocks[11] + splitBlocks[15] + splitBlocks[14] + splitBlocks[4]

        #FOR MARKING PURPOSES
        removingArr = ''
        for i in blocks[blockCount]:
            removingArr += str(i)
        print('round ' + str(round + 1) + ' of encryption:' + '\n' + removingArr + '\n')
            

    #After all encryptions round are performed, end encryption occurs

    #performs final key whitening
    for bit in range(64):
        result = (int(block[bit]) + int(keyWhitenEnd[bit])) % 2
        block[bit] = result
    blocks[blockCount] = block
    
    #assigns ciphertext to be used in next encryptions CBC
    CBCCipher = block

    #FOR MARKING PURPOSES
    removingArr = ''
    for i in blocks[blockCount]:
        removingArr += str(i)
    print('Final block ciphertext:\n' + removingArr + '\n')

    #increments for each block encrypted
    blockCount += 1 

#puts all blocks together
for block in blocks:
    for bit in range(64):
        cipherText += str(block[bit]) 

print('Ciphertext (of message X):\n' + cipherText + '\n')


