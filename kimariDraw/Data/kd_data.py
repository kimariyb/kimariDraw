import numpy as np


class KDData:

    def __init__(self, unit, figure_size, color_theme, font_family, plot_style, num_data):
        self.unit = unit
        self.figure_size = figure_size
        self.color_theme = color_theme
        self.font_family = font_family
        self.plot_style = plot_style
        self.num_Data = num_data

    def __str__(self):
        return f"KDData(unit={self.unit}, figure_size={self.figure_size}, color_theme={self.color_theme}, font_family={self.font_family}, plot_style={self.plot_style}, num_data={self.num_Data})"

    def get_num_x(self):
        """
        Returns the number of x-axis values
        """
        x = []
        for item in self.num_Data:
            x.append(item[0])

        return x

    def get_num_y(self):
        """
        Returns the number of y-axis values
        """
        y = []
        for item in self.num_Data:
            y.append(item[1])

        return y

    def get_numpy_array(self):
        """
        Returns the data as a numpy array
        """
        return np.array([self.get_num_x(), self.get_num_y()])

