import numpy as np
import openpyxl
import pandas as pd


class Parser:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        raise NotImplementedError


class TXTParser(Parser):
    def parse(self):
        # 从 txt 文件中读取数据
        data = np.loadtxt(self.filename)
        # 将数据转换为 DataFrame 对象
        df = pd.DataFrame(data, columns=['x', 'y'])
        return df


class ExcelParser(Parser):
    def parse(self):
        # 打开 Excel 文件
        wb = openpyxl.load_workbook(self.filename)
        # 选择工作表
        ws = wb['Sheet1']
        # 读取数据
        data = []
        for row in ws.iter_rows(values_only=True):
            data.append({'x': row[0], 'y': row[1]})

        # 将数据转换为 DataFrame 对象
        df = pd.DataFrame(data)
        return df
