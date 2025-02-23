import time
import requests
import datetime
from tkinter.filedialog import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from urllib.parse import urlencode

from common.DcaseTransformation import *


class VerficationCode(Frame):
    '''验证码获取'''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack
        self.frame = Frame(self)
        self.frame.pack()
        self.ui()

    def ui(self):
        '''ui布局'''
        # 验证码查询
        option = ['KF微信', 'KF支付宝', 'KF乘客', 'KF司机'] 
        phone_label = Label(self.frame, text='手机号')
        phone_label.grid(row=0, column=0, sticky=NSEW)
        self.phone_entry = Entry(self.frame, width=20)
        self.phone_entry.grid(row=0, column=1)
        appid_label = Label(self.frame, text="appid")
        appid_label.grid(row=0, column=2, sticky=NSEW)
        self.combo = ttk.Combobox(self.frame, values=option)
        # self.combo.set(option[0])
        self.combo.grid(row=0, column=3, sticky=NSEW)
        self.button_get = Button(self.frame, text="获取", command=self.on_get_code_bt_click)
        self.button_get.grid(row=0, column=4, sticky=NSEW)  
        # 验证码固定
        self.fixed_verification_code_label = Label(self.frame, text="输入验证码")
        self.fixed_verification_code_label.grid(row=1, column=2, sticky=NSEW)
        self.fixed_verification_code_entry = Entry(self.frame, width=20)
        self.fixed_verification_code_entry.grid(row=1, column=3, sticky=NSEW)
        self.fixed_verification_code_bt = Button(self.frame, text="固定", command=self.on_fixed_verification_code_bt_click)
        self.fixed_verification_code_bt.grid(row=1, column=4, sticky=NSEW)
        # 测试号延期
        number_extension_bt = Button(self.frame, text="测试号延期", command=self.on_number_extension_bt_click)
        number_extension_bt.grid(row=0, column=5)

        # cookies
        cookies_label = Label(self.frame, text="cookies")
        cookies_label.grid(row=3, column=2)
        self.cookies_text = Text(self.frame, width=50, height=5)
        self.cookies_text.grid(row=3, column=3)

        # 一键续期
        self.default_text = "多手机号逗号间隔"
        nums_label = Label(self.frame, text="多测试号延期")
        nums_label.grid(row=2, column=2)
        self.nums_text = Text(self.frame, width=50, height=5, foreground="gray")
        self.nums_text.insert(1.0, self.default_text)
        self.nums_text.grid(row=2, column=3)
        self.nums_text.bind("<Button-1>", self.clear_nums_text_default_text)
        nums_extension_bt = Button(self.frame, text="一键续期", command=self.nums_extension_bt_click)
        nums_extension_bt.grid(row=2, column=4)

        # case转换
        case_file_bt = Button(self.frame, text="导入文件", command=self.insert_file_path)
        case_file_bt.grid(row=4, column=2)
        self.case_file_entry = Entry(self.frame)
        self.case_file_entry.grid(row=4, column=3, sticky=NSEW)
        case_conversion_bt = Button(self.frame, text="生成", command=self.case_conversion_bt_click)
        case_conversion_bt.grid(row=4, column=4)

    def get_phone_appid(self):
        '''获取验证码'''
        appid = self.combo.get()
        phone_num = self.phone_entry.get()
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
        url = 'http://10.85.172.18:8000/passport/user/v5/querySmsCode'
        # appid, phone_num = self.get_phone_appid()
        # 要发送的数据
        data = {
            'q': '{"country_calling_code":"+86","appid":%s,"cell":"%s","operator":"passport-pre-autotest"}'%(appid, phone_num)
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
            response.raise_for_status()
            result = response.json()
            return result
        except requests.RequestException as e:
            print(f"请求发生异常: {e}")
            return NONE        
 
    def on_get_code_bt_click(self):
        appid, phone_num = self.get_phone_appid()
        result = self.get_curl_code(appid=appid, phone_num=phone_num)
        if result:
            error = result.get('error')
            verication_code = result.get('data')
            if verication_code:
                messagebox.showinfo(message=f'{verication_code}')
            else:
                messagebox.showinfo(message=f'{error}')
        else:
            messagebox.showinfo(message="请求出错")

    def generate_expired_timestamp(self):
        """
        生成未来指定小时数后的时间戳
        :param hours: 未来的小时数，默认为 1
        :return: 时间戳
        """
        now = datetime.datetime.now()
        expired_time = now + datetime.timedelta(days=45)
        return int(expired_time.timestamp())
    
    def get_fixed_verification_code_curl(self, testcell_type, phone):
        """
        发送创建测试单元的请求
        :return: 请求响应结果
        """
        # phone_num = self.phone_entry.get()
        expired_timestamp = self.generate_expired_timestamp()
        testcell_type = testcell_type
        url = 'https://starmap.xiaojukeji.com/mp/console/v1/testcell/create'
        cookies = str(self.cookies_text.get("1.0", END).rstrip())
        # print(cookies)
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '%s'%cookies,
            'Origin': 'https://starmap.xiaojukeji.com',
            'Referer': 'https://starmap.xiaojukeji.com/workflow/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site':'same-origin',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        }
        data = {
            '0': '0',
            'env': '1',
            'cluster': 'hne',
            'department': '出行技术',
            'testcell_type': '%s'%testcell_type,
            'other': '测试',
            'app_info': '{"country_calling_code":"+86","role":1,"expired_time":%s,"origin_id":"1","cell":["%s"],"static_code":"556677"}'%(expired_timestamp, phone)
        }
        encoded_data = urlencode(data)

        try:
            response = requests.post(url, headers=headers, data=encoded_data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return response.json()
            
    def on_fixed_verification_code_bt_click(self):
        '''
        固定验证码
        '''
        phone_num = self.phone_entry.get()
        result = self.get_fixed_verification_code_curl(testcell_type=5, phone=phone_num)
        print(result)
        if result:
            errmsg = result.get('errmsg')
            messagebox.showinfo(message=f'{errmsg}')
        else:
            messagebox.showinfo(message="请求出错")

    def on_number_extension_bt_click(self):
        '''
        单个测试号延期
        testcell_type:3 延期
        '''
        phone = self.phone_entry.get()
        result = self.get_fixed_verification_code_curl(testcell_type=3, phone=phone)
        if result:
            errmsg = result.get('errmsg')
            messagebox.showinfo(message=f'{errmsg}')
        else:
            messagebox.showinfo(message="请求出错")
    
    def clear_nums_text_default_text(self, event):
        current_text = self.nums_text.get("1.0", END).strip()
        # 判断内容是否为默认文案
        if current_text == self.default_text:
            # 清除默认文案
            self.nums_text.delete("1.0", END)
            self.nums_text.config(fg="black")

    def get_nums_text_phone(self):
        # 获取手机号，转列表
        return self.nums_text.get(1.0, END).rstrip().split(',')
    
    def nums_extension_bt_click(self):
        '''多测试号延期'''
        nums = self.get_nums_text_phone()
        for phone in nums:
            print(phone)
            self.get_fixed_verification_code_curl(testcell_type=3, phone=phone)
            time.sleep(1)
        #     if result:
        #         errmsg = result.get('errmsg')
        #         messagebox.showinfo(message=f'{errmsg}')
        # else:
        #     messagebox.showinfo(message="请求出错")
        messagebox.showinfo(message="完成")
    
    def get_file_path(self):
        '''打开file'''
        return askopenfilename()

    def insert_file_path(self):
        '''entry插入路径'''
        self.case_file_entry.delete(0, END)
        self.case_file_entry.insert(0, self.get_file_path())
    
    def case_conversion_bt_click(self):
        # 转换按钮点击
        file_path = self.case_file_entry.get()
        try:
            if len(file_path) < 2:
                logging.error("请提供 Dcase 测试用例 Excel 文件的路径作为命令行参数。")
            else:
                dcaseContent = getDcaseData(file_path)
                createOECase(parseCase(dcaseContent))
        except Exception as e:
            logging.error(f"主程序运行时出错: {e}")

