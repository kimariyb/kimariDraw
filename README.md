<div align="center">
    <img src="figure/logo.png" width="250px"  alt=""/>
</div>

---

kimariDraw 是一个用于绘制化学反应能量折线图的 Python 命令行程序，使用 Matplotlib 和 Numpy 库实现绘图功能。其目的是为了更方便的绘制出化学反应能量折线图，特别是在每周的组会上，需要你绘制化学反应能量折线图的时候，kimariDraw 能快速的帮你制作出化学反应能量折线图。

## 安装

你可以通过以下命令使用 pip 安装 kimariDraw，除此之外还需要确保已经安装了 Matplotlib 和 Numpy。

```bash
pip install kimariDraw
pip install Numpy
pip install Matplotlib
```

除此之外，还可以直接从 Github 上 clone。

```bash
git clone https://github.com/kimariyb/kimariDraw.git
```

## 使用

使用 kimariDraw 绘制折线图需要一个 .kd 格式的文件。该文件应包含绘制折线图所需的数据和参数。以下是一个 .kd 文件的示例：

```basic
# UNIT = Hartree
# TEMPERATURE = 398
# FIGURE_SIZE = 8, 4
# COLOR_THEME = science
# FONT_FAMILY = Arial
# SAVE_IMAGE = png

BEGIN
1, 375.5
2, 405.5
3, 323.7
4, 457.8
5, 300.6
6, 346.9
END
```

文件头格式，文件头必须以 # 开头，包含键值对，以 : 分隔，例如 # UNIT = kj/mol，key 不区分大小写。数据行格式，数据行格式以 BEGIN 开头，用逗号分隔，表示反应进度和能量。数据行每行包含两个数，第一个数表示反应进度，从 1 开始，后面的数表示能量，数据行以 END 开头的行结束。


- UNIT: 能量单位，例如 kJ/mol
- TEMPERATURE: 温度，例如 298，默认为开尔文温度
- FIGURE_SIZE: 画布大小，例如 8,6
- COLOR_THEME: 颜色主题，例如 nature
- FONT_FAMILY: 坐标字体，例如 Times New Roman
- SIVE_IMAGE: 保存的图片格式，例如 PNG

使用 kimariDraw 绘制折线图的命令如下：

```bash
kimariDraw <filename>
```

其中 <filename> 是一个 .kd 格式的文件。

假如要运行 example 目录下的 test2.kd 文件，并且生成 test.png 则可以输入以下指令：

```bash
kimariDraw ./example/test2.kd -s test
```

则可以在当前目录下得到 test.png:

<img src="figure/test.png">

## 支持的参数

kimariDraw 支持以下命令行参数：

- `-s`, `--save_name`：指定输出文件名，默认为 figure.png

## 作者

kimariDraw 是由 kimariyb 开发的。

## 许可证

kimariDraw 使用 MIT 许可证。详细信息请参考 LICENSE 文件。