from pathlib import Path

import pandas as pd
import toml


class SpectrumConfig:
    def __init__(self):
        self.plot_type = None
        self.x_limit = None
        self.y_limit = None
        self.title = None
        self.x_label = None
        self.y_label = None
        self.font_family = None
        self.figure_size = None
        self.colors = None
        self.line_style = None
        self.zero_line = None
        self.serial = None
        self.legend = None
        self.legend_text = None

    @staticmethod
    def from_toml(file_path):
        config = SpectrumConfig()
        with open(file_path, 'r', encoding='utf-8') as file:
            data = toml.load(file)

        config.plot_type = data.get('PlotType')
        config.x_limit = data.get('xLimit')
        config.y_limit = data.get('yLimit')
        config.title = data.get('Title')
        config.x_label = data.get('xLabel')
        config.y_label = data.get('yLabel')
        config.font_family = data.get('FontFamily')
        config.figure_size = data.get('FigureSize')
        config.colors = data.get('Colors')
        config.line_style = data.get('LineStyle')
        config.zero_line = data.get('ZeroLine')
        config.serial = data.get('Serial')
        config.legend = data.get('Legend')
        config.legend_text = data.get('LegendText')

        return config

    def __str__(self):
        return f"PlotType: {self.plot_type}\nxLimit: {self.x_limit}\nyLimit: {self.y_limit}\nTitle: {self.title}\n"\
               f"xLabel: {self.x_label}\nyLabel: {self.y_label}\nFontFamily: {self.font_family}\nFigureSize: {self.figure_size}\n"\
               f"Colors: {self.colors}\nLineStyle: {self.line_style}\nZeroLine: {self.zero_line}\nSerial: {self.serial}\n"\
               f"Legend: {self.legend}\nLegendText: {self.legend_text}\n"


def get_dataframe(file_name: str):
    """
    装载记录光谱数据的 txt 文件，并返回为一个 pandas DataFrame 对象
    :return: DataFrame 对象
    """
    file_path = Path(file_name)
    # 读取文件
    with file_path.open('r', encoding='utf-8') as f:
        df = pd.read_csv(f, delim_whitespace=True, header=None)
    return df

def


if __name__ == '__main__':
    config = SpectrumConfig.from_toml('settings.toml')
    print(config)
