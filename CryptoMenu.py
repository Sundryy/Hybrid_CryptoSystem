#testing creating 2048 bit prime
from Crypto.Util import number
from tkinter import filedialog
import CSI2108_StreamCipher_FARROW_10653054
import CSI2108_KeyExchange_FARROW_10653054
#p = number.getPrime(2048)
#q = number.getPrime(2048)
#print(p * q)


def optionsMenu():
    '''
    print('\n==== generating RSA key pair ====\n\n\n')
    p = number.getPrime(2048)
    q = number.getPrime(2048)
    possibleE, n, phi = CSI2108_KeyExchange_FARROW_10653054.findinge(p, q)
    e = 13 #very common e values im finding
    d = CSI2108_KeyExchange_FARROW_10653054.findingD(e, phi)
    '''


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

            plaintext = chooseType()
            if plaintext:
                binPlain, keyStream, binCipher = CSI2108_StreamCipher_FARROW_10653054.encrypt(plaintext)
                print('\n============\n  Results\n============\n')
                print(' Plaintext (binary):', binPlain, '\n')
                print('         Key stream:', keyStream, '\n')
                print('Ciphertext (binary):', binCipher, '\n')
            else:
                print('No plaintext selected')

        if choice == '2':
            ciphertext = chooseType()
            if ciphertext:
                binCipher, keyStream, binPlain = CSI2108_StreamCipher_FARROW_10653054.decrypt(ciphertext)
                print('\n============\n  Results\n============\n')
                print('Ciphertext (binary):', binCipher, '\n')
                print('         Key stream:', keyStream, '\n')
                print(' Plaintext (binary):', binPlain, '\n')
            else:
                print('No ciphertext selected')

        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            pass
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
        print('1. Submit a file (with text)')
        print('2. Enter text')
        print('3. Exit')
        choice = input('Enter an option: ')

        if choice == '1':
            file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            try:
                file = open(file_path, 'r')
                plainORcipher = file.read()
            except:
                return 0
            
        if choice == '2':
            plainORcipher = input('Enter plaintext: ')

        else:
            return 0
        
        return plainORcipher
    


#p = number.getPrime(2048)
#q = number.getPrime(2048)
#possibleE, n, phi = CSI2108_KeyExchange_FARROW_10653054.findinge(p, q)

#print(possibleE)





if __name__ == '__main__':
    optionsMenu()