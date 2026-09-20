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

用 RMSPE 评估，我们最终模型的测试误差为 \${glue:text}`sacr_RMSPE`。请记住，这个误差的单位就是响应变量的单位，在这里是美元（USD）。这是否说明，我们的模型能根据房屋面积这一预测变量很好地预测房屋售价？同样，这个问题依旧不好回答，需要知道你打算如何使用这个预测结果。

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

完整萨克拉门托房价数据的售价与面积散点图，并叠加最优拟合直线。
:::

## 简单线性回归与 k 近邻回归的比较

```{index} 回归; 方法的比较
```

现在我们已经对简单线性回归和 k 近邻回归有了大致了解，就可以开始比较这两种方法以及它们做出的预测，并讨论其异同。首先，我们来看看萨克拉门托房地产数据上简单线性回归模型的预测可视化（用房屋面积预测价格），以及由同一个问题得到的“最佳”k 近邻回归模型，结果见 {numref}`fig:08-compareRegression`。

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

在 {numref}`fig:08-compareRegression` 中，我们看到了哪些差异？一个明显的差异是两条橙色线的形状。在简单线性回归中，我们只能得到一条直线；而在 k 近邻回归中，拟合线灵活得多，可以相当曲折。不过，把模型限制为直线，有一个很大的可解释性优势。一条直线只需两个数字就能确定：纵截距和斜率。截距告诉我们，所有预测变量都等于 0 时的预测值是多少；斜率告诉我们，预测变量每增加一个单位，响应变量预计会增加多少。k 近邻回归虽然实现和理解起来都很简单，但它的曲折拟合线并不具备这种可解释性。

```{index} 欠拟合; 回归
```

不过，有时使用简单线性回归模型也会有劣势，尤其是响应变量与预测变量之间的关系并非线性，而是呈其他形状（例如弯曲或振荡）时。这种情况下，简单线性回归给出的预测模型会欠拟合，也就是说模型的预测值与实际的观测值吻合得不太好。这样的模型在训练数据上评估拟合优度时，RMSE 可能相当高；而在测试数据集上评估预测质量时，RMSPE 也会相当高。在这样的数据集上，k 近邻回归的表现可能更好。此外，后续教材中还会介绍其他类型的回归，它们在预测这类数据时可能做得更好。

这两个模型在萨克拉门托房价数据集上表现如何？在 {numref}`fig:08-compareRegression` 中，我们还打印了 RMSPE，它是在未参与训练/拟合模型的测试数据集上做预测算出来的。简单线性回归模型的 RMSPE 略低于 k 近邻回归模型的 RMSPE。考虑到简单线性回归模型的可解释性也更好，如果要在实践中比较两者，我们多半会选择简单线性回归模型。

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

与 k 近邻分类和 k 近邻回归一样，我们可以从只有一个预测变量的简单情形，扩展到含有多个预测变量的情形，即*多元线性回归*。做法与 k 近邻回归非常相似：只需在指定训练数据时加入更多预测变量。但请回想，线性回归既不需要用交叉验证来选参数，也不需要对数据做标准化（即中心化和缩放）。还要再次注意，多个预测变量会带来同样的顾虑，这与多元 k 近邻回归和分类中的情形一样：预测变量更多**并非**总是更好。不过，{numref}`第 %s 章 <classification2>` 中的预测变量选择算法同样适用于线性回归，因此本章不再重复介绍。

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

用 RMSPE 评估，我们模型的测试误差为 \${glue:text}`sacr_mult_RMSPE`。预测变量有两个时，我们可以把线性回归给出的预测结果画出来，它构成一个*最优拟合平面*，如 {numref}`fig:08-3DlinReg` 所示。

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

