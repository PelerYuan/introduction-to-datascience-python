## 用 `Pipeline` 把流程串起来

```{index} scikit-learn; Pipeline
```

`scikit-learn` 包集合还提供了 [`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html?highlight=pipeline#sklearn.pipeline.Pipeline)，
它可以把多个数据分析步骤串联起来，省去为中间步骤编写大量本来必需的代码。
为了演示整个工作流，我们从 `wdbc_unscaled.csv` 数据从头做起。
首先读取数据、创建模型，并为数据指定一个预处理器。

```{code-cell} ipython3
# load the unscaled cancer data, make Class readable
unscaled_cancer = pd.read_csv("data/wdbc_unscaled.csv")
unscaled_cancer["Class"] = unscaled_cancer["Class"].replace({
   "M" : "Malignant",
   "B" : "Benign"
})
unscaled_cancer

# create the K-NN model
knn = KNeighborsClassifier(n_neighbors=7)

# create the centering / scaling preprocessor
preprocessor = make_column_transformer(
    (StandardScaler(), ["Area", "Smoothness"]),
)
```

```{index} scikit-learn; make_pipeline, scikit-learn; fit
```

接下来，我们用
[`make_pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.make_pipeline.html#sklearn.pipeline.make_pipeline) 函数把这些步骤放进一个 `Pipeline`。
`make_pipeline` 函数接收一个步骤列表，按顺序应用到数据分析中；这里我们只有
`preprocessor` 和 `knn` 两个步骤。
最后，我们对流水线调用 `fit`。
注意，我们不需要分别对 `preprocessor` 调用 `fit` 和 `transform`，
流水线会替我们妥善完成这件事。
还请注意，对流水线调用 `fit` 时，可以把
整个 `unscaled_cancer` 数据框传给 `X` 参数，因为预处理步骤会丢弃
我们列出的两个变量之外的所有变量，也就是 `Area` 和 `Smoothness`。
`y` 响应变量参数则和之前一样，传入 `unscaled_cancer["Class"]` 序列。

```{code-cell} ipython3
from sklearn.pipeline import make_pipeline

knn_pipeline = make_pipeline(preprocessor, knn)
knn_pipeline.fit(
    X=unscaled_cancer,
    y=unscaled_cancer["Class"]
)
knn_pipeline
```

和之前一样，拟合对象会列出用于训练模型的函数。不过现在，拟合对象还包含了
整个工作流的信息，其中包括标准化这一预处理步骤。
换句话说，我们用 `predict` 函数配合 `knn_pipeline` 对象对新观测做预测时，
它会先对新观测应用同样的预处理步骤。
举个例子，我们来预测两个新观测的类别标签：
一个是 `Area = 500`、`Smoothness = 0.075`，另一个是 `Area = 1500`、`Smoothness = 0.1`。

```{code-cell} ipython3
new_observation = pd.DataFrame({"Area": [500, 1500], "Smoothness": [0.075, 0.1]})
prediction = knn_pipeline.predict(new_observation)
prediction
```

分类器预测第一个观测为良性，第二个为恶性。{numref}`fig:05-workflow-plot` 展示了这个
训练好的 k 近邻模型在大量新观测上会做出的预测。
你已经见过好几次这样的彩色预测图了，
但我们一直没有提供生成它们的代码，因为代码有点复杂。
如果你有兴趣挑战一下自己，我们现在把它列在下面。
基本思路是：用 `numpy` 的 `meshgrid` 函数造出由合成新观测构成的网格，
预测每个点的标签，再用一张透明度很高
（`opacity` 取值很小）、点半径很大的彩色散点图把这些预测画出来。看看你能不能弄明白每一行代码在做什么！

```{note}
理解这段代码并不是读懂本书后续内容的必需条件。
把它列在这里，是供那些希望在自己的数据分析中
使用类似可视化的人参考。
```

```{code-cell} ipython3
:tags: [remove-output]
import numpy as np

# create the grid of area/smoothness vals, and arrange in a data frame
are_grid = np.linspace(
    unscaled_cancer["Area"].min() * 0.95, unscaled_cancer["Area"].max() * 1.05, 50
)
smo_grid = np.linspace(
    unscaled_cancer["Smoothness"].min() * 0.95, unscaled_cancer["Smoothness"].max() * 1.05, 50
)
asgrid = np.array(np.meshgrid(are_grid, smo_grid)).reshape(2, -1).T
asgrid = pd.DataFrame(asgrid, columns=["Area", "Smoothness"])

# use the fit workflow to make predictions at the grid points
knnPredGrid = knn_pipeline.predict(asgrid)

# bind the predictions as a new column with the grid points
prediction_table = asgrid.copy()
prediction_table["Class"] = knnPredGrid

# plot:
# 1. the colored scatter of the original data
unscaled_plot = alt.Chart(unscaled_cancer).mark_point(
    opacity=0.6,
    filled=True,
    size=40
).encode(
    x=alt.X("Area")
        .scale(
            nice=False,
            domain=(
                unscaled_cancer["Area"].min() * 0.95,
                unscaled_cancer["Area"].max() * 1.05
            )
        ),
    y=alt.Y("Smoothness")
        .scale(
            nice=False,
            domain=(
                unscaled_cancer["Smoothness"].min() * 0.95,
                unscaled_cancer["Smoothness"].max() * 1.05
            )
        ),
    color=alt.Color("Class").title("Diagnosis")
)

# 2. the faded colored scatter for the grid points
prediction_plot = alt.Chart(prediction_table).mark_point(
    opacity=0.05,
    filled=True,
    size=300
).encode(
    x="Area",
    y="Smoothness",
    color=alt.Color("Class").title("Diagnosis")
)
unscaled_plot + prediction_plot
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("fig:05-workflow-plot", (unscaled_plot + prediction_plot))
```

:::{glue:figure} fig:05-workflow-plot
:name: fig:05-workflow-plot

平滑度对面积的散点图，其中背景颜色表示分类器的判别结果。
:::

+++

## 习题

本章内容的练习题可以在配套的
[练习册仓库](https://worksheets.python.datasciencebook.ca) 的
“分类一：训练与预测（Classification I: training and predicting）”一行中找到。你可以预览
本章练习册（worksheet）的非交互版本，只需点击“查看练习册（view worksheet）”。
如果要交互式地做习题，请按照
练习册仓库中的说明下载所有练习册，并按照
{numref}`第 %s 章 <move-to-your-own-machine>` 中的计算机环境配置说明操作。这样就能确保
练习册提供的自动反馈与引导能
按预期正常工作。


+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
