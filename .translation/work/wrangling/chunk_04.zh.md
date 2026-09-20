+++

我们先来看看如何计算：报告自己把某种特定语言作为在家主要使用语言的加拿大人数，最少和最多各是多少。
首先回顾一下 `region_lang` 的样子：

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang = pd.read_csv("data/region_lang.csv")
region_lang
```

```{index} Series; 最小, Series; 最大
```

对于任一地区，我们用 `.min` 算出把某种特定语言作为在家主要使用语言的加拿大人数最少是多少，
用 `.max` 算出最多是多少。

```{code-cell} ipython3
region_lang["most_at_home"].min()
```

```{code-cell} ipython3
region_lang["most_at_home"].max()
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("lang_most_people", "{0:,.0f}".format(int(region_lang["most_at_home"].max())))
```

由此可以看到，数据集中有些语言没有任何人作为在家主要使用语言。我们还看到，
使用人数最多的在家主要使用语言，有 {glue:text}`lang_most_people` 人使用。如果你想知道的是
这次调查中的总人数，也可以用 `sum` 这个汇总统计量方法。
```{code-cell} ipython3
region_lang["most_at_home"].sum()
```

```{index} Series; 求和, Series; 均值, Series; 中位数, Series; 标准差, 汇总统计量
```

其他常用的汇总统计量还有 `mean`、`median` 和 `std`，三者分别用来计算观测的均值、中位数和标准差。
我们还可以用 `agg` 一次算出多个统计量，把结果“聚合”起来。例如，如果想一次同时算出 `min` 和 `max`，
可以给 `agg` 传入参数 `["min", "max"]`。请注意，`agg` 输出的是一个 `Series` 对象。

```{code-cell} ipython3
region_lang["most_at_home"].agg(["min", "max"])
```

`pandas` 包还提供了 `describe` 方法。这个函数很好用，能一次算出许多常用的汇总统计量，
给出变量的*汇总*。

```{code-cell} ipython3
region_lang["most_at_home"].describe()
```

除了前面介绍的汇总方法，`describe` 方法还会输出 `count`（数据框中观测的总数，也就是行数），
以及第 25、第 50 和第 75 百分位数。{numref}`tab:basic-summary-statistics` 概览了一些有用的
汇总统计量，它们都可以用 `pandas` 算出来。

```{table} 基础汇总统计量
:name: tab:basic-summary-statistics
| Function | Description |
| -------- | ----------- |
| `count` | 观测（行）的个数 |
| `mean` | 观测的均值 |
| `median` | 观测的中位数 |
| `std` | 观测的标准差 |
| `max` | 一列中的最大值 |
| `min` | 一列中的最小值 |
| `sum` | 所有观测的求和 |
| `agg` | 一次聚合多个统计量 |
| `describe` | 汇总 |
```

+++
+++

```{index} see: NaN; 缺失数据
```

```{index} 缺失数据
```


```{note}
在 `pandas` 中，`NaN` 这个取值常用来表示缺失数据。
默认情况下，`pandas` 计算汇总统计量（如 `max`、`min`、`sum` 等）时会忽略这些取值。
如果你查看这些函数的文档，会看到一个输入变量 `skipna`，它默认被设为 `skipna=True`。
也就是说，`pandas` 在计算统计量时会跳过 `NaN` 取值。
```

### 在数据框上计算汇总统计量

如果你想在整张数据框上计算汇总统计量，该怎么办？其实，{numref}`tab:basic-summary-statistics`
里的函数可以直接用在整个数据框上！
例如，我们可以用 `max` 求出每一列的最大值。

```{code-cell} ipython3
region_lang.max()
```

可以看到，对于包含 `"Vancouver"`、`"Halifax"` 这类字符串数据的列，最大值是这样确定的：
把字符串按字母顺序排序，然后返回最后一个。如果只想要数值列的最大值，
可以传入 `numeric_only=True`：

```{code-cell} ipython3
region_lang.max(numeric_only=True)
```

我们也可以求数据框中每一列的 `mean`。对字符串列求均值没有意义，
所以这里*必须*提供关键字参数 `numeric_only=True`，让均值只在数值列上计算。

```{code-cell} ipython3
region_lang.mean(numeric_only=True)
```

如果你只想对其中一部分列求汇总统计量，可以先用 `[]` 或 `.loc[]` 选出这些列，
再像前面处理单列那样求汇总统计量。例如，要得到 `"mother_tongue"` 到 `"lang_known"`
之间所有列的均值和标准差，可以先用 `.loc[]` 选出这些列，再用 `agg` 同时求 `mean` 和 `std`。
```{code-cell} ipython3
region_lang.loc[:, "mother_tongue":"lang_known"].agg(["mean", "std"])
```

## 使用 `groupby` 对分组后的行执行操作

+++

```{index} DataFrame; groupby
```
如果想了解语言在不同地区之间有什么差异，该怎么办？这时就需要一个新工具，用来按地区把行分组。
用 `pandas` 中的 `groupby` 函数就能做到。把汇总函数与 `groupby` 搭配使用，
就可以按数据集内部的子组汇总取值，如 {numref}`fig:summarize-groupby` 所示。
例如，我们可以用 `groupby` 把 `tidy_lang` 数据框按地区分组，然后计算数据集中每个地区
把这种语言作为在家主要使用语言的加拿大人数的最小值和最大值。

+++ {"tags": []}

```{figure} img/wrangling/summarize.002.png
:name: fig:summarize-groupby
:figclass: figure

把汇总统计量函数与 `groupby` 搭配使用，便于对每一组的一列或多列计算该统计量。
这样会生成一个新的数据框：每个组占一行，每个汇总统计量占一列。
每张表格颜色较深的最上面一行代表表头。这个示意例子中的橙色、蓝色和绿色的行，
分别对应三个组各自包含的行。
```

+++

`groupby` 函数至少要有一个参数——用于分组的列。这里我们只用一列来分组（`region`）。

```{code-cell} ipython3
region_lang.groupby("region")
```

请注意，`groupby` 会把 `DataFrame` 对象转换成 `DataFrameGroupBy` 对象，其中含有数据框
各个组的信息。接下来，我们就可以对 `DataFrameGroupBy` 对象应用聚合函数。这里我们先选出
`most_at_home` 列，再用 `agg` 求出分组数据的最小值和最大值。

```{code-cell} ipython3
region_lang.groupby("region")["most_at_home"].agg(["min", "max"])
```

得到的数据框以 `region` 作为索引名。这与我们在 {numref}`pivot-wider` 中使用 `pivot`
函数时的情况类似；和当时一样，你可以用 `reset_index` 把它恢复成普通数据框，
`region` 则成为列名。

```{code-cell} ipython3
region_lang.groupby("region")["most_at_home"].agg(["min", "max"]).reset_index()
```
你也可以把多个列名传给 `groupby`。例如，如果我们想了解不同类别的语言，
即 Aboriginal（原住民）、Non-Official & Non-Aboriginal（非官方且非原住民）和
Official（官方），在不同地区家庭中的使用情况，就要给 `groupby` 传一个列表，
其中包含 `region` 和 `category`。

```{code-cell} ipython3
region_lang.groupby(["region", "category"])["most_at_home"].agg(["min", "max"]).reset_index()
```

你也可以在整张数据框上按组计算汇总统计量。

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.groupby("region").agg(["min", "max"]).reset_index()
```

如果你只想要其中一部分列，比如 `"most_at_home"` 到 `"lang_known"` 之间的列，
你可能会想先调用 `groupby`，再用 `["most_at_home":"lang_known"]`；但 `groupby`
返回的是 `DataFrameGroupBy` 对象，它不支持在 `[]` 里使用范围。
另一种做法是调换顺序：先用 `["most_at_home":"lang_known"]`，再用 `groupby`。
这样做能行得通，但必须小心！例如在我们这个例子里，就会报错。

```{code-cell} ipython3
:tags: [remove-output]
region_lang["most_at_home":"lang_known"].groupby("region").max()
```

```{code-cell} ipython3
:tags: ["remove-input"]
print('KeyError: "region"')
```

这是因为用 `[]` 只选出了 `"most_at_home"` 到 `"lang_known"` 之间的列，
其中并不包含 `"region"`！因此，正确的做法是先用 `groupby`，
再用 `[]` 传入一个包含 `region` 的列名列表；这种写法总是行得通。

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.groupby("region")[["most_at_home", "most_at_work", "lang_known"]].max().reset_index()
```

要想知道每个组里有多少个观测，可以用 `value_counts`。

```{index} DataFrame; value_counts
```

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.value_counts("region")
```

这个方法还可以接收 `normalize` 参数，把输出显示为比例而不是计数。

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.value_counts("region", normalize=True)
```

+++

## 跨列应用函数

计算汇总统计量并不是唯一需要跨列应用函数的情形。另外还有两类常见的数据整理任务也要跨列应用函数。
第一类是：想把某种变换（如测量单位的换算）应用到多个列上。
{numref}`fig:mutate-across` 展示了这样一次数据变换；请注意，这种变换不会改变数据框的形状。

```{figure} img/wrangling/summarize.005.png
:name: fig:mutate-across
:figclass: figure

把一种变换应用到许多列上。每张表格颜色较深的最上面一行代表表头。
```

例如，假设我们想用 `.astype` 函数把 `region_lang` 数据框中所有数值列从 `int64` 类型
转换成 `int32` 类型。重新查看 `region_lang` 数据框，可以看到这些列就是从 `mother_tongue`
到 `lang_known` 的那些列。

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang
```

```{index} DataFrame; apply, DataFrame; loc[]
```

我们只需调用 `.astype` 函数，就能把它应用到所需的列范围上。

```{index} DataFrame; astype, Series; astype
```

```{code-cell} ipython3
region_lang_nums = region_lang.loc[:, "mother_tongue":"lang_known"].astype("int32")
region_lang_nums.info()
```
现在可以看到，从 `mother_tongue` 到 `lang_known` 的列都是 `int32` 类型，
而且得到的数据框与输入数据框具有相同的列数和行数。

第二类情形是：你想在每一行内部跨列应用函数，也就是*按行*（row-wise）计算。
{numref}`fig:rowwise` 展示了这种操作，它生成单独的一列，其中的取值概括原始数据框中每一行的内容；这一新列还可以加回原始数据中。

```{figure} img/wrangling/summarize.004.png
:name: fig:rowwise
:figclass: figure

在数据框中按行应用函数，生成一个新列。
每张表格颜色较深的最上面一行代表表头。
```

例如，假设我们想知道 `region_lang_nums` 数据集中每种语言、每个地区
在 `mother_tongue` 和 `lang_known` 之间的最大值。换句话说，我们要*按行*应用 `max` 函数。
要想让 `max` 知道我们想按行计算（而不是默认的逐列分别计算），只需指定参数 `axis=1`。

```{code-cell} ipython3
region_lang_nums.max(axis=1)
```

可以看到，我们得到的是一个序列，其中包含数据框每一行在 `mother_tongue`、
`most_at_home`、`most_at_work` 和 `lang_known` 之间的最大值。
我们常常希望把按行计算得到的结果作为新列加入数据框，以便作图或继续分析。为此，
我们将使用列赋值或 `assign` 函数来新建一列。下一节会讨论这种做法。

```{note}
`pandas` 提供了许多可以应用到数据框上的方法（例如 `max`、`astype` 等），
但有时你可能想把自己的函数应用到数据框的多个列上。这时
你可以使用更通用的 [`apply`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html) 方法。
```

(pandas-assign)=
