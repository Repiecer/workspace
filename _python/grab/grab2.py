import httpx
import time
import sys

classids = ['20262027129001075T01',
            '20262027129001071T01',
            '20262027129001070T01',
            '20262027129001069T01',
            '20262027129001072T01',
            '20262027129001073T01',
            '20262027129001074T01',
            '20262027129001075T01',
            '20262027129001076T01',
            '20262027129001077T01',
            '20262027129001078T01',
            '20262027129001079T01',
            '20262027129001080T01',
            '20262027129001081T01',
            '20262027129001082T01',
            '20262027129001083T01',
            '20262027129001084T01',
            '20262027129001085T01',
            '20262027129001086T01']

secretvals = ['WTkgINXMCxChIi7ECVViwAV%2F8LYC91HJCrqpQsAqLL%2FV044zFK2skeeZ6ktsMd9q3zZIWgeKHNGe7zJUCwxWZfEEIpj3WDrpzW04XHM4TSy8eKvjCB7SDWY1Kpi3FwFyDxZjnHPqCq4rXI%2Bsas59IY3r6v0CjQXsISDOOIUeYbOUe49q5dLAZ2%2B%2B5LrbAGw%2BcewBRN4CW7dpriwLAzedJbQ7v5SSjPwv44%2FanXp6MOA%3D',
              'WTkgINXMCxChIi7ECVViwKs6Vwvh2U%2BYsLJZ2wycD9jJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcotvp%2BRPu3LL%2Bkf7wGceVXfpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              'WTkgINXMCxChIi7ECVViwPQf3nFjorc8EfviBs4yi7XJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcotvp%2BRPu3LL%2Bkf7wGceVXfpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              'Z0kKHe6jGZmCfcGPrGfvvzh3de7p4jIlDrFdH3pWwbfJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcotvp%2BRPu3LL%2Bkf7wGceVXfpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              'WTkgINXMCxChIi7ECVViwOWsHsi3TY0btPCpl7Ugv2bJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcincYz%2FxL5JV6qwAvTD0SxjpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              'WTkgINXMCxChIi7ECVViwE%2BUZha5QvhIBKRHgbFzzqvJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcincYz%2FxL5JV6qwAvTD0SxjpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              'WTkgINXMCxChIi7ECVViwGIGWvKfBvvYa6zCOhV%2B4kzJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcincYz%2FxL5JV6qwAvTD0SxjpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              'WTkgINXMCxChIi7ECVViwAV%2F8LYC91HJCrqpQsAqLL%2FV044zFK2skeeZ6ktsMd9q3zZIWgeKHNGe7zJUCwxWZfEEIpj3WDrpzW04XHM4TSy8eKvjCB7SDWY1Kpi3FwFyDxZjnHPqCq4rXI%2Bsas59IX5Sq43SR67lRWBcNoSsTKKUe49q5dLAZ2%2B%2B5LrbAGw%2BcewBRN4CW7dpriwLAzedJbQ7v5SSjPwv44%2FanXp6MOA%3D',
              'WTkgINXMCxChIi7ECVViwDll8ghd6U%2F%2FEVBgF6MOO0zV044zFK2skeeZ6ktsMd9q3zZIWgeKHNGe7zJUCwxWZfEEIpj3WDrpzW04XHM4TSy8eKvjCB7SDWY1Kpi3FwFyDxZjnHPqCq4rXI%2Bsas59IX5Sq43SR67lRWBcNoSsTKKUe49q5dLAZ2%2B%2B5LrbAGw%2BcewBRN4CW7dpriwLAzedJbQ7v5SSjPwv44%2FanXp6MOA%3D',
              'WTkgINXMCxChIi7ECVViwIMid%2BN7%2FgNeb7IdN1iVwy%2FJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcincYz%2FxL5JV6qwAvTD0SxjpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              'WTkgINXMCxChIi7ECVViwBQI6R1TfRoxG2Fbfo%2FyhJDJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcincYz%2FxL5JV6qwAvTD0SxjpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              'WTkgINXMCxChIi7ECVViwOWSHjnhtYVTHjNcFRjaovHV044zFK2skeeZ6ktsMd9q3zZIWgeKHNGe7zJUCwxWZfEEIpj3WDrpzW04XHM4TSy8eKvjCB7SDWY1Kpi3FwFyDxZjnHPqCq4rXI%2Bsas59IX5Sq43SR67lRWBcNoSsTKKUe49q5dLAZ2%2B%2B5LrbAGw%2BcewBRN4CW7dpriwLAzedJbQ7v5SSjPwv44%2FanXp6MOA%3D',
              '03DqPxgSyu%2BQg5E%2Ft2zpTt%2B5K2%2Bl7XHoIqLAPjY%2FLPrV044zFK2skeeZ6ktsMd9q3zZIWgeKHNGe7zJUCwxWZfEEIpj3WDrpzW04XHM4TSy8eKvjCB7SDWY1Kpi3FwFyDxZjnHPqCq4rXI%2Bsas59IX5Sq43SR67lRWBcNoSsTKKUe49q5dLAZ2%2B%2B5LrbAGw%2BcewBRN4CW7dpriwLAzedJbQ7v5SSjPwv44%2FanXp6MOA%3D',
              '03DqPxgSyu%2BQg5E%2Ft2zpTgCkU4Lrwg%2Bn%2BUHizPyXAsrV044zFK2skeeZ6ktsMd9q3zZIWgeKHNGe7zJUCwxWZfEEIpj3WDrpzW04XHM4TSy8eKvjCB7SDWY1Kpi3FwFyDxZjnHPqCq4rXI%2Bsas59IX5Sq43SR67lRWBcNoSsTKKUe49q5dLAZ2%2B%2B5LrbAGw%2BcewBRN4CW7dpriwLAzedJbQ7v5SSjPwv44%2FanXp6MOA%3D',
              '03DqPxgSyu%2BQg5E%2Ft2zpTjdkeIbZoaNqYh6SfpUzEqDJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcquXBPzavWmd0m4l2Nn3%2BETpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              '03DqPxgSyu%2BQg5E%2Ft2zpTvqLwUTm8uaDtIlAuhvDneLJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcquXBPzavWmd0m4l2Nn3%2BETpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              '03DqPxgSyu%2BQg5E%2Ft2zpTtpSXFnU%2BhfG22fo7vr7DP7JPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcquXBPzavWmd0m4l2Nn3%2BETpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              '03DqPxgSyu%2BQg5E%2Ft2zpTmiu8Blat1dUMkdHG%2B3w4aPJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcquXBPzavWmd0m4l2Nn3%2BETpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D',
              '03DqPxgSyu%2BQg5E%2Ft2zpTnqEO5h6vaRaF8260mGuj3%2FJPCVL6xEtYNel%2FEdzQpm0gKoJetVDXh1NgMZKE%2B0WJqAnVWp0cZGgaawCKLWyMTJNcIWTr8dH3riEDW1FVE%2BHNCSpepP1HhHX%2BMcVcQSzcquXBPzavWmd0m4l2Nn3%2BETpDiHb%2B4jOwT9ABRcAPSVFHgxauz8IU6iAGWo0IUl63g%3D%3D']

def add_class(classid, secretval):
    
    URL = "https://xsxk.nuist.edu.cn/xsxk/elective/clazz/add"
    TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzg4MjczMjQ3MDIyLCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoiNzdrMW90cnQ4YWk4bXJqcTU2NDN1aHBtM3QifQ.r4rQrDBlHm7w1UBSSxkFk5gj80wH-ZZPenuBl8h747WiAAZWtyN94uDw_ZVBuCpQSog3uOHXroqFhGpnDVu6xw"
    BATCH_ID = "0eaba5636fab45f995daf533b50f2576"

    headers = {
        "Cookie": f"route=7a64d2cafa90cef3cd58670333027aa1; Authorization={TOKEN}",
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
        f"&clazzId={classid}"
        f"&secretVal={secretval}"
    )

    with httpx.Client(http2=True, timeout=15, verify=False) as client:
        resp = client.post(URL, headers=headers, content=body)
        data = resp.json()
        msg = data.get('msg', '')
        print(msg[4:], end='')
        if msg!='课容量已满':
            sys.exit(0)



ans = 0
while True:
    print('route', ans)
    for i in range(len(classids)):
        
        add_class(classids[i], secretvals[i])
    print()
    ans +=1
    time.sleep(1)
