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



if __name__ == "__main__":
    root = Tk()
    root.title("test tools")
    root.geometry("1000x600+70+10")

    tabStyle = ttk.Style()
    tabStyle.configure('TNotebook.Tab', foreground='blue')

    tabNote = ttk.Notebook(root, width=1000, height=600)
    # tabNote.add(DevicesApp(tabNote), text="手机常用功能")
    tabNote.add(VerficationCode(tabNote), text="验证码查询")
    tabNote.add(QrcodeApp(tabNote), text="二维码生成")
    # tabNote.add(UrlDecodeEncode(tabNote), text="url编码解码")
    # tabNote.add(DeviceLog(tabNote), text="日志")
    tabNote.add(TimesstampHash(tabNote), text="时间戳md5转换")
    tabNote.add(TranslaterApp(tabNote), text="翻译")
    # tabNote.add(Md5Transformation(tabNote), text="加密解密")
    tabNote.add(Health(tabNote), text="健康计算")
    tabNote.add(ImageProcessing(tabNote), text="图片处理")
    tabNote.pack(expand=0, anchor='nw')
    # NodebookFunc(master=root)

    root.mainloop()
