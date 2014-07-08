README
Asguard v1

INTRO
---------------------------------
  Welcome and thank you for choosing to use the Asguard secure file storage system. Asguard is developed to provide an easy and secure way of backing up your important data. Many other file systems require a third party to host a server that you store your data on. The flaw there is you must then trust that the third party is treating your data confidentially. Even if you do trust the third party, they would still be vulnerable to attacks, as no computer connected to the internet is never 100% secure. Storing data on your own computer has the same vulnerabilities, if not worse, than a third party since your personal computer is likely less secure than a third party's systems. Even if you take your important data, put it on an external hard drive, and hide the drive, it still is vulnerable to being found and stolen. 
  Asguard solves these all these problems by taking the data you want to store, encrypting it, and chopping it up and handing the pieces to other users of the system. Users dont know what pieces of whose data they are holding onto and therefore the possibility of your data getting compromised drops drasticly!

TAHOE-LAFS
---------------------------------
  Asguard uses as it's storage medium the open source application Tahoe-LAFS. Tahoe is an open source, peer to peer, distributed file system. Users of Tahoe join a network of other users, all of whom offer space on their machines to store peices of other people's data. You send your data through a "Gateway" which duplicates and encrypts your data before segmenting it and storing different segments on different computers. The algorithm knows where different pieces of the file are stored so it can rebuild the file later. Files are duplicated to protect against the scenario that a machine holding part of a file goes offline. Duplicating the pieces ensures that even if some machines are down, theres enough redundant pieces to rebuild the data.
  Tahoe's gateway method of storing data presents a flaw in conveinience. Your data can only be accessed via the same gateway that you sent it to. Normally this gateway is on your own machine, meaning that you can only access your data from the computer you stored it with. Thisis all well and good buut in the event that your computer breaks down, your data is lost forever. Remote, public gateways exist but your data is insecure on it's way to the gateway. Asguard resolves this flaw by encrypting your data before it leaves your computer. Asguard also provides users with a simple GUI interface to interact with the system. Because Tahoe also encrypts data as it goes through the gateway, your data is doubly encrypted as well as split up and scattered. 
  
  More info on Tahoe-LAFS can be found at https://tahoe-lafs.org/trac/tahoe-lafs

HOW IT WORKS
---------------------------------
Step 1: Download and Install Asguard.
As you are reading this, chances are you've already downloaded Asguard. Installation instructions are below.

Step 2: Log in. 
When you run Asguard you are first presented with a standard username/password prompt. Asguard is a decentralized system and therefore does not provide a mechanism for verifying credentials. These credentials together are a key to finding and decrypting a file that contains all the information about the storage of your other files (known as the Keyfile). If you provide the wrong credentials, you wont be able to access your files. Instead you will be offered a fresh new empty sile storage system. MAKE SURE TO REMEMBER YOUR CREDENTIALS there is no way to recover credentials when lost. 
WARNING: User credentials form the weakest part of any security system. Therefore the longer and more complicated your credentials are, the better. While Tahoe's security stems from being only able to access data from the same computer it was stored with, Asguard sacrifices this security measure to provide the conveinence of accessing secure data anywhere. It is advised that between your username and your password you use UPPER and lower case letters in conjunction with numbers and any other characters you can find on your keyboard.  

Step 3: Navigate the file system.
Asguard uses a FTP-like dual window interface, with the contents of your local file system in the left hand window and the Files stored on Asguard in the right hand window. The interface also allows you to navigate directories/folders in both systems, as well as permiting creation and removal of directories.
WARNING: Removing a directory/folder will recursivly delete all files and folders contained within.

Step 4: Upload a file.
Select a file or directory/folder in the Local window and either click the "Upload button" or drag the file to the Asguard window. Asguard then encrypts your file using the chosen encryption algorithm (default is AES) with a randomly generated key. The data is then sent to a public Tahoe-LAFS gateway for storage The key and the location of the file are then recorded in the keyfile for later retrieval. By default, Asguard does not delete the copy of the file stored on the local machine.

Step 5: Download a file.
Simply step 4 in reverse. Select a file or directory/folder in the Asguard window and either click the "Download" button or drag the file to the Local window. Asguard retrieves the file from the Tahoe-LAFS gateway and decrypts it using the information stored in the keyfile.

INSTALLATION
---------------------------------


BUGS/DESIRED FEATURES
---------------------------------
*Alternate Algorithm option: There already are working implementations of two other encryption algorthims in the source code, but currently there isnt an option from the user interface to use them instead of the default AES-256 algorithm. To be fair, AES is currently industry standard and is as secure, if not moreso than the other algorithms.
*Clobber option: The option to delete the original file from the local machine. The code already exists, theres just no way to access it from the user interface.

LEGAL/CREDITS
---------------------------------
Asguard was developed as an undergradtate senior software development project at Western Washington University. As this was an academic exercise with a small team, there is the chance that the original developers will leave the project after graduation. The source code was developed using open source code and will remain open source under the liscense below. We leave this project to the community for use and future development.
The original collaborators were Paul Croft, Caiden Robinson, Tim Sargent, and Dane Sharafinsky. Dr Christopher Reedy acted as an adivisor on the project.

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