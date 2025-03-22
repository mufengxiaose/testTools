import tkinter as tk


class CustomFrame(tk.Frame):
    """
    自定义的 Frame 类，继承自 tkinter.Frame
    """
    def __init__(self, master=None):
        """
        初始化方法
        :param master: 父窗口或容器
        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.paned_window()

    def create_widgets(self):
        """
        创建并布局子组件
        """
        self.label = tk.Label(self, text="这是一个自定义的 Frame")
        self.label.pack()

        self.button = tk.Button(self, text="点击我", command=self.on_button_click)
        self.button.pack()

    def on_button_click(self):
        """
        按钮点击事件处理方法
        """
        print("按钮被点击了！")
    
    def paned_window(self):
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=1)
        # 创建两个 Frame 并添加到 PanedWindow 中
        frame1 = tk.Frame(paned, bg="lightgreen")
        paned.add(frame1)

        frame2 = tk.Frame(paned, bg="lightyellow")
        paned.add(frame2)

        # 在 Frame 中添加标签
        self.label1 = tk.Label(frame1, text="左边的 Frame")
        self.label1.pack(pady=20)

        label2 = tk.Label(frame2, text="右边的 Frame")
        label2.pack(pady=20)


        # 添加一个按钮用于切换数据
        button = tk.Button(frame1, text="切换数据", command=self.switch_data)
        button.pack(pady=10)

        # 定义切换数据的函数
    def switch_data(self):
        # 定义数据列表
        data_list = ["数据 1", "数据 2", "数据 3"]
        current_index = 0
        # global current_index
        current_index = (current_index + 1) % len(data_list)
        self.label1.config(text=data_list[current_index])



if __name__ == "__main__":
    root = tk.Tk()
    app = CustomFrame(master=root)
    root.mainloop()