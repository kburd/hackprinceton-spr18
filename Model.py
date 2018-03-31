from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import tensorflow as tf
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib3 as lib


class Scraper:

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', "foot"]:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(self, body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def scrape(self, link):

        http = lib.PoolManager()
        response = http.request('GET', link)
        html = response.data


        #TODO
        #Get Stuff between periods in url

        #TODO
        #Modify num at end of file

        #TODO
        #Determine what sub folder to place it in

        # print(text_from_html(html))
        # html = urllib3.request.urlopen(link).read()

        # JUNK TO USE LATER...
        # name_idx = link.index('www') + 4
        # outlet_name = link[name_idx:name_idx + 3]

        # # iterate to find the next available number
        # i = 1
        # while True:
        # 	try:
        # 		open('Articles/' + outlet_name + str(i) + '.txt', 'a')
        # 		i+=1
        # 		pass
        # 	except:
        # 		break

        # file = open('Articles/' + outlet_name + str(i) + '.txt', 'w')

        file = open('Articles/cnn1.txt', 'w')
        file.write(self.text_from_html(html))
        file.close()


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


                input("___________________________________________")

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


class NeuralNetwork:

    w = []
    b = []
    x = []
    y = []
    yPrime = []

    sess = None
    trainStep = None

    #Disable Warning
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    def __init__(self, config, ticker):

        #Variables
        self.w = tf.Variable(tf.ones([config.numInputNodes, config.numOutputNodes]))
        self.b = tf.Variable(tf.ones([config.numOutputNodes]))
        self.x = tf.placeholder(tf.float32, shape=[None, config.numInputNodes])
        self.yPrime = tf.placeholder(tf.float32, shape=[None, config.numOutputNodes])
        self.y = tf.matmul(self.x, self.w) + self.b

        #Start Session
        self.sess = tf.InteractiveSession()
        self.sess.run(tf.global_variables_initializer())

        #Set up Trainer
        crossEntropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.yPrime, logits=self.y))
        self.trainStep = tf.train.GradientDescentOptimizer(0.5).minimize(crossEntropy)



    def train(self, inputData, outputData):

        self.trainStep.run(feed_dict={self.x: inputData, self.yPrime: outputData})

    def accuracy(self, inputTest, outputTest):

        correctPrediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.yPrime, 1))
        accuracy = tf.reduce_mean(tf.cast(correctPrediction, tf.float32))
        return accuracy.eval(feed_dict={self.x: inputTest, self.yPrime: outputTest})

    def predict(self, inputData):

        output = tf.matmul(inputData, self.w) + self.b
        return output.eval()[0][0]

    def save(self, filename):

        saver = tf.train.Saver()
        saver.save(self.sess, "/tmp/" + filename + "/test.ckpt")

    def load(self, filename):

        saver = tf.train.Saver()
        saver.restore(self.sess, "/tmp/" + filename + "/test.ckpt")


class Configuration:

    def __init__(self):

        configFile = open("config.txt", 'r')
        rawData = configFile.readlines()

        data = []
        for line in rawData:

            if line[0] != "#" and line[0] != "\n":
                data += [line.strip("\n")]

        self.numInputNodes = int(data[0])
        self.numOutputNodes = int(data[1])

        self.keywords = []
        for i in range(self.numInputNodes):
            self.keywords += [data[2 + i]]


def getValue(key, requestString):

    paramString = requestString.split(" ")[1].strip("/")
    pairs = paramString.split("&")

    for i in range(len(pairs)):
        pair = pairs[i].split("=")

        if len(pair) == 1:
            return

        tempKey = pair[0]
        tempValue = pair[1]

        if tempKey == key:

            return tempValue


class RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        mode = getValue("mode", self.requestline)
        message = format("%s is not a mode") % mode

        if mode == "echo":
            message = "Hola Mundo"

        if mode == 'train':

            config = Configuration()
            filename = getValue("filename", self.requestline)

            indexer = Indexer(config)
            indexer.indexTestBank()

            net = NeuralNetwork(config, filename)
            #Train test bank one subfolder at a time to make training easy
            net.save("Test")

            message = "Training Successful"

        if mode == "test":

            config = Configuration()
            link = getValue("link", self.requestline)
            filename = getValue("filename", self.requestline)

            scraper = Scraper()
            textFile = scraper.scrape(link)

            indexer = Indexer()
            analyze = indexer.indexText(textFile)

            net = NeuralNetwork(config, filename)
            net.load("Temp")

            bias = net.predict(analyze)
            message = bias

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.end_headers()

        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def run():

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Running Erlich...')
    httpd.serve_forever()


run()




