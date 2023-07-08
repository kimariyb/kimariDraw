import os

from src.Utils.utils import welcome, main_view
from src.Parser.parser_factory import ParserFactory


def main():
    # 设置欢迎界面
    welcome()
    # 输入文件路径，并处理异常
    url = input()
    if not os.path.isfile(url):
        raise FileNotFoundError(f"File not found: {url}")

    # 从 Parser 工厂中创建一个 Parser，并处理异常
    try:
        parser = ParserFactory.create_parser(url)
        dataframe = parser.parse()
    except Exception as e:
        raise ValueError(f"Error parsing data from file: {url}: {e}")

    # 主页面
    main_view()



if __name__ == '__main__':
    main()
