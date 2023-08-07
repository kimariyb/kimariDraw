<h1 align="center">
    <img src="figure/logo.png" width="200">
</h1><br>


KimariDraw 是一款开源的 Python 脚本，旨在绘制各种光谱图形，特别适用于处理著名的波函数分析程序 Multiwfn  生成的光谱数据。它能够将 Multiwfn 生成的数据以美观、清晰的方式重新绘制成单曲线单子图、多曲线单子图、单曲线多子图以及多曲线多子图。

当你使用 KimariDraw 时，你可以享受到以下的功能：

- **支持多种光谱类型**：KimariDraw 支持使用 Multiwfn 绘制 NMR、IR 等光谱导出的数据，即 Multiwfn 生成的文本文件。

- **支持多子图绘制**：KimariDraw 不仅支持一单子图的绘制，同时也支持多子图的绘制。

- **支持多种文件格式**：KimariDraw 支持将图片导出为多种文件格式，如 PNG、JPG、PDF、SVG 等。

- **易于安装和配置**：KimariDraw 的安装和配置十分简单，您只需要按照项目 README 文件中的说明进行操作即可。

- **自定义功能强大**：KimariDraw 可以根据需要自定义曲线的颜色、图例以及格式，可以达到科研论文要求。

Multiwfn 是一个非常强大的波函数分析程序。Multiwfn 免费、开源、高效、灵活，它支持几乎所有最重要的波函数分析方法。目前，Multiwfn 是量子化学领域的常用工具之一，得到了广泛的应用和认可。

**如果您对 Multiwfn 还不熟悉，请访问 [Multiwfn 官网](http://sobereva.com/multiwfn/)了解更多信息。**

## 安装

### 常规安装

1. 首先，安装 Python 环境和 pip 包管理工具。如果您还没有安装它们，请先安装它们。并确保 Python 版本为 3.8 版本，如果和开发的版本不符，有可能无法运行 KimariDraw。

```shell
python==3.8.13
```

2. 下载 KimariDraw 源代码：

```shell
git clone https://github.com/kimariyb/kimariDraw.git
```

3. 进入 KimariDraw 目录并安装依赖：

```shell
cd kimariDraw
pip install -r requirements.txt
```
这将自动安装 KimariDraw 所需的 pandas、matplotlib 和 proplot 等依赖项。请注意，如果您已经安装了这些依赖项，则可以跳过此步骤。如果由于网速问题，下载过慢，可以尝试使用国内源安装依赖。

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```



### 虚拟环境安装

**推荐！**我们推荐使用 anaconda 虚拟环境进行安装，方便对包进行管理，同时也不会影响其他项目的环境。

1. 如果没有安装 Python，可以不用安装 Python，直接前往 [anaconda 官网](https://www.anaconda.com/)下载 anaconda 最新版本。安装并配置好以后，使用 anaconda 新建一个环境。

```shell
conda create -n kimaridraw python=3.8.13
```

2. 激活名为 kimaridraw 的 conda 环境

```shell
conda activate kimaridraw
```

3. 下载 KimariDraw 源代码：

```shell
git clone https://github.com/kimariyb/kimariDraw.git
```

4. 进入 KimariDraw 目录并安装依赖：

```shell
cd kimariDraw
pip install -r requirements.txt
```

这将自动安装 KimariDraw 所需的 pandas、matplotlib 和 proplot 等依赖项。同时，由于激活的 conda 环境，因此 pip 安装的包只会在 kimaridraw 环境下使用，如果不激活就不会被使用。这样就很好的避免了不同任务依赖的环境不同，所导致的版本冲突。

## 使用

在使用 KimariDraw 之前，必须使用 Multiwfn 自行根据量子化学计算程序生产的各种光谱计算产生的 `.out` 文件得到光谱的数据。如果不了解如何使用 Multiwfn 绘制各类光谱，可以浏览 Sob 的 [使用Multiwfn绘制红外、拉曼、UV-Vis、ECD、VCD和ROA光谱图](http://sobereva.com/224)。

**请注意：在正式运行前，请确保已经安装了 KimariDraw 所需要的模块和包，以免程序报错！**

### 直接通过命令行运行

KimariDraw 可以直接使用命令行命令运行，

运行 kimaridraw.py 进入 KimariDraw 主程序：

```shell
KimariDraw --  A Python script that processes Multiwfn spectral data and plots various spectra.
Version: v2.4.0, release date: Aug-6-2023
Developer: Kimariyb, Ryan Hsiun
Address: XiaMen University, School of Electronic Science and Engineering
KimariDraw home website: https://github.com/kimariyb/kimariDraw
```

## 配置



## 绘制效果

### 绘制单子图

### 绘制多子图

<img src="figure/multi_IR.png" style="zoom: 25%;"  >

<img src="figure/multi_UV.png">


## 使用脚本批量产生光谱数据

KimariDraw 程序中自带了一个用来批量产生 Multiwfn 光谱数据的脚本。如果想要批量产生绘制光谱的数据，可以在 `script` 文件夹中找到这个脚本。其中 `GenData.sh` 为 Linux 系统下的脚本，`GenData.bat` 为 Windows 系统下的脚本。

`GenData.sh` 以及 `GenData.bat` 都需要一个名为 `commands.txt` 的文件。`commands.txt` 文件包含了执行 Multiwfn 生成数据所需要的命令，如果想要使用这个脚本，则必须对 Multiwfn 有一定的了解。得到的数据可以使用 KimariDraw 继续绘制光谱，如下所示（可以使用图片编辑工具把 x 轴 y 轴标题删了）；也可以用 Origin 绘制你想要效果的光谱。


## 鸣谢

在开发 KimariDraw 时，主要使用了以下 Python 开源模组，在这里对开发这些模组的工作人员表示感谢。

- **matplotlib**
- **pandas**
- **proplot**
- **toml**


## 许可证

KimariDraw 基于 MIT 许可证开源。这意味着您可以自由地使用、修改和分发代码。有关更多信息，请参见 LICENSE 文件。

