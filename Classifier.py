import nltk
import json
from pathlib import Path
from nltk.stem.lancaster import LancasterStemmer
from Indexer_v2 import *

class Classifier:
    
    def __init__(self):
        
        self.class_words = {}
        self.stemmer = LancasterStemmer()
        self.corpus_words = {}
        
    def train(self):
        
        training_data = []

        # read training data
        content = []
        indexer = Indexer()
        
        master = "Articles"
        subFolders = os.listdir(master)
        
        if '.DS_Store' in subFolders:
            subFolders.remove('.DS_Store')

        for sub in subFolders:
            subfolder = os.listdir(master + "/" + sub)
            
            if '.DS_Store' in subfolder:
                subfolder.remove('.DS_Store')

            for text in subfolder:
                
                content = indexer.indexText(master + "/" + sub + "/" + text)
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

        # we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
##        print ("Corpus words and counts: %s \n" % corpus_words)
##        # also we have all words in each class
##        print ("Class words: %s" % class_words)
##        print("\n")

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

    def test(self, sentence):
        
        scores = []
        # loop through classes
        for c in self.class_words.keys():
            # calculate score of sentence for each class
            score = self.calculateClassScore(sentence, c, show_details=False)
            scores.append(score)
            
        return scores

    def save(self, type):
        # if type == "Test":
            with open('SaveData/classwords.json', 'w') as fp:
                json.dump(self.class_words, fp, sort_keys=True, indent=4)
            with open('SaveData/corpuswords.json', 'w') as fp:
                json.dump(self.corpus_words, fp, sort_keys=True, indent=4)            

    def load(self, type):
        # if type == "Test":
            classFile = Path("SaveData/classwords.json")
            wordFile = Path("SaveData/corpuswords.json")
            if classFile.exists():
                with open('SaveData/classwords.json', 'r') as fp:
                    self.class_words = json.load(fp)
            if wordFile.exists():
                with open('SaveData/corpuswords.json', 'r') as fp:
                    self.corpus_words = json.load(fp)

classifier = Classifier()
classifier.train()
print(classifier.test("this is the end of the world"))



##scores = []
##
##def get_all_scores(sentence):
##    # loop through classes
##    for c in class_words.keys():
##        # calculate score of sentence for each class
##        score = calculate_class_score(sentence, c, show_details=False)
##        scores.append(score)
##    return scores
##
##print(get_all_scores("this is the end of the world"))  