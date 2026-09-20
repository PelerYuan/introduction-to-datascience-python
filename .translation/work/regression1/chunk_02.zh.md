+++

```{note}
这里没有像 {numref}`第 %s 章 <classification2>` 那样指定 `stratify` 参数，因为 `train_test_split` 函数无法按定量变量分层。
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

接下来，我们用交叉验证来选择 $K$。在 K-NN 分类中，我们用准确率来衡量预测结果与真实标签的吻合程度；在回归的场景下则不能沿用同一个指标，因为我们的预测几乎不可能与响应变量的真实取值*完全*一致。因此在 K-NN 回归中，我们改用均方根预测误差（root mean square prediction error，RMSPE）。计算 RMSPE 的数学公式为：

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

房价（美元）与房屋面积（平方英尺）的散点图，其中包含示例预测值（橙色线条），以及这些预测值与真实响应值相比的误差（竖线）。
:::

+++

```{index} RMSPE; 与 RMSE 的比较
```

```{note}
在使用许多代码包时，我们用来评估 K-NN 回归模型预测质量的评估输出会被标注为“RMSE”，也就是“均方根误差”（root mean squared error）。为什么会这样，而不是 RMSPE 呢？在统计学中，我们尽量把话说得精确，以表明所计算的预测误差来自训练数据（*样本内*预测）还是测试数据（*样本外*预测）。在训练数据上做预测并评估预测质量时，我们说 RMSE；相比之下，在测试数据或验证数据上做预测并评估预测质量时，我们说 RMSPE。RMSE 与 RMSPE 的计算式完全相同，唯一的区别在于其中的 $y$ 取自训练数据还是测试数据。不过很多人对两者都直接用 RMSE，靠上下文来表明均方根误差是基于哪一份数据计算的。
```

```{index} scikit-learn, scikit-learn; Pipeline, scikit-learn; make_pipeline, scikit-learn; make_column_transformer
```

现在我们知道了如何评估模型对数值的预测效果，接下来就用 Python 做交叉验证，选出最优的 $K$。首先创建一个列变换器（column transformer）来预处理数据。请注意，我们在预处理中加入了标准化，是为了养成良好习惯；但由于只有一个预测变量，技术上并不需要这一步：不存在两个量纲不同的预测变量相互比较的风险。接着我们为 K-NN 回归创建模型流水线。注意这里改用 `KNeighborsRegressor` 模型对象，以表示这是一个回归问题，而不是前几章讨论的分类问题。使用 `KNeighborsRegressor` 实际上是在告诉 `scikit-learn`：调优和评估需要使用不同的指标（而不是准确率）。随后我们指定一个参数网格，其中近邻个数从 1 到 200。然后创建一个 5 折 `GridSearchCV` 对象，并传入流水线和参数网格。这里还有一点小麻烦：与 `scikit-learn` 中的分类模型不同——分类模型默认就用准确率来调优，正合我们的需要——`scikit-learn` 中的回归模型默认不用 RMSPE 来调优。因此，我们需要把 `scoring` 参数设为 `"neg_root_mean_squared_error"`，以指明调优时要使用 RMSPE。

```{note}
表示近邻个数的参数标识符 `"kneighborsregressor__n_neighbors"`，是我们查看 `sacr_pipeline.get_params()` 的输出得到的，做法与 {numref}`第 %s 章 <classification1>` 中一样。
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

接下来，我们调用 `sacr_gridsearch` 的 `fit` 方法来运行交叉验证。请注意，输入特征用了两层方括号（`sacramento_train[["sqft"]]`），这样得到的是只含一列的数据框。正如我们在 {numref}`第 %s 章 <wrangling>` 中学到的，传入列名列表就能得到包含部分列的数据框；`["sqft"]` 是只含一个元素的列表，所以得到的数据框只有一列。如果只用一层方括号（`sacramento_train["sqft"]`），得到的则是一个序列。在 `scikit-learn` 中，把输入特征当作数据框处理比当作序列更方便，因此这里我们选择两层方括号。而在响应变量那边，用序列就可以了，所以只用一层方括号（`sacramento_train["price"]`）。

与 {numref}`第 %s 章 <classification2>` 一样，模型拟合完成后，我们会把 `cv_results_` 的输出放进数据框，只提取需要的列，按 5 折计算标准误，并把参数列重命名得更易读。


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
与分类的情形类似，把近邻个数设得太小或太大，都会使 RMSPE 增大，如 {numref}`fig:07-choose-k-knn-plot` 所示。这里发生了什么？

{numref}`fig:07-howK` 展示了 $K$ 取不同值时回归模型的表现。每张图都给出了我们的 K-NN 回归模型在 6 个不同的 $K$ 值下预测的房屋售价：1、3、25、{glue:text}`best_k_sacr`、250 和 699（也就是全部训练数据）。对每个模型，我们都预测数据集中出现过的各种房屋面积（这里是 500 到 5,000 平方英尺）对应的价格，并把预测价格画成橙色线条。

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

取六个不同 $K$ 值时 K-NN 回归模型预测的房屋价格（用橙色线条表示）。
:::

+++

```{index} 过拟合; 回归
```

{numref}`fig:07-howK` 表明，当 $K$ = 1 时，橙色线条完美地穿过了我们几乎所有的训练观测。这是因为某个区域的预测值（通常）只取决于单个观测。一般来说，$K$ 太小时，线条会相当贴近训练数据，即使不能与之完全吻合。如果我们换一份来自萨克拉门托房地产市场、包含房屋价格和面积的训练数据集，最终会得到完全不同的预测。换句话说，模型受数据的*影响太大*。由于模型紧紧跟随训练数据，它对新的观测就做不出准确预测，而新观测通常不会带有与原训练数据相同的波动。回忆分类各章的内容可知，这种模型受有噪声数据影响过大的行为称为*过拟合*；在回归的语境中我们也用同一个术语。

```{index} 欠拟合; 回归
```

{numref}`fig:07-howK` 中 $K$ 相当大的那几张图，比如 $K$ = 250 或 699，又是什么情况呢？这时橙色线条变得极其平滑，而当 $K$ 等于整个数据集中的数据点个数时，它实际上变成了一条水平线。这是因为，对于某个 x 取值（这里是房屋面积），我们的预测值取决于许多近邻观测；如果 $K$ 等于数据集的大小，预测值就只是数据集中房屋价格的均值（完全忽略了房屋面积）。与 $K=1$ 的例子相比，这条平滑、不灵活的橙色线条并不怎么贴近训练观测。换句话说，模型受训练数据的*影响不够*。回忆分类各章的内容可知，这种行为称为*欠拟合*；在回归的语境中我们同样使用这个术语。

理想情况下，上面讨论的两种情况都不是我们想要的。我们希望模型既能（1）跟随训练数据整体的“趋势”，真正利用训练数据学到有用的东西，又能（2）不跟随有噪声的波动，这样我们才有把握说模型能很好地迁移/泛化到其他新数据。如果我们再看看 $K$ 的其他取值，特别是 $K$ = {glue:text}`best_k_sacr`（正如交叉验证所建议的），就会发现它达到了这个目标：它跟随房屋价格随房屋面积上升的趋势，又不会受价格中那些个别波动的影响。这一切都与 $K$ 的取值如何影响 K-NN 分类类似，上一章已经讨论过。


<<TERM>>
column transformer = 列变换器
<<END>>
