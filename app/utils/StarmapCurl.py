import requests
from tkinter import messagebox

def curl_starmap_url_extension(ticket, numbers, cookies):

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
    return response

def curl_starmap_url_fixed(ticket, numbers, cookies, code):
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

if __name__ == "__main__":
    ticket = "223462f9e70685b979a9f98a5fa88a290002690000"
    cookies = "CASE_SSO_USERNAME=cliuxiao_v; username=cliuxiao_v; dj_star_ticket=f99616eb511ce5f45e2b5158acded6860001652000; app_id=2690; ENG_prod_SESSION_ID=a787a9fbb7055c9d98d503202fd0351f000915000; ticket=223462f9e70685b979a9f98a5fa88a290002690000"
    cookies_dict = {item.split('=')[0]: item.split('=')[1] for item in cookies.split('; ')}
    # print(cookies_dict)
    numbers = "11000052322"
    print(cookies_dict)
    curl_starmap_url_extension(ticket, numbers, cookies)
    curl_starmap_url_fixed(ticket, numbers, cookies=cookies_dict, code="556677")