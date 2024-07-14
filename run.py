from anima import ParseAnimaList, OperateAnimeConfigFile
from rss import GetXml, Filter
from downloader import InvokeDownloader
import test
import sys

def param():

    global test_flag
    import sys
    test_flag = False if "-t" in sys.argv else True

def main():
    xml_history = {}
    rule_sets = OperateAnimeConfigFile.rule_sets()

    for anime_name, anime_rule_set in rule_sets.items():
        
        # 获取列表中的数据
        anima_rule = ParseAnimaList(anime_rule_set)
        rss, whitelist, blacklist, episodes, downloader = anima_rule()

        # 获取订阅内容
        xml = GetXml(rss, xml_history)
        xml_history[rss] = xml()

        # 获取下载列表
        f = Filter(xml_history[rss], whitelist, blacklist, episodes)
        download_list = f()
        if not download_list: continue
        print(anime_name,  download_list)

        if test_flag:
            # 下载种子, 并记录已下载的文件
            for episode in download_list:
                url = download_list[episode]
                InvokeDownloader(url, downloader)
                OperateAnimeConfigFile.write_episode_to_anime_config(anime_name, episode)

if __name__ == "__main__":
    test.test_anime_config()
    param(); main()