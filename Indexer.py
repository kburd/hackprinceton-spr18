import os

class Indexer:

    def __init__(self, config):

        self.dict = {}
        self.indexedWords = config.keywords

    def indexTestBank(self):

        master = "Articles"
        subFolders = os.listdir(master)

        for sub in subFolders:

            subfolder = os.listdir(master + "\\" + sub)

            for text in subfolder:
                indexing = self.indexText(master + "\\" + sub + "\\" + text)
                self.dict[text] = indexing


    def indexText(self, fileDir):

        file = open(fileDir, "r")
        rawText = file.read()

        words = rawText.replace(".", "").replace(",", "").replace('"', "").replace(')', "").replace('(', "")\
            .replace('?', "").replace(':', "").lower().split(" ")

        temp = [0]*len(self.indexedWords)

        for word in words:

            print(word)

            if word in self.indexedWords:

                temp[self.indexedWords.index(word)] += 1

        return temp