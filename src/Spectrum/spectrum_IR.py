from matplotlib import pyplot as plt
from pandas import DataFrame

from src.Spectrum.spectrum import Spectrum


class IRSpectrum(Spectrum):
    def __init__(self):
        super().__init__('NMR')

    def plot_spectrum(self, dataframe: DataFrame):
        # 将 NMR 谱图绘制出来
        # 设置全局字体、字重和轴线宽度
        plt.rcParams.update({
            'font.family': 'Arial',
            'font.weight': 'bold',
            'axes.linewidth': 1.5
        })

        # 创建画布和子图对象
        fig, ax = plt.subplots(figsize=self.figure_size)

        fig.plot(dataframe['x'], dataframe['y'])

        return fig, ax
