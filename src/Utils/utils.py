import datetime


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
    print('1. NMR \t 2. IR \t 3. Raman \t 4. UV-Vis \t 5. ECD \t 6. VCD')


def nmr_view(self):
    """
    NMR 选择界面
    """
    print('0. Plot NMR spectrum now!')
    print('1. Save graphical file of NMR spectrum in current folder')
    print('2. Set lower and upper limits of X-axis')
    print('3. Set upper and lower limits of Y-axis')
    print('4. Set size of figure')
    print('5. Set colors of curves and spikes')
    print('6. Set format of saving graphical file')


def ir_view():
    pass




