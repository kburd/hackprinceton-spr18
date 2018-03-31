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