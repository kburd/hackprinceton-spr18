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
        #print(link.split("\\"))

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


scraper = Scraper()
scraper.scrape("http://www.foxnews.com/us/2018/03/31/jury-convinced-noor-salman-knew-pulse-nightclub-attack-but-had-no-option-but-to-acquit-foreman-says.html")
