import time,datetime
from tkinter import *
from tkinter import ttk


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
        # root.after(1000, self.update_time) # 1000 ms后调用
