from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib3 as lib

LEFT_BIAS_PATH = './Articles/LeftBias/'
RIGHT_BIAS_PATH = './Articles/RightBias/'
NEUTRAL_PATH = './Articles/UserQuery/'
QUERY_PATH = './Articles/UserQuery.txt'


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

    def scrape(self, link, score=None):

        http = lib.PoolManager()
        response = http.request('GET', link)
        html = response.data
        
        if 'www' in link:
            name_idx = link.index('www.') + len('www.')
        elif 'https://' in link:
            name_idx = link.index('https://') + len('https://')
        elif 'http://' in link:
            name_idx = link.index('http://') + len('http://')
            
        elif 'http://' in link:
            name_idx = link.index('http://') + len('http://')
            
        outlet_name = link[name_idx:name_idx + 3]

        # iterate to find the next available number
        i = 1
        while score != None:
            # check if file# exists
            try:
                if score == 0.0:
                    open(NEUTRAL_PATH + outlet_name + str(i) + '.txt')
                elif score < 0.5:
                    open(LEFT_BIAS_PATH + outlet_name + str(i) + '.txt')
                else:
                    open(RIGHT_BIAS_PATH + outlet_name + str(i) + '.txt')
                i+=1
                pass
            except:
                break

        # add article to dedicated folder (0=No Bias, <0.5=Left Bias, >0.5=Right Bias)
        if score == None:
            file_name = ""
            file = open(QUERY_PATH,'w') 
        elif score == 0.0:
            file_name = NEUTRAL_PATH + outlet_name + str(i) + '.txt'
            file = open(file_name, 'w')
        elif score < 0.5:
            file_name = LEFT_BIAS_PATH + outlet_name + str(i) + '.txt'
            file = open(LEFT_BIAS_PATH + outlet_name + str(i) + '.txt', 'w')
        else:

            file = open(RIGHT_BIAS_PATH + outlet_name + str(i) + '.txt', 'w')
            file_name = RIGHT_BIAS_PATH + outlet_name + str(i) + '.txt'
            file = open(file_name, 'w')

        file.write(self.text_from_html(html))
        file.close()

        return file_name

<<<<<<< HEAD
=======
# s = Scraper()
# s.scrape('https://www.nbcnews.com/politics/donald-trump/trump-tells-aides-not-talk-publicly-about-russia-policy-moves-n861256')
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
>>>>>>> 29ffb32d14845b1a84e86f6ba738b58dae3f80e6
