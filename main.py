from tkinter import Tk
from tkinter import ttk
from app.views.VerficationCode import VerficationCode
from app.views.QrcodeApp import QrcodeApp
from app.views.TimesstampHash import TimesstampHash
from app.views.Health import Health
from app.views.ImageProcessing import ImageProcessing
from app.views.DevicesApp import DevicesApp
from app.views.PanedWindowDemo import CustomFrame


if __name__ == "__main__":
    root = Tk()
    root.title("test tools")
    root.geometry("1200x600+70+10")

    tabStyle = ttk.Style()
    tabStyle.configure('TNotebook.Tab', foreground='blue')
    tabNote = ttk.Notebook(root, width=1200, height=600)

    tab_info = [
        (DevicesApp, "手机常用功能"),
        (VerficationCode, "常用测试工具"),
        (QrcodeApp, "二维码生成"),
        (TimesstampHash, "时间戳md5转换"),
        (Health, "健康计算"),
        (ImageProcessing, "图片处理"),
        (CustomFrame, "PanedWindowDemo")
    ]

    # 使用循环添加选项卡
    for app_class, tab_text in tab_info:
        tabNote.add(app_class(tabNote), text=tab_text)
    tabNote.pack(expand=0, anchor='nw')

    root.mainloop()
