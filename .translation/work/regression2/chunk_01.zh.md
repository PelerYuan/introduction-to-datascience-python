
(regression2)=
# 回归 II：线性回归

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
from IPython.display import HTML
from IPython.display import Image
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
```

## 概述
到目前为止，我们解决所有预测性问题——无论是分类还是回归——用的都是基于 k 近邻（K-NN）的方法。
在回归问题中，还有一种常用方法，叫作*线性回归*。本章介绍线性回归的基本概念，
演示如何用 `scikit-learn` 在 Python 中做线性回归，
并说明它与 k 近邻回归相比有哪些长处和不足。和往常一样，重点放在只有一个预测变量和一个响应变量的情形；
不过本章最后会用一个*多元线性回归（multivariable linear regression）*的例子，说明预测变量
不止一个时该怎么办。

## 本章学习目标
学完本章后，你将能够：

- 用 Python 在训练数据上拟合简单线性回归模型和多元线性回归模型。
- 在测试数据上评估线性回归模型。
- 比较并对照同一数据集上由 k 近邻回归和线性回归得到的预测。
- 说明离群值和多重共线性（multicollinearity）会如何影响线性回归。

+++

## 简单线性回归

```{index} 回归; 线性
```

上一章末尾，我们提到 k 近邻回归的一些局限。这种方法虽然简单易懂，但在训练数据的预测变量取值范围
之外预测效果不佳，而且随着训练数据集变大，速度会明显变慢。好在 k 近邻回归有一个替代方案——*线性回归*——它把
这两个局限都化解了。线性回归在实际中也十分常用，因为它给出一个可解释的数学方程，描述
预测变量与响应变量之间的关系。本章前半部分讲*简单*线性回归，
其中只涉及一个预测变量和一个响应变量；后面我们会讨论
 *多元*线性回归，其中涉及多个预测变量。
 和 k 近邻回归一样，简单线性回归预测的也是数值型响应变量（比如赛跑时间、房屋价格或身高）；
 但它*如何*对新观测作出预测，与 k 近邻回归很不一样。
 简单线性回归不是找出最近的 K 个近邻、对它们的取值求平均来得到预测，而是穿过训练数据
 画一条最优拟合直线，再在这条直线上“查”出预测值。

+++

```{index} 回归; 逻辑回归
```

```{note}
虽然前面的章节没有涉及，分类还有一种常用的方法，叫作*逻辑回归*
（它用于分类，尽管名字里带着“回归”二字，这多少有些让人困惑）。在逻辑回归中——和线性回归类似——你先把
模型“拟合”到训练数据上，再为每个新观测“查”出预测值。逻辑回归与 K-NN 分类之间的优势与不足对比，
和线性回归与 k 近邻回归之间的对比类似。在学习逻辑回归之前，
先较好地理解线性回归会很有帮助。读完本章后，如果想进一步了解逻辑回归，
可以看分类各章末尾的“拓展资源”一节。
```

+++

```{index} 萨克拉门托房地产，问题; 回归
```

我们回到 {numref}`第 %s 章 <regression1>` 中的萨克拉门托住房数据，学习如何应用线性回归，并把它与
k 近邻回归作比较。这里先用住房数据的一个较小版本，以便把可视化结果看清楚。
回忆一下我们的预测性问题：能否用加利福尼亚州萨克拉门托地区的房屋面积来预测它的售价？
特别是，回想我们碰到过一栋 2,000 平方英尺的新房，想把它买下来，而广告标价是
\$350,000。我们该按标价出价吗？这个价格是偏高还是偏低？
要用简单线性回归回答这个问题，我们就用手上的数据，穿过已有的数据点画出最优拟合直线。
数据的小子集以及最优拟合直线如图 {numref}`fig:08-lin-reg1` 所示。

```{code-cell} ipython3
:tags: [remove-cell]

import pandas as pd

np.random.seed(2)

sacramento = pd.read_csv("data/sacramento.csv")

small_sacramento = sacramento.sample(n=30)

small_plot = (
    alt.Chart(small_sacramento)
    .mark_circle(opacity=1)
    .encode(
        x=alt.X("sqft")
            .scale(zero=False)
            .title("House size (square feet)"),
        y=alt.Y("price")
            .axis(format="$,.0f")
            .scale(zero=False)
            .title("Price (USD)"),
    )
)


# create df_lines with one fake/empty line (for starting at 2nd color later)
df_lines = {"x": [500, 500], "y": [100000, 100000], "number": ["-1", "-1"]}

# set the domains (range of x values) of lines
min_x = small_sacramento["sqft"].min()
max_x = small_sacramento["sqft"].max()

# add the line of best fit
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(small_sacramento[["sqft"]], small_sacramento[["price"]])
pred_min = float(lm.predict(pd.DataFrame({"sqft": [min_x]})))
pred_max = float(lm.predict(pd.DataFrame({"sqft": [max_x]})))

df_lines["x"].extend([min_x, max_x])
df_lines["y"].extend([pred_min, pred_max])
df_lines["number"].extend(["0", "0"])

# add other similar looking lines
intercept_l = [-64542.23, -6900, -64542.23]
slope_l = [190, 175, 160]
for i in range(len(slope_l)):
    df_lines["x"].extend([min_x, max_x])
    df_lines["y"].extend([
                        intercept_l[i] + slope_l[i] * min_x,
                        intercept_l[i] + slope_l[i] * max_x,
                    ])
    df_lines["number"].extend([f"{i+1}", f"{i+1}"])

df_lines = pd.DataFrame(df_lines)

# plot the bogus line to skip the same color as the scatter
small_plot += alt.Chart(
    df_lines[df_lines["number"] == "-1"]
).mark_line().encode(
    x="x", y="y", color=alt.Color("number", legend=None)
)
# plot the real line with 2nd color
small_plot += alt.Chart(
    df_lines[df_lines["number"] == "0"]
).mark_line().encode(
    x="x", y="y", color=alt.Color("number", legend=None)
)

small_plot
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("fig:08-lin-reg1", small_plot)
```

:::{glue:figure} fig:08-lin-reg1
:name: fig:08-lin-reg1

萨克拉门托住房数据子集的售价与面积散点图，图中画出了最优拟合直线。
:::

+++

```{index} 直线; 方程
```

```{index} see: 线; 直线
```

这条直线的方程是：

$$\text{house sale price} = \beta_0 + \beta_1 \cdot (\text{house size}),$$
其中

- $\beta_0$ 是这条直线的*纵截距*（房屋面积为 0 时的价格）
- $\beta_1$ 是这条直线的*斜率*（房屋面积增加时价格上升的快慢）

因此，用数据找出最优拟合直线，等价于找出使这条直线*参数化*（即与之对应）的系数
$\beta_0$ 和 $\beta_1$。
当然，在这个具体问题里，0 平方英尺的房子的想法有点荒唐；
但你可以把这里的 $\beta_0$ 看作“基础价”，把
$\beta_1$ 看作每平方英尺面积带来的价格增量。
我们把这个想法再推得远一点：如果去算一栋 *600 万*平方英尺的房子的价格，直线的方程会怎样？
那 *负* 2,000 平方英尺又怎样？结果是，公式本身不会出任何问题；只要你去问，线性
回归会很乐意对荒唐的预测变量取值作出预测。但即使你*可以*作出这些不着边际的预测，也不该这么做。
预测范围大致应落在原始数据的范围之内，只有在确实说得通时，才可以稍微超出一点。例如，
{numref}`fig:08-lin-reg1` 中的数据低端只到大约 600 平方英尺，但
用线性回归模型预测 500 平方英尺的价格，大概还是合理的。

回到例子！有了系数 $\beta_0$ 和 $\beta_1$，我们就可以用上面的方程，代入预测变量的取值
——这里是 2,000 平方英尺——算出预测售价。{numref}`fig:08-lin-reg2` 展示了这个过程。

```{code-cell} ipython3
:tags: [remove-cell]
from sklearn.linear_model import LinearRegression

lm = LinearRegression()
lm.fit(small_sacramento[["sqft"]], small_sacramento[["price"]])
prediction = float(lm.predict(pd.DataFrame({"sqft": [2000]})))

# the vertical dotted line
line_df = pd.DataFrame({"x": [2000]})
rule = alt.Chart(line_df).mark_rule(strokeDash=[6], size=1.5).encode(x="x")

# the red point
point_df = pd.DataFrame({"x": [2000], "y": [prediction]})
point = alt.Chart(point_df).mark_circle(color="red", size=80, opacity=1).encode(x="x", y="y")

# overlay all plots
small_plot_2000_pred = (
    small_plot
    + rule
    + point
    # add the text
    + alt.Chart(
        pd.DataFrame(
            {
                "x": [2450],
                "y": [prediction - 41000],
                "prediction": ["$" + "{0:,.0f}".format(prediction)],
            }
        )
    )
    .mark_text(dy=-5, size=15)
    .encode(x="x", y="y", text="prediction")
)

small_plot_2000_pred
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-lin-reg2", small_plot_2000_pred)
glue("pred_2000", "{0:,.0f}".format(prediction))
```

:::{glue:figure} fig:08-lin-reg2
:name: fig:08-lin-reg2

售价与面积的散点图，图中画出最优拟合直线，并用红点标出一栋 2,000 平方英尺房屋的预测售价。
:::

+++

我们用简单线性回归在这个小数据集上预测一栋 2,000 平方英尺房屋的售价，得到预测值
\${glue:text}`pred_2000`。不过等一下……简单
线性回归究竟是怎样选出最优拟合直线的呢？穿过这些数据点可以画出
许多条不同的直线。
几个看似合理的例子如图 {numref}`fig:08-several-lines` 所示。

```{code-cell} ipython3
:tags: [remove-cell]

several_lines_plot = small_plot.copy()

several_lines_plot += alt.Chart(
    df_lines[df_lines["number"] != "0"]
).mark_line().encode(x="x", y="y", color=alt.Color("number",legend=None))

several_lines_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-several-lines", several_lines_plot)
```

:::{glue:figure} fig:08-several-lines
:name: fig:08-several-lines

售价与面积的散点图，图中画出了多条可以穿过这些数据点的可能直线。
:::

+++

```{index} RMSPE
```

简单线性回归选出最优拟合直线的方式，是选出这样一条直线：它到训练数据中每个观测数据点的
**纵向距离平方的平均值**最小（等价于让均方根误差 RMSE 最小）。{numref}`fig:08-verticalDistToMin` 用线段画出了
这些纵向距离。最后，要评估简单线性回归模型的预测
准确率，我们用 RMSPE（均方根预测误差，root mean squared prediction error）——也就是 k 近邻回归中用过的
同一个衡量预测性能的指标。

```{code-cell} ipython3
:tags: [remove-cell]

small_sacramento_pred = small_sacramento
# get prediction
small_sacramento_pred = small_sacramento_pred.assign(
    predicted=lm.predict(small_sacramento[["sqft"]])
)
# melt the dataframe to create separate df to create lines
small_sacramento_pred = small_sacramento_pred[["sqft", "price", "predicted"]].melt(
    id_vars=["sqft"]
)

v_lines = []
for i in range(len(small_sacramento)):
    sqft_val = small_sacramento.iloc[i]["sqft"]
    line_df = small_sacramento_pred.query("sqft == @sqft_val")
    v_lines.append(alt.Chart(line_df).mark_line(color="black").encode(x="sqft", y="value"))

error_plot = alt.layer(*v_lines, small_plot).configure_circle(opacity=1)
error_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-verticalDistToMin", error_plot)
```

:::{glue:figure} fig:08-verticalDistToMin
:name: fig:08-verticalDistToMin

售价与面积的散点图，图中用线段表示预测值与观测数据点之间的纵向距离。
:::

+++

## 用 Python 做线性回归

+++

```{index} scikit-learn
```

在 Python 中，我们可以用 `scikit-learn` 做简单线性回归，做法与 k 近邻回归非常相似。
区别在于，我们不创建 `KNeighborsRegressor` 模型对象，
而是使用 `LinearRegression` 模型对象；
和平时一样，先要从 `sklearn` 把它导入进来。
另一个区别是，线性回归不需要选择 $K$，因此也不需要做交叉验证。
下面演示如何用常见的 `scikit-learn` 工作流，根据房屋面积预测房屋
售价。我们在完整的萨克拉门托房地产数据集上使用简单线性回归方法。

```{index} 种子; numpy.random.seed
```

和平时一样，我们先加载包、设置种子、读取数据，并把一部分测试数据
放进保险箱，等选定最终模型后再回来取用。我们现在就来
处理这些。

```{code-cell} ipython3
import numpy as np
import altair as alt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")

np.random.seed(1)

sacramento = pd.read_csv("data/sacramento.csv")

sacramento_train, sacramento_test = train_test_split(
    sacramento, train_size=0.75
)
```

有了训练数据，接下来我们创建并拟合线性回归模型对象。
我们还会用 `coef_[0]` 属性取出直线的斜率，
用 `intercept_` 属性取出直线的截距。

```{index} scikit-learn; 拟合
```

```{code-cell} ipython3
# fit the linear regression model
lm = LinearRegression()
lm.fit(
   sacramento_train[["sqft"]],  # A single-column data frame
   sacramento_train["price"]  # A series
)

# make a dataframe containing slope and intercept coefficients
pd.DataFrame({"slope": [lm.coef_[0]], "intercept": [lm.intercept_]})
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("train_lm_slope", "{:0.0f}".format(lm.coef_[0]))
glue("train_lm_intercept", "{:0.0f}".format(lm.intercept_))
glue("train_lm_slope_f", "{0:,.0f}".format(lm.coef_[0]))
glue("train_lm_intercept_f", "{0:,.0f}".format(lm.intercept_))
```

```{index} 标准化
```

```{note}
你还会注意到另一个区别：我们没有对预测变量做标准化（也就是缩放并中心化）。
回忆一下，在 k 近邻模型中，拟合结果会随事先是否标准化而变化。在线性回归中，
标准化不影响拟合结果（但它*确实*会影响方程中的系数！）。所以你想标准化也可以——不会有什么坏处——
但如果让预测变量保持原来的形式，最优拟合系数通常在事后更容易解释。
```
