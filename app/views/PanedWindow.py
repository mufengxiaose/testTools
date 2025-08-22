from tkinter import *


class CustomeFrame(Frame):
    """
    自定义的 Frame 类，继承自 tkinter.Frame
    """
    def __init__(self, master = None):
        """
        初始化方法
        :param master: 父窗口或容器
        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        """
        创建布局
        """
        self.devices_frame = Frame(self, bg="lightgreen")
        self.devices_frame.pack()

        self.time_stamp_frame = Frame(self, bg="lightyellow")
        self.time_stamp_frame.pack()


if __name__ == "__main__":
    root = Tk()
    app = CustomeFrame(master=root)
    root.mainloop()