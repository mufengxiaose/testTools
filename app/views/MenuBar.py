from tkinter import *

class MenuBar(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.menubar = Menu(self.master, tearoff=False)
        self.master.config(menu=self.menubar)

    def fileMenu(self):
        file_menu = Menu(self.menubar, tearoff=False)
        file_menu.add_command(label='file')
        self.menubar.add_cascade(lable='File', menu=file_menu)