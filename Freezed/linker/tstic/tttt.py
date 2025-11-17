import requests
import json

url = "http://httpbin.org/ip"  # 也可以直接在浏览器访问这个地址
r = requests.get(url)  # 获取返回的值
ip = json.loads(r.text)["origin"]  # 取其中某个字段的值
print(ip)

# 发送get请求
url = f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query&lang=zh-CN'
# 其中fields字段为定义接受返回参数，可不传；lang为设置语言，zh-CN为中文，可以传
res = requests.get(url)		# 发送请求
jsonobj = json.loads(res.text)
print(res.json(), end="\n")

data = json.loads(res.text)
with open('json.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))

dataJson = json.load(open('json.json', encoding='UTF-8'))  # 打开json文件，并将其中的数据全部读取
jsondata = [dataJson["country"], dataJson["regionName"], dataJson["city"]]  # 读取json文件中我们需要的部分
print(jsondata)
