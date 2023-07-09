<h1 align="center">
    <img src="figure/logo.png" width="200">
</h1><br>


KimariDraw 是一款基于 Python 开发的开源绘图软件，专门用来处理著名的波函数分析程序 Multiwfn 绘制光谱所产生的数据，并重新绘制出美观、清晰的各种光谱图。对于科学研究人员和化学爱好者而言，KimariDraw 是一个非常实用的工具，它可以帮助用户更好地展示和分析波函数分析数据，有助于更好地理解和解释分析结果。

Multiwfn 是一个非常强大的波函数分析程序。Multiwfn 免费、开源、高效、灵活，它支持几乎所有最重要的波函数分析方法。Multiwfn 已经成为了量子化学领域的常用工具之一，目前得到了广泛的应用和认可。

**如果您对 Multiwfn 还不熟悉，请访问 [Multiwfn 官网](http://sobereva.com/multiwfn/)了解更多信息。**

当你使用 KimariDraw 时，你可以享受到以下的功能：

- **支持多种光谱类型**：KimariDraw 目前支持使用 Multiwfn 绘制 NMR、IR 等光谱导出的曲线数据，即 Multiwfn 生成的文本文件，也支持 Excel 文件（必须安装约定进行配置）。

- **美观的图形界面**：KimariDraw 的图形用户界面易于使用，您可以轻松地调整图表的大小、颜色等，以便更好地呈现您的数据。

- **支持多种文件格式**：KimariDraw 支持导入多种数据文件格式，包括文本文件和 Excel 文件。除此之外，KimariDraw 也支持将图表导出为多种文件格式，如 PNG、JPG、PDF 等。

- **易于安装和配置**：KimariDraw 的安装和配置十分简单，您只需要按照项目 README 文件中的说明进行操作即可。

## 安装

本项目已经开源在 Github 上，您可以通过以下步骤安装 KimariDraw：

1. 首先，您需要确保已经安装了 Python 环境和 pip 包管理工具。如果您还没有安装它们，请先安装它们。

2. 下载 KimariDraw 源代码：

```shell
git clone https://github.com/kimariyb/kimariDraw.git
```

3. 进入 KimariDraw 目录并安装依赖：

```shell
cd kimariDraw
pip install -r requirements.txt
```
这将自动安装 KimariDraw 所需的 numpy、matplotlib 和 scipy 等依赖项。请注意，如果您已经安装了这些依赖项，则可以跳过此步骤。

## 使用

要使用 KimariDraw，请执行以下步骤：

**请注意：在正式运行前，请确保已经安装了 Python 和 pip 包管理工具，以免程序报错！**

1. 在命令行中导航到 KimariDraw 目录。

2. 运行 main.py：

```shell
python main.py
```

3. 输入 Multiwfn 输出的文本文件 `.txt` 或 Excel 文件 `.xlsx` 的路径。例如本项目中的 `data\NMR_curvewei.txt` 文件。

```shell
data/NMR_curvewei.txt
```

4. 选择 `1. NMR`，绘制 NMR 谱。

<img src="figure/nmr.png">

## 鸣谢

在开发 KimariDraw 时，主要使用了以下 Python 开源模组，在这里对开发这些模组的工作人员表示感谢。

- **numpy**
- **pandas**
- **matplotlib**
- **openpyxl**
- **scipy**

同时也感谢 Multiwfn 和其开发者卢天老师，为众多计算化学玩家带来这样一款，实用、轻便、功能强大的波函数分析软件。

## 许可证

KimariDraw 基于 MIT 许可证开源。这意味着您可以自由地使用、修改和分发代码。有关更多信息，请参见 LICENSE 文件。


