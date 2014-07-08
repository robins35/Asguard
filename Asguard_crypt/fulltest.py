import hashlib, os
from filecrypt.ALL_filecrypt import *
##from filecrypt.keyfile import *
from keyfile.keyfile import *

#myfile= raw_input("Enter a file to encrypt: ")
#myoutfile= raw_input("What do you want to call it when it is encrypted: ")
#mode= raw_input("Which algorithm do you wish to use [AES, Blowfish, CAST]?")

myfile = "blarg.txt"
myoutfile = "blarg-enc"
mode = "AES"

while (True):
	print ""
	if not myoutfile:
		myoutfile=myfile+".enc"

        passwd = make_password()
	key= make_key(passwd)
	print "MADE KEY, len = " + str(len(key))
        print "key = " + key
	if chr(10) in key:
            print "contains NL"
	if chr(12) in key:
            print "contains NP"
	if chr(13) in key:
            print "contains CR"
	if chr(32) in key:
            print "contains SPACE"
	if chr(9) in key:
            print "contains TAB"
        if chr(59) in key:
            print "contains SEMICOLON"

	encrypt_file(key, myfile, myoutfile, mode)
	print "File encrypted\n"

	add_entry(myoutfile, mode, passwd, myoutfile)
	print "Added file to keyfile.ini"

	keys = {}
	read_keyfile(keys)
	key = keys[myoutfile][1]
        print "RETRIEVED KEY"
	print "key size = " + str(sys.getsizeof(key))
	print "key length = " + str(len(key))
        print "key = " + key

        if chr(10) in key:
		print "contains NL"
	if chr(12) in key:
		print "contains NP"
	if chr(13) in key:
		print "contains CR"
	if chr(32) in key:
		print "contains SPACE"
	if chr(9) in key:
		print "contains TAB"
        if chr(59) in key:
            print "contains SEMICOLON"

	#go= raw_input("Ready to decrypt?")

	decrypt_file(key, myoutfile, myfile, mode)
	print "File decrypted"

	#remove_entry(myoutfile)


