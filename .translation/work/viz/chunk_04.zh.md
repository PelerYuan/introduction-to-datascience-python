```{code-cell} ipython3
morley_hist_categorical = alt.Chart(morley_df).mark_bar(opacity=0.5).encode(
    x=alt.X("Speed").bin(),
    y=alt.Y("count()").stack(False),
    color="Expt:N"
)

morley_hist_categorical = morley_hist_categorical + v_line
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_categorical", morley_hist_categorical, display=True)
```

:::{glue:figure} morley_hist_categorical
:figwidth: 700px
:name: morley_hist_categorical

迈克尔逊光速数据的直方图，把实验当作分类变量着色。
:::

遗憾的是，想用颜色把实验编号区分开，结果弄得有些混乱。{numref}`morley_hist_categorical` 里的所有颜色都混在了一起；虽然仍能从中得出*一些*认识（例如实验 1 和实验 3 中有一些测量值的偏差最大），但这并不是传达信息、回答问题的最清晰方式。我们换一种策略：把直方图排成一张网格，每格放一个子图。

+++

```{index} altair; 分面
```

我们可以用 `facet` 函数创建由多个子图按网格排列而成的图。`facet` 的参数指定用一个或多个变量把图形拆分成子图（下面代码中的 `Expt`），以及网格中应有多少列。本例中我们选择把子图排成一列（`columns=1`），因为这样更容易比较不同子图里直方图在 `x` 轴上的位置。我们还降低了每张图的高度，好让它们都能放进同一个视图。请注意，我们复用了上面刚创建的那张图，而不是从头重新创建一张同样的图。我们还显式声明 `facet` 用的是分类变量，因为分面只应针对分类变量来做。

```{code-cell} ipython3
morley_hist_facet = morley_hist_categorical.properties(
    height=100
).facet(
    "Expt:N",
    columns=1
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_facet", morley_hist_facet, display=True)
```

:::{glue:figure} morley_hist_facet
:figwidth: 700px
:name: morley_hist_facet

按实验纵向拆分的迈克尔逊光速数据直方图。
:::

{numref}`morley_hist_facet` 中的可视化清楚地表明各个实验彼此之间有多准确。测量值波动最大的是实验 1，其测量值大致在 650–1050 km/sec 之间。测量值波动最小的是实验 2，其测量值大致在 750–950 km/sec 之间。差别最大的几个实验，总体上仍然得到了相当接近的结果！

```{index} altair; alt.X, altair; alt.Y, altair; configure_axis
```

要让这张图更清楚，还有三处收尾工作。首先，也是最重要的，是用 `alt.X` 和 `alt.Y` 函数加上有信息量的坐标轴标签，并用 `configure_axis` 函数调大字号以保持清晰可读。我们还可以加一个标题；对 `facet` 图来说，只要把 `title` 传给 facet 函数即可。最后一点也许最不易察觉：在这张图上，虽然很容易把各个实验互相比较，却很难体会所有实验总体上到底有多准确。例如，图上 800 这个值相对于真实光速到底有多准确？为了回答这个问题，我们要把数据转换成相对误差，而不是绝对测量值。

```{code-cell} ipython3
speed_of_light = 299792.458
morley_df["RelativeError"] = (
    100 * (299000 + morley_df["Speed"] - speed_of_light) / speed_of_light
)
morley_df
```

```{code-cell} ipython3
morley_hist_rel = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X("RelativeError")
        .bin()
        .title("Relative Error (%)"),
    y=alt.Y("count()").title("# Measurements"),
    color=alt.Color("Expt:N").title("Experiment ID")
)

# Recreating v_line to indicate that the speed of light is at 0% relative error
v_line = alt.Chart(morley_df).mark_rule(strokeDash=[6], size=1.5).encode(
    x=alt.datum(0)
)

morley_hist_relative = (morley_hist_rel + v_line).properties(
    height=100
).facet(
    "Expt:N",
    columns=1,
    title="Histogram of relative error of Michelson’s speed of light data"
)

```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_relative", morley_hist_relative, display=True)
```

:::{glue:figure} morley_hist_relative
:figwidth: 700px
:name: morley_hist_relative

按实验纵向拆分的相对误差直方图，坐标轴和标签更清晰。
:::

哇，真了不起！这些 1879 年的光速测量结果，误差只有真实光速的 *0.05%* 左右。{numref}`morley_hist_relative` 告诉你：虽然实验 2 和实验 5 也许最为准确，但考虑到当时的可用技术，所有实验都做得相当出色。

#### 为直方图选择箱宽

在 `altair` 中创建直方图时，它会尝试选择一个合理的箱数。我们可以用 `bin` 方法里的 `maxbins` 参数来改变箱数。

```{index} altair; maxbins
```

```{code-cell} ipython3
morley_hist_maxbins = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X("RelativeError").bin(maxbins=30),
    y="count()"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_maxbins", morley_hist_maxbins, display=False)
```

:::{glue:figure} morley_hist_maxbins
:figwidth: 700px
:name: morley_hist_maxbins

迈克尔逊光速数据的直方图。
:::


可是，箱数取多少才合适呢？很遗憾，正确的箱数或箱宽并没有硬性规则。这完全取决于你要解决的问题；*正确*的箱数或箱宽，就是*能帮你回答所提问题*的那个。为你要解决的问题选出合适的设置，往往需要反复迭代。通常值得多试几个不同的 `maxbins`，看看在你想回答的问题背景下，哪一个最能清楚地呈现数据。

为了体会不同分箱方式对可视化的影响，我们就用本节一直在处理的这张直方图来做实验。在 {numref}`morley_hist_max_bins` 中，我们把默认设置与另外三张直方图作比较，后者的 `maxbins` 分别设为 200、70 和 5。在这里可以看到，默认箱数和 `maxbins=70` 都能有效地帮助我们回答问题。另一方面，`maxbins=200` 和 `maxbins=5` 分别过小和过大。

```{code-cell} ipython3
:tags: ["remove-cell"]
morley_hist_default = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X(
        "RelativeError",
        title="Relative error (%)",
        bin=True
    ),
    y=alt.Y(
        "count()",
        stack=False,
        title="# Measurements"
    ),
    color=alt.Color(
        "Expt:N",
        title="Experiment ID",
        legend=None
    )
).properties(height=100, width=250)

morley_hist_max_bins = alt.vconcat(
    alt.hconcat(
        (morley_hist_default + v_line).facet(
            "Expt:N",
            columns=1,
            title=alt.TitleParams("Default (bin=True)", fontSize=16, anchor="middle", dx=15)
        ),
        (morley_hist_default.encode(
            x=alt.X(
                "RelativeError",
                bin=alt.Bin(maxbins=5),
                title="Relative error (%)"
            )
        ) + v_line).facet(
            "Expt:N",
            columns=1,
            title=alt.TitleParams("maxbins=5", fontSize=16, anchor="middle", dx=15)
        ),
    ),
    alt.hconcat(
        (morley_hist_default.encode(
            x=alt.X(
                "RelativeError",
                bin=alt.Bin(maxbins=70),
                title="Relative error (%)"
            )
        ) + v_line).facet(
            "Expt:N",
            columns=1,
            title=alt.TitleParams("maxbins=70", fontSize=16, anchor="middle", dx=15)
        ),
        (morley_hist_default.encode(
            x=alt.X(
                "RelativeError",
                bin=alt.Bin(maxbins=200),
                title="Relative error (%)"
            )
        ) + v_line).facet(
            "Expt:N",
            columns=1,
            title=alt.TitleParams("maxbins=200", fontSize=16, anchor="middle", dx=15)
        )
    ),
    spacing=50
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_max_bins", morley_hist_max_bins, display=True)
```

:::{glue:figure} morley_hist_max_bins
:figwidth: 700px
:name: morley_hist_max_bins

不同 maxbins 取值对直方图的影响。
:::

## 讲解可视化
<font size="5">*讲一个故事*</font>

通常情况下，你的可视化不会完全独立出现，而会是更大规模演示的一部分。此外，可视化可以为演示的任何环节提供辅助信息，从开场到结论都可以。例如，你可以在演示开场时用一张探索性可视化图，说明自己为什么选择更细致的数据分析或模型；也可以用一张分析结果的可视化图，展示分析发现了什么；甚至可以在演示结尾放一张图，为今后的工作方向提供建议。

```{index} 可视化; 讲解
```

无论在什么地方出现，讨论可视化的一个好办法是把它当成一个故事来讲：

1) 交代背景和范围，说明你为什么做这件事。
2) 提出你的可视化要回答的问题，并说明为什么这个问题值得回答。
3) 用你的可视化回答这个问题。务必描述可视化的*所有*方面（包括描述坐标轴）。但你
   可以根据回答问题的需要，突出不同的方面：
    - **趋势（折线图）：** 直线能很好地描述趋势吗？如果能，趋势就是*线性*的；如果不能，趋势就是*非线性*的。趋势是上升、下降，还是两者都不是？
                        趋势中是否有周期性振荡（摆动）？趋势是有噪声的（也就是线条频繁“跳来跳去”）还是平滑的？
    - **分布（散点图、直方图）：** 数据的离散程度如何？大致以哪里为中心？有没有明显的“簇”或“子组”，在直方图上会表现为多个峰？
    - **两个变量的分布（散点图）：** 变量之间的关系是清晰 / 强的（点落在明显的模式中）、弱的（点落在某种模式中但带有一些噪声），还是看不出
      关系（数据噪声太大，无法得出任何结论）？
    - **数量（条形图）：** 各条形彼此相比有多大？不同组的条形中是否有模式？
4) 总结你的发现，并用它们引出你接下来要讲的内容。

下面用两个例子说明，如何按这四个步骤讲解本章前面出现过的示例可视化。每一步都用括号中的编号标出，例如（3）。

```{index} Mauna Loa
```

**Mauna Loa 大气 CO$_{\text{2}}$ 测量数据：**（1）当前许多形式的能源生产与转换——从汽车发动机到天然气发电厂——都依赖燃烧化石燃料，并产生温室气体作为副产物，其中通常主要是二氧化碳（CO$_{\text{2}}$）。这些气体在地球大气中过多，就会使大气截留更多来自太阳的热量，导致全球变暖。（2）为了评估大气中 CO$_{\text{2}}$ 浓度上升得有多快，我们（3）使用了夏威夷 Mauna Loa 观测站的一套数据，其中包含 1980 年到 2020 年的 CO$_{\text{2}}$ 测量值。我们把测得的 CO$_{\text{2}}$ 浓度画在纵轴上，把时间画在横轴上。从这张图可以看到，随时间推移存在清晰、上升、总体呈线性的趋势。图中还有每年发生一次、与夏威夷季节相吻合的周期性振荡，其振幅相对于整体趋势的增长很小。这说明大气中的 CO$_{\text{2}}$ 显然在随时间上升，（4）也许值得进一步研究其中的成因。

```{index} 迈克尔逊光速
```

**迈克尔逊光速实验：**（1）与 19 世纪末相比，我们对光物理的现代认识已经进步了很多；当年迈克尔逊和莫雷的实验首次证明光速是有限的。根据现代实验，我们现在知道光的传播速度约为每秒 299,792.458 千米。（2）但是，我们最初测量这个基本物理常数的准确程度如何？某些实验是否比另一些实验得到了更准确的结果？（3）为了更好地理解这一点，我们把迈克尔逊在 1879 年所做的 5 次实验的数据画成彼此堆叠的直方图，每次实验有 20 轮试验。横轴表示测量值相对于我们今天所知真实光速的误差，用百分比表示。从这张图可以看到，大多数结果的相对误差至多为 0.05%。你还能看到，实验 1 和实验 3 的测量值离真实值最远，而实验 5 往往给出最稳定的准确结果。（4）值得进一步研究这些实验之间的差异，看看它们为什么会产生不同的结果。

## 保存可视化

<font size="5">*按需要选择合适的输出格式*</font>

```{index} see: 位图; 栅格图
```

```{index} 栅格图, 矢量图
```

正如存储数据集有很多方式一样，存储可视化和图像也有很多方式。该选哪一种取决于若干因素，例如文件大小或类型的限制（比如把可视化作为会议论文的一部分提交，或送到海报打印店），以及它将在哪里显示（例如网上、论文中、海报上、广告牌上、报告幻灯片里）。一般来说，图像分为两大类：*栅格*格式和*矢量*格式。

```{index} 栅格图; 文件类型
```

**栅格**图像表示成由正方形像素组成的二维网格，每个像素有各自的颜色。栅格图像在存储前往往要先*压缩*，以占用更少的空间。如果图像在加载和显示时无法被完美重建，这种压缩格式就是*有损*的，同时希望这种变化不易察觉。相反，*无损*格式可以完美地显示原始图像。

- *常见文件类型：*
    - [JPEG](https://en.wikipedia.org/wiki/JPEG)（`.jpg`、`.jpeg`）：有损，通常用于照片
    - [PNG](https://en.wikipedia.org/wiki/Portable_Network_Graphics)（`.png`）：无损，通常用于统计图形和线条图
    - [BMP](https://en.wikipedia.org/wiki/BMP_file_format)（`.bmp`）：无损，原始图像数据，不压缩（很少使用）
    - [TIFF](https://en.wikipedia.org/wiki/TIFF)（`.tif`、`.tiff`）：通常无损，不压缩，多用于美术设计和出版
- *开源软件：* [GIMP](https://www.gimp.org/)

```{index} 矢量图; 文件类型
```

**矢量**图像表示成一组数学对象（直线、曲面、形状、曲线）。计算机显示图像时，会用这些对象的数学公式重新绘制所有元素。

- *常见文件类型：*
    - [SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics)（`.svg`）：通用
    - [EPS](https://en.wikipedia.org/wiki/Encapsulated_PostScript)（`.eps`）：通用（很少使用）
- *开源软件：* [Inkscape](https://inkscape.org/)

栅格图像和矢量图像的优缺点正好相反。宽高固定的栅格图像，无论显示什么内容，占用的空间和加载时间都相同（唯一的例外是：对某些图像，压缩算法可能把文件压得更小，或者运行得更快）。矢量图像占用的空间和加载时间取决于图像的复杂程度，因为每次显示时计算机都要重新绘制所有元素。例如，把包含 100 万个点的散点图存成 SVG 文件，你的计算机可能要花一些时间才能打开。反过来，矢量图可以随意放大 / 缩放，画面都不会变差；而栅格图像放大到一定程度就会显得“像素化”。

```{index} PDF
```

```{index} see: 可移植文档格式; PDF
```

```{note}
可移植文档格式 [PDF](https://en.wikipedia.org/wiki/PDF)（`.pdf`）常用来*同时*存储栅格和矢量两种格式。如果你打开一个 PDF 时发现加载很久，
可能是因为其中有一张复杂的矢量图，正由你的计算机渲染。
```

下面我们学习如何把图形保存成 `.png` 和 `.svg` 文件格式。这里用的例子是前面创建的 `faithful_scatter_labels` 散点图，它来自 [Old Faithful 数据集](https://www.stat.cmu.edu/~larry/all-of-statistics/=data/faithful.dat) {cite:p}`faithfuldata`，见 {numref}`faithful_scatter_labels`。要把图形保存到文件，可以用 `save` 方法。`save` 方法接收保存文件的路径（例如 `img/viz/filename.png` 表示把名为 `filename.png` 的文件保存到 `img/viz/` 目录）。保存成哪种图像由文件扩展名决定。例如，要创建 PNG 图像文件，就把文件扩展名指定为 `.png`。下面演示如何把 `faithful_scatter_labels` 图保存成 PNG 和 SVG 两种文件类型。

```{code-cell} ipython3
faithful_scatter_labels.save("img/viz/faithful_plot.png")
faithful_scatter_labels.save("img/viz/faithful_plot.svg")
```

```{code-cell} ipython3
:tags: [remove-cell]

import os
import numpy as np
png_size = np.round(os.path.getsize("img/viz/faithful_plot.png")/(1024*1024), 2)
svg_size = np.round(os.path.getsize("img/viz/faithful_plot.svg")/(1024*1024), 2)

glue("png_size", "{:.2f}".format(png_size))
glue("svg_size", "{:.2f}".format(svg_size))
```

```{list-table} Old Faithful 数据集散点图存成不同文件格式时的文件大小。
:header-rows: 1
:name: png-vs-svg-table

* - 图像类型
  - 文件类型
  - 图像大小
* - 栅格
  - PNG
  - {glue:text}`png_size` MB
* - 矢量
  - SVG
  - {glue:text}`svg_size` MB
```

看看 {numref}`png-vs-svg-table` 中的文件大小。哇，差别还真大！这里 `.png` 图像几乎比 `.svg` 图像小 4 倍。由于图中的点相当多，矢量图格式的 `.svg` 文件比只存储图像数据本身的栅格图像 `.png` 更大。在 {numref}`png-vs-svg` 中，我们展示了放大到只有 3 个数据点的矩形区域时图像的样子。你就能明白矢量图格式为什么这么有用了：正因为它们只是基于数学公式，矢量图可以放大到任意尺寸。这使它们很适合各种尺寸的展示媒介，从论文到海报再到广告牌。

```{figure} img/viz/png-vs-svg.png
---
height: 400px
name: png-vs-svg
---
放大后的 `faithful` 图，栅格格式（PNG，左）和矢量格式（SVG，右）。
```