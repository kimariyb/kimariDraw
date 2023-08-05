from pathlib import Path

import proplot as pplt
import matplotlib.pyplot as plt
import pandas as pd
import toml

from proplot import rc


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
        self.sup_type = None

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
        config.sup_type = data.get('SupType')

        return config

    def __str__(self):
        return f"PlotType: {self.plot_type}\nxLimit: {self.x_limit}\nyLimit: {self.y_limit}\nTitle: {self.title}\n" \
               f"xLabel: {self.x_label}\nyLabel: {self.y_label}\nFontFamily: {self.font_family}\nFigureSize: {self.figure_size}\n" \
               f"Colors: {self.colors}\nLineStyle: {self.line_style}\nZeroLine: {self.zero_line}\nSerial: {self.serial}\n" \
               f"Legend: {self.legend}\nLegendText: {self.legend_text}\nSupType: {self.sup_type}"


def get_dataframe(file_name: str):
    """
    装载记录光谱数据的 txt 文件，并返回为一个 pandas DataFrame 对象
    :return: DataFrame 对象
    """
    file_path = Path(file_name)
    # 读取文件
    with file_path.open('r', encoding='utf-8') as f:
        df = pd.read_csv(f, delim_whitespace=True, header=None)
    # 为列指定新的标签
    df = df.rename(columns={0: 'x', 1: 'y'})
    return df


def read_multiple(multiple_path: str):
    """
    读取 multiple.txt 并将其中的 txt 文件返回为 DataFrame 对象
    :param multiple_path: multiple.txt 文件的绝对路径
    :return: 返回一个装有 DataFrame 对象的集合
    """
    try:
        # 装载 multiple.txt
        multiple_file = Path(multiple_path)
        # 打开 multiple 文件
        with multiple_file.open('r', encoding='utf-8') as file:
            # 将文件记录的每一行返回成一个字符串，删除多余的制表符和空格
            data_paths = [line.strip() for line in file]

        dataframe_list = []
        # 读取每个装载记录光谱数据的 txt 文件并返回为一个 pandas DataFrame 对象
        for data_path in data_paths:
            try:
                dataframe = get_dataframe(data_path)
                dataframe_list.append(dataframe)
            except FileNotFoundError:
                print(f"File {data_path} not found.")
            except Exception as e:
                print(f"An error occurred while processing {data_path}: {str(e)}")

        return dataframe_list

    except FileNotFoundError:
        raise f"File {multiple_path} not found."

    except Exception as e:
        raise f"An error occurred: {str(e)}"


def main():
    # 设置默认的颜色集合
    tableau = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC949", "#AF7AA1", "#FF9DA7", "#9C755F",
               "#BAB0AC"]
    categorical = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22",
                   "#17becf"]
    colorbrewer = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9",
                   "#bc80bd"]
    # 设置全局属性
    rc['font.name'] = 'Arial'
    rc['tick.width'] = 1.3
    rc['meta.width'] = 1.3
    rc['label.weight'] = 'bold'
    rc['tick.labelweight'] = 'bold'
    rc['ytick.major.size'] = 4.6
    rc['ytick.minor.size'] = 2.3
    rc['xtick.major.size'] = 4.6
    rc['xtick.minor.size'] = 2.3

    # 拿到 multiple.txt 中记录的数据，并将其保存为 DataFrame 对象
    data_list = read_multiple("multiple.txt")
    # 图例文本集合
    label_list = ["Acetaldehyde", "Methyl acetate", "Acetone", "N-Methylacetamide"]

    # 创建子图和坐标轴
    fig = pplt.figure(figsize=(5, 1.5 * len(data_list)), dpi=300, span=True, share=True)
    axs = fig.subplots(nrows=4, ncols=1)

    # 根据 DataFrame 的数据绘制多个子图的光谱图
    for ax, data, color, label in zip(axs, data_list, tableau, label_list):
        # 绘制折线图
        ax.plot(data['x'], data['y'], color=color, linewidth=1.3, label=label)
        # 显示图例
        ax.legend(loc='best', fontweight='bold', frame=False)

    # 将多子图的 x 标题和 y 标题 合并
    fig.supylabel("Absorption (in L/mol/cm)", fontsize=11.5)
    fig.supxlabel("Frequency (in cm^-1)", fontsize=11.5)

    # 设置图像的一些杂属性，如果开启多子图绘制时，可以选择是否显示子图的序号。
    axs.format(
        xlabel='', ylabel='',
        grid=False, xlocator=500, ylocator=1000, xlim=(0, 4000), ylim=(0, 3000),
        abc="(a)", abcloc="ul", xminorlocator=250, yminorlocator=500
    )

    plt.show()


if __name__ == '__main__':
    main()
