from matplotlib import pyplot as plt
from pandas import DataFrame


class Spectrum:
    def __init__(self, spectrum_type):
        self.spectrum_type = spectrum_type

    def plot(self, dataframe: DataFrame):
        raise NotImplementedError


class NMRSpectrum(Spectrum):
    def plot(self, dataframe: DataFrame):
        # 创建画布和子图对象
        fig, ax = plt.subplots()

        return fig, ax


class IRSpectrum(Spectrum):
    def plot(self, dataframe: DataFrame):
        pass
