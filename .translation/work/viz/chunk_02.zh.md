+++

### 坐标轴变换与彩色散点图：加拿大语言数据集

```{index} 加拿大语言
```

回顾一下 {numref}`第 %s 章 <intro>`、{numref}`第 %s 章 <reading>` 与 {numref}`第 %s 章 <wrangling>` 中介绍过的
`can_lang` 数据集 {cite:p}`timbers2020canlang`。该数据集记录了 2016 年加拿大人口普查中
各种语言的使用人数。

```{index} 问题; 可视化
```

**问题：** 把某种语言作为母语的人所占的百分比，与把该语言作为家中主要使用语言的人所占的百分比之间，
是否存在关系？这种关系的强度在更高层级的语言类别——官方语言、原住民语言（Aboriginal languages），
以及非官方非原住民语言——中是否呈现出某种模式？

我们先读取并查看这份数据：

```{code-cell} ipython3
:tags: ["output_scroll"]
can_lang = pd.read_csv("data/can_lang.csv")
can_lang
```

```{code-cell} ipython3
:tags: ["remove-cell"]
# use only nonzero entries (to avoid issues with log scale), and wrap in a pd.DataFrame to prevent copy/view warnings later
can_lang = pd.DataFrame(can_lang[(can_lang["most_at_home"] > 0) & (can_lang["mother_tongue"] > 0)])
```

```{index} altair; mark_circle
```

我们先为数据框中的 `mother_tongue` 列与 `most_at_home` 列画一张散点图。
正如上一节的散点图所示，
`mark_point` 默认只画出每个点的轮廓。
如果想把点填充起来，
可以给 `mark_point` 传入参数 `filled=True`，
也可以直接使用简写 `mark_circle`。
点要不要填充，主要取决于个人偏好，
不过图中有很多点互相重叠时，空心点让人更容易看清每一个点。
由此得到的图形见 {numref}`can_lang_plot`。

```{code-cell} ipython3
can_lang_plot = alt.Chart(can_lang).mark_circle().encode(
    x="most_at_home",
    y="mother_tongue"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("can_lang_plot", can_lang_plot, display=False)
```

:::{glue:figure} can_lang_plot
:figwidth: 700px
:name: can_lang_plot

以某种语言为母语的加拿大人人数，与以该语言为家中主要使用语言的人数之间的散点图。
:::

要初步提高 {numref}`can_lang_plot` 的可解释性，
我们应该把默认的坐标轴名称换成信息更明确的标签。
要让图中的坐标轴标签更易读，
可以把较长的标签分成多行显示。
为此，我们把 title 写成一个字符串列表，
列表中的每个字符串对应新的一行文字。
我们还可以加大字号，
进一步提高可读性。

```{index} altair; 多行标签
```

```{code-cell} ipython3
can_lang_plot_labels = alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home")
        .title(["Language spoken most at home", "(number of Canadian residents)"]),
    y=alt.Y("mother_tongue")
        .scale(zero=False)
        .title(["Mother tongue", "(number of Canadian residents)"])
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("can_lang_plot_labels", can_lang_plot_labels, display=False)
```

:::{glue:figure} can_lang_plot_labels
:figwidth: 700px
:name: can_lang_plot_labels

以某种语言为母语的加拿大人人数，与以该语言为家中主要使用语言的人数之间的散点图，并带有 x 轴和 y 轴标签。
:::


```{code-cell} ipython3
:tags: ["remove-cell"]
import numpy as np
numlang_speakers_max=int(max(can_lang["mother_tongue"]))
print(numlang_speakers_max)
numlang_speakers_min = int(min(can_lang["mother_tongue"]))
print(numlang_speakers_min)
log_result = int(np.floor(np.log10(numlang_speakers_max/numlang_speakers_min)))
print(log_result)
glue("numlang_speakers_max", "{0:,.0f}".format(numlang_speakers_max))
glue("numlang_speakers_min", "{0:,.0f}".format(numlang_speakers_min))
glue("log_result", log_result)
```

很好！{numref}`can_lang_plot_labels` 的坐标轴和标签现在清楚多了，也更容易解读。不过散点本身还有改进的空间：
214 个数据点大多挤在图形的左下方。数据之所以挤成一团，是因为
在加拿大讲英语或法语的人（也就是右上角的两个点）远多于讲其他语言的人。
具体来说，最常用的母语有 {glue:text}`numlang_speakers_max` 名使用者，
而最不常用的母语只有 {glue:text}`numlang_speakers_min`。
这两个数字的大小相差六个数量级！
我们可以筛选数据，确认右上角的这两个点
对应的正是加拿大的两种官方语言：

```{index} DataFrame; loc[]
```

```{code-cell} ipython3
:tags: ["output_scroll"]
can_lang.loc[
    (can_lang["language"]=="English")
    | (can_lang["language"]=="French")
]
```

```{index} 对数标度, altair; 对数标度
```

回忆一下，我们这个关于数据的问题涉及*全部*语言；
所以要妥善回答这个问题，
就需要调整坐标轴的标度，以便看清所有散点。
具体来说，我们会把水平和垂直坐标轴
改成**对数**（**log**）标度，以此改进这张图。
数据中同时出现*非常大*和*非常小*的取值时，对数标度就很有用，
因为它有助于把小的取值拉开、把大的取值压缩在一起。
例如，$\log_{10}(1) = 0$、$\log_{10}(10) = 1$、$\log_{10}(100) = 2$，以及 $\log_{10}(1000) = 3$；
在对数标度上，
1、10、100 和 1000 这几个数值彼此间距完全相同！
可见，做这种变换就是把大的取值拉近、把小的取值推远。
请注意，如果你的数据可能取到 0，对数标度也许并不合适
（因为在 Python 中 `log10(0)` 是 `-inf`）。这种情况下还有其他变换数据的方法，但已超出本书范围。

在 `altair` 可视化中，只要在 scale 方法里使用参数 `type="log"`，就能实现对数标度。

```{code-cell} ipython3
can_lang_plot_log = alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home")
        .scale(type="log")
        .title(["Language spoken most at home", "(number of Canadian residents)"]),
    y=alt.Y("mother_tongue")
        .scale(type="log")
        .title(["Mother tongue", "(number of Canadian residents)"])
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("can_lang_plot_log", can_lang_plot_log, display=False)
```

:::{glue:figure} can_lang_plot_log
:figwidth: 700px
:name: can_lang_plot_log

以某种语言为母语的加拿大人人数，与以该语言为家中主要使用语言的人数之间的散点图，其中 x 轴和 y 轴已按对数调整。
:::

在上面的图中你会注意到两件事。把坐标轴改成对数后会产生很多刻度和网格线，
让图形看起来相当杂乱，很难把注意力集中到数据上。
你还会看到，x 轴上倒数第二个刻度标签不见了；
Altair 之所以省掉它，是因为那些大数字并排放不下。
另外也不容易判断 100,000,000 这个标签属于最后一个刻度还是倒数第二个刻度。
要解决这些问题，我们可以把刻度和网格线的数量限制为只保留主要的七条，
并把数字格式改成带后缀的形式，让标签更短。

```{index} altair; 刻度数量, altair; 刻度格式
```

```{code-cell} ipython3
can_lang_plot_log_revised = alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home")
        .scale(type="log")
        .title(["Language spoken most at home", "(number of Canadian residents)"])
        .axis(tickCount=7, format="s"),
    y=alt.Y("mother_tongue")
        .scale(type="log")
        .title(["Mother tongue", "(number of Canadian residents)"])
        .axis(tickCount=7, format="s")
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("can_lang_plot_log_revised", can_lang_plot_log_revised, display=False)
```

:::{glue:figure} can_lang_plot_log_revised
:figwidth: 700px
:name: can_lang_plot_log_revised

以某种语言为母语的加拿大人人数，与以该语言为家中主要使用语言的人数之间的散点图，其中 x 轴和 y 轴已按对数调整。图中只显示主要的网格线。后缀“k”表示 1,000（“kilo”），而后缀“M”表示 1,000,000（“million”）。
:::


```{code-cell} ipython3
:tags: ["remove-cell"]
english_mother_tongue = can_lang.loc[can_lang["language"]=="English"].mother_tongue.values[0]
census_popn = int(35151728)
result = round((english_mother_tongue/census_popn)*100,2)
glue("english_mother_tongue", "{0:,.0f}".format(english_mother_tongue))
glue("census_popn", "{0:,.0f}".format(census_popn))
glue("result", "{:.2f}".format(result))

```

与 {numref}`第 %s 章 <wrangling>` 中的一些例子类似，
我们可以把计数换算成百分比，为这些数字提供参照，也让它们更容易理解。
做法是：把以某种语言为母语、或以该语言作为家中主要使用语言的人数，
除以居住在加拿大的人口数，再乘以 100\%。
例如，
在 2016 年加拿大人口普查中报告自己的母语为英语的人所占百分比为
{glue:text}`english_mother_tongue` / {glue:text}`census_popn` $\times$
100\% = {glue:text}`result`\%

下面我们把以某种语言为母语的人所占百分比，与以该语言作为家中主要使用语言的人所占百分比，
分别赋给 `can_lang` 数据框中的两个新列。由于新列是追加在数据表末尾的，
我们在变换之后选取了这两列，
这样你能清楚地看到表格变换后的输出。
请注意，我们把加拿大人口数用 `_` 分隔书写，这样读起来更方便；
这不会影响 Python 对这个数字的解释方式，仅仅是为了便于阅读。

```{index} DataFrame; 列赋值, DataFrame; []
```

```{code-cell} ipython3
canadian_population = 35_151_728
can_lang["mother_tongue_percent"] = can_lang["mother_tongue"]/canadian_population*100
can_lang["most_at_home_percent"] = can_lang["most_at_home"]/canadian_population*100
can_lang[["mother_tongue_percent", "most_at_home_percent"]]
```

接下来，我们修改可视化，改用刚算出的百分比
（并相应调整坐标轴标签，以反映单位的变化）。最终结果见 {numref}`can_lang_plot_percent`。
这里的刻度标签默认都能放下，所以我们没有给标签加后缀。
请注意，后缀有时也更难理解，
因此除非你的交流对象是技术背景的人，一般建议避免使用后缀（数值很小时尤其如此）。

```{code-cell} ipython3
can_lang_plot_percent = alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Language spoken most at home", "(percentage of Canadian residents)"]),
    y=alt.Y("mother_tongue_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Mother tongue", "(percentage of Canadian residents)"]),
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
# Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
glue("can_lang_plot_percent", can_lang_plot_percent.properties(height=320, width=420), display=False)
```

:::{glue:figure} can_lang_plot_percent
:figwidth: 700px
:name: can_lang_plot_percent

以某种语言为母语的加拿大人所占百分比，与以该语言为家中主要使用语言的加拿大人所占百分比之间的散点图。
:::

{numref}`can_lang_plot_percent` 正是回答本节第一个问题所要用的可视化，也就是：
把某种语言作为母语的人所占百分比，与把该语言作为家中主要使用语言的人所占百分比之间
是否存在关系。要完整回答这个问题，我们需要借助
{numref}`can_lang_plot_percent`
来评估数据的几个关键特征：

```{index} 关系; 正, 关系; 负, 关系; 无
```

- **方向：** x 变量增大时 y 变量往往也增大，那么 y 与 x 就是**正**相关关系（positive relationship）。x 增大时 y 往往减小，
  那么 y 与 x 就是**负**相关关系。如果 x 增大时 y 没有明显的增大或减小，
  那么 y 与 x **几乎没有**相关关系。

```{index} 关系; 强, 关系; 弱
```

- **强度：** x 增大时 y 变量*稳定地*增大、减小或保持不变，
  这种关系就是**强**相关关系；否则就是**弱**相关关系。直观地说，
  散点靠得比较近、整体看起来更像一条“线”或“曲线”而不是一团“云”时，这种关系就强。

```{index} 关系; 线性, 关系; 非线性
```

- **形状：** 如果能大致沿着这些数据点画出一条直线，这种关系就是**线性**关系；否则就是**非线性**关系。

在 {numref}`can_lang_plot_percent` 中可以看到，
把某种语言作为母语的人所占百分比越高，
在家中讲这种语言的人所占百分比也越高。
因此，这两个变量之间是**正**相关关系。
此外，因为 {numref}`can_lang_plot_percent` 中的点相当集中，
整体更像一条“线”而不是一团“云”，
所以可以说这是一种**强**相关关系。
最后，因为在
{numref}`can_lang_plot_percent`
中穿过这些点画一条直线
能相当好地贴合我们观察到的模式，所以我们说这种关系是**线性**的。

接下来看探索性数据分析问题的第二部分！
回忆一下，我们想知道在 {numref}`can_lang_plot_percent` 中发现的关系的强度，
是否取决于更高层级的语言类别（官方语言、原住民语言，
以及非官方、非原住民语言）。
一种常见的探索方法，是给已经画好的散点图上的数据点按组着色。
例如，既然 2016 年加拿大人口普查中记录的每种语言都有对应的
更高层级语言类别，我们就可以
给之前那张散点图上的点着色，
以表示每种语言所属的更高层级语言类别。

这里我们要按取值所属的 `category` 组把它们区分开。我们可以在 `encode` 方法中加上 `color` 参数，
指定用 `category` 列为点着色。加上这个参数后，点会按所属组着色，
图的一侧也会出现图例。
语言类别的标签本身已经说明了含义，
所以我们可以删掉图例标题，这样既能减少视觉杂乱，又不会削弱图表的表达效果。

```{code-cell} ipython3
can_lang_plot_category=alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Language spoken most at home", "(percentage of Canadian residents)"]),
    y=alt.Y("mother_tongue_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Mother tongue", "(percentage of Canadian residents)"]),
    color="category"
).configure_axis(titleFontSize=12)

```

```{code-cell} ipython3
:tags: ["remove-cell"]
# Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
glue("can_lang_plot_category", can_lang_plot_category.properties(height=320, width=420), display=False)
```

:::{glue:figure} can_lang_plot_category
:figwidth: 700px
:name: can_lang_plot_category

以某种语言为母语的加拿大人所占百分比，与以该语言为家中主要使用语言的加拿大人所占百分比之间的散点图，按语言类别着色。
:::


另一个可以调整的地方是图例的位置。
这属于个人偏好，对可视化并不关键。
我们用 `alt.Legend` 方法移动图例标题，
并指定把它放在图形顶部。
这样图例项会自动改成水平排列，而不是垂直排列，
不过也可以在 `alt.Legend` 中指定 `direction="vertical"`，保留垂直排列。

```{index} altair; alt.Legend
```

```{code-cell} ipython3
can_lang_plot_legend = alt.Chart(can_lang).mark_circle().encode(
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
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
# Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
glue("can_lang_plot_legend", can_lang_plot_legend.properties(height=320, width=420), display=False)
```

:::{glue:figure} can_lang_plot_legend
:figwidth: 700px
:name: can_lang_plot_legend

以某种语言为母语的加拿大人所占百分比，与以该语言为家中主要使用语言的加拿大人所占百分比之间的散点图，按语言类别着色，并调整了图例。
:::

```{index} 配色方案, 色盲模拟器
```

在 {numref}`can_lang_plot_legend` 中，点使用的是 `altair` 默认的配色方案 `"tableau10"`。
这在多数情况下都是合适的选择，色觉减弱的人也容易分辨。
一般来说，Altair 默认使用的配色方案会与所展示数据的类型相匹配，
挑选时兼顾色觉正常和色觉减弱的人，让两者都容易解读。
如果你对某个颜色搭配没有把握，可以使用
这个[色盲模拟器](https://www.color-blindness.com/coblis-color-blindness-simulator/)检查
你的可视化对色盲是否友好。

全部可用的配色方案，以及如何创建自己的配色方案，
都可以在 [Altair 文档](https://altair-viz.github.io/user_guide/customization.html#customizing-colors)中查看。
要更换图表的配色方案，
我们可以在 `color` 编码的 `scale` 中加上 `scheme` 参数。
下面我们选择 `"dark2"` 主题，结果见 {numref}`can_lang_plot_theme`。
我们还把 `shape` 图形属性映射设到 `category` 变量上；
这样每个语言类别的散点形状都不一样。这类
视觉冗余——也就是用散点的颜色和形状同时传达同一信息——能
进一步提高可视化的清晰度和可及性，
但如果形状和颜色种类太多，也会增加视觉噪声，
所以要谨慎使用。
请注意，这里我们改回使用 `mark_point`，
因为 `mark_circle` 不支持 `shape` 编码，
画出来的点永远是实心圆。

```{code-cell} ipython3
can_lang_plot_theme = alt.Chart(can_lang).mark_point(filled=True).encode(
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
    shape="category"
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
# Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
glue("can_lang_plot_theme", can_lang_plot_theme.properties(height=320, width=420), display=False)
```

<<TERM>>
tick = 刻度
tick label = 刻度标签
visual redundancy = 视觉冗余
accessibility = 可及性
<<END>>
