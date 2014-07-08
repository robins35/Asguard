import random, os, string, hashlib, time, sys
import ConfigParser


def make_key(password):

	key = hashlib.sha256(password).digest()

	return key

def make_password():
	password= ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))
	
	return password
	
def add_entry (fileName, alg, password, sectionName = False, keyfilePath = "keyfile.ini"):

	adder=ConfigParser.RawConfigParser()

	creation= time.asctime( time.localtime(time.time()) )

	sectid=random.randint(0,sys.maxint)
	if (sectionName):
		sectname = sectionName
	else:
		sectname= "ENTRY# " + str(sectid)

	adder.add_section(sectname)
	adder.set(sectname, "FILE", fileName)
	adder.set(sectname, "ALGORITHM", alg)
	adder.set(sectname, "KEY", password)

	with open(keyfilePath, "a") as keyfile:
		adder.write(keyfile)

def update_section_name (oldSectionName, newSectionName, 
			 keyfilePath = "keyfile.ini"):
	
	adder=ConfigParser.RawConfigParser()
	adder.read(keyfilePath)
	if (adder.has_section(oldSectionName)):
		# get all section options
		ops = adder.options(oldSectionName)
		# make new section
		adder.add_section(newSectionName)
		# transfer all options to new section
		for op in ops:
			adder.set(newSectionName,
				  op,
				  adder.get(oldSectionName,op))
		# remove old section
		adder.remove_section(oldSectionName)

		with open(keyfilePath, "wb") as keyfile:
			adder.write(keyfile)

def remove_entry (sectionName, keyfilePath = "keyfile.ini"):
	
	adder=ConfigParser.RawConfigParser()
	adder.read(keyfilePath)
	adder.remove_section(sectionName)
	
	with open(keyfilePath, "wb") as keyfile:
		adder.write(keyfile)
		
def read_keyfile(keys, keyfilepath = "keyfile.ini"):   

	reader=ConfigParser.RawConfigParser()

	reader.read(keyfilepath)
	sections= reader.sections()

	for x in sections:
		name= reader.get(x,"FILE")
		alg= reader.get(x,"ALGORITHM")
		key= reader.get(x,"KEY")
		key = make_key(key)
		i= [alg, key]
		keys[x]= i
	
	return keys
	

def create_keyfile():
	
		creator=ConfigParser.RawConfigParser()
	 	
	 	with open("keyfile.ini", "wb") as keyfile:
			creator.write(keyfile)
