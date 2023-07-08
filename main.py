import os

from pandas import DataFrame

from src.Utils.utils import welcome
from src.Parser.parser_factory import ParserFactory


def main():
    # 初始变量
    url = ''
    spectrum_type = ''
    # 设置欢迎界面
    welcome()
    # 输入文件路径，
    url = input()
    # 处理异常
    if not os.path.isfile(url):
        raise FileNotFoundError(f"File not found: {url}")
    # 从 Parser 工厂中创建一个 Parser，并处理异常
    try:
        parser = ParserFactory.create_parser(url)
        dataframe = parser.parse()
    except Exception as e:
        raise ValueError(f"Error parsing data from file: {url}: {e}")
    # 主程序界面
    print('Please enter the spectrum you want to plot.')
    print('1. NMR')
    spectrum_type = input()
    # 判断
    if spectrum_type == '1':
        pass
    elif spectrum_type == '2':
        pass


if __name__ == '__main__':
    main()
