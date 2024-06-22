import os

# 获取当前位置
home_dir = os.path.dirname(__file__)
# 获取父目录
PARENT_DIR = os.path.dirname(home_dir)
# 获取配置文件所在位置
ALIST = os.path.join(home_dir, "anima_config.yml")

class Rss:
    # 过滤天数, 只获取 Day 天内的内容
    DAY = 7

    # 过滤器标识, 当为 True 时启动其过滤器
    BLACKLIST = True
    EPISODE = True
    DATE = True



class Aria2Config:
    LOG = "/tmp/aria2.log"
    PATH = "/var/tmp/animation"

    port = 6800
    server = "localhost"

    SERVER = f"http://{server}:{port}/rpc"
    SECRET = "LoongLit"