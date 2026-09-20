(clustering)=
# 聚类

```{code-cell} ipython3
:tags: [remove-cell]

# get rid of futurewarnings from sklearn kmeans
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from chapter_preamble import *
```

## 概述

在探索性数据分析中，我们常常需要看看数据里是否存在有意义的子组，也就是*簇*（cluster）。
这样的分组有多种用途，
例如提出新的问题，或者改进预测分析。
本章介绍如何用 k-means 算法做聚类，
并介绍选择簇数的方法。

## 本章学习目标

学完本章后，你将能够：

- 描述适合使用聚类的场景，
以及聚类能从数据中提取出什么洞见。
- 解释 k 均值聚类（k-means clustering）算法。
- 解读一次 k-means 分析的结果。
- 区分聚类、分类和回归。
- 判断聚类前何时需要对变量做缩放，并用 Python 完成缩放。
- 使用 `scikit-learn` 在 Python 中完成 k 均值聚类。
- 用肘部法则（elbow method）为 k 均值聚类选择簇数。
- 用彩色散点图在 Python 中可视化 k 均值聚类的结果。
- 描述 k 均值聚类算法的优势、局限和假设。


## 聚类

```{index} 聚类
```

聚类是一项数据分析任务，
它把数据集划分成若干彼此相关的子组。
例如，我们可以用聚类把一批文档
分成对应不同主题的组，把一份人类遗传信息数据
分成对应不同祖先亚群的组，或者把一份线上客户数据
分成对应不同购买行为的组。数据划分好之后，我们就可以
用这些子组提出关于数据的新问题，并接着做一次
预测性建模。在本课程中，聚类只用于探索性分析，
也就是揭示数据中的模式。

```{index} 分类、回归、有监督学习、无监督学习
```

请注意，聚类与分类、回归是根本不同的任务。具体来说，
分类和回归都是*有监督任务*，其中存在*响应变量*（一个
类别标签或取值），而且我们有带标签或取值的过往数据
作为例子，可以据此预测未来数据的标签或取值。相比之下，聚类是
*无监督任务*：我们没有任何响应变量的标签或取值可以依靠，
只能去理解和考察数据的结构。这种做法既有优势也有不足。
聚类不需要对数据做额外的标注或输入。例如，要把
维基百科上所有文章都手工标上主题标签几乎不可能，
但我们不用这些信息就能对文章聚类，自动找出
对应不同主题的分组。然而，既然没有响应变量，
评估一次聚类的“质量”就没那么容易。分类可以用测试数据集
衡量预测表现。聚类却没有一个公认的好办法来评估。
在本书中，我们用可视化来判断聚类的质量，
严格的评估留到更进阶的课程。

既然没有响应变量，评估一次聚类的“质量”就没那么容易。
分类可以用测试数据集衡量预测表现。聚类却没有一个公认的好
办法来评估。在本书中，我们用可视化来判断聚类的
质量，严格的评估留到更进阶的课程。

```{index} K-means
```

和分类一样，
可以用来对观测聚类、寻找子组的方法有很多。
本书重点介绍应用广泛的 k-means 算法 {cite:p}`kmeans`。
在今后的学习中，你可能还会遇到层次聚类、
主成分分析、多维标度法等等；
这些其他方法该从哪里开始学起，
可以看本章末尾的拓展资源一节。

```{index} 半监督
```

```{note}
还有一类所谓的*半监督*（semisupervised）任务：
只有一部分数据带有响应变量的标签或取值，
绝大多数数据则没有。
这类任务的目标是找出数据中的潜在结构，
从而推测缺失的标签。
例如，如果一份无标签数据集大到无法手工标注，
而你愿意提供几个有信息量的示例标签作为“种子”，
用来推测全部数据的标签，这类任务就很有用。
```

## 一个示例

```{index} Palmer 企鹅
```

本章使用的数据集来自
[`palmerpenguins` R 包](https://allisonhorst.github.io/palmerpenguins/) {cite:p}`palmerpenguins`。这份
数据由 Kristen Gorman 博士和
南极帕尔默站长期生态研究站点收集，包含
在该站点附近发现的成年企鹅的测量值（{numref}`09-penguins`）{cite:p}`penguinpaper`。
我们的目标是使用两个
变量——企鹅的喙长和鳍肢长，单位都是毫米——来判断
数据中是否存在不同类型的企鹅。
弄清这一点，或许能帮助我们用数据驱动的方式
发现和分类物种。请注意，我们把这份数据集缩减到 18 条观测和 2 个变量；
这样便于我们画出清晰的图，从教学角度说明聚类是如何运作的。

```{figure} img/clustering/gentoo.jpg
---
height: 400px
name: 09-penguins
---
一只巴布亚企鹅。
```

开始之前，我们先设置随机种子。
这样可以保证分析可复现。
本章后面会更详细地讲到，
在这里设置种子很重要，
因为 k 均值聚类算法为每个簇挑选起始位置时会用到随机性。

```{index} 种子; numpy.random.seed
```

```{code-cell} ipython3
import numpy as np

np.random.seed(6)
```

```{index} 读取函数; read_csv
```

现在我们可以读取并预览 `penguins` 数据。

```{code-cell} ipython3
import pandas as pd

penguins = pd.read_csv("data/penguins.csv")
penguins
```

我们先使用标准化后的数据 `penguins_standardized`，
来说明 k 均值聚类如何运作（回忆一下 {numref}`第 %s 章 <classification1>` 中讲过的标准化）。
本章后面会回到原始的 `penguins` 数据，看看如何把标准化自动
纳入聚类流水线。

```{code-cell} ipython3
:tags: [remove-cell]
penguins_standardized = penguins.assign(
	bill_length_standardized=(penguins["bill_length_mm"] - penguins["bill_length_mm"].mean())/penguins["bill_length_mm"].std(),
    flipper_length_standardized=(penguins["flipper_length_mm"] - penguins["flipper_length_mm"].mean())/penguins["flipper_length_mm"].std()
).drop(
    columns=["bill_length_mm", "flipper_length_mm"]
)
```

```{code-cell} ipython3
penguins_standardized
```

接下来，我们用这份数据集画一张散点图，
看看能否发现数据中的子类型或分组。

```{code-cell} ipython3
import altair as alt

scatter_plot = alt.Chart(penguins_standardized).mark_circle().encode(
    x=alt.X("flipper_length_standardized").title("Flipper Length (standardized)"),
    y=alt.Y("bill_length_standardized").title("Bill Length (standardized)")
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("scatter_plot", scatter_plot, display=True)
```

:::{glue:figure} scatter_plot
:figwidth: 700px
:name: scatter_plot

标准化喙长与标准化鳍肢长的散点图。
:::

```{index} altair、altair; mark_circle
```

从 {numref}`scatter_plot` 中的可视化结果看，
我们可能会猜想数据里有几种企鹅亚型。
在 {numref}`scatter_plot` 中大致可以看到 3 组观测，
包括：

1. 鳍肢和喙都短的一组，
2. 鳍肢短但喙长的一组，以及
3. 鳍肢和喙都长的一组。

```{index} K-means、肘部法则
```

变量个数较少时，数据可视化是帮我们粗略感受这类模式的好工具。
但如果要把数据分组——并且选出组的个数——作为
可复现分析的一部分，我们就需要稍微更自动化的手段。
另外，聚类时考虑的变量越多，
用可视化找分组就越困难。
要把数据严格地分成若干组，
就得使用聚类算法。
本章重点介绍*k-means* 算法，
一种应用广泛、往往很有效的聚类方法，
并结合*肘部法则*
来选择簇数。
这个过程会把数据分成若干组；
{numref}`colored_scatter_plot` 展示了这些组，
用不同颜色的散点表示。

```{code-cell} ipython3
:tags: [remove-cell]
from sklearn import set_config
from sklearn.cluster import KMeans

# Output dataframes instead of arrays
set_config(transform_output="pandas")

kmeans = KMeans(n_clusters=3)

penguin_clust = kmeans.fit(penguins_standardized)

penguins_clustered = penguins_standardized.assign(cluster=penguin_clust.labels_)

colored_scatter_plot = alt.Chart(penguins_clustered).mark_circle().encode(
    x=alt.X("flipper_length_standardized", title="Flipper Length (standardized)"),
    y=alt.Y("bill_length_standardized", title="Bill Length (standardized)"),
    color=alt.Color("cluster:N")
)

glue("colored_scatter_plot", colored_scatter_plot, display=True)
```

:::{glue:figure} colored_scatter_plot
:figwidth: 700px
:name: colored_scatter_plot

标准化喙长与标准化鳍肢长的散点图，各组用不同颜色标出。
:::


这些组的标签是什么？很遗憾，我们没有任何标签。k-means
和几乎所有聚类算法一样，只会输出没有意义的“簇标签”，
它们通常是整数：0、1、2、3 等。但在这样简单的情形里，
既然我们能轻松地在散点图上看到各个簇，我们就可以
根据它们在图中的位置，给这些组起人工标签：

- 鳍肢短且喙短（<font color="#f59518">橙色簇</font>），
- 鳍肢短且喙长（<font color="#4c78a8">蓝色簇</font>）。
- 鳍肢长且喙长（<font color="#e45756">红色簇</font>）。

做出这些判断之后，我们就可以用它们来辅助物种
分类，或者对数据提出更多问题。例如，我们可能
想弄清鳍肢长与喙长之间的关系，而这一关系可能因
我们手上企鹅的类型而异。

## k-means 算法

### 衡量聚类质量

```{code-cell} ipython3
:tags: [remove-cell]

clus = penguins_clustered[penguins_clustered["cluster"] == 0][["bill_length_standardized", "flipper_length_standardized"]]
```

```{index} see: 簇内平方距离和; WSSD
```

```{index} WSSD
```

k-means 算法是一种把数据分成 K 个簇的方法。
它先从数据的一个初始聚类开始，然后不断
调整数据点的簇归属来改进它，
直到无法再改进为止。但我们如何衡量
一次聚类的“质量”，“改进”又是指什么？
在 k 均值聚类中，我们用一个簇的
*簇内平方距离和（WSSD）*来衡量它的质量，它也叫*惯性（inertia）*。计算它需要两步。
第一步是计算簇中心（cluster center）：对簇内的数据点求每个变量的均值。
例如，假设有一个簇包含 4 条观测，我们用两个变量 $x$ 和 $y$ 对数据聚类，
那么簇中心的坐标 $\mu_x$ 和 $\mu_y$ 可以这样算出：


$$
\mu_x = \frac{1}{4}(x_1+x_2+x_3+x_4) \quad \mu_y = \frac{1}{4}(y_1+y_2+y_3+y_4)
$$

```{code-cell} ipython3
:tags: [remove-cell]

clus_rows = clus.shape[0]

mean_flipper_len_std = round(np.mean(clus["flipper_length_standardized"]),2)
mean_bill_len_std = round(np.mean(clus["bill_length_standardized"]),2)

glue("clus_rows_glue", "{:d}".format(clus_rows))
glue("mean_flipper_len_std_glue","{:.2f}".format(mean_flipper_len_std))
glue("mean_bill_len_std_glue", "{:.2f}".format(mean_bill_len_std))
```

```{code-cell} ipython3
:tags: [remove-cell]

toy_example_clus1_center = alt.layer(
    alt.Chart(clus).mark_circle(size=75, opacity=1, color='steelblue').encode(
        x=alt.X("flipper_length_standardized"),
        y=alt.Y("bill_length_standardized")
    ),
    alt.Chart(clus).mark_circle(color='steelblue', size=300, opacity=1, stroke='black').encode(
        x=alt.X("mean(flipper_length_standardized)")
            .scale(zero=False, padding=20)
            .title("Flipper Length (standardized)"),
        y=alt.Y("mean(bill_length_standardized)")
            .scale(zero=False, padding=30)
            .title("Bill Length (standardized)"),
    )
)

glue('toy-example-clus1-center', toy_example_clus1_center, display=True)
```

在上例的第一个簇中有 {glue:text}`clus_rows_glue` 个数据点。这些点连同它们的簇中心
（标准化鳍肢长 {glue:text}`mean_flipper_len_std_glue`，标准化喙长 {glue:text}`mean_bill_len_std_glue`）
一起展示在 {numref}`toy-example-clus1-center` 中。

:::{glue:figure} toy-example-clus1-center
:figwidth: 700px
:name: toy-example-clus1-center

`penguins_standardized` 数据集示例中的簇 0。观测用小蓝点表示，簇中心用一个带黑色描边的大蓝点高亮标出。
:::

```{code-cell} ipython3
:tags: [remove-cell]

centroid_lines = alt.Chart(
    clus.assign(
        mean_bill_length=clus['bill_length_standardized'].mean(),
        mean_flipper_length=clus['flipper_length_standardized'].mean()
    )
).mark_rule(size=1.5).encode(
    alt.Y('bill_length_standardized'),
    alt.Y2('mean_bill_length'),
    alt.X('flipper_length_standardized'),
    alt.X2('mean_flipper_length')
)
toy_example_clus1_dists = centroid_lines + toy_example_clus1_center

glue('toy-example-clus1-dists', toy_example_clus1_dists, display=True)
```

```{index} 距离; K-means
```

计算 WSSD 的第二步，是把簇内每个点到
簇中心的距离平方相加。
我们用的是直线距离／欧氏距离（Euclidean distance）公式，
也就是我们在 {numref}`第 %s 章 <classification1>` 里学过的那个公式。
在上文那个含 {glue:text}`clus_rows_glue` 条观测的簇里，
WSSD $S^2$ 的计算式是：

$$
S^2 = \left((x_1 - \mu_x)^2 + (y_1 - \mu_y)^2\right) + \left((x_2 - \mu_x)^2 + (y_2 - \mu_y)^2\right)\\
 + \left((x_3 - \mu_x)^2 + (y_3 - \mu_y)^2\right)  +  \left((x_4 - \mu_x)^2 + (y_4 - \mu_y)^2\right)
$$

在企鹅数据示例的第一个簇中，这些距离用 {numref}`toy-example-clus1-dists` 中的线段表示。

:::{glue:figure} toy-example-clus1-dists
:figwidth: 700px
:name: toy-example-clus1-dists

`penguins_standardized` 数据集示例中的簇 0。观测用小蓝点表示，簇中心用一个带黑色描边的大蓝点高亮标出。各观测到簇中心的距离用黑色线段表示。
:::

```{code-cell} ipython3
:tags: [remove-cell]

toy_example_all_clus_dists = alt.layer(
    alt.Chart(
        penguins_clustered.assign(
            mean_bill_length=penguins_clustered.groupby('cluster')['bill_length_standardized'].transform('mean'),
            mean_flipper_length=penguins_clustered.groupby('cluster')['flipper_length_standardized'].transform('mean')
        )
    ).mark_rule(size=1.25).encode(
        alt.Y('bill_length_standardized'),
        alt.Y2('mean_bill_length'),
        alt.X('flipper_length_standardized'),
        alt.X2('mean_flipper_length')
    ),
    alt.Chart(penguins_clustered).mark_circle(size=40, opacity=1).encode(
        alt.X("flipper_length_standardized"),
        alt.Y("bill_length_standardized"),
        alt.Color('cluster:N')
    ),
    alt.Chart(penguins_clustered).mark_circle(size=200, opacity=1, stroke = "black").encode(
        alt.X("mean(flipper_length_standardized)")
          .scale(zero=False)
          .title("Flipper Length (standardized)"),
        alt.Y("mean(bill_length_standardized)")
          .scale(zero=False)
          .title("Bill Length (standardized)"),
        alt.Detail('cluster:N'),
        alt.Color('cluster:N')
    )
)
glue('toy-example-all-clus-dists', toy_example_all_clus_dists, display=True)
```

$S^2$ 越大，簇就越分散，因为 $S^2$ 大意味着
各点离簇中心远。不过请注意，“大”是相对于*两方面*而言的：
既是聚类时所用变量的标度，*也是*簇内数据点的个数。如果簇里的点
都离中心很近，而簇内数据点又很多，$S^2$ 仍然可能很大。

算出所有簇的 WSSD 之后，
把它们加总就得到*总 WSSD*。在我们的例子里，
这就是把 18 条观测的全部距离平方相加。
这些距离用
{numref}`toy-example-all-clus-dists` 中的黑色线段表示。

:::{glue:figure} toy-example-all-clus-dists
:figwidth: 700px
:name: toy-example-all-clus-dists

`penguins_standardized` 数据集示例中的全部簇。观测用橙色、蓝色和黄色的小点表示，簇中心用带黑色描边的较大点表示。各观测到各自簇中心的距离用黑色线段表示。
:::

由于 k-means 用直线距离衡量聚类的质量，
它只能基于定量变量做聚类。
不过请注意，k-means 算法有一些变体，
也有其他完全不同的聚类算法，
它们使用别的距离度量，
从而可以对非定量数据聚类。
这些内容超出了本书的范围。