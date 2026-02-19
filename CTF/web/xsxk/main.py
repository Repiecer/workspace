import requests
from http.cookies import SimpleCookie

url = 'https://xsxk.nuist.edu.cn/xsxk/elective/clazz/add'
data = {
    'clazzType': 'FANKC',
    'clazzId': '2025202621200002504',
    'secretVal': f'g8CVjSrx5S%2F6NjcYOtoqrOLA4zDKKSl30ZxMQ5fTRLP8VtYv%2FC4GCVAMRHP4p6JY7N%2BLoCHCDvgk%2BTwP7XriXtXph4zW03Z2BvsbbvA7y%2Fnhv%2FIZUauCRg0Jya0%2BWAQMGQA%2BFeAOHml3nYY2FsIC4Xp6pXiyhnGDvwP7wilMDNoQ%3D'
}

cookies_str = 'route=9b588388c72efc64461890c4edb3d800; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY4NDY5NzE1NTk4LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoiMTExODJodGc2NGppZHJldHYybmlnY29iMTcifQ.efLQB8hzPyFGWvhmdUPcY_mBBVoAwpo_bQpggrB_oDcOSetjcQqwQOk_tGoH-tB9H6eF8vazeYVbYLrPqLRhNQ'

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

