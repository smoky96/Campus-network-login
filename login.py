import os
import time

import requests
import platform
import msvcrt
import sys

from logger import setup_custom_log

logger, _ = setup_custom_log("", "connect")


def param_init(username, password):
    post_addr = "http://172.16.200.13/"
    post_header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Content-Length": "40",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "myusername=2018170896",
        "DNT": "1",
        "Host": "172.16.200.13",
        "Referer": "http://172.16.200.13/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}
    post_data = {
        "DDDDD": username,
        "upass": password,
        "0MKKey": "123"
    }
    return post_addr, post_header, post_data


def pwd_input(info):
    sys.stdout.write(info)
    sys.stdout.flush()
    star_cnt = 0
    chars = []
    while True:
        new_char = msvcrt.getch()
        if new_char == b'\r' or new_char == b'\n':  # 如果是换行，则输入结束
            print('')
            break
        elif new_char == b'\b':  # 如果是退格，则删除末尾一位
            if chars:
                star_cnt -= star_cnt
                del chars[-1]
                sys.stdout.write('\b')  # 后退一格，但无法删除星号...
                sys.stdout.flush()
        else:
            star_cnt += 1
            chars.append(new_char)
            sys.stdout.write('*')  # 显示为星号
            sys.stdout.flush()
    return "".join([str(c, encoding='utf-8') for c in chars])


def is_connect():
    if "Linux" in platform.platform():
        ret = os.system("ping -c 1 www.baidu.com")
    else:
        ret = os.system("ping -n 1 www.baidu.com")
    print(ret)
    if ret == 0:
        return True
    else:
        return False


def login_request(username, password, keep_alive):
    post_addr, post_header, post_data = param_init(username, password)
    print("Request now...")
    logger.info("Request now...")
    result = requests.post(post_addr, data=post_data, headers=post_header)
    print("Request return: {}".format(result))
    logger.info("Request return: {}".format(result))
    if is_connect():
        print("success")
        logger.info("success")
    else:
        print("Login failed")
        logger.warning("Login failed")
    while keep_alive:
        if not is_connect():
            print("Host offline, request now...")
            logger.info("Host offline, request now...")
            result = requests.post(post_addr, data=post_data, headers=post_header)
            print("Request return: {}".format(result))
            logger.info("Request return: {}".format(result))
            if not is_connect():
                print("Login failed, retry immediately...")
                logger.warning("Login failed, retry immediately...")
                continue
            else:
                print("Success")
                logger.info("Success")
        time.sleep(60)
    input("press Enter to quit")


def main():
    username = input("Enter the user name: ")
    password = pwd_input("Enter the pass word: ")
    keep_alive = input("Keep alive ? ('y' or 'n'): ")
    while keep_alive != 'y' and keep_alive != 'n':
        print("please enter 'y' or 'n':")
        keep_alive = input()
    if keep_alive == 'y':
        keep_alive = True
    else:
        keep_alive = False

    login_request(username, password, keep_alive)


if __name__ == "__main__":
    main()
