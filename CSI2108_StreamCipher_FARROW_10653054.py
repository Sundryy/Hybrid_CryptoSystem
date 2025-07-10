import random

#assigns the starting LFSR flip - flop values from FF15 to FF0, followed by P values in the same array from P0 to Pm-1
LFSR1values = [0,0,1,1,0,0,0,0,1,0,0,1,1,0,1,1,1,0,1]
LFSR2values = [0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,1,0,0]
LFSR3values = [1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0]
LFSR4values = [1,0,1,1,0,1,0,0,1,1,1,0,1,1,0,1,0,1]

#Encrypts plaintext based on chosen LFSR values
def encrypt(X):
    

    ''' NONCE IS MEANT TO GO INTO THE KEYSTREAM TO MAKE THE KEYSTREAMS UNIQUELY DIFFERENT NOT THE PLAINTEXT BINARY!!!!! CHANGE THIS!!!'''
    nonce = random.randint(5000000, 1000000000000)
    #convert binary to decimal
    blockInt = int(X, 2)
    #multiple nonce value into binary
    blockInt = nonce * blockInt
    #convert decimal to binary
    X = bin(blockInt)[2:]
    

    #assigning local variables to be used in the function
    LFSR1 = LFSR1values.copy()
    LFSR2 = LFSR2values.copy()
    LFSR3 = LFSR3values.copy()
    LFSR4 = LFSR4values.copy()
    tempVal = None
    #binX = ''
    y = ''
    k = []
    clocks = 0
    


    binX = X
    '''
    #turn X string into binary
    for letter in X:
        #turns each letter into ascii, then each letter into binary
        binLetter = format(ord(letter), '08b')
        binX += str(binLetter)
    '''

    #performs as many clocks as needed to generate enough bits in keystream
    while clocks != len(binX):
        #generates next bit for LFSR1 based on XOR and AND gates in LFSR2
        nextLFSR1bit = (LFSR2[15] + (LFSR2[14]*LFSR2[16]) + LFSR2[12] + LFSR2[13] + LFSR2[10] + (LFSR2[9]*LFSR2[17]) + LFSR2[6] + LFSR2[4]) % 2
        #generates next bit for LFSR2 based on XOR and AND gates in LFSR3
        nextLFSR2bit = (LFSR3[15] + LFSR3[13] + LFSR3[14] + LFSR3[11] + (LFSR3[10]*LFSR3[16]) + LFSR3[5]) % 2
        #generates next bit for LFSR3 based on XOR and AND gates in LFSR4
        nextLFSR3bit = ((LFSR4[11]*LFSR4[16]) + LFSR4[8] + LFSR4[7] + LFSR4[5] + LFSR4[4] + (LFSR4[3]*LFSR4[17])) % 2
        #generates next bit for LFSR4 based on XOR and AND gates in LFSR1
        nextLFSR4bit = (((LFSR1[15]+LFSR1[14])*LFSR1[16]) + (LFSR1[12]*LFSR1[17]) + LFSR1[10] + LFSR1[9] + (LFSR1[6]*LFSR1[18]) + LFSR1[5] + LFSR1[4] + LFSR1[2]) % 2

        #LFSR1 flip-flops moving right, assigning flip-flop 15 the next generated bit from LFSR2
        for i in range(len(LFSR1) - 3):
            #moves first flip-flop to its right
            if i == 0:
                tempVal = LFSR1[i + 1]
                LFSR1[i + 1] = LFSR1[i]
            #takes last bit to be passed off for keystream and assigns LFSR2 generated bit to flip-flop 15
            elif i == 15:
                passoff1 = tempVal
                LFSR1[0] = nextLFSR1bit
            #moves all other flip-flop values to its right
            else:
                tempVal2 = LFSR1[i + 1]
                LFSR1[i + 1] = tempVal
                tempVal = tempVal2
        
        #LFSR2 flip-flops moving right, assigning flip-flop 15 the next generated bit from LFSR3
        for i in range(len(LFSR2) - 2):
            #moves first flip-flop to its right
            if i == 0:
                tempVal = LFSR2[i + 1]
                LFSR2[i + 1] = LFSR2[i]
            #takes last bit to be passed off for keystream and assigns LFSR3 generated bit to flip-flop 15
            elif i == 15:
                passoff2 = tempVal
                LFSR2[0] = nextLFSR2bit
            #moves all other flip-flop values to its right
            else:
                tempval2 = LFSR2[i + 1]
                LFSR2[i + 1] = tempVal
                tempVal = tempval2
        
        #LFSR3 flip-flops moving right, assigning flip-flop 15 the next generated bit from LFSR4
        for i in range(len(LFSR3) - 1):
            #moves first flip-flop to its right
            if i == 0:
                tempVal = LFSR3[i + 1]
                LFSR3[i + 1] = LFSR3[i]
            #takes last bit to be passed off for keystream and assigns LFSR4 generated bit to flip-flop 15
            elif i == 15:
                passoff3 = tempVal
                LFSR3[0] = nextLFSR3bit
            #moves all other flip-flop values to its right
            else:
                tempval2 = LFSR3[i + 1]
                LFSR3[i + 1] = tempVal
                tempVal = tempval2
        
        #LFSR4 flip-flops moving right, assigning flip-flop 15 the next generated bit from LFSR1
        for i in range(len(LFSR4) - 2):
            #moves first flip-flop to its right
            if i == 0:
                tempVal = LFSR4[i + 1]
                LFSR4[i + 1] = LFSR4[i]
            #takes last bit to be passed off for keystream and assigns LFSR1 generated bit to flip-flop 15
            elif i == 15:
                passoff4 = tempVal
                LFSR4[0] = nextLFSR4bit
            #moves all other flip-flop values to its right
            else:
                tempval2 = LFSR4[i + 1]
                LFSR4[i + 1] = tempVal
                tempVal = tempval2

        #generate bit of keystream from flip-flop 0 outputs
        passoff5 = (passoff1 + passoff2) % 2
        passoff6 = (passoff3 + passoff4) % 2
        #save bit to keystream
        k.append((passoff5 + passoff6) % 2)
        clocks += 1

    #FOR MARKING PURPOSES
    kStream = ''
    for bit in range(len(k)):
        kStream += str(k[bit])


    #XOR keystream and binary of plaintext
    for bit in range(len(binX)):
        y += str((int(binX[bit]) + k[bit]) % 2)
    
    #returns encrypted ciphertext
    return kStream, y

#Decrypts binary ciphertext based on LFSR values
def decrypt(LFSR1,LFSR2,LFSR3,LFSR4, y):
    #assigning local variables to be used in the function
    LFSR1 = LFSR1values.copy()
    LFSR2 = LFSR2values.copy()
    LFSR3 = LFSR3values.copy()
    LFSR4 = LFSR4values.copy()
    tempVal = None
    binX = ''
    plaintext = ''
    k = []
    bytesArr = []
    clocks = 0

    #FOR MARKING PURPOSES
    print('\nCiphertext: \n', y, '\n')

    #performs as many clocks as needed to generate enough bits in keystream
    while clocks != len(y):
        #generates next bit for LFSR1 based on XOR and AND gates in LFSR2
        nextLFSR1bit = (LFSR2[15] + (LFSR2[14]*LFSR2[16]) + LFSR2[12] + LFSR2[13] + LFSR2[10] + (LFSR2[9]*LFSR2[17]) + LFSR2[6] + LFSR2[4]) % 2
        #generates next bit for LFSR2 based on XOR and AND gates in LFSR3
        nextLFSR2bit = (LFSR3[15] + LFSR3[13] + LFSR3[14] + LFSR3[11] + (LFSR3[10]*LFSR3[16]) + LFSR3[5]) % 2
        #generates next bit for LFSR3 based on XOR and AND gates in LFSR4
        nextLFSR3bit = ((LFSR4[11]*LFSR4[16]) + LFSR4[8] + LFSR4[7] + LFSR4[5] + LFSR4[4] + (LFSR4[3]*LFSR4[17])) % 2
        #generates next bit for LFSR4 based on XOR and AND gates in LFSR1
        nextLFSR4bit = (((LFSR1[15]+LFSR1[14])*LFSR1[16]) + (LFSR1[12]*LFSR1[17]) + LFSR1[10] + LFSR1[9] + (LFSR1[6]*LFSR1[18]) + LFSR1[5] + LFSR1[4] + LFSR1[2]) % 2
        
        #LFSR1 flip-flops moving right, assigning flip-flop 15 the next generated bit from LFSR2
        for i in range(len(LFSR1) - 3):
            #moves first flip-flop to its right
            if i == 0:
                tempVal = LFSR1[i + 1]
                LFSR1[i + 1] = LFSR1[i]
            #takes last bit to be passed off for keystream and assigns LFSR2 gate outputs to the last flip-flop
            elif i == 15:
                passoff1 = tempVal
                LFSR1[0] = nextLFSR1bit 
            #moves all other flip-flop values to its right
            else:
                tempVal2 = LFSR1[i + 1]
                LFSR1[i + 1] = tempVal
                tempVal = tempVal2
        
        #LFSR2 flip-flops moving right, assigning flip-flop 15 the next generated bit from LFSR3
        for i in range(len(LFSR2) - 2):
            #moves first flip-flop to its right
            if i == 0:
                tempVal = LFSR2[i + 1]
                LFSR2[i + 1] = LFSR2[i]
            #takes last bit to be passed off for keystream and assigns LFSR2 generated bit to flip-flop 15
            elif i == 15:
                passoff2 = tempVal
                LFSR2[0] = nextLFSR2bit
            #moves all other flip-flop values to its right
            else:
                tempval2 = LFSR2[i + 1]
                LFSR2[i + 1] = tempVal
                tempVal = tempval2
        
        #LFSR3 flip-flops moving right, assigning flip-flop 15 the next generated bit from LFSR4
        for i in range(len(LFSR3) - 1):
            #moves first flip-flop to its right
            if i == 0:
                tempVal = LFSR3[i + 1]
                LFSR3[i + 1] = LFSR3[i]
            #takes last bit to be passed off for keystream and assigns LFSR4 generated bit to flip-flop 15
            elif i == 15:
                passoff3 = tempVal
                LFSR3[0] = nextLFSR3bit
            #moves all other flip-flop values to its right
            else:
                tempval2 = LFSR3[i + 1]
                LFSR3[i + 1] = tempVal
                tempVal = tempval2
        
        #LFSR4 flip-flops moving right, assigning flip-flop 15 the next generated bit from LFSR1
        for i in range(len(LFSR4) - 2):
            #moves first flip-flop to its right
            if i == 0:
                tempVal = LFSR4[i + 1]
                LFSR4[i + 1] = LFSR4[i]
            #takes last bit to be passed off for keystream and assigns LFSR1 generated bit to flip-flop 15
            elif i == 15:
                passoff4 = tempVal
                LFSR4[0] = nextLFSR4bit
            #moves all other flip-flop values to its right
            else:
                tempval2 = LFSR4[i + 1]
                LFSR4[i + 1] = tempVal
                tempVal = tempval2

        #generate bit of keystream from flip-flop 0 outputs
        passoff5 = (passoff1 + passoff2) % 2
        passoff6 = (passoff3 + passoff4) % 2
        #save bit to keystream
        k.append((passoff5 + passoff6) % 2)
        clocks += 1
    
    #FOR MARKING PURPOSES
    kStream = ''
    for bit in range(len(k)):
        kStream += str(k[bit])
    
    #XOR keystream and encrypted binary, forming decrypted binary of plaintext
    for bit in range(len(y)):
        binX += str((int(y[bit]) + k[bit]) % 2)

    #converts binary to plaintext
    for bit in range(0, len(binX), 8):
        bytesArr.append(binX[bit:bit+8])
    for bits in bytesArr:
        plaintext += chr(int(bits, 2))

    #returns plaintext
    return kStream, plaintext