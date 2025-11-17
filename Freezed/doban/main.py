import requests
import re
import lxml
from bs4 import BeautifulSoup
url = 'https://movie.douban.com/top250'
headers = { 
           'User-Agent': 
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' 
               }
html = requests.get(url=url, headers=headers).text
nameList = []
href = re.findall('<a href="(https://movie.douban.com/subject/\\d+/)">\\s+<img', html)
for i in href:
    temp = requests.get(url=i, headers=headers).text
    name = re.findall('<span property="v:itemreviewed">(.*)</span>', temp)
    nameList.append(name[0])
    print(nameList)