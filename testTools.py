# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : testTools.py
# Time       ：2022/8/20 下午5:12
# Author     ：Carl
# Description：
"""
import os
import time
import qrcode
import requests
import platform
import subprocess
import datetime
import hashlib
import random
import threading
from tkinter.filedialog import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image as Img


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


class QrcodeApp(Frame):
    '''二维码生成'''
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        # 设置frame
        self.qrcodeFrame = Frame(self)
        self.qrcodeFrame.grid()
        # 输入文字
        self.input_text = Text(self.qrcodeFrame, height=6, width=100)
        self.input_text.grid(row=0)
        # 生成二维码按钮
        self.button = Button(self.qrcodeFrame, text="生成二维码", command=self.showQrcodeImg)
        self.button.grid(row=1, sticky=W)

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
        self.img = Img.open(os.getcwd() + "/qrcodeImg/img.png")
        self.photo = ImageTk.PhotoImage(self.img)
        self.qc_label = Label(self.qrcodeFrame, image=self.photo)
        self.qc_label.grid(row=2)

class DevicesApp(Frame):
    '''手机部分'''
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()

        self.deviceFrame = Frame(self)
        self.deviceFrame.grid()
        # 手机链接状态，设备名显示
        self.status_label = Label(self.deviceFrame, text="设备链接状态：")
        self.status_label.grid(row=0, column=0, sticky=W)

        self.status_text = Text(self.deviceFrame, width=20, height=1, font=20)
        self.status_text.grid(row=0, column=1, sticky=W, columnspan=3)

        self.refresh_status_bt = Button(self.deviceFrame, text="刷新状态", width=12,
                                           command=self.deviceConnect)
        self.refresh_status_bt.grid(row=0, column=4)

        # 获取手机日志
        self.log_label = Label(self.deviceFrame, text="日志存放路径：")
        self.log_label.grid(row=1, column=0, sticky=W)

        self.log_text = Entry(self.deviceFrame, width=40)
        self.log_text.grid(row=1, column=1, sticky=W, columnspan=3)

        self.get_log_bt = Button(self.deviceFrame, width=12, text="获取手机日志",
                                    command=self.showLogPath)
        self.get_log_bt.grid(row=1, column=4, sticky=W)

        # Android屏幕共享
        self.scrcpy_bt = Button(self.deviceFrame, text="投屏", width=12, command=self.callScrcpy)
        self.scrcpy_bt.grid(row=3, column=0, sticky=W)

        # Android截图
        self.screenshot_bt = Button(self.deviceFrame, text="手机截图", width=12,
                                       command=self.creatScreenshotToplevel)
        self.screenshot_bt.grid(row=3, column=1, sticky=W)

        # 重启手机
        self.reset_devices_bt = Button(self.deviceFrame, text='重启手机', width=12,
                                          command=self.resetDevices)
        self.reset_devices_bt.grid(row=3, column=2, sticky=W)

        # 启动app直接获取设备链接状态
        self.deviceConnect()

        # 安装apk
        self.install_apk()

    #手机状态部分
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

    #log 部分
    def GetLog(self):
        '''获取设备日志'''
        _file = '/mobile_log'
        CommonFunc().creatFile(file_path=_file)
        log_file = os.getcwd() + _file
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file = "adb logcat -v threadtime > " + log_file + "/" + ctime + ".log"
        log1 = subprocess.Popen(args=file, shell=True, stdin=subprocess.PIPE, stdout=None)
        time.sleep(15)
        os.system("taskkill /t /f /pid {}".format(log1.pid))
        lists = os.listdir(log_file)
        lists.sort(key=lambda fn:os.path.getmtime(log_file + '/' + fn))
        file_new = os.path.join(log_file, lists[-1])
        return file_new

    def showLogPath(self):
        '''日志路径显示'''
        self.log_text.delete(1, END)
        self.log_text.insert(1, self.GetLog())

    #Android手机截图
    def screenshotMethod(self):
        """截图"""
        _file = "/screenShot"
        CommonFunc().creatFile(file_path=_file)
        scr_file = os.getcwd() + _file
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        status = CommonFunc().runCmd("adb devices").strip()
        str = "adb shell screencap -p /sdcard/" +  ctime + ".png"
        pull_str = "adb pull /sdcard/" + ctime + ".png" + " " + scr_file
        if status == "List of devices attached":
            return messagebox.showinfo(message="手机未链接\n请重新链接手机")
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
        photo = Img.open(self.screenshotMethod())
        width, height = photo.size[0], photo.size[1] #获取图片宽高
        photo = photo.resize((int(width*0.3), int(height*0.3))) #图盘等比缩放
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
        openFIleBt = Button(self.deviceFrame, text="导入安装包", command=self.get_file_path)
        openFIleBt.grid(row=2, column=0, sticky=W)

        self.fileEntry = Entry(self.deviceFrame)
        self.fileEntry.grid(row=2, column=1, columnspan=3, sticky=NSEW)

        installBt = Button(self.deviceFrame, text="安装", command=self.install_thread)
        installBt.grid(row=2, column=4, sticky=NSEW)

    def get_file_path(self):
        '''获取文件路径'''
        filepath = askopenfilename()
        self.fileEntry.delete(0, END)
        self.fileEntry.insert(0, filepath)

    def install_package(self):
        '''安装package'''
        file_path = self.fileEntry.get()
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


if __name__ == '__main__':
    root = Tk()
    root.title("test tools")
    root.geometry("1000x600+10+10")

    tabNote = ttk.Notebook(root)
    tabNote.add(DevicesApp(tabNote), text="手机常用功能")
    tabNote.add(TranslaterApp(tabNote), text="翻译")
    tabNote.add(QrcodeApp(tabNote), text="二维码生成")
    tabNote.pack(expand=0, anchor='nw')


    root.mainloop()