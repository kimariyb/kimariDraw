from kd_parser import KDFileParser
from kd_plot import *

if __name__ == '__main__':
    url = "./test_data/test2.kd"
    kd_data = KDFileParser(url).parse().get_kd_data()
    print(kd_data)
    print(type(kd_data.figure_size))
    print(kd_data.get_num_x())
    print(kd_data.get_num_y())
    print(kd_data.get_numpy_array())
    
    kd_draw(kd_data)





