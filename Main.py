import os
import tensorflow as tf

def inputFunction():
    return input("Enter Link: ")

def parser(link):
    return None

def indexer(file):
    return None

def outputFunction(bias):
    return None

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

    def __init__(self,inputNodes, outputNodes,ticker):

        #Variables
        self.w = tf.Variable(tf.ones([inputNodes,outputNodes]))
        self.b = tf.Variable(tf.ones([outputNodes]))
        self.x = tf.placeholder(tf.float32, shape=[None, inputNodes])
        self.yPrime = tf.placeholder(tf.float32, shape=[None, outputNodes])
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


link = inputFunction()
textFile = parser(link)
analyze = indexer(textFile)

model = NeuralNetwork(0, 0, "Temp")
model.load("Temp")

bias = model.predict(analyze)
outputFunction(bias)




