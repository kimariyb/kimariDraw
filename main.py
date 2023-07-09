import os

from matplotlib import pyplot as plt

from Spectrum.spectrum_factory import SpectrumFactory
from Parser.parser_factory import ParserFactory
from Utils.utils import welcome, main_view


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
    main_choice = main_view()
    # 设置全局字体、字重和轴线宽度
    plt.rcParams.update({
        'font.family': 'Arial',
        'font.weight': 'bold',
        'axes.linewidth': 1.5
    })
    if main_choice == "1":
        # 创建一个 NMRSpectrum 对象
        nmr_spectrum = SpectrumFactory.create_spectrum('NMR')
        # 调用绘图函数
        fig, ax = nmr_spectrum.plot_spectrum(dataframe)
        # 展示图片
        fig.show()
        # 询问是否保存图片
        save_choice = input('Do you want to save the image? (y/n) ')
        if save_choice.lower() == 'y':
            fig.savefig('NMR_Spectrum' + '.' + nmr_spectrum.save_format, dpi=500, bbox_inches='tight')


if __name__ == '__main__':
    main()
