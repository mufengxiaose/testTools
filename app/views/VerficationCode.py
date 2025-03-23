import time
import requests
import datetime
from tkinter.filedialog import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from urllib.parse import urlencode
from common.DcaseTransformation import *
from app.stytles.tk_stytles import STYTLE


class VerficationCode(Frame):
    '''验证码获取'''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # 调用pack方法将Frame放置到父窗口中
        self.pack()
        # 创建一个子Frame用于布局UI元素
        self.frame = Frame(self, **STYTLE["frame"])
        self.frame.pack(fill=BOTH, expand=True)
        # 调用ui方法进行UI布局
        self.ui()

    def ui(self):
        '''ui布局'''
        # 验证码查询
        # 定义可选择的appid选项
        option = ['KF微信', 'KF支付宝', 'KF乘客', 'KF司机'] 
        # 创建手机号标签
        phone_label = Label(self.frame, text='手机号', **STYTLE["label"])
        # 将手机号标签放置到网格布局中
        phone_label.grid(row=0, column=0, sticky=NSEW)
        # 创建手机号输入框
        self.phone_entry = Entry(self.frame, width=20)
        # 将手机号输入框放置到网格布局中
        self.phone_entry.grid(row=0, column=1)
        # 创建appid标签
        appid_label = Label(self.frame, text="appid，仅线上", **STYTLE["label"])
        # 将appid标签放置到网格布局中
        appid_label.grid(row=0, column=2, sticky=NSEW)
        # 创建下拉选择框，用于选择appid
        self.combo = ttk.Combobox(self.frame, values=option)
        # 未设置默认选中项，可根据需求取消注释设置默认值
        # self.combo.set(option[0])
        # 将下拉选择框放置到网格布局中
        self.combo.grid(row=0, column=3, sticky=NSEW)
        # 创建获取验证码按钮，并绑定点击事件处理函数
        self.button_get = Button(self.frame, text="获取",
                                 command=self.on_get_code_bt_click, **STYTLE["button"])
        # 将获取验证码按钮放置到网格布局中
        self.button_get.grid(row=0, column=4, sticky=NSEW)  

        # 验证码固定
        # 创建输入验证码标签
        self.fixed_verification_code_label = Label(self.frame, text="固定验证码输入", **STYTLE["label"])
        # 将输入验证码标签放置到网格布局中
        self.fixed_verification_code_label.grid(row=2, column=2, sticky=NSEW)
        # 创建输入验证码输入框
        self.fixed_verification_code_entry = Entry(self.frame, width=20, foreground="gray")
        self.fixed_verification_code_entry_txt = "非连续性6位数字"
        self.fixed_verification_code_entry.insert(1, self.fixed_verification_code_entry_txt)
        self.fixed_verification_code_entry.bind("<Button-1>", self.clear_verfication_code_text_default_text)
        self.fixed_verification_code_entry.bind("<FocusOut>", self.fixed_verification_code_entry_on_focus_out)
        # 将输入验证码输入框放置到网格布局中
        self.fixed_verification_code_entry.grid(row=2, column=3, sticky=NSEW)
        # 创建固定验证码按钮，并绑定点击事件处理函数
        self.fixed_verification_code_bt = Button(self.frame, text="固定",
                                                 command=self.on_fixed_verification_code_bt_click, **STYTLE["button"])
        # 将固定验证码按钮放置到网格布局中
        self.fixed_verification_code_bt.grid(row=2, column=4, sticky=NSEW)

        # 测试号延期
        # 创建测试号延期按钮，并绑定点击事件处理函数
        number_extension_bt = Button(self.frame, text="测试号延期", command=self.on_number_extension_bt_click, **STYTLE["button"])
        # 将测试号延期按钮放置到网格布局中
        number_extension_bt.grid(row=0, column=5)

        # cookies
        # 创建cookies标签
        cookies_label = Label(self.frame, text="cookies", **STYTLE["label"])
        # 将cookies标签放置到网格布局中
        cookies_label.grid(row=3, column=2)
        # 创建cookies文本输入框
        self.cookies_text = Text(self.frame, width=50, height=5)
        # 将cookies文本输入框放置到网格布局中
        self.cookies_text.grid(row=3, column=3)

        # 一键续期
        # 定义默认提示文本
        self.default_text = "多手机号逗号间隔"
        # 创建多测试号延期标签
        nums_label = Label(self.frame, text="输入要延期测试账号", **STYTLE["label"])
        # 将多测试号延期标签放置到网格布局中
        nums_label.grid(row=1, column=2)
        # 创建多测试号输入框，设置初始文本和颜色
        self.nums_text = Text(self.frame, width=50, height=5, foreground="gray")
        self.nums_text.insert(1.0, self.default_text)
        # 将多测试号输入框放置到网格布局中
        self.nums_text.grid(row=1, column=3)
        # 绑定鼠标点击事件，用于清除默认提示文本
        self.nums_text.bind("<Button-1>", self.clear_nums_text_default_text)
        self.nums_text.bind("<FocusOut>", self.nums_text_on_focus_out)
        # 创建一键续期按钮，并绑定点击事件处理函数
        nums_extension_bt = Button(self.frame, text="一键续期", command=self.nums_extension_bt_click, **STYTLE["button"])
        # 将一键续期按钮放置到网格布局中
        nums_extension_bt.grid(row=1, column=4)

        # case转换
        # 创建导入文件按钮，并绑定点击事件处理函数
        case_file_bt = Button(self.frame, text="导入文件", command=self.insert_file_path, **STYTLE["button"])
        # 将导入文件按钮放置到网格布局中
        case_file_bt.grid(row=4, column=2)
        # 创建文件路径输入框
        self.case_file_entry = Entry(self.frame)
        # 将文件路径输入框放置到网格布局中
        self.case_file_entry.grid(row=4, column=3, sticky=NSEW)
        # 创建生成按钮，并绑定点击事件处理函数
        case_conversion_bt = Button(self.frame, text="生成", command=self.case_conversion_bt_click, **STYTLE["button"])
        # 将生成按钮放置到网格布局中
        case_conversion_bt.grid(row=4, column=4)

    def get_phone_appid(self):
        '''获取验证码'''
        # 获取下拉选择框中选中的appid选项
        appid = self.combo.get()
        # 获取手机号输入框中的内容
        phone_num = self.phone_entry.get()
        # 根据选中的appid选项，将其转换为对应的数字id
        if appid == "KF微信":
            appid = 130003
        elif appid == "KF支付宝":
            appid = 130004
        elif appid == "KF乘客":
            appid = 130000
        elif appid == "KF司机":
            appid = 130001
        return appid, phone_num

    def get_curl_code(self, appid, phone_num):
        # 定义请求的URL
        url = 'http://10.85.172.18:8000/passport/user/v5/querySmsCode'
        # 要发送的数据
        data = {
            'q': '{"country_calling_code":"+86","appid":%s,"cell":"%s","operator":"passport-pre-autotest"}' % (appid, phone_num)
        }
        print(data)
        # 对数据进行 URL 编码
        encoded_data = urlencode(data)

        # 设置请求头，这里根据 curl 命令的行为推测，实际可能需要根据服务器要求调整
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            # 发送 POST 请求
            response = requests.post(url, data=encoded_data, headers=headers)
            # 检查响应状态码，如果不是200，抛出异常
            response.raise_for_status()
            # 将响应内容解析为JSON格式
            result = response.json()
            return result
        except requests.RequestException as e:
            print(f"请求发生异常: {e}")
            # 这里应该是None，原代码有误
            return None

    def on_get_code_bt_click(self):
        # 获取appid和手机号
        appid, phone_num = self.get_phone_appid()
        # 调用get_curl_code方法获取验证码结果
        result = self.get_curl_code(appid=appid, phone_num=phone_num)
        if result:
            # 获取结果中的错误信息
            error = result.get('error')
            # 获取结果中的验证码数据
            verication_code = result.get('data')
            if verication_code:
                # 如果有验证码数据，弹出消息框显示验证码
                messagebox.showinfo(message=f'{verication_code}')
            else:
                # 如果没有验证码数据，弹出消息框显示错误信息
                messagebox.showinfo(message=f'{error}')
        else:
            # 如果请求结果为空，弹出消息框提示请求出错
            messagebox.showinfo(message="请求出错")

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

    def get_fixed_verification_code_curl(self, testcell_type, phone):
        """
        发送创建测试单元的请求
        :return: 请求响应结果
        """
        # 获取过期时间戳
        expired_timestamp = self.generate_expired_timestamp()
        testcell_type = testcell_type
        # 定义请求的URL
        url = 'https://starmap.xiaojukeji.com/mp/console/v1/testcell/create'
        # 获取cookies文本输入框中的内容，并去除末尾的换行符
        cookies = str(self.cookies_text.get("1.0", END).rstrip())
        # print(cookies)
        # 设置请求头
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '%s' % cookies,
            'Origin': 'https://starmap.xiaojukeji.com',
            'Referer': 'https://starmap.xiaojukeji.com/workflow/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        }
        # 要发送的数据
        data = {
            '0': '0',
            'env': '1',
            'cluster': 'hne',
            'department': '出行技术',
            'testcell_type': '%s' % testcell_type,
            'other': '测试',
            'app_info': '{"country_calling_code":"+86","role":1,"expired_time":%s,"origin_id":"1","cell":["%s"],"static_code":"556677"}' % (
                expired_timestamp, phone)
        }
        # 对数据进行 URL 编码
        encoded_data = urlencode(data)

        try:
            # 发送 POST 请求
            response = requests.post(url, headers=headers, data=encoded_data)
            # 检查响应状态码，如果不是200，抛出异常
            response.raise_for_status()
            # 将响应内容解析为JSON格式
            return response.json()
        except requests.RequestException as e:
            # 如果请求出错，弹出消息框提示cookies可能过期
            messagebox.showinfo(message="cookies 可能过期")
            print(f"请求失败：{e}")

    def on_fixed_verification_code_bt_click(self):
        '''
        固定验证码
        '''
        # 获取手机号输入框中的内容
        phone_num = self.phone_entry.get()
        # 获取多测试号输入框中的手机号列表
        nums = self.get_nums_text_phone()
        for phone in nums:
            # 调用get_fixed_verification_code_curl方法发送请求
            result = self.get_fixed_verification_code_curl(testcell_type=5, phone=phone)
            print(result)
            # 每次请求间隔1秒
            time.sleep(1)
        if result:
            # 获取结果中的错误信息
            errmsg = result.get('errmsg')
            # 弹出消息框显示错误信息
            messagebox.showinfo(message=f'{errmsg}')
        else:
            # 如果请求结果为空，弹出消息框提示请求出错
            messagebox.showinfo(message="请求出错")

    def on_number_extension_bt_click(self):
        '''
        单个测试号延期
        testcell_type:3 延期
        '''
        # 获取手机号输入框中的内容
        phone = self.phone_entry.get()
        # 调用get_fixed_verification_code_curl方法发送请求
        result = self.get_fixed_verification_code_curl(testcell_type=3, phone=phone)
        if result:
            # 获取结果中的错误信息
            errmsg = result.get('errmsg')
            # 弹出消息框显示错误信息
            messagebox.showinfo(message=f'{errmsg}')
        else:
            # 如果请求结果为空，弹出消息框提示请求出错
            messagebox.showinfo(message="请求出错")

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
        nums = self.get_nums_text_phone()
        for phone in nums:
            print(phone)
            # 调用get_fixed_verification_code_curl方法发送请求
            self.get_fixed_verification_code_curl(testcell_type=3, phone=phone)
            # 每次请求间隔1秒
            time.sleep(1)
        # 所有请求完成后，弹出消息框提示完成
        messagebox.showinfo(message="完成")

    def get_file_path(self):
        '''打开file'''
        # 打开文件选择对话框，返回选择的文件路径
        return askopenfilename()

    def insert_file_path(self):
        '''entry插入路径'''
        # 清空文件路径输入框中的内容
        self.case_file_entry.delete(0, END)
        # 将选择的文件路径插入到文件路径输入框中
        self.case_file_entry.insert(0, self.get_file_path())

    def case_conversion_bt_click(self):
        # 转换按钮点击
        # 获取文件路径输入框中的内容
        file_path = self.case_file_entry.get()
        try:
            if len(file_path) < 2:
                # 如果文件路径长度小于2，记录错误日志
                logging.error("请提供 Dcase 测试用例 Excel 文件的路径作为命令行参数。")
            else:
                # 调用getDcaseData函数获取测试用例数据
                dcaseContent = getDcaseData(file_path)
                # 调用parseCase函数解析测试用例数据，再调用createOECase函数创建测试用例
                createOECase(parseCase(dcaseContent))
        except Exception as e:
            # 如果发生异常，记录错误日志
            logging.error(f"主程序运行时出错: {e}")

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