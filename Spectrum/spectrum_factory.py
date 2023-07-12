from Spectrum.spectrum_IR import IRSpectrum
from Spectrum.spectrum_NMR import NMRSpectrum
from Spectrum.spectrum_Raman import RamanSpectrum


class SpectrumFactory:
    @staticmethod
    def create_spectrum(spectrum_type):
        if spectrum_type == "NMR":
            return NMRSpectrum()
        elif spectrum_type == "IR":
            return IRSpectrum()
        elif spectrum_type == "Raman":
            return RamanSpectrum()
        else:
            raise ValueError("Unsupported spectrum type")
