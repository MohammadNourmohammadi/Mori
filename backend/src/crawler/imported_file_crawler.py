from crawler.abstract import Crawler
import json

class ImportedFileCrawler(Crawler):

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
        self.data = {}
    
    def obtain_data(self):
        f = open(self.path)
        self.data = json.load(f)

    def get_data(self):
        return self.data

    
