# NOTE: the tahoe-LAFS /bin directory will need to be in your shell PATH variable before this will run!!


import subprocess
import os
import re #regular expressions

#Upload takes the file path to the file to be uploaded
# and the tahoe path ex: "tahoe:tahoe_child/my_new_file.txt"
# the return value is the new file's URI, or the empty string 
# if there was an error
def Upload(LocalFilePath, TahoePathToSaveFile):
    #create a subprocess to run the command
    #so far this is the only way to redirect the output of a command
    #subprocess will raise an exception, OSError, when a command is not found.
    process = subprocess.Popen(["tahoe", "put", LocalFilePath, 
                                TahoePathToSaveFile],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    
    output, errors = process.communicate()
    
    print "Errors: " + errors;
    
    #remove new line at the end
    output = output.rstrip('\n')
    return output
    
def Remove(TahoePathToFile):
    f = open(os.devnull, 'w') #used to supress stdout
    retVal = subprocess.call(["tahoe", "rm", TahoePathToFile], stdout=f)
    f.close()
    return retVal
    
def Get(TahoePathToFile, LocalPathToSaveFile):
    f = open(os.devnull, 'w') #used to supress stdout
    retVal = subprocess.call(["tahoe","get",TahoePathToFile,LocalPathToSaveFile], stdout=f)
    f.close()
    return retVal

    #Get_Aliases() retrieves the aliases found in ~/.tahoe/private/aliases
    #the return value is either a list of tuples ((alias1, URI:), (alias2, URI:))
    #or if no aliases are found the return value is the empty list ()
def Get_Aliases():
    
    #create a subprocess to run the command
    #so far this is the only way to redirect the output of a command
    #subprocess will raise an exception, OSError, when a command is not found.
    process = subprocess.Popen(["tahoe", "list-aliases"], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        
    output, errors = process.communicate()
        
    # output is of form alias_name1: URI:DIR2:uri_string\n 
    #                   alias_name2: URI:DIR2:uri_string\n
    #                   \n
    
    
    tupleList = ()
    if (len(output) > 0):
        #remove the new line at the end
        output = output.rstrip('\n')
        
        #split each alias
        aliasList = output.split('\n')
        
        #now split each alias into (alias_name, URI)
        for alias in aliasList:
            new_tuple = tuple(alias.replace(' ','').split(':', 1))
            tupleList = tupleList + (new_tuple,)    

    return tupleList
    
#Get_SubTree() retrieves the subtree structure underneath 
#   the alias name TahoeAlias. TahoeAlias should be of the form "alias_name:"
#   or "alias_name:child_dir/grandchild_dir/"
#   the return value is a list of tuples. Each tuple in the list is of the form
#   (path/to/file/or/directory, URI:OfFileOrDirectory)
#   ex, if an alias named 'tahoe:' exists, and below it is a directory called
#   "tahoe_child" which contains a text file named "sample.txt" 
#   and you call Get_SubTree("tahoe:")
#   the return value will be: 
#   (   (tahoe:, URI:DIR2:so300gnwg0230r02fj0sjf0sf0)
#       (tahoe_child, URI:DIR2:adasfowefoj33r023sljb)
#       (tahoe_child/sample.txt, URI:LIT:sodfjowjef23t0jgbwef0w)
#   )
    
def Get_SubTree(TahoePathToDirectory):
    
    #create a subprocess to run the command
    #so far this is the only way to redirect the output of a command
    #subprocess will raise an exception, OSError, when a command is not found.
    process = subprocess.Popen(["tahoe", "manifest", TahoePathToDirectory], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        
    output, errors = process.communicate()
        
    
    tupleList = ()
    if (len(output) > 0):
        #remove the new line at the end
        output = output.rstrip('\n')
        
        #split each path
        pathList = output.split('\n')
        pathList[0] = pathList[0] + TahoePathToDirectory
        
        #now split each alias into (alias_name, URI)
        for path in pathList:
            new_tuple = tuple(path.split(' ', 1))
            new_new_tuple = new_tuple[::-1]
            tupleList = tupleList + (new_new_tuple,)
            
    return list(tupleList)

# New_Directory() creates a new directory
#   ex: to create a directory named dir under tahoe:tahoe_child do
#   New_Directory("tahoe:tahoe_child/dir")
# Upon success the return value is the URI of the newly created directory
# Upon failure the return value is the empty string ""
def New_Directory(TahoePathToDirectory):
    #create a subprocess to run the command
    #so far this is the only way to redirect the output of a command
    #subprocess will raise an exception, OSError, when a command is not found.
    process = subprocess.Popen(["tahoe", "mkdir", TahoePathToDirectory], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        
    output, errors = process.communicate()
    
    retVal = "";
    
    if (len(output) > 0):
        #remove the new line at the end
        output = output.rstrip('\n')
        
        retVal = output
        
    return retVal
    
#ls returns a list of the files in directory TahoePathToDirectory    
    
def ls(TahoePathToDirectory):
    #create a subprocess to run the command
    #so far this is the only way to redirect the output of a command
    #subprocess will raise an exception, OSError, when a command is not found.
    process = subprocess.Popen(["tahoe", "ls", TahoePathToDirectory], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        
    output, errors = process.communicate()
    
    output = output.rstrip('\n')
    
    contents = []
    if (len(output) > 0):
        contents = output.split('\n')
        
    return contents
    
    
#From Tahoe-LAFS:
# immutable file read-only capability string             URI:CHK:
# immutable file verify capability string               URI:CHK-Verifier:
# immutable LIT file read-only capability string        URI:LIT:
# mutable file read-write capability string             URI:SSK:
# mutable file read-only capability string              URI:SSK-RO:
# mutable file verify capability string                 URI:SSK-Verifier:    
def is_File(URI):
    pattern = 'URI:(CHK|LIT|SSK)(-Verifier|-RO)?:.*'
    
    matchObj = re.match(pattern,URI)
    
    retVal = False
    
    if (matchObj):
        retVal = True
        
    return retVal

#from Tahoe-LAFS:
# immutable directory read-only capability string       URI:DIR2-CHK:
# immutable directory verify capability string          URI:DIR2-CHK-Verifier:
# immutable LIT directory read-only capability string   URI:DIR2-LIT:
# mutable directory read-write capability string        URI:DIR2:
# mutable directory read-only capability string         URI:DIR2-RO:
# mutable directory verify capability string            URI:DIR2-Verifier:
def is_Dir(URI):
    pattern = 'URI:DIR2(-CHK|-CHK-Verifier|-LIT|-RO|-Verifier)?:.*'
    
    matchObj = re.match(pattern,URI)
    
    retVal = False
    
    if (matchObj):
        retVal = True
        
    return retVal
    
"""
#Example Usage


###### file paths ############
localPath = "/Users/danesharafinski/Desktop/tahoe.txt"  # the path to file on local machine
TahoePathToSaveFile = "tahoe:mypyupload.txt"  # the full Tahoe Path to save the file

#attempt to upload the file
retVal = Upload(localPath, TahoePathToSaveFile)

if (retVal == 0):
    print "Upload sucessful, retVal=" + str(retVal)
else:
    print "Upload failed, retVal=" + str(retVal)
    
    
#attempt to get the file
retVal = Get(TahoePathToSaveFile, localPath)

if (retVal == 0):
    print "Retrieval successful, wrote to " + localPath
else:
    print "Retrieval failed, retVal=" + str(retVal)  
    
#attempt to delete the file
retVal = Remove(TahoePathToSaveFile)

if (retVal == 0):
    print "Deletion sucessful, retVal=" + str(retVal)
else:
    print "Deletion failed, retVal=" + str(retVal)
   
   
#retrieve the aliases
print "\nALIASES........\n"
aliases = Get_Aliases()
for alias in aliases:
    print alias
    
    
print "\nSUBTREE.......\n"
#retrieve subtree
subtree = Get_SubTree("tahoe:")
for file in subtree:
    print file 
"""
