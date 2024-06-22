import time, datetime
import re
import feedparser
from config import Rss

class GetXml:

    def __init__(self, rss_url:str, xml_history:dict) -> dict:
        self.url = rss_url
        self.xml_history = xml_history
        
    def __call__(self) -> tuple:
        if self.url in self.xml_history.keys():
            return self.xml_history[self.url]
        else:
            return self.rss_oschina()
        
    def rss_oschina(self) -> dict:
        a = feedparser.parse(self.url)["entries"]
        return a
    
class _ParseXML:

    def __init__(self, xml_item:dict) -> None:
        
        self.item = xml_item

    def published_parsed(self):
        return self.item["published_parsed"]

    def title(self):
        return self.item["title"]

    def episode(self):
        """获取视频集数, 去除合集"""
        pattern = r'\[\d{2}\]|-\s\d+|E\d+|\[\d{2}v2\]'
        pattern_collection = r' \d+[-|~]\d+ |E\d+[-|~]E\d+'
        episode = re.findall(pattern, self.title())
        collection = re.findall(pattern_collection, self.title())

        return re.findall(r"\d+", episode[0])[0] if episode and not collection else False
    
    def url(self):
        url = self.item["link"]
        links = self.item['links']
        if ".torrent" in url: return url

        for link in links:
            href = link['href']
            if ".torrent" in href: return href

class Filter:
    """过滤器"""

    def __init__(self, xml:dict, whitelist:list, blacklist:list, episodes:list) -> None:
        self.xml, self.whitelist, self.blacklist, self.episodes = xml, whitelist, blacklist, episodes        
    
    def __call__(self) -> list:
        episode_list = {}
        for item in self.xml:
            px = _ParseXML(item)
            
            # 过滤设定时间之外的订阅内容
            if Rss.DATE:
                self.xml_published = px.published_parsed()
                if not self.__published: continue

            # 白名单通过, 拒绝黑名单
            
            self.xml_title = px.title()

            if not self.__whitelist(): continue
            if Rss.BLACKLIST:
                if self.__blacklist(): continue

            # 过滤已下载的剧集
            self.xml_episode = px.episode()
            if Rss.EPISODE:
                if not self.xml_episode: continue
                if self.__episode_exist(): continue

            if self.xml_episode in episode_list.keys(): continue
            # 设置 剧集: 下载链接 列表
            episode_list[self.xml_episode] = px.url()

        return episode_list

    
    def __published(self):
    # 过滤时间范围之外的数据
        current_date = datetime.date.today()
        delta = datetime.timedelta(days=Rss.DAY)
        results = datetime.datetime.strftime(current_date - delta, "%Y-%m-%d")
        return True if self.xml_published > time.strptime(results, "%Y-%m-%d") else False

    def __whitelist(self):
        
        for white in self.whitelist:
            if white in self.xml_title: return True

    def __blacklist(self):
        for black in self.blacklist:
            if black in self.xml_title: return True

    def __episode_exist(self):
        
        if self.xml_episode in self.episodes: return True
