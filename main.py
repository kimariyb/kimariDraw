from matplotlib import pyplot as plt

from Parser.parser_factory import ParserFactory
from Utils.plot import plot_spectrum, plot_multi_spectrum
from Utils.utils import welcome, input_file_path, main_view, single_or_multiple


def set_global_plot_settings():
    # 设置全局字体、字重和轴线宽度
    plt.rcParams.update({
        'font.family': 'Arial',
        'font.weight': 'bold',
        'axes.linewidth': 1.5
    })


def main():
    while True:

        # 设置欢迎界面
        welcome()

        # 设置全局字体、字重和轴线宽度
        set_global_plot_settings()

        # 输入文件路径，并处理异常
        url = input_file_path()

        while True:
            # 选择绘制 Single 还是 Multiple
            first_choice = single_or_multiple()
            if first_choice == '0':
                # 如果选择 0 则返回输入路径
                break
            elif first_choice == '1':
                # 如果选择 1 则绘制 Single
                # 从 Parser 工厂中创建一个 Parser，并处理异常
                try:
                    parser = ParserFactory.create_parser(url)
                    dataframe = parser.parse()
                except Exception as e:
                    raise ValueError(f"Error parsing data from file: {url}: {e}")

                while True:
                    # 主页面
                    main_choice = main_view()
                    if main_choice == '0':
                        break  # 退出当前的内部循环
                    elif main_choice == '1':
                        plot_spectrum(dataframe, 'NMR')
                    elif main_choice == '2':
                        plot_spectrum(dataframe, 'IR')
                    elif main_choice == '3':
                        plot_spectrum(dataframe, 'Raman')
                    elif main_choice == '4':
                        plot_spectrum(dataframe, 'UV')
                    elif main_choice == '5':
                        plot_spectrum(dataframe, 'ECD')
                    elif main_choice == '6':
                        plot_spectrum(dataframe, 'VCD')
                    elif main_choice == '7':
                        plot_spectrum(dataframe, 'PES')
                    else:
                        print("Unknown choice. Please enter a valid option.")

            elif first_choice == '2':
                # 如果选择 2 则绘制 Multiple
                # 如果选择 1 则绘制 Single
                # 从 Parser 工厂中创建一个 Parser，并处理异常
                try:
                    parser = ParserFactory.create_parser(url)
                    dataframe = parser.parse_multi()
                except Exception as e:
                    raise ValueError(f"Error parsing data from file: {url}: {e}")

                while True:
                    # 主页面
                    main_choice = main_view()
                    if main_choice == '0':
                        break  # 退出当前的内部循环
                    elif main_choice == '1':
                        plot_multi_spectrum(dataframe, 'NMR')
                    elif main_choice == '2':
                        plot_multi_spectrum(dataframe, 'IR')
                    elif main_choice == '3':
                        plot_multi_spectrum(dataframe, 'Raman')
                    elif main_choice == '4':
                        plot_multi_spectrum(dataframe, 'UV')
                    elif main_choice == '5':
                        plot_multi_spectrum(dataframe, 'ECD')
                    elif main_choice == '6':
                        plot_multi_spectrum(dataframe, 'VCD')
                    elif main_choice == '7':
                        plot_multi_spectrum(dataframe, 'PES')
                    else:
                        print("Unknown choice. Please enter a valid option.")


if __name__ == '__main__':
    main()
