## 在测试集上评估

要评估模型在未见过的数据上预测得怎么样，我们来看它在测试数据上的 RMSPE。为此，首先要用 $K =$ {glue:text}`best_k_sacr` 个近邻在整个训练数据集上重新训练 K-NN 回归模型。正如我们在 {numref}`第 %s 章 <classification2>` 中所见，这一步不必自己手动完成，`scikit-learn` 会自动替我们做好。要用最佳模型在测试数据上做预测，我们可以调用已拟合的 `GridSearchCV` 对象的 `predict` 方法。接着用 `mean_squared_error` 函数（传入 `y_true` 和 `y_pred` 参数）计算均方预测误差，最后开平方得到 RMSPE。我们不直接使用 `score` 方法——如 {numref}`第 %s 章 <classification2>` 中那样——是因为 `KNeighborsRegressor` 模型默认使用的评分指标与 RMSPE 不同。

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

以 RMSPE 衡量，我们最终模型的测试误差为 \${glue:text}`test_RMSPE`。
请注意，RMSPE 的度量单位与响应变量相同。
换句话说，对于新观测，我们预计预测误差*大致*为 \${glue:text}`test_RMSPE`。
从一个角度看，这是好消息：这个值和调优后模型的交叉验证 RMSPE 估计值差不多
（该估计值为 \${glue:text}`cv_RMSPE`），
因此可以说，该模型看上去能很好地泛化到它从未见过的新数据。
不过，与 K-NN 分类的情形很像，这个 RMSPE 值算不算*好*——也就是说，
大约 \${glue:text}`test_RMSPE` 的误差是否可以接受——完全取决于具体应用。
在这个应用里，这个误差不算大得无法承受，但也绝不可忽略；
\${glue:text}`test_RMSPE`
可能占购房者预算的相当大一部分，甚至决定他们到底买不买得起、能不能给房子出价。

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

最终 K-NN 回归模型预测的房价（橙色线）。
:::

+++

## 多元 K-NN 回归

与 K-NN 分类一样，K-NN 回归也可以使用多个预测变量。此时预测变量的尺度会带来同样的顾虑。同样，做预测时要先找出与待预测的新点最接近的 $K$ 个观测；尺度大的变量所起的作用会远大于尺度小的变量。因此，我们应当重新定义流水线中的预处理器（preprocessor），把所有预测变量都纳入进来。

还要注意，K-NN 回归中预测变量的选择与 K-NN 分类有同样的顾虑：预测变量更多**并不**总是更好，而且选用哪些预测变量对预测质量可能有很大影响。好在 K-NN 回归同样可以使用 {numref}`第 %s 章 <classification2>` 中的预测变量选择算法。算法是同一个，本章不再重复介绍。

```{index} k 近邻; 多元回归, 萨克拉门托房地产市场
```

下面我们用 `scikit-learn` 对萨克拉门托房地产数据做一次多元 K-NN 回归分析。这一次，我们用房屋面积（以平方英尺计）和卧室数量作为预测变量，并继续用房屋售价作为我们要预测的响应变量。在开始建模之前先做探索性数据分析（例如把数据可视化），始终是良好实践。{numref}`fig:07-bedscatter` 表明，卧室数量也许能提供有助于预测房屋售价的有用信息。

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

{numref}`fig:07-bedscatter` 表明，卧室数量增加时，房屋售价往往也随之上升，但两者关系相当弱。把卧室数量加入模型，能否提高我们预测价格的能力？要回答这个问题，我们需要新建一个使用房屋面积和卧室数量的 K-NN 回归模型，再把它与之前只用房屋面积的模型比较。我们现在就动手！

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

这里我们看到，交叉验证给出的最小 RMSPE 估计值出现在 $K =$ {glue:text}`best_k_sacr_multi` 时。
如果要在*模型调优过程中*把这个多元 K-NN 回归模型与只有单个预测变量的模型作比较
（例如，像讲解分类模型评估与调优的那一章所述那样在做前向选择（forward selection）），
那就必须比较仅用训练数据通过交叉验证估计出的 RMSPE。
回头看，单预测变量模型的交叉验证 RMSPE 估计值为 \${glue:text}`cv_RMSPE`。
多元模型的交叉验证 RMSPE 估计值为 \${glue:text}`cv_RMSPE_2pred`。
因此在这个例子里，加入这个额外的预测变量并没有让模型提升多少。

不管怎样，我们继续分析，看看如何用多元 K-NN 回归模型做预测，并在测试数据上评估它的性能。和前面一样，我们用最佳模型对测试数据做预测，也就是调用已拟合的 `GridSearchCV` 对象的 `predict` 方法。最后，我们用 `mean_squared_error` 函数计算 RMSPE。

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

这一次，我们在同一个数据集上做 K-NN 回归，但把卧室数量也作为预测变量，得到的 RMSPE 测试误差为 \${glue:text}`RMSPE_mult`。
{numref}`fig:07-knn-mult-viz` 把模型的预测叠加在数据之上做了可视化。这次有 2 个预测变量而不是 1 个，所以预测不再是二维空间中的一条直线，而是三维空间中的一个曲面。

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

K-NN 回归模型的预测以三维空间中的曲面表示，叠加在使用三个预测变量（价格、房屋面积和卧室数量）的数据之上。一般我们并不推荐使用三维可视化；这里只是为了教学演示，才用三维可视化展示预测曲面是什么样子。
```

+++

可以看到，在有 2 个预测变量时，预测形成的是曲面而不是直线。新加入的预测变量（卧室数量）与价格有关（价格变化时，卧室数量也随之变化），并且不完全由房屋面积（我们的另一个预测变量）决定，因此它为我们做预测带来了额外而有用的信息。例如，在这个模型中，我们会预测面积为 2,500 平方英尺的房屋，其价格通常随卧室数量增加而略有上升。如果没有卧室数量这个额外的预测变量，我们对这两栋房子会给出相同的预测价格。

+++

## K-NN 回归的优势与局限

与 K-NN 分类（其实任何预测算法都是如此）一样，K-NN 回归既有优势也有不足。这里列出其中一些：

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

本章所讲内容对应的练习题，可以在配套的[练习册仓库](https://worksheets.python.datasciencebook.ca)中“Regression I: K-nearest neighbors”那一行找到。点击“查看练习册（view worksheet）”，你就能预览本章练习册的非交互版本。要交互式地做这些习题，请按练习册仓库中的说明下载全部练习册，并按 {numref}`第 %s 章 <move-to-your-own-machine>` 中给出的计算机环境配置说明操作。这样才能保证练习册提供的自动反馈和指导按预期正常工作。


+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```

<<TERM>>
Sacramento = 萨克拉门托
scale (of predictors, noun) = 尺度
<<END>>