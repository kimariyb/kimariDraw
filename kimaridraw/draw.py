from datetime import datetime
from pathlib import Path

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
        self.developer = "Kimariyb, Ryan Hsiun"
        self.version = "2.5.0"
        self.release_date = str(datetime.today().strftime("%b-%d-%Y"))
        self.address = "XiaMen University, School of Electronic Science and Engineering"
        self.website = "https://github.com/kimariyb/kimariDraw"


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
        :param legend_text: 图例文本，默认为空
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
        self.legend_text = legend_text
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
    x_max = data.iloc[:, 0].max()
    x_min = data.iloc[:, 0].min()
    # 得到 x 的最大值和最小值之后，程序自动设定 xlim
    init_xlim = auto_xlim(x_max, x_min)
    # 根据 1~n 列的数据的最大值和最小值设定 ylim
    y_max = data.iloc[:, 1].max()
    y_min = data.iloc[:, 1].min()
    init_ylim = auto_ylim(y_max, y_min)
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


def auto_xlim(x_max, x_min):
    """
    根据最大值和最小值，自动生成一个较为整齐的 xlim
    :param x_max: x 数据的最大值
    :param x_min: x 数据的最小值
    :return: 返回一个 auto xlim list
    """
    auto_x = []

    return auto_x


def auto_ylim(y_max, y_min):
    """
    根据最大值和最小值，自动生成一个较为整齐的 ylim
    :param y_max: y 数据的最大值
    :param y_min: y 数据的最小值
    :return: 返回一个 auto ylim list
    """
    auto_y = []

    return auto_y


def main():
    """
    :param is_sup: 是否开启子图模式
    :param is_serial: 是否显示子图序号
    :param sup_layout: 子图的排版
    """
    pass


if __name__ == '__main__':
    main()
