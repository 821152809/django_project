# 判断输入的内容是否是中文
def is_Chinese(content):
    for ch in content:
        if "\u4e00" <= ch <= "\u9fff":
            return True
        else:
            return False
