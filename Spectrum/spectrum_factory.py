from Spectrum.Spectrum_PES import PESSpectrum
from Spectrum.spectrum_ECD import ECDSpectrum
from Spectrum.spectrum_IR import IRSpectrum
from Spectrum.spectrum_NMR import NMRSpectrum
from Spectrum.spectrum_Raman import RamanSpectrum
from Spectrum.spectrum_UV import UVSpectrum
from Spectrum.spectrum_VCD import VCDSpectrum


class SpectrumFactory:
    @staticmethod
    def create_spectrum(spectrum_type):
        if spectrum_type == "NMR":
            return NMRSpectrum()
        elif spectrum_type == "IR":
            return IRSpectrum()
        elif spectrum_type == "Raman":
            return RamanSpectrum()
        elif spectrum_type == "UV":
            return UVSpectrum()
        elif spectrum_type == "ECD":
            return ECDSpectrum()
        elif spectrum_type == "VCD":
            return VCDSpectrum()
        elif spectrum_type == "PES":
            return PESSpectrum()
        else:
            raise ValueError("Unsupported spectrum type")
