+++

{numref}`fig:img-pivot-longer` 详细说明了要用 `melt` 函数完成这一数据变换时需要指定的参数。

+++ {"tags": []}

```{figure} img/wrangling/pandas_melt_args_labels.png
:name: fig:img-pivot-longer
:figclass: figure

`melt` 函数的语法。
```

+++

```{index} 列范围
```

```{index} see: :; 列范围
```

我们用 `melt` 把 Toronto、Montréal、Vancouver、Calgary 和 Edmonton 这几列合并成一列，列名为 `region`；同时新建一列 `mother_tongue`，存放每个大都市区中把各语言报告为母语的加拿大人数。

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_mother_tidy = lang_wide.melt(
    id_vars=["category", "language"],
    var_name="region",
    value_name="mother_tongue",
)
lang_mother_tidy
```

```{note}
在上面的代码里，对 `melt` 函数的调用被拆成了好几行。回忆一下，{numref}`第 %s 章 <intro>` 讲过，某些情况下这是允许的。例如，像上面那样调用函数时，输入参数位于圆括号 `()` 之间，Python 就知道要继续读下一行。每一行都以逗号 `,` 结尾，读起来更方便。像这样把长行拆成多行是值得提倡的，因为它对代码可读性帮助很大。一般来说，每行代码最好控制在 80 个字符左右。
```

上面的数据现在已经是整洁数据了，因为整洁数据的三条标准都已满足：

1.  所有变量（`category`、`language`、`region` 和 `mother_tongue`）现在都各自成为数据框中的一列。
2.  每条观测，即每个 `category`、`language`、`region` 的组合以及把该语言作为母语的加拿大人数，都位于同一行。
3.  每个取值只占一个单元格，即它在数据框中的行、列位置不与其他取值共用。

+++

(pivot-wider)=
### 整理数据：用 `pivot` 从长格式变为宽格式

```{index} DataFrame; pivot
```

假设我们的观测分散在多行，而不是集中在同一行。例如，在 {numref}`fig:long-to-wide` 中，左侧的表格就是不整洁的长格式，因为 `count` 列里混有三个变量（population、commuter 和 incorporated 计数），而且每条观测的信息（这里是某个地区的 population、commuter 与 incorporated 计数）被拆到了三行。请记住：整洁数据的一条标准就是每条观测必须位于同一行。

使用这种格式的数据——两个或多个变量混在同一列里——会让许多常用的 `pandas` 函数难以使用。例如，要找出通勤人数的最大值，就需要额外做一步筛选，先把通勤人数的取值挑出来，然后才能计算最大值。相比之下，如果数据是整洁的，我们只要计算通勤人数那一列的最大值即可。要把这份不整洁的数据集整理成整洁（在这个例子里也是更宽）的格式，我们需要创建名为 “population”、“commuters” 和 “incorporated” 的列。{numref}`fig:long-to-wide` 的右侧表格展示了这一过程。

+++ {"tags": []}

```{figure} img/wrangling/pivot_functions.002.png
:name: fig:long-to-wide
:figclass: figure

从长格式变为宽格式。
```

+++

在 Python 里整理这类数据，可以用 `pivot` 函数。`pivot` 函数通常会增加数据集的列数（把数据变宽），同时减少行数。为了学会使用 `pivot`，我们用一个例子来演示，用的是 `region_lang_top5_cities_long.csv` 数据集。这份数据集记录的是五个大城市（Toronto、Montréal、Vancouver、Calgary 和 Edmonton）中把某种语言作为主要语言在家里和工作中使用的加拿大人数。

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_long = pd.read_csv("data/region_lang_top5_cities_long.csv")
lang_long
```

上面这份数据集为什么不整洁呢？在这个例子里，每条观测是某个地区中的一种语言。可是每条观测都被拆到了多行：一行记录 `most_at_home` 的计数，另一行记录 `most_at_work` 的计数。假设这份数据的目标是可视化“在家里使用主要语言的加拿大人数”与“在工作中使用主要语言的加拿大人数”之间的关系。以数据当前的形式，这件事很难做到，因为这两个变量存放在同一列里。{numref}`fig:img-pivot-wider-table` 展示了如何用 `pivot` 函数整理这份数据。

+++ {"tags": []}

```{figure} img/wrangling/pandas_pivot_long-wide.png
:name: fig:img-pivot-wider-table
:figclass: figure

用 `pivot` 函数把长格式变为宽格式。
```

+++

{numref}`fig:img-pivot-wider` 详细说明了使用 `pivot` 函数时需要指定的参数。

+++ {"tags": []}

```{figure} img/wrangling/pandas_pivot_args_labels.png
:name: fig:img-pivot-wider
:figclass: figure

`pivot` 函数的语法。
```

+++

我们将按照 {numref}`fig:img-pivot-wider` 里的说明调用该函数，然后再给列重命名。

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_home_tidy = lang_long.pivot(
    index=["region", "category", "language"],
    columns=["type"],
    values=["count"]
).reset_index()

lang_home_tidy.columns = [
    "region",
    "category",
    "language",
    "most_at_home",
    "most_at_work",
]
lang_home_tidy
```

```{index} DataFrame; reset_index
```

第一步中请注意，我们加了一次 `reset_index` 调用。当传给 `pivot` 的 `index` 是多个列名时，这些列名会成为每一行的“名字”；用 `[]` 或 `loc` 筛选行时依据的就是这些名字，而不是简单的数字。这可能让人困惑……`reset_index` 的作用是回到我们熟悉的常规行为：每一行用整数“命名”。这一点比较微妙，但要点是：调用 `pivot` 之后，最好接着调用 `reset_index`。

第二步操作是给列重命名。执行 `pivot` 操作时，它会保留原来的列名 `"count"`，并把 `"type"` 作为第二个列名加上去。一列有两个名字，很容易让人困惑！所以我们重新命名，让每列只有一个名字。

```{index} DataFrame; info
```

我们可以用 `info` 函数打印出数据框的一些有用信息。第一行告诉了我们 `lang_home_tidy` 的 `type`（它是一个 `pandas` 的 `DataFrame`）。第二行告诉我们数据有多少行：1070 行，并且可以用 0 到 1069 之间的数字为这些行建立索引（记住，Python 从 0 开始计数！）。接着是关于各列的打印输出。这里总共有 5 列。它打印出的那张小表格会告诉你每一列的名字、非空取值的个数（也就是不是缺失值的条目数），以及这些取值的类型。最后两行汇总了每一列的类型，以及数据框在你的计算机上占用的内存大小。
```{code-cell} ipython3
lang_home_tidy.info()
```

现在数据是整洁的了！我们可以再按三条标准检查一遍，确认这份数据是整洁数据集。

1.  所有统计变量都各自成为数据框中的一列（即 `most_at_home` 和 `most_at_work` 已经分到数据框中各自的列里）。
2.  每条观测（即某个地区里的一种语言）都位于同一行。
3.  每个取值只占一个单元格（即它在数据框中的行、列位置不与其他取值共用）。

你可能注意到，整洁数据集中的列数与混乱数据集中的列数相同。所以 `pivot` 其实并没有把数据“变宽”。原因只是原来的 `type` 列里只有两个类别。如果它有两个以上类别，`pivot` 就会创建更多列，我们也能看到数据集“变宽”了。

+++

(str-split)=
### 整理数据：用 `str.split` 处理多个分隔符

```{index} Series; str.split, 分隔符
```

```{index} see: 定界符; 分隔符
```

同一个单元格里存放多个取值时，数据同样不算整洁。下面展示的数据集比上面处理过的那些还要混乱：`Toronto`、`Montréal`、`Vancouver`、`Calgary` 和 `Edmonton` 这几列把在家里和工作中使用主要语言的加拿大人数放在同一列里，中间用分隔符（separator，也就是 `/`）隔开。列名本身就是某个变量的取值，*而且*每个取值并没有自己独立的单元格！要把这份混乱数据变成整洁数据，我们必须解决这些问题。

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_messy = pd.read_csv("data/region_lang_top5_cities_messy.csv")
lang_messy
```

首先，我们像前面那样用 `melt` 创建两列：`region` 和 `value`。新的 `region` 列将存放地区名称，新的 `value` 列暂时存放还需要进一步拆分的数据，也就是在家里和工作中使用主要语言的加拿大人数。

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_messy_longer = lang_messy.melt(
    id_vars=["category", "language"],
    var_name="region",
    value_name="value",
)

lang_messy_longer
```

接下来，我们把 `value` 列拆成两列。在基本 Python 里，如果要把字符串 `"50/0"` 拆成两个数 `["50", "0"]`，我们会用字符串的 `split` 方法，并指明按斜杠字符 `"/"` 拆分。
```{code-cell} ipython3
"50/0".split("/")
```

`pandas` 包提供了类似的函数，可以通过 `str` 方法访问。所以，要拆分数据框中整列的所有条目，我们会用 `str.split` 方法。该方法的输出是一个数据框，其中包含两列：一列只有每个地区中在家里最常使用该语言的加拿大人数，另一列只有在工作中最常使用该语言的加拿大人数。我们把不再需要的 `value` 列从 `lang_messy_longer` 数据框中删掉，然后把 `str.split` 得到的两列赋给两个新列。
{numref}`fig:img-separate`
列出了使用 `str.split` 需要指定的内容。

+++ {"tags": []}

```{figure} img/wrangling/str-split_args_labels.png
:name: fig:img-separate
:figclass: figure

`str.split` 函数的语法。
```

```{code-cell} ipython3
tidy_lang = lang_messy_longer.drop(columns=["value"])
tidy_lang[["most_at_home", "most_at_work"]] = lang_messy_longer["value"].str.split("/", expand=True)
tidy_lang
```

这份数据集现在整洁了吗？回忆一下整洁数据的三条标准：

  - 每一行是一条观测，
  - 每一列是一个变量，
  - 每个取值只占一个单元格。

可以看到，这份数据现在满足全部三条标准，分析起来更容易了。不过我们还没做完！虽然从上面的数据框里看不出来，但所有变量实际上都是 `object` 数据类型。可以用 `info` 方法检查一下。
```{code-cell} ipython3
tidy_lang.info()
```

`pandas` 数据框中的 object 列，要么是字符串列，要么是混合类型的列。在前面 {numref}`pivot-wider` 那个例子里，`most_at_home` 和 `most_at_work` 两个变量是 `int64`（整数），属于数值型数据。类型发生变化，是因为读取这份混乱数据集时出现了分隔符（`/`）。Python 把这些列读成了字符串类型，而 `str.split` 默认返回 `object` 数据类型的列。

`region`、`category` 和 `language` 存放的是分类取值，把它们存成 `object` 类型是合理的。不过，假设我们想用一些把 `most_at_home` 和 `most_at_work` 列当作数字处理的函数（例如找出某列中高于某个数值阈值的行），如果变量存成 `object`，这些函数就用不了。好在 `pandas` 的 `astype` 方法能很自然地解决这类问题：它会把列转换成指定的数据类型。这里我们选择 `int` 数据类型，表示这些变量存放的是整数计数。注意，下面我们会把新的数值序列*赋值*给 `tidy_lang` 中的 `most_at_home` 和 `most_at_work` 列；这种语法我们之前在 {numref}`ch1-adding-modifying` 中见过，本章后面在 {numref}`pandas-assign` 中还会更深入地讨论。

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang["most_at_home"] = tidy_lang["most_at_home"].astype("int")
tidy_lang["most_at_work"] = tidy_lang["most_at_work"].astype("int")
tidy_lang
```

```{code-cell} ipython3
tidy_lang.info()
```

现在我们看到 `most_at_home` 和 `most_at_work` 列都是 `int64` 数据类型，说明它们是整数类型（也就是数字）！

+++

## 用 `[]` 提取行或列

既然 `tidy_lang` 数据确实*整洁*了，我们就可以开始用 `pandas` 那一整套强大的函数来操作它。我们先回顾一下 {numref}`第 %s 章 <intro>` 里的 `[]`，它可以取出数据框中行**或**列的子集。本节将重点介绍 `[]` 更高级的用法，并深入讲解在 `[]` 中筛选行子集时可以使用的各种逻辑表达式（logical statement）。

```{index} DataFrame; [], 逻辑表达式
```

```{index} see: 逻辑表达式; 逻辑运算符
```