---
jupytext:
  formats: py:percent,md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

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

在探索性数据分析中，看看数据里是否存在有意义的子组，也就是*簇*（cluster），往往很有帮助。这样的分组有多种用途，例如提出新的问题，或者改进预测分析。本章介绍 k 均值聚类算法，并介绍选择簇数的方法。

## 本章学习目标

学完本章后，你将能够：

- 描述适合使用聚类的场景，以及聚类能从数据中提取出什么洞见。
- 解释 k 均值聚类（k-means clustering）算法。
- 解读 k 均值聚类分析的结果。
- 区分聚类、分类和回归。
- 判断聚类前何时需要对变量做缩放，并用 Python 完成缩放。
- 使用 `scikit-learn` 在 Python 中完成 k 均值聚类。
- 用肘部法则（elbow method）为 k 均值聚类选择簇数。
- 用彩色散点图在 Python 中可视化 k 均值聚类的结果。
- 描述 k 均值聚类算法的优势、局限和假设。


## 聚类

```{index} 聚类
```

聚类是一项数据分析任务，它把数据集划分成若干由相互关联的数据构成的子组。例如，我们可以用聚类把一批文档分成对应不同主题的组，把一份人类遗传信息数据分成对应不同祖先亚群的组，或者把一份线上客户数据分成对应不同购买行为的组。数据划分好之后，例如，我们可以用这些子组提出关于数据的新问题，并接着做一次预测性建模。在本课程中，聚类只用于探索性分析，也就是揭示数据中的模式。

```{index} 分类、回归、有监督学习、无监督学习
```

请注意，聚类与分类、回归是根本不同的任务。具体来说，分类和回归都是*有监督任务*，其中存在*响应变量*（一个类别标签或取值），而且我们有带标签或取值的过往数据作为例子，可以据此预测未来数据的标签或取值。相比之下，聚类是*无监督任务*：我们没有任何响应变量的标签或取值可以依靠，只能去理解和考察数据的结构。这种做法既有优势也有不足。聚类不需要对数据做额外的标注或输入。例如，要把维基百科上所有文章都手工标上主题标签几乎不可能，但我们不用这些信息就能对文章聚类，自动找出对应不同主题的分组。然而，既然没有响应变量，评估一次聚类的“质量”就没那么容易。分类可以用测试数据集衡量预测表现。聚类则没有唯一的最佳评估方法。在本书中，我们用可视化来判断聚类的质量，严格的评估留到更进阶的课程。

既然没有响应变量，评估一次聚类的“质量”就没那么容易。分类可以用测试数据集衡量预测表现。聚类则没有唯一的最佳评估方法。在本书中，我们用可视化来判断聚类的质量，严格的评估留到更进阶的课程。

```{index} K-means
```

和分类一样，可以用来对观测聚类、寻找子组的方法有很多。本书重点介绍应用广泛的 k 均值聚类算法 {cite:p}`kmeans`。在今后的学习中，你可能还会遇到层次聚类、主成分分析、多维标度法等等；这些其他方法该从哪里开始学起，可以看本章末尾的拓展资源一节。

```{index} 半监督
```

```{note}
还有一类所谓的*半监督*（semisupervised）任务：只有一部分数据带有响应变量的标签或取值，绝大多数数据则没有。这类任务的目标是找出数据中的潜在结构，从而推测缺失的标签。例如，如果一份无标签数据集大到无法手工标注，而你愿意提供几个有信息量的示例标签作为“种子”，用来推测全部数据的标签，这类任务就很有用。
```

## 一个示例

```{index} Palmer 企鹅
```

本章使用的数据集来自 [`palmerpenguins` R 包](https://allisonhorst.github.io/palmerpenguins/) {cite:p}`palmerpenguins`。这份数据由 Kristen Gorman 博士和南极帕尔默站长期生态研究站点收集，包含在该站点附近发现的成年企鹅的测量值（{numref}`09-penguins`）{cite:p}`penguinpaper`。我们的目标是使用两个变量——企鹅的喙长和鳍肢长，单位都是毫米——来判断数据中是否存在不同类型的企鹅。弄清这一点，或许能帮助我们用数据驱动的方式发现和分类物种。请注意，我们把这份数据集缩减到 18 条观测和 2 个变量；这样便于我们画出清晰的图，从教学角度说明聚类是如何运作的。

```{figure} img/clustering/gentoo.jpg
---
height: 400px
name: 09-penguins
---
一只巴布亚企鹅。
```

开始之前，我们先设置随机种子。这样可以保证分析可复现。本章后面会更详细地讲到，在这里设置种子很重要，因为 k 均值聚类算法为每个簇挑选起始位置时会用到随机性。

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

我们先使用标准化后的数据 `penguins_standardized`，来说明 k 均值聚类如何运作（回忆一下{numref}`第 %s 章 <classification1>`中讲过的标准化）。本章后面会回到原始的 `penguins` 数据，看看如何把标准化自动纳入聚类流水线。

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

接下来，我们用这份数据集画一张散点图，看看能否发现数据中的子类型或分组。

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

从{numref}`scatter_plot` 中的可视化结果看，我们可能会猜想数据里有几种企鹅亚型。在{numref}`scatter_plot` 中大致可以看到 3 组观测，包括：

1. 鳍肢和喙都短的一组，
2. 鳍肢短但喙长的一组，以及
3. 鳍肢和喙都长的一组。

```{index} K-means、肘部法则
```

变量个数较少时，数据可视化是帮我们粗略感受这类模式的好工具。但如果要把数据分组——并且选出组的个数——作为可复现分析的一部分，我们就需要稍微更自动化的手段。另外，聚类时考虑的变量越多，用可视化找分组就越困难。要把数据严格地分成若干组，就得使用聚类算法。本章重点介绍 *k 均值聚类*算法，一种应用广泛、往往很有效的聚类方法，并结合*肘部法则*来选择簇数。这个过程会把数据分成若干组；{numref}`colored_scatter_plot` 展示了这些组，用不同颜色的散点表示。

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


这些组的标签是什么？很遗憾，我们没有任何标签。k 均值聚类和几乎所有聚类算法一样，只会输出没有意义的“簇标签”，它们通常是整数：0、1、2、3 等。但在这样简单的情形里，既然我们能轻松地在散点图上看到各个簇，我们就可以根据它们在图中的位置，给这些组起人工标签：

- 鳍肢短且喙短（<font color="#f59518">橙色簇</font>），
- 鳍肢短且喙长（<font color="#4c78a8">蓝色簇</font>）。
- 鳍肢长且喙长（<font color="#e45756">红色簇</font>）。

做出这些判断之后，我们就可以用它们来辅助物种分类，或者对数据提出更多问题。例如，我们可能想弄清鳍肢长与喙长之间的关系，而这一关系可能因我们手上企鹅的类型而异。

## k 均值聚类

### 衡量聚类质量

```{code-cell} ipython3
:tags: [remove-cell]

clus = penguins_clustered[penguins_clustered["cluster"] == 0][["bill_length_standardized", "flipper_length_standardized"]]
```

```{index} see: 簇内平方距离和; WSSD
```

```{index} WSSD
```

k 均值聚类算法是一种把数据分成 K 个簇的方法。它先从数据的一个初始聚类开始，然后不断调整数据点的簇归属来改进它，直到无法再改进为止。但我们如何衡量一次聚类的“质量”，“改进”又是指什么？在 k 均值聚类中，我们用一个簇的*簇内平方距离和*（within-cluster sum-of-squared-distances，WSSD）来衡量它的质量，它也叫*惯性（inertia）*。计算它需要两步。第一步是计算簇中心（cluster center）：对簇内的数据点求每个变量的均值。例如，假设有一个簇包含 4 条观测，我们用两个变量 $x$ 和 $y$ 对数据聚类，那么簇中心的坐标 $\mu_x$ 和 $\mu_y$ 可以这样算出：


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

在上例的第一个簇中有 {glue:text}`clus_rows_glue` 个数据点。这些点连同它们的簇中心（标准化鳍肢长 {glue:text}`mean_flipper_len_std_glue`，标准化喙长 {glue:text}`mean_bill_len_std_glue`）一起展示在{numref}`toy-example-clus1-center` 中。

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

计算 WSSD 的第二步，是把簇内每个点到簇中心的距离平方相加。我们用的是直线距离／欧氏距离（Euclidean distance）公式，也就是我们在{numref}`第 %s 章 <classification1>`里学过的那个公式。在上文那个含 {glue:text}`clus_rows_glue` 条观测的簇里，WSSD $S^2$ 的计算式是：

$$
S^2 = \left((x_1 - \mu_x)^2 + (y_1 - \mu_y)^2\right) + \left((x_2 - \mu_x)^2 + (y_2 - \mu_y)^2\right)\\
 + \left((x_3 - \mu_x)^2 + (y_3 - \mu_y)^2\right)  +  \left((x_4 - \mu_x)^2 + (y_4 - \mu_y)^2\right)
$$

在企鹅数据示例的第一个簇中，这些距离用{numref}`toy-example-clus1-dists` 中的线段表示。

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

$S^2$ 越大，簇就越分散，因为 $S^2$ 大意味着各点离簇中心远。不过请注意，“大”是相对于*两方面*而言的：既是聚类时所用变量的标度，*也是*簇内数据点的个数。如果簇里的点都离中心很近，而簇内数据点又很多，$S^2$ 仍然可能很大。

算出所有簇的 WSSD 之后，把它们加总就得到*总 WSSD*。在我们的例子里，这就是把 18 条观测的全部距离平方相加。这些距离用{numref}`toy-example-all-clus-dists` 中的黑色线段表示。

:::{glue:figure} toy-example-all-clus-dists
:figwidth: 700px
:name: toy-example-all-clus-dists

`penguins_standardized` 数据集示例中的全部簇。观测用橙色、蓝色和黄色的小点表示，簇中心用带黑色描边的较大点表示。各观测到各自簇中心的距离用黑色线段表示。
:::

由于 k 均值聚类用直线距离衡量聚类的质量，它只能基于定量变量做聚类。不过请注意，k 均值聚类算法有一些变体，也有其他完全不同的聚类算法，它们使用别的距离度量，从而可以对非定量数据聚类。这些内容超出了本书的范围。

+++

### 聚类算法

```{index} K-means; 算法
```

```{code-cell} ipython3
:tags: [remove-cell]

# Set up the initial "random" label assignment the same as in the R book
penguins_standardized['label'] = [
    2, 2, 1, 1, 0, 0, 0, 1,
    2, 2, 1, 2, 1, 2,
    0, 1, 2, 2
]
points_kmeans_init = alt.Chart(penguins_standardized).mark_point(size=75, filled=True, opacity=1).encode(
    alt.X("flipper_length_standardized").title("Flipper Length (standardized)"),
    alt.Y("bill_length_standardized").title("Bill Length (standardized)"),
    alt.Color('label:N').legend(None),
    alt.Shape('label:N').legend(None).scale(range=['square', 'circle', 'triangle']),
    alt.Size('label:O').legend(None).scale(type='ordinal', range=[50, 50, 100]),
)

glue('toy-kmeans-init-1', points_kmeans_init, display=True)
```

我们开始 k 均值聚类算法，先选定 K，再把数量大致相等的观测随机分配到这 K 个簇中。一个随机初始化的例子见{numref}`toy-kmeans-init-1`。


:::{glue:figure} toy-kmeans-init-1
:figwidth: 700px
:name: toy-kmeans-init-1

标签的随机初始化。每个簇用不同的颜色和形状表示。
:::

```{code-cell} ipython3
:tags: [remove-cell]

from sklearn.metrics import euclidean_distances

def plot_kmean_iterations(iterations, data, centroid_init):
    """Plot kmeans cluster and label updates for multiple iterations"""
    dfs = []
    centroid_inits = []
    for i in range(1, iterations+1):
        data['iteration'] = f'Iteration {i}'
        data['update_type'] = 'Center Update'
        data['flipper_centroid'] = data['label'].map(centroid_init['flipper_length_standardized'])
        data['bill_centroid'] = data['label'].map(centroid_init['bill_length_standardized'])
        dfs.append(data.copy())

        data['iteration'] = f'Iteration {i}'
        data['update_type'] = 'Label Update'
        cluster_columns = ['bill_length_standardized', 'flipper_length_standardized']
        data['label'] = np.argmin(euclidean_distances(data[cluster_columns], centroid_init), axis=1)
        data['flipper_centroid'] = data['label'].map(centroid_init['flipper_length_standardized'])
        data['bill_centroid'] = data['label'].map(centroid_init['bill_length_standardized'])
        dfs.append(data.copy())

        centroid_init = data.groupby('label')[cluster_columns].mean()

    points = alt.Chart(
        pd.concat(dfs),
        width=200,
        height=200
    ).mark_point(filled=True, size=50, opacity=1).encode(
        alt.X("flipper_length_standardized").scale(domain=(-2, 2)),
        alt.Y("bill_length_standardized").scale(domain=(-2, 2)),
        alt.Color('label:N').legend(None),
        alt.Shape('label:N').legend(None).scale(range=['square', 'circle', 'triangle']),
        alt.Size('label:O').legend(None).scale(type='ordinal', range=[50, 50, 100]),
    )

    centroids = points.mark_point(filled=True, stroke='black', strokeWidth=1.25).encode(
        alt.X("mean(flipper_centroid)")
            .scale(domain=(-2, 2))
            .title("Flipper Length (standardized)"),
        alt.Y("mean(bill_centroid)")
            .scale(domain=(-2, 2))
            .title("Bill Length (standardized)"),
        size=alt.value(200)
    )

    return (points + centroids).facet(
        row=alt.Row('iteration', header=alt.Header(title='', labelFontSize=18)),
        column=alt.Column('update_type', header=alt.Header(title='', labelFontSize=18))
    )
```

```{code-cell} ipython3
:tags: [remove-cell]

centroid_init = penguins_standardized.groupby('label').mean()

glue('toy-kmeans-iter-1', plot_kmean_iterations(3, penguins_standardized.copy(), centroid_init.copy()), display=True)
```

```{index} WSSD; 总计
```

接下来，k 均值聚类包含两个主要步骤，它们都力求最小化所有簇的 WSSD 之和，即*总 WSSD*：

1. **中心更新**：计算每个簇的中心。
2. **标签更新**：把每个数据点重新分配到簇中心离它最近的那个簇。

这两个步骤反复执行，直到簇归属不再发生变化。k 均值聚类前三轮迭代的情形见{numref}`toy-kmeans-iter-1`。每一行对应一轮迭代：其中左列展示中心更新，右列展示标签更新（也就是把数据重新分配到各簇）。

:::{glue:figure} toy-kmeans-iter-1
:figwidth: 700px
:name: toy-kmeans-iter-1

在 `penguins_standardized` 示例数据集上做 k 均值聚类的前三轮迭代。每一对图对应一轮迭代。每对图中，第一幅图展示中心更新，第二幅图展示把数据重新分配到簇的结果。簇中心用带黑色描边的较大点表示。
:::

+++

请注意，此时我们就可以终止算法了，因为第三轮迭代中没有任何归属发生变化；从此往后，簇中心和标签都将保持不变。

```{index} K-means; 终止
```

```{note}
k 均值聚类*保证*会停下来吗，还是会永远迭代下去？好在答案是：k 均值聚类保证在*若干*轮迭代之后停止。如果你感兴趣，可以看看背后的推理，它分三步：（1）每一轮迭代中，标签更新和中心更新都会让总 WSSD 下降；（2）总 WSSD 总是大于或等于 0；（3）把数据分配到簇的方式只有有限多种。因此到了某个时刻，总 WSSD 必然不再下降，这意味着没有任何归属在发生变化，算法也就终止了。
```

### 随机重启

```{index} K-means; 重启
```

与前面几章学过的分类和回归模型不同，k 均值聚类可能会“卡”在劣质解里。例如，{numref}`toy-kmeans-bad-init-1` 展示了 k 均值聚类一次运气不佳的随机初始化。

```{code-cell} ipython3
:tags: [remove-cell]

# Set up the initial "random" label assignment the same as in the R book
penguins_standardized['label'] = [1, 1, 2, 2, 0, 2, 0, 2, 2, 2, 1, 2, 0, 0, 0, 1, 1, 1]
centroid_init = penguins_standardized.groupby('label').mean()

points_kmeans_init = alt.Chart(penguins_standardized).mark_point(size=75, filled=True, opacity=1).encode(
    alt.X("flipper_length_standardized").title("Flipper Length (standardized)"),
    alt.Y("bill_length_standardized").title("Bill Length (standardized)"),
    alt.Color('label:N').legend(None),
    alt.Shape('label:N').legend(None).scale(range=['square', 'circle', 'triangle']),
    alt.Size('label:O').legend(None).scale(type='ordinal', range=[50, 50, 100]),
)

glue('toy-kmeans-bad-init-1', points_kmeans_init, display=True)
```

:::{glue:figure} toy-kmeans-bad-init-1
:figwidth: 700px
:name: toy-kmeans-bad-init-1

标签的随机初始化。
:::

```{code-cell} ipython3
:tags: [remove-cell]

glue('toy-kmeans-bad-iter-1', plot_kmean_iterations(4, penguins_standardized.copy(), centroid_init.copy()), display=True)
```

{numref}`toy-kmeans-bad-iter-1` 展示了在采用{numref}`toy-kmeans-bad-init-1` 中那种运气不佳的随机初始化时，k 均值聚类的迭代过程会是什么样子


:::{glue:figure} toy-kmeans-bad-iter-1
:figwidth: 700px
:name: toy-kmeans-bad-iter-1

随机初始化效果很差时，在 `penguins_standardized` 示例数据集上做 k 均值聚类的前四轮迭代。每一对图对应一轮迭代。每对图中，第一幅图展示中心更新，第二幅图展示把数据重新分配到簇的结果。簇中心用带黑色描边的较大点表示。
:::

这个聚类结果看起来相对较差，但 k 均值聚类无法改进它。用 k 均值聚类给数据分组时，要解决这个问题，我们应该把标签随机重新初始化几次，对每次初始化各运行一遍 k 均值聚类，然后选出最终总 WSSD 最低的那个聚类结果。

### 选择 K

要用 k 均值聚类对数据分组，我们还必须选定簇数 K。但与分类不同，这里没有响应变量，也无法用某种模型预测误差指标来做交叉验证。此外，K 选得太小，多个簇就会被合并到一起；K 选得太大，簇又会被细分。无论哪种情况，我们都可能漏掉数据中有趣的结构。{numref}`toy-kmeans-vary-k-1` 展示了 K 的取值对这份企鹅鳍肢长与喙长数据做 k 均值聚类的影响：图中给出了 K 从 1 到 9 时各不相同的聚类结果。

```{code-cell} ipython3
:tags: [remove-cell]

from sklearn.cluster import KMeans

penguins_standardized = penguins_standardized.drop(columns=["label"])

dfs = []
inertias = []
for i in range(1, 10):
    data = penguins_standardized.copy()
    knn = KMeans(n_clusters=i, n_init='auto')
    knn.fit(data)
    data['n_clusters'] = f'{i} Cluster' + ('' if i == 1 else 's')
    data['label'] = knn.labels_
    dfs.append(data)
    inertias.append(knn.inertia_)

points = alt.Chart(pd.concat(dfs), width=200, height=200).mark_point(filled=True, opacity=1).encode(
    alt.X('bill_length_standardized')
        .scale(zero=False)
        .title("Flipper Length (standardized)"),
    alt.Y('flipper_length_standardized')
        .scale(zero=False)
        .title("Bill Length (standardized)"),
    alt.Color('label:N').legend(None),
    alt.Shape('label:N').legend(None).scale(range=['square', 'circle', 'triangle', 'cross', 'diamond', 'triangle-right', 'triangle-down', 'triangle-left']),
    alt.Size('label:O').legend(None).scale(type='ordinal', range=[50, 50, 100, 100, 100, 100, 100, 100]),
    # alt.Shape('label:N').legend(None),
)

vary_k = alt.layer(
    points,
    points.mark_point(filled=True, stroke='black', strokeWidth=1.25).encode(
        alt.X('mean(bill_length_standardized)'),
        alt.Y('mean(flipper_length_standardized)'),
        size=alt.value(200)
    )
).facet(
    alt.Facet(
        'n_clusters:N',
        header=alt.Header(title='', labelFontSize=16)
    ),
    columns=3
)
glue('toy-kmeans-vary-k-1', vary_k, display=True)
```



:::{glue:figure} toy-kmeans-vary-k-1
:figwidth: 700px
:name: toy-kmeans-vary-k-1

K 从 1 到 9 时企鹅数据的聚类结果。簇中心用带黑色描边的较大点表示。
:::


```{index} 肘部法则
```

如果把 K 设得小于 3，聚类就会把本来分开的几组数据合并到一起；这会导致很大的总 WSSD，因为簇中心（图中用带黑色描边的较大形状表示）离簇内任何一个数据点都不近。反过来，如果把 K 设得大于 3，聚类就会把数据中的子组进一步细分；这样做确实仍能让总 WSSD 下降，但下降的幅度*越来越小*。如果把总 WSSD 对簇数作图，就会看到：当我们取到大致合适的簇数时，总 WSSD 的下降趋于平缓，或者形成一个“肘部形状”（{numref}`toy-kmeans-elbow`）。

```{code-cell} ipython3
:tags: [remove-cell]

elbow_plot = alt.layer(
    alt.Chart(
        pd.DataFrame({
            'wssd': inertias,
            'k': range(1, len(inertias) + 1)
        })
    ).mark_line(point=True).encode(
        x=alt.X("k").title("Number of clusters"),
        y=alt.Y("wssd").title("Total within-cluster sum of squares"),
    ),
    alt.Chart().mark_text(size=22, align='left', baseline='bottom').encode(
        x=alt.datum(3.3),
        y=alt.datum(9.8),
        text=alt.datum('Elbow')
    ),
    alt.Chart().mark_text(size=50, align='left', baseline='bottom', fontWeight=100, angle=25).encode(
        x=alt.datum(2.8),
        y=alt.datum(5),
        text=alt.datum('🠃')
    )
)

glue('toy-kmeans-elbow', elbow_plot, display=True)
```

:::{glue:figure} toy-kmeans-elbow
:figwidth: 700px
:name: toy-kmeans-elbow

K 取 1 到 9 时的总 WSSD。
:::

## 用 Python 实现 k 均值聚类

```{index} K-means, scikit-learn; KMeans
```

```{index} see: KMeans; scikit-learn
```

在 Python 中做 k 均值聚类时，所用的工作流与前面分类、回归两章类似。回到原始的（未标准化的）`penguins` 数据，回忆一下：k 均值聚类用直线距离判断哪些点彼此相似。因此，数据中各个变量的*标度*会影响数据点最终被分到哪个簇。标度大的变量在决定簇归属时，作用比标度小的变量大得多。为解决这个问题，我们通常在聚类前对数据做标准化，这样可以保证每个变量的均值为 0、标准差为 1。`scikit-learn` 中的 `StandardScaler` 函数就能完成这件事。

```{index} scikit-learn; StandardScaler, scikit-learn;KMeans, 标准化;K-means, K-means;标准化
```

```{code-cell} ipython3
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")

preprocessor = make_column_transformer(
    (StandardScaler(), ["bill_length_mm", "flipper_length_mm"]),
    verbose_feature_names_out=False,
)
preprocessor
```

为了表明做的是 k 均值聚类，我们要创建一个 `KMeans` 模型对象。它至少接受一个参数：簇数 `n_clusters`，这里设为 3。

```{index} KMeans;n_clusters
```

```{code-cell} ipython3
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
kmeans
```

```{index} scikit-learn;make_pipeline, scikit-learn;Pipeline, scikit-learn;fit
```

要真正运行 k 均值聚类，我们把预处理器和模型对象组合进 `Pipeline`，再调用 `fit` 函数。请注意，k 均值聚类算法对簇归属做随机初始化，不过本章开头已经设定了随机种子，所以这次聚类的结果可以复现。

```{code-cell} ipython3
from sklearn.pipeline import make_pipeline

penguin_clust = make_pipeline(preprocessor, kmeans)
penguin_clust.fit(penguins)
penguin_clust
```

```{index} KMeans; labels_, KMeans; inertia_
```

拟合好的 `KMeans` 对象——它是流水线中的第二项，可以用 `penguin_clust[1]` 取到——包含很多信息，可用来可视化各个簇、选取 K 以及评估总 WSSD。我们先来把各个簇画成彩色散点图！为此，需要先把簇归属添加到原始的 `penguins` 数据框中。这些信息可以从聚类对象的 `labels_` 属性中取出（“labels”是聚类中“assignments”的常见替代说法），再添加到数据框中。

```{code-cell} ipython3
penguins["cluster"] = penguin_clust[1].labels_
penguins
```

现在 `penguins` 数据框中已经包含了簇归属，我们可以像{numref}`cluster_plot` 那样把它们可视化出来。请注意，这里画的是*未标准化*的数据；如果出于某种原因想可视化*标准化*的数据，就得先直接在 `StandardScaler` 预处理器上调用 `fit` 和 `transform` 函数把它取出来。和{numref}`第 %s 章 <viz>`一样，加上 `:N` 后缀能让 `altair` 把 `cluster` 变量当作名义型／分类变量，从而在可视化时使用离散的颜色映射。

```{index} altair; :N
```

```{code-cell} ipython3
cluster_plot=alt.Chart(penguins).mark_circle().encode(
    x=alt.X("flipper_length_mm").title("Flipper Length").scale(zero=False),
    y=alt.Y("bill_length_mm").title("Bill Length").scale(zero=False),
    color=alt.Color("cluster:N").title("Cluster"),
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cluster_plot", cluster_plot, display=True)
```

:::{glue:figure} cluster_plot
:figwidth: 700px
:name: cluster_plot

按 k 均值聚类返回的簇归属给数据着色。
:::

```{index} WSSD; 总计, KMeans; inertia_
```

```{index} see: WSSD; KMeans
```

前面提到过，我们还需要通过观察总 WSSD 随簇数变化的图形，找到“肘部”出现的位置，从而选定 K。总 WSSD 存放在聚类对象的 `.inertia_` 属性里（“inertia”是 `scikit-learn` 用来表示 WSSD 的术语）。

```{code-cell} ipython3
penguin_clust[1].inertia_
```

要计算各种 K 取值下的总 WSSD，我们需要创建一个数据框，其中包含不同的 `k` 取值，以及用每个 k 值运行 k 均值聚类得到的 WSSD。为了创建这个数据框，我们要用到 Python 中的“列表推导式（list comprehension）”：把同一个操作重复执行多次，并把结果放进列表返回。下面这个列表推导式的例子把 0 到 2 这几个数存进列表：

```{index} 列表推导式
```

```{code-cell} ipython3
[n for n in range(3)]
```

列表推导式里的变量 `n` 可以随意改名，也可以在其中执行任何想做的运算。例如，可以把 1 到 4 这些数都平方后存进列表：

```{code-cell} ipython3
[number**2 for number in range(1, 5)]
```

接下来，我们用这个办法计算 K 取 1 到 9 时的 WSSD。对每个 K 值，都新建一个 `KMeans` 模型，再和前面创建的预处理器一起包进 `scikit-learn` 流水线。我们把算出的 WSSD 存进列表，再用它创建一个数据框，同时包含各 K 取值和对应的 WSSD。

```{note}
我们创建变量 `ks` 来保存待考察的 k 取值范围，这样一旦决定改用别的 k 值，只需要在一处修改。否则，很容易忘记在列表推导式或数据框赋值中一并更新。如果同一个取值要用多次，把它赋给变量名后复用最稳妥。
```

```{code-cell} ipython3
ks = range(1, 10)
wssds = [
    make_pipeline(
    	preprocessor,
    	KMeans(n_clusters=k)  # Create a new KMeans model with `k` clusters
    ).fit(penguins)[1].inertia_
    for k in ks
]

penguin_clust_ks = pd.DataFrame({
    "k": ks,
    "wssd": wssds,
})

penguin_clust_ks
```

现在数据框中已经有了 `wssd` 和 `k` 两列，我们可以画一张折线图（{numref}`elbow_plot`），寻找其中的“肘部”，据此确定该用哪个 K 值。

```{code-cell} ipython3
elbow_plot = alt.Chart(penguin_clust_ks).mark_line(point=True).encode(
    x=alt.X("k").title("Number of clusters"),
    y=alt.Y("wssd").title("Total within-cluster sum of squares"),
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("elbow_plot", elbow_plot, display=True)
```

:::{glue:figure} elbow_plot
:figwidth: 700px
:name: elbow_plot

总 WSSD 随簇数变化的图。
:::

看起来这组数据选三个簇最合适，因为折线的“肘部”在这里最明显。从图中还能看出，WSSD 一直在下降，这与增加簇数时的预期一致。不过，肘部图上也可能出现某一步 WSSD 上升的情形，让折线上鼓起一个小峰。这是因为初始中心位置碰巧选得不好时，k 均值聚类可能“卡”在劣质解里，本章前面已经提到过这一点。

```{index} KMeans; n_init
```

```{note}
`scikit-learn` 实现的 k 均值聚类很少卡在劣质解里，因为 `scikit-learn` 会谨慎地选取初始中心，尽量避免这种情况发生。如果你画的肘部图上仍然出现了小峰，可以在创建 `KMeans` 对象时调大 `n_init` 参数，例如 `KMeans(n_clusters=k, n_init=10)`，多尝试几种不同的随机中心初始化。从分析的角度看，这个值越大越好，但有个权衡取舍：聚类次数一多，耗时就会很长。
```

## 习题

本章讲到的内容配有练习题，可在配套的[练习册仓库](https://worksheets.python.datasciencebook.ca)的“聚类（Clustering）”一行中找到。你可以预览本章练习册（worksheet）的非交互版本，只需点击“查看练习册（view worksheet）”。如果要交互式地做习题，请按照练习册仓库中的说明下载所有练习册，并按照{numref}`第 %s 章 <move-to-your-own-machine>`中的计算机配置说明做好准备。这样才能保证练习册提供的自动反馈和指导按预期发挥作用。

## 拓展资源

- 《An Introduction to Statistical Learning》第 10 章 {cite:p}`james2013introduction` 是继续学习聚类以及一般意义上的无监督学习的绝佳去处。单就聚类而言，它提供了与 k 均值聚类配套的出色入门介绍，还讲了*层次*聚类，适用于你预期数据中存在子组、子组之中又有子组等情况。在更一般的无监督学习方面，它介绍了*主成分分析（PCA）*，这是减少数据集中预测变量个数时很常用的一种方法。

+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
