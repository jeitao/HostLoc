#!/usr/bin/env python
from time import sleep
from urllib.parse import urljoin
import hashlib
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from redis import Redis
import os

HEADERS = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
}

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHANNEL_NAM = os.environ.get('CHANNEL_NAM')
ROOT_URL = "https://www.hostloc.com/forum.php?mod=forumdisplay&fid=45&filter=author&orderby=dateline"
BOT = Bot(token=TELEGRAM_BOT_TOKEN)
REDIS_CONN = Redis(host='redis', db=0)


def send_telegram_message(title, url):
    """
    发送telegram消息通知
    :param title: 标题
    :param url: 地址
    """
    try:
        BOT.send_message(CHANNEL_NAM, "{}\n{}".format(title, url))
    except Exception:
        send_telegram_message(title, url)


def title_to_md5(title):
    """
    返回标题的MD5值
    :param title: 标题
    """
    md5 = hashlib.md5()
    md5.update(bytes(title, encoding='utf-8'))
    return md5.hexdigest().upper()


def get_response():
    """
    获取页面返回的response
    """
    try:
        return requests.get(ROOT_URL, headers=HEADERS)
    except Exception:
        return get_response()


if __name__ == '__main__':
    while True:
        resp = get_response()
        soup = BeautifulSoup(resp.text, 'lxml')
        posts = soup.find("table", id="threadlisttableid").findAll("tbody")
        for item in posts:
            if item.get("id") and item["id"].startswith("normalthread"):
                post_a_tag = item.find("a", class_="xst")
                post_url = urljoin(ROOT_URL, post_a_tag["href"])
                post_title = post_a_tag.get_text()
                post_title_md5 = title_to_md5(post_title)
                if REDIS_CONN.get(post_title_md5) is None:
                    send_telegram_message(post_title, post_url)
                    REDIS_CONN.set(post_title_md5, post_title, ex=24 * 60 * 60)
        sleep(5)
