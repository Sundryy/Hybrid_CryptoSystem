import RSAKeyPair
import re

#encrypts int value of message x using RSA public key
def encryption(publicKey, x):
    #array of plaintext blocks
    blocks = []
    #array of plaintext block lengths (for padding leading zero's)
    blockLengths = []
    plaintextDecimals = []
    #array of encrypted blocks
    encryptedBlocks = []
    #stores decimal encrypted blocks
    encryptedBlockDecimals = []

    encryptedKey = ''
    
    #split key into 4090-bit blocks
    for bit in range(0, len(x), 4090):
        #store plaintext block into array 
        block = str(x[bit: bit + 4090])
        blocks.append(block)

    #find block lengths and perform encryptions
    for block in range(len(blocks)):

        #length of plaintext key
        blockLength = len(blocks[block])


        #convert binary block to decimal
        blockInt = int(blocks[block], 2)
        plaintextDecimals.append(str(blockInt))
        #encrypt the block (x to power e (mod n)) using fast exponentiation
        encryptedBlockDecimal = RSAKeyPair.squareAndMultiply(blockInt,publicKey[1], publicKey[0])
        encryptedBlockDecimals.append(encryptedBlockDecimal)
        #convert encrypted decimal to binary
        encryptedBlock = bin(encryptedBlockDecimal)[2:]
        shadowBlock = encryptedBlock
        #if len(encryptedBlock) < blockLength:
        encryptedBlock = '/' + str(blockLength) + '/' + encryptedBlock

        #store encrypted block
        #encryptedBlocks.append(encryptedBlock)
        encryptedKey += str(encryptedBlock)

    #returns ciphertext blocks
    return encryptedKey


#decryption using private key and value of n in public key
def decryption(n, privateKey, y):
    #splits padding schemes and seperates into blocks
    EncryptedBlocksPaddings = re.findall(r"\d+", y)
    #recreates the binary key as a string
    decryptedCipherText = ''

    #converts blocks to decimal, decrypts, converts to binary and reforms the plaintext message
    for block in range(1, len(EncryptedBlocksPaddings), 2):
        #convert binary block ciphertext to decimal
        blockInt = int(EncryptedBlocksPaddings[block], 2)
        #decrypts the block using the decimal of encrypted block and private key.
        decryptedBlockDecimal = RSAKeyPair.squareAndMultiply(blockInt,privateKey, n)
        #convert to binary
        decryptedBinary = bin(decryptedBlockDecimal)
        #removes the '0b' before the binary of block.
        decryptedBinary = decryptedBinary[2:]
        #pads block to plaintext block length
        decryptedBinary = decryptedBinary.zfill(int(EncryptedBlocksPaddings[block - 1]))
        decryptedCipherText += decryptedBinary

    return decryptedCipherText


#calculates signature of h(x)
def signing(x, d, n):
    binX = ''
    #convert message into binary
    for letter in x:
        #turns each letter into ascii, then each letter into binary
        binLetter = format(ord(letter), '08b')
        binX += str(binLetter)
    #convert binary to decimal
    decimal = int(binX, 2)
    #calculates signature
    signatureDecimal = RSAKeyPair.squareAndMultiply(decimal,d,n)
    #returns signature
    return signatureDecimal

#reverses signature
def unsigning(s, e, n):
    #decrypts signature using signature^e (mod n)
    unsignedx = RSAKeyPair.squareAndMultiply(s,e,n)
    #returns reversed signature
    return unsignedx

#checks h(x) and reversed signature match
def signatureCheck(x, z):
    #validity flag
    isValid = 1
    #convert message x into binary
    binX = ''
    for letter in x:
        #turns each letter into ascii, then each letter into binary
        binLetter = format(ord(letter), '08b')
        binX += str(binLetter)
    
    #converts unsigned message z into binary (currently in decial)
    binZ = bin(z)[2:].zfill(len(binX))
    print('Hash digest binary:         ', binX)
    print('Decrypted signature binary: ', binZ, '\n')

    #compare x and z binary for different bit sequence
    for bit in range(len(binX)):
        if binX[bit] != binZ[bit]:
            isValid = 0

    #signature matches hash digest
    if isValid == 1:
        print('Hash digest and signature match.')
    #signature does not match hash digest
    else:
        print('Hash digest and signature do not match.')

        

if __name__ == '__main__':
    #plaintext
    x = "011111110000100000111110010010111101101010111101000100011000111000111110001110110000011111110101000001000111010000011110000110001001110111010010011111100100110011001011111100011011111010110010010100111010101000010110111001011000100001001110100000011000010110001010101100000111000101111010000110000010000001010101011111111001001000001000100110111000110011100110100100001011101110001010000011000011100001101110010010101010100111000010100001101111011010000101011000001010110100111011010111100010010011110000000100111111110101011100100001000111001011101011000101111001000111000001"

    p, q, possibleE, e, n, phi, publicKey, privateKey = RSAKeyPair.generateKeyPair()

    print('\n---- PRIMALITY TEST ----\n')
    #testing prime p for primality
    #print(millerRabinPrimTest(p)) NEED TO FIX THIS!
    #testing prime q for primality
    #print(millerRabinPrimTest(q)) NEED TO FIX THIS!

    print('---- VALUES ----\n')
    #outputting values
    print('List of possible e values:\n', possibleE, '\n')
    print('p: ', p)
    print('q: ', q)
    print('e: ', e)
    print('n: ', n)
    print('phi: ', phi)
    print('d: ', privateKey ,'\n')

    #output encryption
    print('---- ENCRYPTION / DECRYPTION -----\n')
    print('Public key:  ( ' + str(publicKey[0]), ', ' + str(publicKey[1]), ')')
    print('Private key: ' + str(privateKey) + '\n')
    print('Plaintext: ', x, '\n')

    #performs encryption on plaintext X
    y = encryption(publicKey, x)

    #performs decryption on encrypted blocks y
    decryptedCipherText = decryption(publicKey[0],privateKey, y)

    #checks original and decrypted plaintext for matching binary sequence
    for bit in range(len(x)):
        #if sequence does not match, decryption was unsuccessful
        if x[bit] != decryptedCipherText[bit]:
            print('\n\n---- Decryption unsuccessful ----\n')
            print('plaintexts vary, encryption/decryption failed')
            exit()

    #only occurs on successful decryption
    print('\n\n---- Decryption successful ----\n')
    print('Decrypted plaintext: ', decryptedCipherText)
    