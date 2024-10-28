# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : demoTk.py
# Time       ：2023/11/30 下午1:58
# Author     ：Carl
# Description：
"""
from tkinter import ttk
from tkinter import *
import threading
import os
import time
import qrcode
import requests
import platform
import base64
import datetime
import hashlib
import random
import threading
import subprocess
from tkinter.filedialog import *
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from Crypto.Cipher import AES
from urllib import parse

class MenuBar(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # self.pack()
        self.master = master

        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.fileMenu()
        self.helpMenu()

    def fileMenu(self):
        fileMenu = Menu(self.menu, tearoff=False)
        fileMenu.add_command(label="Item")
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        self.menu.add_cascade(label="File", menu=fileMenu)

    def helpMenu(self):
        editMenu = Menu(self.menu, tearoff=False)
        editMenu.add_command(label="Exit", command=self.exitProgram)
        # editMenu.add_command(label="Redo")
        self.menu.add_cascade(label="help", menu=editMenu)

    def exitProgram(self):
        exit()

class UrlDecodeEncode(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        # Label(self, text="UrlDecodeEncode").pack()
        self.frame = Frame(self)
        self.label_frame = LabelFrame(self.frame, text="url解码编码")
        self.label_frame.place(relx=0.2, rely=0.2, relwidth=0.3, relheight=0.6)
        # self.DecodeEncodeGui()

    # def DecodeEncodeGui(self):
    #     '''Gui'''
    #     self.inputTxt = Text(self.label_frame, height=13, width=100)
    #     self.outputTxt = Text(self.label_frame,height=13, width=100)
    #     self.EncodeBt = Button(self.label_frame, text='解码')
    #     self.DecodeBt = Button(self.label_frame, text='编码')
    #
    #     self.inputTxt.grid(row=0, column=1, sticky=NSEW)
    #     self.EncodeBt.grid(row=0, column=0, rowspan=2, sticky=W)
    #     self.DecodeBt.grid(row=1, column=0, rowspan=2, sticky=W)
    #     self.outputTxt.grid(row=2, column=1, sticky=NSEW)
    #     # self.inputTxt.insert(INSERT, 'asdf')

class IndexPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(expand=1, fill='both')

        self.leftFrame()
        self.rightFrame()

    def leftFrame(self):
        self.frame_left = Frame(self, background='yellow')
        self.frame_left.pack(side='left', expand=False, fill='y', padx=5, pady=5, anchor='w')
        # self.frame_left.grid(row=1, column=0, ipadx=20, ipady=30, padx=(10, 40), sticky=NSEW)
        bt_list = ['手机', 'url解析', '时间转换', '二维码']
        for i in bt_list:
            bt = Button(self.frame_left, text=i, height=2)
            bt.grid(ipadx=50, padx=(10, 40), sticky=NSEW)
            bt.bind("<Button-1>", self.changePage)

    def rightFrame(self):
        self.frame_right = Frame(self, background='red', width=200)
        self.frame_right.pack(side='right', expand=True, fill='both')
        PhoneTools(self.frame_right)
        QrcodeApp(self.frame_right)
    def changePage(self, event):
        res = event.widget['text']
        for i in self.frame_right.winfo_children():
            i.destroy()
        if res == '手机':
            self.frame_left.destroy()
            IndexPage(self.frame_right)
        elif res == 'url解析':
            # self.frame_right.destroy()
            Page2(self.frame_right)
            # UrlDecodeEncode(self.frame_right)
        elif res == '时间转换':
            Page3(self.frame_right)

        elif res == '二维码':
            QrcodeApp(self.frame_right)


class Page2(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack(expand=1, fill="both")
        self.frame = Frame(self)
        self.frame.pack()
        Label(self.frame, text="我是page2").pack()
        Button(self.frame, text='anniu ').pack()

class PhoneTools(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=1, fill='both')
        self.frame = Frame(self)
        self.frame.pack()

        self.label_frame = LabelFrame(self.frame, text='手机', bg='green')
        self.label_frame.pack()

        self.status_label = Label(self.label_frame, text="设备链接状态：")
        # self.status_label.grid(row=0, column=0, sticky=W)
        self.status_label.grid()

        self.status_text = Text(self.label_frame, width=20, height=1, font=20)
        self.status_text.grid(row=0, column=1, sticky=W, columnspan=3)

        self.refresh_status_bt = Button(self.label_frame, text="刷新状态", width=12,
                                        command=self.deviceConnect)
        self.refresh_status_bt.grid(row=0, column=4)

        # 获取手机日志
        self.log_label = Label(self.label_frame, text="日志存放路径：")
        self.log_label.grid(row=1, column=0, sticky=W)

        self.log_text = Entry(self.label_frame, width=40)
        self.log_text.grid(row=1, column=1, sticky=W, columnspan=3)

        self.get_log_bt = Button(self.label_frame, width=12, text="获取手机日志",
                                 command=self.showLogPath)
        self.get_log_bt.grid(row=1, column=4, sticky=W)

        # Android屏幕共享
        self.scrcpy_bt = Button(self.label_frame, text="投屏", width=12, command=self.callScrcpy)
        self.scrcpy_bt.grid(row=3, column=0, sticky=W)

        # Android截图
        self.screenshot_bt = Button(self.label_frame, text="手机截图", width=12,
                                    command=self.creatScreenshotToplevel)
        self.screenshot_bt.grid(row=3, column=1, sticky=W)

        # 重启手机
        self.reset_devices_bt = Button(self.label_frame, text='重启手机', width=12,
                                       command=self.resetDevices)
        self.reset_devices_bt.grid(row=3, column=2, sticky=W)

        # 启动app直接获取设备链接状态
        self.deviceConnect()

        # 安装apk
        self.install_apk()

        # 手机状态部分

    def callScrcpy(self):
        '''使用scrcpy功能'''
        if CommonFunc().getSystemName() == 'Window':
            pass
        else:
            return os.popen('scrcpy')

    def GetDeviceList(self):
        '''获取设备状态'''
        status = CommonFunc().runCmd("adb devices").strip()
        if status == "List of devices attached":
            status = "设备链接失败"
        elif "offline" in status:
            subprocess.Popen("adb kill-server")
            subprocess.Popen("adb devices")
        else:
            status = status.replace("List of devices attached", "").strip()
        return status

    def deviceConnect(self):
        '''设备链接'''
        self.status_text.delete(1.0, END)
        self.status_text.insert(1.0, self.GetDeviceList())

        # log 部分

    def GetLog(self):
        '''获取设备日志'''
        _file = '/mobile_log'
        CommonFunc().creatFile(file_path=_file)
        log_file = os.getcwd() + _file
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file = "adb logcat -v threadtime > " + log_file + "/" + ctime + ".log"
        if self.GetDeviceList() == "设备链接失败":
            messagebox.showinfo(message="手机未链接\n请重新链接手机")
        else:
            log1 = subprocess.Popen(args=file, shell=True, stdin=subprocess.PIPE, stdout=None)
            time.sleep(15)
            os.system("taskkill /t /f /pid {}".format(log1.pid))
            lists = os.listdir(log_file)
            lists.sort(key=lambda fn: os.path.getmtime(log_file + '/' + fn))
            file_new = os.path.join(log_file, lists[-1])
        return file_new

    def showLogPath(self):
        '''日志路径显示'''
        self.log_text.delete(1, END)
        self.log_text.insert(1, self.GetLog())

    # Android手机截图
    def screenshotMethod(self):
        """截图"""
        _file = "/screenShot"
        CommonFunc().creatFile(file_path=_file)
        scr_file = os.getcwd() + _file
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        status = CommonFunc().runCmd("adb devices").strip()
        str = "adb shell screencap -p /sdcard/" + ctime + ".png"
        pull_str = "adb pull /sdcard/" + ctime + ".png" + " " + scr_file
        if status == "List of devices attached":
            messagebox.showinfo(message="手机未链接\n请重新链接手机")
        else:
            CommonFunc().runCmd(str)
            CommonFunc().runCmd(pull_str)
            lists = os.listdir(scr_file)
            lists.sort(key=lambda fn: os.path.getmtime(scr_file + '/' + fn))
            file_new = os.path.join(scr_file, lists[-1])
            return file_new

    def showScreenshotPic(self):
        '''显示截图'''
        global screenImg
        photo = Image.open(self.screenshotMethod())
        width, height = photo.size[0], photo.size[1]  # 获取图片宽高
        photo = photo.resize((int(width * 0.3), int(height * 0.3)))  # 图盘等比缩放
        screenImg = ImageTk.PhotoImage(photo)
        return screenImg

    def creatScreenshotToplevel(self):
        '''创建toplevel'''
        top = Toplevel()
        top.title("截图")
        top.geometry('320x630')
        label = Label(top, image=self.showScreenshotPic())
        label.pack()
        # 重启手机

    def resetDevices(self):
        str0 = "adb reboot"
        return CommonFunc().runCmd(str0)

    def install_apk(self):
        '''安装apk'''
        openFIleBt = Button(self.label_frame, text="导入安装包", command=self.get_file_path)
        openFIleBt.grid(row=2, column=0, sticky=W)

        self.fileEntry = Entry(self.label_frame)
        self.fileEntry.grid(row=2, column=1, columnspan=3, sticky=NSEW)

        installBt = Button(self.label_frame, text="安装", command=self.install_thread)
        installBt.grid(row=2, column=4, sticky=NSEW)

    def get_file_path(self):
        '''获取文件路径'''
        filepath = askopenfilename()
        self.fileEntry.delete(0, END)
        self.fileEntry.insert(0, filepath)

    def install_package(self):
        '''安装package'''
        file_path = self.fileEntry.get()
        print(file_path)
        if " " in str(file_path):
            messagebox.showinfo(message="apk路径有空格\n安装失败")
        else:
            status = CommonFunc().runCmd("adb devices").strip()
            if status == "List of devices attached":
                return messagebox.showinfo(message="手机未链接\n请重新链接手机")
            elif ".apk" in str(file_path):
                p = "adb install "
                if "Success" in CommonFunc().runCmd(p + file_path):
                    messagebox.showinfo(message="安装成功")
                else:
                    messagebox.showinfo(message="安装失败")
            else:
                messagebox.showinfo(message="确认文件是否正确")

    def install_thread(self):
        """启用安装线程"""
        t1 = threading.Thread(target=self.install_package)
        t1.start()
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

class QrcodeApp(Frame):
    '''二维码生成'''
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        # 设置frame
        self.frame = Frame(self)
        self.frame.pack()
        self.label_frame = LabelFrame(self.frame, text='二维码生成')
        self.label_frame.place(relx=0.2, rely=0.2, relwidth=0.3, relheight=0.6)
        # self.qrcodeFrame = Frame(self, width=1000)
        # self.qrcodeFrame.grid()
        # 输入文字
        self.input_text = Text(self.label_frame, height=6, width=100)
        self.input_text.grid(row=0, column=0, sticky=NSEW)
        # 生成二维码按钮
        self.button = Button(self.label_frame, text="生成二维码", command=self.showQrcodeImg)
        self.button.grid(row=0, column=1, sticky=NSEW)

    def getText(self):
        '''获取文字内容'''
        return self.input_text.get("1.0", END)

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
        self.img = Image.open(os.getcwd() + "/qrcodeImg/img.png")
        self.photo = ImageTk.PhotoImage(self.img)
        self.qc_label = Label(self.label_frame, image=self.photo)
        self.qc_label.grid()
class Page3(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack(expand=1, fill="both")
        Label(self, text="我是page3").pack()



if __name__ == '__main__':
    root = Tk()
    root.wm_title("Tkinter window")
    root.wm_geometry("1200x600")
    app = MenuBar(root)
    IndexPage(root)
    # Index(root)
    root.mainloop()


