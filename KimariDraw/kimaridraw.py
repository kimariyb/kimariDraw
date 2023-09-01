# -*- coding: utf-8 -*-
"""
kimaridraw.py
Briefly describe the functionality and purpose of the file.

This is a Main function file!

This file is part of KimariDraw.
KimariDraw is a Python script that processes Multiwfn spectral data and plots various spectra.

@author:
Kimariyb (kimariyb@163.com)

@license:
Licensed under the MIT License.
For details, see the LICENSE file.

@Data:
2023-09-01
"""
import argparse
import sys
import wx
import math
import os

import numpy as np
import pandas as pd
import proplot as pplt
import toml

from datetime import datetime
from pathlib import Path
from proplot import rc

# 获取当前文件被修改的最后一次时间
time_last = os.path.getmtime(os.path.abspath(__file__))
# 全局的静态变量
__version__ = "2.5.2.2"
__developer__ = "Kimariyb, Ryan Hsiun"
__address__ = "XiaMen University, School of Electronic Science and Engineering"
__website__ = "https://github.com/kimariyb/kimariDraw"
__release__ = str(datetime.fromtimestamp(time_last).strftime("%b-%d-%Y"))


class Spectrum:
    """
    用于记录光谱各种属性的类

    Attributes:
        x_limit (list[float, float, float]): x 轴的刻度，最小值、最大值以及间距
        left_y_limit (list[float, float, float]): 左 y 轴的刻度，最小值、最大值以及间距
        right_y_limit (list[float, float, float]): 右 y 轴的刻度，最小值、最大值以及间距
        x_label (str): x 轴的标签
        left_y_label (str): y 轴标签，左 y 轴标签
        right_y_label (str): y 轴标签，右 y 轴标签
        title (str): 标题
        font_family (str): 字体家族
        font_size (list[float, float, float]): 字体字号，常规字号、标签字号以及标题字号
        figure_size (tuple[float, float]): 图像大小，宽度和高度
        curve_style (str or list[str]): 曲线样式主题，可以是单个字符串或字符串列表
        curve_colors (str or list[str]): 曲线颜色主题，可以是单个字符串或字符串列表
        line_colors (str or list[str]): 直线颜色主题，可以是单个字符串或字符串列表
        legend_text (str or list[str]): 图例文本，可以是单个字符串或字符串列表
        is_legend (bool): 是否开启图例
        is_zero (bool): 是否显示零坐标轴
        is_showLine (bool): 是否显示直线，如果 Spectrum.lineData != None，则为 True
        save_format (str): 保存光谱的格式，如 png, jpg, svg 等
        save_dpi (float): 保存光谱的分辨率 dpi
        lineData (DataFrame): 直线数据
        curveData (DataFrame): 曲线数据
    """

    def __init__(self, **kwargs):
        # 构造函数逻辑
        # 曲线数据 DataFrame，必须传入的参数
        self.curveData = kwargs.get('curveData')
        # 直线数据 DataFrame
        self.lineData = kwargs.get('lineData')

        # 拿到 curveData x 数据和 left_y 数据
        x_array = np.array(self.curveData.iloc[:, 0])
        left_y_array = np.array((self.curveData.iloc[:, 1:]))

        # x 轴的标签 string，默认为 x label，可以为 None
        self.x_label = kwargs.get('x_label', 'X Label')

        # 左 y 轴标签 string，可以为 None
        self.left_y_label = kwargs.get('left_y_label', 'Left Label')

        # 右 y 轴标签 string，可以为 None
        self.right_y_label = kwargs.get('right_y_label', 'Right Label')

        # 标题 string，默认为 title，可以为 None
        self.title = kwargs.get('title', 'Title')

        # 判断 lineData 是否存在，如果不为 None
        if self.lineData is not None:
            right_y_array = np.array((self.lineData.iloc[:, 1:]))
            # 右 y 轴的刻度，最小值、最大值以及间距，必须为 list[float, float, float]，默认为 'auto'
            self.right_y_limit = kwargs.get('right_y_limit', 'auto')
            # 如果为 auto，则调用 auto_lim() 方法自动生成 right_y_limit
            if self.right_y_limit == 'auto':
                self.right_y_limit = auto_lim(np.max(right_y_array), np.min(right_y_array))
            if self.right_y_limit != 'auto' and (
                    not isinstance(self.right_y_limit, list) or len(self.right_y_limit) != 3):
                raise ValueError("right_y_limit must be a list of three floats [min, max, step]")
        else:
            # 如果 lineData 为 None，则将 line 有关的属性全设为 None
            self.right_y_label = None
            self.right_y_limit = None

        # x 轴的刻度，最小值、最大值以及间距，必须为 list[float, float, float]，默认为 'auto'
        self.x_limit = kwargs.get('x_limit', 'auto')
        # 如果为 auto，则调用 auto_lim() 方法自动生成 x_limit
        if self.x_limit == 'auto':
            self.x_limit = auto_lim(np.max(x_array), np.min(x_array))
        if self.x_limit != 'auto' and (not isinstance(self.x_limit, list) or len(self.x_limit) != 3):
            raise ValueError("x_limit must be a list of three floats [min, max, step]")

        # 左 y 轴的刻度，最小值、最大值以及间距，必须为 list[float, float, float]，默认为 'auto'
        self.left_y_limit = kwargs.get('left_y_limit', 'auto')
        # 如果为 auto，则调用 auto_lim() 方法自动生成 left_y_limit
        if self.left_y_limit == 'auto':
            self.left_y_limit = auto_lim(np.max(left_y_array), np.min(left_y_array))
        if self.left_y_limit != 'auto' and (not isinstance(self.left_y_limit, list) or len(self.left_y_limit) != 3):
            raise ValueError("left_y_limit must be a list of three floats [min, max, step]")

        # 字体家族 string，默认为 Arial
        self.font_family = kwargs.get('font_family', 'Arial')

        # 字体字号，常规字号、标签字号以及标题字号，必须为 list[float, float, float]，默认为 [10.5, 12, 14]
        self.font_size = kwargs.get('font_size', [10.5, 12, 14])
        if self.font_size is not None and (not isinstance(self.font_size, list) or len(self.font_size) != 3):
            raise ValueError("font_size must be a list of three floats [regular_size, label_size, title_size]")

        # 图像大小，必须为 tuple(float, float)，默认为 (6, 5)
        self.figure_size = kwargs.get('figure_size', (6, 5))
        if self.figure_size is not None and (not isinstance(self.figure_size, tuple) or len(self.figure_size) != 2):
            raise ValueError("figure_size must be a tuple of two floats (width, height)")

        # 曲线样式主题 string，也可以是一个 list[string...]，默认为 -
        curve_style = kwargs.get('curve_style', ['-'])
        if isinstance(curve_style, str):
            self.curve_style = [curve_style]
        elif isinstance(curve_style, list):
            self.curve_style = curve_style
        else:
            self.curve_style = None

        # 曲线颜色主题 string，也可以是一个 list[string...]，默认为 red
        curve_colors = kwargs.get('curve_colors', ['red'])
        if isinstance(curve_colors, str):
            self.curve_colors = [curve_colors]
        elif isinstance(curve_colors, list):
            self.curve_colors = curve_colors
        else:
            self.curve_colors = None

        # 直线颜色主题 string, 也可以是一个 list[string...]，默认为 black
        line_colors = kwargs.get('line_colors', ['black'])
        if isinstance(line_colors, str):
            self.line_colors = [line_colors]
        elif isinstance(line_colors, list):
            self.line_colors = line_colors
        else:
            self.line_colors = None

        # 图例文本 string，也可以是一个 list[string...]，默认为 None
        legend_text = kwargs.get('legend_text', None)
        if isinstance(legend_text, str):
            self.legend_text = [legend_text]
        elif isinstance(legend_text, list):
            self.legend_text = legend_text
        else:
            self.legend_text = None

        # 是否开启图例 bool，根据 curveData 自动判断
        if self.curveData.shape[1] >= 3:
            self.is_legend = kwargs.get('is_legend', True)
        else:
            self.is_legend = kwargs.get('is_legend', False)

        # 是否显示零坐标轴 bool，根据 curveData 自动判断
        if (self.curveData.iloc[:, 1:].values < 0).any():
            self.is_zero = kwargs.get('is_zero', True)
        else:
            self.is_zero = kwargs.get('is_zero', False)

        # 是否显示直线 bool，根据 lineData 是否为 None 判断
        if self.lineData is not None:
            self.is_showLine = kwargs.get('is_showLine', True)
        else:
            self.is_showLine = kwargs.get('is_showLine', False)

        # 保存光谱的格式 string，分别可以为 png, jpg, svg ...，默认为 png
        self.save_format = kwargs.get('save_format', 'png')

        # 保存光谱的分辨率 dpi float，默认为 400
        self.save_dpi = kwargs.get('save_dpi', 400.0)

    def __str__(self):
        return f"Spectrum Object:\n" \
               f"  x_limit: {self.x_limit}\n" \
               f"  left_y_limit: {self.left_y_limit}\n" \
               f"  right_y_limit: {self.right_y_limit}\n" \
               f"  x_label: {self.x_label}\n" \
               f"  left_y_label: {self.left_y_label}\n" \
               f"  right_y_label: {self.right_y_label}\n" \
               f"  title: {self.title}\n" \
               f"  font_family: {self.font_family}\n" \
               f"  font_size: {self.font_size}\n" \
               f"  figure_size: {self.figure_size}\n" \
               f"  curve_style: {self.curve_style}\n" \
               f"  curve_colors: {self.curve_colors}\n" \
               f"  line_colors: {self.line_colors}\n" \
               f"  legend_text: {self.legend_text}\n" \
               f"  is_legend: {self.is_legend}\n" \
               f"  is_zero: {self.is_zero}\n" \
               f"  save_format: {self.save_format}\n" \
               f"  save_dpi: {self.save_dpi}\n" \
               f"  lineData: {self.lineData}\n" \
               f"  curveData: {self.curveData}\n"

    def draw_spectrum(self):
        """
        当实例化一个 Spectrum 对象后，就可以调用 draw_spectrum 方法绘制光谱

        Warnings:
            调用 draw_spectrum 时会自动保存光谱在当前文件夹下

        Examples:
            spectrum = init_spectrum(**kwargs)
            spectrum.draw_spectrum()

        Returns:
            None
        """
        # 设置全局属性，也就是图片的风格样式
        rc['font.family'] = self.font_family
        rc['title.size'] = self.font_size[2]
        rc['label.size'] = self.font_size[1]
        rc['font.size'] = self.font_size[0]
        rc['tick.width'] = 1.3
        rc['meta.width'] = 1.3
        rc['title.weight'] = 'bold'
        rc['title.pad'] = 10.0
        rc['axes.labelpad'] = 8.0
        rc['label.weight'] = 'bold'
        rc['tick.labelweight'] = 'bold'
        rc['ytick.major.size'] = 4.6
        rc['ytick.minor.size'] = 2.5
        rc['xtick.major.size'] = 4.6
        rc['xtick.minor.size'] = 2.5

        # 创建实例用于绘制光谱
        fig, ax = pplt.subplots(figsize=self.figure_size, share=False)

        # 如果 curveData 的列数比 2 大，则说明绘制的曲线不只一条
        if len(self.curveData.columns) > 2:

            # 绘制多曲线 curve，从 0 开始循环至 curveData 的列数
            for i in range(len(self.curveData.columns) - 1):
                # 第一列作为 x 值，其他列作为 y 值
                curve_x = self.curveData.iloc[:, 0]
                curve_y = self.curveData.iloc[:, i + 1]
                # 绘制多曲线图
                ax.line(curve_x, curve_y, linewidth=1.3, color=self.curve_colors[i], linestyle=self.curve_style[i],
                        label=self.legend_text[i])

            # 对 ax 进行格式化处理
            ax.format(
                ylocator=self.left_y_limit[2], ylim=(self.left_y_limit[0], self.left_y_limit[1]),
                yminorlocator=(self.left_y_limit[2] / 2)
            )
            if self.is_showLine is True:
                # 分别拿到 line 的 x 和 y
                line_x = self.lineData.iloc[:, 0]
                line_y = self.lineData.iloc[:, 1]
                # 创建第二个 y 轴
                ax2 = ax.alty(linewidth=0.8, label=self.right_y_label)
                # 绘制 line
                ax2.line(line_x, line_y, color=self.line_colors[0], linewidth=0.8)
                # 如果开启双 Y 轴，则还需要将 ax2 格式化
                ax2.format(
                    ylocator=self.right_y_limit[2],
                    ylim=(self.right_y_limit[0], self.right_y_limit[1]),
                    yminorlocator=(self.right_y_limit[2] / 2)
                )

        # 如果 curveData 的列数等于 2，则说明绘制的曲线为单曲线图
        elif len(self.curveData.columns) == 2:
            # 分别拿到 curve 的 x 和 y
            curve_x = self.curveData.iloc[:, 0]
            curve_y = self.curveData.iloc[:, 1]
            # 绘制 curve
            ax.line(curve_x, curve_y, linewidth=1.3, color=self.curve_colors[0], linestyle=self.curve_style[0],
                    label=self.legend_text[0])
            # 对 ax 进行格式化处理
            ax.format(
                ylocator=self.left_y_limit[2], ylim=(self.left_y_limit[0], self.left_y_limit[1]),
                yminorlocator=(self.left_y_limit[2] / 2)
            )
            if self.is_showLine is True:
                # 分别拿到 line 的 x 和 y
                line_x = self.lineData.iloc[:, 0]
                line_y = self.lineData.iloc[:, 1]
                # 创建第二个 y 轴
                ax2 = ax.alty(linewidth=0.8, label=self.right_y_label)
                # 绘制 line
                ax2.line(line_x, line_y, color=self.line_colors[0], linewidth=0.8)
                # 如果开启双 Y 轴，则还需要将 ax2 格式化
                ax2.format(
                    ylocator=self.right_y_limit[2],
                    ylim=(self.right_y_limit[0], self.right_y_limit[1]),
                    yminorlocator=(self.right_y_limit[2] / 2)
                )
        # 如果 curveData 的列数比 2 还小，则说明绘制的曲线数据存在问题
        else:
            raise Exception(
                "The curve data has fewer columns than expected (less than 2). "
                "There is an issue with the plotted curve data."
            )
        # 如果开启显示图例，则执行下面的代码
        if self.is_legend is True:
            ax.legend(loc='ur', ncols=1, fontweight='bold', fontsize=12.5, frame=False, bbox_to_anchor=(0.95, 0.96))
        # 如果开启显示 Zero 轴，则执行下面的代码
        if self.is_zero is True:
            # 显示 Zero 轴
            ax.axhline(y=0, color='black', linewidth=1.25)

        # 最后调用 fig.format 处理 x 轴和标题
        fig.format(
            xlabel=self.x_label, ylabel=self.left_y_label, title=self.title, grid=False,
            xlocator=self.x_limit[2], xlim=(self.x_limit[0], self.x_limit[1]),
            xminorlocator=(self.x_limit[2] / 2),
        )

        # 文件名初始值
        save_name = f"figure.{self.save_format}"
        i = 1
        # 首先检查当前路径是否存在以 figure.save_type 为文件名的文件
        while os.path.exists(save_name):
            # 文件名已存在，添加数字后缀
            save_name = f"figure{i}.{self.save_format}"
            i += 1
        # 保存图像，保存图像的名字为 figure + save_format
        fig.savefig(save_name, dpi=300, bbox_inches="tight", pad_inches=0.2)
        # 输出保存成功的信息
        print("Saving successful!\n")

    def set_xlim(self):
        """
        设置 Spectrum 的 x_limit 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input lower and upper limit of X-axis, eg. 150,300,50\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 x_limit
        self.x_limit = list(map(float, your_input.split(',')))
        print("Setting successful!\n")

    def set_left_ylim(self):
        """
        设置 Spectrum 的 left_y_limit 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input lower and upper limit of left Y-axis, eg. 150,300,50\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 left_y_limit
        self.left_y_limit = list(map(float, your_input.split(',')))
        print("Setting successful!\n")

    def set_right_ylim(self):
        """
        设置 Spectrum 的 right_y_limit 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input lower and upper limit of right Y-axis, eg. 150,300,50\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 right_y_limit
        self.right_y_limit = list(map(float, your_input.split(',')))
        print("Setting successful!\n")

    def toggle_legend(self):
        """
        设置 Spectrum 的 is_legend 属性


        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        print("0 Turn off showing the legend")
        print("1 Turn on showing the legend")
        your_input = input("Please enter the option of your choice:\n")
        if your_input.lower() == "r":
            return
        elif your_input == "0":
            self.is_legend = False
        elif your_input == "1":
            self.is_legend = True
        else:
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")
        print("Setting successful!\n")

    def toggle_zero_axis(self):
        """
        设置 Spectrum 的 is_zero 属性


        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        print("0 Turn off drawing of the zero axis")
        print("1 Turn on drawing of the zero axis")
        your_input = input("Please enter the option of your choice:\n")
        if your_input.lower() == "r":
            return
        elif your_input == "0":
            self.is_zero = False
        elif your_input == "1":
            self.is_zero = True
        else:
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")
        print("Setting successful!\n")

    def toggle_line(self):
        """
        设置 Spectrum 的 is_showLine 属性


        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        print("0 Turn off drawing of the discrete lines")
        print("1 Turn on drawing of the discrete lines")
        your_input = input("Please enter the option of your choice:\n")
        if your_input.lower() == "r":
            return
        elif your_input == "0":
            self.is_showLine = False
        elif your_input == "1":
            self.is_showLine = True
        else:
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")
        print("Setting successful!\n")

    def set_font_family(self):
        """
        设置 Spectrum 的 font_family 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input the font family that you want to set: \n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 font_family
        self.font_family = your_input
        print("Setting successful!\n")

    def set_font_size(self):
        """
        设置 Spectrum 的 font_size 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input the font size that you want to set, eg. 10.5,12,14\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 font_family
        self.font_size = list(map(float, your_input.split(',')))
        print("Setting successful!\n")

    def set_save_format(self):
        """
       设置 Spectrum 的 save_format 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input format of saving spectrum file, eg. png\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 save_format
        self.save_format = your_input
        print("Setting successful!\n")

    def set_save_dpi(self):
        """
       设置 Spectrum 的 save_dpi 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input dpi of saving spectrum, eg. 300\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 save_dpi
        self.save_dpi = float(your_input)
        print("Setting successful!\n")

    def set_figure_size(self):
        """
       设置 Spectrum 的 figure_size 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input figure size of spectrum file, eg. 8,5\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 figure_size
        self.figure_size = tuple(map(float, your_input.split(',')))
        print("Setting successful!\n")

    def set_title_label(self):
        """
       设置 Spectrum 的 title、x_label、left_y_label 以及 right_y_label 属性

        Returns:
            None
        """
        # 这是一个循环，如果要退出循环回到主页面，需要输入 r
        while True:
            print("Type \"r\": Return to main menu")
            print(f"0 Set the xlabel of the spectrum, {self.x_label}")
            print(f"1 Set the left ylabel of the spectrum, {self.left_y_label}")
            print(f"2 Set the right ylabel of the spectrum, {self.right_y_label}")
            print(f"3 Set the title of the spectrum, {self.title}")
            your_input = input("Please enter the option of your choice: \n")
            if your_input.lower() == 'r':
                break
            if your_input == '0':
                self.x_label = input("Please input the xlabel of the spectrum: \n")
                continue
            elif your_input == '1':
                self.left_y_label = input("Please input the left ylabel of the spectrum: \n")
                continue
            elif your_input == '2':
                self.right_y_label = input("Please input the right ylabel of the spectrum: \n")
                continue
            elif your_input == '3':
                self.title = input("Please input the title of the spectrum: \n")
                continue
            else:
                print("Invalid input. Please press the Enter button and make a valid selection.")
                input("Press Enter to continue...\n")
            print("Setting successful!\n")


def read_path(file_path):
    """
    读取 toml 文件中 path 所指向的 txt 或 xlxs 文件的内容

    Args:
        file_path: toml 文件中 path 所表示的路径

    Returns:
        data(DataFrame): 返回一个 Pandas DataFrame 对象

    """
    file = Path(file_path)
    # 根据文件的后缀是否为 txt 或者 xlsx 判断
    if file.suffix == ".txt":
        # 如果是 Multiwfn 输出的 txt 文件，调用 Pandas 的 read_csv 方法读取
        data = pd.read_csv(file_path, delim_whitespace=True, header=None)
    elif file.suffix == ".xlsx":
        # 读取包含光谱数据的 Excel 文件，假设文件包含一个名为 Sheet1 的表格
        data = pd.read_excel(file_path, sheet_name=0, dtype={'column_name': float})
    else:
        # 文件格式不支持
        raise ValueError("Unsupported file format.")

    return data


def create_spectrum(toml_file):
    """
    创建一个 Spectrum 对象并将 line_data 和 curve_data 赋值

    Args:
        toml_file(str): toml 文件路径

    Returns:
        Spectrum: 初始化好的 Spectrum 对象

    """
    # 从 toml 文件中获取 line_data 数据和 curve_data 数据的来源
    with open(toml_file, 'r', encoding='utf-8') as file:
        toml_data = toml.load(file)

    # 获取 toml 文件的当前文件夹
    current_folder = os.path.dirname(os.path.abspath(toml_file))

    # 获取 curve 的配置，curve 是必须存在的
    curve = toml_data.get('curve')
    if curve is None:
        raise ValueError("Missing 'curve' configuration. It is required.")
    else:
        # 处理 curve 表的路径属性
        curve_path = curve['path']
        # 如果 toml 文件中 curve 和 line 表的 path 属性仅为一个相对路径，则将相对路径设置为 toml 文件的相对路径，而不是主程序的相对路径
        if os.path.isabs(curve_path):
            # 如果是绝对路径，则直接使用该路径
            curve_data_source = curve_path
        # 如果 toml 文件中 curve 和 line 表的 path 属性仅为一个绝对路径，则直接使用这个绝对路径
        else:
            # 如果是相对路径，则与当前文件夹拼接
            curve_data_source = os.path.join(current_folder, curve_path)
        # 根据 curve 的 path 属性得到 curve_data
        curve_data = read_path(curve_data_source)
        # 首先判断 color 属性存不存在，如果不存在则赋值为默认的 red
        if 'color' in curve:
            curve_color = curve['color']
        else:
            # 默认为红色
            curve_color = ['red']

        # 接着判断 style 属性存不存在，如果不存在则赋值为默认的 -
        if 'style' in curve:
            curve_style = curve['style']
        else:
            # 默认为 -
            curve_style = ['-']

        # 接着判断 legend 属性存不存在，如果不存在则赋值为 [None]
        if 'legend' in curve:
            legend_text = curve['legend']
        else:
            # 默认为 [None]
            legend_text = [None]

    # 获取 line 的配置，line 可以不存在
    line = toml_data.get('line')
    if line is None:
        # 如果 line 不存在，则直接返回 None
        line_data, line_color = None, None
    else:
        line_path = line['path']
        if os.path.isabs(line_path):
            # 如果是绝对路径，则直接使用该路径
            line_data_source = line_path
        else:
            # 如果是相对路径，则与当前文件夹拼接
            line_data_source = os.path.join(current_folder, line_path)
        # 根据 line 的 path 属性得到 line_data
        line_data = read_path(line_data_source)
        if 'color' in line:
            # 根据 line 的 color 属性得到 line_color
            line_color = line['color']
        else:
            # 默认为黑色
            line_color = ['black']

    return Spectrum(curveData=curve_data, lineData=line_data, line_colors=line_color, curve_colors=curve_color,
                    curve_style=curve_style, legend_text=legend_text)


def count_degree(expected, max_value, min_value, symmetrical=False):
    """
    Calculate the maximum and minimum degrees of the expected scale,
    which are multiples of the estep.

    Args:
        expected (float): The desired interval of the scale.
        max_value (float): The maximum value of the data.
        min_value (float): The minimum value of the data.
        symmetrical (bool, optional): Whether to enable symmetrical scale.
            Defaults to False.

    Returns:
        tuple: The maximum and minimum degrees (maxi, mini).

    """
    # The final effect is to take 1 unit up when max/expected belongs to the interval (-1, Infinity),
    # otherwise take 2 units. Similarly, take 1 unit down when min/expected belongs to the interval (-Infinity,1),
    # otherwise take 2 units.
    maxi = int(max_value / expected + 1) * expected
    mini = int(min_value / expected - 1) * expected

    # If max and min are exactly on the scale lines, the logic above would take one extra unit up or down.
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
    Automatically generate a neat xlim or ylim based on the maximum and minimum values.
    The lim includes the maximum value and minimum value of the x or y axis,
    as well as the x or y axis tick locator.

    Args:
        max_value (float): The maximum value of x or y data.
        min_value (float): The minimum value of x or y data.
        is_deviation (bool, optional): Whether to allow deviation.
            Defaults to False.

    Returns:
        list: Auto lim list [lim_min, lim_max, locator].

    """
    # Initialize the desired number of scale intervals
    split_number = 4

    # Initialize a magic array and calculate the initial interval (temp_gap) and scaling factor (multiple)
    magic_array = [2, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100]
    temp_gap = (max_value - min_value) / split_number
    multiple = 10 ** (math.floor(math.log10(temp_gap) - 1))
    expected = next((val * multiple for val in magic_array if val > temp_gap / multiple), None)

    # Calculate the maximum and minimum degrees of the expected scale
    maxi, mini = count_degree(expected, max_value, min_value)

    if not is_deviation:
        while True:
            temp_split_number = round((maxi - mini) / expected)

            # Update the maximum and minimum values based on conditions
            if (maxi == 0 or mini - min_value <= maxi - max_value) and temp_split_number < split_number:
                # Update the minimum value (move left)
                mini -= expected
            else:
                # Update the maximum value (move right)
                maxi += expected

            # Exit the loop when the desired number of splits is reached
            if temp_split_number == split_number:
                break

            if temp_split_number > split_number:
                # Find the index of the current magic number
                magic_idx = next((i for i, val in enumerate(magic_array) if val * multiple == expected), None)

                # If the index exists and is not the last one, update the expected value and the maximum
                # and minimum values
                if magic_idx is not None and magic_idx < len(magic_array) - 1:
                    # Update the expected value (increase)
                    expected = magic_array[magic_idx + 1] * multiple
                    # Update the maximum and minimum values
                    maxi, mini = count_degree(expected, max_value, min_value)
                else:
                    break
            else:
                # Find the index of the current magic number
                magic_idx = next((i for i, val in enumerate(magic_array) if val * multiple == expected), None)

                # If the index exists and is not the first one, update the expected value and the
                # maximum and minimum values
                if magic_idx is not None and magic_idx > 0:
                    # Update the expected value (decrease)
                    expected = magic_array[magic_idx - 1] * multiple
                    # Update the maximum and minimum values
                    maxi, mini = count_degree(expected, max_value, min_value)
                else:
                    break

    interval = (maxi - mini) / split_number
    lim = [mini, maxi, interval]

    return lim


def validate(file):
    """
    判断输入的文件是否为 toml 文件

    Args:
        file(str): toml 文件的路径
    """
    # 首先判断输入的是否为 toml 文件，如果不是，则抛出异常。并在屏幕上打印不支持该文件
    if not file.endswith(".toml"):
        raise ValueError("Error: Unsupported file format. Only TOML files are supported.\n")

    # 判断输入的 toml 文件是否存在，如果不存在，则抛出异常。并在屏幕上打印未找到该文件
    if not os.path.isfile(file):
        raise FileNotFoundError("Error: File not found.\n")


def welcome_view():
    """显示程序的基本信息、配置信息以及版权信息。

    Returns:
        None
    """
    # 程序最后输出版本和基础信息
    print(f"KimariDraw --  A Python script that processes Multiwfn spectral data and plots various spectra.")
    print(f"Version: {__version__}, release date: {__release__}")
    print(f"Developer: {__developer__}")
    print(f"Address: {__address__}")
    print(f"KimariDraw home website: {__website__}\n")
    # 获取当前日期和时间
    now = datetime.now().strftime("%b-%d-%Y, 00:45:%S")
    # 程序结束后提示版权信息和问候语
    print(f"(Copyright (C) 2023 Kimariyb. Currently timeline: {now})\n")


def select_file():
    """通过命令行或者 GUI 界面选择一个文件，这个文件必须是 toml 文件，并且满足程序所指定的 toml 文件内容

    Notes:
        1. 如果直接写入 toml 文件的绝对路径，则直接返回 toml_path
        2. 如果输入 Enter 则弹出 GUI 界面选择 toml 文件
        3. 如果输入 q 则退出整个程序

    Returns:
        toml_path(str): 返回一个 toml 文件路径
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
        # 对应与直接输入 Enter，如果输入 ENTER 则显示 GUI 界面，不会退出主程序
        if not input_str:
            # 弹出文件选择对话框
            if dialog.ShowModal() == wx.ID_CANCEL:
                # 如果没有选择文件，即选择取消，则打印提示信息，并回到 input_str 输入文本这里
                print("Hint: You did not select a file.\n")
                # 返回 None 表示未选择文件, 继续主循环
                continue
            input_path = dialog.GetPath()
            try:
                # 得到文件后，必须验证是否为 toml 文件，如果不是则继续输入
                validate(input_path)
            except (ValueError, FileNotFoundError) as e:
                print(str(e))
                # 继续主循环
                continue
            print(f"Hint: Selected toml file path: {input_path}\n")
            # 销毁对话框
            dialog.Destroy()
            # 返回 input_path
            return input_path
        # 对应直接填写文件路径
        else:
            # 对于直接输入了路径的情况，执行验证逻辑
            try:
                # 得到文件后，必须验证是否为 toml 文件，如果不是则继续输入
                validate(input_str)
            except (ValueError, FileNotFoundError) as e:
                print(str(e))
                # 继续主循环
                continue
            print(f"Hint: Selected toml file path: {input_str}\n")
            # 返回 input_str
            return input_str


def main_view(input_file):
    """
    KimariDraw 的主程序界面，这个界面是一个交互式的界面。用户可以输入指令自定义的绘制用户想要绘制的 Spectrum

    Args:
        input_file: 从 select_file() 或命令行参数读取到的 toml 文件路径

    Returns:
        None
    """
    # 调用 create_spectrum() 实例化一个 spectrum 对象，这个对象在退出程序之前都不会消失
    spectrum = create_spectrum(input_file)
    while True:
        # 显示主页面，如果不输入 q，则一直在主程序中
        print(" \"q\": Exit program gracefully\t \"r\": Load a new file")
        print("********************************************************")
        print("****************** Main function menu ******************")
        print("********************************************************")
        print(f"-1 Set font family of the spectrum, current: {spectrum.font_family}")
        print(f"-2 Set font size of the spectrum, current: {spectrum.font_size}")
        print("-3 Set title/xlabel/ylabel of the spectrum")
        print(f"-4 Set format of saving spectrum file, current: {spectrum.save_format}")
        print(f"-5 Set dpi of saving spectrum, current: {spectrum.save_dpi}")
        print(f"-6 Set figure size of spectrum file, current: {spectrum.figure_size}")
        print("0 Save graphical file of the spectrum in current folder!")
        print(f"1 Set lower and upper limit of X-axis, current: {spectrum.x_limit}")
        print(f"2 Set lower and upper limit of left Y-axis, current: {spectrum.left_y_limit}")
        print(f"3 Set lower and upper limit of right Y-axis, current: {spectrum.right_y_limit}")
        print(f"4 Toggle showing legend text, current: {spectrum.is_legend}")
        print(f"5 Toggle showing the zero axis, current: {spectrum.is_zero}")
        print(f"6 Toggle showing discrete lines, current: {spectrum.is_showLine}")

        # 接受用户的指令，并根据用户的指令
        choice = input()
        # 如果输入 0，则直接调用 draw_spectrum() 方法，保存图片
        if choice == "0":
            spectrum.draw_spectrum()
            continue
        # 如果输入 1，调用 set_xlim 方法修改 xlim
        elif choice == "1":
            spectrum.set_xlim()
            continue
        # 如果输入 2，调用 set_left_ylim 方法修改 left xlim
        elif choice == "2":
            spectrum.set_left_ylim()
            continue
        # 如果输入 3，调用 set_right_ylim 方法修改 right ylim
        elif choice == "3":
            spectrum.set_right_ylim()
            continue
        # 如果输入 4，是否显示图例文本 toggle_legend
        elif choice == "4":
            spectrum.toggle_legend()
            continue
        # 如果输入 5，是否开启 zero 轴 toggle_zero_axis
        elif choice == "5":
            spectrum.toggle_zero_axis()
            continue
        # 如果输入 6，是否显示 line 数据 toggle_line
        elif choice == "6":
            spectrum.toggle_line()
        # 如果输入 -1，设置绘制光谱的字体
        elif choice == "-1":
            spectrum.set_font_family()
            continue
        # 如果输入 -2，设置绘制光谱的字号
        elif choice == "-2":
            spectrum.set_font_size()
            continue
        # 如果输入 -3，设置 title、xlabel、ylabel(包括 left label 和 right label)
        elif choice == "-3":
            spectrum.set_title_label()
            continue
        # 如果输入 -4，设置保存图片的格式
        elif choice == "-4":
            spectrum.set_save_format()
            continue
        # 如果输入 -5，设置保存图片的 dpi
        elif choice == "-5":
            spectrum.set_save_dpi()
            continue
        # 如果输入 -6，设置图片的大小
        elif choice == "-6":
            spectrum.set_figure_size()
            continue
        # 如果输入 q 则退出程序
        elif choice.lower() == "q":
            print()
            print("The program has already terminated!")
            print("Thank you for your using! Have a good time!")
            sys.exit()
        # 如果输入 r 则重新加载一个新的 toml 文件
        elif choice.lower() == "r":
            toml_file = select_file()
            # 重新载入一个 spectrum，并用这个 spectrum 继续循环
            spectrum = create_spectrum(toml_file)
            continue
        # 如果输入的内容不符合要求，提示按下空格重新选择。
        else:
            print()
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")


def main():
    # 命令行运行方式
    if len(sys.argv) > 1:
        # 处理命令行参数
        arg = sys.argv[1]
        # 创建 ArgumentParser 对象
        parser = argparse.ArgumentParser(prog='KimariDraw', add_help=False,
                                         description='KimariDraw -- A Python script that processes Multiwfn spectral '
                                                     'data and plots various spectra.')
        # 添加 -h 参数
        parser.add_argument('--help', '-h', action='help', help='Show this help message and exit')
        # 添加 -v 参数
        parser.add_argument('--version', '-v', action='version', version=__version__)
        # 添加输入文件参数
        parser.add_argument('input', type=str, help='Text file containing spectral data generated by Multiwfn')
        # 解析参数
        args = parser.parse_args()
        # 处理命令行参数
        input_file = args.input
        # 进入主程序 main_view()
        main_view(input_file=input_file)
    # 否则就直接进入主程序
    else:
        # 创建一个 wx 实例
        app = wx.App()
        # 显示欢迎界面
        welcome_view()
        # 选择需要解析的 toml 文件路径
        selected_file = select_file()
        # 进入主程序
        main_view(selected_file)

