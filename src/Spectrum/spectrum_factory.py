from src.Spectrum.spectrum import NMRSpectrum, IRSpectrum


class SpectrumFactory:
    @staticmethod
    def create_spectrum(spectrum_type):
        if spectrum_type == "NMR":
            return NMRSpectrum(spectrum_type)
        elif spectrum_type == "IR":
            return IRSpectrum(spectrum_type)
        else:
            raise ValueError("Unsupported spectrum type")
