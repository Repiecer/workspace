import requests
from http.cookies import SimpleCookie

url = 'https://xsxk.nuist.edu.cn/xsxk/elective/clazz/add'
data = {
    'clazzType': 'FANKC',
    'clazzId': '2025202621300051504',
    'secretVal': 'gvQAbZNbV7WUcNlo2NuGHjRh1xL6it12PcEDhIKIT98VtYv%2FC4GCVAMRHP4p6JY7N%2BLoCHCDvgk%2BTwP7XriXtZ%2BQpqeJB4YsxNFyoLbn%2B6ENkJ1lo%2BIiEVQpHQN2zFK%2FBlB6jLF1%2BdTEzuN8Eg6zQnDwCmejXIXgBeYHExT9R%2Fs%3D'
}

cookies_str = 'route=e8621a4a430d4c44ae231be5b47e4a48; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY2OTgwNTgxNDU0LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoicjBjbW0wZHExZWhwNnFtcmdvNGg4ajBsYTAifQ.R5AyilXTIsHQLPfYZs77U4U8Hu987NioGrbS0jb0oUx0M3qDF5atkLQKbx9icXYTGqJfFjZfDum8p4l7nlPBoQ'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
cookie = SimpleCookie()
cookie.load(cookies_str)
jar = requests.cookies.RequestsCookieJar()

for key, morsel in cookie.items():
    jar.set(key, morsel.value, domain='xsxk.nuist.edu.cn', path='/')

response = requests.post(url, data=data, cookies=jar, headers=headers)
print(response.text)

