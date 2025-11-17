import urllib.request
from time import sleep
from lxml import etree
while True:
    
    response = urllib.request.urlopen('https://gkcf.jxedu.gov.cn/')
    html = etree.HTML(response.read().decode('utf-8'))

    if html.xpath('/html/body/div/div[2]/div/form/div[4]/div/input/@value')[0]=='成绩查询暂未开放':
        print('Not Yet')
    else:
        print('Time UpTime UpTime UpTime UpTime UpTime UpTime UpTime UpTime Up')
    sleep(10)
