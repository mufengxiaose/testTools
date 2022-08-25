# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : testTools.py
# Time       ：2022/8/20 下午5:12
# Author     ：Carl
# Description：
"""
import os, time, sys
import qrcode
import requests
import platform
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from PIL import Image as Img



class TranslaterApp(tk.Frame):
    '''翻译功能'''
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.place(width=800, height=600)
        # 设置frame
        text_frame = tk.Frame(self, borderwidth=1, relief='sunken')
        text_frame.pack(padx=10, pady=10)
        # 文字输入
        self.input_text = tk.Text(text_frame, width=300, height=10, wrap=tk.WORD, font=15)
        self.input_text.pack()
        # 翻译按钮
        self.button = tk.Button(text_frame, text="翻译", command=self.resultsText,
                                width=30)
        self.button.pack(anchor="center")
        # 显示翻译结果
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

class QrcodeApp(tk.Frame):
    '''二维码生成'''
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        # 设置frame
        self.qrcodeFrame = tk.Frame(self)
        self.qrcodeFrame.grid()
        # 输入文字
        self.input_text = tk.Text(self.qrcodeFrame, height=6, width=100)
        self.input_text.grid(row=0)
        # 生成二维码按钮
        self.button = tk.Button(self.qrcodeFrame, text="生成二维码", command=self.showQrcodeImg)
        self.button.grid(row=1, sticky=tk.W)

    def getText(self):
        '''获取文字内容'''
        return self.input_text.get("1.0", tk.END)

    def qrcodeGeneration(self):
        '''生成二维码'''
        file_path = "/qrcodeImg"
        CommonFunc().creatFile(file_path=file_path)
        qr_file = os.getcwd() + file_path
        self.qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=6,
            border=3,
        )
        self.qr.add_data(self.getText())
        self.qr.make(fit=True)
        return self.qr.make_image().save(qr_file + "/img.png")

    def showQrcodeImg(self):
        """展示二维码图片"""
        self.qrcodeGeneration()
        self.img = Img.open(os.getcwd() + "/qrcodeImg/img.png")
        self.photo = ImageTk.PhotoImage(self.img)
        self.qc_label = tk.Label(self.qrcodeFrame, image=self.photo)
        self.qc_label.grid(row=2)

class DevicesApp(tk.Frame):
    '''手机部分'''
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        self.deviceFrame = tk.Frame(self)
        self.deviceFrame.grid()
        # 手机链接状态，设备名显示
        self.status_label = tk.Label(self.deviceFrame, text="设备链接状态：")
        self.status_label.grid(row=0, column=0)

        self.status_text = tk.Text(self.deviceFrame, width=20, height=1, font=20)
        self.status_text.grid(row=0, column=1, sticky=tk.W)

        self.refresh_status_bt = tk.Button(self.deviceFrame, text="刷新状态", width=12)
        self.refresh_status_bt.grid(row=0, column=2)

        # 获取手机日志
        self.log_label = tk.Label(self.deviceFrame, text="日志存放路径：")
        self.log_label.grid(row=1, column=0, sticky=tk.W)

        self.log_text = tk.Entry(self.deviceFrame, width=60)
        self.log_text.grid(row=1, column=1, sticky=tk.W)

        self.get_log_bt = tk.Button(self.deviceFrame, width=12, text="获取手机日志")
        self.get_log_bt.grid(row=1, column=2, sticky=tk.W)

        # Android屏幕共享
        self.scrcpy_bt = tk.Button(self.deviceFrame, text="投屏", width=12)
        self.scrcpy_bt.grid(row=2, column=0, sticky=tk.W)

        # Android截图
        self.screenshot_bt = tk.Button(self.deviceFrame, text="手机截图", width=12,
                                       command=self.callScrcpy)
        self.screenshot_bt.grid(row=2, column=1, sticky=tk.W)

    def callScrcpy(self):
        '''使用scrcpy功能'''
        system = CommonFunc().getSystemName()
        print(system)


class CommonFunc():
    '''通用功能封装'''

    def runCmd(self, master):
        '''执行cmd'''
        return os.popen(master).read()

    def creatFile(self, file_path):
        """判断目录是否存在，没有则创建"""
        self._file = os.getcwd() + file_path
        if not os.path.exists(self._file):
            return os.mkdir(self._file)
        else:
            pass

    def getSystemName(self):
        '''获取电脑系统名称'''
        return platform.system()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("test tools")
    root.geometry("800x600+10+10")

    tabNote = ttk.Notebook(root)
    tabNote.add(DevicesApp(tabNote), text="手机常用功能")
    tabNote.add(TranslaterApp(tabNote), text="翻译")
    tabNote.add(QrcodeApp(tabNote), text="二维码生成")

    tabNote.pack(expand=0, anchor='nw')

    root.mainloop()