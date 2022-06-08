# -*- coding:utf-8 -*-
import os, sys
curPath = os.path.abspath(os.path.dirname('.'))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import subprocess
import threading
import datetime
import socket
import qrcode
import xlrd
from tkinter import *
import platform
from PIL import Image as Img
from PIL import ImageTk
from tkinter import ttk
from tkinter.filedialog import *
from tkinter import messagebox
import time


class App():

    def __init__(self):

        self.workbook = xlrd.open_workbook("address.xls")
        self.sheet = self.workbook.sheet_by_name("Sheet1")
        '''初始化页面'''
        frame = Frame(window)
        frame.pack()
        self.tab()
        self.status()
        self.device_log()
        self.get_fileBtn()
        self.install_package_btn()
        self.uninstall_wallet()
        self.screen_shot()
        self.show_pc_host()
        self.share_screen_btn()
        self.show_qrcode_btn()
        self.deviceConnect()
        self.chain_combobox()
        self.wallet_text()

    def tab(self):
        '''tab栏'''
        self.tabNode = ttk.Notebook()
        self.deviceControl = Frame(self.tabNode)
        self.qrControl = Frame(self.tabNode)
        self.wallet_key = Frame(self.tabNode)
        self.tabNode.add(self.deviceControl, text="手机")
        self.tabNode.add(self.qrControl, text="二维码")
        self.tabNode.add(self.wallet_key, text="钱包地址")
        self.tabNode.pack(expand=1, fill='both')

    def status(self):
        '''定义手机状态'''
        self.deviceStatus = Label(self.deviceControl, text="设备显示")
        self.statusText = Text(self.deviceControl,  width=30,
                               height=1.4, bd=2, fg='blue', font='Helvetica -16')
        self.statusBtn = Button(self.deviceControl, text="更新状态", command=self.deviceConnect)
        self.deviceStatus.place(x=10, y=11)
        self.statusText.place(x=70, y=10)
        self.statusBtn.place(x=360, y=4)

    def device_log(self):
        '''获取设备日志显示'''
        self.logBtn = Button(self.deviceControl, text='获取日志', width=10, command=self.show_log_file)
        self.logFilePath = Text(self.deviceControl, fg="blue",
                           bd=2, width=60, height=1, font='Helvetica -16')
        self.logBtn.place(x=10, y=40)
        self.logFilePath.delete(1.0, END)
        self.logFilePath.insert(1.0, "日志存放路径")
        self.logFilePath.place(x=92, y=46)

    def get_fileBtn(self):
        '''打开文件路径'''
        self.importFileBtn = Button(self.deviceControl, text='导入安装包', command=self.get_file_path)
        self.importFileBtn.place(x=10, y=80)

    def get_file_path(self):
        '''获取文件路径'''
        filepath = askopenfilename()
        self.entry_import.delete(0, END)
        self.entry_import.insert(0, filepath)

    def install_package_btn(self):
        '''安装apk'''
        self.entry_import = Entry(self.deviceControl, width=60, bd=2, font=("宋体", 11))
        self.installBt = Button(self.deviceControl, text="安装", width=13, command=self.install_package)
        self.entry_import.delete(0, END)
        self.entry_import.insert(0, "apk路径...")
        self.entry_import.place(x=80, y=88)
        self.installBt.place(x=570, y=80)

    def uninstall_wallet(self):
        '''卸载钱包'''
        self.uninstallBtn = Button(self.deviceControl, text="卸载钱包", width=20,
                                   command=DeviceTools().uninstall_huobi)
        self.uninstallBtn.place(x=10, y=120)

    def screen_shot(self):
        '''手机截图显示'''
        self.screenShotBtn = Button(self.deviceControl, text="手机截图", width=20,
                                    command=self.show_screenshot_pic)
        self.screenShotBtn.place(x=200, y=120)

    def share_screen_btn(self):
        '''手机屏幕共享'''
        self.shareScreenBt = Button(self.deviceControl, text="屏幕共享", width=20,
                                    command=DeviceTools().share_screen)
        self.shareScreenBt.place(x=10, y=150)

    def show_pc_host(self):
        '''获取电脑ip'''
        self.getHostIpBt = Button(self.deviceControl, text="获取ip地址", width=20,
                                  command=self.get_host_ip)
        self.getHostIpBt.place(x=200, y=150)

    def deviceConnect(self):
        '''设备链接'''
        self.statusText.delete(1.0, END)
        self.statusText.insert(1.0, DeviceTools().get_device())

    def show_log_file(self):
        '''日志路径显示'''
        self.logFilePath.delete(1.0, END)
        self.logFilePath.insert(1.0, DeviceTools().get_log())

    def show_qrcode_btn(self):
        '''二维码显示'''
        self.qrInfoText = Text(self.qrControl, width=57, height=4, fg='black', bd=2, font='Helvetica -16')
        self.qrInfoBt = Button(self.qrControl, text='生成二维码', width=30,
                               command=self.show_qr_img)
        self.qrInfoText.delete(1.0, END)
        self.qrInfoText.insert(1.0, "输入生成二维码信息")
        self.qrInfoText.place(x=10, y=10)
        self.qrInfoBt.place(x=100, y=100)


    def install_package(self):
        '''安装package'''
        file_path = self.entry_import.get()
        print(file_path)
        if  " " in str(file_path):
            messagebox.showinfo(message="apk路径有空格\n安装失败")
        else:
            status = DeviceTools().runCmd("adb devices").strip()
            if status == "List of devices attached":
                return messagebox.showinfo(message="手机未链接\n请重新链接手机")
            elif ".apk" in str(file_path):
                p = "adb shell pm list packages"
                if "com.huobionchainwallet" in DeviceTools().runCmd(p):
                    DeviceTools().runCmd("adb install -r " + file_path)
                    messagebox.showinfo(message="install success")
                else:
                    DeviceTools().runCmd("adb install " + file_path)
                    if "com.huobionchainwallet" in DeviceTools().runCmd(p):
                        messagebox.showinfo(message="安装成功")
                    else:
                        messagebox.showinfo(message="安装失败")
            else:
                messagebox.showinfo(message="确认文件是否正确")

    def show_screenshot_pic(self):
        '''显示截图'''
        global img0
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        photo = Img.open(DeviceTools().screen_shot_method())
        photo = photo.resize((250, 500))
        img0 = ImageTk.PhotoImage(photo)
        img1 = Label(self.deviceControl, image=img0)
        img1.place(x=750, y=50)
        show_path = Label(self.deviceControl,
                                  text=os.path.abspath(".") + r'\screenshot' + ctime + ".png",
                                  font=("微软雅黑", 10), fg="green")
        show_path.place(x=710, y=10)

    def get_host_ip(self):
        '''获取电脑ip'''
        get_ip = socket.gethostbyname(socket.gethostname())
        var_ip = StringVar(value='ip:' + get_ip)
        ip_label = Label(self.deviceControl, textvariable=var_ip, font=("宋体", 14, ), fg="blue")
        ip_label.place(x=400, y=150)
        return ip_label

    def qrcode_generation(self):
        '''二维码生成'''
        file_path = "/qrcodeImg"
        DeviceTools().creat_file(file_path=file_path)
        qr_file = os.getcwd() + file_path
        self.qc_info = self.qrInfoText.get("1.0", END)
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
        """展示二维码图片"""
        self.qrcode_generation()
        self.img = Img.open(os.getcwd() + "/qrcodeImg/img.png")
        self.photo = ImageTk.PhotoImage(self.img)
        self.qc_label = Label(self.qrControl, image=self.photo)
        self.qc_label.place(x=600, y=10)

    def chain_combobox(self):
        """主链显示combobox"""
        Label(self.wallet_key, text="主链选择：",).place(x=1, y=1)
        self.chainCombobox = ttk.Combobox(self.wallet_key)
        self.chainCombobox['value'] = self.get_chain_datas()
        self.chainCombobox.current(0)
        self.chainCombobox.place(x=80, y=1)
        self.chainCombobox.bind("<<ComboboxSelected>>", self.show_address)

    def wallet_text(self):
        """链信息显示框"""
        self.walletText = Text(self.wallet_key, height=15, width=85,
                               font=('微软雅黑', '15',))
        self.scroll_bar = Scrollbar(self.wallet_key)
        self.scroll_bar.config(command=self.walletText)
        self.walletText.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.place(x=1020, y=29, height=410)
        self.walletText.place(x=1, y=30)

    def get_address_datas(self):
        rows = self.sheet.nrows
        datas = []
        for i in range(2, rows):
            datas.append(self.sheet.row_values(i))
        return datas

    def get_chain_datas(self):
        chain_datas = []
        rows = self.sheet.nrows
        for i in range(2, rows):
            chain_datas.append(self.sheet.row_values(i)[0])
        chain_datas = list(set(chain_datas))
        chain_datas.sort()
        return chain_datas

    def show_address(self, chain):
        self.chain = chain
        self.chain = self.chainCombobox.get()
        self.walletText.delete(1.0, END)
        rows = self.sheet.nrows
        for i in range(2, rows):
            if self.chain == self.get_address_datas()[i][0]:
                chain_address = self.get_address_datas()[i][1]
                chain_key = self.get_address_datas()[i][2]
                chain_info = "链：" + self.chain + "\n" + \
                             "链地址: " + chain_address + "\n" + "私钥/助记词： " + chain_key + "\n" + "\n"
                self.walletText.insert(1.0, chain_info)

class DeviceTools(App):

    def __init__(self):
        super(App, self).__init__()

    def runCmd(self, str):
        '''启动cmd'''
        self.str = str
        cmd = os.popen(self.str)
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

    def creat_file(self, file_path):
        """判断目录是否存在，没有则创建"""
        self._file = os.getcwd() + file_path
        if not os.path.exists(self._file):
            return os.mkdir(self._file)
        else:
            pass


    def uninstall_huobi(self):
        '''卸载安装包'''
        status = self.runCmd("adb devices").strip()
        str = "adb uninstall com.huobionchainwallet"
        if status == "List of devices attached":
            return messagebox.showinfo(message="手机未链接\n请重新链接手机")
        else:
            self.runCmd(str)
            if "com.huobionchainwallet" in self.runCmd(str):
                messagebox.showinfo(message="卸载失败")
            else:
                messagebox.showinfo(message="卸载成功")

    def screen_shot_method(self):
        """截图"""
        _file = "/screenShot"
        self.creat_file(file_path=_file)
        scr_file = os.getcwd() + _file
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        status = self.runCmd("adb devices").strip()
        str = "adb shell screencap -p /sdcard/" +  ctime + ".png"
        pull_str = "adb pull /sdcard/" + ctime + ".png" + " " + scr_file
        if status == "List of devices attached":
            return messagebox.showinfo(message="手机未链接\n请重新链接手机")
        else:
            self.runCmd(str)
            self.runCmd(pull_str)
            lists = os.listdir(scr_file)
            lists.sort(key=lambda fn: os.path.getmtime(scr_file + '/' + fn))
            file_new = os.path.join(scr_file, lists[-1])
            return file_new

    def share_screen(self):
        '''手机同屏显示'''
        if (platform.system() == 'Windows'):
            os.startfile(os.path.abspath(".") + "/scrcpy/scrcpy.exe")
        elif (platform.system() == 'Linux'):
            print('Linux系统')
        else:
            os.system("/usr/local/bin/scrcpy")


if __name__ == '__main__':
    window = Tk()
    window.title("测试")
    window.geometry("1100x650")
    app = App()
    window.mainloop()
