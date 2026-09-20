
(inference)=
# 统计推断

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
```

## 概述

在实际的数据分析中，一项典型任务是根据从总体中抽取的观测数据，对感兴趣的总体某个未知方面作出结论；我们通常拿不到*整个*总体的数据。
数据集中的各种汇总、模式、趋势或关系如何推广到更大的总体，这类数据分析问题称为*推断性问题*（inferential question）。
本章先介绍从总体中抽样的基本思想，再介绍统计推断中的两种常用技术：*点估计*与*区间估计*。

## 本章学习目标

学完本章后，你将能够：

- 描述可以用统计推断回答的真实问题示例。
- 定义常见的总体参数（例如均值、比例、标准差）——这些参数通常用抽样数据来估计——并学会根据样本估计这些参数。
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

我们常常需要了解：从一部分数据中观测到的量，与更大总体中同样的量之间有什么关系。
例如，假设一家零售商正在考虑销售 iPhone 配件，他们想估计这个市场可能有多大。
此外，他们还想制定策略，思考如何把产品推销到北美的高校校园。
这位零售商可能会提出下面这个问题：

*北美所有本科生中拥有 iPhone 的比例是多少？*

```{index} 总体, 总体; 参数
```

在上面这个问题中，我们想对北美*所有*本科生作出结论；这些学生的全体就称为**总体**。
一般来说，总体就是我们想要研究的全部个体或个案。
此外，上面这个问题要计算的是一个基于整个总体的量——拥有 iPhone 的比例。
这个比例称为**总体参数**。一般来说，总体参数是整个总体的一个数值特征。
要算出上例中的这个数值，我们得逐一询问北美的每一位本科生是否拥有 iPhone。
在实践中，直接计算总体参数往往既费时又费钱，有时甚至无法做到。

```{index} 样本, 样本; 估计, 推断
```

```{index} see: 统计推断; 推断
```

更实际的做法是针对**样本**做测量，也就是从总体中抽取的一部分个体。
然后我们可以计算一个**样本估计值**——样本的某个数值特征——用它来估计总体参数。
例如，假设我们在北美随机抽取十名本科生（即样本），算出其中拥有 iPhone 的学生所占的比例（即样本估计值）。
这时，我们也许会觉得这个比例可以合理地估计整个总体中拥有 iPhone 的学生比例。
{numref}`fig:11-population-vs-sample` 展示了这一过程。
一般来说，利用样本对抽取该样本的更大总体作出结论，这一过程称为**统计推断**。

+++

```{figure} img/inference/population_vs_sample.png
:name: fig:11-population-vs-sample

用更大总体中的样本得到总体参数点估计的过程。在本例中，一个容量为 10 的样本里有 6 人拥有 iPhone，由此算出的 iPhone 拥有者总体比例估计值为 60%。
这张示例图中实际的总体比例是 53.8%。
```

+++

请注意，比例并不是我们可能关心的*唯一*一种总体参数。例如，假设一名在加拿大不列颠哥伦比亚大学读书的本科生想租一套公寓。这名学生需要制定预算，所以想了解不列颠哥伦比亚省温哥华市单间公寓的租金情况。这名学生可能会提出下面这个问题：

*加拿大温哥华的单间公寓平均月租金是多少？*

在这个例子里，总体是温哥华所有出租的单间公寓，总体参数是*平均月租金*。这里我们用平均数作为集中趋势的度量，来描述单间公寓租金的“典型取值”。
但即便只在这一个例子里，我们也可能关心许多其他总体参数。比如，我们知道温哥华的每套单间公寓月租金并不相同。
这名学生可能想了解月租金的波动有多大，希望找到一个衡量租金离散程度（或变异性）的指标，例如标准差。
又或者，这名学生可能关心月租金超过 \$1000 的单间公寓所占的比例。
我们想回答的问题会帮助我们确定要估计的参数。如果我们有办法观测到温哥华所有出租的单间公寓，就能精确算出上面每一个数；因此，这些都是总体参数。
在实践中你会遇到许多种观测和总体参数，但本章只关注两类情形：

1. 用分类观测估计某个类别的比例
2. 用定量观测估计平均数（或均值）

+++

## 抽样分布

### 比例的抽样分布

```{index} Airbnb
```

我们来看一个例子，用的是 [Inside Airbnb](http://insideairbnb.com/) 的数据 {cite:p}`insideairbnb`。Airbnb 是一个在线平台，可以预订度假短租和住宿场所。
这份数据集包含加拿大温哥华 2020 年 9 月的房源信息。我们的数据包括 ID 编号、街区、房间类型、房源可容纳的人数、浴室数、卧室数、床位数以及每晚价格。

```{code-cell} ipython3
import pandas as pd

airbnb = pd.read_csv("data/listings.csv")
airbnb
```

假设温哥华市政府想了解 Airbnb 租赁信息，以便规划市政条例；他们想知道有多少 Airbnb 房源被列为整套住宅和公寓（而不是私人房间或共享房间）。
因此，他们可能想估计所有 Airbnb 房源中房间类型列为“整套住宅或公寓”的真实比例。
当然，我们通常拿不到真实的总体，但这里不妨（出于学习目的）设想这份数据集就代表了加拿大温哥华全部 Airbnb 出租房源的总体。
我们可以像前面几章那样，用 `value_counts` 函数配合 `normalize` 参数，求出每种房间类型的房源比例。

```{index} DataFrame; [], DataFrame; value_counts
```

```{code-cell} ipython3
airbnb["room_type"].value_counts(normalize=True)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("population_proportion", "{:.3f}".format(airbnb["room_type"].value_counts(normalize=True)["Entire home/apt"]))
```

可以看到，数据集中 `Entire home/apt` 房源的比例是 {glue:text}`population_proportion`。
这个值 {glue:text}`population_proportion` 就是总体参数。请记住，在真实的数据分析问题中，这个参数取值通常是未知的，因为一般无法对整个总体做测量。

```{index} DataFrame; sample, 种子;numpy.random.seed
```

也许我们可以用一小部分数据来近似它！为了探究这个想法，我们来随机抽取 40 个房源（*即*从总体中抽取容量为 40 的随机样本），并计算这个样本的比例。
我们将用 `DataFrame` 对象的 `sample` 方法抽取样本。`sample` 的参数 `n` 指定要抽取的样本量。
由于这里开始用到随机性，我们还会用 numpy 设置随机种子，让结果可以复现。

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

可以看到，这个随机样本中整套住宅/公寓房源的比例是 {glue:text}`sample_1_proportion`。哇——这和真实的总体取值很接近！
但别忘了，这个比例是用容量为 40 的随机样本算出来的。由此产生两个结果。
第一，这个值只是一个*估计值*，也就是我们利用这个样本对总体参数作出的最佳猜测。既然这里估计的只是单个数值，我们通常称它为**点估计**。
第二，由于样本是随机抽取的，如果我们再抽取*另一个*容量为 40 的随机样本并计算它的比例，答案就不会相同：

```{code-cell} ipython3
airbnb.sample(n=40)["room_type"].value_counts(normalize=True)
```

果然如此！这一次我们得到的估计值不同了。这说明我们的点估计可能并不可靠。
的确，由于**抽样变异性**的存在，估计值会随样本不同而变化。那么，我们应该预期随机样本的估计值有多大变化？
换句话说，仅凭单个样本得到的点估计，到底有多可信？

```{index} 抽样分布
```

为了弄清楚这一点，我们将从房源总体中模拟抽取许多个样本（远远多于两个），每个样本的容量都是 40，并计算每个样本中整套住宅/公寓房源的比例。
这次模拟会产生许多样本比例，我们可以用直方图把它们画出来。
从一个总体中抽取给定容量（我们通常记作 $n$）的全部可能样本，其估计值的分布称为**抽样分布**。
抽样分布能帮助我们看出，从这一总体抽取容量为 40 的样本时，样本比例预期会有多大的变化。

```{index} DataFrame; sample
```

我们再次用 `sample` 从 Airbnb 房源总体中抽取容量为 40 的样本。不过这次我们借助列表推导式（list comprehension）把这一操作重复多次（前面在 {numref}`第 %s 章 <clustering>` 中也是这样做的）。
这里我们把该操作重复 20,000 次，得到 20,000 个容量为 40 的样本。
为了清楚地看出数据框中的每一行来自 20,000 个样本中的哪一个，我们还用 `assign` 函数添加了一列 `replicate` 来记录这一信息（这个函数在前面 {numref}`第 %s 章 <wrangling>` 中已经介绍过）。
`concat` 调用把列表推导式返回的 20,000 个数据框合并成一个大的数据框。

```{code-cell} ipython3
samples = pd.concat([
    airbnb.sample(40).assign(replicate=n)
    for n in range(20_000)
])
samples
```

由于 `replicate` 列标明了重复编号或样本编号，我们可以确认，样本似乎确实从样本 0 开始、到样本 19,999 结束，共有 20,0000 个。

+++

现在样本已经取好了，我们需要计算每个样本中整套住宅/公寓房源的比例。
我们先用 `replicate` 变量对数据分组——把每个样本中的房源归到一起——然后用 `value_counts` 并设置 `normalize=True`，算出每个样本中的比例。
下面打印了所得数据框的开头和结尾若干行，说明我们最终得到 20,000 个点估计，每一个样本对应一个。

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

返回的对象是一个序列（series）。正如前面学过的，我们可以用 `reset_index` 把它变成数据框。
不过这里有一点需要注意：对分组后的序列使用 `value_counts` 函数再调用 `reset_index`，会出现两个同名的列，因而报错（在这里，`room_type` 会出现两次）。
好在有个简单的解决办法：调用 `reset_index` 时，可以用 `name` 参数指定新列的名称：

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

现在我们可以用直方图画出样本比例的抽样分布，其中样本的容量为 40（见 {numref}`fig:11-example-proportions7`）。
请记住：在现实世界中，我们拿不到完整的总体，因此无法抽取许多样本，也无法真正构造或画出抽样分布。
我们特意构造了这个例子，让它*确实*能拿到完整总体，从而可以出于学习目的直接把这个抽样分布画出来。

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

{numref}`fig:11-example-proportions7` 中的抽样分布呈钟形（bell-shaped），大致对称，并且是单峰的。
分布的中心在 {glue:text}`sample_proportion_center` 附近，样本比例的取值大致从 {glue:text}`sample_proportion_min` 到 {glue:text}`sample_proportion_max`。
事实上，我们还可以计算样本比例的均值。

```{code-cell} ipython3
sample_estimates["sample_proportion"].mean()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("sample_proportion_mean", "{:.3f}".format(sample_estimates["sample_proportion"].mean()))
```

我们注意到，样本比例的中心就在总体比例取值 {glue:text}`sample_proportion_mean` 附近！
一般来说，抽样分布的均值应该等于总体比例。
这是个好消息，因为这说明样本比例既不会高估也不会低估总体比例。
换句话说，如果你像上面那样抽取许多样本，结果并不会倾向于高估或低估总体比例。
在真实的数据分析中，你只能拿到自己抽到的单个样本，这就意味着你可以认为样本点估计高于或低于真实总体比例的可能性大致相同。

+++

### 均值的抽样分布

上一节中，我们关心的变量——`room_type`——是*分类*的，总体参数是比例。
正如本章引言所说，每类变量都有许多总体参数可选。如果我们想推断的是*定量*变量的总体，又该怎么办？
例如，一位到加拿大温哥华旅游的旅客可能想估计 Airbnb 房源每晚价格的总体*均值*（或平均数）。知道平均数有助于他们判断某个房源是否定价过高。
我们可以用直方图画出每晚价格的总体分布。

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

