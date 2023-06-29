import numpy as np
import matplotlib.pyplot as plt

from kimariDraw.Data.kd_data import KDData


def kd_draw(data: KDData, save_name='figure'):
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
    ax.set_xlim(0, np.max(num_x) + 1)
    y_min = np.min(num_y) * 1.25 if np.min(num_y) < 0 else np.min(num_y) * 0.75
    y_max = np.max(num_y) * 1.25 if np.max(num_y) > 0 else np.max(num_y) * 0.75
    ax.set_ylim(y_min, y_max)

    # 绘制平台
    # 绘制数据点
    # for i in range(len(num_x)):
    #    ax.scatter(num_x[i], num_y[i])

    # 在每个数据点上绘制长度为 0.4 的水平线
    for i, (x, y) in enumerate(zip(num_x, num_y)):
        ax.plot([x - 0.2, x + 0.2], [y, y], color='black', linewidth=3)
        if abs(y) > 100:
            ax.text(x, y + 2, f"{y:.1f}", ha='center', va='bottom', fontweight='bold', fontsize=10)
        else:
            ax.text(x, y + 0.5, f"{y:.1f}", ha='center', va='bottom', fontweight='bold', fontsize=10)

    for i in range(len(num_x) - 1):
        ax.plot([num_x[i]+0.2, num_x[i+1]-0.2], [num_y[i], num_y[i+1]],  color='black', linewidth=1, linestyle='--')

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
    save_fig_url = save_name + "." + data.save_image
    plt.savefig(save_fig_url, dpi=700)

    # 显示图像
    plt.show()
