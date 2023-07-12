import os

from matplotlib import pyplot as plt

from Parser.parser_factory import ParserFactory
from Utils.utils import welcome, main_view, plot_nmr_spectrum


def input_file_path():
    # 输入文件路径，并处理异常
    url = input("Please enter the file path: ")
    if not os.path.isfile(url):
        raise FileNotFoundError(f"File not found: {url}")
    return url


def set_global_plot_settings():
    # 设置全局字体、字重和轴线宽度
    plt.rcParams.update({
        'font.family': 'Arial',
        'font.weight': 'bold',
        'axes.linewidth': 1.5
    })


def main():
    # 设置欢迎界面
    welcome()
    # 输入文件路径，并处理异常
    url = input_file_path()

    # 从 Parser 工厂中创建一个 Parser，并处理异常
    try:
        parser = ParserFactory.create_parser(url)
        dataframe = parser.parse()
    except Exception as e:
        raise ValueError(f"Error parsing data from file: {url}: {e}")

    # 设置全局字体、字重和轴线宽度
    set_global_plot_settings()

    while True:
        # 主页面
        main_choice = main_view()
        if main_choice == '0':
            break
        elif main_choice == '1':
            plot_nmr_spectrum(dataframe)


if __name__ == '__main__':
    main()
