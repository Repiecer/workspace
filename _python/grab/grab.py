import httpx
import time
def grab_lessons(batch_id="0eaba5636fab45f995daf533b50f2576", token="eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzg4MjczMjQ3MDIyLCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoiNzdrMW90cnQ4YWk4bXJqcTU2NDN1aHBtM3QifQ.r4rQrDBlHm7w1UBSSxkFk5gj80wH-ZZPenuBl8h747WiAAZWtyN94uDw_ZVBuCpQSog3uOHXroqFhGpnDVu6xw"):
    url = f"https://xsxk.nuist.edu.cn/xsxk/elective/grablessons?batchId={batch_id}"
    
    headers = {
        "Host": "xsxk.nuist.edu.cn",
        "Cookie": f"route=7a64d2cafa90cef3cd58670333027aa1; Authorization={token}",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Not;A=Brand";v="8", "Chromium";v="150"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://xsxk.nuist.edu.cn/xsxk/profile/index.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i"
    }
    
    with httpx.Client(http2=True, timeout=15, verify=False) as client:
        resp = client.get(url, headers=headers)
        return resp
ans = 0
while True:

    print(grab_lessons().status_code, ans)
    ans +=1
    time.sleep(60)