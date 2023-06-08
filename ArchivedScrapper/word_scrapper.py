from collections import deque
from bs4 import BeautifulSoup
import requests
# word locater class
class WordLocator:
  def __init__(self, url : str):
    # sends get method to url -> receive requests.Response
    self._root = url
    self._all_webpages = [] # list of urls
    self._located_webpages = []
  def _locate(self, word : str):
    """
    BST through web pages. 
    for each web page, extract visible text,
      1. if word in page, append url to _webpages
      2. find all non-visited internal links and add to queue
    """
    f_all = open("txt.txt", "a",  encoding="utf-8")
    f_located = open("txt_located.txt", "a",  encoding="utf-8")

    q = deque()
    q.append(self._root)
    visited = set()
    while q:
      # Search for visible text tags and locate word
      url = q.pop()
      f_all.write((url if url.startswith(self._root) else self._root + url) + '\n')

      if url.startswith(self._root):
        visited.add(url[len(self._root):])
      else:
        visited.add(self._root + url)
      visited.add(url)
      webpage = requests.get(url if url.startswith(self._root) else self._root + url)
      soup = BeautifulSoup(webpage.content, 'html.parser')
      
      if word in soup.get_text():
        self._located_webpages.append(url)
        print(url)
        f_located.write((url if url.startswith(self._root) else self._root + url) + "\n")
      
      # find all valid neighbor and add to queue
      for link in soup.find_all('a'):
        neighbor = link.get('href')
        
        # must consider relative and absolute routing.
        if neighbor and (neighbor.startswith(self._root) or neighbor[0] == '/') and not neighbor.endswith('.pdf') and neighbor not in visited:
          q.append(neighbor)

  def find_word(self, word):
    self._locate(word)
    return self._located_webpages

  def find_subdomain(self):
    """
    BST through web pages. 
    for each web page, check url for change in subdomain
    """
    f_subdomains = open("txt_subdomains.txt", "a",  encoding="utf-8")

    q = deque()
    q.append(self._root)
    visited = set()
    subdomains = set()
    while q:
      # Search for visible text tags and locate word
      url = q.pop()
      visited.add(url)
      webpage = requests.get(url)
      soup = BeautifulSoup(webpage.content, 'html.parser')
      
      if url[:url.find('.')] not in subdomains:
        subdomains.add(url[:url.find('.')])
        print(url[:url.find('.')])
        f_subdomains.write(url[:url.find('.')] + "\n")
      
      # find all valid neighbor and add to queue
      for link in soup.find_all('a'):
        neighbor = link.get('href')
        
        # must consider relative and absolute routing.
        if neighbor and neighbor.startswith('https://') and neighbor not in visited:
          q.append(neighbor)

if __name__ == '__main__':
  word_locator = WordLocator('https://www.necktie.com.hk')
  word_locator.find_subdomain()


