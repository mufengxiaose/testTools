# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath("."))
import time
import tkinter
import socket
import qrcode
import platform
from tkinter import messagebox
from tkinter import ttk
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
        _file = '/mobile_log'
        self.creat_file(file_path=_file)
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

    def get_file_path(self):
        '''获取文件路径'''
        filepath = askopenfilename()
        entry_import.delete(0, tkinter.END)
        entry_import.insert(0, filepath)

    def install_package(self):
        '''安装package'''
        file_path = entry_import.get()
        if  " " in str(file_path):
            tkinter.messagebox.showinfo(message="apk路径有空格\n安装失败")
        else:
            status = self.runCmd("adb devices").strip()
            if status == "List of devices attached":
                return tkinter.messagebox.showinfo(message="手机未链接\n请重新链接手机")
            elif ".apk" in str(file_path):
                p = "adb shell pm list packages"
                if "com.huobionchainwallet" in self.runCmd(p):
                    self.runCmd("adb install -r " + file_path)
                    messagebox.showinfo(message="install success")
                else:
                    self.runCmd("adb install " + file_path)
                    if "com.huobionchainwallet" in self.runCmd(p):
                        messagebox.showinfo(message="安装成功")
                    else:
                        messagebox.showinfo(message="安装失败")
            else:
                tkinter.messagebox.showinfo(message="确认文件是否正确")

    def uninstall_package(self):
        '''卸载安装包'''
        status = self.runCmd("adb devices").strip()
        str = "adb uninstall com.huobionchainwallet"
        if status == "List of devices attached":
            return tkinter.messagebox.showinfo(message="手机未链接\n请重新链接手机")
        else:
            self.runCmd(str)
            if "com.huobionchainwallet" in self.runCmd(str):
                messagebox.showinfo(message="卸载失败")
            else:
                messagebox.showinfo(message="卸载成功")

    def screen_Shot(self):
        """截图"""
        _file = "/screenShot"
        self.creat_file(file_path=_file)
        scr_file = os.getcwd() + _file
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        status = self.runCmd("adb devices").strip()
        str = "adb shell screencap -p /sdcard/" +  ctime + ".png"
        pull_str = "adb pull /sdcard/" + ctime + ".png" + " " + scr_file
        if status == "List of devices attached":
            return tkinter.messagebox.showinfo(message="手机未链接\n请重新链接手机")
        else:
            self.runCmd(str)
            self.runCmd(pull_str)
            lists = os.listdir(scr_file)
            lists.sort(key=lambda fn: os.path.getmtime(scr_file + '/' + fn))
            file_new = os.path.join(scr_file, lists[-1])
            return file_new

    def show_packages_3(self):
        '''查看三方库'''
        pass

    def get_host_ip(self):
        '''获取电脑ip'''
        _ip = socket.gethostbyname(socket.gethostname())
        ip_label = tkinter.Label(deviceControl, text="ip: " + _ip, font=("宋体", 14, ), fg="blue")
        ip_label.place(x=400, y=150)
        return ip_label

    def get_hash_md5(self):
        '''md5加密'''
        pass

    def creat_file(self, file_path):
        """
        判断目录是否存在，不存在则创建
        :param file_path:
        :return:
        """
        self._file = os.getcwd() + file_path
        if not os.path.exists(self._file):
            return os.mkdir(self._file)
        else:
            pass

    def qrcode_generation(self):
        '''二维码生成'''
        file_path = "/qrcodeImg"
        self.creat_file(file_path=file_path)
        qr_file = os.getcwd() + file_path
        self.qc_info = qrInfoText.get("1.0", tkinter.END)
        self.qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=6,
            border=3,
        )
        self.qr.add_data(self.qc_info)
        self.qr.make(fit=True)
        self.qr_img = self.qr.make_image()
        return self.qr_img.save(qr_file + "/img.png")

    def show_qr_img(self):
        """
        展示二维码图片
        :return:
        """
        self.qrcode_generation()
        self.img = Image.open(os.getcwd() + "/qrcodeImg/img.png")
        self.photo = ImageTk.PhotoImage(self.img)
        self.qc_label = tkinter.Label(qrControl, image=self.photo)
        self.qc_label.place(x=600, y=10)

    def share_screen(self):
        '''手机同屏显示'''
        if (platform.system() == 'Windows'):
            os.startfile(os.path.abspath(".") + "/scrcpy/scrcpy.exe")
        elif (platform.system() == 'Linux'):
            print('Linux系统')
        else:
            os.system("/usr/local/bin/scrcpy")

    def show_screenshot_pic(self):
        '''显示截图'''
        global img0
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        photo = Image.open(mobileTools().screen_Shot())
        photo = photo.resize((250, 500))
        img0 = ImageTk.PhotoImage(photo)
        img1 = tkinter.Label(deviceControl, image=img0)
        img1.place(x=750, y=50)
        show_path = tkinter.Label(deviceControl,
                                  text=os.path.abspath(".") + r'\screenshot' + ctime + ".png",
                                  font=("微软雅黑", 10), fg="green")
        show_path.place(x=710, y=10)


    def get_record_file(self):
        '''取出录屏文件'''
        self.stop_task()
        _file = "/Record"
        self.creat_file(file_path=_file)
        file_path = os.getcwd()
        _file = file_path + r'\Record'
        if os.path.exists(_file):
            pass
        else:
            os.mkdir(_file)
        str = "adb pull " + self.record_file + _file
        get_file = self.runCmd(str)
        return get_file

def deviceConnect():
    '''设备链接状态文案'''
    deviceStatusText.delete(1.0, tkinter.END)
    deviceStatusText.insert(1.0, mobileTools().get_device())
def show_log_file():
    '''显示日志路径'''
    deviceLogPath.delete(1.0, tkinter.END)
    deviceLogPath.insert(1.0, mobileTools().get_log())



#创建主窗口
window = tkinter.Tk()
window.title("Android 测试工具")
window.geometry("1100x650+10+10")
#Frame
tabNote = ttk.Notebook()
deviceControl = ttk.Frame(tabNote) #常用
qrControl = ttk.Frame(tabNote) # 二维码
tabNote.add(deviceControl, text="常用")
tabNote.add(qrControl, text="二维码")
tabNote.pack(expand=1, fill='both')

#设备状态
deviceStatus = tkinter.Label(deviceControl, text='设备状态')
deviceStatusText = tkinter.Text(deviceControl, width=30, height=1.4, bd=2, fg='blue', font='Helvetica -16')
deviceConnect()
refreshStatusBtn = tkinter.Button(deviceControl, text="更新状态", command=deviceConnect)
deviceStatus.place(x=10, y=11)
deviceStatusText.place(x=70, y=10)
refreshStatusBtn.place(x=360, y=4)
#日志部分
deviceLogBt = tkinter.Button(deviceControl,  text='获取日志', width=10, command=show_log_file)
deviceLogPath =tkinter.Text(deviceControl, fg="blue",
                           bd=2, width=60, height=1, font='Helvetica -16')
deviceLogBt.place(x=10, y=40)
deviceLogPath.delete(1.0, tkinter.END)
deviceLogPath.insert(1.0, "日志存放路径")
deviceLogPath.place(x=92, y=46)
#安装卸载
importFileBt = tkinter.Button(deviceControl, text='导入安装包', command=mobileTools().get_file_path)
entry_import = tkinter.Entry(deviceControl, width=60, bd=2, font=("宋体", 11, 'bold'))
installBt = tkinter.Button(deviceControl, text="安装", width=13, command=mobileTools().install_package)
uninstallBt = tkinter.Button(deviceControl, text="卸载钱包", width=20, command=mobileTools().uninstall_package)
entry_import.delete(0, tkinter.END)
entry_import.insert(0, "apk路径...")
importFileBt.place(x=10, y=80)
entry_import.place(x=80, y=88)
installBt.place(x=570, y=80)
uninstallBt.place(x=10, y=120)
#截图
screenShotBt = tkinter.Button(deviceControl, text="截图", width=20, command=mobileTools().show_screenshot_pic)
screenShotBt.place(x=200, y=120)
#实时屏幕
shareScreenBt = tkinter.Button(deviceControl, text="屏幕共享",width=20, command=mobileTools().share_screen)
shareScreenBt.place(x=10, y=150)
#获取ip
getHostIpBt = tkinter.Button(deviceControl, text="获取ip地址", width=20, command=mobileTools().get_host_ip)
getHostIpBt.place(x=200, y=150)

#二维码显示
qrInfoText = tkinter.Text(qrControl, width=57, height=4, fg='black', bd=2, font='Helvetica -16')
qrInfoBt = tkinter.Button(qrControl, text='生成二维码', width=30, command=mobileTools().show_qr_img)
qrInfoText.delete(1.0, tkinter.END)
qrInfoText.insert(1.0, "输入生成二维码信息")
qrInfoText.place(x=10, y=10)
qrInfoBt.place(x=100, y=100)


if __name__ == '__main__':
    window.mainloop()