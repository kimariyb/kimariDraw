from src.Parser.parser_factory import ParserFactory
from src.Spectrum.spectrum_factory import SpectrumFactory


def test():
    data = ParserFactory.create_parser("../data/NMR_curvewei.txt").parse()
    print(data)
    nmr_spectrum = SpectrumFactory.create_spectrum("NMR")
    nmr_spectrum.load_dataframe(data)
    fig, ax = nmr_spectrum.plot_spectrum()
    fig.show()


if __name__ == "__main__":
    test()
