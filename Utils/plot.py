from Spectrum.spectrum_factory import SpectrumFactory
from Utils.utils import ask_save_image


def plot_spectrum(dataframe, spectrum_type):
    # 创建一个 Spectrum 对象
    spectrum = SpectrumFactory.create_spectrum(spectrum_type)
    # 调用绘图函数
    fig, ax = spectrum.creat_figure(dataframe)
    # 展示图片
    fig.show()
    # 询问是否保存图片
    if ask_save_image(spectrum.save_format):
        fig.savefig('output/' + spectrum_type + '_Spectrum' + '.' + spectrum.save_format, dpi=500, bbox_inches='tight')


def plot_multi_spectrum(dataframe, spectrum_type):
    # 创建一个 Spectrum 对象
    spectrum = SpectrumFactory.create_spectrum(spectrum_type)
    # 调用绘图函数
    fig, ax = spectrum.creat_multi_figure(dataframe)
    # 展示图片
    fig.show()
    # 询问是否保存图片
    if ask_save_image(spectrum.save_format):
        fig.savefig('output/' + spectrum_type + '_Spectrum' + '.' + spectrum.save_format, dpi=500, bbox_inches='tight')
