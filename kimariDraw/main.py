import argparse

from kimariDraw.Parser.kd_parser import KDFileParser
from kimariDraw.Plot.kd_plot import kd_draw


def parse_args():
    parser = argparse.ArgumentParser(description='Draw energy profile plot using matplotlib')
    parser.add_argument('input_file', type=str, help='path to input data file')
    parser.add_argument('-s', '--save_name', type=str, default='figure.png', help='name of the output image file')
    return parser.parse_args()


def main():
    args = parse_args()
    # 读取数据    
    data = KDFileParser(args.input_file).parse().get_kd_data()
    # 判断 save_name 是否为空
    if args.save_name is None:
        kd_draw(data)
    else:
        kd_draw(data, args.save_name)


if __name__ == "__main__":
    main()
