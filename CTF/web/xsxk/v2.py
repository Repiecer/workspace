import requests
import urllib.parse
import json

# 请求配置
url = "https://xsxk.nuist.edu.cn/xsxk/elective/clazz/add"

# 请求头
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY2OTgwNTgxNDU0LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoicjBjbW0wZHExZWhwNnFtcmdvNGg4ajBsYTAifQ.R5AyilXTIsHQLPfYZs77U4U8Hu987NioGrbS0jb0oUx0M3qDF5atkLQKbx9icXYTGqJfFjZfDum8p4l7nlPBoQ',
    'batchid': 'e49350a1926a4bfb95cf24eb361411c3',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'route=e8621a4a430d4c44ae231be5b47e4a48; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY2OTgwNTgxNDU0LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoicjBjbW0wZHExZWhwNnFtcmdvNGg4ajBsYTAifQ.R5AyilXTIsHQLPfYZs77U4U8Hu987NioGrbS0jb0oUx0M3qDF5atkLQKbx9icXYTGqJfFjZfDum8p4l7nlPBoQ',
    'origin': 'https://xsxk.nuist.edu.cn',
    'priority': 'u=1, i',
    'referer': 'https://xsxk.nuist.edu.cn/xsxk/elective/grablessons?batchId=e49350a1926a4bfb95cf24eb361411c3',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'
}

# 请求体数据（从你提供的负载解析）
data = {
    'clazzType': 'FANKC',
    'clazzId': '2025202621300051504',
    'secretVal': 'gvQAbZNbV7WUcNlo2NuGHjRh1xL6it12PcEDhIKIT98VtYv/C4GCVAMRHP4p6JY7N+LoCHCDvgk+TwP7XriXtRFAmN9sxVOkSqUBfbZ5cZANkJ1lo+IiEVQpHQN2zFK/FBlB6jLF1+dTEzuN8Eg6zQnDwCmejXIXgBeYHExT9R/s='
}

# 注意：URL编码中的 %2B 是加号(+)的编码，%2F 是斜杠(/)的编码
# Python的requests会自动处理编码，所以可以直接使用解码后的值

# 发送POST请求
try:
    response = requests.post(url, headers=headers, data=data)
    
    print("=" * 60)
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    # 尝试解析JSON响应
    try:
        result = response.json()
        print(f"JSON响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        # 常见的响应字段解析
        if 'code' in result:
            print(f"\n返回代码: {result['code']}")
        if 'message' in result:
            print(f"返回消息: {result['message']}")
        if 'data' in result:
            print(f"返回数据: {result['data']}")
            
    except json.JSONDecodeError:
        print(f"文本响应: {response.text[:500]}...")  # 只显示前500字符
    
    print("=" * 60)
    
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")