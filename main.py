import re

import requests
from bs4 import BeautifulSoup
from datetime import date
import subprocess
from DownlodManager import DownloadManager


def get_detail_urls(url='https://park.gsj.mobi/program/voice/100000061'):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.select(".column_yokolist")
    return [article.select_one("a").get("href") for article in articles]


def get_detail_page_info(url='https://park.gsj.mobi/voice/show/23234'):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.select_one("h1").text
    recorded_at = datestring_to_date(soup.select_one("div.voice_date").text.strip())
    pattern = re.compile(r'mp3: \"(.*?)\"', re.MULTILINE | re.DOTALL)
    scripts = soup.select("script")
    url = ""
    for script in scripts:
        match = pattern.search(str(script.contents))
        if match:
            url = "https:" + match.group(1)
            break
    return url, title, recorded_at


def datestring_to_date(datestring):
    ymd = datestring.split('/')
    return date(int(ymd[0]), int(ymd[1]), int(ymd[2]))


def download(url, title, recorded_at: date):
    ymd = recorded_at.strftime("%Y-%m-%d")
    name = "%s %s" % (ymd, title)
    name = re.sub(r'[\\/:*?"<>|]+', '', name)
    artist = "Tokyo FM"
    album = "清水みさとの、サウナいこ？"
    genre = "Radio"
    cmd = 'ffmpeg -i "%s" ' \
          '-metadata title="%s" ' \
          '-metadata artist="%s" ' \
          '-metadata album="%s" ' \
          '-metadata date="%s" ' \
          '-metadata genre="%s" ' \
          '"%s.mp3"' \
          % (url, name, artist, album, ymd, genre, name)
    subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    dm = DownloadManager()
    dm.load()

    for url in get_detail_urls('https://park.gsj.mobi/program/voice/100000061?page=3'):
        url, title, recorded_at = get_detail_page_info(url)
        date_str = recorded_at.strftime("%Y-%m-%d")
        if dm.is_downloaded(date_str):
            print("%s is already downloaded" % date_str)
        else:
            print("%s downloading" % date_str)
            download(url, title, recorded_at)
            dm.add(date_str, title, url)

    dm.save()
