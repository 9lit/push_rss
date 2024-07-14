import inspect, sys
from config import ALIST, PARENT_DIR
sys.path.append(PARENT_DIR)
from push_rss import string_to_list, read, write

class OperateAnimeConfigFile:

    def get_config_file(): return read(ALIST)

    def rule_sets() -> dict:
        return OperateAnimeConfigFile.get_config_file()['animation']
    
    def rss_list() -> list:
        return OperateAnimeConfigFile.get_config_file()['rss']

    def default() -> tuple:
        return OperateAnimeConfigFile.get_config_file()['default']

    
    def write_episode_to_anime_config(name, episode):

        def format_episode():
            # 格式化集数, 如果集数格式为 1 则格式化为 01
            return episode if len(str(episode)) > 1 else f"0{episode}"
        
        def alter():
            #将新的集数写入到字典中去
            episode= format_episode()
            new_config = OperateAnimeConfigFile.get_config_file()
            episode_config = new_config['animation'][name]["episode"]
            new_config['animation'][name]["episode"] = f"{episode_config},{episode}" if episode_config else episode
            return new_config
        
        write(content=alter(), path=ALIST)


class ParseAnimaList:

    def __init__(self, anime_rule_set) -> None:
        self.anime_rule_set = anime_rule_set
        self.default = OperateAnimeConfigFile.default()
        self.rss_list = OperateAnimeConfigFile.rss_list()

    def __call__(self) -> tuple:

        return self.rss(), self.whitelist(), self.blacklist(), self.episode(), self.downloader()


    def __main(self) -> list:

        # 获取调用者的方法名称
        caller_frame = inspect.stack()[1]
        caller_name = caller_frame[3]
        
        # 获取追番列表中的规则集, 白名单, 黑名单, 集数, 以及下载器
        try: config_name = self.anime_rule_set[caller_name]
        except KeyError: config_name = []
        return string_to_list(config_name) if config_name else []
    
    def rss(self) -> str:

        try:
            rss_number = self.__main()[0]
            rss_string = self.rss_list[rss_number]
        except IndexError:
            default_rss_number = self.default[self.rss.__name__]
            rss_string = self.rss_list[default_rss_number]

        return rss_string

    def downloader(self) -> str: 
        downloader = self.__main(); default_downloader = self.default[self.downloader.__name__]
        
        return downloader[0] if downloader else default_downloader

    
    def whitelist(self) -> list: return self.__main()
    
    def blacklist(self) -> list: return self.__main()
    
    def episode(self) -> list: return self.__main()    