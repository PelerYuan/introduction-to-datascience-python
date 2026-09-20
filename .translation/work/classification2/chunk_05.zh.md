## 预测变量选择

```{note}
本节不是后续章节的必读内容。收录在此，是给那些有兴趣了解无关变量会如何影响分类器性能、
以及如何挑选一部分有用变量充当预测变量的读者。
```

```{index} 无关预测变量
```

调优分类器时，另一个可能很重要的环节，是决定数据中的哪些变量用作预测变量。从只用一个预测变量，到用上数据中的每一个变量，技术上都可以选；k 近邻算法接受任意个数的预测变量。不过，**并非**预测变量越多，预测效果就一定越好！事实上，有时把无关变量也算进来，反而会拉低分类器的性能。

+++ {"toc-hr-collapsed": true}

### 无关预测变量的影响

我们来看一个例子：给 k 近邻算法提供更多预测变量，它的表现反而更差。在这个例子中，我们修改了乳腺癌数据，只保留原始数据里的 `Smoothness`、`Concavity` 和 `Perimeter` 三个变量。随后又用随机数生成器自己造了一些无关变量。对每条观测来说，这些无关变量都以相同的概率取 0 或 1，与 `Class` 变量的取值无关。换句话说，无关变量与 `Class` 变量之间没有任何实质关系。

```{code-cell} ipython3
:tags: [remove-cell]

np.random.seed(4)
cancer_irrelevant = cancer[["Class", "Smoothness", "Concavity", "Perimeter"]]
d = {
    f"Irrelevant{i+1}": np.random.choice(
        [0, 1], size=len(cancer_irrelevant), replace=True
    )
    for i in range(40)  ## in R textbook, it is 500, but the downstream analysis only uses up to 40
}
cancer_irrelevant = pd.concat((cancer_irrelevant, pd.DataFrame(d)), axis=1)
```

```{code-cell} ipython3
cancer_irrelevant[
    ["Class", "Smoothness", "Concavity", "Perimeter", "Irrelevant1", "Irrelevant2"]
]
```

接下来我们构建一系列 K-NN 分类器，它们的预测变量除了 `Smoothness`、`Concavity` 和 `Perimeter`，还包含越来越多的无关变量。具体来说，我们创建 6 个数据集，其中的无关预测变量分别为 0、5、10、15、20 和 40 个。然后为每个数据集构建一个模型，并用 5 折交叉验证调优。{numref}`fig:06-performance-irrelevant-features` 给出了交叉验证准确率估计值随无关预测变量个数的变化。随着无关预测变量增多，分类器的估计准确率不断下降。原因在于，无关变量会为每两条观测之间的距离增加一个随机的量；无关变量越多，这种（随机）影响就越大，也就越会破坏为待预测新观测的类别投票的那组最近邻。

```{code-cell} ipython3
:tags: [remove-cell]

# get accuracies after including k irrelevant features
ks = [0, 5, 10, 15, 20, 40]
fixedaccs = list()
accs = list()
nghbrs = list()

for i in range(len(ks)):
    cancer_irrelevant_subset = cancer_irrelevant.iloc[:, : (4 + ks[i])]
    cancer_preprocessor = make_column_transformer(
        (
            StandardScaler(),
            list(cancer_irrelevant_subset.drop(columns=["Class"]).columns),
        ),
    )
    cancer_tune_pipe = make_pipeline(cancer_preprocessor, KNeighborsClassifier())
    param_grid = {
        "kneighborsclassifier__n_neighbors": range(1, 21),
    }  
    cancer_tune_grid = GridSearchCV(
        estimator=cancer_tune_pipe,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        return_train_score=True,
    )

    X = cancer_irrelevant_subset.drop(columns=["Class"])
    y = cancer_irrelevant_subset["Class"]

    cancer_model_grid = cancer_tune_grid.fit(X, y)
    accuracies_grid = pd.DataFrame(cancer_model_grid.cv_results_)
    sorted_accuracies = accuracies_grid.sort_values(
        by="mean_test_score", ascending=False
    )

    res = sorted_accuracies.iloc[0, :]
    accs.append(res["mean_test_score"])
    nghbrs.append(res["param_kneighborsclassifier__n_neighbors"])

    ## Use fixed n_neighbors=3
    cancer_fixed_pipe = make_pipeline(
        cancer_preprocessor, KNeighborsClassifier(n_neighbors=3)
    )

    cv_5 = cross_validate(estimator=cancer_fixed_pipe, X=X, y=y, cv=5)
    cv_5_metrics = pd.DataFrame(cv_5).agg(["mean", "sem"])
    fixedaccs.append(cv_5_metrics.loc["mean", "test_score"])
```

```{code-cell} ipython3
:tags: [remove-cell]

summary_df = pd.DataFrame(
    {"ks": ks, "nghbrs": nghbrs, "accs": accs, "fixedaccs": fixedaccs}
)
plt_irrelevant_accuracies = (
    alt.Chart(summary_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "accs",
            title="Model Accuracy Estimate",
            scale=alt.Scale(zero=False),
        ),
    )
)
glue("fig:06-performance-irrelevant-features", plt_irrelevant_accuracies)
```

:::{glue:figure} fig:06-performance-irrelevant-features
:name: fig:06-performance-irrelevant-features

纳入无关预测变量的影响。
:::

准确率确实如预期那样下降了，但 {numref}`fig:06-performance-irrelevant-features` 有一点出人意料：即使有 40 个无关变量，这个方法仍然优于基准的多数类分类器（准确率约为 {glue:text}`cancer_train_b_prop`%）。这怎么可能？{numref}`fig:06-neighbors-irrelevant-features` 给出了答案：k 近邻分类器的调优过程会靠增加近邻个数，来抵消无关变量带来的额外随机性。当然，由于无关变量给数据带来了大量额外噪声，近邻个数并不会平滑地增加，但总体趋势是上升的。{numref}`fig:06-fixed-irrelevant-features` 印证了这一证据：如果把近邻个数固定为 $K=3$，准确率下降得更快。

```{code-cell} ipython3
:tags: [remove-cell]

plt_irrelevant_nghbrs = (
    alt.Chart(summary_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "nghbrs",
            title="Tuned number of neighbors",
        ),
    )
)
glue("fig:06-neighbors-irrelevant-features", plt_irrelevant_nghbrs)
```

:::{glue:figure} fig:06-neighbors-irrelevant-features
:name: fig:06-neighbors-irrelevant-features

无关预测变量个数不同时调优得到的近邻个数。
:::

```{code-cell} ipython3
:tags: [remove-cell]

melted_summary_df = summary_df.melt(
            id_vars=["ks", "nghbrs"], var_name="Type", value_name="Accuracy"
        )
melted_summary_df["Type"] = melted_summary_df["Type"].apply(lambda x: "Tuned K" if x=="accs" else "K = 3")

plt_irrelevant_nghbrs_fixed = (
    alt.Chart(
        melted_summary_df
    )
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "Accuracy",
            scale=alt.Scale(zero=False),
        ),
        color=alt.Color("Type"),
    )
)
glue("fig:06-fixed-irrelevant-features", plt_irrelevant_nghbrs_fixed)
```

:::{glue:figure} fig:06-fixed-irrelevant-features
:name: fig:06-fixed-irrelevant-features

近邻个数调优与未调优时，准确率随无关预测变量个数的变化。
:::

+++

### 寻找好的预测变量子集

那么，既然不加考虑地把所有变量都当作预测变量并不理想，我们该怎样挑选*应该*使用的变量呢？一个简单办法是依靠你对数据的专业理解，判断哪些变量不太可能是有用的预测变量。例如，我们一直在研究的这份癌症数据中，`ID` 变量只是观测的唯一标识符。它与细胞的任何测量属性都无关，因此不应把 `ID` 变量当作预测变量。当然，这是非常明确的情形。但其余变量就没那么好判断了，它们看起来都是合理的候选。究竟哪个子集能造出最好的分类器，并不清楚。你可以借助可视化和其他探索性分析，帮助判断哪些变量可能有用，但要考虑的变量一多，这个过程既费时又容易出错。因此我们需要一种更系统、更程序化的变量选择方法。总的来说，这个问题很难解决，人们已经针对一些特定的应用场景提出了不少方法。这里我们讨论两种基本的选择方法，作为这一主题的入门。想进一步了解变量选择（包括更高级的方法），可以查看本章末尾的拓展资源。

```{index} 变量选择; 最优子集
```

```{index} see: 预测变量选择; 变量选择
```

要系统地选择预测变量，你首先想到的办法可能是：把所有可能的预测变量子集都试一遍，然后挑出能得到“最好”分类器的那个集合。这个做法确实是一种著名的变量选择方法，叫作*最优子集选择*（best subset selection）{cite:p}`bealesubset,hockingsubset`。具体来说，你要

1. 为预测变量的每一个可能子集分别建立一个模型，
2. 用交叉验证对每个模型调优，
3. 选出交叉验证准确率最高的那个预测变量子集。

最优子集选择适用于任何分类方法（K-NN 或其它方法）。不过，只要可供选择的预测变量稍微多一点（比如 10 个左右），它就会变得非常慢。原因在于，可能的预测变量子集个数随预测变量个数增长得极快，而每个子集都得训练一次模型（训练本身就很慢！）。例如，如果只有 2 个预测变量——把它们叫作 A 和 B——那么有 3 种变量组合可试：只用 A、只用 B，以及 A 和 B 一起用。如果有 3 个预测变量——A、B 和 C——那么有 7 种可试：A、B、C、AB、BC、AC 和 ABC。一般来说，$m$ 个预测变量需要训练的模型个数是 $2^m-1$；换句话说，到了 10 个预测变量，要训练的模型就超过*一千*个，而到了 20 个预测变量，要训练的模型超过*一百万*个！所以，最优子集选择虽然方法简单，但在实践中往往计算成本太高，用不起来。

```{index} 变量选择; 前向
```

另一种思路是每次加入一个预测变量，逐步把模型搭建起来。这种方法叫作*前向选择*（forward selection）{cite:p}`forwardefroymson,forwarddraper`，同样适用范围很广，而且相当直观。它包含以下步骤：

1. 起始模型不含任何预测变量。
2. 重复以下 3 个步骤，直到没有预测变量可用：
    1. 对每个尚未使用的预测变量，把它加入模型，组成一个*候选模型*。
    2. 对所有候选模型进行调优。
    3. 把交叉验证准确率最高的候选模型更新为当前模型。
3. 选出在准确率与简洁性之间权衡最好的模型。

假设总共有 $m$ 个预测变量可用。第一轮迭代要建立 $m$ 个候选模型，每个含 1 个预测变量。第二轮迭代要建立 $m-1$ 个候选模型，每个含 2 个预测变量（一个是上一轮选中的，另一个是新增的）。你想迭代多少轮，这个规律就延续多少轮。如果一直做到没有预测变量可选，最终要训练的模型个数是 $\frac{1}{2}m(m+1)$。相比最优子集选择所需的 $2^m-1$ 个模型，这是*很大*的改进！例如，10 个预测变量时，最优子集选择要训练 1000 多个候选模型，而前向选择只需训练 55 个候选模型。因此本节余下的部分都用前向选择。

```{note}
继续之前先提醒一句。你每多训练一个模型，就越可能运气不好，撞上一个模型：它的交叉验证准确率估计值很高，但在测试数据和其他未来观测上的真实准确率却很低。
前向选择要训练大量模型，所以出现这种情况的风险相当高。要把风险压下来，只有在数据量很大、预测变量总数相对较少时才使用前向选择。更高级的方法在这方面的毛病要小得多；想进一步了解高级的预测变量选择方法，可以查看本章末尾的拓展资源。
```

+++

### 用 Python 实现前向选择

```{index} 变量选择; 实现
```

下面我们动手用 Python 实现前向选择。先在这个示例中取出较小的一组预测变量——`Smoothness`、`Concavity`、`Perimeter`、`Irrelevant1`、`Irrelevant2` 和 `Irrelevant3`——以及作为标签的 `Class` 变量。我们还会取出全部预测变量的列名。

```{code-cell} ipython3
cancer_subset = cancer_irrelevant[
    [
        "Class",
        "Smoothness",
        "Concavity",
        "Perimeter",
        "Irrelevant1",
        "Irrelevant2",
        "Irrelevant3",
    ]
]

names = list(cancer_subset.drop(
    columns=["Class"]
).columns.values)

cancer_subset
```

要实现前向选择，本可以使用 `scikit-learn` 的 [`SequentialFeatureSelector`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html)，但很难把这个做法与参数调优结合起来，为每一组特征找到合适的近邻个数。所以我们改为手写前向选择算法。具体来说，我们需要这样的代码：尝试把每个可用的预测变量加入模型，找出其中最好的，然后继续迭代。如果你还记得数据整理那一章的末尾，我们提过有时需要比前面用过的更灵活的迭代形式，这时通常要借助 *for 循环*；参见《Python for Data Analysis》{cite:p}`mckinney2012python` 中的[控制流一节](https://wesmckinney.com/book/python-basics.html#control_for)。这里我们会用两个 for 循环：一个遍历不断增大的预测变量集合规模（就是下面 `for i in range(1, n_total + 1):` 那一行），另一个检查每一轮该加入哪个预测变量（就是下面 `for j in range(len(names))` 那一行）。对每一组待尝试的预测变量，我们取出对应的预测变量子集，把它送入预处理器，构建一个用 10 折交叉验证调优 K-NN 分类器的 `Pipeline`，最后记录估计准确率。

```{code-cell} ipython3
from sklearn.compose import make_column_selector

accuracy_dict = {"size": [], "selected_predictors": [], "accuracy": []}

# store the total number of predictors
n_total = len(names)

# start with an empty list of selected predictors
selected = []

# create the pipeline and CV grid search objects
param_grid = {
    "kneighborsclassifier__n_neighbors": range(1, 61, 5),
}
cancer_preprocessor = make_column_transformer(
    (StandardScaler(), make_column_selector(dtype_include="number"))
)
cancer_tune_pipe = make_pipeline(cancer_preprocessor, KNeighborsClassifier())
cancer_tune_grid = GridSearchCV(
    estimator=cancer_tune_pipe,
    param_grid=param_grid,
    cv=10,
    n_jobs=-1
)

# for every possible number of predictors
for i in range(1, n_total + 1):
    accs = np.zeros(len(names))
    # for every possible predictor to add
    for j in range(len(names)):
        # Add remaining predictor j to the model
        X = cancer_subset[selected + [names[j]]]
        y = cancer_subset["Class"]

        # Find the best K for this set of predictors
        cancer_tune_grid.fit(X, y)
        accuracies_grid = pd.DataFrame(cancer_tune_grid.cv_results_)

        # Store the tuned accuracy for this set of predictors
        accs[j] = accuracies_grid["mean_test_score"].max()

    # get the best new set of predictors that maximize cv accuracy
    best_set = selected + [names[accs.argmax()]]

    # store the results for this round of forward selection
    accuracy_dict["size"].append(i)
    accuracy_dict["selected_predictors"].append(", ".join(best_set))
    accuracy_dict["accuracy"].append(accs.max())

    # update the selected & available sets of predictors
    selected = best_set
    del names[accs.argmax()]

accuracies = pd.DataFrame(accuracy_dict)
accuracies
```

```{index} 变量选择; 肘部法则
```

有意思！前向选择过程首先加入了三个有意义的变量 `Perimeter`、`Concavity` 和 `Smoothness`，随后才轮到无关变量。{numref}`fig:06-fwdsel-3` 把准确率随模型中预测变量个数的变化画了出来。可以看到，随着有意义的预测变量被加入，估计准确率大幅上升；而加入无关变量时，准确率要么小幅波动，要么因为模型试图调整近邻个数以应对额外噪声而下降。要从这一串模型中挑出合适的那个，你得在准确率高与模型简洁（即预测变量更少、过拟合机会更小）之间取得平衡。找到这种平衡的办法，是在 {numref}`fig:06-fwdsel-3` 中寻找*肘部*（elbow），也就是图上准确率不再急剧上升、趋于平稳或开始下降的位置。{numref}`fig:06-fwdsel-3` 里的肘部看起来出现在含 3 个预测变量的模型处；过了这一点，准确率就趋于平稳。所以在这里，准确率与预测变量个数之间的最佳权衡出现在 3 个变量上：`Perimeter, Concavity, Smoothness`。换句话说，我们成功地把无关预测变量从模型中剔除了！不过，永远要记得：交叉验证给出的是真实准确率的*估计值*；看图判断肘部落在哪里、判断加入某个变量是否带来准确率的实质性提升，都要靠你自己拿主意。

```{code-cell} ipython3
:tags: [remove-cell]

fwd_sel_accuracies_plot = (
    alt.Chart(accuracies)
    .mark_line(point=True)
    .encode(
        x=alt.X("size", title="Number of Predictors"),
        y=alt.Y(
            "accuracy",
            title="Estimated Accuracy",
            scale=alt.Scale(zero=False),
        ),
    )
)
glue("fig:06-fwdsel-3", fwd_sel_accuracies_plot)
```

:::{glue:figure} fig:06-fwdsel-3
:name: fig:06-fwdsel-3

用前向选择构建的模型序列中，估计准确率随预测变量个数的变化。
:::

+++

```{note}
选择哪些变量作为预测变量，本身就属于分类器调优的一部分，所以你*不能在这个过程里使用测试数据*！
```

## 习题

本章内容的练习题见配套的[练习册仓库](https://worksheets.python.datasciencebook.ca)，在“Classification II: evaluation and tuning”这一行。点击“查看练习册（view worksheet）”可以预览本章练习册的非交互版本。如果想交互式地做这些习题，请按练习册仓库中的说明下载全部练习册，并按 {numref}`第 %s 章 <move-to-your-own-machine>` 中的说明配置计算机环境。这样才能保证练习册提供的自动反馈与指导按预期工作。

+++

## 拓展资源