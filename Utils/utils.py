import configparser
import datetime
import os


def welcome():
    version_info = {
        'version': '2.0',
        'release_date': '2023-07',
        'developer': 'Kimariyb (XiaMen University, School of Electronic Science and Engineering)',
        'website': 'https://github.com/kimariyb/kimariDraw',
    }

    # 获取当前日期和时间
    now = datetime.datetime.now()

    # 定义界面文本
    # 定义界面文本
    interface_text = f"""
KimariDraw -- A spectrum plotting program based on Multitwfn.
Version {version_info['version']}, release date: {version_info['release_date']}
Developer: {version_info['developer']}
KimariDraw Github website: {version_info['website']}

( Current date: {now.date()}  Time: {now.strftime("%H:%M:%S")} )

Input file path, for example d:\\project\\kimariDraw\\data\\NMR_curve.txt
( Supported: .txt file and .xlsx file )
    """

    # 打印界面文本
    print(interface_text)


def main_view():
    """
    主程序界面
    """
    print('Please enter the spectrum you want to plot.')
    print('1. NMR')
    print('2. IR')
    print('3. Raman')
    print('4. UV-Vis')
    print('5. ECD')
    print('6. VCD')
    choice = input()
    if choice not in ['1', '2', '3', '4', '5', '6']:
        raise ValueError("Invalid spectrum type, please input the correct numeric code.")
    return choice


def read_nmr_config(filename):
    """
    获得 NMR configuration
    :param filename: 文件名字
    :return:
    """
    # 构建绝对路径
    file_path = os.path.join(os.path.dirname(__file__), '..', filename)

    config = configparser.ConfigParser()
    config.read(file_path)

    # 读取配置项
    figure_size = tuple(map(int, config.get('NMR', 'figure_size').split(',')))
    save_format = config.get('NMR', 'save_format')
    curve_colors = config.get('NMR', 'curve_color')
    spike_colors = config.get('NMR', 'spike_color')
    x_limit = tuple(map(float, config.get('NMR', 'x_limit').split(',')))
    y_limit = tuple(map(float, config.get('NMR', 'y_limit').split(',')))

    return figure_size, x_limit, y_limit, curve_colors, spike_colors, save_format
