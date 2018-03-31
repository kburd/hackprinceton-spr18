import os
from Configuration import * 

class Indexer:
<<<<<<< HEAD
    
=======

    def __init__(self):

        self.dict = {}

    def indexTestBank(self):

        master = "Articles"
        subFolders = os.listdir(master)

        for sub in subFolders:
            # print(sub)
            if os.path.isdir(master + "/" + sub):
                # print(sub)
                subfolder = os.listdir(master + "/" + sub)

                for text in subfolder:
                    if text != '.DS_Store':
                        indexing = self.indexText(master + "/" + sub + "/" + text)
                        self.dict[text] = indexing


>>>>>>> 34b023725a94cbae626386980ad6af52ea58c06b
    def indexText(self, fileDir):

        file = open(fileDir, "r")
        print(fileDir)
        rawText = file.read()
        
        text = rawText.replace("  ", " ").replace("   ", " ").split('. ')
        
        for line in text:
            print(line)


        return text
