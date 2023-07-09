import numpy as np
from pandas import DataFrame


class Spectrum:
    def __init__(self, spectrum_type):
        self.spectrum_type = spectrum_type
        self.dataframe = None
        self.x_limits = None
        self.y_limits = None
        self.figure_size = None
        self.curve_colors = None
        self.spike_colors = None
        self.save_format = None

    def load_dataframe(self, dataframe):
        """
        load dataframe in the spectrum
        :param dataframe: dataframe to load
        :return:
        """
        self.dataframe = dataframe

    def plot_spectrum(self):
        """
        将谱图绘制出来
        :return: fig ax
        """
        raise NotImplementedError

    def set_x_limits(self, lower=None, upper=None, spacing=None):
        """
        设置 X 轴的上下限
        :param lower: 下限
        :param upper: 上限
        :param spacing: 刻度间隔
        :return:
        """
        self.x_limits = (lower, upper, spacing)
        print(f'Setting X-axis limits to ({lower}, {upper}, {spacing})...')

    def set_y_limits(self, lower=None, upper=None, spacing=None):
        """
        设置 Y 轴的上下限
        :param lower: 下限
        :param upper: 上限
        :param spacing: 刻度间隔
        :return:
        """

        self.y_limits = (lower, upper, spacing)
        print(f'Setting Y-axis limits to ({lower}, {upper}, {spacing})...')

    def set_figure_size(self, width, height):
        """
        设置图片大小
        :param width: 宽
        :param height: 高
        :return:
        """
        self.figure_size = (width, height)
        print(f'Setting figure size to {self.figure_size}...')

    def set_curve_colors(self, colors):
        """
        设置曲线颜色
        :param colors: 颜色
        :return:
        """
        self.curve_colors = colors
        print(f'Setting curve colors to {colors}...')

    def set_spike_colors(self, colors):
        """
        设置曲线颜色
        :param colors: 颜色
        :return:
        """
        self.spike_colors = colors
        print(f'Setting spike colors to {colors}...')

    def set_save_format(self, format_type):
        """
        保存图片的格式
        :param format_type: 保存格式
        :return:
        """
        self.save_format = format_type
        print(f'Setting save format to {format_type}...')

