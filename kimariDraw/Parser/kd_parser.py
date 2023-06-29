import os.path

from kimariDraw.Parser.kd_file import KDFile


class KDFileParser:
    def __init__(self, filepath):
        """
        初始化方法，接收一个文件路径作为参数
        """
        self.filepath = filepath

    def parse(self):
        """
        解析符合 .kd 文件格式的文件，返回一个 KDFile 对象
        """
        header, data = self._parse_file()
        return KDFile(header, data)

    def _validate(self):
        """
        验证符合上述格式的 KD 文件是否存在数据行。
        如果存在数据行，返回 True；否则返回 False。
        """
        # 确保文件后缀为 .kd
        if not self.filepath.endswith('.kd'):
            print(f"{self.filepath} 不是一个 KD 文件")
            return False

        # 确保文件存在
        if not os.path.isfile(self.filepath):
            print(f"{self.filepath} 文件不存在")
            return False

        # 验证是否存在数据行
        with open(self.filepath, 'r', encoding="utf-8") as f:
            begin_found = False
            for line in f:
                line = line.strip()
                if line == 'BEGIN':
                    begin_found = True
                elif line == 'END':
                    return begin_found

        return False  # 没有找到 BEGIN 和 END 标记，返回 False

    def _parse_file(self):
        """
        解析文件，返回头部字典和数据列表
        """
        if not self._validate():
            raise ValueError('Invalid KD file format')

        header = {'unit': None,
                  'figure_size': None,
                  'color_theme': None,
                  'font_family': None,
                  'save_image': None}

        data = []

        with open(self.filepath, 'r', encoding="utf-8") as f:
            lines = f.readlines()

        # 解析文件头
        for line in lines[:5]:
            key, value = line[2:].strip().split(' = ')
            if key == 'FIGURE_SIZE':
                width, height = map(int, value.split(','))
                header[key.lower()] = (width, height)
            else:
                header[key.lower()] = value

        # 解析数据行
        data_started = False
        for line in lines:
            if data_started:
                if line.strip() == 'END':
                    break
                x_str, y_str = line.strip().split(',')
                x, y = float(x_str), float(y_str)
                data.append((x, y))
            elif line.strip() == 'BEGIN':
                data_started = True

        return header, data
