#testing creating 2048 bit prime
from Crypto.Util import number
from tkinter import filedialog
import CSI2108_StreamCipher_FARROW_10653054
import CSI2108_KeyExchange_FARROW_10653054
import CSI2108_HashFunction_FARROW_10653054
import re




def optionsMenu():
    #generates RSA key pair
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

            #OPTIONS CONTAIN X, Y, Keys (if applicable)
            #oh just create a dictionary within the function call that includes the required things rather than large unfilled sometimes dictionary


        if choice == '1':
            print('\n====================\nENCRYPT PLAINTEXT\n=====================')
            plainText = chooseType()
            if plainText:
                keyStream,binCipher = CSI2108_StreamCipher_FARROW_10653054.encrypt(plainText)
                displayResults(
                    {
                        "Plaintext (binary | pre-nonce implementation)": plainText,
                        "Key stream": keyStream,
                        "Ciphertext (binary)": binCipher 
                    }
                )
            else:
                print('No plaintext selected')
                #continue


        if choice == '2':
            ciphertext = chooseType()
            if ciphertext:
                keyStream, binPlain = CSI2108_StreamCipher_FARROW_10653054.decrypt(ciphertext)
                displayResults(
                    {
                        "Ciphertext (binary)":binCipher,
                        "Key stream": keyStream,
                        "Plaintext (binary)": binPlain
                    }
                )
            else:
                print('No ciphertext selected')
                #continue


        elif choice == '3':
            plainKey = chooseType()
            if plainKey:
                cipherKey = CSI2108_KeyExchange_FARROW_10653054.encryption(publicKey, plainKey)

                displayResults(
                    {
                        "Plaintext key":plainKey,
                        "Ciphertext key (binary)":cipherKey
                    }
                )
            else:
                print('No plaintext key entered')
                #continue


        elif choice == '4':
            cipherKey = chooseType()
            if cipherKey:
                plainKey = CSI2108_KeyExchange_FARROW_10653054.decryption(publicKey[0], privateKey,cipherKey)

                displayResults(
                    {
                        "Cipher key (binary)":cipherKey,
                        "Plain key (binary)": plainKey
                    }
                )
            else:
                print('No ciphertext key entered')
                #continue
            
        elif choice == '5':
            plainText = chooseType()
            if plainText:
                digest = CSI2108_HashFunction_FARROW_10653054.hashFunction(plainText)

                displayResults(
                    {
                        "Plaintext (binary)": plainText
                        "Hash digest": digest
                    }
                ) 
                '''
                print('\n============\n  Results\n============\n')
                print('\n Plaintext (binary):', plainText)
                print('\n Hash Digest:', digest)
                '''
            else:
                print('No plaintext entered')
                #continue

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
