import qrcode
import os
from tkinter import *
from PIL import Image, ImageTk
from common.common import CommonFunc

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