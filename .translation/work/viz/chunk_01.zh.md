```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
from IPython.display import Image
```

(viz)=
# 有效的数据可视化

## 概述
本章介绍数据可视化的概念与工具，内容超出我们目前已经见过和练习过的范围。我们会着重讲解有效数据可视化的指导原则，并说明数据可视化如何独立于任何特定工具或编程语言。在此过程中，还会涉及用 Python 为数据创建可视化图形的一些具体做法（散点图、条形图、折线图和直方图）。

## 本章学习目标

学完本章后，你将能够：

- 说明借助数据集回答具体问题时，何时该使用以下几种可视化：
    - 散点图
    - 折线图
    - 条形图
    - 直方图
- 给定一个数据集和一个问题，从上述图形类型中挑选合适的一种，用 Python 创建最能回答该问题的可视化。
- 评价一张可视化图形的效果，并提出改进建议，以便更好地回答给定的问题。
- 结合可视化图形，用非技术的语言表达得出的结论。
- 识别创建有效可视化的经验法则。
- 使用 Python 中的 `altair` 库，借助以下要素创建并改进上述可视化：
    - 图形标记（graphical mark）：`mark_point`、`mark_line`、`mark_circle`、`mark_bar`、`mark_rule`
    - 编码通道（encoding channel）：`x`、`y`、`color`、`shape`
    - 标签：`title`
    - 变换：`scale`
    - 子图：`facet`
- 说明 `altair` 图形的两个关键要素：
    - 图形标记
    - 编码通道
- 说明栅格图（raster graphics）与矢量图两种输出格式的区别。
- 使用 `chart.save()` 把可视化图形保存为 `.png` 和 `.svg` 格式。

## 选择可视化图形

<font size="5">*提出问题，并回答它*</font>

```{index} 问题; 可视化
```

可视化的目的在于回答关于某个数据集的问题。因此，在创建可视化图形**之前**，首先要做的就是把你想要回答的、关于数据的问题表述清楚。好的可视化能不受干扰地清楚回答你的问题；*出色的*可视化甚至不需要额外解释，就能让人看出问题本身是什么。你可以把自己的可视化想象成项目海报展示的一部分：即使你没有站在海报前讲解，有效的可视化也能把你的信息传达给观众。

回想一下 {numref}`第 %s 章 <intro>` 中介绍的各种数据分析问题。用本章将要介绍的可视化方法，我们能够回答的*只有描述性和探索性*问题。请注意，不要用这里介绍的可视化去回答任何*预测性、推断性、因果性*或*机理性*问题，因为要恰当地回答这些问题所需的工具，我们还没有学过。

和大多数编程任务一样，在找到适合自己数据和问题的可视化之前，出错并迭代几次完全没问题（而且相当常见）。可用的绘图图形种类很多（目录可参见《Fundamentals of Data Visualization》的第 5 章 {cite:p}`wilkeviz`）。本书要介绍的图形类型见 {numref}`plot_sketches`；你应该选择哪一种，取决于你的数据和你想回答的问题。一般来说，何时该用哪类图形的指导原则如下：

```{index} 可视化; 折线图, 可视化; 直方图, 可视化; 散点图, 可视化; 条形图, 分布
```

- **散点图**用来展示两个定量变量之间的关系
- **折线图**用来展示相对于某个独立且有序的量（例如时间）的趋势
- **条形图**用来展示数量之间的比较
- **直方图**用来展示某个定量变量的分布（也就是它所有可能的取值，以及每个取值出现的频率）

```{figure} img/viz/plot-sketches-1.png
---
height: 400px
name: plot_sketches
---
散点图、折线图和条形图以及直方图的示例。
```


所有类型的可视化都有各自的用法（以及误用），但有三类通常难以理解，或者很容易被更好的做法取代。特别要避免使用**饼图**：一般来说用条形更好，因为比较条形的高度比比较饼图扇区的大小更容易。也不要使用**三维可视化**，因为把它们转换成静态的二维图像格式后，通常很难理解。最后，不要用表格做数值比较；人快速处理视觉信息的能力远胜于处理文字和数学。条形图通常又是更好的选择。

+++

## 改进可视化图形

<font size="5">*传达信息，减少噪声*</font>

仅仅能用 Python 和 `altair`（或任何其他工具）做出一张可视化图形，并不意味着它就能有效地把你的信息传达给别人。选定大致的可视化类型之后，你还得加以改进，让它符合自己的具体需要。下面列出了一些可用的经验法则。这些法则大致分为两类：你要*让可视化图形传达你的信息*，并且要*尽可能减少视觉噪声*。人处理信息的认知能力有限；这两类改进都是为了减轻观众观看可视化图形时的心理负担，让他们更容易快速理解并记住你的信息。

**传达信息**

- 确保可视化图形尽可能简单、直白地回答问题。
- 使用图例和标签，让别人不看周围的文字也能看懂你的可视化图形。
- 确保可视化图形上的文字、符号、线条等都足够大，容易看清。
- 确保数据清晰可见；不要把数据的形状或分布藏在其他对象（例如条形）后面。
- 确保使用色盲者也能看懂的配色方案（这部分人在总人口中的比例大得惊人——约 1% 到 10%，具体取决于性别和血统 {cite:p}`deebblind`）。
  例如，[配色方案](https://altair-viz.github.io/user_guide/customization.html#customizing-colors)
  功能让你可以选择这类配色方案；图形画好之后，你还可以上传到[色盲模拟器](https://www.color-blindness.com/coblis-color-blindness-simulator/)之类的在线工具进行检查。
- 冗余有时也有帮助：用多种方式传达同一条信息，能加深观众的印象。

**减少噪声**

- 少用颜色。颜色太多会分散注意力、制造出并不存在的模式，还会削弱信息的传达。
- 警惕标记重叠（overplotting）。标记重叠指的是表示数据的标记互相交叠，它的问题在于：在发生重叠的区域，你无法看出这里究竟表示了多少个数据点。如果图中的点或线太多，已经开始显得杂乱，就得换一种做法。
- 绘图区域（点、线和条形所在的区域）只做到需要的大小即可。简单的图形可以画得小一些。
- 不要调整坐标轴去放大微小的差异。差异小，就把它显示为小！

+++

## 用 `altair` 创建可视化图形

<font size="5">*迭代地构建可视化图形*</font>

```{index} altair
```

本节会给出一些示例，说明在给定数据集和待回答的问题时，如何选择和改进可视化图形，以及随后如何用 Python 和 `altair` 把它创建出来。要使用 `altair` 包，先得导入它。我们还会导入 `pandas`，用来读入数据。

```{code-cell} ipython3
import pandas as pd
import altair as alt
```

```{note}
本章的示例可视化都使用相对较小的数据集，所以用 `altair` 的默认设置就足够了。不过，如果你想用行数超过 5,000 的数据框绘图，`altair` 会报错。要绘制更大的数据集，最简单的做法是在导入 `altair` 包之后立刻启用 `vegafusion` 数据转换器：`alt.data_transformers.enable("vegafusion")`。这样最多可以绘制 100,000 个图形对象（例如含 100,000 个点的散点图）。要可视化*更大*的数据集，请参阅 [altair 文档](https://altair-viz.github.io/user_guide/large_datasets)。
```

### 散点图与折线图：冒纳罗亚 CO$_{\text{2}}$ 数据集

```{index} 冒纳罗亚
```

[冒纳罗亚 CO$_{\text{2}}$ 数据集](https://www.esrl.noaa.gov/gmd/ccgg/trends/data.html)由 NOAA/GML 的 Pieter Tans 博士和斯克里普斯海洋研究所的 Ralph Keeling 博士整理，记录了 1959 年以来夏威夷冒纳罗亚研究站大气中二氧化碳（CO$_{\text{2}}$，单位为百万分率）的浓度 {cite:p}`maunadata`。本书将重点关注 1980—2020 年。

```{index} 问题; 可视化
```

**问题：** 大气中 CO$_{\text{2}}$ 的浓度会随时间变化吗？有没有值得注意的有趣模式？

```{code-cell} ipython3
:tags: ["remove-cell"]
mauna_loa = pd.read_csv("data/mauna_loa.csv")
mauna_loa["day"]=1
mauna_loa["date_measured"]=pd.to_datetime(mauna_loa[["year", "month", "day"]])
mauna_loa = mauna_loa[["date_measured", "ppm"]].query('ppm>0 and date_measured>"1980-1-1"')
mauna_loa.to_csv("data/mauna_loa_data.csv", index=False)
```

首先读入并查看数据：

```{code-cell} ipython3
# mauna loa carbon dioxide data
co2_df = pd.read_csv(
    "data/mauna_loa_data.csv",
    parse_dates=["date_measured"]
)
co2_df
```


```{code-cell} ipython3
co2_df.info()
```

可以看到，`co2_df` 数据框中有两列：`date_measured` 和 `ppm`。`date_measured` 列保存测量的日期，类型是 `datetime64`。`ppm` 列保存每个日期测得的 CO$_{\text{2}}$ 浓度，单位为百万分率，类型是 `float64`，这是小数的常见类型。

```{index} 日期与时间
```

```{note}
`read_csv` 之所以能把 `date_measured` 列解析成 `datetime` 向量类型，是因为该列采用的是国际标准日期格式，即 ISO 8601，这种格式把日期写成 `year-month-day`，并且我们使用了 `parse_dates=True`。`datetime` 向量是一种具有特殊性质的 `double` 向量，能够正确处理日期。例如，`datetime` 类型向量允许 `altair` 之类的函数把它们当作数值日期处理，而不是当作字符向量，尽管其中包含非数字字符（例如 `co2_df` 数据框中 `date_measured` 列的取值）。这意味着 Python 不会不小心把日期按错误的顺序绘制出来（也就是说，不会像字符向量那样按字母数字顺序排列）。关于日期与时间的更多内容可以看[这里](https://wesmckinney.com/book/time-series.html)。
```

我们要研究的是两个变量（CO$_{\text{2}}$ 浓度和日期）之间的关系，所以从散点图入手比较合适。散点图把数据表示为一个个单独的点，每个点有 `x`（水平轴）和 `y`（垂直轴）坐标。这里我们用测量日期作为 `x` 坐标，用 CO$_{\text{2}}$ 浓度作为 `y` 坐标。图形用 `alt.Chart()` 函数创建。创建图形时有几个基本方面需要指定：

```{index} altair; 图形标记, altair; 编码通道, altair; mark_point
```

- 要可视化的**数据框**名称。
    - 这里我们把 `co2_df` 数据框作为参数传给 `alt.Chart`
- **图形标记**，它规定映射后的数据应该如何显示。
    - 创建图形标记要用 `Chart.mark_*` 方法（图形标记的清单见
      [altair 参考文档](https://altair-viz.github.io/user_guide/marks.html)）。
    - 这里我们用 `mark_point` 函数把数据可视化为散点图。
- **编码通道**，它告诉 `altair` 数据框中的各列如何映射到图形中的视觉属性。
    - 创建编码要用 `encode` 函数。
    - `encode` 方法在编码通道（例如 x、y）与数据集中的字段之间建立键值映射，字段通过字段名（列名）来访问
    - 这里我们把图形的 `x` 轴设为 `date_measured` 变量，
      在 `y` 轴上绘制 `ppm` 变量。
    - 对 y 轴，我们还提供了方法
      `scale(zero=False)`。默认情况下，`altair` 根据数据选择 y 轴的上下界，
      并让 `y=0` 留在视野内。
      这往往是很有用的默认行为，但在这里，由于最小值大于 300
      ppm，我们就很难看出数据中的任何趋势。于是我们提供 `scale(zero=False)`，
      告诉 altair 根据数据选择一个合理的下界，这个下界
      不必是 0。
    - 要改变编码通道的属性，
      需要借助辅助函数 `alt.Y` 和 `alt.X`。
      这些辅助函数用来定制顺序、标题和标度等内容。
      这里我们用 `alt.Y` 改变 y 轴的取值范围，
      让它从 `date_measured` 列中的最小值开始，
      而不是从 0 开始。

```{code-cell} ipython3
co2_scatter = alt.Chart(co2_df).mark_point().encode(
    x="date_measured",
    y=alt.Y("ppm").scale(zero=False)
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("co2_scatter", co2_scatter, display=False)
```

:::{glue:figure} co2_scatter
:figwidth: 700px
:name: co2_scatter

大气中 CO$_{2}$ 的浓度随时间变化的散点图。
:::

{numref}`co2_scatter` 中的可视化图形显示，大气中 CO$_{\text{2}}$ 的浓度随时间有明显上升的趋势。这张图对我们问题的前半部分给出了肯定回答，但这似乎是从散点图中能得出的唯一结论。

关于这份数据，有一点很重要：我们要考察的变量之一是时间。时间是一类特殊的定量变量，因为它给数据加上了额外的结构——数据点有自然的先后顺序。具体来说，数据集中的每个观测都有前一个和后一个观测，观测的顺序很重要；改变顺序就会改变它们的含义。遇到这种情况，我们通常用折线图来可视化数据。折线图用线段把观测的 `x` 和 `y` 坐标依次连接起来，从而突出它们的顺序。

```{index} altair; mark_line
```

在 `altair` 中可以用 `mark_line` 函数创建折线图。现在我们试着只用默认参数把 `co2_df` 可视化为折线图：

```{code-cell} ipython3
co2_line = alt.Chart(co2_df).mark_line().encode(
    x="date_measured",
    y=alt.Y("ppm").scale(zero=False)
)
```


```{code-cell} ipython3
:tags: ["remove-cell"]
glue("co2_line", co2_line, display=False)
```

:::{glue:figure} co2_line
:figwidth: 700px
:name: co2_line

大气中 CO$_{2}$ 的浓度随时间变化的折线图。
:::

```{index} 标记重叠
```

啊哈！{numref}`co2_line` 显示，数据中*确实*还有另一个有趣的现象：除了随时间上升，浓度似乎还在上下振荡。就目前的这张图而言，仍然很难判断振荡有多快，不过，回答我们的问题，折线似乎比散点图更合适。这两张图的对比还说明散点图有一个常见问题：点常常挨得太近，甚至互相叠在一起，把原本清楚的信息搅乱了（*标记重叠*）。

```{index} altair; alt.X, altair; alt.Y, altair; configure_axis
```

可视化的大致细节定下来之后，就该做改进了。这张图相当简单，没有多少视觉噪声需要去除。但为了提高清晰度，有几件事必须做，例如加上信息明确的坐标轴标签，并把字体调到更容易阅读的字号。添加坐标轴标签要用 `title` 方法配合 `alt.X` 和 `alt.Y` 函数。改变字号要用 `configure_axis` 函数，并指定 `titleFontSize` 参数。

```{code-cell} ipython3
co2_line_labels = alt.Chart(co2_df).mark_line().encode(
    x=alt.X("date_measured").title("Year"),
    y=alt.Y("ppm").scale(zero=False).title("Atmospheric CO2 (ppm)")
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("co2_line_labels", co2_line_labels, display=False)
```

:::{glue:figure} co2_line_labels
:figwidth: 700px
:name: co2_line_labels

大气中 CO$_{2}$ 的浓度随时间变化的折线图，坐标轴和标签更清晰。
:::

```{note}
`altair` 中的 `configure_*` 函数还支持更多定制，例如调整图形大小、改变字体颜色，以及许多其他选项，可参见[这里](https://altair-viz.github.io/user_guide/configuration.html)。
```

```{index} altair; alt.Scale
```

最后，我们看看能不能稍微改动一下图形，以便更好地理解这种振荡。请注意，用少量几张图来回答问题的不同侧面，完全没问题。为此我们要用到*标度*，这是 `altair` 的另一个重要特性，它可以方便地变换各个变量并设定界限。具体来说，这里我们用 `alt.Scale` 函数只放大几年的数据（比如 1990—1995 年）。`domain` 参数接收一个长度为 2 的列表，用来指定限制坐标轴的上下界。我们还给 `mark_line` 加上了 `clip=True` 参数。这告诉 `altair` 把设定取值范围之外的数据“裁剪”（删除）掉，使其不会延伸到绘图区域之外。由于我们在编码上同时使用了 `scale` 和 `title` 方法，所以把它们分行堆叠，让代码更易读。

```{code-cell} ipython3
co2_line_scale = alt.Chart(co2_df).mark_line(clip=True).encode(
    x=alt.X("date_measured")
        .scale(domain=["1990", "1995"])
        .title("Measurement Date"),
    y=alt.Y("ppm")
        .scale(zero=False)
        .title("Atmospheric CO2 (ppm)")
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("co2_line_scale", co2_line_scale, display=False)
```

:::{glue:figure} co2_line_scale
:figwidth: 700px
:name: co2_line_scale

1990 年至 1995 年大气中 CO$_{2}$ 的浓度随时间变化的折线图。
:::

有意思！看来每年大气 CO$_{\text{2}}$ 都会上升，在 4 月前后达到峰值，随后一直下降到 9 月下旬前后，然后又再次上升，直到年底。夏威夷有两个季节：5 月到 10 月是夏季，11 月到 4 月是冬季。因此，CO$_{\text{2}}$ 的振荡模式与这两个季节相当吻合。

有一个很贴切的类比：构建数据可视化就像画一幅画。我们先准备一张空白画布，第一件事是给画布打底，为作画做好准备。在数据可视化中，这相当于调用 `alt.Chart` 并指定要用的数据集。接下来，我们勾画画面的背景。在数据可视化中，这相当于用 `encode` 函数把数据映射到坐标轴上。然后，我们把要表现的主要对象画进图中。在数据可视化中，这就是图形标记（例如 `mark_point`、`mark_line` 等）。最后，我们给画面添加细节和修饰。在数据可视化中，这就是微调坐标轴标签、改变字体、调整点的大小，以及做其他类似的事情。



### 散点图：老忠实间歇泉的喷发时间数据集

```{index} 老忠实间歇泉
```

`faithful` 数据集收录了美国怀俄明州黄石国家公园老忠实间歇泉的测量值，包括两次喷发之间的等待时间，以及紧接着那次喷发的持续时间（单位为分钟）。首先读入数据，然后回答下面的问题：

```{index} 问题; 可视化
```

**问题：** 喷发前的等待时间与喷发的持续时间之间是否存在关系？

```{code-cell} ipython3
faithful = pd.read_csv("data/faithful.csv")
faithful

```

这里我们再次研究两个定量变量（等待时间和喷发时间）之间的关系。但如果你看看数据框的输出，就会注意到：与冒纳罗亚 CO$_{\text{2}}$ 数据集中的时间不同，这里的两个变量都没有天然的先后顺序。所以散点图很可能是最合适的可视化方式。我们用 `altair` 包创建散点图，把 `waiting` 变量放在水平轴上，把 `eruptions` 变量放在垂直轴上，并用 `mark_point` 作为图形标记。结果见 {numref}`faithful_scatter`。

```{code-cell} ipython3
faithful_scatter = alt.Chart(faithful).mark_point().encode(
    x="waiting",
    y="eruptions"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("faithful_scatter", faithful_scatter, display=False)
```

:::{glue:figure} faithful_scatter
:figwidth: 700px
:name: faithful_scatter

等待时间与喷发时间的散点图。
:::

从 {numref}`faithful_scatter` 可以看出，数据倾向于分成两组：一组等待时间和喷发时间都短，另一组两者都长。请注意，这里没有出现标记重叠：各点总体上分得很清楚，形成的模式也很清晰。要改进这张图，我们只需加上坐标轴标签，并把字体调得更容易阅读。

```{code-cell} ipython3
faithful_scatter_labels = alt.Chart(faithful).mark_point().encode(
    x=alt.X("waiting").title("Waiting Time (mins)"),
    y=alt.Y("eruptions").title("Eruption Duration (mins)")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("faithful_scatter_labels", faithful_scatter_labels, display=False)
```

:::{glue:figure} faithful_scatter_labels
:figwidth: 700px
:name: faithful_scatter_labels

等待时间与喷发时间的散点图，坐标轴和标签更清晰。
:::


指定 `mark_point(size=10, color="black")` 可以改变点的大小和图形的颜色。

```{code-cell} ipython3
faithful_scatter_labels_black = alt.Chart(faithful).mark_point(size=10, color="black").encode(
    x=alt.X("waiting").title("Waiting Time (mins)"),
    y=alt.Y("eruptions").title("Eruption Duration (mins)")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("faithful_scatter_labels_black", faithful_scatter_labels_black, display=False)
```

:::{glue:figure} faithful_scatter_labels_black
:figwidth: 700px
:name: faithful_scatter_labels_black

等待时间与喷发时间的散点图，点用黑色标出。
:::
