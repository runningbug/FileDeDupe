import os
import platform
import hashlib

#
# stores data about a file relevant to the FileDeDupe application
#
class FileDefinition:
    
    # takes the path where the file is found and the filename
    def __init__(self, path, filename):

        try:
            self._path = path
            self._filename = filename
            self._fullPathFilename = os.path.join(self._path, self._filename)
            self._modificationTime = os.path.getmtime(self._fullPathFilename)
            self._sizeBytes = os.path.getsize(self._fullPathFilename)
            self._isSymLink = os.path.islink(self._fullPathFilename)
                
            if (platform.system() == "Windows"):                                            # getting creation date is tricky as hard to get creation time on Linux...
                self._creationTime = os.path.getctime(self._fullPathFilename)
            else:
                stat = os.stat(self._fullPathFilename)                                      # get the stat data on the file
            
                try:
                    self._creationTime = stat.st_birthtime                                  # try and get the birthtime (will prob work on Mac)
                except AttributeError:
                    self._creationTime = stat.st_mtime                                      # probably Linux, let's settle for the modification time
        except:
            raise


    # deletes the referenced file from the file system
    def DeleteFile(self, verbose=True):

        if (verbose):
            print("Deleting File: " + self._fullPathFilename)

            try:
                os.remove(self._fullPathFilename)
            except OSError:
                return (False)

        return (True)


    # returns whether the referenced file is a sym link
    def IsSymLink(self):
        return (self._isSymLink)


    # gets the full path of the file (path+filename)
    def GetFullPathFilename(self):
        return (self._fullPathFilename)


    # gets the size of the file in bytes
    def GetSizeBytes(self):
        return (self._sizeBytes)


    # gets the last modification time
    def GetLastModificationTime(self):
        return (self._modificationTime)


    # gets the creation time of the file (NOTE: on Linux will be the modification time)
    def GetCreationTime(self):
        return (self._creationTime)


    # returns whether this file is considered "older" than another file
    def IsOlderThan(self, file):

        fileCreationTime = file.GetCreationTime()

        if (self._creationTime==fileCreationTime):
            return (self._modificationTime<file.GetModificationTime())
        else:
            return (self._creationTime<fileCreationTime)


    # gets the SHA512 hash of the file
    # will calculate it if it hasn't already been calculated, else it will just return
    # the already stored hash value for the file referenced by this FileDefinition object
    def GetHash(self, verbose=True):

        if (not(hasattr(self, 'hash'))):
                
            if (verbose):
                print("Hash: " + self.GetFullPathFilename() + " --> ", end='', flush=True)
    
            sha512 = hashlib.sha512()

            with open(self.GetFullPathFilename(), 'rb') as file:
                while (True):
                    data = file.read(65536)                         # 64 kb chunks
                                
                    if (data):
                        sha512.update(data)
                    else:
                        break   
           
            self.hash = sha512.hexdigest()

            if (verbose):
                print(self.hash)

        return (self.hash)