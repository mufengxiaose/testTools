import os
import time
import datetime
import threading
import subprocess
from tkinter.filedialog import *
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from app.utils.common import CommonFunc
from app.utils.Logger import Logger
from app.stytles.tk_stytles import STYTLE

logger = Logger().get_logger()


class DevicesApp(Frame):
    '''手机部分'''
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()

        self.deviceFrame = Frame(self, **STYTLE["frame"])
        self.deviceFrame.pack(fill=BOTH, expand=True)
        # 手机链接状态，设备名显示
        self.status_label = Label(self.deviceFrame, text="设备链接状态：", **STYTLE["label"])
        self.status_label.grid(row=0, column=0, sticky=W)

        self.status_text = Text(self.deviceFrame, width=40, height=1, font=20)
        self.status_text.grid(row=0, column=1, sticky=W, columnspan=2)

        self.refresh_status_bt = Button(self.deviceFrame, text="刷新状态", width=12,
                                           command=self.deviceConnect, **STYTLE["button"])
        self.refresh_status_bt.grid(row=0, column=3)

        # 获取手机日志
        self.log_label = Label(self.deviceFrame, text="日志存放路径：", **STYTLE["label"])
        self.log_label.grid(row=1, column=0, sticky=W)

        self.log_text = Text(self.deviceFrame, width=40, height=1, font=20)
        self.log_text.grid(row=1, column=1, sticky=W, columnspan=2)

        self.get_log_bt = Button(self.deviceFrame, width=12, text="获取手机日志",
                                    command=self.show_log_path, **STYTLE["button"])
        self.get_log_bt.grid(row=1, column=3, sticky=W)

        # Android屏幕共享
        self.scrcpy_bt = Button(self.deviceFrame, text="投屏", width=12, 
                                command=self.callScrcpy, **STYTLE["button"])
        self.scrcpy_bt.grid(row=2, column=2, sticky=W)

        # Android截图
        self.screenshot_bt = Button(self.deviceFrame, text="手机截图", width=12,
                                       command=self.creatScreenshotToplevel, **STYTLE["button"])
        self.screenshot_bt.grid(row=2, column=3, sticky=W)

        # 重启手机
        self.reset_devices_bt = Button(self.deviceFrame, text='重启手机', width=12,
                                          command=self.resetDevices, **STYTLE["button"])
        self.reset_devices_bt.grid(row=4, column=0, sticky=W)

        # 启动app直接获取设备链接状态
        self.deviceConnect()

        # 安装apk
        self.install_apk()

        # push文件
        self.pushFileUI()
    #手机状态部分
    def callScrcpy(self):
        '''使用scrcpy功能'''
        status = CommonFunc().runCmd("adb devices").strip()
        try:
            if status == "List of devices attached":
                return messagebox.showinfo(message="设备链接失败\n请重新链接手机")
            if CommonFunc().getSystemName() == 'Window':
                pass
            else:
                return os.popen('scrcpy')
        except Exception as e:
            print(f'投屏失败{e}')

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
        logger.info(f"deviceConnect_click_{self.deviceConnect}")

    #log 部分
    def get_log(self):
        '''获取设备日志'''
        status = self.get_devices_status()
        try:
            if status == "List of devices attached":
                messagebox.showinfo(message="手机未链接\n请重新链接手机")
            else:
                log_file_name = self.create_log_file_name()
                adb_logcat_text = "adb logcat -v threadtime > " + log_file_name
                adb_logcat = subprocess.Popen(args=adb_logcat_text, shell=True, stdin=subprocess.PIPE, stdout=None)
                time.sleep(8)
                os.system("taskkill /t /f /pid {}".format(adb_logcat.pid))
        except Exception as e:
            logger.info(f"get_log_error_{e}")
    
    def create_log_file_name(self):
        '''
        生成日志路径
        :return:
        '''
        log_path = '/mobile_log'
        CommonFunc().creatFile(file_path=log_path)
        log_file = os.getcwd() + log_path
        format_time = self.create_format_time()
        log_name = log_file + "/" + format_time + ".log"
        return log_name

    
    # def log_thread(self):
    #     thread = threading.Thread(target=self.GetLog)
    #     thread.start()
    
    # def on_log_button_click(self):
    #     self.log_thread()

    # 获取设备当前状态
    def get_devices_status(self):
        adb_devices = "adb devices"
        status = CommonFunc().runCmd(content=adb_devices).strip()
        return status

    def show_log_path(self):
        '''日志路径显示'''
        status = self.get_devices_status()
        try:
            if status == "List of devices attached":
                self.log_text.delete(1.0, END)
                messagebox.showinfo(message="设备链接失败")
                logger.info(f"show_log_path_device_link_error_{status}")
            else:
                self.get_log()
                self.log_text.delete(1.0, END)
                self.log_text.insert(1.0, self.create_log_file_name())
        except Exception as e:
            logger.info(f"show_log_path_error{e}")

    def create_format_time(self):
        format_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        return format_time
    
    #Android手机截图
    def screenshotMethod(self):
        """截图"""
        _file = "/screenShot"
        CommonFunc().creatFile(file_path=_file)
        scr_path = os.getcwd() + _file
        format_time = self.create_format_time()
        picture = format_time + ".png"
        screen_pic = "adb shell screencap -p /sdcard/" + picture
        pull_pic = "adb pull /sdcard/" + picture + " " + scr_path
        status = self.get_devices_status()
        try:
            if status == "List of devices attached":
                messagebox.showinfo(message="手机未链接\n请重新链接手机")
            # 截图
            else:
                CommonFunc().runCmd(screen_pic)
                # pull
                CommonFunc().runCmd(pull_pic)
                lists = os.listdir(scr_path)
                lists.sort(key=lambda fn: os.path.getmtime(scr_path + '/' + fn))
                file_new = os.path.join(scr_path, lists[-1])
                return file_new
        except Exception as e:
            logger.info(f'screen_pic_failed_{e}')

    def showScreenshotPic(self):
        '''显示截图'''
        global screenImg
        try:
            photo = Image.open(self.screenshotMethod())
            width, height = photo.size[0], photo.size[1] #获取图片宽高
            photo = photo.resize((int(width*0.3), int(height*0.3))) #图盘等比缩放
            screenImg = ImageTk.PhotoImage(photo)
            return screenImg
        except Exception as e:
            logger.info(f"show_screen_pic_error_{e}")
            return

    def creatScreenshotToplevel(self):
        '''创建toplevel'''
        image_ = self.showScreenshotPic()
        if hasattr(self, 'top') and isinstance(self.top, Toplevel):
            self.top.destroy()
        try:
            if image_:
                self.top = Toplevel()
                self.top.title("截图")
                self.top.geometry('320x630')
                label = Label(self.top, image=image_)
                label.pack()
        except Exception as e:
            logger.info(f"screen_shot_error_{e}")
            
    # 重启手机
    def resetDevices(self):
        reboot = "adb reboot"
        return CommonFunc().runCmd(reboot)

    # push文件功能
    def pushFileUI(self):
        # openFIleBt = Button(self.deviceFrame, text="文件", command=self.get_push_file,
        #                     **STYTLE["button"])
        # openFIleBt.grid(row=3, column=0, sticky=W)

        # self.push_fileEntry = Entry(self.deviceFrame)
        # self.push_fileEntry.grid(row=3, column=1, columnspan=3, sticky=NSEW)

        push_Bt = Button(self.deviceFrame, text="push文件，路径push>>sdcard", 
                         command=self.on_push_button_click, **STYTLE["button"])
        push_Bt.grid(row=2, column=1, sticky=NSEW)

    def adb_push(self, local_path, remote_path):
        # local_path = self.push_fileEntry.get()
        # remote_path = "/sdcard"
        try:
            if " " in str(local_path):
                messagebox.showinfo(message="文件路径有空格")
            else:
                process = subprocess.Popen(
                    ['adb', 'push', local_path, remote_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                stdout, stderr = process.communicate()
                if process.returncode == 0:
                    # 命令执行成功
                    print("文件推送成功！")
                    messagebox.showinfo(message="文件推送成功")
                else:
                    # 命令执行失败
                    print("文件推送失败！")
                    messagebox.showinfo(message="文件推送失败")
        except Exception as e:
            print(f"发生异常{e}")
    def run_adb_push_in_stread(self, local_path, remote_path):
        thread = threading.Thread(target=self.adb_push, args=(local_path, remote_path))
        thread.start()
        thread.join(2)
    
    def on_push_button_click(self):
        # local_path = self.push_fileEntry.get()
        local_path = askopenfilename()
        print(f"local_path__{local_path}")
        remote_path = "/sdcard"
        if local_path:
            return self.run_adb_push_in_stread(local_path, remote_path)
        else:
            return messagebox.showinfo(message="文件为空")

    
    def get_push_file(self):
        filepath = askopenfilename()
        self.push_fileEntry.delete(0, END)
        self.push_fileEntry.insert(0, filepath)

    def install_apk(self):
        '''安装apk'''
        # openFIleBt = Button(self.deviceFrame, text="导入安装包", 
        #                     command=self.get_file_path, **STYTLE["button"])
        # openFIleBt.grid(row=2, column=0, sticky=W)

        # self.adb_install_fileEntry = Entry(self.deviceFrame)
        # self.adb_install_fileEntry.grid(row=2, column=1, columnspan=3, sticky=NSEW)

        installBt = Button(self.deviceFrame, text="安装.apk文件", 
                           command=self.on_adb_install_click, **STYTLE["button"])
        installBt.grid(row=2, column=0, sticky=NSEW)

    def get_file_path(self):
        '''获取.apk文件路径'''
        filepath = askopenfilename()
        self.adb_install_fileEntry.delete(0, END)
        self.adb_install_fileEntry.insert(0, filepath)

    def adb_install_package(self):
        '''安装package'''
        # local_path = self.adb_install_fileEntry.get()
        local_path = askopenfilename(filetypes=[("apk文件", "*.apk")])
        print(local_path)
        status = self.get_devices_status()
        # adb_install = ["adb", "install", " ", local_path]
        adb_install = "adb install" + " "
        if local_path:          
            if status == "List of devices attached":
                return messagebox.showinfo(message="手机未链接\n请重新链接手机")
            elif " " in local_path:
                messagebox.showinfo(message="apk路径有空格\n安装失败")
            elif ".apk" in str(local_path):              
                messagebox.showinfo(message="安装中...")
                if "Success" in CommonFunc().runCmd(adb_install + local_path):
                    messagebox.showinfo(message="安装成功")
                else:
                    messagebox.showinfo(message="安装失败")
                
                # stdout, stderr = CommonFunc().run_subprocess_popen(args=adb_install)
                # print(f"stdout:{stdout}" + "\n" + f"stderr:{stderr}")
                # if "Success" in stdout:
                #     messagebox.showinfo(message="安装成功")
                # else:
                #     messagebox.showinfo(message="安装失败")
            else:
                messagebox.showinfo(message="确认文件是否正确")
        else:
            messagebox.showinfo(message="文件不能为空")


    def run_adb_install_thread(self):
        """启用安装线程"""
        thread = threading.Thread(target=self.adb_install_package)
        thread.start()
        if thread.is_alive():
            print("Thread is still running")
        else:
            print("Thread has finished")
    # 安装apk点击
    def on_adb_install_click(self):
        self.run_adb_install_thread()