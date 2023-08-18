import math
import os
from datetime import datetime
from pathlib import Path

import toml
import wx
import numpy as np
import pandas as pd
import proplot as pplt
from proplot import rc

# 全局变量设定
# 进入主程序时，如果需要修改字号，则使用此全局变量
FONT_SIZE = [10.5, 12, 14]
# 进入主程序时，如果需要修改字体，则使用此全局变量
FONT_FAMILY = "Arial"
# 进入主程序时，如果需要修改 x_limit，则使用此全局变量，默认为 auto
X_LIMIT = "auto"
# 进入主程序时，如果需要修改 y_limit，则使用此全局变量，默认为 auto
Y_LIMIT = "auto"
# 进入主程序时，如果需要修改 x_label, y_label, title, 则使用此全局变量，默认为空
LABEL_TITLE = ["", "", ""]
# 进入主程序时，如果需要修改图片大小，则使用此全局变量，默认为 6, 4
FIGURE_SIZE = (6, 4)
# 进入主程序时，用来判断是否开启 y=0 轴，默认为 auto
IS_ZERO = "auto"
# 进入主程序时，用来判断是否显示图例，默认为 auto
IS_LEGEND = "auto"
# 进入主程序时，如果需要修改保存图片的格式，则使用此全局变量，默认为 png
SAVE_FORMAT = "png"
# 进入主程序时，如果需要修改保存图片的 dpi，则使用此全局变量，默认为 300
DPI = 300


class Version:
    """
    用于记录版本信息和一些内容的类
    """

    def __init__(self):
        # 获取文件最后修改时间戳
        # 获取当前文件的绝对路径
        file_path = os.path.abspath(__file__)
        # 获取最后修改时间的时间戳
        timestamp = os.path.getmtime(file_path)
        self.developer = "Kimariyb, Ryan Hsiun"
        self.version = "2.5.1.1"
        self.release_date = str(datetime.fromtimestamp(timestamp).strftime("%b-%d-%Y"))
        self.address = "XiaMen University, School of Electronic Science and Engineering"
        self.website = "https://github.com/kimariyb/kimariDraw"


# 全局的 Version 对象
VERSION = Version()


class Spectrum:
    """
    用于记录光谱各种属性的类
    """

    def __init__(self, x_limit=None, y_limit=None, x_label=None, y_label=None, title=None, font_family=None,
                 font_size=None, figure_size=None, line_style=None, colors=None, legend_text=None, is_legend=None,
                 is_zero=None, data=None):
        """
        初始化 Spectrum 类
        :param data: 绘制光谱所需要的数据，初始化时为 None。是一个 dataframe 对象
        :param x_limit: X 轴坐标的最小、最大值以及间距，例如 [0, 4000, 500]，默认为 auto
        :param y_limit: Y 轴坐标的最小、最大值以及间距，例如 [0, 3000, 1000]，默认为 auto
        :param x_label: X 轴标签，默认为空
        :param y_label: Y 轴标签，默认为空
        :param title: 标题，默认为空
        :param font_family: 字体，默认为 Arial
        :param font_size: 字号，可选择 large、medium、small，默认为 medium
        :param figure_size: 图片大小，默认为 (8, 5)
        :param line_style: 曲线格式，默认为直线 -，可选择 -，-- 等，也可以选择一个集合
        :param colors: 曲线的颜色，默认为 black，也可以选择一个集合，同时也可以选择内置的颜色主题
        :param legend_text: 图例文本，默认为空，也可以选择一个集合，或者一个字符串
        :param is_legend: 是否开启图例，可选择 auto，False，True，默认为 auto
        :param is_zero: 是否开启 y=0 轴，可选择 auto，False，True，默认为 auto
        """
        self.data = data
        # 得到 x 数据
        x_array = np.array(data.iloc[:, 0])
        self.x_limit = x_limit
        # 如果输入 auto 则直接使用 auto_lim 方法
        if self.x_limit == "auto":
            self.x_limit = auto_lim(np.max(x_array), np.min(x_array))
        # 得到 y 数据
        y_array = np.array((data.iloc[:, 1:]))
        self.y_limit = y_limit
        # 如果输入 auto 则直接使用 auto_lim 方法
        if self.y_limit == "auto":
            self.y_limit = auto_lim(np.max(y_array), np.min(y_array))
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.font_family = font_family
        self.font_size = font_size
        self.figure_size = figure_size
        self.line_style = line_style if isinstance(line_style, list) else [line_style]
        self.colors = colors if isinstance(colors, list) else [colors]
        self.legend_text = legend_text if isinstance(legend_text, list) else [legend_text]
        self.is_legend = is_legend
        # 根据数据自动判断是否开启 legend，如果有三列或以上的数据，就说明需要开启
        # 如果输入 auto 则直接调用该方法
        if self.is_legend == "auto":
            if self.data.shape[1] >= 3:
                self.is_legend = True
            else:
                self.is_legend = False
        self.is_zero = is_zero
        # 根据数据自动判断是否开启 y=0 轴，如果所有的 y 轴数据存在 <0 的数，则需要开启
        # 如果输入 auto 则直接调用该方法
        if self.is_zero == "auto":
            if (data.iloc[:, 1:].values < 0).any():
                self.is_zero = True
            else:
                self.is_zero = False

    def __str__(self):
        return f"Spectrum Object:\n" \
               f"  x_limit: {self.x_limit}\n" \
               f"  y_limit: {self.y_limit}\n" \
               f"  x_label: {self.x_label}\n" \
               f"  y_label: {self.y_label}\n" \
               f"  title: {self.title}\n" \
               f"  font_family: {self.font_family}\n" \
               f"  font_size: {self.font_size}\n" \
               f"  figure_size: {self.figure_size}\n" \
               f"  line_style: {self.line_style}\n" \
               f"  colors: {self.colors}\n" \
               f"  legend_text: {self.legend_text}\n" \
               f"  is_legend: {self.is_legend}\n" \
               f"  is_zero: {self.is_zero}\n" \
               f"  data:\n{self.data}\n"


def init_spectrum(file_path):
    """
    根据一个 Multiwfn 输出的 txt 文件或一个记载光谱数据的 excel 文件初始化光谱
    :return: Spectrum 对象
    :return: 同时返回一个 dataframe 对象
    """
    # 读取 Multiwfn 输出的 txt 文件或者一个记载光谱数据的 excel 文件
    file = Path(file_path)
    # 根据文件的后缀是否为 txt 或者 xlsx 判断
    if file.suffix == ".txt":
        # 如果是 Multiwfn 输出的 txt 文件，调用 Pandas 的 read_csv 方法读取
        data = pd.read_csv(file, delim_whitespace=True, header=None)
    elif file.suffix == ".xlsx":
        # 读取包含光谱数据的 Excel 文件，假设文件包含一个名为 Sheet1 的表格
        data = pd.read_excel(file, sheet_name=0, dtype={'column_name': float})
    else:
        # 文件格式不支持
        raise ValueError("Unsupported file format.")

    # 初始化 spectrum
    spectrum = Spectrum(x_limit=X_LIMIT, y_limit=Y_LIMIT, x_label=LABEL_TITLE[0], y_label=LABEL_TITLE[1],
                        title=LABEL_TITLE[2], font_family=FONT_FAMILY, font_size=FONT_SIZE, figure_size=FIGURE_SIZE,
                        line_style=None, colors=None, legend_text=None, is_legend=IS_LEGEND, is_zero=IS_ZERO,
                        data=data)

    return spectrum


def count_degree(estep, max_value, min_value, symmetrical=False):
    """
    求出期望的最大刻度和最小刻度，为 estep 的整数倍
    :param estep: 最佳期望的间隔
    :param max_value: 数据的最大值
    :param min_value: 数据的最小值
    :param symmetrical: 是否开启正负刻度
    :return:
    """
    # 最终效果是当 max/estep 属于 (-1,Infinity) 区间时，向上取 1 格，否则取 2 格。
    # 当 min/estep 属于 (-Infinity,1) 区间时，向下取 1 格，否则取 2 格。
    maxi = int(max_value / estep + 1) * estep
    mini = int(min_value / estep - 1) * estep
    # 如果 max 和 min 刚好在刻度线的话，则按照上面的逻辑会向上或向下多取一格
    if max_value == 0:
        maxi = 0
    if min_value == 0:
        mini = 0
    if symmetrical and maxi * mini <= 0:
        tm = max(abs(maxi), abs(mini))
        maxi = tm
        mini = -tm

    return maxi, mini


def auto_lim(max_value, min_value, is_deviation=False):
    """
    根据最大值和最小值，自动生成一个较为整齐的 xlim 或 ylim，lim 包括 x 或 y 轴的最大值，x 或 y 轴的最小值，
    以及 x 或 y 轴的刻度 locator
    :param max_value: x 或 y 数据的最大值
    :param min_value: x 或 y 数据的最小值
    :param is_deviation 是否允许误差，默认为 False
    :return: 返回一个 auto lim list [lim_min, lim_max, locator]
    """
    # 初始化一个理想的刻度间隔段数，即希望刻度区间有多少段
    split_number = 4
    # 初始化一个魔术数组
    magic_array = [2, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100]  # 计算出初始间隔 temp_gap 和缩放比例 multiple
    temp_gap = (max_value - min_value) / split_number
    # temp_gap 除以 magic_array 后刚刚处于魔数区间内，先求 multiple 的幂 10 指数，
    # 例如当 temp_gap 为 120，想要把 temp_gap 映射到魔数数组（即处理为 10 到 100 之间的数），则倍数为 10，即 10 的 1 次方。
    multiple = 10 ** (math.floor(math.log10(temp_gap) - 1))
    # 查找大于temp_gap / multiple的第一个魔术数字
    estep = next((val * multiple for val in magic_array if val > temp_gap / multiple), None)

    # 求出期望的最大刻度和最小刻度，为 estep 的整数倍
    maxi, mini = count_degree(estep, max_value, min_value)

    if not is_deviation:
        while True:
            temp_split_number = round((maxi - mini) / estep)
            # 根据条件判断更新最大值和最小值
            if (maxi == 0 or mini - min_value <= maxi - max_value) and temp_split_number < split_number:
                mini -= estep  # 更新最小值（向左移动）
            else:
                maxi += estep  # 更新最大值（向右移动）
            # 达到预期的分割数量，退出循环
            if temp_split_number == split_number:
                break
            if temp_split_number > split_number:
                # 查找当前魔术数字的索引
                magic_idx = next((i for i, val in enumerate(magic_array) if val * multiple == estep), None)
                # 如果索引存在且不是最后一个，更新 estep 和最大值最小值
                if magic_idx is not None and magic_idx < len(magic_array) - 1:
                    estep = magic_array[magic_idx + 1] * multiple  # 更新 estep（增加）
                    maxi, mini = count_degree(estep, max_value, min_value)  # 更新最大值和最小值
                else:
                    break
            else:
                # 查找当前魔术数字的索引
                magic_idx = next((i for i, val in enumerate(magic_array) if val * multiple == estep), None)
                # 如果索引存在且不是第一个，更新 estep 和最大值最小值
                if magic_idx is not None and magic_idx > 0:
                    estep = magic_array[magic_idx - 1] * multiple  # 更新 estep（减少）
                    maxi, mini = count_degree(estep, max_value, min_value)  # 更新最大值和最小值
                else:
                    break

    # 得到间距
    interval = (maxi - mini) / split_number

    lim = [mini, maxi, interval]

    return lim


def show_info(version_info: Version):
    """
    显示程序的基本信息、配置信息以及版权信息。
    """
    # 程序最后输出版本和基础信息
    print(f"KimariDraw --  A Python script that processes Multiwfn spectral data and plots various spectra.")
    print(f"Version: {version_info.version}, release date: {version_info.release_date}")
    print(f"Developer: {version_info.developer}")
    print(f"Address: {version_info.address}")
    print(f"KimariDraw home website: {version_info.website}\n")
    # 获取当前日期和时间
    now = datetime.now().strftime("%b-%d-%Y, 00:45:%S")
    # 程序结束后提示版权信息和问候语
    print(f"(Copyright © 2023 Kimariyb. Currently timeline: {now})\n")


def validate(toml_path):
    """
    判断输入的 toml 文件是否符合标准
    :param toml_path: toml 文件的路径
    """
    # 首先判断输入的是否为 toml 文件，如果不是，则抛出异常。并在屏幕上打印不支持该文件
    if not toml_path.endswith(".toml"):
        raise ValueError("Error: Unsupported file format. Only TOML files are supported.\n")

    # 判断输入的 toml 文件是否存在，如果不存在，则抛出异常。并在屏幕上打印未找到该文件
    if not os.path.isfile(toml_path):
        raise FileNotFoundError("Error: File not found.\n")


def select_file():
    """
    和用户交互式的选择需要输入的 toml 文件，并返回 toml 文件的路径
    如果直接写入 toml 文件的绝对路径，则直接返回 toml_path
    如果输入 Enter 则弹出 GUI 界面选择 toml 文件
    如果输入 q 则退出整个程序
    :return: toml_path
    """
    # 创建文件对话框
    dialog = wx.FileDialog(None, "Select toml file", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    while True:
        # 输入的文本
        input_str = input("Input toml file path, for example E:\\Hello\\World.toml\n"
                          "Hint: Press ENTER button directly can select file in a GUI window. "
                          "If you want to exit the program, simply type the letter \"q\" and press Enter.\n")
        # 如果输入为 "q"，则退出主程序
        if input_str.lower() == "q":
            print("The program has exited！")
            exit()
        # 对应与直接输入 Enter，如果输入 ENTER 则显示对话框，不会退出主程序
        if not input_str:
            # 弹出文件选择对话框
            if dialog.ShowModal() == wx.ID_CANCEL:
                # 如果没有选择文件，即选择取消，则打印提示信息，并回到 input_str 输入文本这里
                print("Hint: You did not select a file.\n")
                # 返回 None 表示未选择文件, 继续主循环
                continue
            input_path = dialog.GetPath()
            try:
                validate(input_path)
            except (ValueError, FileNotFoundError) as e:
                print(str(e))
                # 继续主循环
                continue
            print("Hint: Selected toml file path:", input_str)
            # 销毁对话框
            dialog.Destroy()
            # 返回 input_path
            return input_path
        # 对应直接填写文件路径
        else:
            # 对于直接输入了路径的情况，执行验证逻辑
            try:
                validate(input_str)
            except (ValueError, FileNotFoundError) as e:
                print(str(e))
                # 继续主循环
                continue
            print("Hint: Selected toml file path:", input_str)
            # 返回 input_str
            return input_str


def load_toml(toml_path):
    """
    读取 toml 文件，并将所有读取到的 spectrum 对象封装成一个集合
    :param toml_path: toml 文件路径
    :return: 返回一个 spectrum 对象
    """
    # 读取 toml 文件的内容
    with open(toml_path, 'r', encoding='utf-8') as file:
        toml_data = toml.load(file)
    # 获取文件配置列表
    file_path, legends, colors, styles = None, None, None, None
    # 如果不存在文件配置，默认为空列表
    toml_configs = toml_data.get('file', [])
    for file_config in toml_configs:
        # 获取文件路径
        file_path = file_config.get('path', '')
        # 获取图例文本列表
        legends = file_config.get('legend', [])
        # 获取曲线颜色列表
        colors = file_config.get('color', [])
        # 获取曲线格式列表
        styles = file_config.get('style', [])

    # 得到 spectrum 对象
    spectrum = init_spectrum(file_path)
    # 将 toml 文件中的 legends, colors 和 styles 赋值给 Spectrum 对象
    spectrum.legend_text = legends
    spectrum.colors = colors
    spectrum.line_style = styles

    return spectrum


def draw_spectrum(spectrum: Spectrum, is_show):
    """
    根据 spectrum 对象绘制光谱
    :param spectrum: 一个 spectrum 对象
    :param is_show: 是否显示图片
    """
    # 设置全局属性
    rc['font.name'] = spectrum.font_family
    rc['title.size'] = spectrum.font_size[2]
    rc['label.size'] = spectrum.font_size[1]
    rc['font.size'] = spectrum.font_size[0]
    rc['tick.width'] = 1.3
    rc['meta.width'] = 1.3
    rc['label.weight'] = 'bold'
    rc['tick.labelweight'] = 'bold'
    rc['ytick.major.size'] = 4.6
    rc['ytick.minor.size'] = 2.5
    rc['xtick.major.size'] = 4.6
    rc['xtick.minor.size'] = 2.5

    # 将 spectrum 中的 data 数据赋值给一个变量
    spectrum_data = spectrum.data
    # 得到图例的集合 legend_text
    legend_list = spectrum.legend_text
    # 得到颜色的集合 colors
    colors_list = spectrum.colors
    # 得到颜色的集合 colors
    style_list = spectrum.line_style
    # 声明一个画布对象和坐标轴对象
    fig, ax = pplt.subplots(figsize=spectrum.figure_size, span=True, share=True)
    # 根据 DataFrame 的数据绘制单子图的光谱图
    # 首先判断 DataFrame 对象所记载的是否为多曲线图
    if len(spectrum_data.columns) > 2:
        # 第一列作为 x 值，其他列作为 y 值
        x = spectrum_data.iloc[:, 0]
        y_columns = spectrum_data.columns[1:]
        # 如果 spectrum 记载的数据大于 2，则绘制多曲线图
        for column, legend, color, style in zip(y_columns, legend_list, colors_list, style_list):
            y = spectrum_data[column]
            # 绘制多曲线图
            ax.plot(x, y, label=legend, color=color, linestyle=style, linewidth=1.3)
    else:
        # 第一列作为 x 值，第二列作为 y 值
        x = spectrum_data.iloc[:, 0]
        y = spectrum_data.iloc[:, 1]
        # 否则绘制单曲线图
        ax.plot(x, y, labels=legend_list, color=colors_list, linestyle=style_list, linewidth=1.3)
    # 如果开启显示图例，则执行下面的代码
    if spectrum.is_legend:
        ax.legend(loc='best', ncols=1, fontweight='bold', fontsize=12.5, frame=False, bbox_to_anchor=(0.95, 0.96))
    # 如果开启显示 Zero 轴，则执行下面的代码
    if spectrum.is_zero:
        # 显示 Zero 轴
        ax.axhline(y=0, color='black', linewidth=1.25)
    # 设置 x 轴 y 轴标签
    fig.format(
        xlabel=spectrum.x_label, ylabel=spectrum.y_label, title=spectrum.title,
        grid=False, xlocator=spectrum.x_limit[2], ylocator=spectrum.y_limit[2],
        xlim=(spectrum.x_limit[0], spectrum.x_limit[1]), ylim=(spectrum.y_limit[0], spectrum.y_limit[1]),
        xminorlocator=(spectrum.x_limit[2] / 2), yminorlocator=(spectrum.y_limit[2] / 2)
    )
    # 如果 is_show = True，则调用 fig.show()
    if is_show:
        fig.show()

    return fig, ax


def save_figure(spectrum):
    """
    调用该方法可以保存当前设置下的图片
    :param spectrum: 一个 spectrum 对象
    """
    global DPI, SAVE_FORMAT
    # 根据 DPI 和 SAVE_FORMAT 保存图片
    # 文件名初始值
    file_name = f"figure.{SAVE_FORMAT}"
    i = 1
    # 首先检查当前路径是否存在以 figure.save_type 为文件名的文件
    while os.path.exists(file_name):
        # 文件名已存在，添加数字后缀
        file_name = f"figure{i}.{SAVE_FORMAT}"
        i += 1
    # 调用 draw_spectrum 方法
    fig, ax = draw_spectrum(spectrum, False)
    # 保存光谱图
    fig.savefig(file_name, dpi=DPI, bbox_inches="tight", pad_inches=0.2)
    print()
    print("The picture is successfully saved!")
    print()


def show_menu():
    """
    主程序页面，显示主程序，不包括实现逻辑
    """
    print(" \"q\": Exit program gracefully\t \"r\": Load a new file")
    print("********************************************************")
    print("****************** Main function menu ******************")
    print("********************************************************")
    print(f"-1 Set font family of the spectrum, current: {FONT_FAMILY}")
    print(f"-2 Set font size of the spectrum, current: {FONT_SIZE}")
    print("-3 Set title/xlabel/ylabel of the spectrum")
    print(f"-4 Set format of saving spectrum file, current: {SAVE_FORMAT}")
    print(f"-5 Set dpi of saving spectrum, current: {DPI}")
    print(f"-6 Set figure size of spectrum file, current: {FIGURE_SIZE}")
    print("0 Plot spectrum!")
    print("1 Save graphical file of the spectrum in current folder")
    print(f"2 Set lower and upper limit of X-axis, current: {X_LIMIT}")
    print(f"3 Set lower and upper limit of Y-axis, current: {Y_LIMIT}")
    print(f"4 Showing legend text, current: {IS_LEGEND}")
    print(f"5 Showing the zero axis, current: {IS_ZERO}")


def set_xlim(spectrum):
    """
    修改全局变量 X_LIMIT，已达到开启图例的目的
    :param spectrum: 一个 spectrum 对象
    """
    global X_LIMIT
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    x_choice = input("Please input lower and upper limit of X-axis, eg. 150, 300, 50\n")
    if x_choice.lower() == "r":
        return
    # 将输入的字符串值修改成一个集合对象
    X_LIMIT = list(map(float, x_choice.split(',')))
    # 将全局变量的值赋值给 spectrum 对象
    spectrum.x_limit = X_LIMIT

    print("Setting successful!\n")


def set_ylim(spectrum):
    """
    修改全局变量 Y_LIMIT，已达到开启图例的目的
    :param spectrum: 一个 spectrum 对象
    """
    global Y_LIMIT
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    y_choice = input("Please input lower and upper limit of Y-axis, eg. 0, 3000, 1000\n")
    if y_choice.lower() == "r":
        return
    # 将输入的字符串值修改成一个集合对象
    Y_LIMIT = list(map(float, y_choice.split(',')))
    # 将全局变量的值赋值给 spectrum 对象
    spectrum.y_limit = Y_LIMIT

    print("Setting successful!\n")


def set_legend(spectrum):
    """
    修改全局变量 IS_LEGEND，已达到开启图例的目的
    :param spectrum: 一个 spectrum 对象
    """
    global IS_LEGEND
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    print("0 Turn off showing the legend")
    print("1 Turn on showing the legend")
    legend_choice = input("Please enter the option of your choice:\n")
    if legend_choice.lower() == "r":
        return
    elif legend_choice == "0":
        IS_LEGEND = False
    elif legend_choice == "1":
        IS_LEGEND = True
    else:
        print("Invalid input. Please press the Enter button and make a valid selection.")
        input("Press Enter to continue...\n")
    # 将全局变量的值赋值给 spectrum 对象
    spectrum.is_legend = IS_LEGEND

    print("Setting successful!\n")


def set_zero(spectrum):
    """
    修改全局变量 IS_ZERO，已达到开启绘制 y=0 轴的目的
    :param spectrum: 一个 spectrum 对象
    """
    global IS_ZERO
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    print("0 Turn off drawing of the zero axis")
    print("1 Turn on drawing of the zero axis")
    zero_choice = input("Please enter the option of your choice:\n")
    if zero_choice.lower() == "r":
        return
    elif zero_choice == "0":
        IS_ZERO = False
    elif zero_choice == "1":
        IS_ZERO = True
    else:
        print("Invalid input. Please press the Enter button and make a valid selection.")
        input("Press Enter to continue...\n")
    # 将全局变量的值赋值给 spectrum 对象
    spectrum.is_zero = IS_ZERO

    print("Setting successful!\n")


def set_figure_size(spectrum):
    """
    修改全局变量 FIGURE_SIZE，已达到修改图片大小的目的
    :param spectrum: 一个 spectrum 对象
    """
    global FIGURE_SIZE
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    size_choice = input("Please input figure size of spectrum file, eg. 8, 5\n")
    if size_choice.lower() == "r":
        return
    # 将输入的字符串值修改成一个元组对象
    FIGURE_SIZE = tuple(map(float, size_choice.split(',')))
    # 将全局变量的值赋值给 spectrum 对象
    spectrum.figure_size = FIGURE_SIZE

    print("Setting successful!\n")


def set_dpi():
    """
    修改全局变量 DPI，已达到修改保存图片的 dpi 的目的
    """
    # 声明全局变量
    global DPI
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    DPI = input("Please input dpi of saving spectrum, eg. 300\n")
    if DPI.lower() == "r":
        return

    print("Setting successful!\n")


def set_save_format():
    """
    修改全局变量 SAVE_FORMAT，已达到修改保存图片的格式目的
    """
    # 声明全局变量
    global SAVE_FORMAT
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    SAVE_FORMAT = input("Please input format of saving spectrum file, eg. png\n")
    if SAVE_FORMAT.lower() == "r":
        return

    print("Setting successful!\n")


def set_title_label(spectrum):
    """
    修改全局变量 LABEL_TITLE，已达到修改 xlabel 、ylabel 和 title 的目的
    :param spectrum: 一个 spectrum 对象
    """
    # 声明全局变量
    global LABEL_TITLE
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    print("0 Set the xlabel of the spectrum")
    print("1 Set the ylabel of the spectrum")
    print("2 Set the title of the spectrum")
    label_choice = input("Please enter the option of your choice: \n")
    if label_choice.lower() == "r":
        return
    elif label_choice == "0":
        LABEL_TITLE[0] = input("Please input the xlabel of the spectrum: \n")
        # 将全局变量的值赋值给 spectrum 对象
        spectrum.x_label = LABEL_TITLE[0]
    elif label_choice == "1":
        LABEL_TITLE[1] = input("Please input the ylabel of the spectrum: \n")
        # 将全局变量的值赋值给 spectrum 对象
        spectrum.y_label = LABEL_TITLE[1]
    elif label_choice == "2":
        LABEL_TITLE[2] = input("Please input the title of the spectrum: \n")
        # 将全局变量的值赋值给 spectrum 对象
        spectrum.title = LABEL_TITLE[2]
    else:
        print("Invalid input. Please press the Enter button and make a valid selection.")
        input("Press Enter to continue...\n")
    print("Setting successful!\n")


def set_font_name(spectrum):
    """
    修改全局变量 FONT_FAMILY，已达到修改字体的目的
    :param spectrum: 一个 spectrum 对象
    """
    # 声明全局变量
    global FONT_FAMILY
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    FONT_FAMILY = input("Please input the font family that you want to set: \n")
    if FONT_FAMILY.lower() == "r":
        return
    # 将全局变量的值赋值给 spectrum 对象
    spectrum.font_family = FONT_FAMILY
    print("Setting successful!\n")


def set_font_size(spectrum):
    """
    修改全局变量 FONT_SIZE，已达到修改字号的目的
    :param spectrum: 一个 spectrum 对象
    """
    # 声明全局变量
    global FONT_SIZE
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    FONT_SIZE = input("Please input the font size that you want to set: \n")
    if FONT_SIZE.lower() == "r":
        return
    # 将全局变量的值赋值给 spectrum 对象
    spectrum.font_size = FONT_SIZE
    print("Setting successful!\n")


def main_menu(toml_file):
    """
    展示主页面菜单，同时实现了主页面菜单 show_menu() 中提到的逻辑
    :param toml_file: 需要读取的 toml 文件
    """
    # 读取 toml 文件，并且得到 toml 记载的 txt 文件数据，并且生成 spectrum 对象
    spectrum = load_toml(toml_file)
    while True:
        # 显示主页面，如果不输入 q，则一直在主程序中
        show_menu()
        # 接受用户的指令，并根据用户的指令
        choice = input()
        # 如果输入 0，则按照当前参数绘制 Spectrum，调用 draw_spectrum() 方法
        if choice == "0":
            draw_spectrum(spectrum, True)
            continue
        # 如果输入 1，按照当前参数绘制的 Spectrum 保存图片，调用 save_figure() 方法
        elif choice == "1":
            save_figure(spectrum)
        # 如果输入 2，调用 set_xlim 方法修改 xlim
        elif choice == "2":
            set_xlim(spectrum)
        # 如果输入 3，调用 set_ylim 方法修改 ylim
        elif choice == "3":
            set_ylim(spectrum)
        # 如果输入 4，是否显示图例文本
        elif choice == "4":
            set_legend(spectrum)
        # 如果输入 5，是否开启 zero 轴
        elif choice == "5":
            set_zero(spectrum)
        # 如果输入 -1，设置绘制光谱的字体
        elif choice == "-1":
            set_font_name(spectrum)
        # 如果输入 -2，设置绘制光谱的字号
        elif choice == "-2":
            set_font_size(spectrum)
        # 如果输入 -3，设置 title、xlabel、ylabel
        elif choice == "-3":
            set_title_label(spectrum)
        # 如果输入 -4，设置保存图片的格式
        elif choice == "-4":
            set_save_format()
        # 如果输入 -5，设置保存图片的 dpi
        elif choice == "-5":
            set_dpi()
        # 如果输入 -6，设置图片的大小
        elif choice == "-6":
            set_figure_size(spectrum)
        # 如果输入 q 则退出程序
        elif choice.lower() == "q":
            print()
            print("The program has already terminated!")
            print("Thank you for your using! Have a good time!")
            exit()
        # 如果输入 r 则重新加载一个新的 toml 文件
        elif choice.lower() == "r":
            toml_file = select_file()
            spectrum = load_toml(toml_file)
            continue
        # 如果输入的内容不符合要求，提示按下空格重新选择。
        else:
            print()
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")


def main():
    # 展示开始界面
    show_info(VERSION)
    # 创建一个 wxPython 应用程序对象
    app = wx.App()
    # 选择需要解析的 toml 文件路径
    selected_file = select_file()
    # 进入主程序
    main_menu(selected_file)


