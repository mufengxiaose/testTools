# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath("."))
import time
import tkinter
from tkinter import ttk
import platform
from tkinter import messagebox
import subprocess
import datetime
from tkinter.filedialog import *
from PIL import ImageTk, Image


class mobileTools(object):

    def runCmd(self, str):
        '''启动cmd'''
        cmd = os.popen(str)
        return cmd.read()

    def get_device(self):
        '''获取设备状态'''
        status = self.runCmd("adb devices").strip()
        if status == "List of devices attached":
            status = "设备链接失败"
        elif "offline" in status:
            subprocess.Popen("adb kill-server")
            subprocess.Popen("adb devices")
        else:
            status = status.replace("List of devices attached", "").strip()
        return status

    def get_log(self):
        '''获取设备日志'''
        file_path = os.getcwd()
        log_file = file_path + r'\mobile_log'
        if os.path.exists(log_file):
            pass
        else:
            os.mkdir(log_file)
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file = "adb logcat -v threadtime > " + log_file + "/" + ctime + ".log"
        log1 = subprocess.Popen(args=file, shell=True, stdin=subprocess.PIPE, stdout=None)
        time.sleep(2)
        os.system("taskkill /t /f /pid {}".format(log1.pid))
        lists = os.listdir(log_file)
        lists.sort(key=lambda fn:os.path.getmtime(log_file + '/' + fn))
        file_new = os.path.join(log_file, lists[-1])
        return file_new

    def get_file_path(self):
        '''获取文件路径'''
        filepath = askopenfilename()
        entry_import.delete(0, tkinter.END)
        entry_import.insert(0, filepath)

    def install_package(self):
        '''安装package'''
        file = entry_import.get()
        if ".apk" in str(file):
            p = "adb shell pm list packages -3"
            if "com.huobionchainwallet" in self.runCmd(p):
                # return runCmd("adb install -r " + file)
                subprocess.Popen("adb install -r " + file, stdout=subprocess.PIPE, encoding='utf8')
            else:
                self.runCmd("adb install " + file)
                # time.sleep(1)
                if "com.huobionchainwallet" in self.runCmd(p):
                    messagebox.showinfo(message="安装成功")
                else:
                    messagebox.showinfo(message="安装失败")
        else:
            messagebox.showinfo(message="确认文件是否正确")

    def uninstall_package(self):
        '''卸载安装包'''
        str = "adb uninstall com.huobionchainwallet"
        uninstallPackgae = self.runCmd(str)
        if "com.huobionchainwallet" in self.runCmd(str):
            messagebox.showinfo(message="卸载失败")
        else:
            messagebox.showinfo(message="卸载成功")

    def screen_Shot(self):
        """截图"""
        file_path = os.getcwd()
        screenshotFile = file_path + r'\screenshot'
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        if not os.path.exists(screenshotFile):
            os.mkdir(screenshotFile)
        str = "adb shell screencap -p /sdcard/" +  ctime + ".png"
        pull_str = "adb pull /sdcard/" + ctime + ".png" + " " + screenshotFile
        self.runCmd(str)
        self.runCmd(pull_str)
        lists = os.listdir(screenshotFile)
        lists.sort(key=lambda fn:os.path.getmtime(screenshotFile + '/' + fn))
        file_new = os.path.join(screenshotFile, lists[-1])
        return file_new

def deviceConnect():
    '''设备链接状态文案'''
    deviceStatusText.delete(1.0, tkinter.END)
    deviceStatusText.insert(1.0, mobileTools().get_device())
def show_log_file():
    '''显示日志路径'''
    deviceLogPath.delete(1.0, tkinter.END)
    deviceLogPath.insert(1.0, mobileTools().get_log())

def show_screenshot_pic():
    global img0
    photo = Image.open(mobileTools().screen_Shot())
    photo = photo.resize((280, 500))
    img0 = ImageTk.PhotoImage(photo)
    img1 = tkinter.Label(window, image=img0)
    img1.place(x=750, y=50)
    show_path = tkinter.Label(window, text="截图保存路径: " + mobileTools().screen_Shot())
    show_path.place(x=100, y=160)

def share_screen():
    if (platform.system() == 'Windows'):
        os.startfile(os.path.abspath(".") + "/scrcpy/scrcpy.exe")
    elif (platform.system() == 'Linux'):
        print('Linux系统')
    else:
        print('其他')

#创建主窗口
window = tkinter.Tk()
window.title("Android 测试工具")
window.geometry("1100x900+10+10")
#设备状态
deviceStatus = tkinter.Label(window, text='设备状态')
deviceStatusText = tkinter.Text(window, width=30, height=1.4, bd=2, fg='blue', font='Helvetica -16')
deviceConnect()
refreshStatusBtn = tkinter.Button(window, text="更新状态", command=deviceConnect)
deviceStatus.place(x=3, y=11)
deviceStatusText.place(x=60, y=10)
refreshStatusBtn.place(x=350, y=4)
#日志部分
deviceLogBt = tkinter.Button(window,  text='获取日志', width=10, command=show_log_file)
deviceLogPath =tkinter.Text(window, fg="blue",
                           bd=2, width=60, height=1, font='Helvetica -16')
deviceLogBt.place(x=3, y=40)
deviceLogPath.delete(1.0, tkinter.END)
deviceLogPath.insert(1.0, "日志存放路径")
deviceLogPath.place(x=86, y=46)
#安装卸载
importFileBt = tkinter.Button(window, text='导入安装包', command=mobileTools().get_file_path)
entry_import = tkinter.Entry(window, width=60, bd=3, font=("宋体", 10, 'bold'))
installBt = tkinter.Button(window, text="安装", width=13, command=mobileTools().install_package)
uninstallBt = tkinter.Button(window, text="卸载钱包", width=20, command=mobileTools().uninstall_package)
importFileBt.place(x=3, y=80)
entry_import.delete(0, tkinter.END)
entry_import.insert(0, "apk路径...")
entry_import.place(x=80, y=88)
installBt.place(x=570, y=80)
uninstallBt.place(x=3, y=120)
#截图
screenShotBt = tkinter.Button(window, text="截图", width=20, command=show_screenshot_pic)
screenShotBt.place(x=200, y=120)
#实时屏幕
shareScreenBt = tkinter.Button(window, text="屏幕共享",width=20, command=share_screen)
shareScreenBt.place(x=10, y=200)


window.mainloop()
