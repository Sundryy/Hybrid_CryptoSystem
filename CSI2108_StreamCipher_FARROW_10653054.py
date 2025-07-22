import random

#Encrypts plaintext based on chosen LFSR values
def encrypt(X):
    LFSR1 = ['/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/',1,0,1]
    LFSR2 = ['/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/',0,0]
    LFSR3 = ['/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/',0]
    LFSR4 = ['/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/',0,1]

    #generates Nonce > converts binary > pads 16 bits
    LFSR1Nonce = bin(random.randint(100, 65535))[2:].zfill(16)
    LFSR2Nonce = bin(random.randint(100, 65535))[2:].zfill(16)
    LFSR3Nonce = bin(random.randint(100, 65535))[2:].zfill(16)
    LFSR4Nonce = bin(random.randint(100, 65535))[2:].zfill(16)

    #LFSRs initialised with nonce values
    for bit in range(16):
        LFSR1[bit] = int(LFSR1Nonce[bit])
        LFSR2[bit] = int(LFSR2Nonce[bit])
        LFSR3[bit] = int(LFSR3Nonce[bit])
        LFSR4[bit] = int(LFSR4Nonce[bit])

    tempVal = None
    y = ''
    k = []
    clocks = 0
    binX = X

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



        for i in range(16):
            
            if i == 0:
                #store bit being replaced
                tempBit1 = LFSR1[i + 1]
                tempBit2 = LFSR2[i + 1]
                tempBit3 = LFSR3[i + 1]
                tempBit4 = LFSR4[i + 1]

                #shift bit right
                LFSR1[i + 1] = LFSR1[i]
                LFSR2[i + 1] = LFSR2[i]
                LFSR3[i + 1] = LFSR3[i]
                LFSR4[i + 1] = LFSR4[i]

            elif i == 15:
                #store bit which forms keystream
                passoff1 = tempBit1
                passoff2 = tempBit2
                passoff3 = tempBit3
                passoff4 = tempBit4
                #move end bit to next LFSR
                LFSR1[0] = nextLFSR1bit
                LFSR2[0] = nextLFSR2bit
                LFSR3[0] = nextLFSR3bit
                LFSR4[0] = nextLFSR4bit

            else:
                #stores bit being replaced
                tempBit1_2 = LFSR1[i + 1]
                tempBit2_2 = LFSR2[i + 1]
                tempBit3_2 = LFSR3[i + 1]
                tempBit4_2 = LFSR4[i + 1]
                #shifts stored bit right
                LFSR1[i + 1] = tempBit1
                LFSR2[i + 1] = tempBit2
                LFSR3[i + 1] = tempBit3
                LFSR4[i + 1] = tempBit4
                #stores bit that was replaced
                tempBit1 = tempBit1_2
                tempBit2 = tempBit2_2
                tempBit3 = tempBit3_2
                tempBit4 = tempBit4_2

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


def decrypt(key, y):
    binX = ''
    bytesArr = []
    plaintext = ''

    for bit in range(len(y)):
        binX += str((int(y[bit]) + int(key[bit])) % 2)
    #split bits into bytes
    for bit in range(0, len(binX), 8):
        bytesArr.append(binX[bit:bit+8])
    #convert bytes to text
    for bits in bytesArr:
        plaintext += chr(int(bits, 2))

    return plaintext




if __name__ == '__main__':
    x = 'test'
    y = encrypt(x)

    print(y)

