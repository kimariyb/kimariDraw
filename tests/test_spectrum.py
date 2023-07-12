from Parser.parser_factory import ParserFactory
from Spectrum.spectrum_factory import SpectrumFactory


def test():
    ParserFactory.create_parser('../data/NMR_curve.txt')
    ir_spectrum = SpectrumFactory.create_spectrum('IR')
    ir_spectrum.plot_spectrum()


if __name__ == "__main__":
    test()

