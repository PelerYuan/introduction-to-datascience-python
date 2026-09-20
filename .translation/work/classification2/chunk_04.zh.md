+++

### 欠拟合与过拟合

为了多建立一些直觉：如果我们不断增大近邻个数 $K$，会发生什么？事实上，交叉验证
准确率估计值反而会开始下降！我们不妨在 `GridSearchCV` 的 `param_grid` 参数中指定
大得多的 $K$ 取值范围来试。{numref}`fig:06-lots-of-ks` 展示了 $K$ 从 1 一直变到
接近数据集观测个数时，估计准确率变化的图形。

```{code-cell} ipython3
:tags: [remove-output]

large_param_grid = {
    "kneighborsclassifier__n_neighbors": range(1, 385, 10),
}

large_cancer_tune_grid = GridSearchCV(
    estimator=cancer_tune_pipe,
    param_grid=large_param_grid,
    cv=10
)

large_cancer_tune_grid.fit(
    cancer_train[["Smoothness", "Concavity"]],
    cancer_train["Class"]
)

large_accuracies_grid = pd.DataFrame(large_cancer_tune_grid.cv_results_)

large_accuracy_vs_k = alt.Chart(large_accuracies_grid).mark_line(point=True).encode(
    x=alt.X("param_kneighborsclassifier__n_neighbors").title("Neighbors"),
    y=alt.Y("mean_test_score")
        .scale(zero=False)
        .title("Accuracy estimate")
)

large_accuracy_vs_k
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:06-lots-of-ks", large_accuracy_vs_k)
```

:::{glue:figure} fig:06-lots-of-ks
:name: fig:06-lots-of-ks

许多 K 取值下，准确率估计值随近邻个数变化的图形。
:::

+++

```{index} 欠拟合; 分类
```

**欠拟合（underfitting）：** 分类器到底发生了什么，才导致这种结果？随着近邻个数
增大，越来越多的训练观测（以及离目标点越来越远的那些观测）都能对新观测的类别
“发表意见”。这就产生了一种“平均效应”，使分类器判别肿瘤为恶性还是良性的边界
变得平滑，也*更简单*。如果走极端，把 $K$ 设为整个训练集的大小，那么无论新观测
长什么样，分类器都会预测同一个标签。一般来说，如果模型*受到训练数据的影响
不够*，就说它对数据**欠拟合**。

```{index} 过拟合; 分类
```

**过拟合（overfitting）：** 反过来，减小近邻个数时，每个数据点对附近点的表决权
都越来越强。由于数据本身带有噪声，判别边界会变得更加“锯齿状”，对应着一个
*不那么简单*的模型。如果走极端，令 $K = 1$，那么分类器实际上就是把每个新观测
匹配到训练数据集中离它最近的邻居。这和 $K$ 很大的情形一样成问题，因为分类器
在新数据上变得不可靠：如果换一个训练集，预测结果会完全不同。一般来说，如果
模型*受到训练数据的影响过多*，就说它对数据**过拟合**。

```{code-cell} ipython3
:tags: [remove-cell]
alt.data_transformers.disable_max_rows()

cancer_plot = (
    alt.Chart(
        cancer_train,
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X(
            "Smoothness",
            scale=alt.Scale(
                domain=(
                    cancer_train["Smoothness"].min() * 0.95,
                    cancer_train["Smoothness"].max() * 1.05,
                )
            ),
        ),
        y=alt.Y(
            "Concavity",
            scale=alt.Scale(
                domain=(
                    cancer_train["Concavity"].min() -0.025,
                    cancer_train["Concavity"].max() * 1.05,
                )
            ),
        ),
        color=alt.Color("Class", title="Diagnosis"),
    )
)

X = cancer_train[["Smoothness", "Concavity"]]
y = cancer_train["Class"]

# create a prediction pt grid
smo_grid = np.linspace(
    cancer_train["Smoothness"].min() * 0.95, cancer_train["Smoothness"].max() * 1.05, 100
)
con_grid = np.linspace(
    cancer_train["Concavity"].min() - 0.025, cancer_train["Concavity"].max() * 1.05, 100
)
scgrid = np.array(np.meshgrid(smo_grid, con_grid)).reshape(2, -1).T
scgrid = pd.DataFrame(scgrid, columns=["Smoothness", "Concavity"])

plot_list = []
for k in [1, 7, 20, 300]:
    cancer_pipe = make_pipeline(cancer_preprocessor, KNeighborsClassifier(n_neighbors=k))
    cancer_pipe.fit(X, y)

    knnPredGrid = cancer_pipe.predict(scgrid)
    prediction_table = scgrid.copy()
    prediction_table["Class"] = knnPredGrid

    # add a prediction layer
    prediction_plot = (
        alt.Chart(
            prediction_table,
            title=f"K = {k}"
        )
        .mark_point(opacity=0.2, filled=True, size=20)
        .encode(
            x=alt.X(
                "Smoothness",
                scale=alt.Scale(
                    domain=(
                        cancer_train["Smoothness"].min() * 0.95,
                        cancer_train["Smoothness"].max() * 1.05
                    ),
                    nice=False
                )
            ),
            y=alt.Y(
                "Concavity",
                scale=alt.Scale(
                    domain=(
                        cancer_train["Concavity"].min() -0.025,
                        cancer_train["Concavity"].max() * 1.05
                    ),
                    nice=False
                )
            ),
            color=alt.Color("Class", title="Diagnosis"),
        )
    )
    plot_list.append(cancer_plot + prediction_plot)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue(
    "fig:06-decision-grid-K",
    ((plot_list[0] | plot_list[1])
    & (plot_list[2] | plot_list[3])).configure_legend(
        orient="bottom", titleAnchor="middle"
    ),
)
```

:::{glue:figure} fig:06-decision-grid-K
:name: fig:06-decision-grid-K

K 取值对过拟合与欠拟合的影响。
:::

+++

过拟合和欠拟合都有问题，都会使模型难以很好地泛化到新数据。拟合模型时，我们需要
在两者之间取得平衡。这两个效应可以在 {numref}`fig:06-decision-grid-K` 中看到，图中
展示了把近邻个数 $K$ 分别设为 1、7、20 和 300 时分类器的变化。

+++

### 在测试集上评估

现在 K 近邻分类器已经调好，并设 $K =$ {glue:text}`best_k_unique`，模型构建到此结束，
接下来要评估它在留出的测试数据上预测的质量，就像前面在
{numref}`eval-performance-clasfcn2` 中做的那样。我们首先要用选定的近邻个数，在整个
训练数据集上重新训练 K 近邻分类器。好在不必手动完成，`scikit-learn` 会自动帮我们做。
要在测试数据上做出预测并评估最优模型的估计准确率，可以用拟合好的 `GridSearchCV`
对象的 `score` 和 `predict` 方法。然后把这些预测传给 `precision`、`recall` 和
`crosstab` 函数，评估估计的精确率与召回率，并打印混淆矩阵。

```{index} scikit-learn;predict, scikit-learn;score, scikit-learn;precision_score, scikit-learn;recall_score, crosstab
```

```{code-cell} ipython3
cancer_test["predicted"] = cancer_tune_grid.predict(
    cancer_test[["Smoothness", "Concavity"]]
)

cancer_tune_grid.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
```

```{code-cell} ipython3
precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
```

```{code-cell} ipython3
recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
```

```{code-cell} ipython3
pd.crosstab(
    cancer_test["Class"],
    cancer_test["predicted"]
)
```
```{code-cell} ipython3
:tags: [remove-cell]
cancer_prec_tuned = precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
cancer_rec_tuned = recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
cancer_acc_tuned = cancer_tune_grid.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
glue("cancer_acc_tuned", "{:0.0f}".format(100*cancer_acc_tuned))
glue("cancer_prec_tuned", "{:0.0f}".format(100*cancer_prec_tuned))
glue("cancer_rec_tuned", "{:0.0f}".format(100*cancer_rec_tuned))
glue("mean_acc_ks", "{:0.0f}".format(100*accuracies_grid["mean_test_score"].mean()))
glue("std3_acc_ks", "{:0.0f}".format(3*100*accuracies_grid["mean_test_score"].std()))
glue("mean_sem_acc_ks", "{:0.0f}".format(100*accuracies_grid["sem_test_score"].mean()))
glue("n_neighbors_max", "{:0.0f}".format(accuracies_grid["n_neighbors"].max()))
glue("n_neighbors_min", "{:0.0f}".format(accuracies_grid["n_neighbors"].min()))
```

乍看之下这有点出人意料：尽管调了近邻个数，分类器的准确率并没有太大变化！我们最初
那个 $K =$ 3 的模型（那时我们还不会调优）估计准确率是 {glue:text}`cancer_acc_1`%，
而调优后的模型 $K =$ {glue:text}`best_k_unique` 的估计准确率是 {glue:text}`cancer_acc_tuned`%。
再看一眼 {numref}`fig:06-find-k` 中一系列近邻个数对应的交叉验证准确率估计值，这个结果
就不那么让人意外了。从 {glue:text}`n_neighbors_min` 个近邻到大约 {glue:text}`n_neighbors_max`
个近邻，交叉验证准确率估计值的变化只有约 {glue:text}`std3_acc_ks`%，而每个估计值的标准误
约为 {glue:text}`mean_sem_acc_ks`%。既然交叉验证准确率估计的是测试集准确率，测试集
准确率同样变化不大就是意料之中的事。还要注意，$K =$ 3 的模型精确率为
{glue:text}`cancer_prec_1`%、召回率为 {glue:text}`cancer_rec_1`%，而调优后的模型精确率为
{glue:text}`cancer_prec_tuned`%、召回率为 {glue:text}`cancer_rec_tuned`%。考虑到召回率
下降了——请记住，在这个应用里，召回率对于确保找出所有恶性肿瘤患者至关重要——
调优后的模型在这种情形下其实可能*更不*受青睐。无论如何，都要对调优结果做批判性
分析。为最大化准确率而调优的模型，对某个具体应用来说未必更好。

## 小结

分类算法用一个或多个定量变量来预测另一个分类变量的取值。具体来说，K 近邻算法先
找出训练数据中离新观测最近的 $K$ 个点，再返回这些训练观测的多数类投票结果。把数据
随机划分为训练集和测试集，就能对分类器进行调优和评估。训练集用来构建分类器；
我们可以通过交叉验证最大化估计准确率，从而对分类器调优（例如选择 K 近邻中的
近邻个数）。模型调好之后，再用测试集估计它的准确率。{numref}`fig:06-overview`
总结了整个流程。

+++

```{figure} img/classification2/train-test-overview.png
:name: fig:06-overview

K 近邻分类概述。
```

+++

```{index} scikit-learn;Pipeline, 交叉验证, K 近邻; 分类, 分类
```

使用 `scikit-learn` 完成 K 近邻分类的整体工作流如下：

1. 用 `train_test_split` 函数把数据划分为训练集和测试集。把 `stratify` 参数设为数据框的类别标签列。暂时把测试集放到一边。
2. 创建一个 `Pipeline`，指明预处理步骤和分类器。
3. 给出你想要调优的一组 $K$ 取值，定义参数网格。
4. 用 `GridSearchCV` 估计一系列 $K$ 取值下分类器的准确率。把第 2 步和第 3 步定义的流水线和参数网格分别作为 `param_grid` 参数和 `estimator` 参数传入。
5. 把训练数据传给第 4 步创建的 `GridSearchCV` 实例的 `fit` 方法，执行网格搜索。
6. 选一个 $K$，使交叉验证准确率估计值较高，且把 $K$ 换成邻近取值时该估计值变化不大。
7. 针对最优参数取值（即 $K$）新建一个模型对象，并调用 `fit` 方法重新训练分类器。
8. 用 `score` 方法在测试集上评估分类器的估计准确率。

最近两章我们一直围绕 K 近邻算法展开，但可以用来预测类别标签的方法还有很多。每种
算法都各有长短，下面把 K-NN 的这些优缺点总结一下。

**优点：** K 近邻分类

1. 算法简单、直观；
2. 对数据形态几乎没有假设；
3. 既适用于二分类（binary classification，即两类）问题，也适用于多分类（multiclass classification，即类别多于 2 类）问题。

**缺点：** K 近邻分类

1. 训练数据变大时速度会变得很慢；
2. 预测变量很多时可能表现不好；
3. 类别不平衡时可能表现不好。

+++