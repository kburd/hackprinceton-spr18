import nltk
import json
from pathlib import Path
from nltk.stem.lancaster import LancasterStemmer
from Parser import *

class Classifier:
    
    def __init__(self):
        
        self.class_words = {}
        self.stemmer = LancasterStemmer()
        self.corpus_words = {}
        
    def train(self):
        
        training_data = []

        # read training data
        content = []
        parser = Parser()
        
        master = "Articles"
        subFolders = os.listdir(master)
        
        if '.DS_Store' in subFolders:
            subFolders.remove('.DS_Store')
            
        if 'UserQuery.txt' in subFolders:
            subFolders.remove('UserQuery.txt')

        for sub in subFolders:
            subfolder = os.listdir(master + "/" + sub)
            
            if '.DS_Store' in subfolder:
                subfolder.remove('.DS_Store')

            for text in subfolder:
                
                content = parser.simpleParse(master + "/" + sub + "/" + text)
                for next in content:
                    training_data.append({"class":sub, "sentence":next})
                    
        # turn a list into a set (of unique items) and then a list again (this removes duplicates)
        classes = list(set([a['class'] for a in training_data]))
        for c in classes:
            # prepare a list of words within each class
            self.class_words[c] = []

        # loop through each sentence in our training data
        for data in training_data:
            # tokenize each sentence into words
            for word in nltk.word_tokenize(data['sentence']):
                # ignore a some things
                if  word not in ["?", "'s"]:
                    # stem and lowercase each word
                    stemmed_word = self.stemmer.stem(word.lower())
                    # have we not seen this word already?
                    if stemmed_word not in self.corpus_words:
                        self.corpus_words[stemmed_word] = 1
                    else:
                        self.corpus_words[stemmed_word] += 1

                    # add the word to our words in class list
                    self.class_words[data['class']].extend([stemmed_word])

    # calculate a score for a given class taking into account word commonality
    def calculateClassScore(self, sentence, class_name, show_details=True):
        score = 0
        # tokenize each word in our new sentence
        for word in nltk.word_tokenize(sentence):
            # check to see if the stem of the word is in any of our classes
            if self.stemmer.stem(word.lower()) in self.class_words[class_name]:
                # treat each word with relative weight
                score += (1 / self.corpus_words[self.stemmer.stem(word.lower())])

                if show_details:
                    print ("   match: %s (%s)" % (self.stemmer.stem(word.lower()), 1 / self.corpus_words[self.stemmer.stem(word.lower())]))
        return score

    def test(self, filename):
        
        if os.path.exists(filename):

            parser = Parser()
            sentences = parser.simpleParse(filename)
        
            scores = [0]*len(self.class_words.keys())
            
            print(self.class_words.keys())
            
            for i in range(len(sentences)):
                 
                # loop through classes
                count = 0
                for c in self.class_words.keys():
                    # calculate score of sentence for each class
                    score = self.calculateClassScore(sentences[i], c, show_details=False)
                    
                    scores[count] += score
                    count += 1
                    
            for j in range(len(scores)):
                scores[j] /= len(sentences)
                
            print(scores)
     
            temp = scores[0]
            scores[0] = scores[1]
            scores[1] = temp
            
            print(scores)
     
            return scores
        
        else:
            return 'None'

    def save(self, modelName):
        
        if not os.path.exists('SaveData/' + modelName):
            os.makedirs('SaveData/' + modelName)
        
        with open('SaveData/' + modelName + '/classwords.json', 'w') as fp:
            json.dump(self.class_words, fp, sort_keys=True, indent=4)
        with open('SaveData/' + modelName + '/corpuswords.json', 'w') as fp:
            json.dump(self.corpus_words, fp, sort_keys=True, indent=4)            

    def load(self, modelName):
        classFile = 'SaveData/' + modelName + '/classwords.json'
        wordFile = 'SaveData/' + modelName + '/corpuswords.json'
        if os.path.exists(classFile):
            with open(classFile, 'r') as fp:
                self.class_words = json.load(fp)
        if os.path.exists(wordFile):
            with open(wordFile, 'r') as fp:
                self.corpus_words = json.load(fp)
