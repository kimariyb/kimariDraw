import os
from pathlib import Path

import proplot as pplt
import matplotlib.pyplot as plt
import pandas as pd
import toml
from pandas import DataFrame

from proplot import rc


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
    # 根据 DataFrame 的数据绘制多个子图的光谱图
    for ax, data, color, label, style in zip(axs, data_list, color_list, label_list, style_list):
        # 首先判断 DataFrame 对象的列数，如果为 2，则直接绘制
        if len(data.columns) == 2:
            # 绘制折线图
            ax.plot(data['x'], data['y'], linewidth=1.3, color=color, label=label, linestyle=style)
        else:
            # 否则需要继续循环绘制多曲线图
            for column, multi_color, multi_label, multi_style in zip(data.columns[1:], color_list, label_list,
                                                                     style_list):
                ax.plot(data['x'], data[column].values, linewidth=1.3, color=multi_color, label=multi_label,
                        linestyle=multi_style)
        # 如果开启显示图例，则执行下面的代码
        if config.legend == 1:
            # 显示图例
            ax.legend(loc='best', ncols=1, fontweight='bold', frame=False)


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
    # 首先判断 DataFrame 对象的列数，如果为 2，则直接绘制
    if len(data.columns) == 2:
        # 绘制折线图
        ax.plot(data['x'], data['y'], linewidth=1.3, color=color_list, label=label_list, linestyle=style_list)
    else:
        # 否则需要继续循环绘制多曲线图
        for i, column in enumerate(data.columns[1:]):
            ax.plot(data['x'], data[column], linewidth=1.3, color=color_list[i], label=label_list[i],
                    linestyle=style_list[i])
    # 如果开启显示图例，则执行下面的代码
    if config.legend == 1:
        # 显示图例
        ax.legend(loc='best', ncols=1, fontweight='bold', frame=False)
    # 如果开启显示 Zero 轴，则执行下面的代码
    if config.zero_line == 1:
        # 显示 Zero 轴
        ax.axhline(y=0, color='black', linewidth=1.25)


def save_spectrum(fig, save_type="png"):
    """
    保存光谱图片为某一格式
    :param save_type: 保存的格式，默认为 png 格式
    :param fig: matplotlib figure 对象
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
    fig.savefig(file_name, dpi=500, bbox_inches="tight", pad_inches=0.2)


def draw_spectrum(config: SpectrumConfig, data_list=None, data=None):
    """
    绘制光谱图
    :param config: SpectrumConfig 对象
    :param data_list: 装有绘制数据的 DataFrame 对象的集合。仅在。
    :param data: 装有绘制数据的 DataFrame 对象
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
        # 显示绘制结果
        plt.show()
        # 最后调用保存图像方法
        save_spectrum(fig)

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
        # 显示绘制结果
        plt.show()
        # 最后调用保存图像方法
        save_spectrum(fig)


if __name__ == '__main__':
    config = SpectrumConfig().from_toml("settings.toml")
    data_list = read_multiple("multiple.txt")
    draw_spectrum(config, data_list=data_list)
