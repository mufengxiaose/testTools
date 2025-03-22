import os
from PIL import Image as Img
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from app.stytles.tk_stytles import STYTLE
class ImageProcessing(Frame):
    '''
    图片处理功能
    '''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack
        self.frame = Frame(self, **STYTLE["frame"])
        self.frame.pack(fill=BOTH, expand=True)
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
        img = Img.open(img)
        output_dir = "images_2"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        new_file = img_name + '.jpg'
        try:
            img.save(os.path.join(output_dir, new_file), quality=factor)
        except IOError as e:
            print(f"图片保存失败{e}")

    def importImgFile(self):
        '''file'''
        img = askopenfilename(filetypes=[('png', '*.png'), ('jpg', '*.jpg'),
                                         ('jpeg', '*jpeg'), ('gif', '*.gif')])
        self.imgEntry.delete(0, END)
        self.imgEntry.insert(0, img)
        