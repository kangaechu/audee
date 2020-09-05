import json


class DownloadManager:
    def __init__(self, album, filename='downloaded.json'):
        self.downloaded = dict()
        self.album = album
        self.filename = filename

    def load(self):
        try:
            with open(self.filename) as f:
                self.downloaded = json.load(f)
        except FileNotFoundError:
            print("create new file: ", self.filename)

    def save(self):
        with open(self.filename, mode='w') as f:
            json.dump(self.downloaded, f, indent=2, ensure_ascii=False)

    def is_downloaded(self, date: str):
        return date in self.downloaded[self.album]

    def add(self, date: str, title: str, url: str):
        self.downloaded[self.album][date] = {'title': title, 'url': url}
