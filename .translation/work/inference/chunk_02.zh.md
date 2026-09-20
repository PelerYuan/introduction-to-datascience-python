+++

```{index} 总体; 分布
```

在 {numref}`fig:11-example-means2` 中可以看到，总体分布只有一个峰。它还偏斜（skewed），
也就是并不对称：大多数房源的每晚价格不到 \$250，但少数房源贵得多，
在直方图右侧拖出一条长尾。
除了把总体分布可视化，我们还可以计算总体均值，
也就是所有 Airbnb 房源每晚价格的平均数。

```{code-cell} ipython3
airbnb["price"].mean()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("population_mean", "{:.2f}".format(airbnb["price"].mean()))
```

```{index} 总体; 参数
```

不列颠哥伦比亚省温哥华市所有 Airbnb 房源的每晚价格平均为 \${glue:text}`population_mean`。
由于这个值是用总体数据算出来的，所以它就是我们的总体参数。

```{index} DataFrame; 样本
```

现在假设我们拿不到总体数据（通常都是如此！），却想估计每晚价格的均值。要回答这个
问题，可以抽取一个随机样本，具体抽多少房源取决于我们有多少时间和资源。假设我们只能抽
40 个房源。这样的样本会是什么样子？既然我们手头确实有总体数据，
不妨利用这一点，用 Python 模拟抽取一个包含 40 个房源的随机样本，仍然使用 `sample`。

```{code-cell} ipython3
one_sample = airbnb.sample(n=40)
```

我们可以画一张直方图，把样本中观测的分布可视化（{numref}`fig:11-example-means-sample-hist`），
并计算样本均值。

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

大小为 40 的这个样本，其平均数是 \${glue:text}`estimate_mean`。这个数就是整个总体均值
的点估计。回忆一下，总体均值是
\${glue:text}`population_mean`。可见我们的估计值与
总体参数相当接近：与总体均值大约相差
{glue:text}`diff_perc`%。请注意，实践中我们通常无法计算估计的准确程度，
因为拿不到总体参数；如果拿得到，那也就不必估计了！

```{index} 抽样分布
```

另外，回忆上一节的内容：点估计会有波动；如果再从总体中抽取一个随机样本，估计值就可能
改变。那么，上面得到的点估计只是运气好而已吗？在这个例子中，大小为 40 的不同样本之间，
估计值的波动有多大？
同样，由于我们能拿到总体数据，可以抽取许多样本，画出样本均值的抽样分布，借此感受这种波动。
这里我们沿用已经存进 `samples` 变量的 20,000 个大小为 40 的样本。
先计算每个重复的样本均值，
再画出大小为 40 的样本的样本均值抽样分布。

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

在 {numref}`fig:11-example-means4` 中，均值的抽样分布呈单峰、钟形。大多数估计值大约介于
\${glue:text}`quantile_1` 与
\${glue:text}`quantile_3` 之间；但也有相当
一部分情形落在这个范围之外（也就是说，点估计与总体参数
相差较大）。所以，我们只用
{glue:text}`diff_perc`% 的误差就估计出了总体均值，
看起来确实相当走运。

```{index} 抽样分布; 与总体分布的比较
```

我们把总体分布、样本分布和
抽样分布画在同一张图上，以便比较，见 {numref}`fig:11-example-means5`。比较这三个分布可以看到，它们的中心
都在同一个价位附近（大约 \$150）。原始
总体分布有一条很长的右侧长尾，样本分布的形状
与总体分布相似。然而，抽样
分布的形状与总体分布、样本分布都不一样。相反，
它呈钟形，离散程度比总体分布和样本
分布都小。样本均值的波动比单个观测小，
因为任何随机样本中都会既有较大的取值、也有较小的取值，
这使平均数不至于太过极端。

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

样本均值的抽样分布波动相当大——也就是说，我们得到的点估计并不十分
可靠——那么，有没有办法改进估计呢？改进
点估计的一种办法是抽取*更大*的样本。为了说明这样做
的影响，我们分别抽取大小为 20、50、100 和 500 的大量样本，并画出
样本均值的抽样分布。我们用一条竖线标出抽样
分布的均值。

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

从 {numref}`fig:11-example-means7` 的可视化结果可以看出，关于样本均值可以清楚地看到三点：

1. 样本均值的均值（即在各个
   样本之间求平均）等于总体均值。换句话说，抽样
   分布以总体均值为中心。
2. 增大样本
   量会减小抽样分布的离散程度（也就是变异性）。因此，样本量越大，总体参数的
   点估计就越可靠。
3. 样本均值的分布大致呈钟形。

```{note}
你可能会注意到，{numref}`fig:11-example-means7` 中 `n = 20` 那一组里，
分布并不*完全*呈钟形，还稍稍向右偏斜！
你还可能注意到，`n = 50` 以及更大的几组里，这种偏斜似乎消失了。
一般来说，无论均值还是比例，抽样分布都只有在
*样本量足够大*之后才会变成钟形。
“足够大”是多大？很遗憾，这完全取决于具体问题。不过
按经验法则，样本量通常至少达到 20 就够了。
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

上一节我们看到，可以用总体中的一个观测样本算出总体参数的**点估计**。而且，
由于我们构造的例子能拿到总体数据，所以可以评估估计有多准确，甚至能看出
不同样本之间估计值的波动有多大。但在真正的
数据分析场景中，我们通常*只有一个样本*，
拿不到总体本身。因此，无法像上一节
那样构造抽样分布。而且正如我们看到的，
样本估计值与总体参数可能相差很大。
所以，只报告单个样本的点估计也许还不够，
我们还需要报告点估计取值的某种*不确定性*。

```{index} 自助法, 置信区间
```

```{index} see: 区间; 置信区间
```

遗憾的是，没有总体的完整数据，就无法构造精确的抽样分布。不过，如果我们能以某种方式
*近似*出样本所对应的抽样分布，就可以
用这个近似来报告样本
点估计有多不确定（正如上面
用*精确*抽样分布所做的那样）。实现这一点有若干种方法；本书
将使用*自助法*（bootstrap）。我们将只使用总体中的一个样本，讨论**区间估计**并
构造
**置信区间**。
置信区间是总体参数的合理取值范围。

关键思路如下。首先，只要样本足够大，它就*看起来像*
总体。请注意 {numref}`fig:11-example-bootstrapping0` 中从总体抽取的
不同大小样本的直方图形状。可以看到，
样本足够大时，样本的分布与总体分布很相似。

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

上一节中，我们*从总体中*
抽取了许多同样大小的样本，以了解样本估计值的变异性。但如果我们的
样本足够大、看起来就像总体，我们就可以把样本
*当作*总体，转而从它里面抽取更多同样大小的
样本（有放回，with replacement）！这个十分巧妙的技巧
叫作**自助法**。请注意，从我们唯一观测到的
样本中抽取许多样本，得到的并不是真正的抽样分布，而是一个
近似，我们称之为**自助分布**。

```{note}
使用自助法时，我们必须*有放回*地抽样。
否则，如果我们有一个大小为 $n$ 的样本，再从中
*无放回*地抽取一个大小为 $n$ 的样本，那只会把原来的样本原封不动地取回来！
```

本节将介绍如何用 Python 从单个
样本创建自助分布。整个过程在 {numref}`fig:11-intro-bootstrap-image` 中做了可视化。
对于大小为 $n$ 的样本，你需要做以下几步：

