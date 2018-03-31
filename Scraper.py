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
            name_idx = link.index('www.') + 4
        elif 'https://' in link:
            name_idx = link.index('https://') + len('https://')
            
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
            file = open(QUERY_PATH,'w')  
        elif score == 0.0:
            file = open(NEUTRAL_PATH + outlet_name + str(i) + '.txt', 'w')
        elif score < 0.5:
            file = open(LEFT_BIAS_PATH + outlet_name + str(i) + '.txt', 'w')
        else:
            file = open(RIGHT_BIAS_PATH + outlet_name + str(i) + '.txt', 'w')

        file.write(self.text_from_html(html))
        file.close()

s = Scraper()
s.scrape('https://www.nbcnews.com/politics/donald-trump/trump-tells-aides-not-talk-publicly-about-russia-policy-moves-n861256')
