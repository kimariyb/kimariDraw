from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame

from Spectrum.spectrum import Spectrum
from Utils.config import read_vcd_config


class VCDSpectrum(Spectrum):
    def __init__(self):
        super().__init__('VCD')
        self.figure_size = read_vcd_config('settings.ini')[0]
        self.x_limits = read_vcd_config('settings.ini')[1]
        self.y_limits = read_vcd_config('settings.ini')[2]
        self.curve_colors = read_vcd_config('settings.ini')[3]
        self.save_format = read_vcd_config('settings.ini')[5]

    def plot_spectrum(self, dataframe: DataFrame):
        """
        将谱图绘制出来
        :return: fig ax
        """
        # 设置全局字体、字重和轴线宽度
        plt.rcParams.update({
            'font.family': 'Arial',
            'font.weight': 'bold',
            'axes.linewidth': 1.5
        })

        # 创建画布和子图对象
        fig, ax = plt.subplots(figsize=self.figure_size)

        # 设置 x 轴和 y 轴的范围
        ax.set_xlim(self.x_limits[0], self.x_limits[1])
        ax.set_ylim(self.y_limits[0], self.y_limits[1])

        # 修改 x 轴和 y 轴的刻度间隔
        x_locator = MultipleLocator(self.x_limits[2])
        y_locator = MultipleLocator(self.y_limits[2])

        ax.xaxis.set_major_locator(x_locator)
        ax.yaxis.set_major_locator(y_locator)

        ax.xaxis.set_minor_locator(MultipleLocator(self.x_limits[2] / 2))
        ax.yaxis.set_minor_locator(MultipleLocator(self.y_limits[2] / 2))

        # 设置 x、y 轴的刻度标签和字体大小
        ax.tick_params(axis='both', which='major', labelsize=13, width=1.5, length=6)
        ax.tick_params(axis='both', which='minor', width=1.5, length=4)
        # 将刻度标签加粗
        for label in ax.xaxis.get_ticklabels():
            label.set_fontweight('bold')
        for label in ax.yaxis.get_ticklabels():
            label.set_fontweight('bold')

        # 绘制 curve
        ax.plot(dataframe['x'], dataframe['y'], linewidth=1.5, color=self.curve_colors)

        # 绘制一个 y = 0 的平行于 x 轴的线段
        ax.axhline(y=0, color='black', linewidth=1.5)

        # 添加坐标轴标签
        ax.set_xlabel('Wavenumber (cm^-1)', fontweight='bold', fontsize=16)
        ax.set_ylabel('Delta Epsilon (arb.)', fontweight='bold', fontsize=16)

        # 调整图表布局，增加底部边距
        fig.subplots_adjust(bottom=0.2)

        return fig, ax
