import random, os, string, hashlib, time
import ConfigParser
from keyfile.keyfile import *

keys= dict()

#key= make_key()
#create_keyfile()
#print "file created"
#read_HEAD()

#add_entry("a.txt", "AES", make_key())
#add_entry("b.txt", "Blowfish", make_key())
#add_entry("c.txt", "CAST", make_key())
#print "entries created"

read_keyfile(keys)
print "Keys:"
print keys

