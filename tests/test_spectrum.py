from src.Parser.parser_factory import ParserFactory
from src.Spectrum.spectrum_factory import SpectrumFactory


def test():
    data = ParserFactory.create_parser("../data/NMR_curve.xlsx").parse()
    print(data)
    SpectrumFactory.create_spectrum("NMR").plot(data)


if __name__ == "__main__":
    test()
