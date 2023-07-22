import datetime
import os


def welcome():
    version_info = {
        'version': '2.3.0',
        'release_date': '2023-Jul',
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


def input_file_path():
    # 输入文件路径，并处理异常
    url = input("Please enter the file path: ")
    if not os.path.isfile(url):
        raise FileNotFoundError(f"File not found: {url}")
    return url


def main_view():
    """
    主程序界面
    """
    print('Please enter the spectrum you want to plot: ')
    print('0. Return')
    print('1. NMR')
    print('2. IR')
    print('3. Raman')
    print('4. UV-Vis')
    print('5. ECD')
    print('6. VCD')
    print('7. PES')
    choice = input()
    if choice not in ['0', '1', '2', '3', '4', '5', '6', '7']:
        raise ValueError("Invalid spectrum type, please input the correct numeric code.")
    return choice


def single_or_multiple():
    """
    选择绘制单例视图还是多例势图
    :return:
    """
    print('Please enter the operation you want: ')
    print('0. Return and enter the file path again.')
    print('1. The Single Spectrum')
    print('2. The Multiple Spectrum')
    choice = input()
    if choice not in ['0', '1', '2']:
        raise ValueError("Invalid choice. Please enter 0 or 1 or 2.")
    return choice


def ask_save_image(save_format):
    # 询问是否保存图片
    save_choice = input('Do you want to save the image? (y/n) ')
    if save_choice.lower() == 'y':
        return True
    else:
        return False
