## 修改和添加列


```{index} DataFrame; [], 列赋值, assign
```

计算汇总统计量或应用函数时，都会生成新的数据框或序列。但如果我们想把这份信息追加到
已有的数据框上呢？例如，假设我们要计算 `region_lang_nums` 数据框每一行的最大值，
再把它作为 `region_lang` 数据框的一个新列追加进去。
这时有两种选择：要么在 `region_lang` 数据框里新建一列，
要么用 `assign` 方法新建一个数据框。第一种做法我们在前面几章已经见过，
也是实践中更常用的模式：
```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang["maximum"] = region_lang_nums.max(axis=1)
region_lang
```
从上面的输出可以看到，`region_lang` 数据框现在多了一列，列名为 `maximum`。
`maximum` 列给出的是 `mother_tongue`、
`most_at_home`、`most_at_work` 和 `lang_known` 之间的最大值，对应每种语言和每个地区，
正是我们指定的结果！

如果要改成新建一个数据框，可以用 `assign` 方法，并为每个要创建的列指定一个参数。
这里我们要新建一个名为 `maximum` 的列，所以传给 `assign` 的参数以 `maximum= ` 开头。
接着在 `=` 后面，我们给出这一列的内容。这里我们和前面一样用 `max` 求最大值。
记得在 `max` 方法中指定 `axis=1`，这样算出来的才是按行的最大值。
```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.assign(
  maximum=region_lang_nums.max(axis=1)
)
```
这个数据框看起来和上一个完全一样，区别在于它是 `region_lang` 的副本，
而不是 `region_lang` 本身；继续修改这个数据框不会影响原来的 `region_lang` 数据框。


```{code-cell} ipython3
:tags: [remove-cell]

# remove maximum coln from region_lang
region_lang = region_lang.drop(columns=["maximum"])

# get english counts for toronto and glue
number_most_home = int(
    official_langs[
        (official_langs["language"] == "English") &
        (official_langs["region"] == "Toronto")
    ]["most_at_home"]
)

toronto_popn = int(region_data[region_data["region"] == "Toronto"]["population"])

glue("number_most_home", "{0:,.0f}".format(number_most_home))
glue("toronto_popn", "{0:,.0f}".format(toronto_popn))
glue("prop_eng_tor", "{0:.2f}".format(number_most_home / toronto_popn))
```

再举一个例子。我们可能会问：“2016 年人口普查中，报告把英语作为在家主要语言的人占多大比例？”
例如在多伦多，有 {glue:text}`number_most_home` 人报告自己把英语作为在家主要使用的语言，
而多伦多的人口为 {glue:text}`toronto_popn` 人。所以，2016 年人口普查中
多伦多报告把英语作为主要语言的人口比例为 {glue:text}`prop_eng_tor`。
那么，从 `region_lang` 数据框出发，我们该怎么算出这个结果呢？

首先，我们需要筛选 `region_lang` 数据框，只保留语言为英语的行。
我们还要把范围限定在 `five_cities` 数据框中的五个主要城市：Toronto、Montréal、Vancouver、Calgary 和 Edmonton。
筛选时只保留与英语有关、并且属于上述五个城市的行。要把这两个逻辑表达式组合起来，
我们用 `&` 符号。
再用 `[]` 操作，以 `"English"` 作为 `language` 筛选行，
并把新数据框命名为 `english_langs`。
```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang = region_lang[
    (region_lang["language"] == "English") &
    (region_lang["region"].isin(five_cities["region"]))
]
english_lang
```

好，现在这个数据框只涉及英语和前面提到的五个城市。
要算出这些城市中讲英语的人口比例，
我们需要把 `five_cities` 数据框中的人口数据加进来。
```{code-cell} ipython3
five_cities
```
上面的数据框显示，2016 年这五个城市的人口分别是
5928040（Toronto）、4098927（Montréal）、2463431（Vancouver）、1392609（Calgary）和 1321426（Edmonton）。
接下来，我们把这份信息加到数据框的一个新列 `city_pops` 中。
这里我们同样用 `assign` 方法和常规列赋值各演示一遍做法。
我们把新列名（`city_pops`）作为参数，后面跟等号 `=`，
最后是该列的数据。
注意，`english_lang` 数据框中各行的顺序是 Montréal、Toronto、Calgary、Edmonton、Vancouver。
所以我们要新建一个名为 `city_pops` 的列，按这个顺序列出这些城市的人口，
再把它加到数据框中。
还要记住，和其他 `pandas` 函数一样，`assign` 默认不会直接修改原数据框，
所以 `english_lang` 数据框不会改变！
```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang.assign(
  city_pops=[4098927, 5928040, 1392609, 1321426, 2463431]
)
```

除了用 `assign` 方法，我们也可以直接用常规列赋值修改 `english_lang` 数据框。
在这个例子里这样做更自然，
因为对于简单的列修改和添加，这种语法更方便。
```{code-cell} ipython3
:tags: [remove-output]
english_lang["city_pops"] = [4098927, 5928040, 1392609, 1321426, 2463431]
english_lang
```
```{code-cell} ipython3
:tags: ["remove-input"]
print("""
/tmp/ipykernel_12/2654974267.py:1: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  english_lang["city_pops"] = [4098927, 5928040, 1392609, 1321426, 2463431]
""")
english_lang
```

```{index} SettingWithCopyWarning
```

等一下……那条警告信息是怎么回事？它似乎在说哪里出了问题，但看看上面的
`english_lang` 数据框，城市人口明明加得好好的！原来，这是前面把 `region_lang`
筛选成最初的 `english_lang` 时留下的影响。细节有点技术性：先用 `[]` 或 `loc[]`
取数据框的子集，紧接着做列赋值，`pandas` 有时不喜欢这种写法。
就你自己的数据分析而言，如果看到 `SettingWithCopyWarning`，只要在继续之前
再核对一遍列赋值的结果是否符合预期就行。
为了方便阅读，本书其余部分会关掉这条警告。
```{code-cell} ipython3
:tags: [remove-cell]
# suppress for the rest of this chapter
pd.options.mode.chained_assignment = None
```

```{index} DataFrame; merge
```

```{note}
像上面那样手动插入数据列 `[4098927, 5928040, ...]` 通常很容易出错，并不推荐这样做。
这里这样做，只是为了演示 `assign` 和常规列赋值的另一种用法。
但在更高级的数据整理中，
人们会用 `merge` 函数以更不容易出错的方式解决这个问题，它可以把两个数据框合并起来。
我们会在本章末尾演示一个使用 `merge` 的例子！
```

现在，数据框里多了一个新列，存放各城市的人口。最后，把所有数值列与 `city_pops` 相除，
就能把它们都换算成讲英语人口的比例。我们直接修改 `english_lang` 的列；这里
直接给数据框赋值即可。这类似于我们在 {numref}`str-split` 中的做法：
当时我们刚读入 `"region_lang_top5_cities_messy.csv"` 数据，需要把几个变量转成数值类型。
这里我们用 `loc[]` 同时给一个列范围赋值。
注意，修改已有的列时同样可以用 `assign` 函数生成一个新的数据框，
只是实际中很少这样做。
还要注意，我们用 `div` 方法并指定参数 `axis=0`，
把一个列范围内的各列除以单个列的取值——这种情况下基本除号 `/` 不起作用。

```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang.loc[:, "mother_tongue":"lang_known"] = english_lang.loc[
    :,
    "mother_tongue":"lang_known"
    ].div(english_lang["city_pops"], axis=0)
english_lang
```

+++

## 用 `merge` 合并数据框

```{index} DataFrame; merge
```

我们回到给 `english_lang` 数据框加入 Toronto、Montréal、Vancouver、Calgary 和 Edmonton
这几座城市人口之前的状态。在添加新列之前，我们已经从 `region_lang` 中筛选出了
`english_lang` 数据框，其中只包含这五个目标城市里讲英语的人。
```{code-cell} ipython3
:tags: ["remove-cell"]
english_lang = region_lang[
    (region_lang["language"] == "English") &
    (region_lang["region"].isin(five_cities["region"]))
]
```

```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang
```
随后我们把这些城市的人口加成一列
（Toronto：5928040，Montréal：4098927，Vancouver：2463431，
Calgary：1392609，Edmonton：1321426）。添加时必须注意顺序正确，这个过程很容易出错。
这里演示的另一种做法是：（1）先新建一个数据框，其中包含城市名称和人口，
（2）认出两者的“regions”是相同的，用 `merge` 把这两个数据框合并起来。

我们调用 `pd.DataFrame`，并以一个字典作为参数来新建数据框。
字典把待建数据框的每个列名与一个条目列表对应起来。这里我们在 `"region"` 列中
列出城市名称，在 `"population"` 列中列出它们的人口。
```{code-cell} ipython3
city_populations = pd.DataFrame({
  "region" : ["Toronto", "Montréal", "Vancouver", "Calgary", "Edmonton"],
  "population" : [5928040, 4098927, 2463431, 1392609, 1321426]
})
city_populations
```
这个新数据框的 `region` 列与 `english_lang` 数据框相同。城市的顺序不同，
但这没关系！我们可以用 `pandas` 中的 `merge` 函数，
按 `region` 把两个数据框匹配着合并起来。参数
`on="region"` 告诉 pandas，我们想用 `region` 列来匹配条目。
```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang = english_lang.merge(city_populations, on="region")
english_lang
```
可以看到，每个城市的人口都是正确的（例如 Montréal：4098927，Toronto：5928040），
从这里就可以接着做我们的分析了。

## 小结

清洗和整理数据可能非常耗时。不过，这是任何数据分析中至关重要的一步。
我们探索了许多把数据清洗、整理成整洁格式的函数。
{numref}`tab:summary-functions-table` 汇总了本章学到的一些关键整理
函数。后续各章会讲到，你可以拿这份整洁数据做更多的事情，
去回答那些让你迫切想找到答案的数据科学问题！

+++

```{table} 数据整理函数汇总
:name: tab:summary-functions-table

| 函数 | 说明 |
| ---      | ----------- |
| `agg` | 计算输入的聚合汇总 |
| `assign` | 在数据框中添加或修改列  |
| `groupby` |  可以对若干行组成的分组应用函数 |
| `iloc` | 用整数索引取数据框的列/行子集 |
| `loc` | 用标签取数据框的列/行子集 |
| `melt` | 一般使数据框变长、变窄 |
| `merge` | 合并两个数据框 |
| `pivot` | 一般使数据框变宽、行数减少 |
| `str.split` | 把字符串列拆分成多列  |
```

## 习题

本章内容的练习题可以在配套的
[练习册仓库](https://worksheets.python.datasciencebook.ca)的
“数据清洗与整理（Cleaning and wrangling data）”一行中找到。你可以预览
本章练习册（worksheet）的非交互版本，只需点击“查看练习册（view worksheet）”。
如果要交互式地做习题，请按照练习册仓库中的说明下载所有练习册，并按照
{numref}`第 %s 章 <move-to-your-own-machine>` 中的计算机环境配置说明操作。
这样才能保证练习册提供的自动反馈和指导按预期正常工作。

+++ {"tags": []}

## 拓展资源

- [`pandas` 包文档](https://pandas.pydata.org/docs/reference/index.html) 是
  另一份资源，可以进一步了解本章的函数、
  可以使用的全部参数，以及其他相关函数。
- [《Python for Data Analysis》](https://wesmckinney.com/book/) {cite:p}`mckinney2012python` 有几章与
  数据整理有关，比本书讲得更深入。例如，
  [数据整理一章](https://wesmckinney.com/book/data-wrangling.html)介绍了整洁数据、
  `melt` 和 `pivot`，也介绍了缺失值
  和更多整理函数（如 `stack`）。
  [数据聚合一章](https://wesmckinney.com/book/data-aggregation.html)介绍了
  `groupby`、聚合函数、`apply` 等。
- 偶尔你会遇到需要遍历数据框中各个条目的情形，而上面这些函数都不够灵活，
  做不到你想要的效果。这时可以考虑使用
  [for 循环](https://wesmckinney.com/book/python-basics.html#control_for) {cite:p}`mckinney2012python`。


+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
