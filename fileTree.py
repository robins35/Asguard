#!/usr/bin/python

#from AG_funcs import is_Dir

class Node():
	def __init__(self, name, URI, dirFlag):
		self.children = dict()
		self.parent = None

		self.name = name
		self.URI = URI
		self.isDir = dirFlag#is_Dir(self.URI)

	def addChild(self, name, URI, dirFlag):
		child = Node(name, URI, dirFlag)
		child.parent = self
		self.children[name] = child

class Tree():
	def __init__(self, rootname, rootURI):
		self.root = Node(rootname, rootURI, True)
		self.ptr = self.root
		self.count = 1

	def hasChild(self, name):
		if name in self.ptr.children:
			return True
		return False

	def resetPtr(self):
		self.ptr = self.root

	def insert(self, fileInfo):
		ptr = self.root
		path = fileInfo[0]
		uri = fileInfo[1]
		dirFlag = fileInfo[2]
		chain = path.split('/')
		name = chain[-1]

		for n in chain:
			if n not in ptr.children:
				ptr.addChild(name, uri, dirFlag)
			ptr = ptr.children[n]

	def listDir(self, dirPath):
		ptr = self.root
		chain = dirPath.split('/')
		if chain[0] != '':
			for n in chain:
				if n not in ptr.children:
					print "ILLEGAL PATH PASSED TO Tree.listDir()"
					return
				ptr = ptr.children[n] 
		l = ptr.children.values()
		return l

	def checkDirPath(self, path):
		ptr = self.root
		chain = path.split('/')

		if chain[0] != '':
			for n in chain:
				if n not in ptr.children:
					return False
				ptr = ptr.children[n]
		if not ptr.isDir: return False
		return True
