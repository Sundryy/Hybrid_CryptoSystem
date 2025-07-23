#testing creating 2048 bit prime
from Crypto.Util import number
from tkinter import filedialog
import CSI2108_StreamCipher_FARROW_10653054
import keyExchangeVerification
import CSI2108_HashFunction_FARROW_10653054
import RSAKeyPair
import re




def optionsMenu():
    #generates RSA key pair
    p, q, possibleE, e, n, phi, publicKey, privateKey = RSAKeyPair.generateKeyPair()

    while True:
        print('1. Encrypt plaintext\n')
        print('2. Decrypt ciphertext\n') #will only work once a plaintext has been encrypted
        print('3. Encrypt key exchange\n')
        print('4. Decrypt key exchange\n') #will work by user copy and pasting encrypted key
        print('5. Produce hash digest of plaintext\n')
        print('6. Produce signature\n')
        print('7. Decrypt signature\n') #will work by user copying and pasing encrypted signature
        print('8. Simulate hybrid cryptosystem encryption & decryption\n')
        print('9. Display Public and Private Key Generated\n')
        choice = input('Enter an option: ')

        if choice == '1':
            print('\n====================\n1. ENCRYPT PLAINTEXT\n====================\n')
            plainText = chooseType('plaintext')
            if plainText:
                keyStream,binCipher = CSI2108_StreamCipher_FARROW_10653054.encrypt(plainText)
                displayResults(
                    {
                        "Plaintext (binary)": plainText,
                        "Key stream": keyStream,
                        "Ciphertext (binary)": binCipher 
                    }
                )



        if choice == '2':
            ciphertext = chooseType('ciphertext')
            key = chooseType('key')

            if ciphertext:
                plaintext = CSI2108_StreamCipher_FARROW_10653054.decrypt(key,ciphertext)
                displayResults(
                    {
                        "Ciphertext (binary)":binCipher,
                        "Key stream": keyStream,
                        "Plaintext (binary)": plaintext
                    }
                )



        elif choice == '3':
            plainKey = chooseType('key')
            if plainKey:
                cipherKey = keyExchangeVerification.encryption(publicKey, plainKey)

                displayResults(
                    {
                        "Plaintext key":plainKey,
                        "Ciphertext key (binary)":cipherKey
                    }
                )



        elif choice == '4':
            cipherKey = chooseType('encrypted key')
            if cipherKey:
                plainKey = keyExchangeVerification.decryption(publicKey[0], privateKey,cipherKey)

                displayResults(
                    {
                        "Cipher key (binary)":cipherKey,
                        "Plain key (binary)": plainKey
                    }
                )


            
        elif choice == '5':
            plainText = chooseType('plaintext')
            if plainText:
                digest = CSI2108_HashFunction_FARROW_10653054.hashFunction(plainText)
                displayResults(
                    {
                        "Plaintext (binary)":plainText,
                        "Hash digest":digest
                    }
                ) 



        elif choice == '6':
            pass
        elif choice == '7':
            pass
        elif choice == '8':
            pass



def chooseType(enteredText):
    while True:
        print('===== Entering a', enteredText, '=====')
        print('1. Submit a file')
        print('2. Enter text')
        print('3. Exit\n')
        choice = input('Enter an option: ')
        binplainORcipher = ''

        if choice == '1':
            file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            try:
                file = open(file_path, 'r')
                plainORcipher = file.read()
            except:
                return 0
           
        elif choice == '2':
            plainORcipher = input('\nEnter text: ')
        
        else:
            print('not an option')
            return 0


        if re.fullmatch('[01]+', plainORcipher):
            binplainORcipher = plainORcipher

        else:
            for letter in plainORcipher:
                #convert x to ascii decimal, then binary
                binLetter = format(ord(letter), '08b')
                binplainORcipher += str(binLetter)
        
        return binplainORcipher
    

def displayResults(resultDictionary):
    print('\n============\n  Results\n============\n')

    for key in resultDictionary:
        print(key, ':', resultDictionary[key], '\n')





#starts program
if __name__ == '__main__':
    optionsMenu()




#
#

#need RSA key creation stuff to go into its own file (it is used by two seperate tasks, 2 seperate code copies) <--- NOT GOOD!



#LIST OF THINGS TO FIX
# 3. Primality is broken (float number is too high for python to deal with)
# 4. Must name and fix up chooseType(), making it clear what you are entering
# 6. nest LFSR arrays into another array -> will shorten length of code but requires all code to be changed in that portion
