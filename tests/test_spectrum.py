from Parser.parser_factory import ParserFactory
from Spectrum.spectrum_factory import SpectrumFactory


def test():
    data = ParserFactory.create_parser('../data/IR_curve.txt').parse()
    ir_spectrum = SpectrumFactory.create_spectrum('IR')
    fig, ax = ir_spectrum.plot_spectrum(data)
    print(ir_spectrum.save_format)
    fig.show()


if __name__ == "__main__":
    test()

