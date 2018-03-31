from Main import Scraper
import sys


if __name__ == "__main__":

    parser = Scraper()
    args = sys.argv
    parser.scrape(args[1])