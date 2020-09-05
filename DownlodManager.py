import json


class DownloadManager:
    def __init__(self, filename='downloaded.json'):
        self.episodes = dict()
        self.filename = filename

    def load(self):
        try:
            with open(self.filename) as f:
                self.episodes = json.load(f)
        except FileNotFoundError:
            print("create new file: ", self.filename)

    def save(self):
        with open(self.filename, mode='w') as f:
            json.dump(self.episodes, f, indent=2, ensure_ascii=False)

    def is_downloaded(self, date: str):
        return date in self.episodes

    def add(self, date: str, title: str, url: str):
        self.episodes[date] = {'title': title, 'url': url}
