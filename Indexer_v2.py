import os
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.tokenize import RegexpTokenizer
# from nltk.tokenize import sent_tokenize
import nltk


class Indexer:
    
    def indexText(self, fileDir):

        file = open(fileDir, "r")
        rawText = file.read()
        
        text = rawText.replace("  ", " ").replace("   ", " ").split('. ')

        return text

    def remove_stop_words_and_punctuation(self, filePath):
        file = open(filePath)
        text = file.read()
        file.close()

        # declare standard 'stop word' along with punctuation (except periods)
        stop_words = set(nltk.corpus.stopwords.words('english'))
        stop_words.update(',', '"', "'", ":", ";", "|", "(", ")", "`")

        word_tokens = nltk.word_tokenize(text)
        word_tokens[:] = [x for x in word_tokens if x != "''"]
        word_tokens[:] = [x for x in word_tokens if x != "``"]
         
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []

        # empty the file
        open(filePath, 'w').close()

        # append to file word-by-word, newline declares the next sentence
        file = open(filePath, 'a')
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        for w in filtered_sentence:
            if (w == '.') | (w == '?') | (w == '!'):
                file.write('\n')
            # elif w.isnumeric():
            #     pass
            else:
                file.write(w + " ")

        file.close()

idx = Indexer()
idx.remove_stop_words_and_punctuation('Articles/UserQuery/bno3.txt')