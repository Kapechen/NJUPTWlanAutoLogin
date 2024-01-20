# %% 引入所需的库
import requests
import socket
import random
import json
import re
import sys
import datetime
import subprocess
import platform


# %% 函数封装
def checkInternetConnection():
    """
    检测电脑是否成功接入互联网
    :return: true,false
    """
    host = "www.baidu.com"
    port = 80
    try:
        sock = socket.create_connection((host, port), timeout=5)
        return True
    except OSError:
        return False
    finally:
        sock.close()


def autoLogin(ipv4Addr, userAccount, userPassword):
    # 官方v=Math.floor(Math.random() * 10000 + 500)即500~10500;防止缓存
    random_v = random.sample(range(500, 10500), 1)
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Dnt": "1",
        "Referer": "https://p.njupt.edu.cn/",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }
    # get请求地址
    url = "https://p.njupt.edu.cn:802//eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C" + f"{userAccount}" + "%40cmcc&user_password=" + f"{userPassword}" + "&wlan_user_ip=" + f"{ipv4Addr}" + "&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&terminal_type=1&lang=zh-cn&v=" + f"{random_v}" + "&lang=zh"
    response = requests.get(url, headers=header)
    processed_text = "{" + re.findall(r"[{](.*?)[}]", response.text)[0] + "}"
    # 后端返回的响应文本信息
    response_json_text = json.loads(processed_text)
    if response_json_text['msg'] == "无法获取用户认证账号!":
        printLog("校园网用户名或密码错误!")
    elif response_json_text['msg'] == 'AC999':
        return None
    else:
        res_msg = response_json_text['msg']
        printLog(f"其余登录信息：{res_msg}")


def getCurrentTime():
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 提取年份、月份、日期、小时、分钟、秒数
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second
    time_str = f"{year}年{month}月{day}日{hour}时{minute}分{second}秒"
    return time_str


def printLog(msg):
    # 输出日志路径
    log_file_path = "./logs.txt"
    with open(log_file_path, 'a') as f:
        print("--------" + getCurrentTime() + "--------", file=f)
        print(msg, file=f)


def getIpv4Addresses():
    system_platform = platform.system()
    ipv4_addresses = []
    if system_platform == "Linux":
        try:
            result = subprocess.run(["ifconfig"], capture_output=True, text=True)
            ifconfig_output = result.stdout
            ipv4_matches = re.finditer(r'inet (\d+\.\d+\.\d+\.\d+)', ifconfig_output)
            for match in ipv4_matches:
                ipv4_addresses.append(match.group(1))
        except Exception as e:
            printLog(f"获取IPv4地址错误: {str(e)}")
    elif system_platform == "Windows":
        try:
            result = subprocess.run(["ipconfig"], capture_output=True, text=True)
            ipconfig_output = result.stdout
            ipv4_matches = re.finditer(r'IPv4 Address[^\d]+(\d+\.\d+\.\d+\.\d+)', ipconfig_output)
            for match in ipv4_matches:
                ipv4_addresses.append(match.group(1))
        except Exception as e:
            printLog(f"获取IPv4地址错误: {str(e)}")
    return ipv4_addresses


# %% 主函数
if __name__ == '__main__':
    # 获取本机ipv4地址(连接校园网未登录前由校园网关路由自动分配 一般是10.133.xxx)
    ipv4Addresses = getIpv4Addresses()
    needed_ipv4 = ipv4Addresses[len(ipv4Addresses) - 1]
    arguments = sys.argv[1:]
    connected_flag = checkInternetConnection()
    while not connected_flag:
        try:
            user_account = arguments[0]
            user_password = arguments[1]
            autoLogin(needed_ipv4, user_account, user_password)
            connected_flag = checkInternetConnection()
        except Exception as e:
            printLog(f"程序运行缺乏输入参数（用户名和密码）: {str(e)}")
