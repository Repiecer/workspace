#encoding:utf-8

import requests
import json
from time import sleep
from tkinter import Tk, Entry, Label, Button, StringVar, scrolledtext, END, INSERT
from random import randint
url = 'https://022c-2409-8a38-5810-42f0-64-234a-4024-7254.ngrok-free.app'
class application(Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry('280x200')
        labe = Label(self, text='Name')
        labe.pack()
        self.textin = Entry(self)
        self.textin.pack()
        start = Button(self, text='Start', command=self.update)
        start.pack()
        self.show = scrolledtext.ScrolledText(self)
        self.show.pack()
    def update(self):
        #上传
        name = self.textin.get()
        diction = {}
        urltime = 'https://apis.map.qq.com/ws/location/v1/ip?key=53VBZ-AFAWG-ZCVQ4-QQUUO-26CKZ-5BFTS'

        html = requests.get(urltime).text.encode('utf-8')
        res = json.loads(html)
        diction["name"] = name
        diction["location"] = [res["result"]['location']['lat']+randint(1, 30), res["result"]['location']['lng']+randint(1, 30)]
        print(diction['name'])
        requests.post(url=url, data=json.dumps(diction))
        
        #下载更新
        response = requests.get(url).text.encode('utf-8')
        self.show.delete(1.0, END)
        for i in json.loads(response):
            
            self.show.insert(INSERT, i["name"]+'  ')
            for j in i["location"]:
                self.show.insert(INSERT, '  '+str(j))
            self.show.insert(INSERT, '\n')
            
if __name__ == "__main__":
    app = application()
    app.mainloop()
