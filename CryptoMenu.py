#testing creating 2048 bit prime
from Crypto.Util import number
p = number.getPrime(2048)
q = number.getPrime(2048)

print(p * q)




#testing file opening

import tkinter as tk
from tkinter import filedialog

#allows choosing files to read
file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

file = open(file_path, 'r')
print(file.read())




def optionsMenu():
    print('1. Encrypt plaintext')
    print('2. Decrypt ciphertext') #will only work once a plaintext has been encrypted
    print('3. Encrypt key exchange')
    print('4. Decrypt key exchange') #will work by user copy and pasting encrypted key
    print('5. Produce hash digest of plaintext')
    print('6. Produce signature')
    print('7. Decrypt signature') #will work by user copying and pasing encrypted signature
    print('8. Simulate hybrid cryptosystem encryption & decryption')
    

