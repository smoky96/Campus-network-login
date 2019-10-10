import argparse
import os
import time

import requests
import platform

from logger import setup_custom_log

logger, _ = setup_custom_log("", "connect")

parser = argparse.ArgumentParser(description="Net Login")
parser.add_argument("--user", type=str)
parser.add_argument("--password", type=str)
parser.add_argument("--keep_alive", action="store_true", default=False)
args = parser.parse_args()

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
    "DDDDD": args.user,
    "upass": args.password,
    "0MKKey": "123"
}


def is_connect():
    if "Linux" in platform.platform():
        ret = os.system("ping -c 1 www.baidu.com")
    else:
        ret = os.system("pint -n 1 www.baidu.com")
    if ret == 0:
        return True
    else:
        return False


def login_request():
    logger.info("Request now...")
    result = requests.post(post_addr, data=post_data, headers=post_header)
    logger.info("Request return: {}".format(result))
    if is_connect():
        logger.info("success")
    else:
        logger.warning("Login failed")
    while args.keep_alive:
        if not is_connect():
            logger.info("Host offline, request now...")
            result = requests.post(post_addr, data=post_data, headers=post_header)
            logger.info("Request return: {}".format(result))
            if not is_connect():
                logger.warning("Login failed, retry immediately...")
                continue
            else:
                logger.info("Success")
        time.sleep(60)


if __name__ == "__main__":
    login_request()
