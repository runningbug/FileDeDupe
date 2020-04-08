# holds FileDefinition data in a format which allows us to
# determine which files are duplicates and which one is the "original"
class FileDuplicateData:

    def __init__(self):
        self._original = None
        self._duplicates = []


    # returns the FileDefinition object we think references the original file
    def GetOriginalFileDefinition(self):
        return (self._original)


    # returns a list of FileDefinition objects that we think are duplicates of the original file
    def GetDuplicatesFileDefinitionList(self):
        return (self._duplicates)


    # returns a list of all FileDefinition objects held by this FileDuplicateData object
    # the item at index 0 is always the one we consider to be the original
    def GetAllFileDefinitions(self):
        return ([self._original] + self._duplicates)


    # returns whether htis dupeData obejct has valid duplicates
    def HasDuplicates(self):
        return (len(self._duplicates)>0)


    # Adds a FileDefinition object to this FileDuplicateData object
    def AddFileDef(self, fileDefinition):
        if ((self._original==fileDefinition) or (fileDefinition in self._duplicates)):                  # first check the fileDefinitions hasnt been added previously
            return

        if (self._original==None):                                                                      # if we don't already have an original, consider it the original
            self._original = fileDefinition
        else:
            if (fileDefinition.IsOlderThan(self._original)):                                            # if the new file added is now considered the original...
                self._duplicates.append(self._original)                                                 # py the current original on the end of the duplicates
                self._original = fileDefinition                                                         # make the original the new file we are adding
            else:
                self._duplicates.append(fileDefinition)                                                 # we're a duplicate, so just add to the end of the duplicates' list

        return (fileDefinition)