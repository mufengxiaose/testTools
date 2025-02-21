import requests
import random
import hashlib
from tkinter import *

class TranslaterApp(Frame):
    '''翻译功能'''
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        # 设置frame
        text_frame = Frame(self, borderwidth=1, relief='sunken',width=500, height=600)
        text_frame.pack()

        data = ['英译汉','汉英译']
        self.combobox = ttk.Combobox(text_frame)
        self.combobox['value'] = data
        self.combobox.current(0)
        self.combobox.grid(row=0, column=1, sticky=W)

        # 文字输入
        label0 = Label(text_frame, text="待翻译文字：")
        label0.grid(row=1, column=0, sticky=W)
        self.input_text = Text(text_frame, height=8)
        self.input_text.grid(row=1, column=1, columnspan=3)
        # 有道翻译按钮
        self.button = Button(text_frame, text="有道翻译", command=self.resultsText)
        self.button.grid(row=2, column=1, sticky=W)
        #百度翻译
        self.baiduApi_bt = Button(text_frame, text="百度翻译", command=self.resultsText)
        self.baiduApi_bt.grid(row=2, column=2, sticky=W)
        # 显示翻译结果
        label1 = Label(text_frame, text='翻译结果：')
        label1.grid(row=3, column=0, sticky=W)
        self.results_text = Text(text_frame, wrap=WORD, height=8)
        self.results_text.grid(row=3, column=1, sticky=W, columnspan=3)

    def getInputText(self):
        '''获取输入信息'''
        return self.input_text.get(1.0, END)

    def resultsText(self):
        '''显示翻译结果'''
        self.results_text.delete(1.0, END)
        try:
            self.results_text.insert(1.0, self.getTranslate())
        except:
            self.results_text.insert(1.0, self.baiduApi())

    def getTranslate(self):
        '''获取有道翻译结果'''
        youdao_url = "http://fanyi.youdao.com/translate"
        params = {
            "doctype": "json",
            "type": "AUTO",
            "i": self.getInputText()
        }
        r = requests.get(url=youdao_url, params=params)
        return r.json()['translateResult'][0][0]['tgt']
    
    # 百度翻译api
    def getMd5(self, data):
        '''md5加密'''
        return hashlib.md5(str(data).encode(encoding='utf-8')).hexdigest()

    def baiduApi(self):
        '''百度api调用'''
        url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        appid = "20220813001305350"
        key = "6096HbMy1F6htfIXEJzk"
        salt = random.randint(300000,900000)
        sign_value = self.getMd5(appid + self.getInputText() + str(salt) + key)
        if self.combobox.get() == "英译汉":
            parmas = {
                "q": self.getInputText(),
                "from": "auto",
                "to": "zh",
                "appid": appid,
                "salt": salt,
                "sign":str(sign_value),
            }
            r = requests.get(url=url, params=parmas)
            return r.json()['trans_result'][0]['dst']
        else:
            parmas = {
                "q": self.getInputText(),
                "from": "auto",
                "to": "en",
                "appid": appid,
                "salt": salt,
                "sign": str(sign_value),
            }
            r = requests.get(url=url, params=parmas)
            return r.json()['trans_result'][0]['dst']