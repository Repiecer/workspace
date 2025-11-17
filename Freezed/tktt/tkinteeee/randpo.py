import tkinter

class chosenRand(tkinter.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title = '学号抽取器'
        self.geometry('500x400')
        resultLable = tkinter.Label(self, text='0',font=(None, 80), background='gray')
        resultLable.pack()
        

application = chosenRand()
application.mainloop()