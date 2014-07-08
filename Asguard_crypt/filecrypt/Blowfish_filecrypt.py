# Written in 2014 by Tim Sargent
# Credit to Eli Bendersky 2010 http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
#
# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# No rights are reserved.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================
#
# USAGE
# ===================================================================
# These two functions will, when called, handle encryption and 
# decryption, respectivly, of any file passed to them
# 
# Arguments:
#
#	key: the encryption key
#
#	in_filename: the name of the file that is to be encrypted.
#


import os, random, struct
from Crypto.Cipher import Blowfish

def encrypt_file(key, in_filename, out_filename, chunksize=64*1024):

	if not out_filename:
		out_filename = in_filename + '.enc'

	iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(8))
	encryptor = Blowfish.new(key, Blowfish.MODE_CBC, iv)
	filesize = os.path.getsize(in_filename)

	with open(in_filename, 'rb') as infile:
		with open(out_filename, 'wb') as outfile:
			outfile.write(struct.pack('<Q', filesize))
			outfile.write(iv)

			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16 - len(chunk) % 16)

				outfile.write(encryptor.encrypt(chunk))
				
			infile.close()
			outfile.close()
#	os.remove(in_filename)
#	os.rename(out_filename, in_filename)	

def decrypt_file(key, in_filename,out_filename, chunksize=24*1024):

	if not out_filename:
		out_filename= in_filename

	with open(in_filename, 'rb') as infile:
		origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
		iv = infile.read(8)

		decryptor = Blowfish.new(key, Blowfish.MODE_CBC, iv)

		with open(out_filename, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(origsize)

