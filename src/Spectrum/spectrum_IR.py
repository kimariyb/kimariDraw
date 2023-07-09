from matplotlib import pyplot as plt
from pandas import DataFrame

from src.Spectrum.spectrum import Spectrum


class IRSpectrum(Spectrum):
    def __init__(self):
        super().__init__('IR')


