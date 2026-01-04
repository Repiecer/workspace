import requests
from http.cookies import SimpleCookie

cookies_str = 'route=e8621a4a430d4c44ae231be5b47e4a48; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY2OTgwNTgxNDU0LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoicjBjbW0wZHExZWhwNnFtcmdvNGg4ajBsYTAifQ.R5AyilXTIsHQLPfYZs77U4U8Hu987NioGrbS0jb0oUx0M3qDF5atkLQKbx9icXYTGqJfFjZfDum8p4l7nlPBoQ'
cookie = SimpleCookie()
cookie.load(cookies_str)
jar = requests.cookies.RequestsCookieJar()
for key, morsel in cookie.items():
    jar.set(key, morsel.value, domain='xsxk.nuist.edu.cn', path='/')

print(jar)

