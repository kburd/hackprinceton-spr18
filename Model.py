from http.server import BaseHTTPRequestHandler, HTTPServer
from Indexer import *
from NeuralNet import *
from Scraper import *

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




