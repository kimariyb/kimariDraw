import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


from kd_data import KDData


class KDProfile:
    def __init__(self, x, y, data: KDData):
        self.x = x
        self.y = y
        self.data = data

    def set_font(self):
        font = self.data.font_family
        if font == 'Arial':
            axis_font = FontProperties(family='sans-serif', size=14)
            axis_font.set_name("Arial")
            axis_font.set_weight("bold")
        elif font == 'Times New Roman':
            axis_font = FontProperties(family='serif', size=14)
            axis_font.set_name("Times New Roman")
            axis_font.set_weight("bold")

    def set_color(self):
        pass

    def set_figure(self):
        pass

    def save_figure(self):
        pass
