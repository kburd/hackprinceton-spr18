from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import sys


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', "foot"]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)


def parse_and_save_article(link='https://www.cnn.com/2018/03/30/politics/scott-pruitt-epa-white-house/index.html'):
	html = urllib.request.urlopen(link).read()

	'''
	# JUNK TO USE LATER...
	name_idx = link.index('www')+3
	outlet_name = link[name_idx:name_idx+3]
	'''

	file = open('./data/cnn1.txt','a')
	file.write(text_from_html(html))
	file.close()


if __name__ == "__main__":
	l = sys.argv
	if len(l) > 1:
		parse_and_save_article(l[1])
	else:
		parse_and_save_article()