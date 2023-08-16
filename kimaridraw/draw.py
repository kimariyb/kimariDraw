import math
import os
from datetime import datetime
from pathlib import Path

import wx
import numpy as np
import pandas as pd

# 全局的字号大小，分别对应 large、medium 以及 small
LARGE_FONTSIZE = []
MEDIUM_FONTSIZE = []
SMALL_FONTSIZE = []


# 全局的颜色主题

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

    def __init__(self, x_limit, y_limit, x_label, y_label, title, font_family, font_size, figure_size, line_style,
                 colors, legend_text, is_legend, is_zero):
        """
        初始化 Spectrum 类
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
        self.x_limit = x_limit
        self.y_limit = y_limit
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
        self.is_zero = is_zero


def init_spectrum(file_path):
    """
    根据一个 Multiwfn 输出的 txt 文件或一个记载光谱数据的 excel 文件初始化光谱
    :return: Spectrum 对象
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
    # 根据第一列的最大值和最小值设定 xlim
    x_array = np.array(data.iloc[:, 0])
    x_max = np.max(x_array)
    x_min = np.min(x_array)
    # 得到 x 的最大值和最小值之后，程序自动设定 xlim
    init_xlim = auto_lim(x_max, x_min)
    # 根据 1~n 列的数据的最大值和最小值设定 ylim
    y_array = np.array((data.iloc[:, 1:]))
    y_max = np.max(y_array)
    y_min = np.min(y_array)
    init_ylim = auto_lim(y_max, y_min)
    # 根据数据自动判断是否开启 legend，如果有三列或以上的数据，就说明需要开启
    if data.shape[1] >= 3:
        auto_legend = True
    else:
        auto_legend = False
    # 根据数据自动判断是否开启 y=0 轴，如果所有的 y 轴数据存在 <0 的数，则需要开启
    if (data.iloc[:, 1:].values < 0).any():
        auto_zero = True
    else:
        auto_zero = False

    spectrum = Spectrum(x_limit=init_xlim, y_limit=init_ylim, x_label="", y_label="", title="", font_family="Arial",
                        font_size=MEDIUM_FONTSIZE, figure_size=(8, 5), line_style="-", colors="black", legend_text="",
                        is_legend=auto_legend, is_zero=auto_zero)

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

    def fixed_num(num):
        if '.' in str(num):
            num = round(float(num), 8)
        return num

    # 设置精度
    maxi = fixed_num(maxi)
    mini = fixed_num(mini)
    interval = fixed_num((maxi - mini) / split_number)

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


def main():
    """
    :param is_sup: 是否开启子图模式
    :param is_serial: 是否显示子图序号
    :param sup_layout: 子图的排版
    """

    # 展示开始界面
    show_info(VERSION)
    # 创建一个 wxPython 应用程序对象
    app = wx.App()
    # 创建文件对话框
    dialog = wx.FileDialog(None, "打开文件", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

    while True:
        # 输入的文本
        input_str = input("Input toml file path, for example E:\\Hello\\World.toml\n"
                          "Hint: Press ENTER button directly can select file in a GUI window.\n")

        # 对应与直接输入 Enter，如果输入 ENTER 则显示对话框，不会推出主程序
        if not input_str:
            # 弹出文件选择对话框
            if dialog.ShowModal() == wx.ID_CANCEL:
                # 如果没有选择文件，即选择取消，则打印提示信息，并回到 input_str 输入文本这里
                print("Hint: You did not select a file.\n")
                # 返回 None 表示未选择文件, 继续主循环
                continue
            toml_path = dialog.GetPath()
            # 检验是否符合要求
            try:
                validate(toml_path)
            except (ValueError, FileNotFoundError) as e:
                print(str(e))
                # 继续主循环
                continue
            print("Hint: Selected toml file path:", toml_path)
            # 销毁对话框
            dialog.Destroy()
            # 返回 toml_path
            break
        # 对应直接填写文件路径
        else:
            # 对于直接输入了路径的情况，执行验证逻辑
            toml_path = input_str
            try:
                validate(toml_path)
            except (ValueError, FileNotFoundError) as e:
                print(str(e))
                # 继续主循环
                continue
            # 在这里可以使用 toml_path 进行后续操作
            print("Hint: Selected toml file path:", toml_path)
            # 返回 toml_path
            break


if __name__ == '__main__':
    main()