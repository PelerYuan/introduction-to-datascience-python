## 用 Python 实现 k 均值聚类

```{index} K-means, scikit-learn; KMeans
```

```{index} see: KMeans; scikit-learn
```

在 Python 中做 k 均值聚类时，所用的工作流
与前面分类、回归两章类似。
回到原始的（未标准化的）`penguins` 数据，
回忆一下：k 均值聚类用直线距离判断哪些点彼此相似。
因此，数据中各个变量的*标度*会影响
数据点最终被分到哪个簇。
标度大的变量在决定簇归属时，
作用比标度小的变量大得多。
为解决这个问题，我们通常在聚类前对数据做标准化，
这样可以保证每个变量的均值为 0、标准差为 1。
`scikit-learn` 中的 `StandardScaler` 函数就能完成这件事。

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

为了表明做的是 k 均值聚类，我们要创建一个 `KMeans`
模型对象。它至少接受一个参数：
簇数 `n_clusters`，这里设为 3。

```{index} KMeans;n_clusters
```

```{code-cell} ipython3
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
kmeans
```

```{index} scikit-learn;make_pipeline, scikit-learn;Pipeline, scikit-learn;fit
```

要真正运行 k 均值聚类，我们把预处理器和模型对象组合进
`Pipeline`，再调用 `fit` 函数。请注意，k-means
算法对簇归属做随机初始化，不过本章开头已经设定了随机种子，
所以这次聚类的结果可以复现。

```{code-cell} ipython3
from sklearn.pipeline import make_pipeline

penguin_clust = make_pipeline(preprocessor, kmeans)
penguin_clust.fit(penguins)
penguin_clust
```

```{index} KMeans; labels_, KMeans; inertia_
```

拟合好的 `KMeans` 对象——它是流水线中的第二项，
可以用 `penguin_clust[1]` 取到——
包含很多信息，可用来可视化各个簇、
选取 K 以及评估总 WSSD。
我们先从用彩色散点图展示各个簇开始！
为此，需要先把簇归属添加到原始的 `penguins` 数据框中。
这些信息可以从聚类对象的 `labels_` 属性中取出
（“labels”是聚类中“assignments”的常见替代说法），
再添加到数据框中。

```{code-cell} ipython3
penguins["cluster"] = penguin_clust[1].labels_
penguins
```

现在 `penguins` 数据框中已经包含了簇归属，
我们可以像 {numref}`cluster_plot` 那样把它们可视化出来。
请注意，这里画的是*未标准化*的数据；
如果出于某种原因想可视化*标准化*的数据，
就得先直接在 `StandardScaler` 预处理器上调用 `fit` 和 `transform` 函数把它取出来。
和 {numref}`第 %s 章 <viz>` 一样，
加上 `:N` 后缀能让 `altair`
把 `cluster` 变量当作名义型／分类变量，
从而在可视化时使用离散的颜色映射。

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

按 k-means 返回的簇归属给数据着色。
:::

```{index} WSSD; 总计, KMeans; inertia_
```

```{index} see: WSSD; KMeans
```

前面提到过，我们还需要
通过观察总 WSSD 随簇数变化的图形，
找到“肘部”出现的位置，从而选定 K。
总 WSSD 存放在聚类对象的 `.inertia_` 属性里
（“inertia”是 `scikit-learn` 用来表示 WSSD 的术语）。

```{code-cell} ipython3
penguin_clust[1].inertia_
```

要计算各种 K 取值下的总 WSSD，我们需要
创建一个数据框，其中包含不同的 `k` 取值，
以及用每个 k 值运行 k 均值聚类得到的 WSSD。
为了创建这个数据框，
我们要用到 Python 中的“列表推导式（list comprehension）”：
把同一个操作重复执行多次，
并把结果放进列表返回。
下面这个列表推导式的例子把 0 到 2 这几个数存进列表：

```{index} 列表推导式
```

```{code-cell} ipython3
[n for n in range(3)]
```

列表推导式里的变量 `n` 可以随意改名，
也可以在其中执行任何想做的运算。
例如，
可以把 1 到 4 这些数都平方后存进列表：

```{code-cell} ipython3
[number**2 for number in range(1, 5)]
```

接下来，我们用这个办法计算 K 取 1 到 9 时的 WSSD。
对每个 K 值，
都新建一个 `KMeans` 模型，
再和前面创建的预处理器一起
包进 `scikit-learn` 流水线。
我们把算出的 WSSD 存进列表，再用它创建一个数据框，
同时包含各 K 取值和对应的 WSSD。

```{note}
我们创建变量 `ks` 来保存待考察的 k 取值范围，
这样一旦决定改用别的 k 值，
只需要在一处修改。
否则，很容易忘记同步更新
列表推导式或数据框赋值中的这一处。
如果同一个取值要用多次，
把它赋给变量名后复用最稳妥。
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

现在数据框中已经有了 `wssd` 和 `k` 两列，我们可以画一张折线图
（{numref}`elbow_plot`），寻找其中的“肘部”，据此确定该用哪个 K 值。

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

看起来这组数据选三个簇最合适，
因为折线的“肘部”在这里最明显。
从图中还能看出，
WSSD 一直在下降，
这与增加簇数时的预期一致。
不过，
肘部图上也可能出现
某一步 WSSD 上升的情形，
让折线上鼓起一个小峰。
这是因为初始中心位置碰巧选得不好时，
k-means 可能“卡”在劣质解里，
本章前面已经提到过这一点。

```{index} KMeans; n_init
```

```{note}
`scikit-learn` 实现的 k-means 很少卡在劣质解里，
因为 `scikit-learn` 会谨慎地选取初始中心，
尽量避免这种情况发生。
如果你画的肘部图上仍然出现了小峰，
可以在创建 `KMeans` 对象时调大 `n_init` 参数，
例如 `KMeans(n_clusters=k, n_init=10)`，多尝试几种不同的随机中心初始化。
从分析的角度看，这个值越大越好，
但代价是：聚类次数一多，耗时就会很长。
```

## 习题

本章讲到的内容配有练习题，
可在配套的
[练习册仓库](https://worksheets.python.datasciencebook.ca)的
“聚类（Clustering）”一行中找到。
点击“查看练习册（view worksheet）”，
即可预览本章练习册的非交互版本。
若要交互式地完成这些习题，请按练习册仓库中的说明下载全部练习册，并按照
{numref}`第 %s 章 <move-to-your-own-machine>` 中的计算机配置说明做好准备。
这样才能保证练习册提供的自动反馈和指导按预期发挥作用。

## 拓展资源

- 《An Introduction to Statistical Learning》第 10 章 {cite:p}`james2013introduction` 是
  继续学习聚类以及一般意义上的无监督学习的绝佳去处。
  单就聚类而言，它提供了与 k 均值聚类配套的出色入门介绍，
  还讲了*层次*聚类，
  适用于你预期数据中存在子组、
  子组之中又有子组等情况。
  在更一般的无监督学习方面，
  它介绍了*主成分分析（PCA）*，
  这是减少数据集中预测变量个数时很常用的一种方法。

+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```

<<TERM>>
nominal = 名义型
elbow plot = 肘部图
<<END>>
