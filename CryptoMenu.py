#testing creating 2048 bit prime
from Crypto.Util import number
from tkinter import filedialog
import CSI2108_StreamCipher_FARROW_10653054
import CSI2108_KeyExchange_FARROW_10653054
import CSI2108_HashFunction_FARROW_10653054
import re




def optionsMenu():
    #generates key pair on program start
    p, q, possibleE, e, n, phi, publicKey, privateKey = CSI2108_KeyExchange_FARROW_10653054.generateKeyPair()

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
            print('\n====================\nENCRYPT PLAINTEXT\n=====================')

            plainText = chooseType()


        
            if plainText:
                keyStream,binCipher = CSI2108_StreamCipher_FARROW_10653054.encrypt(plainText)
                print('\n============\n  Results\n============\n')
                print(' Plaintext (binary | pre-nonce implementation):', plainText, '\n')
                print('         Key stream:', keyStream, '\n')
                print('Ciphertext (binary):', binCipher, '\n')
            else:
                print('No plaintext selected')
                continue

        if choice == '2':
            ciphertext = chooseType()
            if ciphertext:
                keyStream, binPlain = CSI2108_StreamCipher_FARROW_10653054.decrypt(ciphertext)
                print('\n============\n  Results\n============\n')
                print('Ciphertext (binary):', binCipher, '\n')
                print('         Key stream:', keyStream, '\n')
                print(' Plaintext (binary):', binPlain, '\n')
            else:
                print('No ciphertext selected')
                continue

        elif choice == '3':
            plainKey = chooseType()
            if plainKey:
                cipherKey = CSI2108_KeyExchange_FARROW_10653054.encryption(publicKey, plainKey)
                print('\n============\n  Results\n============\n')
                print('Plaintext key:', plainKey, '\n')
                print('Ciphertext key (binary):', cipherKey, '\n' )
            else:
                print('No plaintext key entered')
                continue

        elif choice == '4':
            cipherKey = chooseType()
            if cipherKey:
                plainKey = CSI2108_KeyExchange_FARROW_10653054.decryption(publicKey[0], privateKey,cipherKey)
                print('\n============\n  Results\n============\n')
                print('Cipher key (binary):', cipherKey)
                print('Plain key (binary):', plainKey)
            else:
                print('No ciphertext key entered')
                continue
            
        elif choice == '5':
            plainText = chooseType()
            if plainText:
                digest = CSI2108_HashFunction_FARROW_10653054.hashFunction(plainText)
                print('\n============\n  Results\n============\n')
                print('\n Plaintext (binary):', plainText)
                print('\n Hash Digest:', digest)
            else:
                print('No plaintext entered')
                continue

        elif choice == '6':
            pass
        elif choice == '7':
            pass
        elif choice == '8':
            pass
        else:
            print('not an option')


def chooseType():
    while True:
        print('1. Submit a file')
        print('2. Enter text')
        print('3. Exit')
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
            plainORcipher = input('Enter plaintext: ')
        
        else:
            return 0


        if re.fullmatch('[01]+', plainORcipher):
            binplainORcipher = plainORcipher

        else:
            for letter in plainORcipher:
                #convert x to ascii decimal, then binary
                binLetter = format(ord(letter), '08b')
                binplainORcipher += str(binLetter)
        
        return binplainORcipher


####!!!!!!MUST DEAL WITH ENTERED TEXT THAT IS NEEDING CONVERSION OR IS ALREADY IN BINARY. SIMPLE SOLUTION BUT TOO TIRED TO DO CURRENTLY.

#starts program
if __name__ == '__main__':
    optionsMenu()