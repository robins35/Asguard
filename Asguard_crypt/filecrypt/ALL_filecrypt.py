# Written in 2014 by Tim Sargent
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

# USAGE
# ===================================================================
# These two functions will, when called, handle encryption and 
# decryption, respectivly, of any file passed to them
# 
# Arguments:
#
#	password: Plaintext password obtained either from the user or 
#		randomly generated. The password will be hashed using 
#		SHA-256 and the digest will be used as the encryption 
#		key.
#
#	in_filename: the name of the file that is to be encrypted.
#
#	mode: The selected encryption algorithm to be used to encrypt 
#		the file.

	
import hashlib
import keyfile

def encrypt_file(key, in_filename,out_filename, mode):

	
	if mode == "AES":
		from AES_filecrypt import encrypt_file 
		encrypt_file(key, in_filename, out_filename)
	elif mode == "Blowfish":
		from AES_filecrypt import encrypt_file 
		encrypt_file(key, in_filename, out_filename)
	elif mode == "CAST":
		from CAST_filecrypt import encrypt_file 
		encrypt_file(key, in_filename, out_filename)
	else: 
		from AES_filecrypt import encrypt_file 
		encrypt_file(key, in_filename, out_filename)	
		
def decrypt_file(key, in_filename, out_filename, mode):

	
	if mode == "AES":
		from AES_filecrypt import decrypt_file 
		decrypt_file(key, in_filename,out_filename)
	elif mode == "Blowfish":
		from AES_filecrypt import decrypt_file 
		decrypt_file(key, in_filename,out_filename)
	elif mode == "CAST":
		from CAST_filecrypt import decrypt_file 
		decrypt_file(key, in_filename,out_filename)
	else: 
		from AES_filecrypt import decrypt_file 
		decrypt_file(key, in_filename,out_filename)	
	



