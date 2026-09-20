(regression1)=
# 回归 I：k 近邻

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
from IPython.display import HTML
from IPython.display import Image
import plotly.express as px
import plotly.graph_objects as go
```

## 概述

本章继续探讨如何回答预测性问题。这里要预测的是*数值*变量，所用的方法是*回归*。前两章与此不同，它们用分类来预测类别型变量。不过，回归与分类有许多相似之处：例如，和分类一样，我们会把数据划分为训练集、验证集和测试集，会使用 `scikit-learn` 工作流，会用 k 近邻（K-NN）方法做出预测，也会用交叉验证来选择 K。正因为这些步骤十分相似，读本章之前请务必先读 {numref}`第 %s 章 <classification1>` 和 {numref}`%s <classification2>`——已经讲过的概念，这里会讲得快一些。本章主要讨论只有一个预测变量的情形，章末则展示如何用多个预测变量做回归，也就是*多元回归*（multivariable regression）。请注意，回归也可以用来回答推断性问题和因果问题，不过这超出了本书的范围。

+++

## 本章学习目标
学完本章后，你将能够：

- 识别适合用回归分析做出预测的情形。
- 解释 k 近邻（K-NN）回归算法，并说明它与 k 近邻分类的区别。
- 解读 k 近邻回归的输出。
- 在含两个及以上变量的数据集中，用 Python 完成 k 近邻回归。
- 在 Python 中用均方根预测误差（root mean squared prediction error，RMSPE）评估 k 近邻回归的预测质量。
- 在 Python 中用交叉验证或测试集估计 RMSPE。
- 以最小化交叉验证 RMSPE 估计值为准则，选择 k 近邻回归中的近邻个数。
- 说明欠拟合与过拟合，并解释它们与 k 近邻回归中近邻个数的关系。
- 说明 k 近邻回归的优缺点。

+++

## 回归问题

```{index} 预测性问题, 响应变量
```

回归和分类一样，都属于预测性问题：我们希望用过去的信息预测未来的观测。不过就回归而言，目标是预测*数值*而不是*类别型*取值。你想要预测的变量通常称为*响应变量*。例如，我们可以用一个人每周锻炼的小时数，来预测他参加一年一度波士顿马拉松的比赛用时；也可以用房子的面积来预测它的售价。这两个响应变量——比赛用时和售价——都是数值，因此根据过去的数据预测它们属于回归问题。

```{index} 分类; 与回归的比较
```

```{index} 回归; 与分类的比较
```

和分类的情形一样，可以用来预测数值响应变量的方法有很多。本章重点介绍 **k 近邻**（K-nearest neighbors）算法 {cite:p}`knnfix,knncover`，下一章则学习**线性回归**。以后的学习中，你可能会遇到回归树、样条以及各种局部回归方法；要从哪里开始了解这些方法，可以看下一章末尾的“拓展资源”一节。

分类中的许多概念都可以套用到回归上。例如，回归模型根据过去观测的数据集中相似观测的响应变量，来预测新观测的响应变量。建立回归模型时，我们先把数据划分为训练集和测试集，以确保在训练时未见过的观测上评估方法的性能。最后，我们还可以用交叉验证来评价模型参数的不同取值（例如 k 近邻模型中的 K）。最大的区别在于，我们现在预测的是数值变量，而不是分类变量。

```{index} 分类变量, 数值变量
```

```{note}
通常你可以判断一个变量是数值还是类别型——从而判断自己需要做回归还是分类——方法是取出数据中两个观测 X 和 Y 的响应变量，然后问：“响应变量 X 是否*大于*响应变量 Y？”如果变量是类别型，这个问题毫无意义。（蓝色比红色更大吗？良性比恶性更大吗？）如果变量是数值，问题就有意义。（1.5 小时比 2.25 小时更长吗？\$500,000 比 \$400,000 更多吗？）不过使用这个经验法则时要小心：有时数据中的分类变量会被编码成数字（例如用 “1” 表示 “benign”，用 “0” 表示 “malignant”）。这时你要问的是标签的*含义*（“benign” 与 “malignant”），而不是它们的取值（“1” 与 “0”）。
```

+++

## 探索数据集

```{index} 萨克拉门托房地产市场, 问题; 回归
```

本章和下一章要研究的数据集，包含[加利福尼亚州萨克拉门托的 932 笔房地产交易](https://support.spatialkey.com/spatialkey-sample-csv-data/)，最初由《Sacramento Bee》报道。我们首先要把自己想回答的问题表述清楚。这个例子中的问题仍然是预测性问题：能否用加利福尼亚州萨克拉门托地区一所房子的面积来预测它的售价？对这个问题给出严谨的定量答案，也许能帮助房地产经纪人告诉客户某套房源的挂牌价是否合理，或者帮他确定新挂牌房源的定价。我们先读取并查看数据，同时设定种子值。

```{index} 种子;numpy.random.seed
```

```{code-cell} ipython3
import altair as alt
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")

np.random.seed(10)

sacramento = pd.read_csv("data/sacramento.csv")
sacramento
```

```{index} altair; mark_circle, 可视化; 散点图
```

科学问题指引我们做最初的探索：我们关心的数据列是 `sqft`（房屋面积，以可居住的平方英尺计）和 `price`（房屋售价，以美元（USD）计）。第一步是把数据画成散点图，预测变量（房屋面积）放在 x 轴，想要预测的响应变量（售价）放在 y 轴。

```{note}
由于 {numref}`fig:07-edaRegr` 中 y 轴的单位是美元，我们把坐标轴标签的格式设为：在房价前面加上美元符号，并用逗号分隔，让较大的数字更易读。在 `altair` 中，只要在 `y` 编码通道上使用 `.axis(format="$,.0f")` 就能做到。
```

```{code-cell} ipython3
:tags: [remove-output]

scatter = alt.Chart(sacramento).mark_circle().encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .title("Price (USD)")
)

scatter
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("fig:07-edaRegr", scatter)
```

:::{glue:figure} fig:07-edaRegr
:name: fig:07-edaRegr

售价（美元）与房屋面积（平方英尺）的散点图。
:::

+++

绘图结果见 {numref}`fig:07-edaRegr`。可以看出，在加利福尼亚州萨克拉门托，房子面积越大，售价也越高。因此我们有理由认为，可以用一套尚未售出的房子（我们还不知道它的售价）的面积，来预测它最终的售价。这里并不是说面积大*导致*了售价高，只是说房价往往随面积增大而上升，而且我们也许能用后者预测前者。

+++

## k 近邻回归

```{index} k 近邻, k 近邻; 回归
```

和分类一样，在回归中我们也可以用基于 k 近邻的方法做出预测。在动手建立模型、评估它预测房价的效果之前，我们先从 {numref}`fig:07-edaRegr` 的数据中抽取一个小样本，看看 k 近邻（K-NN）在回归语境下是如何工作的。抽取这个子样本，是为了用少量数据点说明 k 近邻回归的机制；本章后面会使用全部数据。

```{index} DataFrame; sample
```

要抽取一个大小为 30 的小随机样本，我们在 `sacramento` 数据框上使用 `sample` 方法，并指定选取 `n=30` 行。

```{code-cell} ipython3
small_sacramento = sacramento.sample(n=30)
```

接下来假设我们在萨克拉门托遇到一套 2,000 平方英尺的房子，有意购买，挂牌价为 \$350,000。我们该按要价买下它，还是认为它定价偏高、应该压价？没有其他信息时，我们可以用手头的数据，根据已经观测到的售价来预测这套房子的售价，从而对合理的答案有个大致判断。但在 {numref}`fig:07-small-eda-regr` 中可以看到，我们并没有面积*恰好*为 2,000 平方英尺的房子的观测。那该怎么预测它的售价呢？

```{code-cell} ipython3
:tags: [remove-output]

small_plot = alt.Chart(small_sacramento).mark_circle(opacity=1).encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .title("Price (USD)")
)

# add an overlay to the base plot
line_df = pd.DataFrame({"x": [2000]})
rule = alt.Chart(line_df).mark_rule(strokeDash=[6], size=1.5, color="black").encode(x="x")

small_plot + rule
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-small-eda-regr", (small_plot + rule))
```

:::{glue:figure} fig:07-small-eda-regr
:name: fig:07-small-eda-regr

售价（美元）与房屋面积（平方英尺）的散点图，其中竖线在 x 轴上标出 2,000 平方英尺的位置。
:::

+++

```{index} DataFrame; abs, DataFrame; nsmallest
```

我们会沿用 {numref}`第 %s 章 <classification1>` 和 {numref}`%s <classification2>` 中的思路，用与感兴趣的新数据点相邻的点，来推测、预测它可能的售价。在 {numref}`fig:07-small-eda-regr` 所示的例子里，我们找出距离那套 2,000 平方英尺的房子最近的 5 个近邻，并加以标注。

```{code-cell} ipython3
small_sacramento["dist"] = (2000 - small_sacramento["sqft"]).abs()
nearest_neighbors = small_sacramento.nsmallest(5, "dist")
nearest_neighbors
```

```{code-cell} ipython3
:tags: [remove-cell]

nn_plot = small_plot + rule

# plot horizontal lines which is perpendicular to x=2000
h_lines = []
for i in range(5):
    h_line_df = pd.DataFrame({
        "sqft": [nearest_neighbors.iloc[i, 4], 2000],
        "price": [nearest_neighbors.iloc[i, 6]] * 2
    })
    h_lines.append(alt.Chart(h_line_df).mark_line(color="black").encode(x="sqft", y="price"))

# highlight the nearest neighbors in orange
orange_neighbrs = alt.Chart(nearest_neighbors).mark_circle(opacity=1, color="#ff7f0e").encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .title("Price (USD)")
)

nn_plot = alt.layer(*h_lines, small_plot, orange_neighbrs, rule)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-knn5-example", nn_plot)
```

:::{glue:figure} fig:07-knn5-example
:name: fig:07-knn5-example

售价（美元）与房屋面积（平方英尺）的散点图，并用线段连接到 5 个最近的近邻（用橙色标出）。
:::

+++

{numref}`fig:07-knn5-example` 展示了与我们关注的那套 2,000 平方英尺的新房子最接近的 5 个近邻（就房屋面积而言）在面积上的差异。得到这些近邻之后，我们就可以用它们的取值来预测新房子的售价。具体来说，可以取这 5 个取值的均值（也就是平均数）作为预测值，{numref}`fig:07-predictedViz-knn` 中的红点就是它。

```{code-cell} ipython3
prediction = nearest_neighbors["price"].mean()
prediction
```

```{code-cell} ipython3
:tags: [remove-cell]

nn_plot_pred = nn_plot + alt.Chart(
    pd.DataFrame({"sqft": [2000], "price": [prediction]})
).mark_circle(size=80, opacity=1, color="#d62728").encode(x="sqft", y="price")
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("knn-5-pred", "{0:,.0f}".format(prediction))
glue("fig:07-predictedViz-knn", nn_plot_pred)
```

:::{glue:figure} fig:07-predictedViz-knn
:name: fig:07-predictedViz-knn

售价（美元）与房屋面积（平方英尺）的散点图，其中根据 5 个近邻对一套 2,000 平方英尺房子给出的预测价格用红点表示。
:::

+++

我们的预测价格是 \${glue:text}`knn-5-pred`（见 {numref}`fig:07-predictedViz-knn` 中的红点），它远低于 \$350,000；也许我们应该出价比挂牌价低一些。不过故事才刚刚开始。在 k 近邻回归中，我们仍然面临当初做 k 近邻分类时那些没有答案的问题：$K$ 该取多少？模型的预测够不够好？接下来几节会在 k 近邻回归的语境下回答这些问题。

这里要特别提一下 k 近邻回归算法的一个优点：它能很好地处理非线性关系（也就是说，关系不是一条直线）。这源于它用近邻来预测取值的做法。这个算法对数据必须呈现什么样子，只提出很少的假设。

+++

## 训练、评估与调优模型

```{index} 训练集, 测试集
```

和往常一样，我们必须先把一部分测试数据放进保险箱锁起来，等选定最终模型之后再回头使用。现在就来做这件事。请注意，本章余下的部分都会使用完整的萨克拉门托数据集，而不是前面用过的那个 30 个数据点的小样本（{numref}`fig:07-small-eda-regr`）。