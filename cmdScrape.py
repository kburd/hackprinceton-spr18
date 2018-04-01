from Scraper import *
from Parser import *
import sys


if __name__ == "__main__":

    # # to run article scraper and clean it up:
    args = sys.argv
    if len(args) > 2:
        scr = Scraper()
        latest_file = scr.scrape(args[1], float(args[2]))
        idx = Parser()
        idx.complexParse(latest_file)
    
    