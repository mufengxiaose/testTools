import requests
import urllib.parse
from tkinter import messagebox

def curl_starmap_url_extension(ticket, numbers, cookies):
    '''测试号延期'''
    url = "https://mp-platfrom.intra.xiaojukeji.com/platform/tool/cellPostpone" + "?" + "ticket=" + ticket + "&" + "app_id=2690"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "env": "DEV",
        "origin": "https://mp-platfrom.intra.xiaojukeji.com",
        "priority": "u=1, i",
        "referer": "https://mp-platfrom.intra.xiaojukeji.com/mp_tool_big/",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Cookie": "%s"%(cookies)
        }

    data = {
        "resource": "专快司机",
        "resourceDriver": "",
        "type": "账号延期",
        "delivery": "true",
        "engineRoom": "线上花小猪环境",
        "engineRoomList": "",
        "envRoom": "单机房",
        "country_calling_code": "+86",
        "number": "1",
        "CreateType": "乘客",
        "relnameType": "无实名",
        "expreBool": "false",
        "id_type": "1",
        "role": "1",
        "open19": "2",
        "env": "线上花小猪环境",
        "cell": "%s"%(numbers),
        "remark": "测试使用",
        "isNew": "false"
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    print(response.text)
    return response, response.status_code, response.text

def curl_starmap_url_fixed(ticket, numbers, cookies, code):
    '''固定验证码'''
    url = "https://mp-platfrom.intra.xiaojukeji.com/platform/adminTool/apply" + "?" + "ticket" + "=" + "%s"%(ticket) + "&app_id=2690"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "env": "DEV",
        "origin": "https://mp-platfrom.intra.xiaojukeji.com",
        "priority": "u=1, i",
        "referer": "https://mp-platfrom.intra.xiaojukeji.com/mp_tool_big/",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    cookies = cookies

    data = {
        "resource": "专快司机",
        "resourceDriver": "",
        "type": "固定验证码",
        "delivery": "true",
        "engineRoom": "线上花小猪环境",
        "engineRoomList": "",
        "envRoom": "单机房",
        "country_calling_code": "+86",
        "number": "1",
        "CreateType": "乘客",
        "relnameType": "无实名",
        "expreBool": "false",
        "id_type": "1",
        "role": "1",
        "open19": "2",
        "env": "线上花小猪环境",
        "cell": "%s"%(numbers),
        "remark": "测试使用",
        "isNew": "false",
        "code": "%s"%(code),
        "expreBoolWithMp": "true",
        "username": ""
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    print("Status Code:", response.status_code)
    print("Response:", response.text)
    return response

def curl_starmap_url_buriedPoint(ticket, orderIds, cookies):
    '''退款发起'''
    base_url = "https://mp-platfrom.intra.xiaojukeji.com/platform/tool/buriedPoint"
    ticket = ticket
    orderIds = orderIds
    cookies = parse_cookies(cookies_str=cookies)
    url = base_url + "?" + "ticket=" + ticket + "&" + "app_id=2690"
    params = {
        "ticket": ticket,
        "app_id": "2690"
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        # "content-type": "application/x-www-form-urlencoded",
        "content-type": "application/json",
        "origin": "https://mp-platfrom.intra.xiaojukeji.com",
        "priority": "u=1, i",
        "referer": "https://mp-platfrom.intra.xiaojukeji.com/",
        "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Cookies": "%s"%(cookies)
    }
    params_ = {
        "orderIds":orderIds,
        "orderType": "0",
        "trafficType": "0"
    }
    body_parmas = urllib.parse.urlencode(params_)
    print(f"body_parmas:{body_parmas}")
    data = {
        "url": "/platform/tools/pay/cashier/refund",
        "method": "post",
        "name": "刘晓",
        "email": "cliuxiao_v",
        "ticket": ticket,
        "app_id": "2690",  # 保持字符串格式（与curl一致，若后端允许也可传整数2690）
        "body_params": body_parmas # 关键：保留外层双引号
    }

    response = requests.post(
        url=url,
        params=params,
        headers=headers,
        cookies=cookies,
        # data=data
        json=data
    )
    print(response.status_code)
    print(response.text)


def curl_starmap_url_refund(ticket, cookies, orderIds, env):
    '''退款进度查询'''
    pass

def parse_cookies(cookies_str=None):
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
    # cookies_str = self.cookies_text.get("1.0", END)
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

if __name__ == "__main__":
    ticket = "1d94a03f35c42a9105375c5688b914f30002690000"
    cookies = "ENG_prod_SESSION_ID=2341de8a88027d224523fa3f3d13ff02000915000; CASE_SSO_USERNAME=cliuxiao_v; username=cliuxiao_v; dj_star_ticket=ec02b37bfb5863365810a69e92d11d7e0001652000; sidebarStatus=0; language=zh_CN; mp_platform_token=cc6ad5cc282aa6ca41a71f5dad9192520002102263000"
    order_id = "500_202510313410482801000605"
    curl_starmap_url_buriedPoint(ticket=ticket, cookies=cookies,
                                 orderIds=order_id, )