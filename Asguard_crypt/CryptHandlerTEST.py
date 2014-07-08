from CryptHandler import CryptHandler

pathKeyFile = "/home/sharafd/csci492/Asguard/Asguard_crypt/keyfile.ini"

# initialize with username and password so CryptHandler can
# generate the encryption key to decrypt the keyfile
cryptHandler = CryptHandler(pathKeyFile, "Dane", "Password", False)

pathRawFile = "/home/sharafd/csci492/Asguard/Asguard_crypt/blarg.txt"
mode = "AES"

print "ENCRYPTING " + pathRawFile
pathToEncryptedFile = cryptHandler.Encrypt(pathRawFile, mode)
if (len(pathToEncryptedFile) > 0):
    print "FILE ENCRYPTED AT " + pathToEncryptedFile
else:
    print "ENCRYPT FAILED!"

## GUI calls upload
print "GUI CALLS UPLOAD..."
URI = "URI:CHK:sdfjo23020340"
kfKEY = "5555555555555555"    
print "UPDATING KEYFILE KEY TO URI AND ENCRYPTING KEYFILE..."
pathToEncryptedKeyFile = cryptHandler.UpdateAndEncryptKeyFile(URI, pathRawFile)
if (len(pathToEncryptedKeyFile) > 0):
    print "KEYFILE UPDATED AND ENCRYPTED AT " + pathToEncryptedKeyFile
else:
    print "KEYKFILE UPDATE / ENCRYPT FAILED!"

print "DECRYPTING " + pathToEncryptedFile
pathToDecryptedFile = cryptHandler.Decrypt(pathToEncryptedFile, URI)
if (len(pathToDecryptedFile) > 0):
    print "FILE DECRYPTED AT " + pathToDecryptedFile
else:
    print "DECRYPT FAILED!"

print "Removing temp files...."
cryptHandler.Clean()

print "Removing entry from keyfile..."
cryptHandler.RemoveKeyfileEntry(URI)

