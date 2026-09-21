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
到目前为止，我们解决所有预测性问题——无论是分类还是回归——用的都是基于 k 近邻（K-NN）的方法。在回归问题中，还有一种常用方法，叫作*线性回归*。本章介绍线性回归的基本概念，演示如何用 `scikit-learn` 在 Python 中做线性回归，并说明它与 k 近邻回归相比有哪些长处和不足。和往常一样，重点放在只有一个预测变量和一个响应变量的情形；不过本章最后会用一个*多元线性回归（multivariable linear regression）*的例子，说明预测变量不止一个时该怎么办。

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

上一章末尾，我们提到 k 近邻回归的一些局限。这种方法虽然简单易懂，但在训练数据的预测变量取值范围之外预测效果不佳，而且随着训练数据集变大，速度会明显变慢。好在 k 近邻回归有一个替代方案——*线性回归*——恰好能解决这两个局限。线性回归在实际中也十分常用，因为它给出一个可解释的数学方程，描述预测变量与响应变量之间的关系。本章前半部分讲*简单*线性回归，其中只涉及一个预测变量和一个响应变量；后面我们会讨论*多元*线性回归，其中涉及多个预测变量。和 k 近邻回归一样，简单线性回归预测的也是数值型响应变量（比如赛跑时间、房屋价格或身高）；但它*如何*对新观测作出预测，与 k 近邻回归很不一样。简单线性回归不是找出最近的 K 个近邻、对它们的取值求平均来得到预测，而是穿过训练数据画一条最优拟合直线，再在这条直线上“查”出预测值。

+++

```{index} 回归; 逻辑回归
```

```{note}
虽然前面的章节没有涉及，分类还有一种常用的方法，叫作*逻辑回归*（它用于分类，尽管名字里带着“回归”二字，这多少有些让人困惑）。在逻辑回归中——和线性回归类似——你先把模型“拟合”到训练数据上，再为每个新观测“查”出预测值。逻辑回归与 K-NN 分类之间的优势与不足对比，和线性回归与 k 近邻回归之间的对比类似。在学习逻辑回归之前，先较好地理解线性回归会很有帮助。读完本章后，如果想进一步了解逻辑回归，可以看分类各章末尾的“拓展资源”一节。
```

+++

```{index} 萨克拉门托房地产, 问题; 回归
```

我们回到{numref}`第 %s 章 <regression1>`中的萨克拉门托住房数据，学习如何应用线性回归，并把它与
k 近邻回归作比较。这里先用住房数据的一个较小版本，以便把可视化结果看清楚。回忆一下我们的预测性问题：能否用加利福尼亚州萨克拉门托地区的房屋面积来预测它的售价？特别是，回想我们碰到过一栋 2,000 平方英尺的新房，想把它买下来，而广告标价是
\$350,000。我们该按标价出价吗？这个价格是偏高还是偏低？要用简单线性回归回答这个问题，我们就用手上的数据，穿过已有的数据点画出最优拟合直线。数据的小子集以及最优拟合直线如{numref}`fig:08-lin-reg1` 所示。

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

因此，用数据找出最优拟合直线，等价于找出*参数化*（即与之对应）这条最优拟合直线的系数
$\beta_0$ 和 $\beta_1$。当然，在这个具体问题里，0 平方英尺的房子这个想法有点荒唐；但你可以把这里的 $\beta_0$ 看作“基础价”，把
$\beta_1$ 看作每平方英尺面积带来的价格增量。我们把这个想法再推得远一点：如果去算一栋 *600 万*平方英尺的房子的价格，直线的方程会怎样？那*负* 2,000 平方英尺又怎样？结果是，公式本身不会出任何问题；只要你去问，线性回归会很乐意对荒唐的预测变量取值作出预测。但即使你*可以*作出这些不着边际的预测，也不该这么做。你只应把预测限制在原始数据的大致范围内，只有在确实说得通时，才可以稍微超出一点。例如，{numref}`fig:08-lin-reg1` 中的数据低端只到大约 600 平方英尺，但用线性回归模型预测 500 平方英尺的价格，大概还是合理的。

回到例子！有了系数 $\beta_0$ 和 $\beta_1$，我们就可以用上面的方程，代入预测变量的取值——这里是 2,000 平方英尺——算出预测售价。{numref}`fig:08-lin-reg2` 展示了这个过程。

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
\${glue:text}`pred_2000`。不过等一下……简单线性回归究竟是怎样选出最优拟合直线的呢？穿过这些数据点可以画出许多条不同的直线。几个看似合理的例子如{numref}`fig:08-several-lines` 所示。

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

简单线性回归选出最优拟合直线的方式，是选出这样一条直线：它到训练数据中每个观测数据点的**纵向距离平方的平均值**最小（等价于让均方根误差（RMSE）最小）。{numref}`fig:08-verticalDistToMin` 用线段画出了这些纵向距离。最后，要评估简单线性回归模型的预测准确程度，我们用均方根预测误差（root mean squared prediction error，RMSPE）——也就是 k 近邻回归中用过的同一个衡量预测性能的指标。

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

在 Python 中，我们可以用 `scikit-learn` 做简单线性回归，做法与 k 近邻回归非常相似。区别在于，我们不创建 `KNeighborsRegressor` 模型对象，而是使用 `LinearRegression` 模型对象；和平时一样，先要从 `sklearn` 把它导入进来。另一个区别是，线性回归不需要选择 $K$，因此也不需要做交叉验证。下面演示如何用常见的 `scikit-learn` 工作流，根据房屋面积预测房屋售价。我们在完整的萨克拉门托房地产数据集上使用简单线性回归方法。

```{index} 种子; numpy.random.seed
```

和平时一样，我们先加载包、设置种子、读取数据，并把一部分测试数据放进保险箱，等选定最终模型后再回来取用。我们现在就来处理这些事。

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

有了训练数据，接下来我们创建并拟合线性回归模型对象。我们还会用 `coef_[0]` 属性取出直线的斜率，用 `intercept_` 属性取出直线的截距。

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
你还会注意到另一个区别：我们没有对预测变量做标准化（也就是缩放并中心化）。回忆一下，在 k 近邻模型中，拟合结果会随事先是否标准化而变化。在线性回归中，标准化不影响拟合结果（但它*确实*会影响方程中的系数！）。所以你想标准化也可以——不会有什么坏处——但如果让预测变量保持原来的形式，最优拟合系数通常在事后更容易解释。
```

+++

我们的系数为：（截距）$\beta_0=$ {glue:text}`train_lm_intercept`，（斜率）$\beta_1=$ {glue:text}`train_lm_slope`。这意味着最优拟合直线的方程为：

$\text{house sale price} =$ {glue:text}`train_lm_intercept` $+$ {glue:text}`train_lm_slope` $\cdot (\text{house size}).$

换句话说，模型预测：面积为 0 平方英尺的房屋起价为 \${glue:text}`train_lm_intercept_f`，而每增加一平方英尺，房屋价格就提高 \${glue:text}`train_lm_slope_f`。最后，我们在测试数据集上做预测，评估模型的表现如何。

```{code-cell} ipython3
# make predictions
sacramento_test["predicted"] = lm.predict(sacramento_test[["sqft"]])

# calculate RMSPE
RMSPE = mean_squared_error(
    y_true=sacramento_test["price"],
    y_pred=sacramento_test["predicted"]
)**(1/2)

RMSPE
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("sacr_RMSPE", "{0:,.0f}".format(RMSPE))
```

```{index} RMSPE
```

用 RMSPE 评估，我们最终模型的测试误差为 \${glue:text}`sacr_RMSPE`。请记住，这个误差的单位就是响应变量的单位，在这里是美元（USD）。这是否说明，我们的模型根据房屋面积这个预测变量来预测房屋售价就算得上“好”？同样，这个问题依旧不好回答，需要知道你打算如何使用这个预测结果。

为了可视化简单线性回归模型，我们可以画出所有可能遇到的房屋面积下房屋售价的预测值。由于模型是线性的，我们只需算出最小和最大房屋面积对应的预测价格，再用一条直线把这两个点连起来。我们把这条预测直线叠加到原始房价数据的散点图上，这样就可以定性地判断模型是否很好地拟合了数据。{numref}`fig:08-lm-predict-all` 展示了结果。

```{code-cell} ipython3
:tags: [remove-output]
sqft_prediction_grid = sacramento[["sqft"]].agg(["min", "max"])
sqft_prediction_grid["predicted"] = lm.predict(sqft_prediction_grid)

all_points = alt.Chart(sacramento).mark_circle().encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .scale(zero=False)
        .title("Price (USD)")
)

sacr_preds_plot = all_points + alt.Chart(sqft_prediction_grid).mark_line(
    color="#ff7f0e"
).encode(
    x="sqft",
    y="predicted"
)

sacr_preds_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-lm-predict-all", sacr_preds_plot)
```

:::{glue:figure} fig:08-lm-predict-all
:name: fig:08-lm-predict-all

萨克拉门托完整住房数据的售价与面积散点图，并叠加最优拟合直线。
:::

## 简单线性回归与 k 近邻回归的比较

```{index} 回归; 方法的比较
```

现在我们已经对简单线性回归和 k 近邻回归有了大致了解，就可以开始比较这两种方法以及它们做出的预测，并讨论其异同。首先，我们来看看萨克拉门托房地产数据上简单线性回归模型的预测可视化（用房屋面积预测价格），以及由同一个问题得到的“最佳”k 近邻回归模型，结果见{numref}`fig:08-compareRegression`。

```{code-cell} ipython3
:tags: [remove-cell]
from sklearn.model_selection import GridSearchCV
from sklearn.compose import make_column_transformer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# preprocess the data, make the pipeline
sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft"]))
sacr_pipeline_knn = make_pipeline(
    sacr_preprocessor, KNeighborsRegressor(n_neighbors=55)
)  # 55 is the best parameter obtained through cross validation in regression1 chapter

sacr_pipeline_knn.fit(sacramento_train[["sqft"]], sacramento_train[["price"]])

# knn in-sample predictions (on training split)
sacr_preds_knn = sacramento_train
sacr_preds_knn = sacr_preds_knn.assign(
    knn_predicted=sacr_pipeline_knn.predict(sacramento_train)
)

# knn out-of-sample predictions (on test split)
sacr_preds_knn_test = sacramento_test
sacr_preds_knn_test = sacr_preds_knn_test.assign(
    knn_predicted=sacr_pipeline_knn.predict(sacramento_test)
)

sacr_rmspe_knn = np.sqrt(
    mean_squared_error(
        y_true=sacr_preds_knn_test["price"], y_pred=sacr_preds_knn_test["knn_predicted"]
    )
)

# plot knn in-sample predictions overlaid on scatter plot
knn_plot_final = (
    alt.Chart(sacr_preds_knn, title="K-NN regression")
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size (square feet)", scale=alt.Scale(zero=False)),
        y=alt.Y(
            "price",
            title="Price (USD)",
            axis=alt.Axis(format="$,.0f"),
            scale=alt.Scale(zero=False),
        ),
    )
)

knn_plot_final = (
    knn_plot_final
    + knn_plot_final.mark_line(color="#ff7f0e").encode(x="sqft", y="knn_predicted")
    + alt.Chart(  # add the text
        pd.DataFrame(
            {
                "x": [3500],
                "y": [100000],
                "rmspe": [f"RMSPE = {round(sacr_rmspe_knn)}"],
            }
        )
    )
    .mark_text(dy=-5, size=15)
    .encode(x="x", y="y", text="rmspe")
)


# add more components to lm_plot_final
lm_plot_final = (
    alt.Chart(sacramento_train, title="linear regression")
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size (square feet)", scale=alt.Scale(zero=False)),
        y=alt.Y(
            "price",
            title="Price (USD)",
            axis=alt.Axis(format="$,.0f"),
            scale=alt.Scale(zero=False),
        ),
    )
)

lm_plot_final = (
    lm_plot_final
    + lm_plot_final.transform_regression("sqft", "price").mark_line(color="#ff7f0e")
    + alt.Chart(  # add the text
        pd.DataFrame(
            {
                "x": [3500],
                "y": [100000],
                "rmspe": [f"RMSPE = {round(RMSPE)}"],
            }
        )
    )
    .mark_text(dy=-5, size=15)
    .encode(x="x", y="y", text="rmspe")
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-compareRegression", (lm_plot_final | knn_plot_final))
```

:::{glue:figure} fig:08-compareRegression
:name: fig:08-compareRegression

简单线性回归与 k 近邻回归的比较。
:::

+++

在{numref}`fig:08-compareRegression` 中，我们看到了哪些差异？一个明显的差异是两条橙色线的形状。在简单线性回归中，我们只能得到一条直线；而在 k 近邻回归中，拟合线灵活得多，可以相当曲折。不过，把模型限制为直线，有一个很大的可解释性优势。一条直线只需两个数字就能确定：纵截距和斜率。截距告诉我们，所有预测变量都等于 0 时的预测值是多少；斜率告诉我们，预测变量每增加一个单位，响应变量预计会增加多少。k 近邻回归虽然实现和理解起来都很简单，但它的曲折拟合线并不具备这种可解释性。

```{index} 欠拟合; 回归
```

不过，有时使用简单线性回归模型也会有劣势，尤其是响应变量与预测变量之间的关系并非线性，而是呈其他形状（例如弯曲或振荡）时。这种情况下，简单线性回归给出的预测模型会欠拟合，也就是说模型的预测值与实际的观测值吻合得不太好。这样的模型在训练数据上评估拟合优度时，RMSE 可能相当高；而在测试数据集上评估预测质量时，RMSPE 也会相当高。在这样的数据集上，k 近邻回归的表现可能更好。此外，后续教材中还会介绍其他类型的回归，它们甚至可能在预测这类数据时做得更好。

这两个模型在萨克拉门托房价数据集上表现如何？在{numref}`fig:08-compareRegression` 中，我们还打印了 RMSPE，它是在未参与训练/拟合模型的测试数据集上做预测算出来的。简单线性回归模型的 RMSPE 略低于 k 近邻回归模型的 RMSPE。考虑到简单线性回归模型的可解释性也更好，如果要在实践中比较两者，我们多半会选择简单线性回归模型。

```{index} 外推
```

最后，请注意，k 近邻回归模型在数据左右两侧的边界处会变得“平坦”，而线性模型预测的斜率始终不变。在观测数据的取值范围之外做预测称为*外推*（extrapolation）；k 近邻与线性模型在外推时的表现差别很大。平坦的趋势和恒定斜率的趋势哪一种更合理，取决于具体应用。例如，如果房价数据稍有不同，线性模型实际上可能对一套小房子预测出*负的*价格（截距 $\beta_0$ 为负时就会如此），这显然不符合现实。另一方面，房屋面积越大、房价越高这一趋势，对大房子很可能依然成立，因此 k 近邻的“平坦”外推多半也不符合现实。

+++

## 多元线性回归

+++

```{index} 回归; 多元线性, 回归; 多元线性方程
```

```{index} see: 多元线性方程; 平面方程
```

与 k 近邻分类和 k 近邻回归一样，我们可以从只有一个预测变量的简单情形，扩展到含有多个预测变量的情形，即*多元线性回归*。做法与 k 近邻回归非常相似：只需在指定训练数据时加入更多预测变量。但请回想，线性回归既不需要用交叉验证来选参数，也不需要对数据做标准化（即中心化和缩放）。还要再次注意，多个预测变量会带来同样的顾虑，这与多元 k 近邻回归和分类中的情形一样：预测变量更多**并非**总是更好。不过，{numref}`第 %s 章 <classification2>`中的预测变量选择算法同样适用于线性回归，因此本章不再重复介绍。

```{index} 萨克拉门托房地产
```

我们将用萨克拉门托房地产数据演示多元线性回归，预测变量同时取房屋面积（以平方英尺计）和卧室数量，响应变量仍然取房屋售价。用 `scikit-learn` 框架做这件事很容易：只需把 `sqft` 和 `beds` 两个变量设为预测变量，然后照常调用 `fit` 方法即可。

```{code-cell} ipython3

mlm = LinearRegression()
mlm.fit(
    sacramento_train[["sqft", "beds"]],
    sacramento_train["price"]
)
```
最后，我们在测试数据集上做预测，评估模型的质量。

```{index} scikit-learn;predict, scikit-learn;mean_squared_error
```
```{index} see: mean_squared_error;scikit-learn
```
```{index} see: predict;scikit-learn
```

```{code-cell} ipython3
sacramento_test["predicted"] = mlm.predict(sacramento_test[["sqft","beds"]])

lm_mult_test_RMSPE = mean_squared_error(
    y_true=sacramento_test["price"],
    y_pred=sacramento_test["predicted"]
)**(1/2)
lm_mult_test_RMSPE
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("sacr_mult_RMSPE", "{0:,.0f}".format(lm_mult_test_RMSPE))
```

用 RMSPE 评估，我们模型的测试误差为 \${glue:text}`sacr_mult_RMSPE`。预测变量有两个时，我们可以把线性回归给出的预测结果画出来，它构成一个*最优拟合平面*，如{numref}`fig:08-3DlinReg` 所示。

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
mlmPredGrid = mlm.predict(xygrid)

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
        z=mlmPredGrid.reshape(50, -1),
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
    glue("fig:08-3DlinReg", Image("img/regression2/plot3d_linear_regression.png"))
else:
    glue("fig:08-3DlinReg", fig)
```

```{figure} data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
:name: fig:08-3DlinReg
:figclass: caption-hack

线性回归的最优拟合平面，叠加在数据之上（以价格、房屋面积和卧室数量作为预测变量）。请注意，我们一般不建议使用 3D 可视化；这里使用 3D 可视化，只是为了教学目的展示回归平面的样子。
```

+++

可以看到，含两个预测变量的线性回归给出的预测构成一个平坦的平面。这是线性回归的标志性特征，与
k 近邻回归等其他方法得到的起伏、灵活的曲面并不相同。如前所述，这一点在某一方面有优势：对每个预测变量，我们都能从线性回归中得到斜率与截距，从而用数学方式描述这个平面。我们可以从模型对象的
`coef_` 属性中取出这些斜率值，从 `intercept_` 属性中取出截距，如下所示。

```{code-cell} ipython3
mlm.coef_
```

```{code-cell} ipython3
mlm.intercept_
```

当预测变量不止一个时，并不容易看出 `mlm.coef_` 中哪个系数对应哪个变量。特别是，你会看到上面的
`mlm.coef_` 只是一个数值数组，没有任何变量名。遗憾的是，这种对应关系只能由你自己理清：`mlm.coef_` 中系数的排列顺序与你训练时所用预测变量数据框的列顺序*完全一致*。由于训练时我们用的是
`sacramento_train[["sqft", "beds"]]`，因此 `mlm.coef_[0]` 对应 `sqft`，`mlm.coef_[1]`
对应 `beds`。理清对应关系之后，你就可以用这些斜率写出一个数学方程来描述这个预测平面：

```{index} 平面方程
```



$$\text{house sale price} = \beta_0 + \beta_1\cdot(\text{house size}) + \beta_2\cdot(\text{number of bedrooms}),$$
其中：

- $\beta_0$ 是超平面的*纵截距*（房屋面积与卧室数都为 0 时的价格）
- $\beta_1$ 是第一个预测变量的*斜率*（房屋面积增加时价格上升的速度）
- $\beta_2$ 是第二个预测变量的*斜率*（卧室数增加时价格上升的速度）

最后，我们可以把上面模型输出中 $\beta_0$、$\beta_1$ 和 $\beta_2$ 的取值填进去，写出数据的最优拟合平面方程：

```{code-cell} ipython3
:tags: [remove-cell]

icept = "{0:,.0f}".format(mlm.intercept_)
sqftc = "{0:,.0f}".format(mlm.coef_[0])
bedsc = "{0:,.0f}".format(mlm.coef_[1])
glue("icept", icept)
glue("sqftc", sqftc)
glue("bedsc", bedsc)
```

$\text{house sale price} =$ {glue:text}`icept` $+$ {glue:text}`sqftc` $\cdot (\text{house size})$ {glue:text}`bedsc` $\cdot (\text{number of bedrooms})$

这个模型比多元 k 近邻回归模型更容易解释：我们可以写出一个数学方程，说明每个预测变量如何影响预测结果。但一如既往，我们还应该追问：与简单线性回归、多元 k 近邻回归等其他工具相比，多元线性回归的表现究竟如何。如果这种比较属于模型调优过程的一部分——例如，我们正在为多元线性回归和 k 近邻回归尝试许多不同的预测变量组合——那就必须只用训练数据，通过交叉验证来完成比较。但如果已经确定了少数几个（例如 2 个或 3 个）调优后的候选模型，只想做最终比较，那就可以直接比较各方法在测试数据上的预测误差。

```{code-cell} ipython3
lm_mult_test_RMSPE
```

```{index} RMSPE
```

多元线性回归模型得到的 RMSPE 为 \${glue:text}`sacr_mult_RMSPE`。这个预测误差小于多元 k 近邻回归模型的预测误差，说明在这个数据集上预测房屋售价时，我们很可能应当选择线性回归。回顾本章前面只含一个预测变量的简单线性回归模型，其 RMSPE 为 \${glue:text}`sacr_RMSPE`，略高于我们这个更复杂的模型。含两个预测变量的模型在测试数据上的拟合效果略好于只含一个预测变量的模型。如前所述，情况并非总是如此：有时纳入更多预测变量反而会损害模型在未见过的测试数据上的预测性能。

+++

## 多重共线性与离群值

做（可能是多元的）线性回归时，哪些地方会出问题？本节将介绍两个常见问题——*离群值*与*共线预测变量*——并说明它们对预测的影响。

+++

### 离群值

```{index} 离群值
```

离群值是不遵循其余数据常规模式的数据点。在线性回归中，离群值指的是到最优拟合直线的纵向距离比根据其余数据所能预期的要大得多或小得多的点。离群值的问题在于，它们可能对最优拟合直线产生*过大的影响*。一般来说，如果不借助超出本书范围的高级技术，很难准确判断哪些数据属于离群值。

不过，为了说明出现离群值时会发生什么，{numref}`fig:08-lm-outlier` 再次展示了一小部分萨克拉门托住房数据，只是我们额外加入了*一个*数据点（用红色标出）。这套房子面积为 5,000 平方英尺，售价却只有 \$50,000。数据分析师并不知道，这套房子是家长以极不合理的低价卖给子女的。当然，它并不能代表其余数据点所反映的真实住房市场价值；这个数据点就是一个*离群值*。橙色画的是原来的最优拟合直线，红色画的是把离群值包含在内的新最优拟合直线。可以看到红线与橙线相差很大，而这完全是由那一个额外加入的离群数据点造成的。

```{code-cell} ipython3
:tags: [remove-cell]

sacramento_train_small = sacramento_train.sample(100, random_state=2)
sacramento_outlier = pd.DataFrame({"sqft": [5000], "price": [50000]})
sacramento_concat_df = pd.concat((sacramento_train_small, sacramento_outlier))

lm_plot_outlier = (
    alt.Chart(sacramento_train_small)
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size (square feet)", scale=alt.Scale(zero=False)),
        y=alt.Y(
            "price",
            title="Price (USD)",
            axis=alt.Axis(format="$,.0f"),
            scale=alt.Scale(zero=False),
        ),
    )
)
lm_plot_outlier += lm_plot_outlier.transform_regression("sqft", "price").mark_line(
    color="#ff7f0e"
)

outlier_pt = (
    alt.Chart(sacramento_outlier)
    .mark_circle(color="#d62728", size=100)
    .encode(x="sqft", y="price")
)

outlier_line = (
    (
        alt.Chart(sacramento_concat_df)
        .mark_circle()
        .encode(
            x=alt.X(
                "sqft", title="House size (square feet)", scale=alt.Scale(zero=False)
            ),
            y=alt.Y(
                "price",
                title="Price (USD)",
                axis=alt.Axis(format="$,.0f"),
                scale=alt.Scale(zero=False),
            ),
        )
    )
    .transform_regression("sqft", "price")
    .mark_line(color="#d62728")
)

lm_plot_outlier += outlier_pt + outlier_line

glue("fig:08-lm-outlier", lm_plot_outlier)
```

:::{glue:figure} fig:08-lm-outlier
:name: fig:08-lm-outlier

数据子集的散点图，其中离群值用红色标出。
:::

+++

好在只要数据量足够，加入一两个离群值——只要它们的取值不*太*极端——通常不会对最优拟合直线造成很大影响。{numref}`fig:08-lm-outlier-2` 展示了在完整的萨克拉门托原始训练数据上，前面那个离群数据点会如何影响最优拟合直线。可以看到，数据集更大时，加入离群值后直线发生的变化小得多。尽管如此，使用线性回归时仍然要批判性地思考：单个数据点对模型的影响究竟有多大。

```{code-cell} ipython3
:tags: [remove-cell]

sacramento_concat_df = pd.concat((sacramento_train, sacramento_outlier))

lm_plot_outlier_large = (
    alt.Chart(sacramento_train)
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size (square feet)", scale=alt.Scale(zero=False)),
        y=alt.Y(
            "price",
            title="Price (USD)",
            axis=alt.Axis(format="$,.0f"),
            scale=alt.Scale(zero=False),
        ),
    )
)
lm_plot_outlier_large += lm_plot_outlier_large.transform_regression(
    "sqft", "price"
).mark_line(color="#ff7f0e")

outlier_line = (
    (
        alt.Chart(sacramento_concat_df)
        .mark_circle()
        .encode(
            x=alt.X(
                "sqft", title="House size (square feet)", scale=alt.Scale(zero=False)
            ),
            y=alt.Y(
                "price",
                title="Price (USD)",
                axis=alt.Axis(format="$,.0f"),
                scale=alt.Scale(zero=False),
            ),
        )
    )
    .transform_regression("sqft", "price")
    .mark_line(color="#d62728")
)

lm_plot_outlier_large += outlier_pt + outlier_line

glue("fig:08-lm-outlier-2", lm_plot_outlier_large)
```

:::{glue:figure} fig:08-lm-outlier-2
:name: fig:08-lm-outlier-2

完整数据的散点图，其中离群值用红色标出。
:::

+++

### 多重共线性

```{index} 多重共线性
```

第二个问题更隐蔽，做多元线性回归时就可能出现。具体来说，如果你纳入的多个预测变量彼此之间高度线性相关，那么描述最优拟合平面的系数就会非常不可靠——数据上的微小改动就可能让系数发生很大变化。来看一个极端的例子：在萨克拉门托住房数据中，同一套房子由两个人各测量了一次。由于两个人都略有误差，两次测量结果未必完全一致，但它们彼此高度线性相关，如{numref}`fig:08-lm-multicol` 所示。

```{code-cell} ipython3
:tags: [remove-cell]

np.random.seed(1)
sacramento_train = sacramento_train.assign(
    sqft1=sacramento_train["sqft"]
    + 100
    * np.random.choice(range(1000000), size=len(sacramento_train), replace=True)
    / 1000000
)
sacramento_train = sacramento_train.assign(
    sqft2=sacramento_train["sqft"]
    + 100
    * np.random.choice(range(1000000), size=len(sacramento_train), replace=True)
    / 1000000
)
sacramento_train = sacramento_train.assign(
    sqft3=sacramento_train["sqft"]
    + 100
    * np.random.choice(range(1000000), size=len(sacramento_train), replace=True)
    / 1000000
)
sacramento_train

lm_plot_multicol_1 = (
    alt.Chart(sacramento_train)
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size measurement 1 (square feet)"),
        y=alt.Y("sqft1", title="House size measurement 2 (square feet)"),
    )
)

glue("fig:08-lm-multicol", lm_plot_multicol_1)
```

:::{glue:figure} fig:08-lm-multicol
:name: fig:08-lm-multicol

第一个人测量的房屋面积（平方英尺）与第二个人测量的房屋面积（平方英尺）的散点图。
:::

```{code-cell} ipython3
:tags: [remove-cell]

# first LM
lm_fit1 = LinearRegression()
X_train = sacramento_train[["sqft", "sqft1"]]
y_train = sacramento_train[["price"]]

lm_fit1.fit(X_train, y_train)

icept1 = "{0:,.0f}".format(lm_fit1.intercept_[0])
sqft1 = "{0:,.0f}".format(lm_fit1.coef_[0][0])
sqft11 = "{0:,.0f}".format(lm_fit1.coef_[0][1])
glue("icept1", icept1)
glue("sqft1", sqft1)
glue("sqft11", sqft11)

# second LM
lm_fit2 = LinearRegression()
X_train = sacramento_train[["sqft", "sqft2"]]
y_train = sacramento_train[["price"]]

lm_fit2.fit(X_train, y_train)

icept2 = "{0:,.0f}".format(lm_fit2.intercept_[0])
sqft2 = "{0:,.0f}".format(lm_fit2.coef_[0][0])
sqft22 = "{0:,.0f}".format(lm_fit2.coef_[0][1])
glue("icept2", icept2)
glue("sqft2", sqft2)
glue("sqft22", sqft22)

# third LM
lm_fit3 = LinearRegression()
X_train = sacramento_train[["sqft", "sqft3"]]
y_train = sacramento_train[["price"]]

lm_fit3.fit(X_train, y_train)

icept3 = "{0:,.0f}".format(lm_fit3.intercept_[0])
sqft3 = "{0:,.0f}".format(lm_fit3.coef_[0][0])
sqft33 = "{0:,.0f}".format(lm_fit3.coef_[0][1])
glue("icept3", icept3)
glue("sqft3", sqft3)
glue("sqft33", sqft33)
```

如果我们再次在这份数据上拟合多元线性回归模型，那么最优拟合平面的回归系数对数据的确切取值非常敏感。例如，只要把数据稍作改动——比如运行交叉验证，它会将数据随机切分成若干个不同的等份——系数就会出现大幅变化：

最优拟合 1：$\text{house sale price} =$ {glue:text}`icept1` $+$ {glue:text}`sqft1` $\cdot (\text{house size 1}$ $(\text{ft}^2)) +$ {glue:text}`sqft11` $\cdot (\text{house size 2}$ $(\text{ft}^2)).$

最优拟合 2：$\text{house sale price} =$ {glue:text}`icept2` $+$ {glue:text}`sqft2` $\cdot (\text{house size 1}$ $(\text{ft}^2)) +$ {glue:text}`sqft22` $\cdot (\text{house size 2}$ $(\text{ft}^2)).$

最优拟合 3：$\text{house sale price} =$ {glue:text}`icept3` $+$ {glue:text}`sqft3` $\cdot (\text{house size 1}$ $(\text{ft}^2)) +$ {glue:text}`sqft33` $\cdot (\text{house size 2}$ $(\text{ft}^2)).$

因此，做多元线性回归时，重要的是避免纳入高度线性相关的预测变量。不过，具体做法超出了本书的范围；你可以查看本章末尾的拓展资源列表，了解可以去哪里深入学习。

+++

## 设计新的预测变量

在最初的探索中，我们相当幸运，找到了一个预测变量（房屋面积），它似乎与响应变量（售价）之间存在有意义且近乎线性的关系。但如果一时找不到这么好的变量，又该怎么办呢？有时事实就是如此：数据中的变量与响应变量之间的关系不够强，无法给出有用的预测。例如，如果唯一可用的预测变量是“现任房主最喜欢的冰淇淋口味”，那么用它来预测房屋售价大概没什么希望（除非将来在住房市场与房主冰淇淋偏好之间的关系上出现惊人的科学发现）。遇到这类情况，唯一的办法就是获取更有用变量的测量值。

不过，在很多情况下，预测变量与响应变量之间确实存在有意义的关系，只是这种关系不符合你所选回归方法的假设。例如，数据框 `df` 有两个变量 `x` 和 `y`，二者之间的关系是非线性的，简单线性回归无法完整刻画，如{numref}`fig:08-predictor-design` 所示。

```{code-cell} ipython3
:tags: [remove-cell]

np.random.seed(3)
df = pd.DataFrame({"x": np.random.choice(range(10000), size=100, replace=True) / 10000})
df = df.assign(
    y=df["x"] ** 3
    + 0.2 * np.random.choice(range(10000), size=100, replace=True) / 10000
    - 0.1
)
```

```{code-cell} ipython3
df
```

```{code-cell} ipython3
:tags: [remove-cell]

curve_plt = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x=alt.X("x", scale=alt.Scale(zero=False)),
        y=alt.Y(
            "y",
            scale=alt.Scale(zero=False),
        ),
    )
)


curve_plt += curve_plt.transform_regression("x", "y").mark_line(color="#ff7f0e")

glue("fig:08-predictor-design", curve_plt)
```

:::{glue:figure} fig:08-predictor-design
:name: fig:08-predictor-design

预测变量与响应变量之间呈非线性关系的数据集示例。
:::

+++

```{index} 预测变量设计
```

与其直接对 `x` 做线性回归来预测响应 `y`，我们可能掌握了一些关于该问题的科学背景，提示 `y` 应当是 `x` 的三次函数。于是在做回归之前，我们可以*创建一个新的预测变量* `z`：

```{code-cell} ipython3
df["z"] = df["x"] ** 3
```

然后就可以用预测变量 `z` 对 `y` 做线性回归，如{numref}`fig:08-predictor-design-2` 所示。可以看到，变换后的预测变量 `z` 能帮助线性回归模型给出更准确的预测。请注意，{numref}`fig:08-predictor-design` 与{numref}`fig:08-predictor-design-2` 之间，`y` 的响应取值没有发生任何变化；唯一的变化是把 `x` 的取值换成了 `z` 的取值。

```{code-cell} ipython3
:tags: [remove-cell]

curve_plt2 = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x=alt.X("z", title="z = x³" ,scale=alt.Scale(zero=False)),
        y=alt.Y(
            "y",
            scale=alt.Scale(zero=False),
        ),
    )
)


curve_plt2 += curve_plt2.transform_regression("z", "y").mark_line(color="#ff7f0e")

glue("fig:08-predictor-design-2", curve_plt2)
```

:::{glue:figure} fig:08-predictor-design-2
:name: fig:08-predictor-design-2

变换后的预测变量与响应变量之间的关系。
:::

+++

```{index} see: 特征工程; 预测变量设计
```

对预测变量做变换（过程中还可能把多个预测变量组合起来），这种做法称为*特征工程*（feature engineering）。在真实的数据分析问题中，你需要依靠对问题的深入理解——以及前面各章介绍的数据整理工具——来构造出有用的新特征，从而提升预测性能。

```{note}
特征工程*是模型调优的一部分*，因此绝不能用测试数据来评估你构造的特征的好坏。不过，你完全可以使用交叉验证！
```

+++

## 回归的另一面

到目前为止，本书只把回归用于预测。不过，回归也可以看成一种方法，用来理解和量化单个变量对我们所关心的响应变量有多大影响。在本章的房价案例中，除了用历史数据预测未来的成交价，我们可能还想描述房屋面积和卧室数量各自与房价的关系，量化这些关系分别有多强，并评估我们能把这种关系的大小估计得多准确。再进一步，我们可能还想弄清预测变量是否会*导致*价格的变化。回归的这些方面都远远超出本书的范围；不过，你在这里学到的内容会为你打下知识基础，让你日后阅读该主题更进阶的教材时受益良多。

+++

## 习题

本章内容的练习题可以在配套的[练习册仓库](https://worksheets.python.datasciencebook.ca)的“回归 II：线性回归（Regression II: linear regression）”一行中找到。你可以预览本章练习册（worksheet）的非交互版本，只需点击“查看练习册（view worksheet）”。如果要交互式地做习题，请按照练习册仓库中的说明下载所有练习册，并按照{numref}`第 %s 章 <move-to-your-own-machine>`中的计算机环境配置说明操作。这样就能确保练习册提供的自动反馈和指导按预期正常工作。



+++

## 拓展资源

- [`scikit-learn` 网站](https://scikit-learn.org/stable/)是查阅前两章各项函数与包的更多细节以及进阶用法时极好的参考资料。除此之外，网站还提供了许多实用的[教程](https://scikit-learn.org/stable/tutorial/index.html)和[一份内容丰富的进阶示例清单](https://scikit-learn.org/stable/auto_examples/index.html#general-examples)，你可以借助它们继续学习本书范围之外的内容。
- 《An Introduction to Statistical Learning》{cite:p}`james2013introduction` 是学习回归过程中极好的下一站。第 3 章讲解线性回归，数学程度比本书稍高，但跨度不算太大，可以作为一块很好的垫脚石。第 6 章讨论当数据集包含很多预测变量、而你预期其中只有少数几个真正有用时，如何选出“有信息量的”预测变量子集。第 7 章介绍的回归模型比线性回归模型更灵活，同时又保留了线性回归的计算效率。相比之下，我们前面讲过的 k 近邻方法确实更灵活，但数据量一大就会变得非常慢。

+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
