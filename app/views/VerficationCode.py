import time
import requests
import threading
import datetime
from pathlib import Path
from tkinter.filedialog import *
from tkinter import *
from tkinter import ttk
# from datetime import datetime
from app.utils.DcaseFormation import *
from app.stytles.tk_stytles import STYTLE
from app.utils.MsKF import mkdir_kf_pro_file, run_commands_in_dir, kf_branch_parent_file
from app.utils.StarmapCurl import curl_starmap_url_extension, curl_starmap_url_fixed
from app.utils.VerficationCodeFunc import get_curl_code

appids = ['130003', '130000', '130001', '130004']
class VerficationCode(Frame):
    '''验证码获取'''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # 调用pack方法将Frame放置到父窗口中
        self.pack()
        self.wedgit = Frame(self)
        self.wedgit.pack(fill=BOTH, expand=True)
        # 创建一个子Frame用于布局UI元素
        self.verfication_code_frame = Frame(self.wedgit, **STYTLE["verficationcode_frame"])
        self.verfication_code_frame.pack(fill=X, expand=False)
        self.log_output_frame = Frame(self.wedgit)
        self.log_output_frame.pack(fill=X, expand=False)
        # 调用ui方法进行UI布局
        self.ui()
        # dcase转换
        self.dcase_formation_ui()
        self.ms_kf_ui()
        self.log_output_ui()

    def ui(self):
        '''ui布局'''
        # 验证码查询
        # 创建手机号标签
        phone_label = Label(self.verfication_code_frame, text='手机号', **STYTLE["codeLable"])
        # 将手机号标签放置到网格布局中
        phone_label.grid(row=0, column=0, sticky=W)
        # 创建手机号输入框
        self.phone_entry = Entry(self.verfication_code_frame, width=38)
        # 将手机号输入框放置到网格布局中
        self.phone_entry.grid(row=0, column=1)
        # 创建获取验证码按钮，并绑定点击事件处理函数
        self.button_get = Button(self.verfication_code_frame, text="获取验证码",
                                 command=self.on_get_code_bt_click, **STYTLE["button"])
        # 将获取验证码按钮放置到网格布局中
        self.button_get.grid(row=0, column=2, sticky=NSEW)

        # 验证码固定
        # 创建输入验证码标签
        self.fixed_verification_code_label = Label(self.verfication_code_frame, text="固定验证码:", **STYTLE["codeLable"])
        # 将输入验证码标签放置到网格布局中
        self.fixed_verification_code_label.grid(row=3, column=0, sticky=W)
        # 创建输入验证码输入框
        self.fixed_verification_code_entry = Entry(self.verfication_code_frame, width=20, foreground="gray")
        self.fixed_verification_code_entry_txt = "非连续性6位数字"
        self.fixed_verification_code_entry.insert(1, self.fixed_verification_code_entry_txt)
        self.fixed_verification_code_entry.bind("<Button-1>", self.clear_verfication_code_text_default_text)
        self.fixed_verification_code_entry.bind("<FocusOut>", self.fixed_verification_code_entry_on_focus_out)
        # 将输入验证码输入框放置到网格布局中
        self.fixed_verification_code_entry.grid(row=3, column=1, sticky=NSEW)
        # 创建固定验证码按钮，并绑定点击事件处理函数
        self.fixed_verification_code_bt = Button(self.verfication_code_frame, text="固定验证码",
                                                 command=self.on_fixed_verification_code_bt_click_thread, **STYTLE["button"])
        # 将固定验证码按钮放置到网格布局中
        self.fixed_verification_code_bt.grid(row=1, column=1, sticky=W)

        # cookies
        # 创建cookies标签
        cookies_label = Label(self.verfication_code_frame, text="cookies", **STYTLE["codeLable"])
        # 将cookies标签放置到网格布局中
        cookies_label.grid(row=5, column=0, sticky=W)
        # 创建cookies文本输入框
        self.cookies_text = Text(self.verfication_code_frame, width=50, height=5)
        # 将cookies文本输入框放置到网格布局中
        self.cookies_text.grid(row=5, column=1)
        # 创建ticket标签
        ticket_label = Label(self.verfication_code_frame, text="ticket", **STYTLE['codeLable'])
        ticket_label.grid(row=4, column=0, sticky=W)
        # ticket文本输入框
        self.ticket_text = Text(self.verfication_code_frame, width=50, height=5)
        self.ticket_text.grid(row=4, column=1)

        # 一键续期
        # 定义默认提示文本
        self.default_text = "多手机号逗号间隔"
        # 创建多测试号延期标签
        nums_label = Label(self.verfication_code_frame, text="输入要延期测试账号", **STYTLE["codeLable"])
        # 将多测试号延期标签放置到网格布局中
        nums_label.grid(row=2, column=0, sticky=W)
        # 创建多测试号输入框，设置初始文本和颜色
        self.nums_text = Text(self.verfication_code_frame, width=50, height=5, foreground="gray")
        self.nums_text.insert(1.0, self.default_text)
        # 将多测试号输入框放置到网格布局中
        self.nums_text.grid(row=2, column=1)
        # 绑定鼠标点击事件，用于清除默认提示文本
        self.nums_text.bind("<Button-1>", self.clear_nums_text_default_text)
        self.nums_text.bind("<FocusOut>", self.nums_text_on_focus_out)
        # 创建一键续期按钮，并绑定点击事件处理函数
        nums_extension_bt = Button(self.verfication_code_frame, text="一键续期", command=self.nums_extension_bt_click_thread, **STYTLE["button"])
        # 将一键续期按钮放置到网格布局中
        nums_extension_bt.grid(row=1, column=0)


    def on_get_code_bt_click(self):
        # 获取appid和手机号
        self.log_action(message="获取验证码", level="info")
        # 获取手机号输入框中的内容
        phone_num = self.phone_entry.get()
        print(type(phone_num))
        # 调用get_curl_code方法获取验证码结果
        for appid in appids:
            self.log_action(message=f"开始处理appid: {appid}")
            result = get_curl_code(appid=appid, phone_num=phone_num)
            if not result:
                # 接口无返回结果的情况
                self.log_action(message=f"appid: {appid} 调用接口无返回")
                messagebox.showinfo(message=f"appid: {appid} 接口请求失败")
                continue  # 继续处理下一个appid
                # 获取结果中的错误信息
            error_info = result.get('error')
            # 获取结果中的验证码数据
            verification_code = result.get('data')
            if verification_code:
                if verification_code == "验证码过期":
                    self.log_action(message=f"appid: {appid} 验证码：{verification_code}")
                    messagebox.showinfo(message=f'appid: {appid} {verification_code}')
                    continue  # 继续尝试下一个appid
                else:
                    # 获取到有效验证码，返回结果
                    self.log_action(message=f"appid: {appid} 成功获取验证码: {verification_code}")
                    return verification_code  # 可考虑返回验证码供后续使用
            else:
                # 无验证码数据，显示错误信息
                error_msg = error_info or f"appid: {appid} 未获取到验证码"
                self.log_action(message=error_msg)
                # 这里使用continue还是return取决于业务逻辑：
                # continue：继续尝试其他appid
                # return：遇到错误就终止
                continue


    def generate_expired_timestamp(self):
        """
        生成未来指定小时数后的时间戳
        :param hours: 未来的小时数，默认为 1
        :return: 时间戳
        """
        # 获取当前时间
        now = datetime.datetime.now()
        # 计算45天后的时间
        expired_time = now + datetime.timedelta(days=45)
        # 将时间转换为时间戳
        return int(expired_time.timestamp())

    def on_fixed_verification_code_bt_click(self):
        '''
        固定验证码
        '''
        # # 获取手机号输入框中的内容
        # phone_num = self.phone_entry.get()
        # 获取多测试号输入框中的手机号列表
        nums = self.get_nums_text_phone() or self.phone_entry.get()
        ticket = self.ticket_text.get("1.0", END)
        cookies_dict = self.parse_cookies()
        code = self.fixed_verification_code_entry.get()
        for num in nums:
            # 调用curl_starmap_url_fixed方法发送请求
            result = curl_starmap_url_fixed(ticket=ticket, cookies=cookies_dict, code=code, numbers=num)
            print(result)
            self.log_action(message=f"{result}", level='info')
            # 每次请求间隔1秒
            time.sleep(1)
    def parse_cookies(self, cookies_str=NONE):
        """
        将 Cookies 字符串解析为字典，支持异常输入校验和特殊情况处理
        
        参数:
            cookies_str: 原始 Cookies 字符串，格式如 "key1=value1; key2=value2=xyz"
        
        返回:
            dict: 解析后的 Cookies 字典
        
        异常:
            TypeError: 当输入不是字符串类型时抛出
            ValueError: 当输入为空字符串或格式严重错误时抛出
        """
        cookies_str = self.cookies_text.get("1.0", END)
        print("cookies", cookies_str)
        clear_cookies = cookies_str.replace("\n", "").replace("\r", "")
        print("clear_cookies", clear_cookies)
        # cookies_dict = {item.split('=')[0]: item.split('=')[1] for item in clear_cookies.split('; ')}
        # print("cookies_dict", cookies_dict)
        # 1. 校验输入类型
        if not isinstance(cookies_str, str):
            raise TypeError(f"预期输入为字符串，实际收到 {type(cookies_str).__name__} 类型")
        
        # 2. 校验输入内容是否为空
        stripped_cookies = cookies_str.strip()
        if not stripped_cookies:
            raise ValueError("输入的Cookies字符串为空或仅包含空白字符")
        
        cookies_dict = {}
        # 按 '; ' 分割，过滤空字符串
        items = [item.strip() for item in stripped_cookies.split('; ') if item.strip()]
        
        # 3. 校验是否有有效项
        if not items:
            raise ValueError("Cookies字符串格式错误，未找到有效键值对")
        
        for index, item in enumerate(items, 1):
            try:
                if '=' in item:
                    # 只按第一个 '=' 分割，处理值中包含 '=' 的情况
                    key, value = item.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # 校验键是否为空
                    if not key:
                        raise ValueError(f"第{index}项键名为空（格式：{item}）")
                    
                    cookies_dict[key] = value
                else:
                    # 处理没有 '=' 的项（视为键名，值为空）
                    key = item.strip()
                    if not key:
                        raise ValueError(f"第{index}项为无效空值（格式：{item}）")
                    cookies_dict[key] = ""
                    
            except Exception as e:
                # 包装异常信息，方便定位问题
                raise ValueError(f"解析第{index}项时出错：{str(e)}") from e
        
        return cookies_dict

    def on_fixed_verification_code_bt_click_thread(self):
        """固定验证码线程"""
        self.thread_func(target=self.on_fixed_verification_code_bt_click)

    def clear_nums_text_default_text(self, event):
        # 获取多测试号输入框中的内容，并去除首尾空格
        current_text = self.nums_text.get("1.0", END).strip()
        # 判断内容是否为默认文案
        if current_text == self.default_text:
            # 清除默认文案
            self.nums_text.delete("1.0", END)
            # 设置文本颜色为黑色
            self.nums_text.config(fg="black")

    def get_nums_text_phone(self):
        # 获取多测试号输入框中的内容，去除末尾换行符，并按逗号分割成列表
        return self.nums_text.get(1.0, END).rstrip().split(',')

    def nums_extension_bt_click(self):
        '''多测试号延期'''
        # 获取多测试号输入框中的手机号列表
        nums = self.get_nums_text_phone() or self.phone_entry.get()
        ticket = str(self.ticket_text.get("1.0", END).rstrip())
        cookies = str(self.cookies_text.get("1.0", END).rstrip())
        for num in nums:
            print(num)
            print(type(num))
            # 调用curl_starmap_url_extension方法发送请求
            resp, errno, text = curl_starmap_url_extension(ticket=ticket, cookies=cookies, numbers=num)
            # 每次请求间隔1秒
            time.sleep(1)
            self.log_action(f"{resp}{errno}{text}")


    def nums_extension_bt_click_thread(self):
        '''多测试号延期线程'''
        self.thread_func(target=self.nums_extension_bt_click)

    def get_file_path(self):
        '''打开file'''
        # 打开文件选择对话框，返回选择的文件路径
        return askopenfilename()

    def clear_verfication_code_text_default_text(self, event):
        # 获取多测试号输入框中的内容，并去除首尾空格
        current_text = self.fixed_verification_code_entry.get().strip()
        # 判断内容是否为默认文案
        if current_text == self.fixed_verification_code_entry_txt:
            # 清除默认文案
            self.fixed_verification_code_entry.delete(0, END)
            # 设置文本颜色为黑色
            self.fixed_verification_code_entry.config(fg="black")
    
    def fixed_verification_code_entry_on_focus_out(self, event):
        """当 Entry 失去焦点时，恢复原文案"""
        if self.fixed_verification_code_entry.get() == "":
            self.fixed_verification_code_entry.insert(0, self.fixed_verification_code_entry_txt)  # 恢复原文案
            self.fixed_verification_code_entry.config(fg="gray")  # 设置文字颜色为灰色
    
    def nums_text_on_focus_out(self, event):
        """当 Entry 失去焦点时，恢复原文案"""
        if self.nums_text.get("1.0", END).strip() == "":
            self.nums_text.insert("1.0", self.default_text)  # 恢复原文案
            self.nums_text.config(fg="gray")  # 设置文字颜色为灰色

    def dcase_formation_ui(self):
        separator = ttk.Separator(self.verfication_code_frame, style="BlackSeparator.TSeparator")
        separator.grid(row=6, column=0, sticky="ew", pady=10, columnspan=8)
        # 创建选择文件按钮，点击时调用 select_file 函数
        select_button = Button(self.verfication_code_frame, text="选择 Dcase 测试用例文件", command=select_file, **STYTLE['button'])
        select_button.grid(row=7, column=0)

    def ms_kf_ui(self):
        # 分割线
        separator = ttk.Separator(self.verfication_code_frame, style="BlackSeparator.TSeparator")
        separator.grid(row=8, column=0, sticky="ew", pady=10, columnspan=8)
        #创建label、entey、button
        kf_branch_label = Label(self.verfication_code_frame, text="分支名称", **STYTLE["label"])
        kf_branch_label.grid(row=9, column=0)
        self.kf_branch_input_entry = Entry(self.verfication_code_frame, width=38)
        self.kf_branch_input_entry.grid(row=9, column=1)
        kf_branch_bt = Button(self.verfication_code_frame, text="点击开始", command=self.ms_kf_thread,
                              **STYTLE['button'])
        kf_branch_bt.grid(row=9, column=2)

    def ms_kf_branch_func(self):
        branch = self.kf_branch_input_entry.get()
        kf_branch_parent_file()
        mkdir_kf_pro_file(branch=branch)
        target_dir = Path.home() / "code" / branch
        commands_to_run = [
            ["echo", "开始执行命令"],
            ["ms", "_kf", "%s" % (branch)],
        ]
        success, stderr, stdout = run_commands_in_dir(target_dir, commands_to_run)
        self.log_action(message=f"{stderr}{stdout}\n执行完成", level='info')


    def thread_func(self, target=None):
        thread_ = threading.Thread(target=target)
        thread_.start()
        if thread_.is_alive():
            print("线程开始")
        else:
            print("线程结束")

    def ms_kf_thread(self):
        self.log_action(message="开始拉取分支", level='info')
        self.thread_func(target=self.ms_kf_branch_func)

    def log_output_ui(self):
        log_output_label = Label(self.log_output_frame, text="日志输出")
        log_output_label.pack()
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.log_output_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 日志文本框
        self.log_text = tk.Text(
            self.log_output_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            bg="#f0f0f0",
            font=("Consolas", 10)
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)

        # 配置文本标签（用于区分不同类型的日志）
        self.log_text.tag_configure("stdout", foreground="black")
        self.log_text.tag_configure("stderr", foreground="red")
        self.log_text.tag_configure("info", foreground="blue")
        self.log_text.tag_configure("warning", foreground="#FFA500")
        self.log_text.tag_configure("error", foreground="red", font=("Consolas", 10, "bold"))

    def log_action(self, message, level='info'):
        """记录操作日志到文本框"""
        # 获取当前时间
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 格式化日志内容
        log_entry = f"[{timestamp}] {message}\n"
        
        # 启用文本框编辑，插入日志，然后禁用编辑
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] ", "time")
        self.log_text.insert(tk.END, f"{message}\n", level)
        self.log_text.config(state=tk.DISABLED)
        
        # 自动滚动到底部
        self.log_text.see(tk.END)