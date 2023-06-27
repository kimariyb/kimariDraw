from kd_parser import KDFileParser

if __name__ == '__main__':
    url = "./test_data/test1.kd"
    kd_data = KDFileParser(url).parse().get_kd_data()
    print(kd_data)

    print(kd_data.get_num_x())
