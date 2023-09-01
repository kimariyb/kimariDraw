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
import os
import sys
import wx

from datetime import datetime

from KimariDraw.draw.spectrum import create_spectrum
from KimariDraw.utils.common import validate

# 获取当前文件被修改的最后一次时间
time_last = os.path.getmtime(os.path.abspath(__file__))
# 全局的静态变量
__version__ = "2.5.2"
__developer__ = "Kimariyb, Ryan Hsiun"
__address__ = "XiaMen University, School of Electronic Science and Engineering"
__website__ = "https://github.com/kimariyb/kimariDraw"
__release__ = str(datetime.fromtimestamp(time_last).strftime("%b-%d-%Y"))


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
            print("Hint: Selected toml file path:", input_str)
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
            print("Hint: Selected toml file path:", input_str)
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

