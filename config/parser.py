from pathlib import Path

import toml


class SpectrumData:
    def __init__(self, path, size, xlim, ylim, style="-"):
        """
        初始化 Spectrum 对象
        :param path: 数据文件的路径
        :param size: 图片尺寸
        :param xlim: x 坐标轴大小和间距
        :param ylim: y 坐标轴大小和间距
        :param style: 曲线风格，默认为实线 -，可选择其他选项
        """
        self.path = path
        self.size = size
        self.xlim = xlim
        self.ylim = ylim
        self.style = style

    def __str__(self):
        return f"Data file: {self.path}, Size: {self.size}, xlim: {self.xlim}, ylim: {self.ylim}," \
               f" style: {self.style}"


class IRSpectrumData(SpectrumData):
    def __str__(self):
        return f"IR " + super().__str__()


class UVSpectrumData(SpectrumData):
    def __str__(self):
        return f"UV " + super().__str__()


class NMRSpectrumData(SpectrumData):
    def __str__(self):
        return f"NMR " + super().__str__()


def toml_parse(toml_file: str):
    """
    读取 TOML 文件中的数据，并根据光谱类型创建相应的对象列表
    :param toml_file: toml 文件路径
    :return: 返回各种光谱的对象列表
    """
    # 定义光谱类型和相应的类对象
    spectrum_types = {
        'IR': IRSpectrumData,
        'UV': UVSpectrumData,
        'NMR': NMRSpectrumData
    }

    try:
        # 将 toml 文件保存在 Path 对象中
        file_path = Path(toml_file)
        # 打开 toml 文件并将内容保存在 toml_data 对象中
        with file_path.open('r', encoding='utf-8') as f:
            toml_data = toml.load(f)

        # 根据 toml 文件中的内容自动判断光谱类型，并返回相应的对象列表
        spectrum_data_list = []
        # 自动判断 toml 文件所配置的光谱类型
        for spectrum_type in toml_data:
            if spectrum_type in spectrum_types:
                for spectrum in toml_data[spectrum_type]:
                    plot_data_cls = spectrum_types[spectrum_type]
                    plot_data = plot_data_cls(spectrum['path'], spectrum['size'], spectrum['xlim'],
                                              spectrum['ylim'], spectrum.get('style', '-'))
                    spectrum_data_list.append(plot_data)
        return spectrum_data_list

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{toml_file}' not found.") from e
    except toml.TomlDecodeError as e:
        raise ValueError(f"Error parsing TOML file: {e}") from e
    except KeyError as e:
        raise ValueError(f"Missing required key in TOML file: {e}") from e
    except Exception as e:
        raise Exception(f"An error occurred while parsing the file: {e}") from e


if __name__ == '__main__':
    ir_data_list = toml_parse("../spectrum_ir.toml")
    print(ir_data_list[0])
    print(ir_data_list[1])
