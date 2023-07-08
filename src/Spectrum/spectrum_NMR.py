from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame
from scipy import signal

from src.Spectrum.spectrum import Spectrum


class NMRSpectrum(Spectrum):
    def __init__(self):
        super().__init__('NMR')

    def plot_spectrum(self, dataframe: DataFrame):
        """
        将谱图绘制出来
        :param dataframe: pandas dataframe
        :return: fig ax
        """
        # 设置全局字体、字重和轴线宽度
        plt.rcParams.update({
            'font.family': 'Arial',
            'font.weight': 'bold',
            'axes.linewidth': 1.5
        })
        # 设置默认 NMR config
        self.set_x_limits(12, 0, 1)
        self.set_y_limits(0, 30, 5)
        self.set_figure_size(10, 5)
        self.set_curve_colors("#DC143C")
        self.set_spike_colors("#DC143C")
        self.set_save_format("png")

        # 创建画布和子图对象
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=400)

        # 设置 x 轴和 y 轴的范围
        ax.set_xlim(self.x_limits[0], self.x_limits[1])
        ax.set_ylim(self.y_limits[0], self.y_limits[1])

        # 修改 x 轴和 y 轴的刻度间隔
        x_locator = MultipleLocator(self.x_limits[2])
        y_locator = MultipleLocator(self.y_limits[2])

        ax.xaxis.set_major_locator(x_locator)
        ax.yaxis.set_major_locator(y_locator)

        # 设置 x、y 轴的刻度标签和字体大小
        ax.tick_params(axis='both', which='major', labelsize=13, width=1.5, length=5)
        # 将刻度标签加粗
        for label in ax.xaxis.get_ticklabels():
            label.set_fontweight('bold')
        for label in ax.yaxis.get_ticklabels():
            label.set_fontweight('bold')

        # 绘制 curve
        ax.plot(dataframe['x'], dataframe['y'], linewidth=1.5, color=self.curve_colors)
        # 绘制 spike
        peaks, _ = signal.find_peaks(dataframe['y'])
        for i in peaks:
            ax.plot([dataframe['x'][i], dataframe['x'][i]], [0, dataframe['y'][i]], color=self.spike_colors, linewidth=1.5)

        # 添加坐标轴标签
        ax.set_xlabel('Chemical Shift (ppm)', fontweight='bold', fontsize=16)
        ax.set_ylabel('Signal Strength', fontweight='bold', fontsize=16)

        # 调整图表布局，增加底部边距
        fig.subplots_adjust(bottom=0.2)

        return fig, ax



