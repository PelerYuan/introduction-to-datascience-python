:::{glue:figure} can_lang_plot_theme
:figwidth: 700px
:name: can_lang_plot_theme

散点图，比较把某种语言作为母语的加拿大人占比与把该语言作为家中主要语言的占比，散点按语言类别着色，并使用自定义的颜色和形状。
:::

上图已经很好地展示了不同语言类别之间的差异，有了这些信息，就足以回答我们的研究问题了。但如果我们想知道图中每个点究竟对应哪一种语言，又该怎么办呢？用普通的可视化库做不到这一点，因为给每一种语言都单独加上文字标签会带来大量视觉噪声，让图表难以解读。不过，altair 是交互式可视化库，我们可以通过 `Tooltip` 编码通道按需添加信息：只要把鼠标指针悬停在某个点上，该点的文字标签就会显示出来。这里我们还会把 x 轴和 y 轴变量的确切取值也加进提示框。

```{index} altair; alt.Tooltip
```

```{code-cell} ipython3
can_lang_plot_tooltip = alt.Chart(can_lang).mark_point(filled=True).encode(
    x=alt.X("most_at_home_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Language spoken most at home", "(percentage of Canadian residents)"]),
    y=alt.Y("mother_tongue_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Mother tongue", "(percentage of Canadian residents)"]),
    color=alt.Color("category")
        .legend(orient="top")
        .title("")
        .scale(scheme="dark2"),
    shape="category",
    tooltip=alt.Tooltip(["language", "mother_tongue", "most_at_home"])
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
if "BOOK_BUILD_TYPE" in os.environ and os.environ["BOOK_BUILD_TYPE"] == "PDF":
    glue("can_lang_plot_tooltip", Image("img/viz/languages_with_mouse.png"), display=False)
else:
    # Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
    glue("can_lang_plot_tooltip", can_lang_plot_tooltip.properties(height=320, width=420), display=False)
```

:::{glue:figure} can_lang_plot_tooltip
:figwidth: 700px
:name: can_lang_plot_tooltip

散点图，比较把某种语言作为母语的加拿大人占比与把该语言作为家中主要语言的占比，散点按语言类别着色，并使用自定义的颜色和鼠标悬停提示框。
:::

从 {numref}`can_lang_plot_tooltip` 这张图可以清楚地看到，绝大多数加拿大人申报的母语，以及他们在家中说得最多的语言，都是某一种官方语言。再看探索性问题的后半部分，我们能发现什么？在不同高层级的语言类别中，把某种语言作为母语与作为家中主要语言，这两种情况之间的关系是否存在差异？从 {numref}`can_lang_plot_tooltip` 来看，差异似乎不大。对每一个高层级的语言类别而言，把某种语言作为母语的人数占比，与把它作为家中主要语言的人数占比之间，都存在很强的正相关关系（positive relationship），并且呈线性。无论属于哪个类别，这种关系看起来都很相似。

这是否意味着，世界上所有语言的这种关系都是正相关的？更进一步说，如果已经知道有多少人把某种语言作为家中主要语言，我们能否只凭这张数据可视化图就预测出有多少人把它作为母语？这两个问题的答案都是“不能！”不过，借助探索性数据分析，我们可以提出新的假设、新的想法和新的问题（就像本段开头那样）。回答这些问题往往要做更复杂的分析，有时甚至还要收集更多数据。本书后面还会看到更多这样的复杂分析。

### 条形图：岛屿陆块数据集

```{index} 岛屿陆块
```

`islands.csv` 数据集收录了地球上的各个陆块及其面积（单位为千平方英里）{cite:p}`islandsdata`。

```{index} 问题; 可视化
```

**问题：** 七大洲（北美洲、南美洲、非洲、欧洲、亚洲、澳大利亚和南极洲）是地球上最大的七个陆块吗？如果是，紧随其后的几个最大陆块又是哪些？

首先，我们读入并查看数据：

```{code-cell} ipython3
:tags: ["output_scroll"]
islands_df = pd.read_csv("data/islands.csv")
islands_df
```

这里的数据框列出了地球上的各个陆块，我们要比较它们的大小。回答这个问题，合适的可视化方式是条形图。条形图中，每根条形的高度代表某个*数量*的取值（大小、计数、比例、百分比等）。比较分类变量各组的计数或比例时，条形图特别有用。不过要注意，条形图一般不宜用来展示均值或中位数，因为这样会掩盖数据变异的重要信息。更好的做法是展示所有单个数据点的分布，例如使用直方图，我们会在 {numref}`histogramsviz` 中进一步讨论。

```{index} altair; mark_bar
```

我们通过 `altair` 中的 `mark_bar` 函数指定使用条形图。结果见 {numref}`islands_bar`。

```{code-cell} ipython3
islands_bar = alt.Chart(islands_df).mark_bar().encode(
    x="landmass",
    y="size"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("islands_bar", islands_bar, display=False)
```

:::{glue:figure} islands_bar
:figwidth: 400px
:name: islands_bar

地球各陆块大小的条形图。使用默认设置时图形太宽。
:::

好，还不错！{numref}`islands_bar` 中的图形肯定是对的可视化方式，我们能清楚地看到并比较各陆块的大小。主要问题在于，较小陆块的大小很难分辨，而且图形太宽，没法把它们放在一起比较！不过别忘了，我们问的问题只涉及最大的那些陆块；只保留最大的 12 个陆块，图形就能更清楚一些。我们用 `nlargest` 函数来做这件事：第一个参数是要保留的行数，第二个是用来比较大小的列名。为了让陆块名称更容易读，我们再交换 `x` 和 `y` 变量，把标签放到 y 轴上，这样就不用歪着头去读了。

```{note}
回想一下，在 {numref}`第 %s 章 <intro>` 中，我们用 `sort_values` 后接 `head` 取出了某个变量取值最大的十行。其实也可以改用 `pandas` 的 `nlargest` 函数。`nsmallest` 和 `nlargest` 函数与 `sort_values` 后接 `head` 的效果一样，但效率略高，因为它们是专门为此设计的。一般来说，只要有更专用的函数，就该优先使用！
```

```{index} DataFrame; nlargest, DataFrame; nsmallest
```

```{code-cell} ipython3
islands_top12 = islands_df.nlargest(12, "size")

islands_bar_top = alt.Chart(islands_top12).mark_bar().encode(
    x="size",
    y="landmass"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("islands_bar_top", islands_bar_top, display=True)
```

:::{glue:figure} islands_bar_top
:figwidth: 700px
:name: islands_bar_top

地球最大的 12 个陆块各自大小的条形图。
:::


{numref}`islands_bar_top` 中的图形明显更清楚了，也能帮我们回答最初的问题：“七大洲是地球上最大的陆块吗？”以及“紧随其后的几个最大陆块是哪些？”不过，这张图还可以再改进：按各陆块是否属于大洲给条形着色，并按陆块大小而不是字母顺序排列条形。用于给条形着色的数据存放在 `landmass_type` 列中，所以我们把 `color` 编码设为 `landmass_type`。要按 `size` 变量排列陆块，我们会在图形的 y 编码通道中使用 altair 的 `sort` 函数。由于 `size` 变量编码在图形的 x 通道中，我们在 `alt.Y` 上指定 `sort("x")`。这样就会把 `y` 轴上的取值按 `x` 轴取值的升序绘制出来。于是得到的图形中，最长的条形最靠近坐标轴线，这通常是条形排序时视觉效果最好的做法。如果反过来想按 `x-axis` 的降序排列 `y-axis` 上的取值，可以加上一个负号反转顺序，写成 `sort="-x"`。

```{index} altair; sort
```

最后，我们用 `title` 方法定制坐标轴标签和图例标签，并通过指定 `alt.Chart` 的 `title` 参数给图形加上标题。图形标题并非总是必需的，尤其是当它与已有的图注或周围上下文重复时（例如在带注释的幻灯片里）。但如果你决定加上标题，好的图形标题应当给出你希望读者关注的核心信息，例如“地球上最大的七个陆块都是大洲”，或者对所展示信息做一个更概括的总结，例如“地球上最大的十二个陆块”。

```{code-cell} ipython3
islands_plot_sorted = alt.Chart(
	islands_top12,
	title="Earth's seven largest landmasses are continents"
).mark_bar().encode(
    x=alt.X("size").title("Size (1000 square mi)"),
    y=alt.Y("landmass").sort("x").title("Landmass"),
    color=alt.Color("landmass_type").title("Type")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("islands_plot_sorted", islands_plot_sorted, display=True)
```

:::{glue:figure} islands_plot_sorted
:figwidth: 700px
:name: islands_plot_sorted

地球最大的 12 个陆块各自大小的条形图，按陆块类型着色，坐标轴和标签更清晰。
:::


{numref}`islands_plot_sorted` 中的图形现在可以有效地回答我们最初的问题了。陆块按大小排列，大洲和其他陆块的颜色不同，可以很清楚地看出，最大的七个陆块都是大洲。

(histogramsviz)=
### 直方图：迈克尔逊光速数据集

```{index} 迈克尔逊光速
```

`morley` 数据集收录了 1879 年实验中测得的光速测量值。当时做了五次实验，每次实验又做了 20 轮——也就是说，每次实验都收集了 20 个光速测量值 {cite:p}`lightdata`。因为光速是很大的数（真值为 299,792.458 千米/秒），数据被编码成测得的光速减去 299,000。这样编码便于我们关注测量值的波动，这些波动通常远小于 299,000。如果直接使用完整的大数值光速测量值，测量值之间的波动就看不出来，也就难以研究各次实验之间的差异。

```{index} 问题; 可视化
```

**问题：** 已知我们现在对光速的了解（每秒 299,792.458 千米），各次实验的准确程度如何？

首先读入数据。

```{code-cell} ipython3
morley_df = pd.read_csv("data/morley.csv")
morley_df
```

```{index} 分布, altair; histogram, altair; count
```

```{index} see: count; altair
```

在这份实验数据中，迈克尔逊要测量的只是一个定量数值（光速）。该数据集包含这个量的许多测量值。要判断各次实验的准确程度，就需要把测量值的分布可视化（也就是它们所有可能的取值，以及每个取值出现了多少次）。这可以用*直方图*来做。直方图把取值划分到各个箱中，再用竖条显示每个箱里落入了多少个数据点，从而帮助我们观察某个变量在数据集中的分布。

要了解如何在 `altair` 中绘制直方图，我们先像上一节那样画一张条形图。注意这一次我们把 `y` 编码设为 `"count()"`。`morley_df` 里并没有名为 `"count()"` 的列；我们用 `"count()"` 告诉 `altair`，我们希望统计 x 轴上每个取值出现的次数（x 轴编码的是 `Speed` 列）。

```{code-cell} ipython3
morley_bars = alt.Chart(morley_df).mark_bar().encode(
    x="Speed",
    y="count()"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_bars", morley_bars, display=False)
```

:::{glue:figure} morley_bars
:figwidth: 700px
:name: morley_bars

迈克尔逊光速数据的条形图。
:::

上面的条形图能提示哪些取值比其他取值更常见，但条形太细，很难看出数据的整体分布。我们其实并不关心每个确切的 `Speed` 取值出现了多少次，而是关心大多数 `Speed` 取值大体落在什么位置。要更有效地传达这些信息，我们可以用 `bin` 方法把 x 轴划分成若干个箱，也就是“分组区间”，然后统计每个箱里落入多少个 `Speed` 取值。对分箱后的定量变量统计取值个数而画出的条形图，就叫做直方图。

```{code-cell} ipython3
morley_hist = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X("Speed").bin(),
    y="count()"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist", morley_hist, display=False)
```

:::{glue:figure} morley_hist
:figwidth: 700px
:name: morley_hist

迈克尔逊光速数据的直方图。
:::

#### 为 `altair` 图形叠加图层

```{index} altair; +, altair; mark_rule, altair; 图层
```

{numref}`morley_hist` 是个很好的开始。不过，除非能看到真值，否则用这张图无法判断测量有多准确。为了把真实光速可视化，我们用 `mark_rule` 函数加上一条竖线。要用 `mark_rule` 画竖线，需要指定这条线画在 x 轴上的哪个位置。这可以通过 `x=alt.datum(792.458)` 来实现，其中 `792.458` 是真实光速减去 299,000 的结果，而 `alt.datum` 告诉 altair，我们要绘制的是一个单独的数据取值（数字），而不是数据框中的某一列。类似地，用 `y` 轴编码并传入只含单个取值的数据框，就能画出水平线，这个取值就是 y 轴截距。请注意，*竖线*用来标示*横轴*上的量，而*横线*用来标示*纵轴*上的量。

要微调这条竖线的外观，可以用 `strokeDash=[5]` 把它从实线改成虚线，其中 `5` 表示每一段虚线的长度。我们还可以用 `size=2` 改变线的粗细。为了把虚线叠加到直方图上，我们用 `+` 运算符把 `mark_rule` 图形**添加**到 `morley_hist` 上。用 `+` 运算符给图形添加内容，在 `altair` 中叫做*图层叠加*。这是 `altair` 的强大特性：你可以不断迭代同一张图，一次叠加一个图层并逐步改进。如果你已经用赋值符号（`=`）把图形存成了变量，就可以用 `+` 运算符在它上面继续添加。下面我们把用 `mark_rule` 创建的竖线加到前面创建的 `morley_hist` 上。

```{note}
严格来说，创建这条竖线时本来可以省略 data 参数，因为我们并没有用到 `morley_df` 数据框中的任何取值；但后面给这张叠加图层后的图形分面时还会用到它，所以这里就先写上了。
```

```{code-cell} ipython3
v_line = alt.Chart(morley_df).mark_rule(strokeDash=[6], size=1.5).encode(
    x=alt.datum(792.458)
)

morley_hist_line = morley_hist + v_line
```


```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_line", morley_hist_line, display=False)
```

:::{glue:figure} morley_hist_line
:figwidth: 700px
:name: morley_hist_line

迈克尔逊光速数据的直方图，并用竖线标出真实光速。
:::

在 {numref}`morley_hist_line` 中，我们仍然看不出哪些测量值来自哪次实验（实验由 `Expt` 列标示），也许有的实验比其他实验更准确。要完整回答我们的问题，就得在图上把这些测量值彼此区分开。可以尝试用*带颜色的*直方图，把不同实验的计数以不同颜色堆叠在一起。只要把 `Expt` 变量加到 `color` 参数上，就能画出按它着色的直方图。

```{code-cell} ipython3
morley_hist_colored = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X("Speed").bin(),
    y="count()",
    color="Expt"
)

morley_hist_colored = morley_hist_colored + v_line

```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_colored", morley_hist_colored, display=True)
```

:::{glue:figure} morley_hist_colored
:figwidth: 700px
:name: morley_hist_colored

迈克尔逊光速数据的直方图，按实验着色。
:::

```{index} 整数
```

好，{numref}`morley_hist_colored` 看起来……等等！我们没法轻易区分直方图中不同实验的颜色！这是怎么回事？回想一下 {numref}`第 %s 章 <wrangling>` 的内容：你为每个变量选择的*数据类型*会影响 Python 和 `altair` 处理它的方式。这里，`morley` 数据框中的数据类型确实有问题。具体来说，`Expt` 列目前是*整数*，准确地说是 `int64` 类型。但我们希望把它当作*类别*来处理，也就是说，每种实验类型应该对应一个类别。
```{code-cell} ipython3
morley_df.info()
```

```{index} 名义型, altair; :N
```

要解决这个问题，我们可以在 `Expt` 变量后面加上后缀 `:N`，把它转换成 `nominal`（即分类）类型的变量。给 `Expt` 加上 `:N` 后缀能确保 `altair` 把该变量当作分类变量处理，从而在可视化中使用离散的配色方案（[关于数据类型的更多说明见 altair 文档](https://altair-viz.github.io/user_guide/encodings/index.html#encoding-data-types)）。我们还在 `y` 编码上调用 `stack(False)` 方法，让条形不再互相堆叠，而是共用同一条基线。不同颜色的条形会互相遮挡，为了尽量让它们都能看清，我们把 `mark_bar` 中的 `opacity` 参数设为 `0.5`，让条形略微半透明。
<<TERM>>
landmass = 陆块
nominal = 名义型
Michelson = 迈克尔逊
baseline = 基线
run (in an experiment) = 轮次
<<END>>
