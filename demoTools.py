# -*- coding: utf-8 -*-
'''
@Time    : 2023/12/14 20:28
@Author  : Carl
@File    : demoTools.py
'''

from tkinter import *
from tkinter.ttk import *

class MenuBar(Frame):
    '''菜单栏'''
    def __init__(self, master=None):
        # super().__init__(master)
        # self.pack()
        Frame.__init__(self, master)
        self.master = master

        self.menu = Menu(self.master, tearoff=False)
        self.master.config(menu=self.menu)

        self.fileMenu()
        self.helpMenu()

    def fileMenu(self):
        file_menu = Menu(self.menu)
        file_menu.add_command(label='Item')
        # file_menu.add_command(label='Exit',)
        self.menu.add_cascade(label="File", menu=file_menu)

    def helpMenu(self):
        editMenu = Menu(self.menu)
        editMenu.add_command(label='Exit', command=self.exitPrograme)
        self.menu.add_cascade(label="Help", menu=editMenu)

    def exitPrograme(self):
        exit()

if __name__ == '__main__':
    root = Tk()
    root.title('Demo')
    root.geometry("1200x600")
    MenuBar(root)
    root.mainloop()