from Parser.parser_factory import ParserFactory
from Spectrum.spectrum_factory import SpectrumFactory


def test():
    data = ParserFactory.create_parser('../data/multi_curve.txt').parse_multi()
    print(data)
    fig, ax = SpectrumFactory.create_spectrum('UV').plot_multi_spectrum(data)
    fig.show()


if __name__ == "__main__":
    test()

