---
jupytext:
  formats: py:percent,md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(inference)=
# 统计推断

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
```

## 概述

在实际的数据分析中，一项典型任务是根据从总体中抽取的观测数据，对感兴趣的总体某个未知方面作出结论；我们通常拿不到*整个*总体的数据。数据集中的各种汇总、模式、趋势或关系如何推广到更大的总体，这类数据分析问题称为*推断性问题*（inferential question）。本章先介绍从总体中抽样的基本思想，再介绍统计推断中的两种常用技术：*点估计*与*区间估计*。

## 本章学习目标

学完本章后，你将能够：

- 描述可以用统计推断回答的真实问题示例。
- 定义常见的总体参数（例如均值、比例、标准差）——这些参数通常用抽样数据来估计——并根据样本估计这些参数。
- 定义以下统计抽样术语：总体、样本、总体参数、点估计和抽样分布。
- 解释总体参数与样本点估计之间的区别。
- 用 Python 从有限总体中抽取随机样本。
- 用 Python 根据有限总体构造抽样分布。
- 说明样本量如何影响抽样分布。
- 定义自助法（bootstrap）。
- 用 Python 构造自助分布来近似抽样分布。
- 对比自助分布与抽样分布。

+++

## 为什么需要抽样？

我们常常需要了解：从一部分数据中观测到的量，与更大总体中同样的量之间有什么关系。例如，假设一家零售商正在考虑销售 iPhone 配件，他们想估计这个市场可能有多大。此外，他们还想制定策略，思考如何把产品推销到北美的高校校园。这位零售商可能会提出下面这个问题：

*北美所有本科生中拥有 iPhone 的比例是多少？*

```{index} 总体, 总体; 参数
```

在上面这个问题中，我们想对北美*所有*本科生作出结论；这些学生的全体就称为**总体**。一般来说，总体就是我们想要研究的全部个体或个案。此外，上面这个问题要计算的是一个基于整个总体的量——拥有 iPhone 的比例。这个比例称为**总体参数**。一般来说，总体参数是整个总体的一个数值特征。要算出上例中的这个数值，我们得逐一询问北美的每一位本科生是否拥有 iPhone。在实践中，直接计算总体参数往往既费时又费钱，有时甚至无法做到。

```{index} 样本, 样本; 估计, 推断
```

```{index} see: 统计推断; 推断
```

更实际的做法是针对**样本**做测量，也就是从总体中抽取的一部分个体。然后我们可以计算一个**样本估计值**——样本的某个数值特征——用它来估计总体参数。例如，假设我们在北美随机抽取十名本科生（即样本），算出其中拥有 iPhone 的学生所占的比例（即样本估计值）。这时，我们也许会觉得这个比例可以合理地估计整个总体中拥有 iPhone 的学生比例。{numref}`fig:11-population-vs-sample` 展示了这一过程。一般来说，利用样本对抽取该样本的更大总体作出结论，这一过程称为**统计推断**。

+++

```{figure} img/inference/population_vs_sample.png
:name: fig:11-population-vs-sample

用更大总体中的样本得到总体参数点估计的过程。在本例中，一个容量为 10 的样本里有 6 人拥有 iPhone，由此算出的 iPhone 拥有者总体比例估计值为 60%。这张示例图中实际的总体比例是 53.8%。
```

+++

请注意，比例并不是我们可能关心的*唯一*一种总体参数。例如，假设一名在加拿大不列颠哥伦比亚大学读书的本科生想租一套公寓。这名学生需要制定预算，所以想了解不列颠哥伦比亚省温哥华市单间公寓的租金情况。这名学生可能会提出下面这个问题：

*加拿大温哥华的单间公寓平均月租金是多少？*

在这个例子里，总体是温哥华所有出租的单间公寓，总体参数是*平均月租金*。这里我们用平均数作为集中趋势的度量，来描述单间公寓租金的“典型取值”。但即便只在这一个例子里，我们也可能关心许多其他总体参数。比如，我们知道温哥华并不是每套单间公寓的月租金都相同。这名学生可能想了解月租金的波动有多大，希望找到一个衡量租金离散程度（或变异性）的指标，例如标准差。又或者，这名学生可能关心月租金超过 \$1000 的单间公寓所占的比例。我们想回答的问题会帮助我们确定要估计的参数。如果我们有办法观测到温哥华所有出租的单间公寓，就能精确算出上面每一个数；因此，这些都是总体参数。在实践中你会遇到许多种观测和总体参数，但本章只关注两类情形：

1. 用类别型观测估计某个类别的比例
2. 用定量观测估计平均数（或均值）

+++

## 抽样分布

### 比例的抽样分布

```{index} Airbnb
```

我们来看一个例子，用的是 [Inside Airbnb](http://insideairbnb.com/) 的数据 {cite:p}`insideairbnb`。Airbnb 是一个在线平台，可以预订度假短租和住宿场所。这份数据集包含加拿大温哥华 2020 年 9 月的房源信息。我们的数据包括 ID 编号、街区、房间类型、房源可容纳的人数、浴室数、卧室数、床位数以及每晚价格。

```{code-cell} ipython3
import pandas as pd

airbnb = pd.read_csv("data/listings.csv")
airbnb
```

假设温哥华市政府想了解 Airbnb 租赁信息，以便规划市政条例；他们想知道有多少 Airbnb 房源被列为整套住宅和公寓（而不是私人房间或共享房间）。因此，他们可能想估计所有 Airbnb 房源中房间类型列为“整套住宅或公寓”的真实比例。当然，我们通常拿不到真实的总体，但这里不妨（出于学习目的）设想这份数据集就代表了加拿大温哥华全部 Airbnb 出租房源的总体。我们可以像前面几章那样，用 `value_counts` 函数配合 `normalize` 参数，求出每种房间类型的房源比例。

```{index} DataFrame; [], DataFrame; value_counts
```

```{code-cell} ipython3
airbnb["room_type"].value_counts(normalize=True)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("population_proportion", "{:.3f}".format(airbnb["room_type"].value_counts(normalize=True)["Entire home/apt"]))
```

可以看到，数据集中 `Entire home/apt` 房源的比例是 {glue:text}`population_proportion`。这个值 {glue:text}`population_proportion` 就是总体参数。请记住，在真实的数据分析问题中，这个参数取值通常是未知的，因为一般无法对整个总体做测量。

```{index} DataFrame; sample, 种子;numpy.random.seed
```

也许我们可以用一小部分数据来近似它！为了探究这个想法，我们来随机抽取 40 个房源（*即*从总体中抽取容量为 40 的随机样本），并计算这个样本的比例。我们将用 `DataFrame` 对象的 `sample` 方法抽取样本。`sample` 的参数 `n` 指定要抽取的样本量。由于这里开始用到随机性，我们还会用 numpy 设置随机种子，让结果可以复现。

```{code-cell} ipython3
import numpy as np


np.random.seed(155)

airbnb.sample(n=40)["room_type"].value_counts(normalize=True)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("sample_1_proportion", "{:.3f}".format(airbnb.sample(n=40, random_state=155)["room_type"].value_counts(normalize=True)["Entire home/apt"]))
```

```{index} DataFrame; value_counts
```

可以看到，这个随机样本中整套住宅/公寓房源的比例是 {glue:text}`sample_1_proportion`。哇——这和真实的总体取值很接近！但别忘了，这个比例是用容量为 40 的随机样本算出来的。由此产生两个结果。第一，这个值只是一个*估计值*，也就是我们利用这个样本对总体参数作出的最佳猜测。既然这里估计的只是单个数值，我们通常称它为**点估计**。第二，由于样本是随机抽取的，如果我们再抽取*另一个*容量为 40 的随机样本并计算它的比例，答案就不会相同：

```{code-cell} ipython3
airbnb.sample(n=40)["room_type"].value_counts(normalize=True)
```

果然如此！这一次我们得到的估计值不同了。这说明我们的点估计可能并不可靠。的确，由于存在**抽样变异性**，估计值会随样本不同而变化。那么，我们应该预期随机样本的估计值有多大变化？换句话说，仅凭单个样本得到的点估计，到底有多可信？

```{index} 抽样分布
```

为了弄清楚这一点，我们将从房源总体中模拟抽取许多个样本（远远多于两个），每个样本的容量都是 40，并计算每个样本中整套住宅/公寓房源的比例。这次模拟会产生许多样本比例，我们可以用直方图把它们画出来。从一个总体中抽取给定容量（我们通常记作 $n$）的全部可能样本，其估计值的分布称为**抽样分布**。抽样分布能帮助我们看出，从这一总体抽取容量为 40 的样本时，样本比例预期会有多大的变化。

```{index} DataFrame; sample
```

我们再次用 `sample` 从 Airbnb 房源总体中抽取容量为 40 的样本。不过这次我们借助列表推导式（list comprehension）把这一操作重复多次（前面在{numref}`第 %s 章 <clustering>`中也是这样做的）。这里我们把该操作重复 20,000 次，得到 20,000 个容量为 40 的样本。为了清楚地看出数据框中的每一行来自 20,000 个样本中的哪一个，我们还用 `assign` 函数添加了一列 `replicate` 来记录这一信息（这个函数在前面{numref}`第 %s 章 <wrangling>`中已经介绍过）。`concat` 调用把列表推导式返回的 20,000 个数据框合并成一个大的数据框。

```{code-cell} ipython3
samples = pd.concat([
    airbnb.sample(40).assign(replicate=n)
    for n in range(20_000)
])
samples
```

由于 `replicate` 列标明了重复编号或样本编号，我们可以确认，我们似乎确实得到了 20,000 个样本，从样本 0 开始、到样本 19,999 结束。

+++

现在样本已经取好了，我们需要计算每个样本中整套住宅/公寓房源的比例。我们先用 `replicate` 变量对数据分组——把每个样本中的房源归到一起——然后用 `value_counts` 并设置 `normalize=True`，算出每个样本中的比例。下面打印了所得数据框的开头和结尾若干行，说明我们最终得到 20,000 个点估计，每一个样本对应一个。

```{index} DataFrame;groupby, DataFrame;reset_index
```

```{code-cell} ipython3
(
    samples
    .groupby("replicate")
    ["room_type"]
    .value_counts(normalize=True)
)
```

返回的对象是一个 Series（序列）。正如前面学过的，我们可以用 `reset_index` 把它变成数据框。不过这里有一点需要注意：对分组后的 Series 使用 `value_counts` 函数再调用 `reset_index`，会出现两个同名的列，因而报错（在这里，`room_type` 会出现两次）。好在有个简单的解决办法：调用 `reset_index` 时，可以用 `name` 参数指定新列的名称：

```{code-cell} ipython3
(
    samples
    .groupby("replicate")
    ["room_type"]
    .value_counts(normalize=True)
    .reset_index(name="sample_proportion")
)
```

下面我们把所有步骤串起来，并筛选数据框，只保留我们关心的房间类型。

```{code-cell} ipython3
sample_estimates = (
    samples
    .groupby("replicate")
    ["room_type"]
    .value_counts(normalize=True)
    .reset_index(name="sample_proportion")
)

sample_estimates = sample_estimates[sample_estimates["room_type"] == "Entire home/apt"]
sample_estimates
```

现在我们可以用直方图画出样本比例的抽样分布，其中样本的容量为 40（见{numref}`fig:11-example-proportions7`）。请记住：在现实世界中，我们拿不到完整的总体，因此无法抽取许多样本，也无法真正构造或画出抽样分布。我们特意构造了这个例子，让它*确实*能拿到完整总体，从而可以出于学习目的直接把这个抽样分布画出来。

```{code-cell} ipython3
:tags: [remove-output]

sampling_distribution = alt.Chart(sample_estimates).mark_bar().encode(
    x=alt.X("sample_proportion")
        .bin(maxbins=20)
        .title("Sample proportions"),
    y=alt.Y("count()").title("Count"),
)

sampling_distribution
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:11-example-proportions7", sampling_distribution)
```

:::{glue:figure} fig:11-example-proportions7
:name: fig:11-example-proportions7

样本量为 40 时样本比例的抽样分布。
:::

```{code-cell} ipython3
:tags: [remove-cell]

glue("sample_proportion_center", "{:.2f}".format(sample_estimates["sample_proportion"].mean()))
glue("sample_proportion_min", "{:.2f}".format(sample_estimates["sample_proportion"].quantile(0.004)))
glue("sample_proportion_max", "{:.2f}".format(sample_estimates["sample_proportion"].quantile(0.9997)))
```

```{index} 抽样分布; 形状
```

{numref}`fig:11-example-proportions7` 中的抽样分布呈钟形（bell-shaped），大致对称，并且是单峰的。分布的中心在 {glue:text}`sample_proportion_center` 附近，样本比例的取值大致从 {glue:text}`sample_proportion_min` 到 {glue:text}`sample_proportion_max`。事实上，我们还可以计算样本比例的均值。

```{code-cell} ipython3
sample_estimates["sample_proportion"].mean()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("sample_proportion_mean", "{:.3f}".format(sample_estimates["sample_proportion"].mean()))
```

我们注意到，样本比例的中心就在总体比例取值 {glue:text}`sample_proportion_mean` 附近！一般来说，抽样分布的均值应该等于总体比例。这是个好消息，因为这说明样本比例既不会高估也不会低估总体比例。换句话说，如果你像上面那样抽取许多样本，结果并不会倾向于高估或低估总体比例。在真实的数据分析中，你只能拿到自己抽到的单个样本，这就意味着你可以认为样本点估计高于或低于真实总体比例的可能性大致相同。

+++

### 均值的抽样分布

上一节中，我们关心的变量——`room_type`——是*类别型变量*，总体参数是比例。正如本章引言所说，每类变量都有许多总体参数可选。如果我们想推断的是*定量*变量的总体，又该怎么办？例如，一位到加拿大温哥华旅游的旅客可能想估计 Airbnb 房源每晚价格的总体*均值*（或平均数）。知道平均数有助于他们判断某个房源是否定价过高。我们可以用直方图画出每晚价格的总体分布。

```{code-cell} ipython3
:tags: [remove-output]

population_distribution = alt.Chart(airbnb).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()", title="Count"),
)

population_distribution
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:11-example-means2", population_distribution)
```

:::{glue:figure} fig:11-example-means2
:name: fig:11-example-means2

加拿大温哥华全部 Airbnb 房源每晚价格（美元）的总体分布。
:::

+++

```{index} 总体; 分布
```

在{numref}`fig:11-example-means2` 中可以看到，总体分布只有一个峰。它还是偏斜的（skewed），也就是并不对称：大多数房源的每晚价格不到 \$250，但少数房源贵得多，在直方图右侧拖出一条长尾。除了把总体分布可视化，我们还可以计算总体均值，也就是所有 Airbnb 房源每晚价格的平均数。

```{code-cell} ipython3
airbnb["price"].mean()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("population_mean", "{:.2f}".format(airbnb["price"].mean()))
```

```{index} 总体; 参数
```

不列颠哥伦比亚省温哥华市所有 Airbnb 房源的每晚价格平均为 \${glue:text}`population_mean`。由于这个值是用总体数据算出来的，所以它就是我们的总体参数。

```{index} DataFrame; 样本
```

现在假设我们拿不到总体数据（通常都是如此！），却想估计每晚价格的均值。要回答这个问题，可以抽取一个随机样本，具体抽多少房源取决于我们有多少时间和资源。假设我们只能抽
40 个房源。这样的样本会是什么样子？既然我们手头确实有总体数据，不妨利用这一点，用 Python 模拟抽取一个包含 40 个房源的随机样本，仍然使用 `sample`。

```{code-cell} ipython3
one_sample = airbnb.sample(n=40)
```

我们可以画一张直方图，把样本中观测的分布可视化（{numref}`fig:11-example-means-sample-hist`），并计算样本均值。

```{index} altair;mark_bar
```

```{code-cell} ipython3
:tags: [remove-output]

sample_distribution = alt.Chart(one_sample).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()").title("Count"),
)

sample_distribution
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:11-example-means-sample-hist", sample_distribution)
```

:::{glue:figure} fig:11-example-means-sample-hist
:name: fig:11-example-means-sample-hist

40 个 Airbnb 房源样本中每晚价格（美元）的分布。
:::

```{code-cell} ipython3
one_sample["price"].mean()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("estimate_mean", "{:.2f}".format(one_sample["price"].mean()))
glue("diff_perc", "{:.1f}".format(100 * abs(1 - (one_sample["price"].mean() / airbnb["price"].mean()))))
```

容量为 40 的这个样本的平均数是 \${glue:text}`estimate_mean`。这个数就是整个总体均值的点估计。回忆一下，总体均值是
\${glue:text}`population_mean`。可见我们的估计值与总体参数相当接近：均值与总体均值大约相差
{glue:text}`diff_perc`%。请注意，实践中我们通常无法计算估计的准确程度，因为拿不到总体参数；如果拿得到，那也就不必估计了！

```{index} 抽样分布
```

另外，回忆上一节的内容：点估计会有波动；如果再从总体中抽取一个随机样本，估计值就可能改变。那么，上面得到的点估计只是运气好而已吗？在这个例子中，容量为 40 的不同样本之间，估计值的波动有多大？同样，由于我们能拿到总体数据，可以抽取许多样本，画出样本均值的抽样分布，借此感受这种波动。这里我们沿用已经存进 `samples` 变量的 20,000 个容量为 40 的样本。先计算每个重复的样本均值，再画出样本量为 40 时样本均值的抽样分布。

```{code-cell} ipython3
sample_estimates = (
    samples
    .groupby("replicate")
    ["price"]
    .mean()
    .reset_index()
    .rename(columns={"price": "mean_price"})
)
sample_estimates
```

```{code-cell} ipython3
:tags: [remove-output]

sampling_distribution = alt.Chart(sample_estimates).mark_bar().encode(
    x=alt.X("mean_price")
        .bin(maxbins=30)
        .title("Sample mean price per night (dollars)"),
    y=alt.Y("count()").title("Count")
)

sampling_distribution
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:11-example-means4", sampling_distribution)
```

:::{glue:figure} fig:11-example-means4
:name: fig:11-example-means4

样本量为 40 时样本均值的抽样分布。
:::

```{code-cell} ipython3
:tags: [remove-cell]

glue("quantile_1", "{:0.0f}".format(round(sample_estimates["mean_price"].quantile(0.25), -1)))
glue("quantile_3", "{:0.0f}".format(round(sample_estimates["mean_price"].quantile(0.75), -1)))
```

```{index} 抽样分布; 形状
```

在{numref}`fig:11-example-means4` 中，均值的抽样分布呈单峰、钟形。大多数估计值大约介于
\${glue:text}`quantile_1` 与
\${glue:text}`quantile_3` 之间；但也有相当一部分情形落在这个范围之外（也就是说，点估计与总体参数相差较大）。所以，我们只用
{glue:text}`diff_perc`% 的误差就估计出了总体均值，看起来确实相当走运。

```{index} 抽样分布; 与总体分布的比较
```

我们把总体分布、样本分布和抽样分布画在同一张图上，以便比较，见{numref}`fig:11-example-means5`。比较这三个分布可以看到，它们的中心都在同一个价位附近（大约 \$150）。原始总体分布有一条很长的右侧长尾，样本分布的形状与总体分布相似。然而，抽样分布的形状与总体分布、样本分布都不一样。相反，它呈钟形，离散程度比总体分布和样本分布都小。样本均值的波动比单个观测小，因为任何随机样本中都会既有较大的取值、也有较小的取值，这使平均数不至于太过极端。

<!---
```{r 11-example-means4.5}
sample_estimates |>
  summarize(mean_of_sample_means = mean(sample_mean))
```
Notice that the mean of the sample means is \$`r round(mean(sample_estimates$sample_mean),2)`. Recall that the population mean
was \$`r round(mean(airbnb$price),2)`.
-->

```{code-cell} ipython3
:tags: ["remove-cell"]

glue(
    "fig:11-example-means5",
    alt.vconcat(
        population_distribution.mark_bar(clip=True).encode(
            x=alt.X(
                "price",
                bin=alt.Bin(extent=[0, 660], maxbins=40),
                title="Price per night (dollars)",
                #scale=alt.Scale(domainMax=700)
            )
        ).properties(
            title="Population", height=150
        ),
        sample_distribution.encode(
            x=alt.X("price")
                .bin(extent=[0, 660], maxbins=40)
                .title("Price per night (dollars)")
        ).properties(title="Sample (n = 40)").properties(height=150),
        sampling_distribution.encode(
            x=alt.X("mean_price")
                .bin(extent=[0, 660], maxbins=40)
                .title("Price per night (dollars)")
        ).properties(
            title=alt.TitleParams(
                "Sampling distribution of the mean",
                subtitle="For 20,000 samples of size 40"
            )
        ).properties(height=150)
    ).resolve_scale(
        x="shared"
    )
)
```

:::{glue:figure} fig:11-example-means5
:name: fig:11-example-means5

总体分布、样本分布与抽样分布的对比。
:::


+++

样本均值的抽样分布波动相当大——也就是说，我们得到的点估计并不十分可靠——那么，有没有办法改进估计呢？改进点估计的一种办法是抽取*更大*的样本。为了说明这样做的影响，我们分别抽取容量为 20、50、100 和 500 的大量样本，并画出样本均值的抽样分布。我们用一条竖线标出抽样分布的均值。

```{code-cell} ipython3
:tags: ["remove-cell"]

# Plot sampling distributions for multiple sample sizes
base = alt.Chart(
    pd.concat([
        pd.concat([
            airbnb.sample(sample_size).assign(sample_size=sample_size, replicate=replicate)
            for sample_size in [20, 50, 100, 500]
        ])
        for replicate in range(20_000)
    ]).groupby(
        ["sample_size", "replicate"],
        as_index=False
    )["price"].mean(),
    height=150
)

glue(
    "fig:11-example-means7",
    alt.layer(
        base.mark_bar().encode(
            alt.X("price", bin=alt.Bin(maxbins=30)),
            alt.Y("count()")
        ),
        base.mark_rule(color="black", size=1.5, strokeDash=[6]).encode(
            x="mean(price)"
        ),
        base.mark_text(align="left", color="black", size=12, fontWeight="bold", dx=10).transform_aggregate(
            mean_price="mean(price)",
        ).transform_calculate(
            label="'Mean = ' + round(datum.mean_price * 10) / 10"
        ).encode(
            x=alt.X("mean_price:Q", title="Sample mean price per night (dollars)"),
            y=alt.value(10),
            text="label:N"
        )
    ).facet(
        alt.Facet(
            "sample_size:N",
            header=alt.Header(
                title="",
                labelFontWeight="bold",
                labelFontSize=12,
                labelPadding=3,
                labelExpr='"Sample size = " + datum.value'
            )
        ),
        columns=1,
    ).resolve_scale(
        y="independent"
    )
)
```

:::{glue:figure} fig:11-example-means7
:name: fig:11-example-means7

抽样分布的比较，均值用竖线标出。
:::

+++

```{index} 抽样分布; 样本量的影响
```

从{numref}`fig:11-example-means7` 的可视化结果可以看出，关于样本均值可以清楚地看到三点：

1. 样本均值的均值（即在各个样本之间求平均）等于总体均值。换句话说，抽样分布以总体均值为中心。
2. 增大样本量会减小抽样分布的离散程度（也就是变异性）。因此，样本量越大，总体参数的点估计就越可靠。
3. 样本均值的分布大致呈钟形。

```{note}
你可能会注意到，{numref}`fig:11-example-means7` 中 `n = 20` 那一组里，分布并不*完全*呈钟形，还稍稍向右偏斜！你还可能注意到，`n = 50` 以及更大的几组里，这种偏斜似乎消失了。一般来说，无论均值还是比例，抽样分布都只有在*样本量足够大*之后才会变成钟形。“足够大”是多大？很遗憾，这完全取决于具体问题。不过按经验法则，样本量通常至少达到 20 就够了。
```

<!---
```{note}
If random samples of size $n$ are taken from a population, the sample mean
$\bar{x}$ will be approximately Normal with mean $\mu$ and standard deviation
$\frac{\sigma}{\sqrt{n}}$ as long as the sample size $n$ is large enough. $\mu$
is the population mean, $\sigma$ is the population standard deviation,
$\bar{x}$ is the sample mean, and $n$ is the sample size.
If samples are selected from a finite population as we are doing in this
chapter, we should apply a finite population correction. We multiply
$\frac{\sigma}{\sqrt{n}}$ by $\sqrt{\frac{N - n}{N - 1}}$ where $N$ is the
population size and $n$ is the sample size. If our sample size, $n$, is small
relative to the population size, this finite correction factor is less
important.
```
--->

+++

### 小结

1. 点估计是用总体的一个样本算出的单个数值（例如均值或比例）。
2. 估计值的抽样分布，是指从同一总体中抽取所有可能的固定大小样本时，该估计值的分布。
3. 抽样分布的形状通常是单峰钟形，并以总体均值或总体比例为中心。
4. 抽样分布的离散程度与样本量有关。样本量越大，抽样分布的离散程度就越小。

+++

## 自助法

+++

### 概述

*为什么要如此强调抽样分布？*

上一节我们看到，可以用从总体中抽到的一个样本算出总体参数的**点估计**。而且，由于我们构造的例子能拿到总体数据，所以可以评估估计有多准确，甚至能看出不同样本之间估计值的波动有多大。但在真正的数据分析场景中，我们通常*只有一个样本*，拿不到总体本身。因此，无法像上一节那样构造抽样分布。而且正如我们看到的，样本估计值与总体参数可能相差很大。所以，只报告单个样本的点估计也许还不够，我们还需要报告点估计取值的某种*不确定性*。

```{index} 自助法, 置信区间
```

```{index} see: 区间; 置信区间
```

遗憾的是，没有总体的完整数据，就无法构造精确的抽样分布。不过，如果我们能以某种方式*近似*出样本所对应的抽样分布，就可以用这个近似来报告样本点估计有多不确定（正如上面用*精确*抽样分布所做的那样）。实现这一点有若干种方法；本书将使用*自助法*。我们将只使用总体中的一个样本，讨论**区间估计**并构造**置信区间**。置信区间是总体参数的合理取值范围。

关键思路如下。首先，只要样本足够大，它就*看起来像*总体。请注意{numref}`fig:11-example-bootstrapping0` 中从总体抽取的不同大小样本的直方图形状。可以看到，样本足够大时，样本的分布与总体分布很相似。

```{code-cell} ipython3
:tags: [remove-cell]

# plot sample distributions for n = 10, 20, 50, 100, 200 and population distribution
sample_distribution_dict = {}
for sample_n in [10, 20, 50, 100, 200]:
    sample = airbnb.sample(sample_n)
    sample_distribution_dict[f"sample_distribution_{sample_n}"] = (
        alt.Chart(sample, title=f"n = {sample_n}").mark_bar().encode(
            x=alt.X(
                "price",
                bin=alt.Bin(extent=[0, 600], step=20),
                title="Price per night (dollars)",
            ),
            y=alt.Y("count()", title="Count"),
        )
    ).properties(height=150)
# add title and standardize the x axis ticks for population histogram
population_distribution.title = "Population distribution"
population_distribution.encoding["x"]["bin"] = alt.Bin(extent=[0, 600], step=20)

glue(
    "fig:11-example-bootstrapping0",
    (
        (
            sample_distribution_dict["sample_distribution_10"]
            | sample_distribution_dict["sample_distribution_20"]
        )
        & (
            sample_distribution_dict["sample_distribution_50"]
            | sample_distribution_dict["sample_distribution_100"]
        )
        & (
            sample_distribution_dict["sample_distribution_200"]
            | population_distribution.properties(width=350, height=150)
        )
    ),
)
```

:::{glue:figure} fig:11-example-bootstrapping0
:name: fig:11-example-bootstrapping0

从总体抽取的不同大小样本的比较。
:::

+++

```{index} 自助法; 分布
```

上一节中，我们*从总体中*抽取了许多同样大小的样本，以了解样本估计值的变异性。但如果我们的样本足够大、看起来就像总体，我们就可以把样本*当作*总体，转而从它里面抽取更多同样大小的样本（有放回，with replacement）！这个十分巧妙的技巧叫作**自助法**。请注意，从我们唯一观测到的样本中抽取许多样本，得到的并不是真正的抽样分布，而是一个近似，我们称之为**自助分布**。

```{note}
使用自助法时，我们必须*有放回*地抽样。否则，如果我们有一个容量为 $n$ 的样本，再从中*无放回*地抽取一个容量为 $n$ 的样本，那只会把原来的样本原封不动地取回来！
```

本节将介绍如何用 Python 从单个样本创建自助分布。整个过程在{numref}`fig:11-intro-bootstrap-image` 中做了可视化。对于容量为 $n$ 的样本，你需要做以下几步：

+++

1. 从取自总体的原始样本中随机选取一个观测。
2. 记录这个观测的取值。
3. 把这个观测放回样本。
4. 重复第 1 至第 3 步（*有放回*地抽样），直到得到 $n$ 个观测，它们构成一个自助样本。
5. 计算自助样本中这 $n$ 个观测的自助点估计（例如均值、中位数、比例、斜率等）。
6. 重复第 1 至第 5 步很多次，得到点估计的分布（即自助分布）。
7. 计算观测到的点估计附近的合理取值范围。

+++

```{figure} img/inference/intro-bootstrap.jpeg
:name: fig:11-intro-bootstrap-image

自助法流程概览。
```

+++

### 用 Python 实现自助法

我们接着用 Airbnb 的例子，说明如何只靠从总体中抽出的一个样本，构造并使用自助分布。仍然假设我们想估计加拿大温哥华所有 Airbnb 房源每晚价格的总体均值，而手头只有一个样本量为 40 的样本。回想一下，我们的点估计是 \${glue:text}`estimate_mean`。样本中价格的直方图见{numref}`fig:11-bootstrapping1`。

```{code-cell} ipython3
one_sample
```

```{code-cell} ipython3
:tags: ["remove-output"]
one_sample_dist = alt.Chart(one_sample).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()").title("Count"),
)

one_sample_dist
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping1", one_sample_dist)
```

:::{glue:figure} fig:11-bootstrapping1
:name: fig:11-bootstrapping1

样本量为 40 的一个样本中每晚价格（美元）的直方图。
:::

+++

该样本的直方图是偏斜的，有少数几个观测落在右侧较远处。样本均值为 \${glue:text}`estimate_mean`。请记住，在实践中，我们通常只有从总体中抽到的这一个样本。所以这个样本和这个估计值就是我们能使用的全部数据。

```{index} 自助法; 在 Python 中, DataFrame; 样本（自助）
```

现在我们在 Python 中执行上面列出的第 1 至第 5 步，生成一个自助样本，并据此算出点估计。我们继续使用数据框的 `sample` 函数。这里有一点很关键：我们设置 `frac=1`（“fraction”，比例），表示想抽取的条数与数据框的行数同样多（也可以设
`n=40`，但那样就得自己留意数据框里有多少行）。由于做自助法需要有放回抽样，所以要把 `replace` 参数改成 `True`。

```{code-cell} ipython3
:tags: ["remove-output"]

boot1 = one_sample.sample(frac=1, replace=True)
boot1_dist = alt.Chart(boot1).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()", title="Count"),
)

boot1_dist
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping3", boot1_dist)
```

:::{glue:figure} fig:11-bootstrapping3
:name: fig:11-bootstrapping3

单个自助样本的直方图（译注：原文图注为“Bootstrap distribution”，但本图实际画出的是单个自助样本，并非自助分布）。
:::

```{code-cell} ipython3
boot1["price"].mean()
```

从{numref}`fig:11-bootstrapping3` 中可以看到，自助样本的直方图与原始样本的直方图形状相似。虽然两个分布的形状相近，但并不完全相同。你还会发现，原始样本的均值与自助样本的均值不一样。这是怎么发生的呢？请记住，我们是从原始样本中有放回地抽样，所以不会再次抽到完全相同的样本取值。我们是在*假装*这一个样本与总体很接近，并通过从原始样本中再抽一个样本，来模拟从总体中再抽一个样本。

现在我们用原始样本（`one_sample`）生成 20,000 个自助样本，并计算每个重复的均值。要记住，这样做的前提是 `one_sample` *看起来像*原始总体；但既然我们拿不到总体本身，这通常已经是我们能做的最好的选择了。请注意，这里把列表推导式拆成了多行，以便阅读。

```{code-cell} ipython3
boot20000 = pd.concat([
    one_sample.sample(frac=1, replace=True).assign(replicate=n)
    for n in range(20_000)
])
boot20000
```

我们来看看自助样本前六次重复的直方图。

```{code-cell} ipython3
:tags: ["remove-output"]

six_bootstrap_samples = boot20000.query("replicate < 6")
six_bootstrap_fig = alt.Chart(six_bootstrap_samples, height=150).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=20)
        .title("Price per night (dollars)"),
    y=alt.Y("count()").title("Count")
).facet(
    "replicate:N",  # Recall that `:N` converts the variable to a categorical type
    columns=2
)
six_bootstrap_fig
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping-six-bootstrap-samples", six_bootstrap_fig)
```

:::{glue:figure} fig:11-bootstrapping-six-bootstrap-samples
:name: fig:11-bootstrapping-six-bootstrap-samples

自助样本前六次重复的直方图。
:::

+++

从{numref}`fig:11-bootstrapping-six-bootstrap-samples` 中可以看到，各个自助样本的分布有何不同。如果分别计算这六个样本的样本均值，会发现它们彼此也不相同。要计算每个样本的均值，我们先按“replicate”分组，这一列记录的是样本/重复编号。然后计算
`price` 列的均值，并把它重命名为 `mean_price`，让列名更有描述性。最后用 `reset_index`
把 `replicate` 的取值变回数据框中的一列。

```{code-cell} ipython3
(
    six_bootstrap_samples
    .groupby("replicate")
    ["price"]
    .mean()
    .reset_index()
    .rename(columns={"price": "mean_price"})
)
```

自助样本之间的分布和均值之所以不同，是因为我们采用了*有放回*抽样。如果改成*无放回*抽样，那么每次得到的样本取值都会完全一样。

接下来，我们为这 20,000 个自助样本分别计算均值的点估计，并由此得到这些点估计的自助分布。自助分布（{numref}`fig:11-bootstrapping5`）可以提示我们，如果取多个样本，点估计会有怎样的表现。

```{index} DataFrame;reset_index, DataFrame;rename, DataFrame;groupby, Series;mean
```

```{code-cell} ipython3
boot20000_means = (
    boot20000
    .groupby("replicate")
    ["price"]
    .mean()
    .reset_index()
    .rename(columns={"price": "mean_price"})
)

boot20000_means
```

```{code-cell} ipython3
:tags: ["remove-output"]

boot_est_dist = alt.Chart(boot20000_means).mark_bar().encode(
    x=alt.X("mean_price")
        .bin(maxbins=20)
        .title("Sample mean price per night (dollars)"),
    y=alt.Y("count()").title("Count"),
)

boot_est_dist
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping5", boot_est_dist)
```

:::{glue:figure} fig:11-bootstrapping5
:name: fig:11-bootstrapping5

自助样本均值的分布。
:::

+++

我们来比较自助分布——由容量为 40 的原始样本反复抽样构造而来——与真实的抽样分布——相当于从总体中反复抽样。

```{code-cell} ipython3
:tags: [remove-cell]

sampling_distribution.encoding.x["bin"]["extent"] = (90, 250)
bootstr6fig = alt.vconcat(
    alt.layer(
        sampling_distribution,
        alt.Chart(sample_estimates).mark_rule(color="black", size=1.5, strokeDash=[6]).encode(x="mean(mean_price)"),
        alt.Chart(sample_estimates).mark_text(color="black", size=12, align="left", dx=16, fontWeight="bold").encode(
            x="mean(mean_price)",
            y=alt.value(7),
            text=alt.value(f"Mean = {sampling_distribution['data']['mean_price'].mean().round(1)}")
        )
    ).properties(title="Sampling distribution", height=150),
    alt.layer(
        boot_est_dist,
        alt.Chart(boot20000_means).mark_rule(color="black", size=1.5, strokeDash=[6]).encode(x="mean(mean_price)"),
        alt.Chart(boot20000_means).mark_text(color="black", size=12, align="left", dx=18, fontWeight="bold").encode(
            x="mean(mean_price)",
            y=alt.value(7),
            text=alt.value(f"Mean = {boot_est_dist['data']['mean_price'].mean().round(1)}")
        )
    ).properties(title="Bootstrap distribution", height=150)
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping6", bootstr6fig)
```

:::{glue:figure} fig:11-bootstrapping6
:name: fig:11-bootstrapping6

自助样本均值的分布与抽样分布的比较。
:::



```{code-cell} ipython3
:tags: [remove-cell]

glue("one_sample_mean", "{:.2f}".format(one_sample["price"].mean()))
```

```{index} 抽样分布; 与自助分布的比较
```

从{numref}`fig:11-bootstrapping6` 中我们可以得到两个要点。第一，真实抽样分布与自助分布的形状和离散程度相似；自助分布能帮助我们体会点估计的变异性。第二个要点是：这两个分布的均值略有不同。抽样分布的中心是总体均值
\${glue:text}`population_mean`。而自助分布的中心是原始样本中每晚价格的平均值
\${glue:text}`one_sample_mean`。由于我们不断从原始样本中重抽样，可以看到自助分布的中心落在原始样本的均值上（样本均值的抽样分布则不同，它的中心是总体参数的取值）。

{numref}`fig:11-bootstrapping7` 总结了自助法的流程。这里的思路是：当我们只有一个样本时，可以用自助样本均值的分布来近似样本均值的抽样分布。既然自助分布能相当好地近似抽样分布的离散程度，我们就可以借助自助分布的离散程度，结合点估计给出总体参数的合理取值范围！

```{figure} img/inference/11-bootstrapping7-1.png
:name: fig:11-bootstrapping7

自助法流程总结。
```

+++

### 用自助法计算合理取值范围

```{index} 置信区间
```

现在我们已经构造出自助分布，接下来用它来算出一个近似的 95\% 百分位数自助置信区间（percentile bootstrap confidence interval）。**置信区间**是总体参数的合理取值范围。我们要找出覆盖自助分布中间 95\% 的那一段取值，这样就得到了 95\% 置信区间。你也许会问：“95\% 置信”是什么意思？如果我们抽取 100 个随机样本，算出 100 个 95\% 置信区间，那么其中大约 95\% 的区间会覆盖总体参数的取值。请注意，95\% 这个数并没有什么特别之处，我们也可以用其他水平，比如 90\% 或 99\%。置信水平与精度之间存在权衡：置信水平越高，区间越宽；置信水平越低，区间越窄。因此，选择哪个水平取决于我们愿意承担多大的出错概率，而这又取决于出错对我们的应用会有什么后果。一般来说，我们选定的置信水平，既要让自己对不确定性感到安心，又不能严格到让区间失去用处。例如，如果我们的决策会影响人的生命，一旦出错后果致命，那我们可能希望很有把握，于是选择更高的置信水平。

要计算 95\% 百分位数自助置信区间，我们按下面的步骤来做：

1. 把自助分布中的观测按从小到大的顺序排列。
2. 找出这样的取值：有 2.5\% 的观测落在它以下（即第 2.5 百分位数）。把这个取值作为区间的下限。
3. 找出这样的取值：有 97.5\% 的观测落在它以下（即第 97.5 百分位数）。把这个取值作为区间的上限。

要在 Python 中完成这些步骤，我们可以用 DataFrame 的 `quantile` 函数。分位数用比例而不是百分数表示，所以第 2.5 百分位数和第 97.5 百分位数分别对应 0.025 和 0.975
分位数。

```{index} DataFrame; [], DataFrame;quantile
```

```{index} 百分位数
```

```{code-cell} ipython3
ci_bounds = boot20000_means["mean_price"].quantile([0.025, 0.975])
ci_bounds
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("ci_lower", "{:.2f}".format(ci_bounds[0.025]))
glue("ci_upper", "{:.2f}".format(ci_bounds[0.975]))
```

我们的区间，从 \${glue:text}`ci_lower` 到 \${glue:text}`ci_upper`，覆盖了自助分布中位于中间 95\% 的样本均值价格。我们可以在{numref}`fig:11-bootstrapping9` 中把这个区间画在分布上。

```{code-cell} ipython3
:tags: [remove-cell]
# Create the annotation for for the 2.5th percentile
rule_025 = alt.Chart().mark_rule(color="black", size=1.5, strokeDash=[6]).encode(
    x=alt.datum(ci_bounds[0.025])
).properties(
    width=500
)
text_025 = rule_025.mark_text(
    color="black",
    size=12,
    fontWeight="bold",
    dy=-160
).encode(
    text=alt.datum(f"2.5th percentile ({ci_bounds[0.025].round(1)})")
)

# Create the annotation for for the 97.5th percentile
text_975 = text_025.encode(
    x=alt.datum(ci_bounds[0.975]),
    text=alt.datum(f"97.5th percentile ({ci_bounds[0.975].round(1)})")
)
rule_975 = rule_025.encode(x=alt.datum(ci_bounds[0.975]))

# Layer the annotations on top of the distribution plot
bootstr9fig = boot_est_dist + rule_025 + text_025 + rule_975 + text_975
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping9", bootstr9fig)
```

:::{glue:figure} fig:11-bootstrapping9
:name: fig:11-bootstrapping9

带百分位数上下限的自助样本均值分布。
:::



+++

要完成对总体参数的估计，我们需要报告点估计以及置信区间的下限和上限。这里 40 个
Airbnb 房源每晚价格的样本均值为 \${glue:text}`one_sample_mean`，而我们有 95\% 的“把握”认为，温哥华所有 Airbnb 房源每晚价格的真实总体均值介于
\${glue:text}`ci_lower` 和 \${glue:text}`ci_upper` 之间。可以看到，我们的区间确实覆盖了真实的总体均值 \${glue:text}`population_mean`！不过在实践中，我们并不知道自己的区间有没有覆盖总体参数，因为我们通常只有一个样本，而不是整个总体。只有一个样本时，这已经是我们能做到的最好结果了！

本章只是统计推断之旅的开端。我们可以把这里学到的概念推广出去，做远远不止于报告点估计和置信区间的事情，比如检验总体之间是否存在真实差异、检验变量之间是否有关联，等等。我们才刚刚触及统计推断的皮毛；不过，本章介绍的内容会成为你今后学习更高级统计方法的基础！

+++

## 习题

本章内容的配套练习题见[练习册仓库](https://worksheets.python.datasciencebook.ca)中“Statistical inference（统计推断）”那两行。点击“查看练习册（view worksheet）”即可预览本章每份练习册的非交互版本。若要交互式地做这些习题，请按照练习册仓库中的说明下载全部练习册，并按{numref}`第 %s 章 <move-to-your-own-machine>`中给出的计算机环境配置说明操作。这样才能确保练习册提供的自动反馈与指导按预期正常工作。

+++

## 拓展资源

- 《OpenIntro Statistics》 {cite:p}`openintro` 的第 4 至第 7 章在进一步学习统计推断时，是一个不错的进阶选择。虽然它无疑仍是一部入门教材，但这里的内容会更偏数学一些。视你的基础而定，你也许反而应该先读第 1 至第 3 章，那里会讲到概率论的一些基本概念。概率论看似偏离主题，其实它正是*统计学的语言*；如果对概率有扎实的掌握，更高阶的统计学对你来说就会水到渠成！

+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
