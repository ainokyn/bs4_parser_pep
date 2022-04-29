import re
from urllib.parse import urljoin
import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm
PEP = 'https://peps.python.org/'
from collections import Counter

session = requests_cache.CachedSession()
response = session.get(PEP)
soup = BeautifulSoup(response.text, features='lxml')
id = soup.find(attrs={'id': 'index-by-category'})
tr_tag = id.find_all('tr')
list_status = []
result = [('Статус', 'Количество')]
for tag in tr_tag:
    url_a_tag = tag.find('a')
    if url_a_tag is not None:
        href = url_a_tag['href']
        link = urljoin(PEP, href)
        response = session.get(link)
        soup = BeautifulSoup(response.text, features='lxml')
        dl_tag = soup.find('dl')
        status = dl_tag.find('dt', string='Status')
        name_status = status.find_next_sibling()
        text_name_status = name_status.text
        list_status.append(text_name_status)
        td_tag = tag.find('td')
        if td_tag is not None:
            status_in_table = td_tag.text[1:]
        EXPECTED_STATUS = {
            'A': ['Active', 'Accepted'],
            'D': ['Deferred'],
            'F': ['Final'],
            'P': ['Provisional'],
            'R': ['Rejected'],
            'S': ['Superseded'],
            'W': ['Withdrawn'],
            '': ['Draft', 'Active'],
            }
        if text_name_status in EXPECTED_STATUS[status_in_table]:
            continue
        else:
            print(text_name_status, status_in_table)
count = Counter(list_status)
total = len(list_status)
k = list(count.keys())
f = list(count.values())
for i, q in list(zip(k, f)):
    result.append((i, q))
print(result)
