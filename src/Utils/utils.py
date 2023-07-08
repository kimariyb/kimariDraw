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
Hint: Press ENTER button directly can select file in a GUI window. 
    """

    # 打印界面文本
    print(interface_text)


