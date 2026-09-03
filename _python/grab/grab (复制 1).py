import httpx

URL = "https://xsxk.nuist.edu.cn/xsxk/elective/clazz/add"
TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzg4MjI4NTg4NzgxLCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoiNnZmYm40cm5iZ2lhZXB0Y3BiM2c3aG1sbnAifQ.2DgQlsp75E097DjMlvGK7YiPtmqm3GZWtGM4Bfhmov6aqEpKjWR5ePTD0J1HVJyRBsLMw_TeJI_eXlWem9Xb7w"
BATCH_ID = "0eaba5636fab45f995daf533b50f2576"

headers = {
    "Cookie": f"route=33efcd2f3cc6ef258b1dbadfba047ee9; Authorization={TOKEN}",
    "Authorization": TOKEN,
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Sec-Ch-Ua": '"Not;A=Brand";v="8", "Chromium";v="150"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Batchid": BATCH_ID,
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "Origin": "https://xsxk.nuist.edu.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": f"https://xsxk.nuist.edu.cn/xsxk/elective/grablessons?batchId={BATCH_ID}",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i",
}

# secretVal 已含 URL 编码（%2F 等），必须用 content 原样发送，
# 否则放入 data 字典会被 httpx 二次编码（% -> %25）导致服务器无法解密
body = (
    "clazzType=XGKC"
    "&clazzId=20262027129001076T01"
    "&secretVal=WTkgINXMCxChIi7ECVViwDll8ghd6U%2F%2FEVBgF6MOO0zV044zFK2skeeZ6ktsMd9q3zZIWgeKHNGe7zJUCwxWZfEEIpj3WDrpzW04XHM4TSy8eKvjCB7SDWY1Kpi3FwFyZOTqXNYXIJeaKIVL5b0MH7vb6KNPoVL81qIYguXrcOt%2BTGXeLps7CtzKFk5mF3klG0cuZKqJu%2FOxdexqQptw1bQ7v5SSjPwv44%2FanXp6MOA%3D"
)

with httpx.Client(http2=True, timeout=15, verify=False) as client:
    resp = client.post(URL, headers=headers, content=body)
    print(resp.http_version, resp.status_code)
    print(resp.text)
