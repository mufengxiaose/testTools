# -*- coding: utf-8 -*-
'''
@Time    : 2022/8/29 22:59
@Author  : Carl
@File    : demo.py
'''
from tkinter import *
from tkinter import ttk


class MenuBar(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.menu = Menu(self.master, tearoff=False)
        self.master.config(menu=self.menu)

        self.fileMenu()
        self.helpMenu()

    def fileMenu(self):
        file_menu = Menu(self.menu)
        file_menu.add_command(label='Item')
        self.menu.add_cascade(label='File', menu=file_menu)

    def helpMenu(self):
        help_menu = Menu(self.menu)
        help_menu.add_command(label='exit', command=self.exitProgram)
        self.menu.add_cascade(label='help', menu=help_menu)

    def exitProgram(self):
        exit()

class UrlDecodeEncode(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # self.master = master
        self.pack()

        self.frame = Frame(self)
        self.frame.pack()
        self.ui()
        self.ui1()


    def ui(self):
        label_frame = LabelFrame(self.frame, text='标签1')
        self.inputEntry = Entry(label_frame)
        self.outputEntry = Entry(label_frame)
        button = Button(label_frame, text='Decode')

        self.inputEntry.grid()
        self.outputEntry.grid()
        button.grid()
        label_frame.grid(row=0, column=0)

    def ui1(self):
        label_frame = LabelFrame(self.frame, text='标签2')
        self.inputEntry = Entry(label_frame)
        self.outputEntry = Entry(label_frame)
        button = Button(label_frame, text='Decode')

        self.inputEntry.grid()
        self.outputEntry.grid()
        button.grid()
        label_frame.grid(row=1, column=1)

class Phone(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # self.master = master
        self.pack
        self.frame = Frame(self)
        self.frame.pack()
        button = Button(self.frame, text='button')
        button.grid(row=0, column=0)

class tabNode(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        tab = ttk.Notebook(self.master, padding=(30, 10))
        tab.grid()
        tab.add(UrlDecodeEncode(tab), text='手机')
        tab.add(Phone(tab), text='手机1')
        # tab.add(UrlDecodeEncode(tab), text='手机2')
        # tab.add(UrlDecodeEncode(tab), text='手机3')

if __name__ == '__main__':
    root = Tk()
    root.title("demo")
    root.geometry('400x400')
    MenuBar(root)
    # UrlDecodeEncode(root)
    tabNode(root)
    root.mainloop()