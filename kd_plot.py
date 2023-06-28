import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


from kd_data import KDData


class KDProfile:
    def __init__(self, data: KDData):
        """
        初始化 KDProfile constructor
        :param data: KDData 对象
        """
        self.data = data

    def axis_init(self):
        """
        初始化坐标轴
        :return:
        """
        pass

    def set_font(self):
        """
        修改坐标轴字体
        :return:
        """
        font = self.data.font_family
        if font == 'Arial':
            pass
        elif font == 'Times New Roman':
            pass
        elif font == 'Calibri':
            pass

    def set_color(self):
        """
        修改主题颜色
        :return:
        """
        color_theme = self.data.color_theme
        if color_theme == 'nature':
            pass
        elif color_theme == 'science':
            pass

    def set_figure(self):
        """
        修改图片画布大小
        :return:
        """
        figure_size = self.data.figure_size
        plt.figure(figure=figure_size, dpi=700)

    def save_figure(self):
        pass
