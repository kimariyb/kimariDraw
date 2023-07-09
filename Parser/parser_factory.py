from Parser.parser import TXTParser, ExcelParser


class ParserFactory:
    @staticmethod
    def create_parser(filename):
        if filename.endswith('.txt'):
            return TXTParser(filename)
        elif filename.endswith('.xlsx'):
            return ExcelParser(filename)
        else:
            raise ValueError('Unsupported file type')
