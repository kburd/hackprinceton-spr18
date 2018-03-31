from http.server import BaseHTTPRequestHandler, HTTPServer
from Indexer_v2 import *
from Classifier import *
from Scraper import *
from Configuration import *

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

def biasCalculation(outputs):
    
    return str(len(outputs))


class RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        mode = getValue("mode", self.requestline)
        message = format("%s is not a mode") % mode

        if mode == "echo":
            message = "Hola Mundo"

        if mode == 'train':

            config = Configuration()
            modelName = getValue("modelName", self.requestline)

            ml = Classifier()
            ml.train()
            ml.save(modelName)

            message = "Training Successful"

        if mode == "test":

            config = Configuration()
            link = getValue("link", self.requestline)
            modelName = getValue("modelName", self.requestline)

            scraper = Scraper()
            scraper.scrape(link)

            indexer = Indexer()
            analyze = indexer.indexText('./Articles/UserQuery.txt')

            ml = Classifier()
            ml.load(modelName)
            outputs = ml.test('./Articles/UserQuery.txt')
            print(outputs)
            message = biasCalculation(outputs)

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




