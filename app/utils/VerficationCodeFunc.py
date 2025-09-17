# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : VerficationCodeFunc.py
# Time       ：2025/6/25 15:06
# Author     ：Carl
# Description：
"""
import requests
import tkinter as TK
from io import StringIO
from urllib.parse import urlencode
from tkinter import messagebox


def get_curl_code(phone_num, timeout=3):
    # 定义请求的URL
    url = 'http://10.85.172.18:8000/passport/user/v5/querySmsCode'
    # 要发送的数据
    appids = ['130001', '130000', '130003', '130004']
    for appid in appids:
        data = {
            'q': '{"country_calling_code":"+86","appid":%s,"cell":"%s","operator":"passport-pre-autotest"}' % (
            appid, phone_num)
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
            response = requests.post(url, data=encoded_data, headers=headers, timeout=timeout)
            # 检查响应状态码，如果不是200，抛出异常
            response.raise_for_status()
            # 将响应内容解析为JSON格式
            result = response.json()
            return result
        except requests.Timeout:
            messagebox.showinfo(message="请内网操作")
            raise ValueError(f"请求超时，超时时间{timeout}s")
        except requests.RequestException as e:
            print(f"请求发生异常: {e}")
            # 这里应该是None，原代码有误
            return None
    
class TextRedirector(StringIO):
    """将输出重定向到 Text 组件的工具类"""
    def __init__(self, text_widget, tag="stdout"):
        super().__init__()
        self.text_widget = text_widget
        self.tag = tag

    def write(self, string):
        """重写 write 方法，将内容插入到 Text 组件"""
        # 在主线程中更新 UI
        self.text_widget.after(0, self._append_text, string)
        super().write(string)

    def _append_text(self, string):
        """将文本追加到 Text 组件并自动滚动到底部"""
        self.text_widget.insert(TK.END, string, self.tag)
        self.text_widget.see(TK.END)  # 自动滚动到底部