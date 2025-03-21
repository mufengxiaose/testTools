import os
from tkinter import Tk, ttk
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox
from common.VerficationCode import VerficationCode
from common.Translater import TranslaterApp
from common.QrcodeApp import QrcodeApp
from common.TimesstampHash import TimesstampHash
from common.Health import Health
from common.ImageProcessing import ImageProcessing
from common.DevicesApp import DevicesApp
from common.PanedWindowDemo import CustomFrame


if __name__ == "__main__":
    root = Tk()
    root.title("test tools")
    root.geometry("1000x600+70+10")

    tabStyle = ttk.Style()
    tabStyle.configure('TNotebook.Tab', foreground='blue')
    tabNote = ttk.Notebook(root, width=1000, height=600)

    tab_info = [
        (DevicesApp, "手机常用功能"),
        (VerficationCode, "验证码查询"),
        (QrcodeApp, "二维码生成"),
        (TimesstampHash, "时间戳md5转换"),
        (TranslaterApp, "翻译"),
        (Health, "健康计算"),
        (ImageProcessing, "图片处理"),
        (CustomFrame, "PanedWindowDemo")
    ]

    # 使用循环添加选项卡
    for app_class, tab_text in tab_info:
        tabNote.add(app_class(tabNote), text=tab_text)
    tabNote.pack(expand=0, anchor='nw')

    root.mainloop()
