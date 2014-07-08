#!/usr/bin/python

import os
from httplib2 import Http
import re
import json


#Get returns True upon success and False upon failure
#uses default port number 3456
# URI should be the URI of the file one wishes to retrieve **does not
#    need to be preceded by URI of tahoe: alias**
# Dest_Path should be the path where the file should be saved
# to. The file at Dest_Path is overwritten or created if not
# exist
def Get(URI, Dest_Path):
    http = Http()

    URI = re.sub(':','%3A', URI) #tahoe says having colons is bad
    addr = "http://127.0.0.1:3456/uri/" + URI

    okay = True

    try:
        resp, content = http.request(addr, "GET")
        if resp.status >= 400:
            okay = False
    except IOError:
        print "Could not connect to 127.0.0.1:3456"
        okay = False
        
    if (okay):
        try:
            dfile = open(Dest_Path, 'wb') #open for writing in binary format
            dfile.write(content)
            dfile.close()
        except IOError:
            print "Could not create " + Dest_Path
            okay = False

    return okay



#Upload returns the newly created URI upon success
# returns the empty string upon failure
# LocalPath should be the path to the local file to be uploaded
# TahoeURIPath should be the URI for the tahoe: alias followed
# by the path to the destination file
# ex: TahoeURIPath == URI:DIR2:ydybelxuqr6wr/tahoe_child/new_upload.txt

def Upload(LocalPath, TahoeURIPath):
    http = Http()
    print TahoeURIPath
    TahoeURIPath = re.sub(':','%3A', TahoeURIPath) #tahoe says having colons is bad
    addr = "http://127.0.0.1:3456/uri/" + TahoeURIPath

    content = ""
    okay = True

    try:
        fileh = open(LocalPath, "rb")

    except IOError:
        print "File " + LocalPath + " not found"
        okay = False

    if (okay):
        try:
            response, content = http.request(addr, "PUT", fileh)

            if response.status >= 400:
                print response
                content = ""
        except IOError:
            print "Could not connect to 127.0.0.1:3456"

    #content contains URI of uploaded file
    #else content is the empty string
    return content


#Remove returns the URI of the deleted file upon success
# returns the empty string if there was a failure
# TahoeURIPath should be the URI for the tahoe: alias followed
# by the path to the destination file
# ex: TahoeURIPath == URI:DIR2:ydybelxuqr6wr/tahoe_child/new_upload.txt
def Remove(TahoeURIPath):
    http = Http()

    TahoeURIPath = re.sub(':','%3A', TahoeURIPath) #tahoe says having colons is bad
    addr = "http://127.0.0.1:3456/uri/" + TahoeURIPath

    content = ""

    try:
        response, content = http.request(addr, "DELETE")

        if response.status >= 400:
            content = ""

    except IOError:
        print "Could not connect to 127.0.0.1:3456"

    return content
        

#New_Directory creates a new directory
# TahoeURIPath should be the URI for the tahoe: alias followed
# by the path to the destination directory
# ex: TahoeURIPath == URI:DIR2:ydybelxuqr6wr/tahoe_child/new_dir
def New_Directory(TahoeURIPath):
    http = Http()

    TahoeURIPath = re.sub(':', '%3A', TahoeURIPath) #tahoe says having colons is bad

    addr = "http://127.0.0.1:3456/uri/" + TahoeURIPath + "?t=mkdir"

    try:
        response, content = http.request(addr, "PUT")

        if response.status >= 400:
            content = ""

    except IOError:
        print 'Could not connect to 127.0.0.1:3456'

    return content

#Move will move a tahoe-located file to a different
#tahoe directory
# If New_TahoeURIPath already contains a file
# then it file will be replaced by the file specified
# by Old_TahoeURIPath
# Move will return True upon success and False upon failure
# Old_TahoeURIPath and New_TahoeURIPath should be the complete path
# ie: Odl_TahoeURIPath == URI:DIR2:ydybelxuqr6wr/tahoe_child/new_upload.txt
# ie: New_TahoeURIPath == URI:DIR2:ydybelxuqr6wr/tahoe_child/sub_dir1/sub_dir2/new_upload.txt
def Move(Old_TahoeURIPath, New_TahoeURIPath):
    http = Http()

    okay = True

    Old_TahoeURIPath = re.sub(':', '%3A', Old_TahoeURIPath) #tahoe says having colons is bad
    New_TahoeURIPath = re.sub(':', '%3A', New_TahoeURIPath)

    #pull out old filename
    old_name = re.search('^.*\/([a-z0-9_]+\.?[a-z]*)$', Old_TahoeURIPath, re.I)
    if(old_name):
        old_name = old_name.group(1)
    else:
        print "Error: Could not extract filename from Old_TahoeURIPath"
        okay = False

    #pull out new filename
    new_name = re.search('^.*\/([a-z0-9_]+\.?[a-z]*)$', New_TahoeURIPath, re.I)
    if(new_name):
        new_name = new_name.group(1)
    else:
        print "Error: Could not extract filename from New_TahoeURIPath"
        okay = False

    if (okay):
        #remove filenames and trailing "/" from paths
        Old_TahoeURIPath = Old_TahoeURIPath[:-(len(old_name) + 1)]
        New_TahoeURIPath = New_TahoeURIPath[:-(len(new_name) + 1)]
        addr = "http://127.0.0.1:3456/uri/" + Old_TahoeURIPath+ "?t=relink&from_name="+ old_name + "&to_dir=" + New_TahoeURIPath + "&to_name=" + new_name + "&replace=only-files"

        print "URL = " + addr

        try:
            response, content = http.request(addr, "POST")
                
        except IOError:
            print "Could not connect to 127.0.0.1:3456"
            okay = False

        if response.status >= 400:
            code = response.status
            okay = False
            print "Error: "
            if (code == 404):
                print "Source dir/file or destination dir does not exist"
                print content
            elif (code == 400):
                print "Source or destination path has non-directory entry"
            elif (code == 409):
                print "Cannot replace a directory"
            else:
                print "Unknown code " + str(response.status)

    return okay

# ls() will return the the contents of the directory
# located at TahoeURIPath
# the return value is a list of dictionaries (one dictionary for each file/dir)
# these are the main fields in each dictionary:
# "name" (name of file or directory)
# "type" (either 'dirnode' or 'filenode')
# "rw_uri" (the direct URI to that file or directory)
#  there are several other fields as well which may or may not 
# be needed in later development such as Read-Only URI's
# and link / create times
def ls(TahoeURIPath):
    http = Http()

    TahoeURIPath = re.sub(':', '%3A', TahoeURIPath)

    addr = "http://127.0.0.1:3456/uri/" + TahoeURIPath + "?t=json"

    okay = True

    try:
        response, content = http.request(addr, "GET")
        if (response.status >= 400):
            okay = False

    except IOError:
        print "Could not connect to 127.0.0.1:3456"
        return None

    # list of dictionaries describing each file or dir
    dict_list = list()

    if (okay):
        # content is in json format
        data = json.loads(content)

        #this won't make much sense unless you look at
        #the structure of JSON data "data"
        if (data[1].has_key("children")):
            list_keys = data[1]["children"].keys()
            for key in list_keys:
                new_dict = data[1]["children"][key][1]
                new_dict['name'] = key
                new_dict['type'] = data[1]["children"][key][0]
                dict_list.append(new_dict)

    return dict_list

def getSubTree(tahoeUriPath):
	return getSubTreeR(tahoeUriPath, "")

def getSubTreeR(tahoeUriPath, normalPath):
	fileList = []
	currentDir = ls(tahoeUriPath)
	if not currentDir:
		return []

	for f in currentDir:
		if "rw_uri" in f: uri = f["rw_uri"]
		else: uri = f["ro_uri"]

		path = normalPath + "/" + f["name"]
		if path[0] == "/": path = path[1:]

		if f["type"] == "dirnode":
			fileList.append((path, uri, True))
			fileList.extend(getSubTreeR(uri, path))
		else:
			fileList.append((path, uri, False))

	return fileList

#######     Example Usage ########################
#######  *note You will need to modify the tahoe: URI ########




###the URI of your tahoe: alias (find this out by running: tahoe manifest)
#uri = "URI:DIR2:tq5weh3oofi2i6ajvaw2jvib6q:z5fo2ymfkonjswjwnno2ws5arwd7gqqi4gyg6grdtq2mwgrru2gaa"



#print "Filename to upload: "
#filename_up = raw_input()

#tahoe_path = uri + "/" + filename_up + "?"

#print "Going to upload: " + tahoe_path

#new_uri =  Upload(filename_up, tahoe_path)

#print "uploaded uri: " + new_uri

### dont judge me on these nested if's I was tired and wanted to go home

#if (new_uri):
#    print "Upload successful, retrieve file as:"
#    filename_dn = raw_input()
#    print "Getting " + filename_up + " as " + filename_dn + "..."
#    
#    result = Get(new_uri, filename_dn)
#    
#    if (result):
#        print "Get successful, press Enter to remove file"
#        print "Removing " + filename_up + " from tahoe-lafs"
#        deleted_uri = Remove(uri + "/" + filename_up)
#        if (deleted_uri):
#            print "Remove successful, done"
#        else:
#            print "Remove failed, aborting"
#    else:
#        print "Get failed, aborting"
#else:
#    print "Upload failed, aborting"


## example usage of Move()

#old_uri_path = "URI:DIR2:ci6dyibgojgvvfstfpsxnj5pgq:ql3hnaxzkhgneghh5vk3ukizafzzlrhceqdx7mwfb5vwo3khppnq/open.png"
#new_uri_path = "URI:DIR2:ci6dyibgojgvvfstfpsxnj5pgq:ql3hnaxzkhgneghh5vk3ukizafzzlrhceqdx7mwfb5vwo3khppnq/new_dir_from_AG/open.png"

#print "Attempting to move..."
#if(Move(old_uri_path, new_uri_path)):
#    print "move success!"
#else:
#    print "move failed"
