import yaml

# 工具方法
def read(path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
    
def write(content, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(content, f, encoding='utf-8', allow_unicode=True)
    
def string_to_list(string:str):
    return string.split(",") if isinstance(string, str) else string