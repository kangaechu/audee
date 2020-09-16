import os

import yaml


class DownloadManager:
    def __init__(self, album, filename='conf/downloaded.yaml'):
        self.downloaded = dict()
        self.album = album
        self.filename = os.path.join(os.path.dirname(__file__), filename)

    def load(self):
        try:
            with open(self.filename) as f:
                self.downloaded = yaml.load(f, Loader=yaml.CLoader)
        except FileNotFoundError:
            print("create new file: ", self.filename)
        if self.album not in self.downloaded:
            self.downloaded[self.album] = {}

    def save(self):
        with open(self.filename, mode='w') as f:
            yaml.dump(self.downloaded, f, encoding='utf-8', allow_unicode=True)

    def is_downloaded(self, date: str):
        return date in self.downloaded[self.album]

    def add(self, date: str, title: str, url: str):
        self.downloaded[self.album][date] = {'title': title, 'url': url}
