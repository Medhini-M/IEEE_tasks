#final file encryption code
#uses AES encryption
#best for files as it is fast, requires less computational power, flexible


from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
import hashlib
import time

##AES - Advanced Encryption Standard
class Encryptor:
    def __init__(self, key):        #constructor
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)      #pads key to block size=16

    def encrypt(self, msg, key, key_size=256):
        msg = self.pad(msg)                          #pads message
        iv = Random.new().read(AES.block_size)       #initialization vector
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv+cipher.encrypt(msg)

    def encrypt_file(self, file_name):          #deletes original file, creates encr file with same name + .enc
        with open(file_name, 'rb') as f1:
            text = f1.read()
            text = text + self.key
        enc = self.encrypt(text, self.key)
        with open(file_name + ".enc", 'wb') as f1:
            f1.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]        #seperates iv from encrypted string
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")        #removes padding, returns original string

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as f1:
            ciphertext = f1.read()
        dec = self.decrypt(ciphertext, self.key)
        pss = dec[-16:]
        #print(pss)
        if pss == self.key:
            with open(file_name[:-4], 'wb') as f1:     #deleltes encrypted file
                f1.write(dec[:-16])
            os.remove(file_name)
        else:
            print("File decryption failed due to wrong password")
            exit()



p = str(input("Enter password: "))                  ##password is the key to encrypting/decrypting
hashed = hashlib.new('md5')                         #16 byte stream
hashed.update(p.encode())                           #p.encode() - converts string to byte stream
bstream = hashed.digest()                           #hashes data, returns in hexadecimal fmt
#print(bstream)

key = bstream
enc = Encryptor(key)


while True:
    choice = int(input("Enter 1 to encrypt file.\nEnter 2 to decrypt file.\nEnter 3 to exit.\n"))
    if choice == 1:
        file = str(input("Enter name of file to be encrypted: "))
        enc.encrypt_file(file)
        print("File encryption successful!!\n")
    elif choice == 2:
        file = str(input("Enter name of file to be decrypted: "))
        enc.decrypt_file(file)
        print("File decrypted successfully!!\n")
    elif choice == 3:
        exit()
    else:
        print("Invalid choice!")


