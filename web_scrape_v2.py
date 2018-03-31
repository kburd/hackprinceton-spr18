from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib3 as lib
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
	http = lib.PoolManager()
	response = http.request('GET', link)
	html = response.data
	# print(text_from_html(html))
	# html = urllib3.request.urlopen(link).read()

	# JUNK TO USE LATER...
	name_idx = link.index('www')+4
	outlet_name = link[name_idx:name_idx+3]

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
	file = open('Articles/cnn1.txt','w')
	file.write(text_from_html(html))
	file.close()


if __name__ == "__main__":
	l = sys.argv
	if len(l) > 1:
		parse_and_save_article(l[1])
	else:
		parse_and_save_article()