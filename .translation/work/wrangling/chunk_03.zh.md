+++

### 按列名提取列

回忆一下，如果传入一个列名列表，`[]` 就会返回由这些列名构成的列子集，形式是数据框。假设我们想从 `tidy_lang` 数据集中选取 `language`、`region`、`most_at_home` 和 `most_at_work` 这几列，那么用在 {numref}`第 %s 章 <intro>` 中学到的方法，把这些列名全部传进方括号即可。

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang[["language", "region", "most_at_home", "most_at_work"]]
```

同样，如果传入的列表只包含一个列名，返回的就是只含这一列的数据框。

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang[["language"]]
```

如果需要提取的只有单独一列，我们也可以传入列名字符串，而不传列表。这时返回的数据类型是序列。在本书中，我们大多这样提取单独的列，不过也会指出少数几处，说明把单独的列作为数据框提取出来更有优势。

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang["language"]
```


### 用 `==` 提取具有特定取值的行

```{index} 逻辑运算符; 相等 (==)
```

```{index} see: ==; 逻辑运算符
```

假设我们只关心 `tidy_lang` 中与加拿大官方语言（英语和法语）对应的那部分行。我们可以用*相等运算符*（equivalency operator，即 `==`）把 `category` 列的取值与 `"Official languages"` 做比较，从而取出这些行。传入这些参数后，`[]` 返回的数据框包含输入数据框的所有列，但只保留逻辑表达式中指定的那些行，也就是 `category` 列取值为 `"Official languages"` 的行。我们把这个数据框命名为 `official_langs`。

```{code-cell} ipython3
:tags: ["output_scroll"]
official_langs = tidy_lang[tidy_lang["category"] == "Official languages"]
official_langs
```

### 用 `!=` 提取不具有特定取值的行

```{index} 逻辑运算符; 不等 (!=)
```

```{index} see: !=; 逻辑运算符
```

如果我们想要数据集中*除* `"Official languages"` 类别之外的所有其他语言类别呢？这可以用*不等运算符*（inequivalency operator，即 `!=`）实现，它表示“不等于”。因此，若要找出 `category` *不*等于 `"Official languages"` 的所有行，就写下方的代码。

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang[tidy_lang["category"] != "Official languages"]
```

(filter-and)=
### 用 `&` 提取同时满足多个条件的行

```{index} 逻辑运算符; 与 (&)
```

```{index} see: &; 逻辑运算符
```

现在假设我们只想查看 Montréal 中法语的那些行。为此需要筛选数据集，找出同时满足多个条件的行。这可以用逻辑与运算符（ampersand，即 `&` 符号）实现，Python 把它解释为“与”。我们按下方所示的代码对 `official_langs` 数据框做筛选，取出 `region == "Montréal"` *并且* `language == "French"` 的行。

```{code-cell} ipython3
tidy_lang[
  (tidy_lang["region"] == "Montréal") &
  (tidy_lang["language"] == "French")
]
```

+++ {"tags": []}

### 用 `|` 提取至少满足一个条件的行

```{index} 逻辑运算符; 或 (|)
```

```{index} see: |; 逻辑运算符
```

假设我们只关心 `official_langs` 数据集中阿尔伯塔省的城市（Edmonton 和 Calgary）对应的行。这里不能用上面那种 `&`，因为 `region` 不可能同时是 Edmonton *和* Calgary。可以改用逻辑或运算符（vertical pipe，即 `|`），它给出的情形是：满足一个条件*或*另一个条件*或*两个条件都满足。在下方代码中，我们让 Python 返回 `region` 列等于“Calgary”*或*“Edmonton”的行。

```{code-cell} ipython3
official_langs[
    (official_langs["region"] == "Calgary") |
    (official_langs["region"] == "Edmonton")
]
```

### 用 `isin` 提取取值属于某个列表的行

```{index} 逻辑运算符; 包含 (isin)
```

```{index} see: isin; 逻辑运算符
```

接下来，假设我们想看这五座城市的人口。我们来读取 `region_data.csv` 文件，它来自 2016 年加拿大人口普查，含有不同地区的家庭户数、土地面积、人口和住宅数量等统计数据。

```{code-cell} ipython3
:tags: ["output_scroll"]
region_data = pd.read_csv("data/region_data.csv")
region_data
```

要得到这五座城市的人口，可以用 `isin` 方法筛选数据集。`isin` 方法用来判断某个元素是否属于一个列表。这里我们筛选的是 `region` 列的取值与我们关注的五座城市中任意一座相同的行：Toronto、Montréal、Vancouver、Calgary 和 Edmonton。

```{code-cell} ipython3
city_names = ["Toronto", "Montréal", "Vancouver", "Calgary", "Edmonton"]
five_cities = region_data[region_data["region"].isin(city_names)]
five_cities
```

```{note}
`==` 与 `isin` 有什么区别？假设有两个 Series，`seriesA` 和 `seriesB`。在 Python 里输入 `seriesA == seriesB`，它会逐元素地比较这两个序列：Python 检查 `seriesA` 的第一个元素是否等于 `seriesB` 的第一个元素，`seriesA` 的第二个元素是否等于 `seriesB` 的第二个元素，依此类推。而 `seriesA.isin(seriesB)` 会把 `seriesA` 的第一个元素与 `seriesB` 中的所有元素比较，接着把 `seriesA` 的第二个元素与 `seriesB` 中的所有元素比较，依此类推。请注意下例中 `==` 与 `isin` 的区别。
```

```{code-cell} ipython3
pd.Series(["Vancouver", "Toronto"]) == pd.Series(["Toronto", "Vancouver"])
```

```{code-cell} ipython3
pd.Series(["Vancouver", "Toronto"]).isin(pd.Series(["Toronto", "Vancouver"]))
```

### 用 `>` 和 `<` 提取高于或低于阈值的行

```{index} 逻辑运算符; 大于 (> 和 >=), 逻辑运算符; 小于 (< 和 <=)
```

```{index} see: >; 逻辑运算符
```

```{index} see: >=; 逻辑运算符
```

```{index} see: <; 逻辑运算符
```

```{index} see: <=; 逻辑运算符
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("census_popn", "{0:,.0f}".format(35151728))
glue("most_french", "{0:,.0f}".format(2669195))
```

我们在 {numref}`filter-and` 中看到，有 {glue:text}`most_french` 人报告自己在 Montréal 把法语作为在家主要使用的语言。如果我们要找的是这样的地区：在那里，把某种官方语言作为在家主要语言的人数多于 Montréal 的法语人数，就可以用 `[]` 取出 `most_at_home` 的取值大于 {glue:text}`most_french` 的行。我们用 `>` 符号查找*高于*阈值的取值，用 `<` 符号查找*低于*阈值的取值；`>=` 和 `<=` 符号同样分别查找*大于或等于*阈值、*小于或等于*阈值的取值。

```{code-cell} ipython3
official_langs[official_langs["most_at_home"] > 2669195]
```

这个操作返回的数据框只有一行，说明在考虑官方语言时，根据 2016 年加拿大人口普查，只有 Toronto 的英语作为在家主要语言的报告人数多于 Montréal 的法语。

### 用 `query` 提取行

```{index} 逻辑表达式; query
```

你也可以用 `query` 方法提取高于、低于、等于或不等于某个阈值的行。例如，下面这句得到的结果与使用 `official_langs[official_langs["most_at_home"] > 2669195]` 时相同。

```{code-cell} ipython3
official_langs.query("most_at_home > 2669195")
```

查询（也就是我们用来选取取值的条件）以字符串形式传入。`query` 方法没有前面介绍的几种做法常用，但在让一长串链式筛选操作读起来更轻松时，它很管用。

(loc-iloc)=
## 用 `loc[]` 筛选行并选取列

```{index} DataFrame; loc[]
```

`[]` 操作只用于筛选行**或**选取列这两件事中的一件，不能同时完成两件。这正是 `loc[]` 的用武之地。先看第一个例子：回忆一下 {numref}`第 %s 章 <intro>` 中的 `loc[]`，我们可以用它取出 `tidy_lang` 数据框中行与列的子集。`loc[]` 的第一个参数给出一个逻辑表达式，把行筛选到只保留与 Toronto 地区有关的那些；第二个参数给出按列名保留的列列表。

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[
    tidy_lang["region"] == "Toronto",
    ["language", "region", "most_at_home", "most_at_work"]
]
```

除了能同时取行和列的子集，`loc[]` 还有两项 `[]` 不具备的特殊能力。首先，`loc[]` 可以指定行和列的*范围*。例如，列列表 `language`、`region`、`most_at_home`、`most_at_work` 对应的正是从 `language` 到 `most_at_work` 的*列范围*（column range）。我们可以不必像上面那样把所有列名逐一列出，而是直接写出列范围 `"language":"most_at_work"`；`:` 语法表示范围，`loc[]` 支持它，而 `[]` 不支持。

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[
    tidy_lang["region"] == "Toronto",
    "language":"most_at_work"
]
```

我们也可以只写一个 `:`——前后都不写任何内容——表示要取回全部内容。例如，要取全部行、并且只保留从 `language` 到 `most_at_work` 的列，可以用下面这个表达式。

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[:, "language":"most_at_work"]
```

我们也可以省略 `:` 范围表达式的开头或结尾，表示我们要的是某个元素“之前的全部”或“之后的全部”。例如，要取包含 `language` 及其之后的所有列，可以写成下面这个表达式：

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[:, "language":]
```
`:` 后面不写任何内容，Python 就把它理解为“从 `language` 开始，直到最后一列”。同样，如果我们要的是到 `language` 为止（含这一列）的全部列，就写成下面这个表达式：

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[:, :"language"]
```

`:` 前面不写任何内容，Python 就把它理解为“从第一列直到 `language`”。用 `:` 选取范围的写法因为更省代码而很方便，但必须谨慎使用。一旦重新排列列的顺序，或者给数据框添加一列，输出就会改变。用列表更明确，不易引起混淆，只是有时要多打很多字。

`.loc[]` 比 `[]` 多的第二项特殊能力，是可以用逻辑表达式*选取列*。`[]` 运算符只能用逻辑表达式筛选行，而 `.loc[]` 两件事都能做！例如，假设我们只想选取 `most_at_home` 和 `most_at_work` 两列。这时可以用 `.str.startswith` 方法，只挑出以“most”开头的列。`str.startswith` 表达式返回一串 `True` 或 `False` 取值，对应的是列名是否以指定的字符开头。

```{code-cell} ipython3
tidy_lang.loc[:, tidy_lang.columns.str.startswith("most")]
```

```{index} Series; str.contains
```

我们也可以用 `.str.contains("_")` 选出含下划线 `_` 的列，因为可以看到，我们想要的列都含下划线，而其他列不含。

```{code-cell} ipython3
tidy_lang.loc[:, tidy_lang.columns.str.contains("_")]
```

## 用 `iloc[]` 按位置提取行和列
```{index} DataFrame; iloc[], 列范围
```
另一种选取行列的做法是使用 `iloc[]`，它按列的位置而不是列的标签来索引。例如，`tidy_lang` 数据框的列标签是 `["category", "language", "region", "most_at_home", "most_at_work"]`。用 `iloc[]`，你可以请求索引为 `1` 的那一列，从而取到 `language` 列（记住 Python 从 `0` 开始计数，所以第二列 `"language"` 的索引是 `1`！）。

```{code-cell} ipython3
tidy_lang.iloc[:, 1]
```

你也可以一次请求多列。在逗号后面传入 `1:`，表示要索引 1 及其之后的列（*即* `language`）。

```{code-cell} ipython3
tidy_lang.iloc[:, 1:]
```

用类似的语法，我们还可以用 `iloc[]` 选取行的范围，或者同时选取行和列的范围。例如，要选取前五行以及索引 1 及其之后的列，可以这样写：

```{code-cell} ipython3
tidy_lang.iloc[:5, 1:]
```

请注意，`iloc[]` 方法并不常用，而且必须谨慎使用。例如，很容易不小心写错整数索引！如果你没记准 `language` 列的索引是 `1`，而用了 `2`，代码里就可能留下一个很难排查的缺陷（bug）。

```{index} Series; str.startswith
```

+++ {"tags": []}

## 聚合数据

+++

### 计算单个列的汇总统计量

```{index} 汇总
```

在许多数据分析中，我们都需要为数据算出一个汇总值（*汇总统计量*）。可能要计算的汇总统计量包括观测的个数、某一列的平均数／均值、最小值等。这种汇总统计量通常根据数据框某一列或若干列的取值算出，如 {numref}`fig:summarize` 所示。

+++ {"tags": []}

```{figure} img/wrangling/summarize.001.png
:name: fig:summarize
:figclass: figure

在 `pandas` 中对一列或多列计算汇总统计量，通常会生成一个序列或数据框，其中含有每个被汇总列的汇总统计量。每张表格颜色较深的最上面一行代表表头。
```
