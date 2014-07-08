from Crypto.Cipher import AES

obj = AES.new('This is a key456', AES.MODE_ECB)
message = "HELLO WORLD!!!!!"

ciphertext = obj.encrypt(message)

print ciphertext

obj2 = AES.new('This is a key456', AES.MODE_ECB)
plaintext= obj2.decrypt(ciphertext)

print plaintext



