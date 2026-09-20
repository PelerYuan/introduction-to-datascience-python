+++

可以看到，含两个预测变量的线性回归给出的预测构成一个平坦的平面。这是线性回归的标志性特征，与
k 近邻回归等其他方法得到的起伏、灵活的曲面并不相同。如前所述，这一点在某一方面有优势：对每个
预测变量，我们都能从线性回归中得到斜率与截距，从而用数学方式描述这个平面。我们可以从模型对象的
`coef_` 属性中取出这些斜率值，从 `intercept_` 属性中取出截距，如下所示。

```{code-cell} ipython3
mlm.coef_
```

```{code-cell} ipython3
mlm.intercept_
```

当预测变量不止一个时，并不容易看出 `mlm.coef_` 中哪个系数对应哪个变量。特别是，你会看到上面的
`mlm.coef_` 只是一个数值数组，没有任何变量名。遗憾的是，这种对应关系只能由你自己理清：
`mlm.coef_` 中系数的排列顺序与你训练时所用预测变量数据框的列顺序*完全一致*。由于训练时我们用的是
`sacramento_train[["sqft", "beds"]]`，因此 `mlm.coef_[0]` 对应 `sqft`，`mlm.coef_[1]`
对应 `beds`。理清对应关系之后，你就可以用这些斜率写出一个数学方程来描述这个预测平面：

```{index} 平面方程
```



$$\text{house sale price} = \beta_0 + \beta_1\cdot(\text{house size}) + \beta_2\cdot(\text{number of bedrooms}),$$
其中：

- $\beta_0$ 是超平面的*纵截距*（房屋面积与卧室数都为 0 时的价格）
- $\beta_1$ 是第一个预测变量的*斜率*（房屋面积增加时价格上升的速度）
- $\beta_2$ 是第二个预测变量的*斜率*（卧室数增加时价格上升的速度）

最后，我们可以把上面模型输出中 $\beta_0$、$\beta_1$ 和 $\beta_2$ 的取值填进去，
写出数据的最优拟合平面方程：

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

这个模型比多元 k 近邻回归模型更容易解释：我们可以写出一个数学方程，说明每个预测变量如何影响
预测结果。但一如既往，我们还应该追问：与简单线性回归、多元 k 近邻回归等其他工具相比，
多元线性回归的表现究竟如何。如果这种比较属于模型调优过程的一部分——例如，我们正在为多元线性
回归和 k 近邻回归尝试许多不同的预测变量组合——那就必须只用训练数据，通过交叉验证来完成
比较。但如果已经确定了少数几个（例如 2 个或 3 个）调优后的候选模型，只想做最终比较，
那就可以直接比较各方法在测试数据上的预测误差。

```{code-cell} ipython3
lm_mult_test_RMSPE
```

```{index} RMSPE
```

多元线性回归模型得到的 RMSPE 为 \${glue:text}`sacr_mult_RMSPE`。这个预测误差小于多元 k 近邻
回归模型的预测误差，说明在这个数据集上预测房屋售价时，我们很可能应当选择线性回归。回顾本章
前面只含一个预测变量的简单线性回归模型，其 RMSPE 为 \${glue:text}`sacr_RMSPE`，
略高于我们这个更复杂的模型。含两个预测变量的模型在测试数据上的拟合效果略好于只含一个预测变量的
模型。如前所述，情况并非总是如此：有时纳入更多预测变量反而会损害模型在未见过的测试数据上的
预测性能。

+++

## 多重共线性与离群值

做（可能是多元的）线性回归时，哪些地方会出问题？本节将介绍两个常见问题——*离群值*与
*共线预测变量*——并说明它们对预测的影响。

+++

### 离群值

```{index} 离群值
```

离群值是不遵循其余数据常规模式的数据点。在线性回归中，它指的是到最优拟合直线的纵向距离
比根据其余数据所能预期的要大得多或小得多的点。离群值的问题在于，它们可能对最优拟合直线
产生*过大的影响*。一般来说，如果不借助超出本书范围的高级技术，很难准确判断哪些数据属于
离群值。

不过，为了说明出现离群值时会发生什么，{numref}`fig:08-lm-outlier` 再次展示了一小部分
萨克拉门托住房数据，只是我们额外加入了*一个*数据点（用红色标出）。这套房子面积为
5000 平方英尺，售价却只有 \$50,000。数据分析师并不知道，这套房子是家长以极不合理的低价
卖给子女的。当然，它并不能代表其余数据点所反映的真实住房市场价值；这个数据点就是一个
*离群值*。橙色画的是原来的最优拟合直线，红色画的是把离群值包含在内的新最优拟合直线。
可以看到红线与橙线相差很大，而这完全是由那一个额外加入的离群数据点造成的。

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

好在只要数据量足够，加入一两个离群值——只要它们的取值不*太*极端——通常不会对最优拟合直线
造成很大影响。{numref}`fig:08-lm-outlier-2` 展示了在完整的萨克拉门托原始训练数据上，前面那个
离群数据点会如何影响最优拟合直线。可以看到，数据集更大时，加入离群值后直线发生的变化小得多。
尽管如此，使用线性回归时仍然要批判性地思考：单个数据点对模型的影响究竟有多大。

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

第二个问题更隐蔽，出现在做多元线性回归的时候。具体来说，如果你纳入的多个预测变量彼此之间
高度线性相关，那么描述最优拟合平面的系数就会非常不可靠——数据上的微小改动就可能让系数
发生很大变化。来看一个极端的例子：在萨克拉门托住房数据中，同一套房子由两个人各测量了一次。
由于两个人都略有误差，两次测量结果未必完全一致，但它们彼此高度线性相关，
如 {numref}`fig:08-lm-multicol` 所示。

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

如果我们再次在这份数据上拟合多元线性回归模型，那么最优拟合平面的回归系数对数据的确切取值
非常敏感。例如，只要把数据稍作改动——比如运行交叉验证，它会将数据随机切分成若干个不同的
等份——系数就会出现大幅变化：

最优拟合 1：$\text{house sale price} =$ {glue:text}`icept1` $+$ {glue:text}`sqft1` $\cdot (\text{house size 1}$ $(\text{ft}^2)) +$ {glue:text}`sqft11` $\cdot (\text{house size 2}$ $(\text{ft}^2)).$

最优拟合 2：$\text{house sale price} =$ {glue:text}`icept2` $+$ {glue:text}`sqft2` $\cdot (\text{house size 1}$ $(\text{ft}^2)) +$ {glue:text}`sqft22` $\cdot (\text{house size 2}$ $(\text{ft}^2)).$

最优拟合 3：$\text{house sale price} =$ {glue:text}`icept3` $+$ {glue:text}`sqft3` $\cdot (\text{house size 1}$ $(\text{ft}^2)) +$ {glue:text}`sqft33` $\cdot (\text{house size 2}$ $(\text{ft}^2)).$

因此，做多元线性回归时，重要的是避免纳入高度线性相关的预测变量。不过，具体做法超出了本书的
范围；你可以查看本章末尾的拓展资源列表，了解可以去哪里深入学习。

+++

## 设计新的预测变量

在最初的探索中，我们相当幸运，找到了一个预测变量（房屋面积），它似乎与响应变量（售价）之间
存在有意义、且近乎线性的关系。但如果一时找不到这么好的变量，又该怎么办呢？有时事实就是如此：
数据中的变量与响应变量之间的关系不够强，无法给出有用的预测。例如，如果唯一可用的预测变量是
“现任房主最喜欢的冰淇淋口味”，那么用它来预测房屋售价大概没什么希望（除非将来在住房市场与
房主冰淇淋偏好之间的关系上出现惊人的科学发现）。遇到这类情况，唯一的办法就是获取更有用
变量的测量值。

不过，在很多情况下，预测变量与响应变量之间确实存在有意义的关系，只是这种关系不符合你所选
回归方法的假设。例如，数据框 `df` 有两个变量 `x` 和 `y`，二者之间的关系是非线性的，
简单线性回归无法完整刻画，如 {numref}`fig:08-predictor-design` 所示。

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

与其直接用 `x` 上的线性回归来预测响应 `y`，我们可能掌握了一些关于该问题的科学背景，
提示 `y` 应当是 `x` 的三次函数。于是在做回归之前，我们可以*创建一个新的预测变量* `z`：

```{code-cell} ipython3
df["z"] = df["x"] ** 3
```

然后就可以用预测变量 `z` 对 `y` 做线性回归，如 {numref}`fig:08-predictor-design-2` 所示。
可以看到，变换后的预测变量 `z` 能帮助线性回归模型给出更准确的预测。请注意，
{numref}`fig:08-predictor-design` 与 {numref}`fig:08-predictor-design-2` 之间，`y` 的响应取值
一个都没有改变；唯一的变化是 `x` 的取值被替换成了 `z` 的取值。

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
