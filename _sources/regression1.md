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

(regression1)=
# 回归 I：k 近邻回归

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
from IPython.display import HTML
from IPython.display import Image
import plotly.express as px
import plotly.graph_objects as go
```

## 概述

本章继续探讨如何回答预测性问题。这里要预测的是*数值*变量，所用的方法是*回归*。前两章与此不同，它们用分类来预测类别型变量。不过，回归与分类有许多相似之处：例如，和分类一样，我们会把数据划分为训练集、验证集和测试集，会使用 `scikit-learn` 工作流，会用 k 近邻（K-NN）方法做出预测，也会用交叉验证来选择 K。正因为这些步骤十分相似，读本章之前请务必先读{numref}`第 %s 章 <classification1>`和{numref}`第 %s 章 <classification2>`——已经讲过的概念，这里会讲得快一些。本章主要讨论只有一个预测变量的情形，章末则展示如何用多个预测变量做回归，也就是*多元回归*（multivariable regression）。请注意，回归也可以用来回答推断性问题和因果问题，不过这超出了本书的范围。

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

和分类的情形一样，可以用来预测数值响应变量的方法有很多。本章重点介绍 **k 近邻**（K-nearest neighbors）算法 {cite:p}`knnfix,knncover`，下一章则学习**线性回归**。以后的学习中，你可能会遇到回归树、样条以及一般的局部回归方法；要从哪里开始了解这些方法，可以看下一章末尾的“拓展资源”一节。

分类中的许多概念都可以套用到回归上。例如，回归模型根据过去观测的数据集中相似观测的响应变量，来预测新观测的响应变量。建立回归模型时，我们先把数据划分为训练集和测试集，以确保在训练时未见过的观测上评估方法的性能。最后，我们可以用交叉验证来评价模型参数的不同取值（例如 k 近邻模型中的 K）。最大的区别在于，我们现在预测的是数值变量，而不是分类变量。

```{index} 分类变量, 数值变量
```

```{note}
通常你可以判断一个变量是数值还是类别型——从而判断自己需要做回归还是分类——方法是取出数据中两个观测 X 和 Y 的响应变量，然后问：“响应变量 X 是否*大于*响应变量 Y？”如果变量是类别型，这个问题毫无意义。（蓝色比红色更大吗？良性比恶性更大吗？）如果变量是数值，问题就有意义。（1.5 小时比 2.25 小时更长吗？\$500,000 比 \$400,000 更多吗？）不过使用这个经验法则时要小心：有时数据中的分类变量会被编码成数字（例如用“1”表示“benign”，用“0”表示“malignant”）。这时你要问的是标签的*含义*（“benign”与“malignant”），而不是它们的取值（“1”与“0”）。
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
由于{numref}`fig:07-edaRegr` 中 y 轴的单位是美元，我们把坐标轴标签的格式设为：在房价前面加上美元符号，并用逗号分隔，让较大的数字更易读。在 `altair` 中，只要在 `y` 编码通道上使用 `.axis(format="$,.0f")` 就能做到。
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

绘图结果见{numref}`fig:07-edaRegr`。可以看出，在加利福尼亚州萨克拉门托，房子面积越大，售价也越高。因此我们有理由认为，可以用一套尚未售出的房子（我们还不知道它的售价）的面积，来预测它最终的售价。这里并不是说面积大*导致*了售价高，只是说房价往往随面积增大而上升，而且我们也许能用后者预测前者。

+++

## k 近邻回归

```{index} k 近邻, k 近邻; 回归
```

和分类一样，在回归中我们也可以用基于 k 近邻的方法做出预测。在动手建立模型、评估它预测房价的效果之前，我们先从{numref}`fig:07-edaRegr` 的数据中抽取一个小样本，看看 k 近邻在回归语境下是如何工作的。抽取这个子样本，是为了用少量数据点说明 k 近邻回归的机制；本章后面会使用全部数据。

```{index} DataFrame; sample
```

要抽取一个大小为 30 的小随机样本，我们在 `sacramento` 数据框上使用 `sample` 方法，并指定选取 `n=30` 行。

```{code-cell} ipython3
small_sacramento = sacramento.sample(n=30)
```

接下来假设我们在萨克拉门托遇到一套 2,000 平方英尺的房子，有意购买，挂牌价为 \$350,000。我们该按要价买下它，还是认为它定价偏高、应该压价？没有其他信息时，我们可以用手头的数据，根据已经观测到的售价来预测这套房子的售价，从而对合理的答案有个大致判断。但在{numref}`fig:07-small-eda-regr` 中可以看到，我们并没有面积*恰好*为 2,000 平方英尺的房子的观测。那该怎么预测它的售价呢？

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

我们会沿用{numref}`第 %s 章 <classification1>`和{numref}`第 %s 章 <classification2>`中的思路，用与感兴趣的新数据点相邻的点，来推测、预测它可能的售价。在{numref}`fig:07-small-eda-regr` 所示的例子里，我们找出距离那套 2,000 平方英尺的房子最近的 5 个近邻，并加以标注。

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

{numref}`fig:07-knn5-example` 展示了与我们关注的那套 2,000 平方英尺新房最接近的 5 个近邻（就房屋面积而言）的面积与这套新房的差别。得到这些近邻之后，我们就可以用它们的取值来预测新房子的售价。具体来说，可以取这 5 个取值的均值（也就是平均数）作为预测值，{numref}`fig:07-predictedViz-knn` 中的红点就是它。

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

我们的预测价格是 \${glue:text}`knn-5-pred`（见{numref}`fig:07-predictedViz-knn` 中的红点），它远低于 \$350,000；也许我们应该出价比挂牌价低一些。不过故事才刚刚开始。在 k 近邻回归中，我们仍然面临当初做 k 近邻分类时那些没有答案的问题：$K$ 该取多少？模型的预测够不够好？接下来几节会在 k 近邻回归的语境下回答这些问题。

这里要特别提一下 k 近邻回归算法的一个优点：它能很好地处理非线性关系（也就是说，关系不是一条直线）。这源于它用近邻来预测取值的做法。这个算法对数据必须呈现什么样子，只提出很少的假设。

+++

## 训练、评估与调优模型

```{index} 训练集, 测试集
```

和往常一样，我们必须先把一部分测试数据放进保险箱锁起来，等选定最终模型之后再回头使用。现在就来做这件事。请注意，本章余下的部分都会使用完整的萨克拉门托数据集，而不是前面用过的那个 30 个数据点的小样本（{numref}`fig:07-small-eda-regr`）。

+++

```{note}
这里没有像{numref}`第 %s 章 <classification2>`那样指定 `stratify` 参数，因为 `train_test_split` 函数无法按定量变量分层。
```

```{code-cell} ipython3
:tags: [remove-cell]
# fix seed right before train/test split for reproducibility with next chapter
# make sure this seed is always the same as the one used before the split in Regression 2
np.random.seed(1)
```

```{code-cell} ipython3
sacramento_train, sacramento_test = train_test_split(
    sacramento, train_size=0.75
)
```

```{index} 交叉验证, RMSPE
```

```{index} see: 均方根预测误差; RMSPE
```

接下来，我们用交叉验证来选择 $K$。在 k 近邻分类中，我们用准确率来衡量预测结果与真实标签的吻合程度；在回归的场景下则不能沿用同一个指标，因为我们的预测几乎不可能与响应变量的真实取值*完全*一致。因此在 k 近邻回归中，我们改用均方根预测误差（root mean square prediction error，RMSPE）。计算 RMSPE 的数学公式为：

$$\text{RMSPE} = \sqrt{\frac{1}{n}\sum\limits_{i=1}^{n}(y_i - \hat{y}_i)^2}$$

其中：

- $n$ 是观测个数，
- $y_i$ 是第 $i^\text{th}$ 个观测的观测值，
- $\hat{y}_i$ 是第 $i^\text{th}$ 个观测的预测值。

换句话说，对测试集（或验证集）中的每个观测，我们计算预测值与响应变量真实值之差的*平方*，再求平均，最后取平方根。之所以用*平方*差（而不是只用差），是因为差值可正可负，也就是说，我们的预测可能高估、也可能低估响应变量的真实值。{numref}`fig:07-verticalerrors` 展示了预测值与真实响应值之间正向和负向的差。因此，如果要衡量误差——也就是预测值与真实响应值之间的距离——我们就要确保只把正值累加起来，而且正值越大代表错误越大。如果预测值与真实值非常接近，RMSPE 就很小；反过来，如果预测值与真实值相差很大，RMSPE 就相当大。使用交叉验证时，我们会选择让 RMSPE 最小的 $K$。

```{code-cell} ipython3
:tags: [remove-cell]

from sklearn.neighbors import KNeighborsRegressor

# (synthetic) new prediction points
pts = pd.DataFrame({"sqft": [1200, 1850, 2250], "price": [300000, 200000, 500000]})
finegrid = pd.DataFrame({"sqft": np.arange(600, 3901, 10)})

# preprocess the data, make the pipeline
sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft"]))
sacr_pipeline = make_pipeline(sacr_preprocessor, KNeighborsRegressor(n_neighbors=4))

# fit the model
X = small_sacramento[["sqft"]]
y = small_sacramento[["price"]]
sacr_pipeline.fit(X, y)

# predict on the full grid and new data pts
sacr_full_preds_hid = pd.concat(
    (finegrid, pd.DataFrame(sacr_pipeline.predict(finegrid), columns=["predicted"])),
    axis=1,
)

sacr_new_preds_hid = pd.concat(
    (small_sacramento[["sqft", "price"]].reset_index(), pd.DataFrame(sacr_pipeline.predict(small_sacramento[["sqft", "price"]]), columns=["predicted"])),
    axis=1,
).drop(columns=["index"])

# to make altair mark_line works, need to create separate dataframes for each vertical error line
errors_plot = (
    small_plot
    + alt.Chart(sacr_full_preds_hid).mark_line(color="#ff7f0e").encode(x="sqft", y="predicted")
    + alt.Chart(sacr_new_preds_hid)
    .mark_circle(opacity=1)
    .encode(x="sqft", y="price")
)
sacr_new_preds_melted_df = sacr_new_preds_hid.melt(id_vars=["sqft"])
v_lines = []
for i in sacr_new_preds_hid["sqft"]:
    line_df = sacr_new_preds_melted_df.query(f"sqft == {i}")
    v_lines.append(alt.Chart(line_df).mark_line(color="black").encode(x="sqft", y="value"))

errors_plot = alt.layer(*v_lines, errors_plot)
errors_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-verticalerrors", errors_plot, display=False)
```

:::{glue:figure} fig:07-verticalerrors
:name: fig:07-verticalerrors

售价（美元）与房屋面积（平方英尺）的散点图，其中包含示例预测值（橙色线条），以及这些预测值与真实响应值相比的误差（竖线）。
:::

+++

```{index} RMSPE; 与 RMSE 的比较
```

```{note}
在使用许多代码包时，用来评估 k 近邻回归模型预测质量的输出会被标注为“RMSE”，也就是“均方根误差”（root mean squared error）。为什么会这样，而不是 RMSPE 呢？在统计学中，我们尽量把话说得精确，以表明所计算的预测误差来自训练数据（*样本内*预测）还是测试数据（*样本外*预测）。在训练数据上做预测并评估预测质量时，我们说 RMSE；相比之下，在测试数据或验证数据上做预测并评估预测质量时，我们说 RMSPE。RMSE 与 RMSPE 的计算式完全相同，唯一的区别在于其中的 $y$ 取自训练数据还是测试数据。不过很多人对两者都直接用 RMSE，靠上下文来表明均方根误差是基于哪一份数据计算的。
```

```{index} scikit-learn, scikit-learn; Pipeline, scikit-learn; make_pipeline, scikit-learn; make_column_transformer
```

现在我们知道了如何评估模型对数值的预测效果，接下来就用 Python 做交叉验证，选出最优的 $K$。首先创建一个列变换器（column transformer）来预处理数据。请注意，我们在预处理中加入了标准化，是为了养成良好习惯；但由于只有一个预测变量，技术上并不需要这一步：不存在比较两个标度不同的预测变量的风险。接着我们为 k 近邻回归创建模型流水线。注意这里改用 `KNeighborsRegressor` 模型对象，以表示这是一个回归问题，而不是前几章讨论的分类问题。使用 `KNeighborsRegressor` 实际上是在告诉 `scikit-learn`：调优和评估需要使用不同的指标（而不是准确率）。随后我们指定一个参数网格，其中近邻个数从 1 到 200。然后创建一个 5 折 `GridSearchCV` 对象，并传入流水线和参数网格。这里还有一点小麻烦：与 `scikit-learn` 中的分类模型不同——分类模型默认就用准确率来调优，正合我们的需要——`scikit-learn` 中的回归模型默认不用 RMSPE 来调优。因此，我们需要把 `scoring` 参数设为 `"neg_root_mean_squared_error"`，以指明调优时要使用 RMSPE。

```{note}
表示近邻个数的参数标识符 `"kneighborsregressor__n_neighbors"`，是我们查看 `sacr_pipeline.get_params()` 的输出得到的，做法与{numref}`第 %s 章 <classification1>`中一样。
```

```{index} scikit-learn; GridSearchCV
```

```{code-cell} ipython3
# import the K-NN regression model
from sklearn.neighbors import KNeighborsRegressor

# preprocess the data, make the pipeline
sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft"]))
sacr_pipeline = make_pipeline(sacr_preprocessor, KNeighborsRegressor())

# create the 5-fold GridSearchCV object
param_grid = {
    "kneighborsregressor__n_neighbors": range(1, 201, 3),
}
sacr_gridsearch = GridSearchCV(
    estimator=sacr_pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="neg_root_mean_squared_error",
)
```

接下来，我们调用 `sacr_gridsearch` 的 `fit` 方法来运行交叉验证。请注意，输入特征用了两层方括号（`sacramento_train[["sqft"]]`），这样得到的是只含一列的数据框。正如我们在{numref}`第 %s 章 <wrangling>`中学到的，传入列名列表就能得到包含部分列的数据框；`["sqft"]` 是只含一个元素的列表，所以得到的数据框只有一列。如果只用一层方括号（`sacramento_train["sqft"]`），得到的则是一个序列。在 `scikit-learn` 中，把输入特征当作数据框处理比当作序列更方便，因此这里我们选择两层方括号。而在响应变量那边，用序列就可以了，所以只用一层方括号（`sacramento_train["price"]`）。

与{numref}`第 %s 章 <classification2>`一样，模型拟合完成后，我们会把 `cv_results_` 的输出放进数据框，只提取需要的列，按 5 折计算标准误，并把参数列重命名，使其更易读。


```{code-cell} ipython3
# fit the GridSearchCV object
sacr_gridsearch.fit(
    sacramento_train[["sqft"]],  # A single-column data frame
    sacramento_train["price"]  # A series
)

# Retrieve the CV scores
sacr_results = pd.DataFrame(sacr_gridsearch.cv_results_)
sacr_results["sem_test_score"] = sacr_results["std_test_score"] / 5**(1/2)
sacr_results = (
    sacr_results[[
        "param_kneighborsregressor__n_neighbors",
        "mean_test_score",
        "sem_test_score"
    ]]
    .rename(columns={"param_kneighborsregressor__n_neighbors": "n_neighbors"})
)
sacr_results
```

在结果数据框 `sacr_results` 中可以看到，`n_neighbors` 变量存放的是 $K$ 的各项取值，`mean_test_score` 变量存放的是交叉验证估计出的 RMSPE……等一下！RMSPE 不是应该非负吗？回想一下，我们在 `GridSearchCV` 对象中指定 `scoring` 参数时，用的值是 `"neg_root_mean_squared_error"`。看到开头的 `neg_` 了吗？它表示*负*（negative）！原来，`scikit-learn` 调优模型时总是设法*最大化*得分，而调优回归模型时我们要*最小化* RMSPE。于是 `scikit-learn` 改用*负的* RMSPE 来绕开这个矛盾。这确实有点绕，但我们还需要再多做一步，把负的 RMSPE 换算回普通的 RMSPE。

```{code-cell} ipython3
sacr_results["mean_test_score"] = -sacr_results["mean_test_score"]
sacr_results
```

好了，现在 `mean_test_score` 变量存放的确实是不同近邻个数下的 RMSPE 取值。最后，`sem_test_score` 变量存放的是交叉验证 RMSPE 估计值的标准误，它衡量我们对这个均值有多不确定。粗略地说，如果估计出的平均 RMSPE 是 \$100,000，标准误是 \$1,000，那么可以预期*真实*的 RMSPE 大致落在 \$99,000 到 \$101,000 之间（不过也可能落在这个范围之外）。

{numref}`fig:07-choose-k-knn-plot` 展示了 RMSPE 如何随近邻个数 $K$ 变化。我们取 RMSPE 的*最小值*来确定近邻个数的最佳设置。RMSPE 最小时，$K$ 的取值为 {glue:text}`best_k_sacr`。

```{code-cell} ipython3
:tags: [remove-cell]
best_k_sacr = sacr_results["n_neighbors"][sacr_results["mean_test_score"].idxmin()]
best_cv_RMSPE = min(sacr_results["mean_test_score"])
glue("best_k_sacr", "{:d}".format(best_k_sacr))
glue("cv_RMSPE", "{0:,.0f}".format(best_cv_RMSPE))
```

```{code-cell} ipython3
:tags: [remove-cell]

sacr_tunek_plot = alt.Chart(sacr_results).mark_line(point=True).encode(
    x=alt.X("n_neighbors:Q", title="Neighbors"),
    y=alt.Y("mean_test_score", scale=alt.Scale(zero=False), title="Cross-Validation RMSPE Estimate")
)

sacr_tunek_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-choose-k-knn-plot", sacr_tunek_plot, display=False)
```

:::{glue:figure} fig:07-choose-k-knn-plot
:name: fig:07-choose-k-knn-plot

近邻个数对 RMSPE 的影响。
:::

要想知道哪个参数取值对应最小的 RMSPE，我们也可以访问最初拟合的 `GridSearchCV` 对象的 `best_params_` 属性。请注意，像上面那样把结果可视化仍然很有用，因为它能额外说明模型性能是怎样变化的。

```{code-cell} ipython3
sacr_gridsearch.best_params_
```

+++

## 欠拟合与过拟合
与分类的情形类似，把近邻个数设得太小或太大，都会使 RMSPE 增大，如{numref}`fig:07-choose-k-knn-plot` 所示。这里发生了什么？

{numref}`fig:07-howK` 展示了 $K$ 取不同值时回归模型的表现。每张图都给出了我们的 k 近邻回归模型在 6 个不同的 $K$ 值下预测的房屋售价：1、3、25、{glue:text}`best_k_sacr`、250 和 699（也就是全部训练数据）。对每个模型，我们都预测数据集中出现过的各种房屋面积（这里是 500 到 5,000 平方英尺）对应的价格，并把预测价格画成橙色线条。

```{code-cell} ipython3
:tags: [remove-cell]

gridvals = [
    1,
    3,
    25,
    best_k_sacr,
    250,
    len(sacramento_train),
]

plots = list()

sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft"]))
X = sacramento_train[["sqft"]]
y = sacramento_train[["price"]]

base_plot = (
    alt.Chart(sacramento_train)
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size (square feet)", scale=alt.Scale(zero=False)),
        y=alt.Y("price", title="Price (USD)", axis=alt.Axis(format="$,.0f")),
    )
)
for i in range(len(gridvals)):
    # make the pipeline based on n_neighbors
    sacr_pipeline = make_pipeline(
        sacr_preprocessor, KNeighborsRegressor(n_neighbors=gridvals[i])
    )
    sacr_pipeline.fit(X, y)
    # predictions
    sacr_preds = sacramento_train
    sacr_preds = sacr_preds.assign(predicted=sacr_pipeline.predict(sacramento_train))
    # overlay the plots
    plots.append(
        base_plot
        + alt.Chart(sacr_preds, title=f"K = {gridvals[i]}")
        .mark_line(color="#ff7f0e")
        .encode(x="sqft", y="predicted")
    )
```

```{code-cell} ipython3
:tags: [remove-cell]

glue(
    "fig:07-howK", (plots[0] | plots[1]) & (plots[2] | plots[3]) & (plots[4] | plots[5])
)
```

:::{glue:figure} fig:07-howK
:name: fig:07-howK

取六个不同 $K$ 值时 k 近邻回归模型预测的房屋价格（用橙色线条表示）。
:::

+++

```{index} 过拟合; 回归
```

{numref}`fig:07-howK` 表明，当 $K$ = 1 时，橙色线条完美地穿过了我们几乎所有的训练观测。这是因为某个区域的预测值（通常）只取决于单个观测。一般来说，$K$ 太小时，线条会相当贴近训练数据，即使不能与之完全吻合。如果我们换一份来自萨克拉门托房地产市场、包含房屋价格和面积的训练数据集，最终会得到完全不同的预测。换句话说，模型受数据的*影响太大*。由于模型紧紧跟随训练数据，它对新的观测就做不出准确预测，而新观测通常不会带有与原训练数据相同的波动。回忆分类各章的内容可知，这种模型受有噪声数据影响过大的行为称为*过拟合*；在回归的语境中我们也用同一个术语。

```{index} 欠拟合; 回归
```

{numref}`fig:07-howK` 中 $K$ 相当大的那几张图，比如 $K$ = 250 或 699，又是什么情况呢？这时橙色线条变得极其平滑，而当 $K$ 等于整个数据集中的数据点个数时，它实际上变成了一条水平线。这是因为，对于某个 x 取值（这里是房屋面积），我们的预测值取决于许多近邻观测；如果 $K$ 等于数据集的大小，预测值就只是数据集中房屋价格的均值（完全忽略了房屋面积）。与 $K=1$ 的例子相比，这条平滑、不灵活的橙色线条并不怎么贴近训练观测。换句话说，模型受训练数据的*影响不够*。回忆分类各章的内容可知，这种行为称为*欠拟合*；在回归的语境中我们同样使用这个术语。

理想情况下，上面讨论的两种情况都不是我们想要的。我们希望模型既能（1）跟随训练数据整体的“趋势”，真正利用训练数据学到有用的东西，又能（2）不跟随有噪声的波动，这样我们才有把握说模型能很好地迁移/泛化到其他新数据。如果我们再看看 $K$ 的其他取值，特别是 $K$ = {glue:text}`best_k_sacr`（正如交叉验证所建议的），就会发现它达到了这个目标：它跟随房屋价格随房屋面积上升的趋势，又不会受价格中那些个别波动的影响。这一切都与 $K$ 的取值如何影响 k 近邻分类类似，上一章已经讨论过。

## 在测试集上评估

要评估模型在未见过的数据上预测得怎么样，我们来看它在测试数据上的 RMSPE。为此，首先要用 $K =$ {glue:text}`best_k_sacr` 个近邻在整个训练数据集上重新训练 k 近邻回归模型。正如我们在{numref}`第 %s 章 <classification2>`中所见，这一步不必自己手动完成，`scikit-learn` 会自动替我们做好。要用最佳模型在测试数据上做预测，我们可以调用已拟合的 `GridSearchCV` 对象的 `predict` 方法。接着用 `mean_squared_error` 函数（传入 `y_true` 和 `y_pred` 参数）计算均方预测误差，最后开平方得到 RMSPE。我们不直接使用 `score` 方法——如{numref}`第 %s 章 <classification2>`中那样——是因为 `KNeighborsRegressor` 模型默认使用的评分指标与 RMSPE 不同。

```{code-cell} ipython3
from sklearn.metrics import mean_squared_error

sacramento_test["predicted"] = sacr_gridsearch.predict(sacramento_test)
RMSPE = mean_squared_error(
    y_true=sacramento_test["price"],
    y_pred=sacramento_test["predicted"]
)**(1/2)
RMSPE
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("test_RMSPE", "{0:,.0f}".format(RMSPE))
```

以 RMSPE 衡量，我们最终模型的测试误差为 \${glue:text}`test_RMSPE`。请注意，RMSPE 的度量单位与响应变量相同。换句话说，对于新观测，我们预计预测误差*大致*为 \${glue:text}`test_RMSPE`。从一个角度看，这是好消息：这个值和调优后模型的交叉验证 RMSPE 估计值差不多（该估计值为 \${glue:text}`cv_RMSPE`），因此可以说，该模型看上去能很好地泛化到从未见过的新数据。不过，与 k 近邻分类的情形很像，这个 RMSPE 值算不算*好*——也就是说，大约 \${glue:text}`test_RMSPE` 的误差是否可以接受——完全取决于具体应用。在这个应用里，这个误差不算大得无法承受，但也绝不可忽略；\${glue:text}`test_RMSPE` 可能占购房者预算的相当大一部分，甚至决定他们到底买不买得起、能不能给房子出价。

最后，{numref}`fig:07-predict-all` 展示了我们最终的模型在萨克拉门托地区可能遇到的各种房屋面积上给出的预测。请注意，我们并不是只对数据中恰好出现的那些房屋面积预测房价，而是对数据集中最小值与最大值之间等间距的取值（大约 500 到 5000 平方英尺）逐一预测。我们把这条预测线叠加在原始房价数据的散点图上，这样就能定性地判断模型是否很好地拟合了数据。本章前面你已经见过几张这样的图，不过这里我们也把生成它的代码提供出来，当作一次学习机会。

```{code-cell} ipython3
:tags: [remove-output]

# Create a grid of evenly spaced values along the range of the sqft data
sqft_prediction_grid = pd.DataFrame({
    "sqft": np.arange(sacramento["sqft"].min(), sacramento["sqft"].max(), 10)
})
# Predict the price for each of the sqft values in the grid
sqft_prediction_grid["predicted"] = sacr_gridsearch.predict(sqft_prediction_grid)

# Plot all the houses
base_plot = alt.Chart(sacramento).mark_circle(opacity=0.4).encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .title("Price (USD)")
)

# Add the predictions as a line
sacr_preds_plot = base_plot + alt.Chart(
    sqft_prediction_grid,
    title=f"K = {best_k_sacr}"
).mark_line(
    color="#ff7f0e"
).encode(
    x="sqft",
    y="predicted"
)

sacr_preds_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-predict-all", sacr_preds_plot)
```

:::{glue:figure} fig:07-predict-all
:name: fig:07-predict-all

最终 k 近邻回归模型预测的房价（橙色线）。
:::

+++

## 多元 k 近邻回归

与 k 近邻分类一样，k 近邻回归也可以使用多个预测变量。此时预测变量的标度会带来同样的顾虑。同样，做预测时要先找出与待预测的新点最接近的 $K$ 个观测；标度大的变量所起的作用会远大于标度小的变量。因此，我们应当重新定义流水线中的预处理器（preprocessor），把所有预测变量都纳入进来。

还要注意，k 近邻回归中预测变量的选择与 k 近邻分类有同样的顾虑：预测变量更多**并不**总是更好，而且选用哪些预测变量对预测质量可能有很大影响。好在 k 近邻回归同样可以使用{numref}`第 %s 章 <classification2>`中的预测变量选择算法。算法是同一个，本章不再重复介绍。

```{index} k 近邻; 多元回归, 萨克拉门托房地产市场
```

下面我们用 `scikit-learn` 对萨克拉门托房地产数据做一次多元 k 近邻回归分析。这一次，我们用房屋面积（以平方英尺计）和卧室数量作为预测变量，并继续用房屋售价作为我们要预测的响应变量。在开始建模之前先做探索性数据分析（例如把数据可视化），始终是良好实践。{numref}`fig:07-bedscatter` 表明，卧室数量也许能提供有助于预测房屋售价的有用信息。

```{code-cell} ipython3
:tags: [remove-output]

plot_beds = alt.Chart(sacramento).mark_circle().encode(
    x=alt.X("beds").title("Number of Bedrooms"),
    y=alt.Y("price").title("Price (USD)").axis(format="$,.0f"),
)

plot_beds
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-bedscatter", plot_beds)
```

:::{glue:figure} fig:07-bedscatter
:name: fig:07-bedscatter

房屋售价与卧室数量的散点图。
:::

+++

{numref}`fig:07-bedscatter` 表明，卧室数量增加时，房屋售价往往也随之上升，但两者关系相当弱。把卧室数量加入模型，能否提高我们预测价格的能力？要回答这个问题，我们需要新建一个使用房屋面积和卧室数量的 k 近邻回归模型，再把它与之前只用房屋面积的模型比较。我们现在就动手！

首先，我们为这次分析构建新的模型对象和预处理器。注意，我们把列表 `["sqft", "beds"]` 传给 `make_column_transformer` 函数，以表明有两个预测变量。此外，我们没有在 `KNeighborsRegressor` 中指定 `n_neighbors`，说明希望这个参数由 `GridSearchCV` 来调优。

```{code-cell} ipython3
sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft", "beds"]))
sacr_pipeline = make_pipeline(sacr_preprocessor, KNeighborsRegressor())
```

接下来，我们用 5 折交叉验证配合 `GridSearchCV` 对象，按照 RMSPE 最小来选取近邻个数：

```{code-cell} ipython3
# create the 5-fold GridSearchCV object
param_grid = {
    "kneighborsregressor__n_neighbors": range(1, 50),
}

sacr_gridsearch = GridSearchCV(
    estimator=sacr_pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="neg_root_mean_squared_error"
)

sacr_gridsearch.fit(
  sacramento_train[["sqft", "beds"]],
  sacramento_train["price"]
)

# retrieve the CV scores
sacr_results = pd.DataFrame(sacr_gridsearch.cv_results_)
sacr_results["sem_test_score"] = sacr_results["std_test_score"] / 5**(1/2)
sacr_results["mean_test_score"] = -sacr_results["mean_test_score"]
sacr_results = (
    sacr_results[[
        "param_kneighborsregressor__n_neighbors",
        "mean_test_score",
        "sem_test_score"
    ]]
    .rename(columns={"param_kneighborsregressor__n_neighbors" : "n_neighbors"})
)

# show only the row of minimum RMSPE
sacr_results.nsmallest(1, "mean_test_score")
```

```{code-cell} ipython3
:tags: [remove-cell]

best_k_sacr_multi = sacr_results["n_neighbors"][sacr_results["mean_test_score"].idxmin()]
min_rmspe_sacr_multi = min(sacr_results["mean_test_score"])
glue("best_k_sacr_multi", "{:d}".format(best_k_sacr_multi))
glue("cv_RMSPE_2pred", "{0:,.0f}".format(min_rmspe_sacr_multi))
```

这里我们看到，交叉验证给出的最小 RMSPE 估计值出现在 $K =$ {glue:text}`best_k_sacr_multi` 时。如果要在*模型调优过程中*把这个多元 k 近邻回归模型与只有单个预测变量的模型作比较（例如，我们正在做前向选择（forward selection），具体做法见讲解分类模型评估与调优的那一章），那就必须比较仅用训练数据通过交叉验证估计出的 RMSPE。回头看，单预测变量模型的交叉验证 RMSPE 估计值为 \${glue:text}`cv_RMSPE`。多元模型的交叉验证 RMSPE 估计值为 \${glue:text}`cv_RMSPE_2pred`。因此在这个例子里，加入这个额外的预测变量并没有让模型提升多少。

不管怎样，我们继续分析，看看如何用多元 k 近邻回归模型做预测，并在测试数据上评估它的性能。和前面一样，我们用最佳模型对测试数据做预测，也就是调用已拟合的 `GridSearchCV` 对象的 `predict` 方法。最后，我们用 `mean_squared_error` 函数计算 RMSPE。

```{code-cell} ipython3
sacramento_test["predicted"] = sacr_gridsearch.predict(sacramento_test)
RMSPE_mult = mean_squared_error(
    y_true=sacramento_test["price"],
    y_pred=sacramento_test["predicted"]
)**(1/2)
RMSPE_mult

```

```{code-cell} ipython3
:tags: [remove-cell]

glue("RMSPE_mult", "{0:,.0f}".format(RMSPE_mult))
```

这一次，我们在同一个数据集上做 k 近邻回归，但把卧室数量也作为预测变量，得到的 RMSPE 测试误差为 \${glue:text}`RMSPE_mult`。{numref}`fig:07-knn-mult-viz` 把模型的预测叠加在数据之上做了可视化。这次有 2 个预测变量而不是 1 个，所以预测不再是二维空间中的一条直线，而是三维空间中的一个曲面。

```{code-cell} ipython3
:tags: [remove-input]

# create a prediction pt grid
xvals = np.linspace(
    sacramento_train["sqft"].min(), sacramento_train["sqft"].max(), 50
)
yvals = np.linspace(
    sacramento_train["beds"].min(), sacramento_train["beds"].max(), 50
)
xygrid = np.array(np.meshgrid(xvals, yvals)).reshape(2, -1).T
xygrid = pd.DataFrame(xygrid, columns=["sqft", "beds"])

# add prediction
knnPredGrid = sacr_gridsearch.predict(xygrid)

fig = px.scatter_3d(
    sacramento_train,
    x="sqft",
    y="beds",
    z="price",
    opacity=0.4,
    labels={"sqft": "Size (sq ft)", "beds": "Bedrooms", "price": "Price (USD)"},
)

fig.update_traces(marker={"size": 2, "color": "red"})

fig.add_trace(
    go.Surface(
        x=xvals,
        y=yvals,
        z=knnPredGrid.reshape(50, -1),
        name="Predictions",
        colorscale="viridis",
        colorbar={"title": "Price (USD)"}
    )
)

fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=1),
    template="plotly_white",
)

# if HTML, use the plotly 3d image; if PDF, use static image
if "BOOK_BUILD_TYPE" in os.environ and os.environ["BOOK_BUILD_TYPE"] == "PDF":
    glue("fig:07-knn-mult-viz", Image("img/regression1/plot3d_knn_regression.png"))
else:
    glue("fig:07-knn-mult-viz", fig)
```

```{figure} data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
:name: fig:07-knn-mult-viz
:figclass: caption-hack

k 近邻回归模型的预测以三维空间中的曲面表示，叠加在使用三个预测变量（价格、房屋面积和卧室数量）的数据之上。一般我们并不推荐使用三维可视化；这里只是为了教学演示，才用三维可视化展示预测曲面是什么样子。
```

+++

可以看到，在有 2 个预测变量时，预测形成的是曲面而不是直线。新加入的预测变量（卧室数量）与价格有关（价格变化时，卧室数量也随之变化），并且不完全由房屋面积（我们的另一个预测变量）决定，因此它为我们做预测带来了额外而有用的信息。例如，在这个模型中，我们会预测面积为 2,500 平方英尺的房屋，其价格通常随卧室数量增加而略有上升。如果没有卧室数量这个额外的预测变量，面积相同、卧室数不同的两栋房子就会得到相同的预测价格（译注：原文此处说「这两栋房子」，但上文只提到一栋 2,500 平方英尺的房子，这里按文意补全为面积相同、卧室数不同的两栋）。

+++

## k 近邻回归的优势与局限

与 k 近邻分类（其实任何预测算法都是如此）一样，k 近邻回归既有优势也有不足。这里列出其中一些：

**优势：** k 近邻回归

1. 是一种简单、直观的算法，
2. 对数据必须呈现什么样子只提出很少的假设，
3. 能很好地处理非线性关系（即关系不是一条直线）。

**不足：** k 近邻回归

1. 训练数据变大时会变得非常慢，
2. 预测变量很多时可能表现不佳，
3. 在你的训练数据取值范围之外可能预测得不好。

+++

## 习题

本章所讲内容对应的练习题，可以在配套的[练习册仓库](https://worksheets.python.datasciencebook.ca)中“Regression I: K-nearest neighbors”那一行找到。点击“查看练习册（view worksheet）”，你就能预览本章练习册的非交互版本。要交互式地做这些习题，请按练习册仓库中的说明下载全部练习册，并按{numref}`第 %s 章 <move-to-your-own-machine>`中给出的计算机环境配置说明操作。这样才能保证练习册提供的自动反馈和指导按预期正常工作。


+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
