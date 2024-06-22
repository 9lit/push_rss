from anima import ParseAnimaList, animalist, write_anima
from rss import GetXml, Filter
from downloader import InvokeDownloader

class self_test:
    from anima import test_anima_config
    test_anima_config()

def main():
    xml_history = {}
    alist = animalist()

    for name, item in alist.items():
        
        # 获取列表中的数据
        anima = ParseAnimaList(item)
        rss, whitelist, blacklist, episodes, downloader = anima()

        # 获取订阅内容
        xml = GetXml(rss, xml_history)
        xml_history[rss] = xml()

        # 获取下载列表
        f = Filter(xml_history[rss], whitelist, blacklist, episodes)
        download_list = f()

        # 下载种子, 并记录已下载的文件
        for episode in download_list:
            url = download_list[episode]
            # InvokeDownloader(url, downloader)
            # write_anima(name, episode)
            print(episode, url, name)
        

if __name__ == "__main__":
    self_test.test_anima_config()
    main()