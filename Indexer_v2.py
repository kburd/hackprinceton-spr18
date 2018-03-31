import os
from Configuration import * 

class Indexer:

    def __init__(self):

        self.dict = {}

    def indexTestBank(self):

        master = "Articles"
        subFolders = os.listdir(master)

        for sub in subFolders:
            
            if os.path.isdir(master + "/" + sub):

                subfolder = os.listdir(master + "/" + sub)
                
            else:
                
                subfolder = []

            for text in subfolder:
                indexing = self.indexText(master + "/" + sub + "/" + text)
                self.dict[text] = indexing


    def indexText(self, fileDir):

        file = open(fileDir, "r")
        rawText = file.read()
        
        text = rawText.replace("  ", " ").replace("   ", " ").split('. ')
        
        for line in text:
            print(line)
            
        print('_________________________________________')


##
##        print(temp)
##
        return text
##
##indexer = Indexer()
##
##indexer.indexTestBank()

##print(indexer.dict)