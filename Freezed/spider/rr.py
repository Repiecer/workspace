import requests

for i in range(1, 1000):
    url = "https://vip.aqdw"+str(i)+".com/videos/tag/cartoon"
    try:
        resss = requests.get(url, timeout=0.5)
    except:
        pass
    else:
        if resss.status_code == 200:
            print(f"URL:HTTPS_{i}", "CONNECT SUCCESSFULLY")

