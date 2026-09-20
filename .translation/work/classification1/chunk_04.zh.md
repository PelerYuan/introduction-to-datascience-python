+++

### 平衡

```{index} 平衡, 不平衡
```

分类器所用的数据集还可能存在另一个问题：*类别不平衡（class imbalance）*，也就是某个标签比另一个标签常见得多。像 k 近邻算法这样的分类器，会用附近数据点的标签来预测新数据点的标签；因此，如果总体上看带某个标签的数据点数量多得多，算法总体上就更可能选中这个标签（即使数据呈现的“模式”提示的并非如此）。类别不平衡其实相当常见，也很重要：从罕见病诊断到恶意邮件识别，很多场景中真正需要识别出的那个“重要”类别（患病、恶意邮件）都比“不重要”的类别（未患病、正常邮件）稀有得多。

```{index} concat
```

为了更好地说明这个问题，我们再来看看标准化后的乳腺癌数据 `cancer`；只不过这次要删去大量恶性肿瘤观测，模拟癌症罕见时数据会呈现什么样子。具体做法是只从恶性肿瘤一组中挑出 3 条观测，良性观测则全部保留。这 3 条观测用 `.head()` 方法选取，该方法会从数据框顶部取指定的行数。接着，我们用 `pandas` 中的 [`concat`](https://pandas.pydata.org/docs/reference/api/pandas.concat.html) 函数把过滤后得到的两个数据框粘回一起。`concat` 函数沿某个轴*拼接*数据框：默认沿 `axis=0` 纵向拼接，把两个数据框合成单个*更高*的数据框，这正是我们这里想要的；如果想横向拼接、得到*更宽*的数据框，就要指定 `axis=1`。新的不平衡数据见 {numref}`fig:05-unbalanced`，各类别的计数我们则用 `value_counts` 函数打印出来。

```{code-cell} ipython3
:tags: ["remove-output"]
rare_cancer = pd.concat((
    cancer[cancer["Class"] == "Benign"],
    cancer[cancer["Class"] == "Malignant"].head(3)
))

rare_plot = alt.Chart(rare_cancer).mark_circle().encode(
    x=alt.X("Perimeter").title("Perimeter (standardized)"),
    y=alt.Y("Concavity").title("Concavity (standardized)"),
    color=alt.Color("Class").title("Diagnosis")
)
rare_plot
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("fig:05-unbalanced", rare_plot)
```

:::{glue:figure} fig:05-unbalanced
:name: fig:05-unbalanced

不平衡数据。
:::

```{code-cell} ipython3
rare_cancer["Class"].value_counts()
```

+++

假设现在我们决定在 k 近邻分类中取 $K = 7$。恶性肿瘤只有 3 条观测，于是分类器*无论肿瘤的凹度和周长是多少，都会预测它是良性的！*这是因为在 7 条观测的多数投票中，最多只有 3 条是恶性的（恶性肿瘤观测总共只有 3 条），所以至少 4 条必然是良性的，良性一方总会胜出。例如，{numref}`fig:05-upsample` 展示了一个新肿瘤观测的情形：它与训练数据中被标为恶性的 3 条观测相当接近。

```{code-cell} ipython3
:tags: [remove-cell]

attrs = ["Perimeter", "Concavity"]
new_point = [2, 2]
new_point_df = pd.DataFrame(
    {"Class": ["Unknown"], "Perimeter": new_point[0], "Concavity": new_point[1]}
)
rare_cancer["Class"] = rare_cancer["Class"].apply(class_dscp)
rare_cancer_with_new_df = pd.concat((rare_cancer, new_point_df), ignore_index=True)
my_distances = euclidean_distances(rare_cancer_with_new_df[attrs])[
    len(rare_cancer)
][:-1]

# First layer: scatter plot, with unknwon point labeled as red "unknown" diamond
rare_plot = (
    alt.Chart(
        rare_cancer_with_new_df
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Perimeter", title="Perimeter (standardized)"),
        y=alt.Y("Concavity", title="Concavity (standardized)"),
        color=alt.Color(
            "Class",
            title="Diagnosis",
        ),
        shape=alt.Shape(
            "Class", scale=alt.Scale(range=["circle", "circle", "diamond"])
        ),
        size=alt.condition("datum.Class == 'Unknown'", alt.value(80), alt.value(30)),
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None))
    )
)

# Find the 7 NNs
min_7_idx = np.argpartition(my_distances, 7)[:7]

# For loop: each iteration adds a line segment of corresponding color
for i in range(7):
    clr = "#1f77b4"
    if rare_cancer.iloc[min_7_idx[i], :]["Class"] == "Malignant":
        clr = "#ff7f0e"
    neighbor = pd.concat([
        rare_cancer.iloc[[min_7_idx[i]], :][attrs],
        new_point_df[attrs],
    ])
    rare_plot = rare_plot + (
        alt.Chart(neighbor)
        .mark_line(opacity=0.3)
        .encode(x="Perimeter", y="Concavity", color=alt.value(clr))
    )

glue("fig:05-upsample", rare_plot)
```

:::{glue:figure} fig:05-upsample
:name: fig:05-upsample

不平衡数据，其中突出显示了新观测的 7 个最近邻。
:::

+++

{numref}`fig:05-upsample-2` 展示了另一种情形：把图中每个区域的背景颜色设为 k 近邻分类器对该位置的新观测会给出的预测。可以看到，判别结果始终是“良性”，对应蓝色。

```{code-cell} ipython3
:tags: [remove-cell]

knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(X=rare_cancer[["Perimeter", "Concavity"]], y=rare_cancer["Class"])

# create a prediction pt grid
per_grid = np.linspace(
    rare_cancer["Perimeter"].min() * 1.05, rare_cancer["Perimeter"].max() * 1.05, 50
)
con_grid = np.linspace(
    rare_cancer["Concavity"].min() * 1.05, rare_cancer["Concavity"].max() * 1.05, 50
)
pcgrid = np.array(np.meshgrid(per_grid, con_grid)).reshape(2, -1).T
pcgrid = pd.DataFrame(pcgrid, columns=["Perimeter", "Concavity"])
pcgrid

knnPredGrid = knn.predict(pcgrid)
prediction_table = pcgrid.copy()
prediction_table["Class"] = knnPredGrid
prediction_table

# create the scatter plot
rare_plot = (
    alt.Chart(
        rare_cancer,
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Perimeter", title="Perimeter (standardized)"),
        y=alt.Y("Concavity", title="Concavity (standardized)"),
        color=alt.Color("Class", title="Diagnosis"),
    )
)

# add a prediction layer, also scatter plot
prediction_plot = (
    alt.Chart(
        prediction_table,
        title="Imbalanced data",
    )
    .mark_point(opacity=0.05, filled=True, size=300)
    .encode(
        x=alt.X(
            "Perimeter",
            title="Perimeter (standardized)",
            scale=alt.Scale(
                domain=(rare_cancer["Perimeter"].min() * 1.05, rare_cancer["Perimeter"].max() * 1.05),
                nice=False
            ),
        ),
        y=alt.Y(
            "Concavity",
            title="Concavity (standardized)",
            scale=alt.Scale(
                domain=(rare_cancer["Concavity"].min() * 1.05, rare_cancer["Concavity"].max() * 1.05),
                nice=False
            ),
        ),
        color=alt.Color("Class", title="Diagnosis"),
    )
)
#rare_plot + prediction_plot
glue("fig:05-upsample-2", (rare_plot + prediction_plot))
```

:::{glue:figure} fig:05-upsample-2
:name: fig:05-upsample-2

不平衡数据，背景颜色表示分类器的判别结果，点表示有标签数据。
:::

+++

```{index} 过采样, DataFrame; sample
```

这个问题虽然简单，但要把它处理得在统计上站得住脚，其实相当微妙；真要讲清楚，所需的细节和数学远超本书的范围。就目前的目的而言，只要对稀有类做*过采样（oversampling）*来重新平衡数据就足够了。也就是说，我们在数据集中把稀有观测重复若干次，让它们在 k 近邻算法中获得更大的表决权。为此，我们先用筛选把各个类别拆成各自的数据框；然后对稀有类的数据框使用 `sample` 方法，把 `Malignant` 观测的条数增加到与 `Benign` 观测相同：把 `n` 参数设为想要的 `Malignant` 观测条数，并设 `replace=True` 表示有放回抽样。最后用 `value_counts` 方法查看各类别现在是否已经平衡。注意，`sample` 是*随机*挑选要复制哪些数据的；如何正确处理数据分析中的随机性，我们将在 {numref}`第 %s 章 <classification2>` 中进一步学习。

```{code-cell} ipython3
:tags: [remove-cell]
# hidden seed call to make the below resample reproducible
# we haven't taught students about seeds / prngs yet, so
# for now just hide this.
np.random.seed(1)
```

```{code-cell} ipython3
malignant_cancer = rare_cancer[rare_cancer["Class"] == "Malignant"]
benign_cancer = rare_cancer[rare_cancer["Class"] == "Benign"]
malignant_cancer_upsample = malignant_cancer.sample(
    n=benign_cancer.shape[0], replace=True
)
upsampled_cancer = pd.concat((malignant_cancer_upsample, benign_cancer))
upsampled_cancer["Class"].value_counts()
```

现在假设我们在这个*平衡*数据上用 $K=7$ 训练 k 近邻分类器。这时再把散点图每个区域的背景颜色设为 k 近邻分类器会给出的判别结果，就得到 {numref}`fig:05-upsample-plot` 所示的情形。可以看到，判别结果合理多了：点靠近标为恶性的观测时，分类器就预测为恶性肿瘤；反过来，点更接近良性肿瘤观测时，就预测为良性。

```{code-cell} ipython3
:tags: [remove-cell]

knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(
    X=upsampled_cancer[["Perimeter", "Concavity"]], y=upsampled_cancer["Class"]
)

# create a prediction pt grid
knnPredGrid = knn.predict(pcgrid)
prediction_table = pcgrid
prediction_table["Class"] = knnPredGrid

# create the scatter plot
rare_plot = (
    alt.Chart(rare_cancer)
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X(
            "Perimeter",
            title="Perimeter (standardized)",
            scale=alt.Scale(
                domain=(rare_cancer["Perimeter"].min() * 1.05, rare_cancer["Perimeter"].max() * 1.05),
                nice=False
            ),
        ),
        y=alt.Y(
            "Concavity",
            title="Concavity (standardized)",
            scale=alt.Scale(
                domain=(rare_cancer["Concavity"].min() * 1.05, rare_cancer["Concavity"].max() * 1.05),
                nice=False
            ),
        ),
        color=alt.Color("Class", title="Diagnosis"),
    )
)

# add a prediction layer, also scatter plot
upsampled_plot = (
    alt.Chart(prediction_table)
    .mark_point(opacity=0.05, filled=True, size=300)
    .encode(
        x=alt.X("Perimeter", title="Perimeter (standardized)"),
        y=alt.Y("Concavity", title="Concavity (standardized)"),
        color=alt.Color("Class", title="Diagnosis"),
    )
)
#rare_plot + upsampled_plot
glue("fig:05-upsample-plot", (rare_plot + upsampled_plot))
```

:::{glue:figure} fig:05-upsample-plot
:name: fig:05-upsample-plot

上采样后的数据，背景颜色表示分类器的判别结果。
:::

### 缺失数据

```{index} 缺失数据
```

实际数据集最常见的问题之一就是*缺失数据*，也就是某些变量的取值没有被记录下来的那些观测。遗憾的是，缺失数据虽然常见，要妥善处理却非常困难，通常要依靠关于数据本身、数据背景以及数据收集方式的专门知识。缺失数据带来的一个典型难题是：缺失项本身可能*有信息量*，也就是说，某些项之所以缺失，与其它变量的取值有关。例如，来自边缘群体的调查对象如果担心如实回答会带来负面后果，就可能不太愿意回答某类问题。这时，倘若我们干脆把带缺失项的数据丢掉，就会在无意中剔除掉该群体的大量成员，使调查结论产生偏差。因此，在真实问题中忽视这一点，很容易得出误导性的分析结果，造成有害影响。本书只介绍这样一类处理缺失项的技巧：缺失项仅仅是“随机缺失”，即某些项之所以缺失，*与观测的其它方面毫无关系*。

我们加载并查看肿瘤图像数据的一个修改版子集，其中含有少量缺失项：

```{code-cell} ipython3
missing_cancer = pd.read_csv("data/wdbc_missing.csv")[["Class", "Radius", "Texture", "Perimeter"]]
missing_cancer["Class"] = missing_cancer["Class"].replace({
   "M" : "Malignant",
   "B" : "Benign"
})
missing_cancer
```

回想一下，k 近邻分类通过计算到附近训练观测的直线距离来做预测，因此需要用到训练数据中*所有*观测的*所有*变量取值。那么，数据存在缺失时该怎么用 k 近邻分类呢？既然带缺失项的观测并不算多，一种办法就是在构建 k 近邻分类器之前直接把这些观测删掉。要做到这一点，只需在开始处理数据之前使用 `dropna` 方法。

```{index} 缺失数据; dropna
```

```{code-cell} ipython3
no_missing_cancer = missing_cancer.dropna()
no_missing_cancer
```

不过，如果很多行都含有缺失项，这个办法就行不通了，因为最后可能丢掉太多数据。此时另一种可行做法是对缺失项做*插补*，也就是根据数据集中其它观测填上合成取值。一个合理的选择是*均值插补*，即用每个变量中现有取值的均值来填补缺失项。做均值插补时，我们使用 `SimpleImputer` 变换器并采用默认参数，再用 `make_column_transformer` 指明哪些列需要插补。

```{index} scikit-learn; SimpleImputer, 缺失数据; 均值插补
```

```{code-cell} ipython3
from sklearn.impute import SimpleImputer

preprocessor = make_column_transformer(
    (SimpleImputer(), ["Radius", "Texture", "Perimeter"]),
    verbose_feature_names_out=False
)
preprocessor
```

为了直观看出均值插补做了什么，我们直接用 `fit` 和 `transform` 函数把变换器应用到 `missing_cancer` 数据框上。插补这一步会用各变量自身的均值填补相应的缺失项。

```{code-cell} ipython3
preprocessor.fit(missing_cancer)
imputed_cancer = preprocessor.transform(missing_cancer)
imputed_cancer
```

缺失数据插补还有许多其它做法，可参见 [`scikit-learn` 文档](https://scikit-learn.org/stable/modules/impute.html)。无论你在数据分析中决定如何处理缺失数据，批判性地思考数据背景、数据收集方式以及你正要回答的问题，始终都至关重要。

+++

(08:puttingittogetherworkflow)=
