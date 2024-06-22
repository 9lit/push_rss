from config import Aria2Config
import xmlrpc.client

class InvokeDownloader(Aria2Config):

    def __init__(self, url, downloader) -> None:
        self.url = url
        
        match downloader:
            case "aria2": self.__aria2()

    def __aria2(self):
        server = xmlrpc.client.ServerProxy(self.SERVER)
        server.aria2.addUri(f'token:{self.SECRET}', [self.url], dict(dir=self.PATH))