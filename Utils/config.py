import configparser
import os

import yaml


def read_multi_config(filename):
    """
    获得 configuration
    :param filename: 文件名字
    :return: colors_list: 颜色列表
    :return: label_list: 标签列表
    """
    # 构建绝对路径
    file_path = os.path.join(os.path.dirname(__file__), '..', filename)

    # 打开 YAML 文件并读取内容
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    # 获取 color 和 label 列表
    color_list = data['color']
    label_list = data['label']

    return color_list, label_list


def read_config(section, filename):
    """
    获得 configuration
    :param section: section
    :param filename: 文件名字
    :return:
    """
    # 构建绝对路径
    file_path = os.path.join(os.path.dirname(__file__), '..', filename)

    config = configparser.ConfigParser()
    config.read(file_path)

    # 读取配置项
    figure_size = tuple(map(int, config.get(section, 'figure_size').split(',')))
    save_format = config.get(section, 'save_format')
    curve_colors = config.get(section, 'curve_color')
    x_limit = tuple(map(float, config.get(section, 'x_limit').split(',')))
    y_limit = tuple(map(float, config.get(section, 'y_limit').split(',')))

    return figure_size, x_limit, y_limit, curve_colors, save_format


def read_nmr_config(filename):
    return read_config('NMR', filename)


def read_ir_config(filename):
    return read_config('IR', filename)


def read_raman_config(filename):
    return read_config('Raman', filename)


def read_uv_config(filename):
    return read_config('UV', filename)


def read_ecd_config(filename):
    return read_config('ECD', filename)


def read_vcd_config(filename):
    return read_config('VCD', filename)


def read_pes_config(filename):
    return read_config('PES', filename)
