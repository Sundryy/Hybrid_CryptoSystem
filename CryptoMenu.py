#testing creating 2048 bit prime
from Crypto.Util import number
from tkinter import filedialog
import CSI2108_StreamCipher_FARROW_10653054
#p = number.getPrime(2048)
#q = number.getPrime(2048)

#print(p * q)


CSI2108_StreamCipher_FARROW_10653054.encrypt()




def optionsMenu():
    while True:
        print('1. Encrypt plaintext')
        print('2. Decrypt ciphertext') #will only work once a plaintext has been encrypted
        print('3. Encrypt key exchange')
        print('4. Decrypt key exchange') #will work by user copy and pasting encrypted key
        print('5. Produce hash digest of plaintext')
        print('6. Produce signature')
        print('7. Decrypt signature') #will work by user copying and pasing encrypted signature
        print('8. Simulate hybrid cryptosystem encryption & decryption')

        choice = input('Enter an option: ')

        if choice == '1':
            pass
        if choice == '2':
            pass
        if choice == '3':
            pass
        if choice == '4':
            pass
        if choice == '5':
            pass
        if choice == '6':
            pass
        if choice == '7':
            pass
        if choice == '8':
            pass
        else:
            print('not an option')






def chooseType():
    while True:
        print('1. Submit a file (with text)')
        print('2. Enter text')
        print('3. Exit')
        choice = input('Enter an option: ')

        if choice == '1':
            file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            try:
                file = open(file_path, 'r')
                plaintext = file.read()
                print(plaintext)
            except:
                print('ERROR - No file selected')
                return 0 #!!!! will be used to check if a plaintext was actually entered
            
        if choice == '2':
            plaintext = input('Enter plaintext: ')
        
        return plaintext






