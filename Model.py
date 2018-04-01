import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from Parser import *
from Classifier import *
from Scraper import *
<<<<<<< HEAD
=======
<<<<<<< Updated upstream
# from Configuration import *
import sys
=======
#from Configuration import *
>>>>>>> Stashed changes
>>>>>>> 29ffb32d14845b1a84e86f6ba738b58dae3f80e6

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
    
    string = ''
    
    for out in outputs:
        string += str(out) + ' '
        
    return string


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

            link = getValue("link", self.requestline)
            modelName = getValue("modelName", self.requestline)

            scraper = Scraper()
            scraper.scrape(link)

            ml = Classifier()
            ml.load(modelName)
            outputs = ml.test('./Articles/UserQuery.txt')
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

<<<<<<< HEAD
run()
=======
if __name__ == "__main__":
    #run()

    # # to run article scraper and clean it up:
<<<<<<< Updated upstream
    # args = sys.argv
    # if len(args) > 1:
    #     scr = Scraper()
    #     latest_file = scr.scrape(args[1], 0.9)
    #     idx = Parser()
    #     idx.remove_stop_words_and_punctuation(latest_file)
=======
    args = sys.argv
    if len(args) > 1:
        scr = Scraper()
        latest_file = scr.scrape(args[1], 0.1)
        idx = Parser()
        idx.remove_stop_words_and_punctuation(latest_file)
>>>>>>> Stashed changes

>>>>>>> 29ffb32d14845b1a84e86f6ba738b58dae3f80e6





