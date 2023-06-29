import argparse
from kd_parser import *
from kd_plot import *
from kd_data import *

def parse_args():
    parser = argparse.ArgumentParser(description='Draw energy profile plot using matplotlib')
    parser.add_argument('input_file', type=str, help='path to input data file')
    parser.add_argument('-s', '--save_name', type=str, default='figure', help='name of the output image file')
    return parser.parse_args()

def main():
    args = parse_args()
    # 读取数据    
    data = KDFileParser(args.input_file).parse().get_kd_data()
    # 判断 save_name 是否为空
    if args.save_name == None:
        kd_draw(data)
    else:
        kd_draw(data, args.save_name)
