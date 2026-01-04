import requests
import json

cookies = {
    'route': 'e8621a4a430d4c44ae231be5b47e4a48',
    'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY2OTgwNTgxNDU0LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoicjBjbW0wZHExZWhwNnFtcmdvNGg4ajBsYTAifQ.R5AyilXTIsHQLPfYZs77U4U8Hu987NioGrbS0jb0oUx0M3qDF5atkLQKbx9icXYTGqJfFjZfDum8p4l7nlPBoQ',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://xsxk.nuist.edu.cn/xsxk/elective/grablessons?batchId=b2ea72125dd74c268b1dfa2388bca61a',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    # 'cookie': 'route=e8621a4a430d4c44ae231be5b47e4a48; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY2OTgwNTgxNDU0LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoicjBjbW0wZHExZWhwNnFtcmdvNGg4ajBsYTAifQ.R5AyilXTIsHQLPfYZs77U4U8Hu987NioGrbS0jb0oUx0M3qDF5atkLQKbx9icXYTGqJfFjZfDum8p4l7nlPBoQ',
}

params = {
    'batchId': 'e49350a1926a4bfb95cf24eb361411c3',
}

response = requests.get('https://xsxk.nuist.edu.cn/xsxk/elective/grablessons', params=params, cookies=cookies, headers=headers)
result = response.json()
print(f"JSON响应: {json.dumps(result, ensure_ascii=False, indent=2)}")