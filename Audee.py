import os
import re
import subprocess
from datetime import date

import requests
from bs4 import BeautifulSoup

from DownlodManager import DownloadManager


def get_detail_urls(url='https://audee.jp/voice/show/27652'):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    voice_section = soup.select_one
    articles = voice_section.select(".box-article-item")
    return [article.select_one("a").get("href") for article in articles]


def datestring_to_date(datestring):
    ymd = datestring.split('(')[0].split('/') # (曜日)を削除
    return date(int(ymd[0]), int(ymd[1]), int(ymd[2]))


def get_detail_page_info(url='https://audee.jp/voice/show/27863'):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.select_one(".ttl-inner").contents[1].strip()
    recorded_at = datestring_to_date(soup.select_one(".txt-date-01").text.strip())
    pattern = re.compile(r'"voice": \"(.*?)\"', re.MULTILINE | re.DOTALL)
    scripts = soup.select("script")
    url = ""
    for script in scripts:
        match = pattern.search(str(script.contents))
        if match:
            url = match.group(1)
            break
    return url, title, recorded_at


class Audee:
    def __init__(self, url, album, prog_dir):
        self.url = url
        self.album = album
        self.prog_dir = prog_dir
        self.artist = "Tokyo FM"
        self.genre = "Radio"

    def download(self):
        dm = DownloadManager(self.album)
        dm.load()

        for url in get_detail_urls(self.url):
            url, title, recorded_at = get_detail_page_info(url)
            date_str = recorded_at.strftime("%Y-%m-%d")
            if dm.is_downloaded(date_str):
                # print("%s %s is already downloaded" % (self.album, date_str))
                pass
            else:
                print("%s %s downloading" % (self.album, date_str))
                self.__download(url, title, recorded_at)
                dm.add(date_str, title, url)

        dm.save()

    def __download(self, url, title, recorded_at: date):
        ymd = recorded_at.strftime("%Y-%m-%d")
        name = "%s %s" % (ymd, title)
        name = re.sub(r'[\\/:*?"<>|]+', '', name)
        audio_filename = os.path.join(self.prog_dir, name + ".mp3")
        cmd = 'ffmpeg -i "%s" ' \
              '-metadata title="%s" ' \
              '-metadata artist="%s" ' \
              '-metadata album="%s" ' \
              '-metadata date="%s" ' \
              '-metadata genre="%s" ' \
              '"%s"' \
              % (url, name, self.artist, self.album, ymd, self.genre, audio_filename)
        subprocess.call(cmd, shell=True)
