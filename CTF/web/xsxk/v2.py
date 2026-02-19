import requests

# 目标请求URL
url = "https://xsxk.nuist.edu.cn/xsxk/elective/clazz/add"

# 注意：这里有两个Cookie项，通常只需关注关键的 'Authorization'
cookies = {
    'route': '9b588388c72efc64461890c4edb3d800',
    'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY4NDY5NzE1NTk4LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoiMTExODJodGc2NGppZHJldHYybmlnY29iMTcifQ.efLQB8hzPyFGWvhmdUPcY_mBBVoAwpo_bQpggrB_oDcOSetjcQqwQOk_tGoH-tB9H6eF8vazeYVbYLrPqLRhNQ',
}

# 请求头部信息，其中的Cookie通常无需重复设置，requests库的cookies参数会处理
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',  # requests自动处理解码，可省略此行
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY4NDY5NzE1NTk4LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoiMTExODJodGc2NGppZHJldHYybmlnY29iMTcifQ.efLQB8hzPyFGWvhmdUPcY_mBBVoAwpo_bQpggrB_oDcOSetjcQqwQOk_tGoH-tB9H6eF8vazeYVbYLrPqLRhNQ',
    'Batchid': '41467e8812f44bd3840c3d7e2b1a14b1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://xsxk.nuist.edu.cn',
    'Priority': 'u=1, i',
    'Referer': 'https://xsxk.nuist.edu.cn/xsxk/elective/grablessons?batchId=41467e8812f44bd3840c3d7e2b1a14b1',
    'Sec-Ch-Ua': '"Chromium";v="143", "Not A(Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

# POST请求的表单数据
data = {
    'clazzType': 'FANKC',
    'clazzId': '2025202621200002504',
    'secretVal': '8CVjSrx5S/6NjcYOtoqrOLA4zDKKSl30ZxMQ5fTRLP8VtYv/C4GCVAMRHP4p6JY7N+LoCHCDvgk+TwP7XriXtXph4zW03Z2BvsbbvA7y/nhv/IZUauCRg0Jya0+WAQMGQA+FeAOHml3nYY2FsIC4Xp6pXiyhnGDvwP7wilMDNoQ=',
}

# 发送POST请求
response = requests.post(url, headers=headers, data=data)

# 打印响应状态码和内容
print(f"状态码: {response.status_code}")
print("响应内容:")
print(response.text)

# 如果响应是JSON格式，也可以使用 response.json() 来解析
result = response.json()
print(result)