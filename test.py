import anima
from config import ALIST, ALIST_DEFAULT
import os, shutil

def test_anime_config():

    print(f"开始检查配置文件{ALIST}")

    if not os.path.exists(ALIST): shutil.copy(ALIST_DEFAULT, ALIST)

    def __check_rss_key(config_name, rss_integer):

        if not isinstance(rss_integer, int): exit(f"{config_name} 的 rss 值类型不是整数型")
        if rss_integer > len(rss_list) -1: exit(f"{config_name} 的 rss 数字大于 rss_list 的长度")

    def __check_downloader_key(config_name, downloader_string):

        if not isinstance(downloader_string, str): exit(f"{config_name} 的 downloader 值类型不是字符串")
        if downloader_string != 'aria2': exit(f"{config_name} 的 downloader 不为 aria2")


    def __check_default_config():

        try:
            config['default']; 
            downloader_string = config['default']['downloader']; rss_integer = config['default']['rss']
            rss_integer = "0" if rss_integer == 0 else rss_integer

        except KeyError:
            exit(f"在缺少默认配置 default 的情况下, {rule_set_name} 缺少键 downloader 或 rss")

        if not (downloader_string and rss_integer): exit(f"{rule_set_name} 缺少键 downloader 或 rss, 其默认配置(default) downloader 或 rss 为空")
        
        rss_integer = 0 if rss_integer == "0" else rss_integer
        __check_rss_key('default', rss_integer); __check_downloader_key('default', downloader_string)



    config = anima.OperateAnimeConfigFile.get_config_file()

    # 检查必要配置的是否缺少
    try: rss_list = config['rss']; rule_sets = config['animation']
    except KeyError as e: exit(f"缺少必要配置配置 {e}")

    # 检查数据类型是否正确
    if not isinstance(rss_list, list): exit("rss 配置格式不正确, 其数据类型为列表")
    if not isinstance(rule_sets, dict): exit("animation 配置格式不正确, 其数据类型为字典")

    # 检查 rss 列表是否为空
    if not rss_list: exit("rss 配置为空, 请检查")

    # 检查规则集 animation
    for rule_set_name, rule_set in rule_sets.items():
        # 检查数据类型
        if not isinstance(rule_sets[rule_set_name], dict): exit(f"{rule_set_name} 配置格式不正确, 其数据类型为字典")
        
        # 检查规则集的主键
        keys = ['episode', 'whitelist', 'downloader', 'rss']
        rule_set_keys = rule_set.keys()
        if 'episode' not in rule_set_keys: exit(f"{rule_set_name}缺少必要的配置项 'episode'")

        # 检查规则集缺少 downloader 和 rss 的情况下,检查 default 配置项
        if ('downloader' and 'rss') not in rule_set_keys: __check_default_config()

        for key in rule_set_keys:

            if key not in keys: print(f"配置{rule_set_name}的键{key}错误, 正确为{keys}")

        
        if "rss" in rule_set_keys: rss_integer = rule_set['rss']; __check_rss_key(rule_set_name, rss_integer)

        if "downloader" in rule_set_keys: downloader_string = rule_set['downloader']; __check_downloader_key(rule_set_name, downloader_string)

    print("自检完成")