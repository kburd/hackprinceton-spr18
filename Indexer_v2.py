import os
from Configuration import * 

class Indexer:
    
    def indexText(self, fileDir):

        file = open(fileDir, "r")
        print(fileDir)
        rawText = file.read()
        
        text = rawText.replace("  ", " ").replace("   ", " ").split('. ')
        
        for line in text:
            print(line)


        return text
