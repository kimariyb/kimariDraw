<h1 align="center">
    <img src="figure/logo.png" width="120">
</h1><br>


KimariDraw 是一款开源的 Python 脚本，旨在绘制各种光谱图形，特别适用于处理著名的波函数分析程序 Multiwfn  生成的光谱数据。它能够将 Multiwfn 生成的数据以美观、清晰的方式重新绘制成单曲线单子图、多曲线单子图、单曲线多子图以及多曲线多子图。

当你使用 KimariDraw 时，你可以享受到以下的功能：

- **支持多种光谱类型**：KimariDraw 支持使用 Multiwfn 绘制 NMR、IR 等光谱导出的数据，即 Multiwfn 生成的文本文件。

- **支持多子图绘制**：KimariDraw 不仅支持一单子图的绘制，同时也支持多子图的绘制（多子图的绘制功能在 2.5.1 版本之后就不存在了，但是在 2.4.0 版本还保留）。

- **支持多种文件格式**：KimariDraw 支持将图片导出为多种文件格式，如 PNG、JPG、PDF、SVG 等。

- **易于安装和配置**：KimariDraw 的安装和配置十分简单，您只需要按照项目 README 文件中的说明进行操作即可。

- **自定义功能强大**：KimariDraw 可以根据需要自定义曲线的颜色、图例以及格式，可以达到科研论文要求。

Multiwfn 是一个非常强大的波函数分析程序。Multiwfn 免费、开源、高效、灵活，它支持几乎所有最重要的波函数分析方法。目前，Multiwfn 是量子化学领域的常用工具之一，得到了广泛的应用和认可。

**如果您对 Multiwfn 还不熟悉，请访问 [Multiwfn 官网](http://sobereva.com/multiwfn/)了解更多信息。**

## 安装

**推荐！** 我们推荐使用 anaconda 虚拟环境进行安装，方便对包进行管理，同时也不会影响其他项目的环境。

1. 如果没有安装 Python，可以不用安装 Python，直接前往 [anaconda 官网](https://www.anaconda.com/)下载 anaconda 最新版本。安装并配置好以后，使用 anaconda 新建一个环境。

```shell
conda create -n KimariDraw python=3.8.13
```

2. 激活名为 kimaridraw 的 conda 环境：

```shell
conda activate KimariDraw
```

3. 使用 pip 工具安装 kimaridraw

```shell
pip install KimariDraw
```

4. 安装 kimaridraw 所需要的包和库：

```shell
pip install pandas==1.4.3 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install numpy==1.23.5 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install proplot==0.9.5 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install matplotlib==3.4.3 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install toml==0.10.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install setuptools==68.0.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install wxpython==4.2.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install openpyxl==3.1.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

这将安装 KimariDraw 所需的 pandas、matplotlib 和 proplot 等依赖项。同时，由于激活的 conda 环境，因此 pip 安装的包只会在 kimaridraw 环境下使用，如果不激活就不会被使用。这样就很好的避免了不同任务依赖的环境不同，所导致的版本冲突。

## 使用

在使用 KimariDraw 之前，必须使用 Multiwfn 自行根据量子化学计算程序生产的各种光谱计算产生的 `.out` 文件得到光谱的数据。如果不了解如何使用 Multiwfn 绘制各类光谱，可以浏览 Sob 的 [使用Multiwfn绘制红外、拉曼、UV-Vis、ECD、VCD和ROA光谱图](http://sobereva.com/224)。

**请注意：在正式运行前，请确保已经安装了 KimariDraw 所需要的模块和包，以免程序报错！**

1. 如果使用 pip 安装了 KimariDraw，可以直接在终端中运行 KimariDraw

```shell
KimariDraw
```

2. 接着程序显示程序头以及提示你要你选择一个 toml 文件，所有的指令和提示非常清晰，比如输入 `q` 可以直接退出，按空格可以使用 GUI 选择 toml 文件。

```shell
KimariDraw --  A Python script that processes Multiwfn spectral data and plots various spectra.
Version: 2.5.1.1, release date: Aug-18-2023                             
Developer: Kimariyb, Ryan Hsiun                                         
KimariDraw home website: https://github.com/kimariyb/kimariDraw

(Copyright © 2023 Kimariyb. Currently timeline: Aug-18-2023, 00:45:26)

Input toml file path, for example E:\Hello\World.toml
Hint: Press ENTER button directly can select file in a GUI window. If you want to exit the program, simply type the letter "q" and press Enter. 
```

3. 输入 toml 文件之后就可以进入主程序页面，接着可以输入命令，每一个命令的含义都在屏幕上显示的非常清楚。假如想直接看看默认的绘图效果，可以输入 `0`。当然大部分情况下，默认的设置都不太可能满足用户的需求，这时候可以输入其他命令修改绘图的设置。最后可以使用命令 `1` 保存图片。

```shell
 "q": Exit program gracefully    "r": Load a new file
********************************************************
****************** Main function menu ******************
********************************************************
-1 Set font family of the spectrum, current: Arial
-2 Set font size of the spectrum, current: [10.5, 12, 14]
-3 Set title/xlabel/ylabel of the spectrum
-4 Set format of saving spectrum file, current: png
-5 Set dpi of saving spectrum, current: 300
-6 Set figure size of spectrum file, current: (6, 4)
0 Plot spectrum!
1 Save graphical file of the spectrum in current folder
2 Set lower and upper limit of X-axis, current: auto
3 Set lower and upper limit of Y-axis, current: auto
4 Showing legend text, current: auto
5 Showing the zero axis, current: auto
```


## 有关 toml 文件

toml 文件是一种用来记录 key-value 的特殊的文件格式。KimariDraw 必须使用 toml 文件作为输入文件。KimariDraw 所需要的 toml 文件格式如下所示，如果有自己的需求可以根据下面的提示自行修改 toml 文件。

```toml
# file 模块用来记录绘图的数据来源，例如 txt 文件和 xlxs 文件
[[file]]
# 记录绘图的数据来源的 txt 文件或者 xlxs 文件的路径，推荐使用绝对路径
path = "UV_curve.txt"
# 配置图例的文本，可以选择一个字符串类型的，也可以选择一个记录多个字符串的集合
legend = ["style: -", "style: --", "style: -", "S0->S11", "S0->S13"]
# 配置曲线的颜色，可以选择一个字符串类型的，也可以选择一个记录多个字符串的集合
# 如果为空，则使用默认的颜色主题，其他的颜色主题可以再程序中配置
color = ["black", "red", "orange", "yellow", "blue"]
# 配置曲线的格式，可以选择一个字符串类型的，也可以选择一个记录多个字符串的集合
# 如果为空，则所有曲线都是 "-" 类型
style = ["-", "--", "--", "--", "--"]
```

`color` 可以使用 `black`、`blue` 这类直接用名字代表的颜色，也可以使用十六进制颜色，例如 `#FFFFFF`

<img src="figure/color.svg">

`style` 可以使用 `"-"、"--"、"-."、":"` 这种字符串代表的 linestyle，也可以是一些元组，例如 `(0, (1, 10))`。

<img src="figure/linestyles.png">

```python
linestyle_str = [
     ('solid', 'solid'),      # Same as (0, ()) or '-'
     ('dotted', 'dotted'),    # Same as (0, (1, 1)) or ':'
     ('dashed', 'dashed'),    # Same as '--'
     ('dashdot', 'dashdot')]  # Same as '-.'

linestyle_tuple = [
     ('loosely dotted',        (0, (1, 10))),
     ('dotted',                (0, (1, 1))),
     ('densely dotted',        (0, (1, 1))),
     ('long dash with offset', (5, (10, 3))),
     ('loosely dashed',        (0, (5, 10))),
     ('dashed',                (0, (5, 5))),
     ('densely dashed',        (0, (5, 1))),

     ('loosely dashdotted',    (0, (3, 10, 1, 10))),
     ('dashdotted',            (0, (3, 5, 1, 5))),
     ('densely dashdotted',    (0, (3, 1, 1, 1))),

     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))]
```

## 绘制效果

1. 示例文件：`example/uv.toml`

<img src="figure/uv.png">

2. 示例文件：`example/ecd.toml`

<img src="figure/ecd.png">

## 使用脚本批量生成光谱

KimariDraw 程序中自带了一个用 KimariDraw 程序批量绘制光谱的脚本。如果需要批量绘制光谱，可以在 `script` 文件夹中找到这个脚本。由于绘制光谱通常在 Windows 系统下进行，所以只提供了能在 Windows 下运行的 batch 脚本 `SpecDraw.exe`。想要使用 `SpecDraw.exe` 脚本必须同时提供一个 `draw.txt` 文件，该文件记录了运行 KimariDraw 所需要使用到的命令。有关 `SpecDraw.exe` 的详细信息可以浏览 SpecDraw 的主页 https://github.com/kimariyb/SpecDraw

## 使用脚本批量产生光谱数据

KimariDraw 程序中自带了一个用来批量产生 Multiwfn 光谱数据的脚本。如果想要批量产生绘制光谱的数据，可以在 `script` 文件夹中找到这个脚本。其中 `GenData.sh` 为 Linux 系统下的脚本，`GenData.bat` 为 Windows 系统下的脚本。

`GenData.sh` 以及 `GenData.bat` 都需要一个名为 `commands.txt` 的文件。`commands.txt` 文件包含了执行 Multiwfn 生成数据所需要的命令，如果想要使用这个脚本，则必须对 Multiwfn 有一定的了解。


## 鸣谢

在开发 KimariDraw 时，主要使用了以下 Python 开源模组，在这里对开发这些模组的工作人员表示感谢。

- **numpy**, https://numpy.org/
- **pandas**, https://pandas.pydata.org/
- **matplotlib**, https://matplotlib.org/
- **proplot**, https://proplot.readthedocs.io/en/latest/
- **wxpython**, https://www.wxpython.org/
- **toml**, https://github.com/uiri/toml
- **setuptools**, https://github.com/pypa/setuptools
- **openpyxl**, https://openpyxl.readthedocs.io/en/stable/

## 许可证

KimariDraw 基于 MIT 许可证开源。这意味着您可以自由地使用、修改和分发代码。

## 如何使用老版本

由于 2.5.1 版本以及以后的所有版本，都不会保留绘制多子图功能，因此对于想要绘制多子图的同学比较难受。如果非要使用 KimariDraw 绘制多子图，可以选择老版本也就是 2.4.0 版本。

直接 clone 本项目后，就可以在 `v2.4 (old version)` 文件夹里找到具体的安装以及使用方法。

```shell
git clone https://github.com/kimariyb/kimariDraw.git
```