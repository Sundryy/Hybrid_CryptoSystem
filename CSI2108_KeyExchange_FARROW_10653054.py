import random
import re
#testing creating 2048 bit prime
from Crypto.Util import number

#primality test to determine whether a number is prime
def millerRabinPrimTest(prime):
    #stores results of test cases
    isPrime = []
    #test cases
    a = []
    #chooses 5 random test cases
    for i in range(5):
        a.append(random.randint(0,10000000))

    #rewrites n - 1 to 2^s x d (where d is odd)
    d = prime - 1 #means n - 1
    s = 0
    #finds d where d is odd (every divide increases exponent s)
    while (d / 2) % 1 == 0: #divides until d is odd, storing number of divides as the exponent
        d = int(d / 2)
        s += 1
    #intialises r (for second test if required)
    r = s

    #iterates through each test case
    for i in range(len(a)):
        #tests a^d = 1 (mod prime)
        result = squareAndMultiply(a[i], d, prime)
        #test case is passes, moving onto next test case
        if result == 1 or result == prime - 1:
            isPrime.append(1)
            continue
        
        #above test failed, moves to next formula

        #tests a^(2^r) x d modulo -1 (mod n)
        else:
            notPrimeFlag = 1
            #finds that value r which satisfies requirement
            # looks at values from 0 to s - 1
            for j in range(r):
                #performs (2^r) x d
                power = (2 ** j) * d
                #a^result above (square multiply used)
                result = squareAndMultiply(a[i], power, prime)
                #r satisfies condition, test case passes, moves onto next test case
                if result == prime - 1:
                    #stores passed test case
                    isPrime.append(1)
                    #changes flag value as test case shows possible prime
                    notPrimeFlag = 0
                    break

            #no r satisfies condition, test case fails, moves onto next test case
            if notPrimeFlag == 1:
                #stores failed test
                isPrime.append(0)
    

    #if a single test case failed, returns no prime result
    for testCaseResult in isPrime:
        if testCaseResult == 0:
            return 'Miller-Rabin test failed, number ' + str(prime) + ' is not a prime number.\n'
    #all test case passes, returns prime result
    return 'Miller-Rabin test passed, number ' + str(prime) + ' is a prime.\n'


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


#determines GCD between the e value in iteration and phi
def findingGCD(e, phi):
    while(phi):
       e, phi = phi, e % phi
    #returns result of GCD.
    return abs(e)


#determines all possible e values (only between 1 and 100 as we are choosing small e regardless)
#also creates n and phi, which are stored in global varaibles outside function
def findinge(p, q):
    #determines n (p x q)
    n = p * q
    #determines phi (p - 1) x (q - 1)
    phi = (p - 1) * (q - 1)

    #array of possible e values fulfilling GCD(e, phi) = 1
    possibleE = []

    #small e ideal -> looking at 100 numbers (1 - 100)
    for e in range(101):
        #cannot consider 0 as a possible value, skipping it
        if e == 0:
            continue

        #performing GCD
        element = findingGCD(e, phi)
        #GCD result is 1, storing as a possible e value
        if element == 1:
            possibleE.append(e)

    #returns possible e's, n and phi
    return possibleE, n, phi


def findingD(e, phi):
    g, t, y = findingDSetUp(e, phi)
    #calculates d
    d = t % phi
    return d

#finds d from chosen e and phi
#Performs extended euclidean algorithm
#https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms-2/
def findingDSetUp(a, b):
    # Base Case 
    if a == 0 : 
        return b, 0, 1

    gcd, x1, y1 = findingDSetUp(b % a, a)
     
    # Update x and y using results of recursive 
    # call
    x = y1 - (b//a) * x1 
    y = x1

    return gcd,x,y

#testing creating 2048 bit prime
from Crypto.Util import number


def generateKeyPair():
    print('\n==== generating RSA key pair ====\n\n\n')
    p = number.getPrime(2048)
    q = number.getPrime(2048)
    possibleE, n, phi = findinge(p, q)
    e = 13 #very common e values im finding
    privateKey = findingD(e, phi)
    publicKey = [n, e]

    return p, q, possibleE, e, n, phi, publicKey, privateKey

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
        encryptedBlockDecimal = squareAndMultiply(blockInt,publicKey[1], publicKey[0])
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
        decryptedBlockDecimal = squareAndMultiply(blockInt,privateKey, n)
        #convert to binary
        decryptedBinary = bin(decryptedBlockDecimal)
        #removes the '0b' before the binary of block.
        decryptedBinary = decryptedBinary[2:]
        #pads block to plaintext block length
        decryptedBinary = decryptedBinary.zfill(int(EncryptedBlocksPaddings[block - 1]))
        decryptedCipherText += decryptedBinary

    return decryptedCipherText

        

if __name__ == '__main__':
    #plaintext
    x = "011111110000100000111110010010111101101010111101000100011000111000111110001110110000011111110101000001000111010000011110000110001001110111010010011111100100110011001011111100011011111010110010010100111010101000010110111001011000100001001110100000011000010110001010101100000111000101111010000110000010000001010101011111111001001000001000100110111000110011100110100100001011101110001010000011000011100001101110010010101010100111000010100001101111011010000101011000001010110100111011010111100010010011110000000100111111110101011100100001000111001011101011000101111001000111000001"

    p, q, possibleE, e, n, phi, publicKey, privateKey = generateKeyPair()

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
    