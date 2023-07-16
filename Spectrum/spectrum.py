from pandas import DataFrame


class Spectrum:
    def __init__(self, spectrum_type):
        self.spectrum_type = spectrum_type
        self.x_limits = None
        self.y_limits = None
        self.figure_size = None
        self.curve_colors = None
        self.save_format = None

    def plot_spectrum(self, dataframe: DataFrame):
        raise NotImplementedError

