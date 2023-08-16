import math
import os
from datetime import datetime
from pathlib import Path

import toml
import wx
import numpy as np
import pandas as pd

# 全局变量设定
# 进入主程序时，如果需要修改字号，则使用此全局变量
FONT_SIZE = []
# 进入主程序时，如果需要修改字体，则使用此全局变量
FONT_FAMILY = "Arial"
# 进入主程序时，如果需要修改颜色主题，则使用此全局变量
COLOR_THEME = "black"
# 进入主程序时，如果需要修改曲线格式，则使用此全局变量
LINE_STYLE = "-"
# 进入主程序时，如果需要修改 x_limit，则使用此全局变量，默认为 auto
X_LIMIT = "auto"
# 进入主程序时，如果需要修改 y_limit，则使用此全局变量，默认为 auto
Y_LIMIT = "auto"
# 进入主程序时，如果需要修改 x_label, y_label, title, 则使用此全局变量，默认为空
LABEL_TITLE = ["", "", ""]
# 进入主程序时，如果需要修改图片大小，则使用此全局变量，默认为 8, 5
FIGURE_SIZE = (8, 5)
# 进入主程序时，用来判断是否开启 y=0 轴，默认为 auto
IS_ZERO = "auto"
# 进入主程序时，用来判断是否显示图例，默认为 auto
IS_LEGEND = "auto"
# 进入主程序时，用来判断是否开启多子图，默认为 auto
IS_SUP = "auto"
# 进入主程序时，用来判断是否显示多子图序号，默认为 True
IS_SERIA = True
# 进入主程序时，如果需要修改多子图的排版，则使用此全局变量，默认为 auto
SUP_LAYOUT = "auto"
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
        timestamp = os.path.getmtime("./draw.py")
        self.developer = "Kimariyb, Ryan Hsiun"
        self.version = "2.5.0"
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
                        line_style=LINE_STYLE, colors=COLOR_THEME, legend_text="", is_legend=IS_LEGEND, is_zero=IS_ZERO,
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
    if symmetrical and maxi * mini < 0:
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
    split_number = 5
    # 初始化一个魔术数组
    magic_array = np.array([10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    # 计算出初始间隔 temp_gap 和缩放比例 multiple
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
    :return: spectrum list
    """
    # 新建一个 spectrum list
    spectrum_list = []
    # 读取 toml 文件的内容
    with open(toml_path, 'r', encoding='utf-8') as file:
        toml_data = toml.load(file)
    # 获取文件配置列表
    toml_configs = toml_data.get('file', [])  # 如果不存在文件配置，默认为空列表
    # 遍历文件配置，
    for file_config in toml_configs:
        # 获取文件路径
        file_path = file_config.get('path', '')
        # 获取图例文本列表
        legends = file_config.get('legend', [])
        # 获取曲线颜色列表
        colors = file_config.get('color', [])
        # 获取曲线格式列表
        styles = file_config.get('style', [])
        # 每遍历一次，就得到一个 Spectrum 对象，将所有得到的 Spectrum 对象放置在一个 list 中
        spectrum = init_spectrum(file_path)
        # 如果 legends, colors, styles 不为空或者空集合，则将得到的配置赋值给 Spectrum 对象
        if legends:
            spectrum.legend_text = legends
        if colors:
            spectrum.colors = colors
        if styles:
            spectrum.line_style = styles
        # 每读取一个就在 list 中追加一个 spectrum
        spectrum_list.append(spectrum)

    return spectrum_list


def draw_multiple(spectrum_list, sup_layout, is_serial=True):
    """
    根据 spectrum list 绘制多子图的光谱
    :param spectrum_list: 由 spectrum 组合成的集合
    :param is_serial: 是否显示子图序号
    :param sup_layout: 子图的排版
    """
    pass


def draw_single(spectrum_list):
    """
    根据 spectrum list 绘制单子图的光谱
    :param spectrum_list: 由 spectrum 组合成的集合
    """
    pass


def draw_spectrum(spectrum_list, is_sup=False):
    """
    根据 spectrum list 绘制光谱
    :param spectrum_list: 由 spectrum 组合成的集合
    :param is_sup: 是否开启子图模式，默认不开启，即为 False
    """
    # 如果开启多子图绘制，也就是 is_sup = True 调用 draw_multiple()
    if is_sup:
        draw_multiple(spectrum_list, sup_layout=None)
    # 如果不开启多子图绘制，也就是 is_sup = False 调用 draw_single()
    else:
        draw_single(spectrum_list)


def main_view():
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
    print(f"-4 Set layout of the subplots, current: {SUP_LAYOUT}")
    print(f"-5 Set format of saving spectrum file, current: {SAVE_FORMAT}")
    print(f"-6 Set dpi of saving spectrum, current: {DPI}")
    print(f"-7 Set figure size of spectrum file, current: {FIGURE_SIZE}")
    print("0 Plot spectrum!")
    print("1 Save graphical file of the spectrum in current folder")
    print(f"2 Set lower and upper limit of X-axis, current: {X_LIMIT}")
    print(f"3 Set lower and upper limit of Y-axis, current: {Y_LIMIT}")
    print("4 Set color theme of curve lines")
    print("5 Set style of curve lines")
    print(f"6 Showing legend text, current: {IS_LEGEND}")
    print(f"7 Showing the subplots, current: {IS_SUP}")
    print(f"8 Showing the zero axis, current: {IS_ZERO}")


def set_sup_layout(spectrum_list):
    """
    修改全局变量 SUP_LAYOUT，已达到修改多子图排版的目的
    :param spectrum_list: 一个装有 spectrum 对象的 spectrum_list
    """
    # 声明全局变量
    global SUP_LAYOUT
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    SUP_LAYOUT = input("Please input layout of the subplots: \n")
    if SUP_LAYOUT.lower() == "r":
        return

    print("Setting successful!\n")


def set_title_label(spectrum_list):
    """
    修改全局变量 LABEL_TITLE，已达到修改 xlabel 、ylabel 和 title 的目的
    :param spectrum_list: 一个装有 spectrum 对象的 spectrum_list
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
        # 遍历 list 中所有的 spectrum 对象
        for spectrum in spectrum_list:
            # 将全局变量的值赋值给 spectrum 对象
            spectrum.x_label = LABEL_TITLE[0]
    elif label_choice == "1":
        LABEL_TITLE[1] = input("Please input the ylabel of the spectrum: \n")
        # 遍历 list 中所有的 spectrum 对象
        for spectrum in spectrum_list:
            # 将全局变量的值赋值给 spectrum 对象
            spectrum.y_label = LABEL_TITLE[1]
    elif label_choice == "2":
        LABEL_TITLE[2] = input("Please input the title of the spectrum: \n")
        # 遍历 list 中所有的 spectrum 对象
        for spectrum in spectrum_list:
            # 将全局变量的值赋值给 spectrum 对象
            spectrum.title = LABEL_TITLE[2]
    else:
        print("Invalid input. Please press the Enter button and make a valid selection.")
        input("Press Enter to continue...\n")
    print("Setting successful!\n")


def set_font_name(spectrum_list):
    """
    修改全局变量 FONT_FAMILY，已达到修改字体的目的
    :param spectrum_list: 一个装有 spectrum 对象的 spectrum_list
    """
    # 声明全局变量
    global FONT_FAMILY
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    FONT_FAMILY = input("Please input the font family that you want to set: \n")
    if FONT_FAMILY.lower() == "r":
        return
    # 遍历 list 中所有的 spectrum 对象
    for spectrum in spectrum_list:
        # 将全局变量的值赋值给 spectrum 对象
        spectrum.font_family = FONT_FAMILY
    print("Setting successful!\n")


def set_font_size(spectrum_list):
    """
    修改全局变量 FONT_SIZE，已达到修改字号的目的
    :param spectrum_list: 一个装有 spectrum 对象的 spectrum_list
    """
    # 声明全局变量
    global FONT_SIZE
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    FONT_SIZE = input("Please input the font size that you want to set: \n")
    if FONT_SIZE.lower() == "r":
        return
    # 遍历 list 中所有的 spectrum 对象
    for spectrum in spectrum_list:
        # 将全局变量的值赋值给 spectrum 对象
        spectrum.font_size = FONT_SIZE
    print("Setting successful!\n")


def main_function(toml_file):
    """
    实现主程序 mian_view() 的逻辑
    :param toml_file: 需要读取的 toml 文件
    """
    # 读取 toml 文件，并且得到 toml 记载的 txt 文件数据，并且生成 spectrum 组成的 list
    spectrum_list = load_toml(toml_file)
    while True:
        # 显示主页面，如果不输入 q，则一直在主程序中
        main_view()
        # 接受用户的指令，并根据用户的指令
        choice = input()
        # 如果输入 0，则按照当前参数绘制 Spectrum，调用 draw_spectrum() 方法
        if choice == 0:
            pass
        # 如果输入 1，按照当前参数绘制的 Spectrum 保存图片，调用 save_figure() 方法
        elif choice == 1:
            pass
        # 如果输入 2，调用 set_xlim 方法修改 xlim
        elif choice == 2:
            pass
        # 如果输入 3，调用 set_ylim 方法修改 ylim
        elif choice == 3:
            pass
        # 如果输入 4，修改曲线的颜色主题
        elif choice == 4:
            pass
        # 如果输入 5，修改曲线的颜色风格
        elif choice == 5:
            pass
        # 如果输入 6，是否显示图例文本
        elif choice == 6:
            pass
        # 如果输入 7，是否开启多子图
        elif choice == 7:
            pass
        # 如果输入 8，是否开启 zero 轴
        elif choice == 8:
            pass
        # 如果输入 -1，设置绘制光谱的字体
        elif choice == "-1":
            set_font_name(spectrum_list)
        # 如果输入 -2，设置绘制光谱的字号
        elif choice == "-2":
            set_font_size(spectrum_list)
        # 如果输入 -3，设置 title、xlabel、ylabel
        elif choice == -3:
            set_title_label(spectrum_list)
        # 如果输入 -4，设置子图的排版
        elif choice == -4:
            set_sup_layout()
        # 如果输入 -5，设置保存图片的格式
        elif choice == -5:
            pass
        # 如果输入 -6，设置保存图片的 dpi
        elif choice == -6:
            pass
        # 如果输入 -7，设置图片的大小
        elif choice == -7:
            pass
        # 如果输入 q 则退出程序
        elif choice.lower() == "q":
            print("Thank you for your using! Have a good time!")
            exit()
        # 如果输入 r 则重新加载一个新的 toml 文件
        elif choice.lower() == "r":
            pass
        # 如果输入的内容不符合要求，提示按下空格重新选择。
        else:
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
    main_function(selected_file)


if __name__ == '__main__':
    main_function("multiple.toml")
