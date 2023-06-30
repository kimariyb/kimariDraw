from kimariDraw.Data.kd_data import KDData


class KDFile:
    def __init__(self, header, data):
        """
        初始化方法，接收一个头部字典和一个数据列表作为参数
        """
        self.header = header
        self.data = data

    def __str__(self):
        """
        返回 KDFile 对象的字符串表示
        """
        return f"Header: {self.header}\nData: {self.data}"

    def get_kd_data(self):
        """
        返回 KDDate 对象的数据列表
        """
        unit = self.header["unit"]
        figure_size = self.header["figure_size"]
        color_theme = self.header["color_theme"]
        font_family = self.header["font_family"]
        plot_style = self.header["plot_style"]
        num_data = self.data

        kd_data = KDData(unit, figure_size, color_theme, font_family, plot_style, num_data)
        return kd_data
