import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from kimariDraw.Data.kd_data import KDData

def modify_style(style):
    """
    修改折线图样式，一种为折线图、另一种为曲线图
    :param style: 样式
    :return:
    """
    pass


def kd_draw(data: KDData, save_name='figure.png'):
    """
    使用 matplotlib 绘制能量折线图
    """
    # 设置全局字体
    plt.rcParams['font.family'] = data.font_family
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.linewidth'] = 1.5

    num_x = data.get_num_x()
    num_y = data.get_num_y()

    # 创建画布和子图对象
    fig, ax = plt.subplots(figsize=data.figure_size)

    # 设置 x 轴和 y 轴的范围
    y_min = np.min(num_y)
    y_max = np.max(num_y)
    x_max = np.max(num_x)
    x_min = np.min(num_x)
    ax.set_xlim(0, x_max + 1)
    # 处理最小值为 0 时，不扩展 y 轴范围的情况
    if y_min == 0:
        y_max *= 1.25 if y_max > 0 else 0.75
        y_min = -15
    else:
        y_min *= 1.25 if y_min < 0 else 0.75
        y_max *= 1.25 if y_max > 0 else 0.75

    ax.set_ylim(y_min, y_max)

    # 更改颜色主题
    colors = []
    if data.color_theme == 'normal':
        colors = ['black', 'black']
    elif data.color_theme == 'nature':
        colors = ['#0072B2', '#D55E00']
    elif data.color_theme == 'science':
        colors = ["#1b9e77", "#d95f02"]

    # 修改折线图样式，一种为折线图、另一种为曲线图
    if data.plot_style == 'line':
        # 绘制平台
        # 在每个数据点上绘制长度为 0.4 的水平线，并在水平线上显示数字
        for i, (x, y) in enumerate(zip(num_x, num_y)):
            ax.plot([x - 0.2, x + 0.2], [y, y], color=colors[0], linewidth=3)
            if abs(y) > 100:
                ax.text(x, y + 2, f"{y:.1f}", ha='center', va='bottom', fontweight='bold', fontsize=10, color=colors[1])
            else:
                ax.text(x, y + 0.5, f"{y:.1f}", ha='center', va='bottom', fontweight='bold', fontsize=10,
                        color=colors[1])
        # 以折线连接平台
        for i in range(len(num_x) - 1):
            ax.plot([num_x[i] + 0.2, num_x[i + 1] - 0.2], [num_y[i], num_y[i + 1]], color=colors[0], linewidth=1,
                    linestyle='--')
    elif data.plot_style == 'curve':
        raise ValueError('不支持的绘图样式')

    # 设置 x 轴和 y 轴标签
    y_label = "Free Energy" + f" ({data.unit})"
    ax.set_xlabel("Reaction Coordinate", fontweight='bold', fontsize=14)
    ax.set_ylabel(y_label, fontweight='bold', fontsize=14)

    # 设置 x 轴和 y 轴坐标
    ax.tick_params(axis='x', color='white')
    ax.tick_params(axis='x', labelcolor='white')

    # 设置标题
    ax.set_title("Chemical Energy Profile", fontweight='bold', fontsize=16)

    # 保存路径
    plt.savefig(save_name, dpi=700)

    # 显示图像
    plt.show()

