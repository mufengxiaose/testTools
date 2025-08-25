import os
import time
import datetime
import threading
import subprocess
import socket
from tkinter.filedialog import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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
        self.wedgit = Frame(self)
        self.wedgit.pack(fill=BOTH, expand=True)
        self.times_stamp_frame = Frame(self.wedgit, **STYTLE["time_stamp_frame"])
        self.times_stamp_frame.pack(fill=X, expand=False)
        self.deviceFrame = Frame(self.wedgit, **STYTLE["devices_frame"])
        self.deviceFrame.pack(fill=X, expand=False)

        # 手机weight
        self.devices_wedgit()
        # 时间转换
        self.times_stamp_wedgit()
    def devices_wedgit(self):
        # 手机链接状态，设备名显示
        self.status_label = Label(self.deviceFrame, text="设备链接状态：", **STYTLE["label"])
        self.status_label.grid(row=0, column=0, sticky=W)

        self.status_text = Text(self.deviceFrame, width=40, height=1, font=20)
        self.status_text.grid(row=0, column=1, sticky=W, columnspan=2)

        self.refresh_status_bt = Button(self.deviceFrame, text="刷新状态",
                                           command=self.deviceConnect, **STYTLE["button"])
        self.refresh_status_bt.grid(row=0, column=3)

        # 获取手机日志
        self.log_label = Label(self.deviceFrame, text="日志存放路径：", **STYTLE["label"])
        self.log_label.grid(row=1, column=0, sticky=W)

        self.log_text = Text(self.deviceFrame, width=40, height=1, font=20)
        self.log_text.grid(row=1, column=1, sticky=W, columnspan=2)

        self.get_log_bt = Button(self.deviceFrame, text="获取手机日志",
                                    command=self.show_log_path, **STYTLE["button"])
        self.get_log_bt.grid(row=1, column=3, sticky=W)

        # Android屏幕共享
        self.scrcpy_bt = Button(self.deviceFrame, text="投屏",
                                command=self.callScrcpy, **STYTLE["button"])
        self.scrcpy_bt.grid(row=2, column=2, sticky=W)

        # Android截图
        self.screenshot_bt = Button(self.deviceFrame, text="手机截图",
                                       command=self.creatScreenshotToplevel, **STYTLE["button"])
        self.screenshot_bt.grid(row=2, column=3, sticky=W)

        # 重启手机
        self.reset_devices_bt = Button(self.deviceFrame, text='重启手机',
                                          command=self.resetDevices, **STYTLE["button"])
        self.reset_devices_bt.grid(row=3, column=0, sticky=W)
        # 启动app直接获取设备链接状态
        self.deviceConnect()
        # 安装apk
        self.install_apk()
        # push文件
        self.pushFileUI()
        # 获取ip
        self.get_default_ip_ui()

    #手机状态部分
    def callScrcpy(self):
        '''使用scrcpy功能'''
        devices_status = CommonFunc().runCmd("adb devices").strip()
        try:
            if "device" not in devices_status:
                messagebox.showinfo(message="设备链接失败\n请重新链接手机")
                return
            if CommonFunc().getSystemName() == 'Window':
                pass
            else:
                return os.popen('scrcpy')
        except Exception as e:
            print(f'投屏失败{e}')

    def GetDeviceList(self):
        '''获取设备状态'''
        devices_status = CommonFunc().runCmd("adb devices").strip()
        if "device" not in devices_status:
            status = "设备链接失败"
        elif "offline" in devices_status:
            subprocess.Popen("adb kill-server")
            subprocess.Popen("adb devices")
        else:
            status = devices_status.replace("List of devices attached", "").strip()
        return status

    def deviceConnect(self):
        '''设备链接'''
        self.status_text.delete(1.0, END)
        self.status_text.insert(1.0, self.GetDeviceList())
        logger.info(f"deviceConnect_click_{self.deviceConnect}")

    #log 部分
    def get_log(self):
        '''获取设备日志'''
        LOG_DURATION = 8
        devices_status = self.get_devices_status()
        try:
            if "device" not in devices_status:
                messagebox.showinfo(message="手机未链接\n请重新链接手机")
                return
            
            log_file_name = self.create_log_file_name()
            cmd = ['adb ', 'logcat ', "-v ", "threadtime ", "> ", log_file_name]
            adb_logcat = subprocess.Popen(
                ''.join(cmd),
                shell=True, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info(f'adb_logcat_info{adb_logcat}')
            time.sleep(LOG_DURATION)
            if adb_logcat.poll() is None:  # 进程仍在运行
                # Windows使用taskkill，Linux/macOS使用pkill
                if os.name == "nt":
                    # 杀死进程组（包括子进程）
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(adb_logcat.pid)],
                        check=True
                    )
                else:
                    # 非Windows系统使用pkill
                    subprocess.run(
                        ["pkill", "-P", str(adb_logcat.pid)],  # 杀死父进程的子进程
                        check=True
                    )
                    adb_logcat.terminate()
                    # 6. 验证日志文件生成


        except subprocess.CalledProcessError as e:
            err_msg = f"进程终止失败：{str(e)}"
            messagebox.showerror("错误", err_msg)
            logger.error(f"get_log_process_error: {err_msg}")
        except FileNotFoundError:
            err_msg = "未找到adb命令，请检查ADB是否已配置到环境变量"
            messagebox.showerror("错误", err_msg)
            logger.error(f"get_log_adb_not_found: {err_msg}")
        except Exception as e:
            err_msg = f"日志获取失败：{str(e)}"
            messagebox.showerror("错误", err_msg)
            logger.error(f"get_log_error: {err_msg}")
    
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


    # 获取设备当前状态
    def get_devices_status(self):
        adb_devices = "adb devices"
        status = CommonFunc().runCmd(content=adb_devices).strip()
        return status

    def show_log_path(self):
        '''日志路径显示'''
        devcies_status = self.get_devices_status()
        try:
            if "device" not in devcies_status:
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
        devcies_status = self.get_devices_status()
        try:
            if "device" not in devcies_status:
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
        push_Bt = Button(self.deviceFrame, text="push文件到手机sdcard",
                         command=self.on_push_button_click, **STYTLE["button"])
        push_Bt.grid(row=2, column=1, sticky=NSEW)

    def adb_push(self, local_path, remote_path):
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
        local_path = askopenfilename(filetypes=[("apk文件", "*.apk")])
        print(local_path)
        status = self.get_devices_status()
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

    def get_default_ip_ui(self):
        get_ip_button = Button(self.deviceFrame, text="ip", command=self.get_default_ip, **STYTLE['button'])
        get_ip_button.grid(row=3, column=1)

    def get_default_ip(self):
        try:
            # 创建一个 UDP 套接字
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 连接到一个外部地址
            s.connect(("8.8.8.8", 80))
            # 获取本地 IP 地址
            ip = s.getsockname()[0]
            s.close()
            print(ip)
            messagebox.showinfo(message=f"ip地址:\n{ip}")
        except Exception as e:
            print(f"获取 IP 地址时出错: {e}")
            return None


    # 时间转换
    def times_stamp_wedgit(self):
        '''时间戳'''
        now_time_label = Label(self.times_stamp_frame, text="现在", **STYTLE["label"])
        now_time_label.grid(row=0, column=0, sticky=W)

        self.now_time = StringVar()
        self.now_time_label = Label(self.times_stamp_frame, text="", **STYTLE["timeLable"])
        self.now_time_label.grid(row=0, column=1, sticky=W)
        self.update_time()


        # 时间戳转时间
        self.timesstamp_label = Label(self.times_stamp_frame, text="时间戳",**STYTLE["label"])
        self.timesstamp_label.grid(row=1, column=0, sticky=W)

        self.timesstamp_entry = Entry(self.times_stamp_frame, width=30)
        self.timesstamp_entry.grid(row=1, column=1, sticky=W)
        self.timesstamp_entry.insert(1, int(time.time()))
        data = ["秒(s)", "毫秒(s)"]
        self.combobox = ttk.Combobox(self.times_stamp_frame,width=7)
        self.combobox['value'] = data
        self.combobox.current(0)
        self.combobox.grid(row=1, column=2, sticky=W)
        conversionBt = Button(self.times_stamp_frame, text="转换", command=self.timesstampToTime, **STYTLE["button"])
        conversionBt.grid(row=1, column=3, sticky=NSEW)

        self.datetime_text = Text(self.times_stamp_frame, height=1.5, width=30)
        self.datetime_text.grid(row=1, column=4, sticky=W)
        self.beijing_label = Label(self.times_stamp_frame, text="北京时间", **STYTLE["label"])
        self.beijing_label.grid(row=1, column=5, sticky=W)
        # 时间转时间戳
        self.time_0 = Label(self.times_stamp_frame, text="时间", **STYTLE["label"])
        self.time_0.grid(row=2, column=0, sticky=W)

        self.time_to_imestamp_entry = Entry(self.times_stamp_frame, width=30)
        self.time_to_imestamp_entry.grid(row=2, column=1, sticky=NSEW)
        self.time_to_imestamp_entry.insert(1, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.beijing_label1 = Label(self.times_stamp_frame, text="北京时间", **STYTLE["label"]).grid(row=2, column=2, sticky=W)
        conversionBt1 = Button(self.times_stamp_frame, text="转换", command=self.timeTotimestamp, **STYTLE["button"])
        conversionBt1.grid(row=2, column=3, sticky=NSEW)
        self.timesstamp_text1 = Text(self.times_stamp_frame, height=1.5, width=30)
        self.timesstamp_text1.grid(row=2, column=4, sticky=W)
        data = ["秒(s)", "毫秒(s)"]
        self.combobox1 = ttk.Combobox(self.times_stamp_frame, width=7)
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
        self.master.after(1000, self.update_time)
