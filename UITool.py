# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : UITool.py
# Time       ：2024/4/29 20:23
# Author     ：Carl
# Description：
"""
from tkinter import (Tk, Frame, Menu)

'''菜单栏'''
class MenuBar(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.fileMenu()
        self.helpMenu()

    def fileMenu(self):
        file_menu = Menu(self.menu)
        file_menu.add_command(label='File')
        file_menu.add_command(label='save')
        file_menu.add_command(label='exit', command=self.exitPro)
        self.menu.add_cascade(label='File', menu=file_menu)

    def helpMenu(self):
        editMenu = Menu(self.menu)
        editMenu.add_command(label="Exit")
        # editMenu.add_command(label="Redo")
        self.menu.add_cascade(label="help", menu=editMenu)

    def exitPro(self):
        exit()



if __name__ == '__main__':
    window = Tk()
    window.title('test')
    window.geometry('800x600')
    MenuBar(window)
    # MenuBar()
    window.mainloop()