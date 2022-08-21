# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : testTools.py
# Time       ：2022/8/20 下午5:12
# Author     ：Carl
# Description：
"""
import tkinter as tk
from tkinter import ttk
import requests

class GetTextApp(tk.Frame):
    '''翻译功能'''
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.place(width=800, height=600)
        # tk.Label(self, text="翻译").pack(anchor="nw")
        text_frame = tk.Frame(self, borderwidth=1, relief='sunken')
        text_frame.pack(padx=10, pady=10)

        self.input_text = tk.Text(text_frame, width=300, height=10, wrap=tk.WORD, font=15)
        self.input_text.pack()

        self.button = tk.Button(text_frame, text="翻译", command=self.resultsText)
        self.button.pack(anchor="center")

        self.results_text = tk.Text(text_frame, width=300, height=10, wrap=tk.WORD)
        self.results_text.pack()

    def getInputText(self):
        '''获取输入信息'''
        return self.input_text.get(1.0, tk.END)

    def resultsText(self):
        '''显示翻译结果'''
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, self.getTranslate())

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



if __name__ == '__main__':
    root = tk.Tk()
    root.title("test tools")
    root.geometry("800x600+10+10")

    tabNote = ttk.Notebook(root)
    tabNote.add(GetTextApp(tabNote), text="翻译")
    tabNote.pack(expand=0, anchor='nw')
    # GetTextApp(root)

    root.mainloop()