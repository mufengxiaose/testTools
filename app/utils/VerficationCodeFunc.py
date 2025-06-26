# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : VerficationCodeFunc.py
# Time       ：2025/6/25 15:06
# Author     ：Carl
# Description：
"""
import requests
from urllib.parse import urlencode
from tkinter import messagebox

def get_curl_code(appid, phone_num, timeout=3):
    # 定义请求的URL
    url = 'http://10.85.172.18:8000/passport/user/v5/querySmsCode'
    # 要发送的数据
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