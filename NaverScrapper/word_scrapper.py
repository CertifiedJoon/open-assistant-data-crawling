from collections import deque
import datetime
from bs4 import BeautifulSoup
from openpyxl import Workbook
import requests

# word locater class
class WordLocator:
  def __init__(self, url : str):
    # sends get method to url -> receive requests.Response
    self._root = url
    self._wb = Workbook()
    self._locate = []
    self._located_webpages = []

  def crawl(self, word):
    """
    BST through web pages. 
    for each web page, extract visible text,
      1. if word in page, append url to _webpages
      2. find all non-visited internal links and add to queue
    """
    sheet = self._wb.active
    sheet.append(['Instruction', 'Response', 'Source', 'MetaData'])
    filename = 'result/' + word.replace(' ', '.') + "_"  + "_crawling_result.xlsx"
    f_located = open(f"txt_{word}_located.txt", "a",  encoding="utf-8")

    q = deque()
    q.append(self._root)
    visited = set()

    while q and len(visited) != 500:
      # Search for visible text tags and locate word
      url = q.pop()
      print(url)

      if url.startswith(self._root):
        visited.add(url[len(self._root):])
      else:
        visited.add(self._root + url)

      visited.add(url)
      webpage = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
      soup = BeautifulSoup(webpage.content, 'html.parser')
      
      # Crawl Data
      instruction = soup.find_all("div", class_="c-heading__content")
      if word in instruction:
        print(url if url.startswith(self._root) else self._root + url)
        responses = soup.find_all("div", class_="se-module-text")
        f_located.write(url + "\n")

        for response in responses:
          sub_soup = BeautifulSoup(response, 'lmxl')
          response_spans = sub_soup.find_all("span")
          txt = ""
          for response_span in response_spans:
            text_soup = BeautifulSoup(response_span)
            txt += text_soup.get_text()
          
          sheet.append([instruction, txt, 'Naver Kin', ''])

      # find all valid neighbor and add to queue
      for link in soup.find_all('a'):
        neighbor = link.get('href')
        if neighbor.startswith('/qna/detail.naver'):
          neighbor = self._root + neighbor
          # must consider relative and absolute routing.
          if neighbor not in visited:
            q.append(neighbor)
    
    self._wb.save(filename)
    

if __name__ == '__main__':
  word_locator = WordLocator('https://kin.naver.com')
  word_locator.crawl('')


