import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from Parser import *
from Classifier import *
from Scraper import *
# from Configuration import *

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
        
def getHTML(result):
    
    if result == -1:
        image = "ScalePhotos/Left.png"
        bias_rating = "ALT-LEFT"
        
    elif result == -.5:
        image = "ScalePhotos/LeftCenter.png"
        bias_rating = "MODERATELY LIBERAL"
        
    elif result == 0:
        image = "ScalePhotos/Center.png"
        bias_rating = "MODERATE"
        
    elif result == .5:
        image = "ScalePhotos/RightCenter.png"
        bias_rating  = "RIGHTY"
        
    elif result == 1:
        image = "ScalePhotos/Right.png"
        bias_rating = "ALT-RIGHT"
        
    else:
        image = ""
        bias_rating = "TBD"
        
        
    # file = open("layout.html")
    file = open("layout_v2.html")
    raw = file.read()
    lines = raw.strip("\n").split("\n")
    
    string = ""
    
    # for line in lines:
    #     if line == "*image*":
    #         line = "src=" + image + " "
    #     string += line

    for line in lines:
        if line == "*text*":
            line = bias_rating
        string += line
          
    return string

def biasCalculation(outputs):
    
    string = ''
    
    string += "Left: " + str(outputs[0]) + "\n"
    string += "Center: " + str(outputs[1]) + "\n"
    string += "Right: " + str(outputs[2]) + "\n"
    
    left = outputs[0]
    center = outputs[1]
    right = outputs[2]
    
    string += "\n"
    
    if right > 2 and right > left:
        result = 1
    
    elif right < .75 and left > 2:
        result = -1
    
    else:
        result = 0
        
    #print(string + " " + str(result))

    return result

class RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        mode = getValue("mode", self.requestline)
        message = format("%s is not a mode") % mode

        if mode == "echo":
            message = "Hola Mundo"
            
        if mode == "init":
            
            message = getHTML(None)

        if mode == 'train':

            modelName = getValue("modelName", self.requestline)

            ml = Classifier()
            ml.train()
            ml.save(modelName)

            message = "Training Successful"

        if mode == "test":
            
            print(self.requestline)

            link = getValue("link", self.requestline)
            modelName = getValue("modelName", self.requestline)

            scraper = Scraper()
            scraper.scrape(link)

            ml = Classifier()
            ml.load(modelName)
            outputs = ml.test('./Articles/UserQuery.txt')
            result = biasCalculation(outputs)
            
            message = getHTML(result)

        # else:
        #     print(self.requestline)
        #     string = self.requestline
        #     string = string.replace("GET /", "")
        #     index = string.index(" ")
        #     file = open(string[:index],"rb")
        #     message = "hello"#file.read()
            # return file(string)

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


    # # to run article scraper and clean it up:

#     args = sys.argv
#     if len(args) > 1:
#         scr = Scraper()
#         latest_file = scr.scrape(args[1], 0.1)
#         idx = Parser()
#         idx.remove_stop_words_and_punctuation(latest_file)





