import configparser
import os


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
    spike_colors = None
    if section == 'NMR':
        config.get(section, 'spike_color')
    x_limit = tuple(map(float, config.get(section, 'x_limit').split(',')))
    y_limit = tuple(map(float, config.get(section, 'y_limit').split(',')))

    return figure_size, x_limit, y_limit, curve_colors, spike_colors, save_format


def read_nmr_config(filename):
    return read_config('NMR', filename)


def read_ir_config(filename):
    return read_config('IR', filename)


def read_raman_config(filename):
    return read_config('Raman', filename)


def read_uv_config(filename):
    return read_config('UV', filename)
