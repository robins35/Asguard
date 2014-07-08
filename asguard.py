#!/usr/bin/python

import sys
from os import listdir
import os
import shutil
#from AG_funcs import Upload, Get_SubTree, is_Dir, ls, Get, Get_Aliases, New_Directory, Remove
from AG_funcs_REST import *
from Asguard_crypt.CryptHandler import CryptHandler
from PyQt4 import QtGui, QtCore
from fileTree import Tree

def cleanPath(pathstr):
	"""retstr = pathstr.split('/')
	if retstr[-1] == '..':
		retstr = retstr[:-2]
	retstr = '/'.join(retstr[1:])
	if retstr[:2] == "//":
		retstr = retstr[1:]
"""
	if pathstr:
		if pathstr[0] == "/":
			pathstr = pathstr[1:]	
	return pathstr

class MainWindow(QtGui.QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.initUI()


	def initUI(self):
		self.fileBrowser = FileBrowser(self)
		self.setCentralWidget(self.fileBrowser)

		uploadFile = QtGui.QAction(QtGui.QIcon('images/cloud-upload.png'), 'Upload', self)
		uploadFile.setShortcut('Ctrl+U')
		uploadFile.setStatusTip('Upload File')
		uploadFile.triggered.connect(self.fileBrowser.uploadDialog)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(uploadFile)

		self.setGeometry(300, 300, 650, 450)
		self.setWindowTitle('Asguard')
		self.show()

	def showDialog(self):
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Upload file', '/home')
		localPath = fname
		tahoeDIR = "tahoe:"
		saveFileAs = fname.split("/")[-1]

		retVal = ''
		#encrypt file
		pathEnc = self.cryptHandle.Encrypt(localPath, "AES")

		retVal = Upload(pathEnc, tahoeDIR + saveFileAs)

		if retVal != '':
			print "Upload successful, retVal=" + str(retVal)
			kfPath = self.cryptHandle.UpdateAndEncryptKeyFile(retVal,
								 localPath)
			# reUpload the keyfile
			Upload(kfPath, self.URI + "/keyfile")
			self.fileBrowser.repopulateList(self.fileBrowser.remoteList)
		else:
			print "Upload failed, retVal=" + str(retVal)

class LocalList(QtGui.QListWidget):
	def __init__(self, parent):
		super(LocalList, self).__init__(parent)
		self.parent = parent
		self.setDragEnabled(True)
		self.setAcceptDrops(True)

	def startDrag(self, e):
		mimeData = QtCore.QMimeData()
		mimeData.setText(self.currentItem().text())
		drag = QtGui.QDrag(self)
		drag.setMimeData(mimeData)
		dropAction = drag.exec_()

	def dragEnterEvent(self, e):
		if e.source() != self:
			e.accept()

	def dragMoveEvent(self, e):
		e.accept()

	def dropEvent(self, e):
		remoteName = str(e.mimeData().text())
		self.parent.download(remoteName)
		"""remotePath = self.parent.URI + "/" + self.parent.remotedir + "/" + remoteName

		localPath = self.parent.localdir + "/" + remoteName
		if localPath[:2] == "//":
			localPath = localPath[1:]

		retVal = Get(str(remotePath), str(localPath))

		if retVal:
			print "SUCCESS"
			self.parent.repopulateList(self)
		else:
			print "Failed to download " + remotePath"""
	

class RemoteList(QtGui.QListWidget):
	def __init__(self, parent):
		super(RemoteList, self).__init__(parent)
		self.parent = parent
		self.setAcceptDrops(True)
		self.setDragEnabled(True)

	def startDrag(self, e):
		mimeData = QtCore.QMimeData()
		mimeData.setText(self.currentItem().text())
		drag = QtGui.QDrag(self)
		drag.setMimeData(mimeData)
		dropAction = drag.exec_()

	def dragEnterEvent(self, e):
		print "MimeText: " + e.mimeData().text()
		if e.source() != self:
			e.accept()

	def dragMoveEvent(self, e):
		e.accept()

	def dropEvent(self, e):
		localPath = self.parent.localdir + "/" + e.mimeData().text()
		saveFileAs = localPath.split("/")[-1]
		savePath = self.parent.remotedir
		if self.parent.remotedir:
			savePath = savePath + "/"
		savePath = savePath + saveFileAs

		#encrypt file
		pathEnc = self.parent.cryptHandle.Encrypt(str(localPath), "AES")

		retVal = Upload(pathEnc, str(self.parent.URI + "/" + savePath))

		if retVal != '':
			print "Upload successful, retVal=" + str(retVal)
			kfPath = self.parent.cryptHandle.UpdateAndEncryptKeyFile(retVal,
								 str(localPath))
			# reUpload the keyfile
			Upload(kfPath, self.parent.URI + "/keyfile")
			self.parent.updateFileTree()
			self.parent.repopulateList(self.parent.remoteList)
		else:
			print "Upload failed, retVal=" + str(retVal)


		e.accept()

class DirectoryListItem(QtGui.QListWidgetItem):
	def __init__(self, parent):
		super(DirectoryListItem, self).__init__(parent)

	def dragEnterEvent(self, e):
		print "Hovering over directory!"
		e.accept()

class LoginDialog(QtGui.QDialog):
	def __init__(self, parent):
		QtGui.QDialog.__init__(self,parent)

		self.resize(250, 150)
		self.buttonBox = QtGui.QDialogButtonBox(self)
		self.buttonBox.setGeometry(QtCore.QRect(130, 100, 100, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.unameLab = QtGui.QLabel(self)
		self.unameLab.setGeometry(QtCore.QRect(10, 10, 65, 32))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.unameLab.setFont(font)
		self.unameLab.setText("Username:")
		self.usrNameEdit = QtGui.QLineEdit(self)
		self.usrNameEdit.setGeometry(QtCore.QRect(80, 10, 150, 32))
		self.usrNameEdit.setFont(font)
		self.pwLab = QtGui.QLabel(self)
		self.pwLab.setGeometry(QtCore.QRect(10, 50, 65, 32))
		self.pwLab.setFont(font)
		self.pwLab.setText("Password:")
		self.pwEdit = QtGui.QLineEdit(self)
		self.pwEdit.setEchoMode(QtGui.QLineEdit.Password)
		self.pwEdit.setGeometry(QtCore.QRect(80, 50, 150, 32))
		self.pwEdit.setFont(font)
		#self.retranslateUi(self)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.processUnamePw)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
		QtCore.QMetaObject.connectSlotsByName(self)

	def processUnamePw(self):
		parent = self.parent()
		parent.username = self.usrNameEdit.text()
		parent.password = self.pwEdit.text()
		self.accept()

class FileBrowser(QtGui.QWidget):
	def __init__(self, parent):
		# DEFINE INSTANCE VARS
		#self.URI = 'URI:DIR2:muyiptb3avposlswpk7dwd6i6m:al2ypupmygotdo73undrq2az4dqjkh3bkcfelj5nmhtcffhoakvq' 
		# GRABBING ROOT ALIAS AND URI
		#self.alias, self.URI = Get_Aliases()[0]
		super(FileBrowser, self).__init__()
		self.username = ''
		self.password = ''
		self.loginDialog = LoginDialog(self)
		results = self.loginDialog.exec_()
		print "RESULTS: " + str(results)
		print "USERNAME: " + self.username
		print "PASSWORD: " + self.password


		with open(os.path.expanduser("~") + "/.tahoe/private/aliases") as f:
			content = f.readline()
			while content == "\n":
				content = f.readline()
		self.alias, self.URI = content.rstrip().split(' ')
		self.localdir = os.path.expanduser("~")
		self.remotedir = ''
		self.remoteFileTree = Tree('', self.URI)

		self.initKey()


		self.initUI()

		#print "ALIASES: "
		#for al in self.aliases:
		#	print al

	def initKey(self):
		retVal = ""
		if (Get(self.URI + "/keyfile", "keyfile")):
		#if os.path.isfile("keyfile"):
			self.cryptHandle = CryptHandler("keyfile", self.username, self.password, True)
		else:
			print "Failed to download remote keyfile, creating new one"
			open("keyfile", "w").close()
			
			self.cryptHandle = CryptHandler("keyfile", self.username, self.password, False)
			#self.cryptHandle.encryptKeyFile()
			path = self.cryptHandle.encryptKeyFile()
			retVal = Upload(path, str(self.URI + "/keyfile"))
			if (retVal != ''):
				print "Upload sucessful, retVal=" + str(retVal)
			else:
				print "Upload failed, retVal=" + str(retVal)


	def initUI(self):
		hbox = QtGui.QVBoxLayout(self)

		self.localList = LocalList(self)
		self.remoteList = RemoteList(self)#QtGui.QListWidget(self)

		splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		splitter.addWidget(self.localList)
		splitter.addWidget(self.remoteList)

		
		self.dlBtn = QtGui.QPushButton("Download", self)
		self.dlBtn.clicked.connect(self.download)
		self.dlBtn.setMaximumWidth(100)
		self.mkDirBtn = QtGui.QPushButton("Make Dir", self)
		self.mkDirBtn.clicked.connect(self.makeRemoteDir)
		self.mkDirBtn.setMaximumWidth(100)
		self.rmBtn = QtGui.QPushButton("Remove Dir/File", self)
		self.rmBtn.clicked.connect(self.removeRemDirFile)
		self.rmBtn.setMaximumWidth(130)

		self.ulBtn = QtGui.QPushButton("Upload", self)
		self.ulBtn.clicked.connect(self.upload)
		self.locMkDirBtn = QtGui.QPushButton("MakeDir", self)
		self.locMkDirBtn.clicked.connect(self.makeLocalDir)
		self.locRmBtn = QtGui.QPushButton("Remove Dir/File")
		self.locRmBtn.clicked.connect(self.removeLocDirFile)

		hspacer = QtGui.QHBoxLayout()
		hspacer.addWidget(self.ulBtn)
		hspacer.addWidget(self.locMkDirBtn)
		hspacer.addWidget(self.locRmBtn)
		hspacer.addStretch(1)
		hspacer.addWidget(self.dlBtn)
		hspacer.addWidget(self.mkDirBtn)
		hspacer.addWidget(self.rmBtn)

		hbox.addLayout(hspacer)
		hbox.addWidget(splitter)
		self.setLayout(hbox)
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

		# SIGNALS/SLOTS
		self.localList.itemDoubleClicked.connect(self.changeLocalDir)
		self.remoteList.itemDoubleClicked.connect(self.changeRemoteDir)

		self.updateFileTree()
		self.repopulateList(self.localList)
		self.repopulateList(self.remoteList)

	def updateFileTree(self):
		self.remoteFileTree = Tree('', self.URI)
		files = getSubTree(self.URI)
		self.URIMap = {}
		#for ent in files:
		for ent in files:
			self.remoteFileTree.insert(ent)
			self.URIMap[ent[0]] = ent[1] 

	def uploadDialog(self):
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Upload file', '/home')
		if fname == "": return
		localPath = fname
		saveFileAs = fname.split("/")[-1]
		savePath = self.remotedir
		if self.remotedir:
			savePath = savePath + "/"
		savePath = savePath + saveFileAs
		print "YO WE'RE UPLOADING!!"
		print str(localPath), str(self.URI + "/" + savePath)

		####
		#encrypt file
		pathEnc = self.cryptHandle.Encrypt(str(localPath), "AES")

		retVal = Upload(pathEnc, str(self.URI + "/" + savePath))

		if retVal != '':
			print "Upload successful, retVal=" + str(retVal)
			kfPath = self.cryptHandle.UpdateAndEncryptKeyFile(retVal,
								 str(localPath))
			# reUpload the keyfile
			Upload(kfPath, self.URI + "/keyfile")
			self.updateFileTree()
			self.repopulateList(self.remoteList)
		else:
			print "Upload failed, retVal=" + str(retVal)

		####
		#retVal = Upload(str(localPath), str(self.URI + "/" + savePath))

		#if (retVal != ''):
		#	print "Upload sucessful, retVal=" + str(retVal)
		#	#self.remoteFileTree.insert(ent)
		#	self.updateFileTree()
		#	self.repopulateList(self.remoteList)
		#else:
		#	print "Upload failed, retVal=" + str(retVal)

	def removeLocDirFile(self):
		if not self.localList.selectedItems():
			print "NOTHING IS SELECTED"
			return
		name = str(self.localList.selectedItems()[0].text())
		if name == "..":
			print "CANNOT REMOVE A DIRECTORY YOU ARE CURRENTLY IN!"
			return
		name = self.localdir + "/" + name
		if name[1] == "/":
			name = name[1:]

		if os.path.isfile(name):
			os.remove(name)
			print name
		elif os.path.isdir(name):
			shutil.rmtree(name)
			print name
		else:
			print "ERROR: Selected value is neither file nor directory?"
			return
		self.repopulateList(self.localList)

	def makeLocalDir(self):
		dirName, ok = QtGui.QInputDialog.getText(self, "New Local Directory", "Enter directory name")

		if ok:
			dirPath = str(self.localdir + "/" + dirName)
			if dirPath[1] == "/":
				dirPath = dirPath[1:]
			if not os.path.exists(dirPath):
				try:
					os.mkdir(dirPath)
				except OSError, e:
					print "FAILED TO MAKE DIRECTORY: " + dirPath
					print str(e)
					return
				self.repopulateList(self.localList)
				print "SUCCESS"
			else:
				print "Directory already exists"
		else:
			print "FAILURE"


	def download(self, fileName = ""):
		if not fileName:
			if not self.remoteList.selectedItems():
				print "NOTHING IS SELECTED"
				return
			else:
				fileName = str(self.remoteList.selectedItems()[0].text())

		remotePath = self.URI + "/" + self.remotedir + "/"
		if remotePath[-2:] == "//":
			remotePath = remotePath[:-1]
		remotePath = remotePath + fileName

		uri = ""
		if (len(self.remotedir) == 0):
			uri = self.URIMap[fileName]
		else:
			uri = self.URIMap[self.remotedir + "/" + fileName]
		

		localPath = self.localdir + "/" + fileName
		if localPath[:2] == "//":
			localPath = localPath[1:]


		retVal = Get(remotePath, localPath)

		if retVal:
			print "SUCCESS"		      
			self.repopulateList(self.localList)
			# decrypt the file
			if (uri == ""):
				print "Failed to find URI for file, cannot decrypt file"
			else:
				path = self.cryptHandle.Decrypt(localPath, uri)
				#move file from the temp location to user's loc
				shutil.move(path, localPath)
		else:
			print "Failed to download " + remotePath

	def upload(self):
		if not self.localList.selectedItems():
			print "NOTHING IS SELECTED"
			return
		localName = str(self.localList.selectedItems()[0].text())
		localPath = self.localdir + "/" + localName

		saveFileAs = localName
		savePath = self.remotedir
		if self.remotedir:
			savePath = savePath + "/"
		savePath = savePath + saveFileAs

		#encrypt file
		pathEnc = self.cryptHandle.Encrypt(localPath, "AES")

		#retVal = Upload(localPath, self.URI + "/" + savePath)
		retVal = Upload(pathEnc, self.URI + "/" + savePath)

		if retVal != '':
			print "Upload successful, retVal=" + str(retVal)
			kfPath = self.cryptHandle.UpdateAndEncryptKeyFile(retVal,
								 localPath)
			# reUpload the keyfile
			Upload(kfPath, self.URI + "/keyfile")
			self.updateFileTree()
			self.repopulateList(self.remoteList)
		else:
			print "Upload failed, retVal=" + str(retVal)
		

	def makeRemoteDir(self):
		text, ok = QtGui.QInputDialog.getText(self, "New Remote Directory", "Enter directory name")

		if ok:
			if (self.remotedir):
				text = "/" + str(text)
			
			retVal = New_Directory(str(self.URI + "/" + self.remotedir + text))

			if retVal:
				self.updateFileTree()
				self.repopulateList(self.remoteList)
				print "SUCCESS"
			else:
				print "FAILURE"

	def removeRemDirFile(self):
		if not self.remoteList.selectedItems():
			print "NOTHING IS SELECTED"
			return
		name = str(self.remoteList.selectedItems()[0].text())
		if name == "..":
			print "CANNOT REMOVE A DIRECTORY YOU ARE CURRENTLY IN!"
			return
		name = self.remotedir + "/" + name
		if name[0] == "/": name = name[1:]

		retVal = Remove(self.URI + "/" + name)

		if retVal:
			uri = self.URIMap[name]
			self.cryptHandle.RemoveKeyfileEntry(uri)
			kfPath = self.cryptHandle.encryptKeyFile()
			Upload(kfPath, self.URI + "/keyfile")
			self.updateFileTree()
			self.repopulateList(self.remoteList)
			print "SUCCESS"
		else:
			print "FAILURE"

	def local_ls(self):
		files = []
		dirlist = []
		for (dirpath, dirnames, filenames) in os.walk(self.localdir): 
			files.extend(filenames)
			dirlist.extend(dirnames)
			break
		return (files, dirlist)

	def remote_ls(self):
		files = []
		dirlist = []

		newlist = self.remoteFileTree.listDir(self.remotedir)
		for ent in newlist:
			if (ent.isDir):
				dirlist.append(ent.name)
			else:
				files.append(ent.name)

		return (files, dirlist)

	def repopulateList(self, listWidget):
		#repopulating local directories
		if (listWidget == self.localList):
			files, dirlist = self.local_ls()
		#repopulating remote directories
		elif(listWidget == self.remoteList):
			files, dirlist = self.remote_ls()
			
		listWidget.clear()
		dirlist.append('..')
		dirlist.sort()
		files.sort()

		for d in dirlist:
			#item = QtGui.QListWidgetItem(listWidget)
			item = DirectoryListItem(listWidget)
			item.setText(d)
			item.setIcon(QtGui.QIcon('images/directory-icon.gif'))
		
		listWidget.addItems(files)
		listWidget.setFrameShape(QtGui.QFrame.StyledPanel)


	def changeLocalDir(self):
		sender = self.sender()
		
		newdir = str(sender.selectedItems()[0].text())
		
		if newdir == "..":
			newdir = "/".join(self.localdir.split("/")[:-1])
		else:
			newdir = self.localdir + "/" + newdir

		if not os.path.isdir(newdir):
			print newdir + " is not a directory"
		else:
			self.localdir = newdir
			self.repopulateList(sender)

	def changeRemoteDir(self):
		sender = self.sender()
		newdir = str(sender.selectedItems()[0].text())
		if newdir == "..":
			newpath = "/".join(self.remotedir.split("/")[:-1])
		else:
			newpath = self.remotedir + '/' + newdir
		newpath = cleanPath(newpath)

		if self.remoteFileTree.checkDirPath(newpath):
			self.remotedir = newpath
			self.repopulateList(sender)
		else:
			print newpath + " is not a directory"

def main():
	app = QtGui.QApplication(sys.argv)
	win = MainWindow()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
