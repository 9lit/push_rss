import inspect
import sys
sys.path.append(r'C:\Users\lain\github')
from push_rss import string_to_list, read, write
from config import ALIST

def test_anima_config():

    config = __read_config()

    try:
        config_default = config['default']
        config_default['downloader'], config_default['rssindex']
        rss = config['rss']
        if not rss: raise "rss 列表为空"
        animation = config['animation']

        for a in animation: animation[a]['whitelist']

    except KeyError as e:
        print(f"配置{ALIST}缺少配置项{e}")
        exit()


def __read_config():
    return read(ALIST)

def animalist() -> dict:
    return __read_config()['animation']

def anima_default() -> tuple:

    config = __read_config()['default']
    return config['downloader'], config['rssindex']

def anima_rss() -> list:
    return __read_config()['rss']

    
def write_anima(name, episode):

    def format_episode():
        # 格式化集数, 如果集数格式为 1 则格式化为 01
        return episode if len(str(episode)) > 1 else f"0{episode}"
    
    def alter():
        #将新的集数写入到字典中去
        episode= format_episode()
        new_config = __read_config()
        episode_config = new_config['animation'][name]["episode"]
        new_config['animation'][name]["episode"] = f"{episode_config},{episode}" if episode_config else episode
        return new_config
    
    write(content=alter(), path=ALIST)


class ParseAnimaList:

    def __init__(self, item) -> tuple:
        self.item = item
        self.default_downloader, self.default_rssindex = anima_default()
        self.rsslist = anima_rss()

    
    def __call__(self) -> tuple:

        return self.rssindex(), self.whitelist(), self.blacklist(), self.episode(), self.downloader()


    def __main(self):

        caller_frame = inspect.stack()[1]
        caller_name = caller_frame[3]

        try: config_name = self.item[caller_name]
        except KeyError: config_name = []
        return string_to_list(config_name) if config_name else config_name
    
    def rssindex(self):

        rss_index = self.__main()

        if rss_index:
            try: rss_config = self.rsslist[rss_index]
            except IndexError:
                print("没有指定的 rss 连接, 默认使用第一个")
                rss_config = self.rsslist[self.default_rssindex]

        else:
            rss_config = self.rsslist[self.default_rssindex]

        return rss_config
    
    def whitelist(self):
        return self.__main()
    
    def blacklist(self):
        return self.__main()
    
    def episode(self):
        return self.__main()
    
    def downloader(self):
        downloader = self.__main()

        return downloader if downloader else self.default_downloader
    