import random
import re
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


def generateKeyPair():
    print('\n==== generating RSA key pair ====\n\n\n')
    p = number.getPrime(2048)
    q = number.getPrime(2048)
    possibleE, n, phi = findinge(p, q)
    e = 13 #very common e values im finding
    privateKey = findingD(e, phi)
    publicKey = [n, e]

    return p, q, possibleE, e, n, phi, publicKey, privateKey

