
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












