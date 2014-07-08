import os
import tempfile
from keyfile.keyfile import *
from filecrypt.ALL_filecrypt import *

class CryptHandler(object):

	#tempPath = ""
	tempPaths = list()

	## When CryptHandler is initialized it creates the keyfile KEY from
	# Username and Password, then attempts to decrypt the keyfile
	# at EncryptedKeyfilePath

	def __init__(self, KeyfilePath, Username, Password, KeyfileIsEncrypted = True):
		self.keyFileKEY = self.makeKeyfileKey(Username, Password)
		if (KeyfileIsEncrypted):
			tempPath = ""
			handle, tempPath = tempfile.mkstemp()

			if (os.path.exists(tempPath) == False):
				print "ERROR: CryptHandler.__init__ could not create temp file"
				return ""

			os.close(handle) #don't need the file to be open
			self.tempPaths.append(tempPath)
		        ## decrypt file using All_filecrypt
			decrypt_file(self.keyFileKEY, KeyfilePath, tempPath, "AES") #default AES for keyfile
			self.keyFilePath = tempPath
			print "CryptHandler: kf path = " + self.keyFilePath
		else:
			self.keyFilePath = KeyfilePath
		return


	######    GUI TOOL  #######
	## Encrypt creates a random key, encrypts file at LocalPath,
	# stores the resulting encrypted file at a temporary location
	# and returns the path to the encrypted file
	def Encrypt(self, LocalPath, EncryptMode, key = False):

		passwd = make_password()
		if (key == False):
			key = make_key(passwd)
		key = make_key(passwd)
		tempPath = ""
		handle, tempPath = tempfile.mkstemp()

		if (os.path.exists(tempPath) == False):
			print "ERROR: CryptHandler.Encrypt could not create temp file"
			return ""

		os.close(handle) #don't need the file to be open
		self.tempPaths.append(tempPath)

		## encrypt file using All_filecrypt
		encrypt_file(key, LocalPath, tempPath, EncryptMode)

		## entry into keyfile using LocalPath as temporary entry id
		fileName = os.path.basename(LocalPath)
		# keyfile.py
		add_entry(fileName, EncryptMode, passwd, LocalPath,self.keyFilePath)
		
		# return path to the encrypted file
		return tempPath

		
	######    GUI TOOL  #######
	## Decrypt looks up the key for the file in the keyfile,
	# decrypts the file and stores it in a temporary location
	# and returns the path to the decrypted file
	def Decrypt(self, LocalPath, URIofTahoeFile):

		tempPath = ""
		keys=dict()
		# keyfile.py
		keys= read_keyfile(keys, self.keyFilePath)
		mymode= keys[URIofTahoeFile][0]
		mykey = keys[URIofTahoeFile][1]

		handle, tempPath = tempfile.mkstemp()
		
		if (os.path.exists(tempPath) == False):
			print "ERROR: CryptHandler.Encrypt could not create temp file"
			return ""

		os.close(handle) #don't need the file to be open
		self.tempPaths.append(tempPath)

		## decrypt file using All_filecrypt
		decrypt_file(mykey, LocalPath, tempPath, mymode)
		
		# return path to the decrypted file
		return tempPath	


	######    GUI TOOL  #######
	## UpdateAndEncryptKeyFile updates the keyfile section name LocalPathPassedToEncrypt
	# to URIreturnedFromUpload, then encrypts the keyfile to a temporary location
	# and returns the path to the encrypted keyfile

	def UpdateAndEncryptKeyFile(self,URIreturnedFromUpload, LocalPathPassedToEncrypt):
		# keyfile.py
		update_section_name (LocalPathPassedToEncrypt,URIreturnedFromUpload,self.keyFilePath)

		return self.encryptKeyFile()




	######    GUI TOOL  #######
	## RemoveKeyfileEntry removes a section from the keyFile
	def RemoveKeyfileEntry (self, URIofTahoeFile):
		# keyfile.py
		remove_entry (URIofTahoeFile, self.keyFilePath)


	######    GUI TOOL MAY ONLY NEED TO BE USED ONCE  #######
        ## encryptKeyFile simply encrypts the keyfile into a temporary location
	# and returns the location
	def encryptKeyFile(self):
		handle, tempKFpath = tempfile.mkstemp()

		if (os.path.exists(tempKFpath) == False):
			print "ERROR: CryptHandler.updateAndEncryptKeyFile could not create temp file"
			return ""

		os.close(handle) #don't need the file to be open
		
		self.tempPaths.append(tempKFpath)

		# encrypt file using All_filecrypt
		encrypt_file(self.keyFileKEY,
					 self.keyFilePath,
					 tempKFpath,
					 "AES")
											  
		return tempKFpath

		
	def makeKeyfileKey(self, username, userpassword):
   
		userword = username + userpassword
		KFkey = hashlib.sha256(userword).digest()
		return KFkey  

	

	## used in conjunction with __exit__
	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.Clean()

	def Clean(self):
		for path in self.tempPaths:
			if (os.path.exists(path) == True):
				os.remove(path)
				self.tempPaths.remove(path)
