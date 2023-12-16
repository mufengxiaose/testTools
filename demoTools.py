# -*- coding: utf-8 -*-
'''
@Time    : 2023/12/14 20:28
@Author  : Carl
@File    : demoTools.py
'''

import os
import platform, qrcode, subprocess, datetime, time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import *
from PIL import ImageTk
from PIL import Image as Img

class MenuBar(tk.Frame):
    '''菜单栏'''
    def __init__(self, master=None):
        # super().__init__(master)
        # self.pack()
        tk.Frame.__init__(self, master)
        self.master = master

        self.menu = tk.Menu(self.master, tearoff=False)
        self.master.config(menu=self.menu)

        self.fileMenu()
        self.helpMenu()

    def fileMenu(self):
        file_menu = tk.Menu(self.menu)
        file_menu.add_command(label='Item')
        # file_menu.add_command(label='Exit',)
        self.menu.add_cascade(label="File", menu=file_menu)

    def helpMenu(self):
        editMenu = tk.Menu(self.menu)
        editMenu.add_command(label='Exit', command=self.exitPrograme)
        self.menu.add_cascade(label="Help", menu=editMenu)

    def exitPrograme(self):
        exit()

class IndexPage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(expand=1, fill='both')

        self.IndexLeftFrame()
        self.IndexRightFrame()

    def IndexLeftFrame(self):
        self.frame_left = tk.Frame(self)
        self.frame_left.pack(side=tk.LEFT, expand=False, fill='y', anchor='w')
        bt_list = ['手机', 'url解析', '时间转换']
        for btn in bt_list:
            bt = tk.Button(self.frame_left, text=btn)
            bt.grid(padx=(10, 40), sticky=tk.NSEW)
            bt.bind('<Button-1>', self.changePage)

    def IndexRightFrame(self):
        self.frame_right = tk.Frame(self, bg='white', height=2)
        self.frame_right.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH, anchor='ne')
        PhoneFrame(self.frame_right)
        QrcodeFrame(self.frame_right)

    def changePage(self, event):
        res = event.widget['text']
        for i in self.frame_right.winfo_children():
            i.destroy()
        if res == '手机':
            self.frame_left.destroy()
            IndexPage(self.frame_right).changePage(None)
        elif res == 'url解析':
            pass
        elif res == '时间转换':
            pass

class PhoneFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=600, height=400)
        # self.pack(expand=1, anchor='nw', fill='x')
        # self.grid(row=0, column=0, sticky=tk.NSEW)
        self.place(x=10, y=10, relwidth=1, relheight=2, width=600, height=400)
        self.frame = tk.Frame(self)
        self.frame.pack(side='left', anchor='nw')
        # self.frame.grid(row=1, column=0, sticky=tk.NSEW)
        style = ttk.Style()
        style.configure("BW.TLabel",  borderwidth=1, relief=tk)

        self.label_frame = ttk.LabelFrame(self.frame, text='手机', width=600, height=400)
        self.label_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.status_label = tk.Label(self.label_frame, text='设备连接状态:')
        self.status_label.grid(row=0, column=0, sticky=tk.NSEW)
        # self.status_label.place(x=10, y=10)

        self.status_text = tk.Text(self.label_frame, width=30, height=1)
        self.status_text.grid(row=0, column=1, sticky=tk.NSEW, columnspan=3)
        # self.status_text.place(x=100, y=10)
        #
        self.refresh_status_button = tk.Button(self.label_frame, text='刷新状态')
        self.refresh_status_button.grid(row=0, column=4, sticky=tk.NSEW)
        # self.refresh_status_button.place(x=300, y=10)
        #
        # 获取手机日志
        self.log_label = tk.Label(self.label_frame, text="日志存放路径：")
        self.log_label.grid(row=1, column=0, sticky=tk.W)

        self.log_text = tk.Entry(self.label_frame, width=40)
        self.log_text.grid(row=1, column=1, sticky=tk.W, columnspan=3)

        self.get_log_bt = tk.Button(self.label_frame, width=12, text="获取手机日志",
                                 command=self.showLogPath)
        self.get_log_bt.grid(row=1, column=4, sticky=tk.W)

        # Android屏幕共享
        self.scrcpy_bt = tk.Button(self.label_frame, text="投屏", width=12, command=self.callScrcpy)
        self.scrcpy_bt.grid(row=3, column=0, sticky=tk.W)

        # Android截图
        self.screenshot_bt = tk.Button(self.label_frame, text="手机截图", width=12,
                                    command=self.creatScreenshotToplevel)
        self.screenshot_bt.grid(row=3, column=1, sticky=tk.W)

        # 重启手机
        self.reset_devices_bt = tk.Button(self.label_frame, text='重启手机', width=12,
                                       command=self.resetDevices)
        self.reset_devices_bt.grid(row=3, column=2, sticky=tk.W)

        # 启动app直接获取设备链接状态
        self.deviceConnect()

        # 安装apk
        self.install_apk()

    # 手机状态部分
    def callScrcpy(self):
        '''使用scrcpy功能'''
        self.phoneStatus()
        if CommonFunc().getSystemName() == 'Window':
            messagebox.showinfo(message='window 暂不支持')
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
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, self.GetDeviceList())

    # log 部分
    def GetLog(self):
        '''获取设备日志'''
        _file = '/mobile_log'
        CommonFunc().creatFile(file_path=_file)
        self.phoneStatus()
        log_file = os.getcwd() + _file
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file = "adb logcat -v threadtime > " + log_file + "/" + ctime + ".log"
        log1 = subprocess.Popen(args=file, shell=True, stdin=subprocess.PIPE, stdout=None)
        time.sleep(15)
        os.system("taskkill /t /f /pid {}".format(log1.pid))
        lists = os.listdir(log_file)
        lists.sort(key=lambda fn: os.path.getmtime(log_file + '/' + fn))
        file_new = os.path.join(log_file, lists[-1])
        return file_new

    def showLogPath(self):
        '''日志路径显示'''
        self.log_text.delete(1, tk.END)
        self.log_text.insert(1, self.GetLog())

        # Android手机截图

    def screenshotMethod(self):
        """截图"""
        _file = "/screenShot"
        CommonFunc().creatFile(file_path=_file)
        scr_file = os.getcwd() + _file
        ctime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        str = "adb shell screencap -p /sdcard/" + ctime + ".png"
        pull_str = "adb pull /sdcard/" + ctime + ".png" + " " + scr_file
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
        width, height = photo.size[0], photo.size[1]  # 获取图片宽高
        photo = photo.resize((int(width * 0.3), int(height * 0.3)))  # 图盘等比缩放
        screenImg = ImageTk.PhotoImage(photo)
        return screenImg

    def creatScreenshotToplevel(self):
        '''创建toplevel'''
        status = CommonFunc().runCmd("adb devices").strip()
        if status == "List of devices attached":
            messagebox.showinfo(message="手机未链接\n请重新链接手机")
        else:
            top = tk.Toplevel()
            top.title("截图")
            top.geometry('320x630')
            label = tk.Label(top, image=self.showScreenshotPic())
            label.pack()
    # 重启手机
    def resetDevices(self):
        self.phoneStatus()
        str0 = "adb reboot"
        return CommonFunc().runCmd(str0)

    def install_apk(self):
        '''安装apk'''
        openFIleBt = tk.Button(self.label_frame, text="导入安装包", command=self.get_file_path)
        openFIleBt.grid(row=2, column=0, sticky=tk.W)

        self.fileEntry = tk.Entry(self.label_frame)
        self.fileEntry.grid(row=2, column=1, columnspan=3, sticky=tk.NSEW)

        installBt = tk.Button(self.label_frame, text="安装", command=self.install_thread)
        installBt.grid(row=2, column=4, sticky=tk.NSEW)

    def get_file_path(self):
        '''获取文件路径'''
        filepath = askopenfilename()
        self.fileEntry.delete(0, tk.END)
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

    def phoneStatus(self):
        status = CommonFunc().runCmd("adb devices").strip()
        if status == "List of devices attached":
            messagebox.showinfo(message='设备链接失败\n请重新链接')

class QrcodeFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=400, height=400)
        # self.pack(anchor='nw', fill='both')
        # self.grid(row=1, column=0, sticky=tk.NSEW,rowspan=2, columnspan=2)
        self.place(x=10, y=300, relwidth=1, relheight=1)
        self.frame = tk.Frame(self, bd=1)
        self.frame.grid(row=1, column=1, sticky=tk.NSEW)

        style = ttk.Style()
        style.configure("QR.TLabel", background="green")

        self.label_frame = ttk.LabelFrame(self.frame, text='二维码生成', style="QR.TLabel", borderwidth=1)
        self.label_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.input_text = tk.Text(self.label_frame, height=10, width=80)
        self.input_text.grid(row=0, column=0, sticky=tk.NSEW)
        self.input_text.insert('1.0', '请输入要生成信息')
        # 生成二维码按钮
        self.button = tk.Button(self.label_frame, text="生成二维码", command=self.showQrcodeImg)
        self.button.grid(row=0, column=1, sticky=tk.NSEW)

        self.showQrcodeUi()
    def getText(self):
        '''获取文字内容'''
        return self.input_text.get("1.0", tk.END)

    def qrcodeGeneration(self):
        '''生成二维码'''
        file_path = "/qrcodeImg"
        CommonFunc().creatFile(file_path=file_path)
        qr_file = os.getcwd() + file_path
        self.qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        self.qr.add_data(self.getText())
        self.qr.make(fit=True)
        self.qr.make_image().save(qr_file + "/img.png")

    def showQrcodeUi(self):
        qrcode_frame = tk.Frame(self)
        qrcode_frame.grid(row=1, column=2, sticky=tk.NSEW)
        self.qrcode_label_frame = ttk.LabelFrame(qrcode_frame, text='二维码')
        self.qrcode_label_frame.grid(row=0, column=0, sticky=tk.NSEW)

    def showQrcodeImg(self):
        """展示二维码图片"""
        self.qrcodeGeneration()
        self.img = Img.open(os.getcwd() + "/qrcodeImg/img.png")
        print('img_size', self.img.size)
        self.img.resize((400, 400), Img.ANTIALIAS)
        print('img_size2', self.img.size)
        self.photo = ImageTk.PhotoImage(self.img)
        self.qc_label = tk.Label(self.qrcode_label_frame, image=self.photo)
        # self.qc_label.grid(row=1, column=1, sticky=tk.NSEW)
        self.qc_label.pack(side='left', anchor='nw')
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
    root.title('Demo')
    root.geometry("1200x600")
    menu = MenuBar(root)
    index = IndexPage(root)
    root.mainloop()