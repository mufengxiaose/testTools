from tkinter import *
from tkinter import messagebox
from app.stytles.tk_stytles import STYTLE
class Health(Frame):
    '''健康测量'''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.frame = Frame(self, **STYTLE["frame"])
        self.weightX = StringVar()
        self.heightX = StringVar()
        self.frame.pack(fill=BOTH, expand=True)
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