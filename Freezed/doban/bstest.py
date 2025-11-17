from bs4 import BeautifulSoup
import requests

url = 'https://movie.douban.com/subject/3793023/'
headers = { 
           'User-Agent': 
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' 
               }
html = requests.get(url=url, headers=headers).text
soup = BeautifulSoup(html, 'lxml')
print(soup.find_all(id='info'))

