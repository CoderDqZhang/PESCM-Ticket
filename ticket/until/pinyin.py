import pinyin

#输入name
def get_pinyin_first_alpha(name):
    print(name)
    return "".join([i[0] for i in pinyin.get(name, " ").split(" ")]).upper()
