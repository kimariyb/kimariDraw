from kd_parser import KDFileParser

if __name__ == '__main__':
    url = input("请输入文件的绝对路径：")
    kd_data = KDFileParser(url).parse().get_kd_data()
    print(kd_data)
