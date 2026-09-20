+++

### 交叉验证

```{index} 验证集
```

选择参数 $K$ 的第一步，是能够只用训练数据就评估分类器。如果这一点做得到，我们就能仅凭训练数据比较分类器在不同 $K$ 取值下的性能，并挑出最好的那一个。正如本节开头所说，做法是把训练数据划分开，用其中一部分训练，用另一部分评估。用来评估的那部分训练数据，通常称为**验证集（validation set）**。

不过，它与前面做过的训练/测试划分有一个关键区别。具体来说，那时我们只能对数据做*一次划分*。因为归根到底，我们要产出的只是一个分类器；要是我们对数据做了多种不同的训练/测试划分，就会造出多个不同的分类器。而在调优分类器的过程中，我们完全可以基于训练数据的多种划分造出多个分类器，逐一评估，再根据__*全部*__结果选择一个参数取值。如果只对整体训练数据划分*一次*，那么选出的最佳参数就会严重依赖哪些数据碰巧落进了验证集。改用多种不同的训练/验证划分，也许能得到更准确的准确率估计值，从而为整体训练数据选出更好的近邻个数 $K$。

我们用 Python 来试试这个想法！具体来说，对整体训练数据生成五组不同的训练/验证划分，训练五个不同的 k 近邻模型，并评估它们的准确率。先从只划分一次开始。

```{code-cell} ipython3
# create the 25/75 split of the *training data* into sub-training and validation
cancer_subtrain, cancer_validation = train_test_split(
    cancer_train, train_size=0.75, stratify=cancer_train["Class"]
)

# fit the model on the sub-training data
knn = KNeighborsClassifier(n_neighbors=3)
X = cancer_subtrain[["Smoothness", "Concavity"]]
y = cancer_subtrain["Class"]
knn_pipeline = make_pipeline(cancer_preprocessor, knn)
knn_pipeline.fit(X, y)

# compute the score on validation data
acc = knn_pipeline.score(
    cancer_validation[["Smoothness", "Concavity"]],
    cancer_validation["Class"]
)
acc
```

```{code-cell} ipython3
:tags: [remove-cell]

accuracies = [acc]
for i in range(1, 5):
    # create the 25/75 split of the training data into training and validation
    cancer_subtrain, cancer_validation = train_test_split(
        cancer_train, test_size=0.25
    )

    # fit the model on the sub-training data
    knn = KNeighborsClassifier(n_neighbors=3)
    X = cancer_subtrain[["Smoothness", "Concavity"]]
    y = cancer_subtrain["Class"]
    knn_pipeline = make_pipeline(cancer_preprocessor, knn).fit(X, y)

    # compute the score on validation data
    accuracies.append(knn_pipeline.score(
        cancer_validation[["Smoothness", "Concavity"]],
        cancer_validation["Class"]
       ))
avg_accuracy = np.round(np.array(accuracies).mean()*100,1)
accuracies = list(np.round(np.array(accuracies)*100, 1))
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("acc_seed1", "{:0.1f}".format(100 * acc))
glue("avg_5_splits", "{:0.1f}".format(avg_accuracy))
glue("accuracies", "[" + "%, ".join(["{:0.1f}".format(acc) for acc in accuracies]) + "%]")
```
```{code-cell} ipython3
:tags: [remove-cell]

```

用这次划分得到的准确率估计值是 {glue:text}`acc_seed1`%。下面把上面的代码再重复 4 次，就又得到 4 组划分。于是我们有了五种不同的数据打乱方式，也就有了五个不同的准确率取值：{glue:text}`accuracies`。这些取值未必有哪一个比别的“更正确”；它们只是用整体训练数据构建的分类器真实内在准确率的五个估计值。把这些估计值取平均（这里是 {glue:text}`avg_5_splits`%），就能对分类器的准确率得到一个总的判断；这样做可以削弱某一个（不）走运的验证集对估计值的影响。

```{index} 交叉验证
```

实践中我们并不用随机划分，而是采用更讲章法的划分流程，让数据集里的每条观测只充当一次验证集。这种策略叫作**交叉验证（cross-validation）**。在**交叉验证**中，我们把**整体训练数据**均分成 $C$ 个等份。接着依次把 $1$ 个等份用作**验证集**，把剩下的 $C-1$ 个等份合起来作**训练集**。该流程见 {numref}`fig:06-cv-image`。这里用了数据集里 $C=5$ 个不同的等份，于是**验证集**有 5 种不同的取法；我们称之为*5 折*交叉验证。

+++

```{figure} img/classification2/cv.png
:name: fig:06-cv-image

5 折交叉验证。
```


+++

```{index} 交叉验证; cross_validate, scikit-learn; cross_validate
```

要在 Python 中用 `scikit-learn` 做 5 折交叉验证，得用另一个函数：`cross_validate`。这个函数要求我们把建模用的 `Pipeline` 作为 `estimator` 参数传入，把折数作为 `cv` 参数传入，把训练数据的预测变量和标签作为 `X` 和 `y` 参数传入。`cross_validate` 的输出是一个字典，所以我们用 `pd.DataFrame` 把它转成 `pandas` 数据框，以便查看得更清楚。请注意，`cross_validate` 会自动对每个训练折和验证折中的类别做分层。

```{code-cell} ipython3
from sklearn.model_selection import cross_validate

knn = KNeighborsClassifier(n_neighbors=3)
cancer_pipe = make_pipeline(cancer_preprocessor, knn)
X = cancer_train[["Smoothness", "Concavity"]]
y = cancer_train["Class"]
cv_5_df = pd.DataFrame(
    cross_validate(
        estimator=cancer_pipe,
        cv=5,
        X=X,
        y=y
    )
)

cv_5_df
```

```{index} see: sem;标准误
```

```{index} 标准误, DataFrame;agg
```

我们关心的验证得分在 `test_score` 列里。接着可以对各折上分类器的验证准确率聚合出*均值*和*标准误（standard error）*。把均值（`mean`）看作准确率的估计值，标准误（`sem`）则衡量这个均值有多不确定。详细讨论超出本章范围；大致说来，如果估计均值为 {glue:text}`cv_5_mean`、标准误为 {glue:text}`cv_5_std`，就可以指望分类器的*真实*平均准确率大致落在 {glue:text}`cv_5_lower`% 到 {glue:text}`cv_5_upper`% 之间（当然也可能落在这个范围之外）。指标数据框中的其他列可以忽略。

```{code-cell} ipython3
cv_5_metrics = cv_5_df.agg(["mean", "sem"])
cv_5_metrics
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cv_5_mean", "{:.2f}".format(cv_5_metrics.loc["mean", "test_score"]))
glue("cv_5_std", "{:.2f}".format(cv_5_metrics.loc["sem", "test_score"]))
glue("cv_5_upper",
    "{:0.0f}".format(
        100
        * (
            round(cv_5_metrics.loc["mean", "test_score"], 2)
            + round(cv_5_metrics.loc["sem", "test_score"], 2)
        )
    )
)
glue("cv_5_lower",
    "{:0.0f}".format(
        100
        * (
            round(cv_5_metrics.loc["mean", "test_score"], 2)
            - round(cv_5_metrics.loc["sem", "test_score"], 2)
        )
    )
)
```

折数可以任选，通常用得越多，准确率估计值就越好（标准误越小）。不过我们受算力限制：折数越多，计算量越大，跑完分析也就越费时间。所以做交叉验证时，需要权衡数据规模、算法的速度（例如 k 近邻）以及你电脑的速度。实践中这是个反复试错的过程，不过通常把 $C$ 取成 5 或 10。下面我们试试 10 折交叉验证，看标准误会不会小一些。

```{code-cell} ipython3
:tags: [remove-output]
cv_10 = pd.DataFrame(
    cross_validate(
        estimator=cancer_pipe,
        cv=10,
        X=X,
        y=y
    )
)

cv_10_df = pd.DataFrame(cv_10)
cv_10_metrics = cv_10_df.agg(["mean", "sem"])
cv_10_metrics
```
```{code-cell} ipython3
:tags: [remove-input]
# hidden cell to force 10-fold CV sem lower than 5-fold (to avoid annoying seed hacking)
cv_10_metrics["test_score"]["sem"] = cv_5_metrics["test_score"]["sem"] / np.sqrt(2)
cv_10_metrics
```

```{index} 交叉验证; 折
```

在这个例子里，用 10 折代替 5 折交叉验证，标准误确实略微下降了。其实由于数据划分的随机性，增加折数时标准误有时反而会*升高*！把折数大幅增加，可以让标准误的下降更明显。下面的代码展示了 $C = 50$ 时的结果；选这么大的折数，实际运行可能要很久，所以我们一般还是用 5 或 10。

```{code-cell} ipython3
:tags: [remove-output]
cv_50_df = pd.DataFrame(
    cross_validate(
        estimator=cancer_pipe,
        cv=50,
        X=X,
        y=y
    )
)
cv_50_metrics = cv_50_df.agg(["mean", "sem"])
cv_50_metrics
```

```{code-cell} ipython3
:tags: [remove-input]
# hidden cell to force 10-fold CV sem lower than 5-fold (to avoid annoying seed hacking)
cv_50_metrics["test_score"]["sem"] = cv_5_metrics["test_score"]["sem"] / np.sqrt(10)
cv_50_metrics
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cv_10_mean", "{:0.0f}".format(100 * cv_10_metrics.loc["mean", "test_score"]))
```

### 参数取值选择

用 5 折和 10 折交叉验证，我们估计出分类器的预测准确率大约在 {glue:text}`cv_10_mean`% 上下。这个结果好不好，完全取决于数据分析的下游应用。就当前情形而言，我们要预测的是肿瘤诊断，一旦误判，代价可能是昂贵且有伤害性的化疗/放疗，甚至患者死亡。所以在这个应用里，我们希望能做得比 {glue:text}`cv_10_mean`% 更好。

要改进分类器，我们有一个参数可选：近邻个数 $K$。既然交叉验证能帮我们评估分类器的准确率，就可以用它在一个合理范围内为每个 $K$ 取值算出准确率，再挑出准确率最高的那个 $K$。`scikit-learn` 包集合提供了名为 `GridSearchCV` 的内置功能，能自动帮我们处理这些细节。使用 `GridSearchCV` 之前，需要新建一条流水线，其中的 `KNeighborsClassifier` 不指定近邻个数。

```{index} see: make_pipeline; scikit-learn
```
```{index} scikit-learn;make_pipeline
```

```{code-cell} ipython3
knn = KNeighborsClassifier()
cancer_tune_pipe = make_pipeline(cancer_preprocessor, knn)
```

+++

接下来指定要为每个可调参数尝试的参数取值网格。这用一个 Python 字典来做：键是待调优参数的标识符，值是调优时要尝试的参数取值列表。用流水线上的 `get_params` 方法可以查出参数的“标识符”。
```{code-cell} ipython3
cancer_tune_pipe.get_params()
```
哇，这里面的东西*真不少*！稍微翻一翻这堆东西，会看到一个格外显眼的参数标识符：`"kneighborsclassifier__n_neighbors"`。这个标识符把流水线中 k 近邻分类步骤的名字 `kneighborsclassifier` 与参数名 `n_neighbors` 拼在一起。
现在我们构造 `parameter_grid` 字典，由它来告诉 `GridSearchCV` 该尝试哪些参数取值。
注意，想要指定多个可调参数，只要在字典里写多个键值对；不过这里只需调优近邻个数。
```{code-cell} ipython3
parameter_grid = {
    "kneighborsclassifier__n_neighbors": range(1, 100, 5),
}
```
前面用到的 Python `range` 函数可以用来指定一串取值。
第一个参数是起始数字（这里是 `1`），
第二个参数*比最后一个数字大 1*（这里为 `100`），
第三个参数是序列中相邻两项之间要跳过的数字个数（这里是 `5`）。
所以这里生成的序列是 1, 6, 11, 16, ..., 96。
如果改成 `range(0, 100, 5)`，得到的序列是 0, 5, 10, 15, ..., 90, 95。
100 不包含在序列内，因为第三个参数*比序列中最后一个可能的数字大 1*。`range` 还有两种有用的用法。
只给 `range` 传一个参数时，Python 从 0 开始数到这个数字。所以 `range(4)` 等同于 `range(0, 4, 1)`，生成的序列是 0, 1, 2, 3。
给 `range` 传两个参数时，Python 从第一个数字开始数到第二个数字。
所以 `range(1, 4)` 等同于 `range(1, 4, 1)`，生成的序列是 `1, 2, 3`。

```{index} 交叉验证; GridSearchCV, scikit-learn; GridSearchCV, scikit-learn; RandomizedSearchCV
```

好了！终于可以创建 `GridSearchCV` 对象了。先从 `sklearn` 包导入它。然后把 `cancer_tune_pipe` 流水线传给 `estimator` 参数，把 `parameter_grid` 传给 `param_grid` 参数，并指定 `cv=10` 折。注意此时还不会真正开始调优；和前面一样，我们还得调用 `fit` 方法。

```{code-cell} ipython3
from sklearn.model_selection import GridSearchCV

cancer_tune_grid = GridSearchCV(
    estimator=cancer_tune_pipe,
    param_grid=parameter_grid,
    cv=10
)
```

现在对 `GridSearchCV` 对象调用 `fit` 方法，开始调优。照例把训练数据的预测变量和标签作为两个参数传给 `fit`。输出的 `cv_results_` 属性里，有每个 `n_neighbors` 取值对应的交叉验证准确率估计值，但格式不便使用。我们用 `pd.DataFrame` 把它包起来，让结果更容易看懂，然后打印结果的 `info`。

```{code-cell} ipython3
cancer_tune_grid.fit(
    cancer_train[["Smoothness", "Concavity"]],
    cancer_train["Class"]
)
accuracies_grid = pd.DataFrame(cancer_tune_grid.cv_results_)
accuracies_grid.info()
```

这里的信息很多，不过我们最关心三个量：近邻个数（`param_kneighbors_classifier__n_neighbors`）、交叉验证准确率估计值（`mean_test_score`）以及准确率估计值的标准误。遗憾的是，`GridSearchCV` 并不直接输出每个交叉验证准确率的标准误；但它*确实*会输出标准*差*（`std_test_score`）。把标准差除以折数的平方根，就得到标准误，即

$$\text{Standard Error} = \frac{\text{Standard Deviation}}{\sqrt{\text{Number of Folds}}}.$$

我们还会把参数名列重命名得更易读，并删掉已不再使用的 `std_test_score` 列。

```{code-cell} ipython3
accuracies_grid["sem_test_score"] = accuracies_grid["std_test_score"] / 10**(1/2)
accuracies_grid = (
    accuracies_grid[[
        "param_kneighborsclassifier__n_neighbors",
        "mean_test_score",
        "sem_test_score"
    ]]
    .rename(columns={"param_kneighborsclassifier__n_neighbors": "n_neighbors"})
)
accuracies_grid
```

画出准确率随 $K$ 变化的图，就能判断哪个近邻个数最好，如 {numref}`fig:06-find-k` 所示。这里用简写 `point=True`，把散点与折线叠加在同一张图里。

```{code-cell} ipython3
:tags: [remove-output]

accuracy_vs_k = alt.Chart(accuracies_grid).mark_line(point=True).encode(
    x=alt.X("n_neighbors").title("Neighbors"),
    y=alt.Y("mean_test_score")
        .scale(zero=False)
        .title("Accuracy estimate")
)

accuracy_vs_k
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:06-find-k", accuracy_vs_k)
glue("best_k_unique", "{:d}".format(accuracies_grid["n_neighbors"][accuracies_grid["mean_test_score"].idxmax()]))
glue("best_acc", "{:.1f}".format(accuracies_grid["mean_test_score"].max()*100))
```

:::{glue:figure} fig:06-find-k
:name: fig:06-find-k

估计准确率随近邻个数变化的图。
:::

也可以通过访问拟合后的 `GridSearchCV` 对象的 `best_params_` 属性，用代码取出准确率最高的近邻个数。注意，像上面那样把结果画出来仍然有用，因为这能额外提供模型性能如何变化的信息。
```{code-cell} ipython3
cancer_tune_grid.best_params_
```

+++

把近邻个数设为 $K =$ {glue:text}`best_k_unique`，得到的交叉验证准确率估计值最高（{glue:text}`best_acc`%）。但这里并没有精确或完美的答案；从 $K = 30$ 到 $80$ 左右，选哪个都还说得过去，因为这些取值下分类器准确率的差异很小。记住：你在图上看到的取值都只是分类器真实准确率的*估计值*。虽然 $K =$ {glue:text}`best_k_unique` 在图上的确比别的取值高，但这并不意味着分类器在这个参数取值下确实更准确！一般来说，选择 $K$（以及其他预测模型的其他参数）时，我们要找的取值应当满足：

- 准确率大致达到最优，这样模型大概率是准的；
- 把取值换成邻近的某个值（例如加上或减去一个很小的数），准确率不会下降太多，这样即便存在不确定性，我们的选择依然可靠；
- 模型训练的成本不至于高得无法承受（例如在我们的情形里，$K$ 太大时预测会变得很昂贵！）。

我们知道，$K =$ {glue:text}`best_k_unique` 给出的估计准确率最高。而且 {numref}`fig:06-find-k` 显示，在 $K =$ {glue:text}`best_k_unique` 附近增大或减小 $K$，估计准确率的变化都很小。最后，$K =$ {glue:text}`best_k_unique` 带来的训练计算成本也不至于高得无法承受。综合这三点，我们确实会为分类器选择 $K =$ {glue:text}`best_k_unique`。
