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
import base64
import datetime
import hashlib
import random
import threading
import subprocess
from tkinter.filedialog import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from Crypto.Cipher import AES
from urllib import parse


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
        self.qrcodeFrame = Frame(self, width=1000)
        self.qrcodeFrame.grid()
        # 输入文字
        self.input_text = Text(self.qrcodeFrame, height=6, width=100)
        self.input_text.grid(row=0, column=0, sticky=NSEW)
        # 生成二维码按钮
        self.button = Button(self.qrcodeFrame, text="生成二维码", command=self.showQrcodeImg)
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
        photo = Image.open(self.screenshotMethod())
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


class TimesstampHash(Frame):
    '''时间戳、md5转换'''
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()

        self.frame = Frame(self)
        self.frame.pack()

        self.times_stamp_wedgit()

    # 时间转换
    def times_stamp_wedgit(self):
        '''时间戳'''
        now_time_label = Label(self.frame, text="现在")
        now_time_label.grid(row=0, column=0, sticky=W)

        self.now_time = StringVar()
        self.now_time_label = Label(self.frame, text="", font=('Helvetica', 20), fg='red')
        self.now_time_label.grid(row=0, column=1, sticky=W)
        self.update_time()


        # 时间戳转时间
        self.timesstamp_label = Label(self.frame, text="时间戳")
        self.timesstamp_label.grid(row=1, column=0, sticky=W)

        self.timesstamp_entry = Entry(self.frame, width=30)
        self.timesstamp_entry.grid(row=1, column=1, sticky=W)
        self.timesstamp_entry.insert(1, int(time.time()))
        data = ["秒(s)", "毫秒(s)"]
        self.combobox = ttk.Combobox(self.frame,width=7)
        self.combobox['value'] = data
        self.combobox.current(0)
        self.combobox.grid(row=1, column=2, sticky=W)
        conversionBt = Button(self.frame, text="转换", command=self.timesstampToTime)
        conversionBt.grid(row=1, column=3, sticky=NSEW)

        self.datetime_text = Text(self.frame, height=1, width=30)
        self.datetime_text.grid(row=1, column=4, sticky=W)
        self.beijing_label = Label(self.frame, text="北京时间")
        self.beijing_label.grid(row=1, column=5, sticky=W)
        # 时间转时间戳
        self.time_0 = Label(self.frame, text="时间")
        self.time_0.grid(row=2, column=0, sticky=W)

        self.time_to_imestamp_entry = Entry(self.frame, width=30)
        self.time_to_imestamp_entry.grid(row=2, column=1, sticky=NSEW)
        self.time_to_imestamp_entry.insert(1, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.beijing_label1 = Label(self.frame, text="北京时间").grid(row=2, column=2, sticky=W)
        conversionBt1 = Button(self.frame, text="转换", command=self.timeTotimestamp)
        conversionBt1.grid(row=2, column=3, sticky=NSEW)
        self.timesstamp_text1 = Text(self.frame, height=1, width=30)
        self.timesstamp_text1.grid(row=2, column=4, sticky=W)
        data = ["秒(s)", "毫秒(s)"]
        self.combobox1 = ttk.Combobox(self.frame, width=7)
        self.combobox1['value'] = data
        self.combobox1.current(0)
        self.combobox1.grid(row=2, column=5, sticky=W)

    def timesstampToTime(self):
        '''时间戳转日期'''
        if self.combobox.get() == "秒(s)":
            time_conversion = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(self.timesstamp_entry.get())))
            self.datetime_text.delete(1.0, END)
            self.datetime_text.insert(1.0, time_conversion)
        else:
            var_time = int(self.timesstamp_entry.get())/1000
            time_convrsion = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(var_time))
            # print(time_convrsion)
            self.datetime_text.delete(1.0, END)
            self.datetime_text.insert(1.0, time_convrsion)

    def timeTotimestamp(self):
        '''时间转时间戳'''
        if self.combobox1.get() == "秒(s)":
            dt = self.time_to_imestamp_entry.get()
            time_conversion = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
            self.timesstamp_text1.delete(1.0, END)
            self.timesstamp_text1.insert(1.0, time_conversion)
        else:
            dt = self.time_to_imestamp_entry.get()
            time_conversion = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))*1000
            # print(time_conversion)
            self.timesstamp_text1.delete(1.0, END)
            self.timesstamp_text1.insert(1.0, time_conversion)

    def update_time(self):
        '''时间显示'''
        now = time.strftime("%Y-%m-%d %H:%M:%S") #格式化时间
        self.now_time_label.configure(text=now) #label时间填充
        root.after(1000, self.update_time) # 1000 ms后调用

class Md5Transformation(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.frame = Frame(self)
        self.frame.pack()

        self.hash_conversion_wedgit()
    # 加密解密
    def hash_conversion_wedgit(self):
        '''md5GUI'''
        r_text = (
            ("AES", "DES"),
            ("RC4", "Rabbit"),
            ("MD5",)
        )
        # 输入框
        self.md5_input_text = Text(self.frame, width=40, font=15)
        self.md5_input_text.grid(row=0, column=0, sticky=NSEW, rowspan=5)

        md5_label = Label(self.frame, text="加密选择，部分需要密码")
        md5_label.grid(row=0, column=1, sticky=NSEW, columnspan=2)
        # 输出框
        self.md5_output_text = Text(self.frame, width=40, font=15)
        self.md5_output_text.grid(row=0, column=3, rowspan=5, sticky=NSEW)
        # 单选按钮
        self.v = StringVar()
        self.v.set("MD5")
        for rindex, r in enumerate(r_text):
            for cindex, c in enumerate(r):
                self.radioBt = Radiobutton(self.frame, text=c, value=c, variable=self.v, height=1)
                self.radioBt.grid(row=rindex+1, column=cindex+1, sticky=W)

        self.salt_text = Text(self.frame, height=1, width=10)
        self.salt_text.grid(row=4, column=1, columnspan=2, sticky=NSEW)
        self.salt_text.insert(1.0, "输入16位密钥")

        self.encryptionBt = Button(self.frame, text="加密", command=self.encryptionFunc)
        self.encryptionBt.grid(row=5, column=1, sticky=W)

        self.decryptionBt = Button(self.frame, text="解密", command=self.decryptionFunc)
        self.decryptionBt.grid(row=5, column=2, sticky=E)

    def encryptionFunc(self):
        '''加密方法'''
        choice = self.v.get()
        inputText = self.md5_input_text.get(1.0, END)
        if choice == "MD5":
            h = hashlib.md5()
            h.update(str(inputText).encode('utf-8'))
            p = "小写32位: " + h.hexdigest() + "\n\n" + "大写32位: " + str(h.hexdigest()).upper()
            self.md5_output_text.delete(1.0, END)
            self.md5_output_text.insert(1.0, p)

        elif choice == "TripleDes":
            output = "TripleDes"
        elif choice == "AES":
            # salt = bytes(str(self.salt_text.get(1.0, END)).encode().strip())
            # # print(len(salt))
            # # print(salt)
            # aes = AES.new(key=salt, mode=AES.MODE_ECB)
            # cipher_text = aes.encrypt(self.md5_input_text.get(1.0, END))
            # print("密文", cipher_text)
            output= "功能未实现"
        elif choice == "DES":
            output= "功能未实现"
        elif choice == "RC4":
            output = "功能未实现"
        elif choice == "Rabbit":
            output= "功能未实现"
        else:
            output = "输入错误"
        return messagebox.showinfo(message={output})


    def decryptionFunc(self):
        '''解密方法'''
        choice = self.v.get()
        inputText = self.md5_input_text.get(1.0, END)
        if choice == "MD5":
            messagebox.showinfo(message="暂不支持解密")
        elif choice == "TripleDes":
            output = "TripleDes"
        elif choice == "AES":
            pass
        elif choice == "DES":
            pass
        elif choice == "RC4":
            pass
        elif choice == "Rabbit":
            pass
        else:
            output = "输入错误"


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

class Health(Frame):
    '''健康测量'''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.frame = Frame(self)
        self.weightX = StringVar()
        self.heightX = StringVar()
        self.frame.pack()
        self.BMIGui()


    def BMIGui(self):
        '''BMI'''
        self.weightLabel = Label(self.frame, text="体重（kg）")
        self.heightLabel = Label(self.frame, text="身高(厘米）")
        self.weightEntry = Entry(self.frame, width=10, textvariable=self.weightX)
        self.heightEntry = Entry(self.frame, width=10, textvariable=self.heightX)

        self.count = StringVar()
        self.count.set("BMI指数")
        self.countLabel = Label(self.frame, textvariable=self.count)
        self.countLabel.grid(row=2, column=1)
        self.countBt = Button(self.frame, text="开始计算", command=self.BMICount)

        self.weightLabel.grid(row=0, column=0, sticky=W)
        self.heightLabel.grid(row=1, column=0)
        self.weightEntry.grid(row=0, column=1)
        self.heightEntry.grid(row=1, column=1)
        self.countBt.grid(row=2, column=0)


    def BMICount(self):
        '''bmi 计算
        体重(kg)/身高(m)^2'''
        weight = self.weightEntry.get()
        height = self.heightEntry.get()
        message = "请输入正确数字"
        if weight==str or weight=='' or height==str or height==' ':
            messagebox.showinfo(message="%s"%message)
        else:
            weight = float(weight)
            height = float(height)/100
            height = height ** 2
            BMI = weight / height
            if BMI<=18.4:
                messagebox.showinfo(message="偏瘦")
            elif BMI>18.4 and BMI<24:
                messagebox.showinfo(message="正常")
            elif BMI>24 and BMI<28:
                messagebox.showinfo(message="过重")
            elif BMI>=28:
                messagebox.showinfo(message="肥胖")
            BMI = "%.2f" % BMI
            self.count.set(BMI)

class ImageProcessing(Frame):
    '''
    图片处理功能
    '''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack
        self.frame = Frame(self)
        self.frame.pack()
        self.ImgGui()

    def ImgGui(self):
        self.img = Button(self.frame, text='单图片处理', command=self.importImgFile)
        self.imgEntry = Entry(self.frame, width=20, textvariable="导入图片")
        self.imgFiles = Button(self.frame, text='多图片处理')
        self.imgsEntry = Entry(self.frame, width=20, textvariable="文件夹")
        self.compressBt = Button(self.frame, text="图片压缩", command=self.compressFunc)
        self.compressfactorCombobox = ttk.Combobox(self.frame, width=7)
        value = ('5', '10', '15', '20', '25', '30', '35', '40')
        self.compressfactorCombobox['value'] = value
        self.compressfactorCombobox.current(0)
        self.label0 = Label(self.frame, text="压缩倍数")

        self.img.grid(row=0, column=0, sticky=W)
        self.imgEntry.grid(row=0, column=1, sticky=W)
        self.imgFiles.grid(row=1, column=0, sticky=W)
        self.imgsEntry.grid(row=1, column=1, sticky=W)
        self.label0.grid(row=2, column=0, sticky=W)
        self.compressBt.grid(row=2, column=2, sticky=W)
        self.compressfactorCombobox.grid(row=2, column=1, sticky=W)

    def compressFunc(self):
        '''img compress'''
        img = self.imgEntry.get()
        filepath, filename = os.path.split(img)
        img_name, filetype = os.path.splitext(filename)
        # factor = self.compressfactor.get()
        factor = self.compressfactorCombobox.get()
        factor = int(factor)
        img = Image.open(img)
        output_dir = "images_2"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        new_file = img_name + '.jpg'
        img.save(os.path.join(output_dir, new_file), quality=factor)

    def importImgFile(self):
        '''file'''
        img = askopenfilename(filetypes=[('png', '*.png'), ('jpg', '*.jpg'),
                                         ('jpeg', '*jpeg'), ('gif', '*.gif')])
        self.imgEntry.delete(0, END)
        self.imgEntry.insert(0, img)

class UrlDecodeEncode(Frame):
    '''url解码编码'''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.frame = Frame(self)
        self.frame.pack()
        self.DecodeEncodeGui()

    def DecodeEncodeGui(self):
        '''Gui'''
        self.inputTxt = Text(self.frame, height=13, width=100)
        self.outputTxt = Text(self.frame,height=13, width=100)
        self.EncodeBt = Button(self.frame, text='编码')
        self.DecodeBt = Button(self.frame, text='解码', command=self.EncodeBtFun)

        self.inputTxt.grid(row=0, column=1, sticky=NSEW)
        self.EncodeBt.grid(row=0, column=0, rowspan=2, sticky=W)
        self.DecodeBt.grid(row=1, column=0, rowspan=2, sticky=W)
        self.outputTxt.grid(row=2, column=1, sticky=NSEW)
        # self.inputTxt.insert(INSERT, 'asdf')
        self.EncodeFun()

    def EncodeFun(self):
        '''解码'''
        url_txt = self.inputTxt.get('1.0', '1.end')
        # url_txt = "http://www.baidu.com?id=1"
        print("url_txt:", url_txt)
        out_txt = parse.unquote(url_txt)
        return out_txt


    def EncodeBtFun(self):
        self.outputTxt.delete('1.0', '1.end')
        self.outputTxt.insert('1.0', self.EncodeFun())
        print('output:' + self.EncodeFun())

class MenuBar(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.menubar = Menu(self.master, tearoff=False)
        self.master.config(menu=self.menubar)

    def fileMenu(self):
        file_menu = Menu(self.menubar, tearoff=False)
        file_menu.add_command(label='file')
        self.menubar.add_cascade(lable='File', menu=file_menu)

if __name__ == '__main__':
    root = Tk()
    root.title("test tools")
    root.geometry("1000x600+70+10")

    tabStyle = ttk.Style()
    tabStyle.configure('TNotebook.Tab', foreground='blue')

    tabNote = ttk.Notebook(root, width=1000, height=600)
    tabNote.add(DevicesApp(tabNote), text="手机常用功能")
    tabNote.add(QrcodeApp(tabNote), text="二维码生成")
    tabNote.add(UrlDecodeEncode(tabNote), text="url编码解码")
    # tabNote.add(DeviceLog(tabNote), text="日志")
    tabNote.add(TimesstampHash(tabNote), text="时间戳md5转换")
    tabNote.add(TranslaterApp(tabNote), text="翻译")
    tabNote.add(Md5Transformation(tabNote), text="加密解密")
    tabNote.add(Health(tabNote), text="健康计算")
    tabNote.add(ImageProcessing(tabNote), text="图片处理")
    tabNote.pack(expand=0, anchor='nw')
    # NodebookFunc(master=root)

    root.mainloop()