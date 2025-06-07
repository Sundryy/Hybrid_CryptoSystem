import random

#primality test to determine whether a number is prime
def millerRabinPrimTest(prime):
    #stores results of each test case
    isPrime = []
    #test cases to determine primality
    a = []
    for i in range(5):
        a.append(random.randint(0,10000000))

    #stores the exponents of (2 pow s) x d
    s = 0
    d = prime - 1
    while (d / 2) % 1 == 0:
        d = int(d / 2)
        s += 1
    #stores exponent as r for second test if required
    r = s

    #iterates through each test case
    for i in range(len(a)):
        #performs formula 1 test, calling function to perform power (through square and multiply)
        result = squareAndMultiply(a[i], d, prime)
        #test case is successful, storing result and moving onto next test case
        if result == 1 or result == prime - 1:
            isPrime.append(1)
            continue

        #above formula test failed, moving onto the next formula test
        else:
            notPrimeFlag = 1
            #looks at each r power (from 0 to s) <-- r is always less or equal to s
            for j in range(r + 1):
                #multiplies exponent 2 with the current r iteration (j)
                power = (2 ** j) * d
                #performs multiplication with exponent (mod prime no.); performed through square and multiply
                result = squareAndMultiply(a[i], power, prime)
                #test case is successful, storing result and moving onto the next test case
                if result == prime - 1:
                    isPrime.append(1)
                    #changes flag value as test case shows possible prime
                    notPrimeFlag = 0
                    break

            #no iterations of r had passed the test case (no flag change), failing both formulas and test case
            if notPrimeFlag == 1:
                #storing failed test
                isPrime.append(0)
    
    #if a single test case is failed, returns no prime result
    for testCaseResult in isPrime:
        if testCaseResult == 0:
            return 'Miller-Rabin test failed, number ' + str(prime) + ' is not a prime number.\n'
    #no test case failures, returning prime success
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
        #cannot consider 0 as a possible value so it skips past
        if e == 0:
            continue

        #performing GCD
        element = findingGCD(e, phi)
        #GCD result is 1, storing as a possible e value
        if element == 1:
            possibleE.append(e)

    #returns possible e's, n and phi
    return possibleE, n, phi

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
    signatureDecimal = squareAndMultiply(decimal,d,n)
    #returns signature
    return signatureDecimal

#reverses signature
def unsigning(s, e, n):
    #decrypts signature using signature^e (mod n)
    unsignedx = squareAndMultiply(s,e,n)
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


    


x = ';OaP@*x6j'
p = 1000000000163   #40-bit prime
q = 1000000006793    #40-bit prime

print('\n---- PRIMALITY TEST ----\n')
print(millerRabinPrimTest(p)) #tests p for primality
print(millerRabinPrimTest(q)) #tests q for primality

possibleE, n, phi = findinge(p, q) #finds e's, n and phi

e = 9 #the chosen e

#performs extended euclidean algorithm to set-up calculating d
g, t, y = findingDSetUp(e, phi)
#calculates d
d = t % phi

print('---- VALUES ----\n')
#outputting values
print('List of possible e values:\n', possibleE, '\n')
print('p: ', p)
print('q: ', q)
print('e: ', e)
print('n: ', n)
print('phi: ', phi)
print('d: ', d, '\n')

#assigns key pair
publicKey = [n, e]
privatekey = d

#calculates signature
s = signing(x, privatekey, publicKey[0])

#pair sent to Alice
signaturePair = [x,s]

print('---- Public Key | Private Key | Signature -----\n')
print('Public key: ', publicKey)
print('Private key: ', privatekey)
print('sent message & signature: ', signaturePair, '\n')

#reverses signature
z = unsigning(signaturePair[1],publicKey[1], publicKey[0])

#checks signature validity
valid = signatureCheck(signaturePair[0], z)








