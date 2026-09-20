## 用 `scikit-learn` 实现 k 近邻

```{index} scikit-learn
```

自己动手用 Python 编写 k 近邻算法，会变得相当复杂，尤其是还想处理多个类别、两个以上的变量，
或者要为多个新观测预测类别的时候。好在 Python 里的
[`scikit-learn` Python 包](https://scikit-learn.org/stable/index.html) {cite:p}`sklearn_api`
已经实现了 k 近邻算法，这个包还提供了许多[其他模型](https://scikit-learn.org/stable/user_guide.html)，
你在本章和本书后续各章都会遇到。使用 `scikit-learn` 包（在 Python 中名为 `sklearn`）里的函数，
能让代码更简单、更易读、也更准确；我们自己要写的代码越少，犯的错误通常也越少。
开始使用 k 近邻之前，需要先用 `set_config` 函数告诉 `sklearn` 包：
我们希望使用 `pandas` 数据框，而不是普通的数组。
```{note}
你会发现下面代码里有一种新的函数导入写法：`from ... import ...`。这样我们就能从 `sklearn` 中
*只*导入 `set_config`，之后调用 `set_config` 时也不必写包名前缀。本章和后续各章会大量使用 `from`
来导入函数，免得 `scikit-learn` 那些很长的名字把代码弄得杂乱不堪
（比如 `sklearn.neighbors.KNeighborsClassifier`，足足有 38 个字符！）。
```

```{code-cell} ipython3
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")
```

现在可以开始使用 k 近邻了。第一步是从 `sklearn.neighbors` 模块导入 `KNeighborsClassifier`。

```{code-cell} ipython3
from sklearn.neighbors import KNeighborsClassifier
```

下面我们来看看如何用 `KNeighborsClassifier` 完成 k 近邻分类。我们沿用前面的 `cancer` 数据集，
以 perimeter 和 concavity 作为预测变量、取 $K = 5$ 个近邻来构建分类器。然后用这个分类器
预测一个新观测的诊断标签：该观测的 perimeter 为 0、concavity 为 3.5，诊断标签未知。
我们先选出需要的两个预测变量和类别标签，存成 `cancer_train`：

```{code-cell} ipython3
cancer_train = cancer[["Class", "Perimeter", "Concavity"]]
cancer_train
```

```{index} scikit-learn; 模型对象, scikit-learn; KNeighborsClassifier
```

接下来，我们创建一个 `KNeighborsClassifier` 实例，得到用于 k 近邻分类的*模型对象*（model object），
并指定使用 $K = 5$ 个近邻；如何选择 $K$ 留到下一章讨论。

```{note}
你可以指定 `weights` 参数，来控制分类新观测时近邻如何投票。默认取值是 `"uniform"`，也就是前面说的：
$K$ 个最近邻每个各投 1 票。其他取值会给每个近邻的票以不同的权重，具体见
[`scikit-learn` 网站](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html?highlight=kneighborsclassifier#sklearn.neighbors.KNeighborsClassifier)。
```

```{code-cell} ipython3
knn = KNeighborsClassifier(n_neighbors=5)
knn
```

```{index} scikit-learn; fit, scikit-learn; 预测变量, scikit-learn; 响应变量
```

要在乳腺癌数据上拟合模型，需要调用模型对象的 `fit` 方法。`X` 参数用来指定预测变量的数据，
`y` 参数用来指定响应变量的数据。所以下面我们设置 `X=cancer_train[["Perimeter", "Concavity"]]` 和
`y=cancer_train["Class"]`，表示 `Class` 是响应变量（也就是我们要预测的变量），而 `Perimeter` 和
`Concavity` 都作为预测变量。注意，`fit` 函数从外面看似乎没做什么，实际上训练 k 近邻模型的
苦活累活全是它干的，它还会修改 `knn` 模型对象。

```{code-cell} ipython3
knn.fit(X=cancer_train[["Perimeter", "Concavity"]], y=cancer_train["Class"]);
```

```{index} scikit-learn; predict
```

用过 `fit` 函数之后，只要把新观测本身传给分类器对象并调用 `predict`，就能对它做出预测。
和前面手工运行 k 近邻分类算法一样，`knn` 模型对象把这个新观测判为“Malignant”。注意，
`predict` 函数输出的是装着模型预测结果的 `array`；你其实可以用 `predict` 一次预测多个观测，
输出之所以存成 `array` 就是这个原因。

```{code-cell} ipython3
new_obs = pd.DataFrame({"Perimeter": [0], "Concavity": [3.5]})
knn.predict(new_obs)
```

这个预测出的恶性肿瘤标签，是这个观测的真实类别吗？我们并不知道，
因为这个观测的诊断结果我们根本没有——我们要预测的正是它！分类器的预测不一定正确，
但下一章我们会学习一些方法，来量化我们认为自己的预测有多准确。

+++

## 用 `scikit-learn` 做数据预处理

### 中心化与缩放

```{index} 缩放
```

使用 k 近邻分类时，每个变量的*标度*（即取值的大小与范围）都起作用。分类器靠找出离新观测最近的观测
来判定类别，所以标度大的变量，影响会远大于标度小的变量。但变量标度大，*并不意味着*它对做出准确预测
更重要。举个例子，假设有个数据集包含两个特征：工资（以美元计）和受教育年限，你想预测相应的工作类型。
计算近邻距离时，1000 美元的差别与 10 年受教育年限的差别相比，前者在数值上大得多。
但就理解问题、回答问题的需要而言，情况恰恰相反：与年薪相差 1000 美元相比，
10 年的受教育年限差别才是巨大的！

+++

```{index} 中心化
```

在许多其他预测模型里，每个变量的*中心*（例如它的均值）同样重要。举例来说，假设有一份数据集，
其中的温度用开尔文度测量；另有一份内容相同的数据集，温度用摄氏度测量，这两个变量就相差一个常数 273
（尽管它们包含的信息完全相同）。同样，在前面那个假设的工作分类例子里，我们多半会看到
工资变量的中心在数万这一量级，而受教育年限变量的中心只有个位数。这一点虽然不影响
k 近邻分类算法，但这么大的平移却会改变许多其他预测模型的结果。

```{index} 标准化; k 近邻
```

要对数据做缩放和中心化，需要先求出变量的*均值*（也就是平均数，用来刻画一组数值的“中心”位置）
和*标准差*（用来衡量取值有多分散）。对变量的每个观测值，都减去均值（即对变量做中心化），
再除以标准差（即对变量做缩放）。做完这一步，数据就称为*标准化*数据，
数据集中所有变量的均值都是 0、标准差都是 1。为了展示标准化会给 k 近邻算法带来什么影响，
我们读取未经标准化的原始威斯康星乳腺癌数据集；在此之前，我们用的都是标准化之后的版本。
我们采用与前面相同的初始整理步骤，并且为了简单起见，只用 `Area`、`Smoothness` 和 `Class` 这三个变量：

```{code-cell} ipython3
unscaled_cancer = pd.read_csv("data/wdbc_unscaled.csv")[["Class", "Area", "Smoothness"]]
unscaled_cancer["Class"] = unscaled_cancer["Class"].replace({
   "M" : "Malignant",
   "B" : "Benign"
})
unscaled_cancer
```

看看上面这份既未缩放、也未中心化的数据，你会看到面积测量值之间的差异远大于光滑度测量值之间的差异。
这会影响预测吗？为了弄清楚，我们要为这两个预测变量画散点图（按诊断结果着色），
一份用刚刚读入的未标准化数据，一份用同一份数据标准化后的版本。但首先，
我们需要用 `scikit-learn` 把 `unscaled_cancer` 数据集标准化。

```{index} see: Pipeline; scikit-learn
```

```{index} see: make_column_transformer; scikit-learn
```

```{index} scikit-learn;Pipeline, scikit-learn; make_column_transformer
```

`scikit-learn` 框架提供了一组*预处理器*（preprocessor），用来加工数据，
它们都位于 [`preprocessing` 模块](https://scikit-learn.org/stable/modules/preprocessing.html)中。
这里我们用 `StandardScaler` 转换器把 `unscaled_cancer` 数据中的预测变量标准化。
要告诉 `StandardScaler` 该标准化哪些变量，需要用
[`make_column_transformer`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.make_column_transformer.html#sklearn.compose.make_column_transformer) 函数
把它包进一个 [`ColumnTransformer`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html#sklearn.compose.ColumnTransformer) 对象。
`ColumnTransformer` 对象还支持同时使用多个预处理器，当你想对每个预测变量分别做不同的预处理时，
这一点特别方便。`make_column_transformer` 函数的主要参数是一串配对：（1）一个预处理器，
（2）你想把该预处理器应用到哪些列。在本例中，我们只有 `StandardScaler` 这一个预处理器，
把它应用到 `Area` 和 `Smoothness` 两列上。

```{code-cell} ipython3
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer

preprocessor = make_column_transformer(
    (StandardScaler(), ["Area", "Smoothness"]),
)
preprocessor
```

```{index} scikit-learn; make_column_transformer, scikit-learn; StandardScaler 
```

```{index} see: StandardScaler; scikit-learn
```

```{index} scikit-learn; fit, scikit-learn; make_column_selector, scikit-learn; StandardScaler
```

可以看到，这个预处理器只包含一个标准化步骤，应用到 `Area` 和 `Smoothness` 两列。注意，
这里我们是靠逐个写出列名，来指定把预处理步骤应用到哪些列的；当预测变量很多时，这种做法会变得相当困难。
与其逐一写出列名，我们可以改用
[`make_column_selector`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.make_column_selector.html#sklearn.compose.make_column_selector) 函数。
例如，若想把所有*数值型*预测变量都标准化，可以用 `make_column_selector`，
并把 `dtype_include` 参数指定为 `"number"`。这样创建的预处理器与前面那个等价。

```{code-cell} ipython3
from sklearn.compose import make_column_selector

preprocessor = make_column_transformer(
    (StandardScaler(), make_column_selector(dtype_include="number")),
)
preprocessor
```

```{index} see: fit ; scikit-learn
```

```{index} scikit-learn; transform
```

现在可以标准化 `unscaled_cancer` 数据框里的数值型预测变量列了。这分两步完成。
先调用 `fit` 函数，把 `unscaled_cancer` 数据作为参数传进去，算出实施标准化所需的量
（每个变量的均值和标准差）。再用 `transform` 函数真正实施标准化。
为了标准化数据而分两步——`fit` *和* `transform`——似乎有点多余。但正因为分两步，
我们才能在 `transform` 这一步指定另一份数据。这样就能用一份数据算出标准化所需的量，
再把同一套标准化应用到另一份数据上。

```{code-cell} ipython3
preprocessor.fit(unscaled_cancer)
scaled_cancer = preprocessor.transform(unscaled_cancer)
scaled_cancer
```
```{code-cell} ipython3
:tags: [remove-cell]
glue("scaled-cancer-column-0", '"'+scaled_cancer.columns[0]+'"')
glue("scaled-cancer-column-1", '"'+scaled_cancer.columns[1]+'"')
```
看起来 `Smoothness` 和 `Area` 变量已经标准化了。好耶！不过新的 `scaled_cancer` 数据框
有两点值得注意。第一，它只保留 `transform` 输入（这里是 `unscaled_cancer`）中
经过预处理步骤的那些列。我们用 `make_column_transformer` 构建的 `ColumnTransformer`，
默认行为是*丢掉*其余各列。这个默认行为与 `sklearn` 的其他部分配合得很好
（下面 {numref}`08:puttingittogetherworkflow` 就会讲到），但如果想可视化预处理的结果，
保留原数据框中的其他列（比如这里的 `Class` 变量）会很有用。要保留其他列，
需要在 `make_column_transformer` 函数中把 `remainder` 参数设为 `"passthrough"`。此外你会看到，
新的列名——{glue:text}`scaled-cancer-column-0` 和 {glue:text}`scaled-cancer-column-1`——
里包含了预处理步骤的名字，两者之间用下划线分隔。这个默认行为在 `sklearn` 中很有用，
因为我们有时会对同样的列应用多个不同的预处理步骤；但同样地，为了可视化，
保留原来的列名会很有用。要保留原列名，需要把 `verbose_feature_names_out` 参数设为 `False`。

```{note}
只有在你想要查看预处理步骤的结果时，才需要指定 `remainder` 和 `verbose_feature_names_out` 参数。
大多数情况下，应当让这两个参数保持默认值。
```

```{code-cell} ipython3
preprocessor_keep_all = make_column_transformer(
    (StandardScaler(), make_column_selector(dtype_include="number")),
    remainder="passthrough",
    verbose_feature_names_out=False
)
preprocessor_keep_all.fit(unscaled_cancer)
scaled_cancer_all = preprocessor_keep_all.transform(unscaled_cancer)
scaled_cancer_all
```

你可能会奇怪：为了给变量做中心化和缩放，何必费这么大劲？难道不能在构建 k 近邻模型之前，
自己动手把 `Area` 和 `Smoothness` 变量缩放、中心化吗？严格说，*可以*；但这样做容易出错。
特别是，我们可能在预测时忘了套用同样的中心化／缩放，也可能不小心用了与训练时*不同*的中心化／缩放。
正确使用 `ColumnTransformer`，能让代码更简单、更易读、也不易出错。另外请注意，
只有你想亲自查看预处理步骤的结果时，才需要在预处理器上调用 `fit` 和 `transform`。
稍后在 {numref}`08:puttingittogetherworkflow` 中你会看到，`scikit-learn` 提供了一些工具，
可以自动把预处理器和模型衔接好，这样你就能按需在 `Pipeline` 上调用 `fit` 和 `transform`，
不必额外写代码。

{numref}`fig:05-scaling-plt` 并排展示了两张散点图——一张对应 `unscaled_cancer`，一张对应 `scaled_cancer`。
两张图都标出了同一个新观测以及它的 $K=3$ 个最近邻。在未标准化数据那张图里，
三个最近邻选得有些奇怪。这些“近邻”从图上看明显落在良性观测的密集区域内部，
而且都与新观测近乎排成一条垂直线（所以这张图看起来只有一条黑线）。
{numref}`fig:05-scaling-plt-zoomed` 放大了未标准化图上这一区域的细节。在这里，
最近邻的计算被标度大得多的面积变量主导了。{numref}`fig:05-scaling-plt` 右侧标准化数据的图，
所选的最近邻就直观合理得多。可见，在使用预测算法时，对数据做标准化可能会带来重要改变。
标准化应当成为你预测建模之前预处理工作的一部分，并且你始终要仔细考虑自己面对的问题领域，
想清楚是否需要标准化数据。

```{code-cell} ipython3
:tags: [remove-cell]

def class_dscp(x):
    if x == "M":
        return "Malignant"
    elif x == "B":
        return "Benign"
    else:
        return x


attrs = ["Area", "Smoothness"]
new_obs = pd.DataFrame({"Class": ["Unknown"], "Area": 400, "Smoothness": 0.135})
unscaled_cancer["Class"] = unscaled_cancer["Class"].apply(class_dscp)
area_smoothness_new_df = pd.concat((unscaled_cancer, new_obs), ignore_index=True)
my_distances = euclidean_distances(area_smoothness_new_df[attrs])[
    len(unscaled_cancer)
][:-1]
area_smoothness_new_point = (
    alt.Chart(
        area_smoothness_new_df,
        title=alt.TitleParams(text="Unstandardized data", anchor="start"),
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Area"),
        y=alt.Y("Smoothness"),
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

# The index of 3 rows that has smallest distance to the new point
min_3_idx = np.argpartition(my_distances, 3)[:3]
neighbor1 = pd.concat([
    unscaled_cancer.loc[[min_3_idx[0]], attrs],
    new_obs[attrs],
])
neighbor2 = pd.concat([
    unscaled_cancer.loc[[min_3_idx[1]], attrs],
    new_obs[attrs],
])
neighbor3 = pd.concat([
    unscaled_cancer.loc[[min_3_idx[2]], attrs],
    new_obs[attrs],
])

line1 = (
    alt.Chart(neighbor1)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)
line2 = (
    alt.Chart(neighbor2)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)
line3 = (
    alt.Chart(neighbor3)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)

area_smoothness_new_point = area_smoothness_new_point + line1 + line2 + line3
```

```{code-cell} ipython3
:tags: [remove-cell]

attrs = ["Area", "Smoothness"]
new_obs_scaled = pd.DataFrame({"Class": ["Unknown"], "Area": -0.72, "Smoothness": 2.8})
scaled_cancer_all["Class"] = scaled_cancer_all["Class"].apply(class_dscp)
area_smoothness_new_df_scaled = pd.concat(
    (scaled_cancer_all, new_obs_scaled), ignore_index=True
)
my_distances_scaled = euclidean_distances(area_smoothness_new_df_scaled[attrs])[
    len(scaled_cancer_all)
][:-1]
area_smoothness_new_point_scaled = (
    alt.Chart(
        area_smoothness_new_df_scaled,
        title=alt.TitleParams(text="Standardized data", anchor="start"),
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Area", title="Area (standardized)"),
        y=alt.Y("Smoothness", title="Smoothness (standardized)"),
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
min_3_idx_scaled = np.argpartition(my_distances_scaled, 3)[:3]
neighbor1_scaled = pd.concat([
    scaled_cancer_all.loc[[min_3_idx_scaled[0]], attrs],
    new_obs_scaled[attrs],
])
neighbor2_scaled = pd.concat([
    scaled_cancer_all.loc[[min_3_idx_scaled[1]], attrs],
    new_obs_scaled[attrs],
])
neighbor3_scaled = pd.concat([
    scaled_cancer_all.loc[[min_3_idx_scaled[2]], attrs],
    new_obs_scaled[attrs],
])

line1_scaled = (
    alt.Chart(neighbor1_scaled)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)
line2_scaled = (
    alt.Chart(neighbor2_scaled)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)
line3_scaled = (
    alt.Chart(neighbor3_scaled)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)

area_smoothness_new_point_scaled = (
    area_smoothness_new_point_scaled + line1_scaled + line2_scaled + line3_scaled
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue(
    "fig:05-scaling-plt",
    area_smoothness_new_point | area_smoothness_new_point_scaled
)
```

:::{glue:figure} fig:05-scaling-plt
:name: fig:05-scaling-plt

未标准化数据与标准化数据下 K = 3 个最近邻的比较。
:::

```{code-cell} ipython3
:tags: [remove-cell]

zoom_area_smoothness_new_point = (
    alt.Chart(
        area_smoothness_new_df,
        title=alt.TitleParams(text="Unstandardized data", anchor="start"),
    )
    .mark_point(clip=True, opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Area", scale=alt.Scale(domain=(395, 405))),
        y=alt.Y("Smoothness", scale=alt.Scale(domain=(0.08, 0.14))),
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
zoom_area_smoothness_new_point + line1 + line2 + line3
glue("fig:05-scaling-plt-zoomed", (zoom_area_smoothness_new_point + line1 + line2 + line3))
```

:::{glue:figure} fig:05-scaling-plt-zoomed
:name: fig:05-scaling-plt-zoomed

未标准化数据下三个最近邻的放大图。
:::

