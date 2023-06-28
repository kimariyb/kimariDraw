import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


from kd_data import KDData


def kd_draw(data: KDData):
    """_summary_

    Args:
        data (KDData): _description_
    """
    
    # 设置全局字体
    plt.rcParams['font.family'] = data.font_family
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.linewidth'] = 1.5
    
    num_x = data.get_num_x()
    num_y = data.get_num_y()
    
    # 将所有的浮点数修改为字符串
    str_x = [f'{num:.2f}' for num in num_x]
        
    # 创建画布和子图对象
    plt.figure(figsize=data.figure_size)
    bars = plt.bar(str_x, num_y, width=0.4, edgecolor='black', linewidth=2.5)
    
    # 将整个条形都变透明
    for bar in bars:
        bar.set_facecolor('none')

    # 在图上显示数值
    for a, b in zip(str_x, num_y):
        plt.text(x=a,
            y=b + 0.02 * np.max(data.get_num_y()),
            s='{:.1f}'.format(b),
            ha='center',
            fontsize=9
        )
    
    # 设置 x 轴和 y 轴的范围
    plt.ylim(np.min(data.get_num_y())*0.9, np.max(data.get_num_y())*1.1)
    
    # 设置 x 轴和 y 轴标签
    y_label = "Free Energy" + f" ({data.unit})" 
    plt.xlabel("", fontweight='bold', fontsize=12)
    plt.ylabel(y_label, fontweight='bold', fontsize=12)
    
    # 隐藏 x 轴坐标和 y 轴坐标
    plt.tick_params(axis='both', which='both', length=0)
    plt.tick_params(labelbottom=False, labelleft=False)
    
    # 设置标题
    plt.title("Chemical Energy Profile", fontweight='bold', fontsize=16)
    
    # 保存路径
    save_fig_url = "figure." + data.save_image
    plt.savefig(save_fig_url, dpi=800)
    
    plt.show()
    
