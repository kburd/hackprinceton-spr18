import urllib3 as lib
from bs4 import BeautifulSoup
from IPython.display import HTML

site = 'https://www.nbcnews.com/politics/donald-trump/trump-tells-aides-not-talk-publicly-about-russia-policy-moves-n861256'
img = 'http://www.openbookproject.net/tutorials/getdown/css/images/lesson4/HTMLDOMTree.png'
# print(soup.title)
# print(soup.prettify())
# print(soup.find_all("a"))

def find_other_articles(link):
	http = lib.PoolManager()
	response = http.request('GET', link)
	soup = BeautifulSoup(response.data)

	all_links = soup.find_all("a")
	for link in all_links:
		link_str = link.get("href")
		if "nbcnews.com" in link_str:
			print(link_str)

def do_prettify(link):
	http = lib.PoolManager()
	response = http.request('GET', link)
	soup = BeautifulSoup(response.data)

	print(soup.prettify())
	# soup.prettify()

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)




if __name__ == "__main__":
	# do_prettify(site)
	# print('hi')
	# print(HTML('<iframe src=http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts width=700 height=500></iframe>'))

	# html = lib.request.urlopen('http://www.nytimes.com/2009/12/21/us/21storm.html').read()
	# print(text_from_html(html))
	find_other_articles('http://www.nytimes.com/2009/12/21/us/21storm.html')


