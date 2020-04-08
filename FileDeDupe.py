import os
from FileDefinition import FileDefinition
from FileDuplicateData import FileDuplicateData
            

#
# Stores data about the files we are considering for de-duplication.
# Has the ability to add files for consideration and to delete files.
#
class FileDeDupe:

        # constructor, takes a path which will be recursivly searched for files
        def __init__(self, path, verbose=True):

            self._fileDefsByPath = {}                                       # stores files in dictionary object keyed by their full path      
            self._fileSizes = {}                                            # stores lists of files in dictionary object keyed by their byte length

            self.PrintHeader()
            self.AddFilesInPath(path, verbose)
        

        # prints header and disclaimer information to the output
        def PrintHeader(self):
            print ("**************************")
            print ("*                        *")
            print ("*     FileDeDupe 1.0     *")
            print ("*                        *")
            print ("**************************\n")
            print ("DISCLAIMER: This software will DELETE files from your file system.")
            print ("Only ever operate on a COPY of your data and ensure the output is as")
            print ("required before deleting any original data.")
            print ("Your use of this software is ENTIRELY AT YOUR OWN RISK.")
            print ("NOTE: Symlinks are simply ignored by this program.")

            return
            

        # takes a path and recursively goes through it, adding a new FileDefinition object for each file found in the app's data store
        def AddFilesInPath(self, path, verbose=True):

            if (verbose):
                print ("\n\nINDEXING FILES RECURSIVELY FROM: " + path + ":\n")

            if (os.path.isdir(path)):
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        if (os.path.isfile(os.path.join(dirpath, filename))):

                            try:
                                fileDef = FileDefinition(dirpath, filename)
                            except:
                                if (verbose):
                                    print("Could not add file with path: " + dirpath + " and filename: " + filename)
                                continue

                            self.AddFile(fileDef, verbose)                
            else:
                raise ValueError("Directory: " + path  + " not found")

            return


        # adds a FileDefinition object to the app's data store
        def AddFile(self, fileDefinition, verbose=True):       
            
            if (not(fileDefinition.IsSymLink())):                                                                   # ignore symlinks
                
                self._fileDefsByPath[fileDefinition.GetFullPathFilename()] = fileDefinition                         # save a reference to the file definition object by its path
                fileSize = fileDefinition.GetSizeBytes()

                if (not(fileSize in self._fileSizes)):                                                              # if we haven't stored this filesize before, create a list keyed by the fileSize
                    self._fileSizes[fileSize] = []
                                    
                self._fileSizes[fileSize].append(fileDefinition)                                                    # append ref to the file definition to the list keyed by the file definition's file size

                if (verbose):                                                                                       
                    print(str(len(self._fileDefsByPath)) + ". " + fileDefinition.GetFullPathFilename())
         
            return


        # deletes all files that are considered duplicates from the file system
        def DeleteAllDuplicates(self, askUser=True, verbose=True):           
            self.DeleteAllFilesFromDupeData(self.GetDupeData(), askUser, verbose)
            
            return


        # takes a dictionary object of all the duplication data objects
        # if askUser is True, it will present all the duplications and ask which file to keep
        # if askUser is False, it will automatically delete all the files tht are considered duplicates
        def DeleteAllFilesFromDupeData(self, dupeData, askUser=True, verbose=True):
         
            if (verbose):
                print("\nDELETING DUPLICATES...\n")

            numDeleted = 0

            for hash, dupeData in dupeData.items():                                                                 # for each list of files indexed by the length of the files in bytes       
                
                duplicateFiles = dupeData.GetAllFileDefinitions()                                                   # get a list of all the files that are the particular length (item in pos 0 will always be the one we consider to be the "original")
                keepFileIndex = 0                                                                                   # assume we'll keep the file in index 0 as this is the one we think is probably the original
                considerDeletion = True
                num = len(duplicateFiles)                       

                if (askUser):                                                                                       # if we are going to ask the user which file to keep
                    while (True):
                        print("\n-------------------------------------------------------------------------------------")
                        print("The following are considered duplicates, file in position 1 is probably the original:\n")
                    
                        for i in range(num):
                            print (str(i+1) + ". " + duplicateFiles[i].GetFullPathFilename())

                        confirm = input("\nWhich file would you like to KEEP ? (1-" + str(num) + "), n=none, a=all, d=default (1): ").strip().lower()

                        if (confirm=="n"):                     
                            keepFileIndex = (-1)                                                                        # doesn't want to keep any, so set index to one that is not in range
                            break
                        elif (confirm=="d"):                                                                          
                            keepFileIndex = 0                                                                           # default to delete is the item at index 0
                            break   
                        elif (confirm=="a"):                                                                            
                            considerDeletion = False                                                                    # wants to keep them all so let's get out of here
                            break
                        else:
                            try:
                                keepFileIndex = (int(confirm)-1)                                                        # try and get the index as an int
                                break
                            except:
                                print ("\nError: Invalid input\n")                                                          
                                continue

                            if ((keepFileIndex<0) or (keepFileIndex>=num)):                                             # check we have an index in range, else skip 
                                print ("\nError, index not in range\n")

                if (considerDeletion):
                    for i in range(num):                                                                                # for every file
                        if (i!=keepFileIndex):                                                                          # if we are not looking at the file we want to keep
                            if (duplicateFiles[i].DeleteFile(verbose)):                                                 # delete it!
                                numDeleted+=1

            if (verbose):
                print("DELETED " + str(numDeleted) + " files")

            return
                    

        # returns an object which contains all the FileDuplicateData objects for files considered by this app, keyed by their hash
        def GetDupeData(self, verbose=True):

            if (verbose):
                print("\nFINDING DUPLICATES...\n")

            dupeData = {}

            for fileSize, files in self._fileSizes.items():                                                             # for each list of files indexed by the length of the files in bytes       
                if (len(files)>1):                                                                                      # there is more than one file with a certain length, so they may be duplicates
                    dupeData.update(self.GetDupeDataFromFileDefList(files))                                             # add to the dupeData object we are building, FileDuplicationData for the list of files 

            if (dupeData):                                                                                              # now need to remove any items that just have an original, as files with same size but different hash may create a duplicate entry with just a single original file and no duplicate list
                 for dupeDataItem in dupeData.copy():    
                     if (not (dupeData[dupeDataItem].HasDuplicates())):
                        del dupeData[dupeDataItem]
            
            if ((verbose) and (not dupeData)):
                    print("NO DUPLICATES FOUND!")
                
            return (dupeData)


        # returns an dictionary of FileDuplicationData keyed by the file's hash
        def GetDupeDataFromFileDefList(self, listFileDefinitions, verbose=True):

            dupeDataDict = {}
            
            for fileDefinition in listFileDefinitions:                                      
                    
                hash = fileDefinition.GetHash(verbose)                                                                  # get the hash of the file we are looking at
                dupeData = None  

                try:                                                                                                    # try and get a stored dupeData object that relates to that hash
                    dupeData = dupeDataDict[hash]                                 
                except KeyError:
                    pass                                                                                                # couldn't get one, we haven't seen this has before
               
                if (not(dupeData)):                                                                                     # we need to create a new dupData object
                    dupeData = FileDuplicateData()
                    dupeDataDict[hash] = dupeData                                                                       # store the FileDuplicateData

                dupeData.AddFileDef(fileDefinition)                                                                     # add the file to the dupeData object
                
            return (dupeDataDict)