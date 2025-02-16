# Title, at each library avaialbe, unavailable,etc
import requests
import json
from bs4 import BeautifulSoup

def get_book(title):
    response = requests.get(
        f"https://tccl.bibliocommons.com/v2/search?query={title[0]}&searchType=title"
    )
    #<a data-key="bib-title" data-test-id="bib-title-S63C6527750" href="/item/show/6527750063" lang="en" rel="noopener" target="_parent">
    soup = BeautifulSoup(response.text, 'html.parser')
    first_result = soup.find('div', class_='cp-search-result-item-content')
    if first_result == None:
        return False
    title_elem = first_result.find('span', class_='title-content')
    magic_number = first_result.find('a', data-key_='bib-title')
    print(magic_number)
    if title_elem.contents == title:
          return True #list of libraries that have it
    else:
          return title_elem.contents
titles = ["The Worlds I See"]
results = get_book(titles)
print(results)