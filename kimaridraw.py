import argparse
import datetime
import os
import sys
from pathlib import Path

import matplotlib
import proplot as pplt
import pandas as pd
import toml

from pandas import DataFrame
from proplot import rc, Colormap

# 提取常量和配置
DEFAULT_DPI = 500
DEFAULT_IMAGE_FORMAT = "png"
VERSION_INFO = {
    'version': 'v2.4.0',
    'release_date': 'Aug-6-2023',
    'developer': 'Kimariyb, Ryan Hsiun',
    'address': 'XiaMen University, School of Electronic Science and Engineering',
    'website': 'https://github.com/kimariyb/kimariDraw',
}


class SpectrumConfig:
    def __init__(self):
        self.plot_type = None
        self.x_limit = None
        self.y_limit = None
        self.title = None
        self.x_label = None
        self.y_label = None
        self.font_family = None
        self.figure_size = None
        self.colors = None
        self.line_style = None
        self.zero_line = None
        self.serial = None
        self.legend = None
        self.legend_text = None
        self.sup_type = None

    @staticmethod
    def from_toml(file_path):
        config = SpectrumConfig()
        with open(file_path, 'r', encoding='utf-8') as file:
            data = toml.load(file)

        config.plot_type = data.get('PlotType')
        config.x_limit = data.get('xLimit')
        config.y_limit = data.get('yLimit')
        config.title = data.get('Title')
        config.x_label = data.get('xLabel')
        config.y_label = data.get('yLabel')
        config.font_family = data.get('FontFamily')
        config.figure_size = data.get('FigureSize')
        config.colors = data.get('Colors')
        config.line_style = data.get('LineStyle')
        config.zero_line = data.get('ZeroLine')
        config.serial = data.get('Serial')
        config.legend = data.get('Legend')
        config.legend_text = data.get('LegendText')
        config.sup_type = data.get('SupType')

        return config

    def __str__(self):
        return f"PlotType: {self.plot_type}\nxLimit: {self.x_limit}\nyLimit: {self.y_limit}\nTitle: {self.title}\n" \
               f"xLabel: {self.x_label}\nyLabel: {self.y_label}\nFontFamily: {self.font_family}\nFigureSize: {self.figure_size}\n" \
               f"Colors: {self.colors}\nLineStyle: {self.line_style}\nZeroLine: {self.zero_line}\nSerial: {self.serial}\n" \
               f"Legend: {self.legend}\nLegendText: {self.legend_text}\nSupType: {self.sup_type}"


def get_dataframe(file_name: str):
    """
    装载记录光谱数据的 txt 文件，并返回为一个 pandas DataFrame 对象
    :return: DataFrame 对象
    """
    file_path = Path(file_name)
    # 读取文件
    with file_path.open('r', encoding='utf-8') as f:
        df = pd.read_csv(f, delim_whitespace=True, header=None)
    # 为列指定新的标签
    df = df.rename(columns={0: 'x'})
    # 判断 DataFrame 对象有多少个列，如果只有两列，就分别命名为 x 和 y
    if len(df.columns) == 2:
        df = df.rename(columns={1: 'y'})
    else:
        # 判断 DataFrame 对象有多少个列，如果只有多列，就分别命名为 x 和 y1、y2 ...
        for i in range(1, len(df.columns)):
            df = df.rename(columns={i: 'y{}'.format(i)})
    return df


def read_multiple(multiple_path: str):
    """
    读取 multiple.txt 并将其中的 txt 文件返回为 DataFrame 对象
    :param multiple_path: multiple.txt 文件的绝对路径
    :return: 返回一个装有 DataFrame 对象的集合
    """
    try:
        # 装载 multiple.txt
        multiple_file = Path(multiple_path)
        # 打开 multiple 文件
        with multiple_file.open('r', encoding='utf-8') as file:
            # 将文件记录的每一行返回成一个字符串，删除多余的制表符和空格
            data_paths = [line.strip() for line in file]

        dataframe_list = []
        # 读取每个装载记录光谱数据的 txt 文件并返回为一个 pandas DataFrame 对象
        for data_path in data_paths:
            try:
                dataframe = get_dataframe(data_path)
                dataframe_list.append(dataframe)
            except FileNotFoundError:
                print(f"File {data_path} not found.")
            except Exception as e:
                print(f"An error occurred while processing {data_path}: {str(e)}")

        return dataframe_list

    except FileNotFoundError:
        raise f"File {multiple_path} not found."

    except Exception as e:
        raise f"An error occurred: {str(e)}"


def is_multiple(data):
    """
    用来判断 data 是单曲线还是多曲线图
    """
    flag = False
    if len(data.columns) > 2:
        flag = True
    else:
        flag = False

    return flag


def draw_multiple(config: SpectrumConfig, axs, data_list):
    """
    绘制多子图的方法
    :param config: SpectrumConfig 对象
    :param axs: proplot Axes 对象集合
    :param data_list: 装有绘制数据的 DataFrame 对象的集合
    """
    # 图例文本集合
    label_list = config.legend_text
    # 颜色集合
    color_list = config.colors
    # 样式集合
    style_list = config.line_style

    # 设置标志位
    flag = 0

    if flag == 0:
        for ax, data in zip(axs, data_list):
            # 首先判断每一个子图是否为多曲线图
            if is_multiple(data):
                # 遍历 DataFrame 对象的列，跳过第一列 'x'
                for i, column in enumerate(data.columns[1:], start=0):
                    multi_color = color_list[i % len(color_list)]
                    multi_label = label_list[i % len(label_list)]
                    multi_style = style_list[i % len(style_list)]
                    # 绘制曲线图
                    ax.plot(data['x'], data[column], linewidth=1.3, linestyle=multi_style, color=multi_color,
                            label=multi_label)

                # 如果开启显示图例，则执行下面的代码
                if config.legend == 1:
                    # 显示图例
                    ax.legend(loc='best', ncols=1, fontweight='bold', frame=False)
                # 如果开启显示 Zero 轴，则执行下面的代码
                if config.zero_line == 1:
                    # 显示 Zero 轴
                    ax.axhline(y=0, color='black', linewidth=1.25)
            else:
                flag = 1

    if flag == 1:
        # 否则绘制单曲线多子图
        for ax, data, color, label, style in zip(axs, data_list, color_list, label_list, style_list):
            # 绘制曲线图
            ax.plot(data['x'], data['y'], linewidth=1.3, color=color, label=label, linestyle=style)

            # 如果开启显示图例，则执行下面的代码
            if config.legend == 1:
                # 显示图例
                ax.legend(loc='best', ncols=1, fontweight='bold', frame=False)
            # 如果开启显示 Zero 轴，则执行下面的代码
            if config.zero_line == 1:
                # 显示 Zero 轴
                ax.axhline(y=0, color='black', linewidth=1.25)


def draw_single(config: SpectrumConfig, ax, data: DataFrame):
    """
    绘制单子图的方法
    :param config: SpectrumConfig 对象
    :param ax: proplot Axes 对象
    :param data: 装有绘制数据的 DataFrame 对象
    """
    # 图例文本集合
    label_list = config.legend_text
    # 颜色集合
    color_list = config.colors
    # 样式集合
    style_list = config.line_style

    # 根据 DataFrame 的数据绘制单子图的光谱图
    # 首先判断 DataFrame 对象所记载的是否为多曲线图
    if is_multiple(data):
        # 循环绘制多曲线图
        for i, column in enumerate(data.columns[1:]):
            ax.plot(data['x'], data[column], linewidth=1.3, color=color_list[i % len(color_list)],
                    label=label_list[i % len(label_list)], linestyle=style_list[i % len(style_list)])
    else:
        # 否则绘制单曲线图
        ax.plot(data['x'], data['y'], linewidth=1.3, color=color_list, label=label_list, linestyle=style_list)

    # 如果开启显示图例，则执行下面的代码
    if config.legend == 1:
        # 显示图例
        ax.legend(loc='best', ncols=1, fontweight='bold', frame=False)
    # 如果开启显示 Zero 轴，则执行下面的代码
    if config.zero_line == 1:
        # 显示 Zero 轴
        ax.axhline(y=0, color='black', linewidth=1.25)


def save_spectrum(fig, save_type, dpi):
    """
    保存光谱图片为某一格式
    :param save_type: 保存的格式，默认为 png 格式
    :param fig: matplotlib figure 对象
    :param dpi: 保存图片的 dpi
    """
    # 文件名初始值
    file_name = f"figure.{save_type}"
    i = 1
    # 首先检查当前路径是否存在以 figure.save_type 为文件名的文件
    while os.path.exists(file_name):
        # 文件名已存在，添加数字后缀
        file_name = f"figure{i}.{save_type}"
        i += 1
    # 保存光谱图
    fig.savefig(file_name, dpi=dpi, bbox_inches="tight", pad_inches=0.2)


def draw_spectrum(config: SpectrumConfig, save_type, dpi, data_list=None, data=None):
    """
    绘制光谱图
    :param config: SpectrumConfig 对象
    :param data_list: 装有绘制数据的 DataFrame 对象的集合。仅在开启子图时使用
    :param data: 装有绘制数据的 DataFrame 对象。仅在不开启子图时使用
    :param save_type: 图片保存的格式，默认为 png 格式
    :param dpi: 保存图片的 dpi
    """
    # 设置全局属性
    rc['font.name'] = config.font_family
    rc['tick.width'] = 1.3
    rc['meta.width'] = 1.3
    rc['label.weight'] = 'bold'
    rc['tick.labelweight'] = 'bold'
    rc['ytick.major.size'] = 4.6
    rc['ytick.minor.size'] = 2.5
    rc['xtick.major.size'] = 4.6
    rc['xtick.minor.size'] = 2.5

    # 得到 xlim 和 ylim 以及 xminor 和 yminor
    min_xlim = config.x_limit[0]
    max_xlim = config.x_limit[1]
    tick_xlim = config.x_limit[2]
    min_ylim = config.y_limit[0]
    max_ylim = config.y_limit[1]
    tick_ylim = config.y_limit[2]
    xminor = tick_xlim / 2
    yminor = tick_ylim / 2

    # 判断多子图是否开启，开启多子图对应 plot_type = 2
    if config.plot_type == 2:
        # 创建子图和坐标轴
        fig = pplt.figure(figsize=config.figure_size, dpi=300, span=True, share=True)
        axs = fig.subplots(nrows=config.sup_type[0], ncols=config.sup_type[1])

        # 调用绘制多子图的方法
        draw_multiple(config, axs, data_list)

        # 设置一个标志，如果开启显示子图的序号，则显示子图
        if config.serial == 1:
            serial_flag = "(a)"
        else:
            serial_flag = False

        # 使用循环设置子图的 x 轴和 y 轴标签
        for ax in axs:
            ax.set_xlabel("", fontsize=11.5)
            ax.set_ylabel("", fontsize=11.5)

        # 设置整个图像的 x 标签和 y 标签
        fig.format(
            xlabel=config.x_label, ylabel=config.y_label
        )

        # 设置图像的一些杂属性，如果开启多子图绘制时，可以选择是否显示子图的序号。
        axs.format(
            grid=False, xlocator=tick_xlim, ylocator=tick_ylim, xlim=(min_xlim, max_xlim), ylim=(min_ylim, max_ylim),
            abc=serial_flag, abcloc="ul", xminorlocator=xminor, yminorlocator=yminor
        )

        # 显示图像
        fig.show()
        # 最后调用保存图像方法
        save_spectrum(fig, save_type, dpi)

    # 如果没有开启子图，则对应 plot_type = 1
    elif config.plot_type == 1:
        # 创建子图和坐标轴
        fig = pplt.figure(figsize=config.figure_size, dpi=300, span=True, share=True)
        ax = fig.subplots()

        # 调用绘制单子图的方法
        draw_single(config, ax, data)

        # 设置 x 轴 y 轴标签
        ax.set_xlabel("", fontsize=11.5)
        ax.set_ylabel("", fontsize=11.5)

        # 设置图像的一些杂属性，如果开启多子图绘制时，可以选择是否显示子图的序号。
        ax.format(
            xlabel=config.x_label, ylabel=config.y_label,
            grid=False, xlocator=tick_xlim, ylocator=tick_ylim, xlim=(min_xlim, max_xlim), ylim=(min_ylim, max_ylim),
            xminorlocator=xminor, yminorlocator=yminor
        )

        # 显示图像
        fig.show()
        # 最后调用保存图像方法
        save_spectrum(fig, save_type, dpi)


def show(version_info, config):
    """
    显示程序的基本信息、配置信息以及版权信息。
    """
    # 程序最后输出版本和基础信息
    print(f"KimariDraw --  A Python script that processes Multiwfn spectral data and plots various spectra.")
    print(f"Version: {version_info['version']}, release date: {version_info['release_date']}")
    print(f"Developer: {version_info['developer']}")
    print(f"Address: {version_info['address']}")
    print(f"KimariDraw home website: {version_info['website']}\n")
    # 获取当前日期和时间
    now = datetime.datetime.now().strftime("%b-%d-%Y, 00:45:%S")
    if config is not None:
        print("The toml configuration is:")
        print(f"{config}\n")

    # 程序结束后提示版权信息和问候语
    print("Copyright © 2023 Kimariyb. All rights reserved.")
    print(f"Currently timeline: {now}\n")


def console_process(version_info):
    """
    当使用命令行调用时，执行这段代码
    """
    # 处理命令行参数
    arg = sys.argv[1]
    # 执行其他逻辑
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(prog='KimariPlot', add_help=False,
                                     description='KimariPlot -- A Python script that processes Multiwfn spectral data '
                                                 'and plots various spectra.')
    # 添加 -h 参数
    parser.add_argument('--help', '-h', action='help', help='Show this help message and exit')
    # 添加输入文件参数
    parser.add_argument('input', type=str, help='Text file containing spectral data generated by Multiwfn')
    # 添加设置文件参数
    parser.add_argument('--set', '-s', dest='set', type=str, default="settings.toml",
                        help='The toml file to record the setting information, the default is settings.toml in the '
                             'current directory')
    # 添加设置图片 dpi 参数
    parser.add_argument('--dpi', '-d', dest='dpi', type=int, help='The dpi of the output graph, the default is 500',
                        default=500)
    # 添加设置图片保存格式
    parser.add_argument('--format', '-f', dest='format', type=str, default='png', help='The image format of the '
                                                                                       'output file, the default is '
                                                                                       'png')
    # 添加版权信息和参数
    parser.add_argument('--version', '-v', action='version', help='Show the version information',
                        version=version_info['version'])
    # 解析参数
    args = parser.parse_args()

    # 处理命令行参数
    input_file = args.input
    set_file = args.set
    dpi = args.dpi
    image_format = args.format

    # 拿到 config 对象
    config = SpectrumConfig().from_toml(set_file)

    # 显示程序信息和配置信息
    show(version_info, config)

    # 判断是否开启绘制多子图，如果开启多子图，则必须传入一个名为 multiple.txt 的文件，否则抛出异常
    if config.plot_type == 2:
        # 读取 multiple.txt
        data_list = read_multiple(input_file)
        # 绘制多子图光谱
        draw_spectrum(config, save_type=image_format, dpi=dpi, data_list=data_list)
        # 如果没有开启多子图
    elif config.plot_type == 1:
        # 读取数据文件
        data = get_dataframe(input_file)
        # 绘制单子图光谱
        draw_spectrum(config, save_type=image_format, dpi=dpi, data=data)


def execute_process():
    """
    当使用可执行程序调用时，执行这段代码
    """
    # 首先显示程序信息和配置信息
    show(VERSION_INFO, config=None)
    # 默认的设置文件
    set_file = "settings.toml"

    # 接着询问是否使用默认的 settings.toml 配置文件，可选 y：是；n：否
    # 如果选择 y 则需要重新输入 toml 配置文件，如果选择 n 则使用 settings.toml
    use_default_settings = input(
        "Do you want to use the default settings.toml configuration file? (y/n):\n").lower() == "n"

    # 如果选择了 y，则覆盖默认的设置文件，并重新输入新的配置文件名
    if use_default_settings:
        set_file = input("Please enter the toml configuration file.\n")
        # 如果什么都不输入直接 Enter，则重新询问，如果输入 q 则退出。
        while set_file == "":
            set_file = input("Please enter the toml configuration file or 'q' to quit.\n")
            if set_file.lower() == "q":
                break

    # 拿到 config 对象
    config = SpectrumConfig().from_toml(set_file)

    # 输入需要绘制的光谱数据
    input_file = input("Please enter a txt file containing spectral data generated by Multiwfn.\n")

    # 接着进入主功能页面，可以设置一些东西
    # 1. 选择保存图片的分辨率
    # 2. 选择保存图片的格式
    # 3. 绘制并保存图片
    while True:
        def main_menu():
            print()
            print("======= Main function page =======")
            print(f"1. Change the dpi of image. now dpi is: {DEFAULT_DPI}")
            print(f"2. Change the format of image. now format is: {DEFAULT_IMAGE_FORMAT}")
            print(f"3. Plot and save the image now!")

        def update_dpi(new_dpi):
            global DEFAULT_DPI
            DEFAULT_DPI = int(new_dpi)
            print(f"Dpi has been changed to: {DEFAULT_DPI}")

        def update_image_format(new_format):
            global DEFAULT_IMAGE_FORMAT
            DEFAULT_IMAGE_FORMAT = new_format
            print(f"Image format has been changed to: {DEFAULT_IMAGE_FORMAT}")

        main_menu()

        select = input("Please select the operation to be performed (enter the corresponding number):\n")
        # 如果选择 1，修改保存图片的分辨率
        if select == "1":
            new_dpi = input("Please enter a new dpi (type q to quit):\n")
            if new_dpi.lower() == "q":
                continue  # 返回主功能页面
            update_dpi(new_dpi)
        # 如果选择 2，修改选择保存图片的格式
        elif select == "2":
            new_format = input("Please enter a new image format (type q to quit):\n")
            if new_format.lower() == "q":
                continue  # 返回主功能页面
            update_image_format(new_format)
        # 如果选择 3，直接绘图
        elif select == "3":
            global DEFAULT_DPI
            global DEFAULT_IMAGE_FORMAT
            # 判断是否开启绘制多子图，如果开启多子图，则必须传入一个名为 multiple.txt 的文件，否则抛出异常
            if config.plot_type == 2:
                # 读取 multiple.txt
                data_list = read_multiple(input_file)
                # 绘制多子图光谱
                draw_spectrum(config, save_type=DEFAULT_IMAGE_FORMAT, dpi=DEFAULT_DPI, data_list=data_list)
                # 如果没有开启多子图
            elif config.plot_type == 1:
                # 读取数据文件
                data = get_dataframe(input_file)
                # 绘制单子图光谱
                draw_spectrum(config, save_type=DEFAULT_IMAGE_FORMAT, dpi=DEFAULT_DPI, data=data)
            print("The picture is drawn and saved!")
            break
        else:
            print("Invalid selection!")


# 命令行运行方式
if len(sys.argv) > 1:
    console_process(VERSION_INFO)
# 直接双击可执行文件运行方式
else:
    execute_process()
