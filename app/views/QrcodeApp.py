import qrcode
import os
from tkinter import *
from PIL import Image, ImageTk
from app.utils.common import CommonFunc
from app.stytles.tk_stytles import STYTLE

class QrcodeApp(Frame):
    '''二维码生成'''
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        # 设置frame
        self.qrcodeFrame = Frame(self)
        self.qrcodeFrame.pack(fill=BOTH, expand=True)
        # 输入文字
        self.input_text = Text(self.qrcodeFrame, height=6, width=100)
        self.input_text.grid(row=0, column=0, sticky=NSEW)
        # 生成二维码按钮
        self.button = Button(self.qrcodeFrame, text="生成二维码", command=self.showQrcodeImg)
        self.button.grid(row=0, column=1, sticky=NSEW)
        self.qc_label = None

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
        img_path = os.path.join(os.getcwd(), "qrcodeImg", "img.png")
        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            print(f"错误：未找到二维码图片 {img_path}")
            return
        resize_img = self.resize_keep_ratio(img=img)
        self.photo = ImageTk.PhotoImage(resize_img)
        if self.qc_label:
            self.qc_label.destroy()
        self.qc_label = Label(self.qrcodeFrame, image=self.photo)
        self.qc_label.grid(row=2)

    def resize_keep_ratio(self, img, target_size=(500, 500), resample=Image.Resampling.LANCZOS):
        """
        等比例缩放图像到目标尺寸，保持宽高比
        :param img: Pillow 图像对象
        :param target_size: 目标尺寸 (width, height)
        :param resample: 重采样算法
        :return: 缩放后的图像
        """
        if hasattr(Image, 'Resampling'):
            resample = Image.Resampling.LANCZOS
        else:
            resample = Image.LANCZOS
        
        # 获取原图宽高
        img_width, img_height = img.size
        target_width, target_height = target_size
        
        # 计算缩放比例（取最小比例，保证图像完全在目标尺寸内）
        scale = min(target_width / img_width, target_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # 等比例缩放
        resized = img.resize((new_width, new_height), resample)
        
        # 创建空白画布（600x600，白色背景）
        final_img = Image.new("RGB", target_size, (255, 255, 255))
        # 将缩放后的图像居中粘贴
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        final_img.paste(resized, (paste_x, paste_y))
        
        return final_img