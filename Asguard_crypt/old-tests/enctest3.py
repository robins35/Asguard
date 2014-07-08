import os, random, struct
from Crypto.Cipher import AES

key= "abc123dohreami.."
infile= "blarg.txt"
outfile= "blarg.txt" 

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
	""" Decrypts a file using AES (CBC mode) with the
		given key. Parameters are similar to encrypt_file,
		with one difference: out_filename, if not supplied
		will be in_filename without its last extension
		(i.e. if in_filename is 'aaa.zip.enc' then
		out_filename will be 'aaa.zip')
	"""

	with open(in_filename, 'rb') as infile:
		origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
		iv = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, iv)

		with open(out_filename, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(origsize)

decrypt_file(key,infile,outfile)
