from Spectrum.spectrum_IR import IRSpectrum
from Spectrum.spectrum_NMR import NMRSpectrum


class SpectrumFactory:
    @staticmethod
    def create_spectrum(spectrum_type):
        if spectrum_type == "NMR":
            return NMRSpectrum()
        elif spectrum_type == "IR":
            return IRSpectrum()
        else:
            raise ValueError("Unsupported spectrum type")
