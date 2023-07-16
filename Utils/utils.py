import datetime

from Spectrum.spectrum_factory import SpectrumFactory


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
    print('0. Return the main view')
    print('1. NMR')
    print('2. IR')
    print('3. Raman')
    print('4. UV-Vis')
    print('5. ECD')
    print('6. VCD')
    choice = input()
    if choice not in ['0', '1', '2', '3', '4', '5', '6']:
        raise ValueError("Invalid spectrum type, please input the correct numeric code.")
    return choice


def plot_nmr_spectrum(dataframe):
    # 创建一个 NMRSpectrum 对象
    nmr_spectrum = SpectrumFactory.create_spectrum('NMR')
    # 调用绘图函数
    fig, ax = nmr_spectrum.plot_spectrum(dataframe)
    # 展示图片
    fig.show()
    # 询问是否保存图片
    if ask_save_image(nmr_spectrum.save_format):
        fig.savefig('NMR_Spectrum' + '.' + nmr_spectrum.save_format, dpi=500, bbox_inches='tight')


def plot_ir_spectrum(dataframe):
    # 创建一个 NMRSpectrum 对象
    ir_spectrum = SpectrumFactory.create_spectrum('IR')
    # 调用绘图函数
    fig, ax = ir_spectrum.plot_spectrum(dataframe)
    # 展示图片
    fig.show()
    # 询问是否保存图片
    if ask_save_image(ir_spectrum.save_format):
        fig.savefig('IR_Spectrum' + '.' + ir_spectrum.save_format, dpi=500, bbox_inches='tight')


def plot_raman_spectrum(dataframe):
    # 创建一个 NMRSpectrum 对象
    raman_spectrum = SpectrumFactory.create_spectrum('Raman')
    # 调用绘图函数
    fig, ax = raman_spectrum.plot_spectrum(dataframe)
    # 展示图片
    fig.show()
    # 询问是否保存图片
    if ask_save_image(raman_spectrum.save_format):
        fig.savefig('Raman_Spectrum' + '.' + raman_spectrum.save_format, dpi=500, bbox_inches='tight')


def plot_uv_spectrum(dataframe):
    # 创建一个 NMRSpectrum 对象
    uv_spectrum = SpectrumFactory.create_spectrum('UV')
    # 调用绘图函数
    fig, ax = uv_spectrum.plot_spectrum(dataframe)
    # 展示图片
    fig.show()
    # 询问是否保存图片
    if ask_save_image(uv_spectrum.save_format):
        fig.savefig('UV_Spectrum' + '.' + uv_spectrum.save_format, dpi=500, bbox_inches='tight')


def ask_save_image(save_format):
    # 询问是否保存图片
    save_choice = input('Do you want to save the image? (y/n) ')
    if save_choice.lower() == 'y':
        return True
    else:
        return False
