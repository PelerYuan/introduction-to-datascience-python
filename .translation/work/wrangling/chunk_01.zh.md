
(wrangling)=
# 数据清洗与整理

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
import pandas as pd
pd.set_option("display.max_rows", 20)
```

## 概述

本章围绕整洁数据（tidy data）的定义展开——它是一种适合分析的数据格式——并介绍把原始数据转换成这种格式所需的工具。
这些内容会结合一个真实的数据科学应用来讲解，让你有机会完整地练习一个案例分析。

+++

## 本章学习目标

学完本章后，你将能够：

- 定义“整洁数据”这一术语。
- 讨论用整洁数据格式存储数据的优势。
- 定义 Python 中的序列（series）和数据框（data frame），并说明二者的关系。
- 描述 Python 中常见的数据类型及其用途。
- 在数据整理任务中按各自的预期用途使用以下函数：
    - `melt`
    - `pivot`
    - `reset_index`
    - `str.split`
    - `agg`
    - `assign` 和常规列赋值
    - `groupby`
    - `merge`
- 在数据整理任务中按各自的预期用途使用以下运算符：
    - `==`、`!=`、`<`、`>`、`<=` 和 `>=`
    - `isin`
    - `&` 和 `|`
    - `[]`、`loc[]` 和 `iloc[]`

## 数据框与序列

在 {numref}`第 %s 章 <intro>` 和 {numref}`第 %s 章 <reading>` 中，重点是*数据框*：
我们学会了如何把数据导入 Python 并成为一个数据框，以及如何在 Python 中对数据框做基本操作。
在本书余下的部分里，这个模式会一直延续。我们用到的大多数工具都会要求
数据在 Python 中以 `pandas` **数据框**的形式表示。因此，本节会深入探讨
数据框究竟是什么，以及它在 Python 中如何表示。
掌握这些知识，有助于我们在数据分析中更有效地运用这些对象。

+++

### 什么是数据框？

```{index} 数据框; 定义
```

```{index} see: 数据框; DataFrame
```

```{index} DataFrame
```

数据框是 Python 中存储数据的表格状结构。数据框值得学习，
因为你在实践中遇到的大多数数据都能自然地存成一张表。为了精确定义数据框，
我们需要先引入几个技术术语：

```{index} 变量, 观测, 取值
```

- **变量（variable）：** 可以被测量的一种特征、数值或数量。
- **观测（observation）：** 给定实体的全部测量值。
- **取值（value）：** 给定实体在单个变量上的一次测量值。

有了这些定义，**数据框**就是 Python 中一种用来存放观测、变量及其取值的
表格型数据结构。最常见的情形是，数据框的每一列对应一个变量，
每一行对应一条观测。例如，
{numref}`fig:02-obs` 展示了一份城市人口数据集。这里，变量
是“region、year、population”；它们每一个都是可以收集或测量的属性。
第一条观测是“Toronto, 2016, 2235145”；
这些就是三个变量在数据集中第一个实体上各自的取值。该数据集共有
13 个实体，对应 {numref}`fig:02-obs` 中的 13 行。

+++

```{figure} img/wrangling/data_frame_slides_cdn.004.png
:name: fig:02-obs
:figclass: figure

存储加拿大各地区人口数据的数据框。在这个示例数据框中，与温哥华市这条观测对应的行用黄色标出，与 population 变量对应的列用蓝色标出。
```

### 什么是序列？

```{index} Series
```

在 Python 中，`pandas` 的**序列**是像列表一样可以包含一个或多个元素的对象。
它只有一列，是有序的，可以被索引，并且可以存放任意数据类型。
`pandas` 包用 `Series` 对象来表示数据框中的各列。
`Series` 里可以混放多种数据类型，但良好的做法是让一个序列只包含一种类型，
因为同一个变量的所有观测都应该是同一类型。
Python 有若干种不同的基本数据类型，如
{numref}`tab:datatype-table` 所示。你可以用
`pd.Series()` 函数创建 `pandas` 序列。例如，要创建
{numref}`fig:02-series` 中所示的序列 `region`，可以这样写。

```{code-cell} ipython3
import pandas as pd

region = pd.Series(["Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa"])
region
```

+++ {"tags": []}

```{figure} img/wrangling/pandas_dataframe_series.png
:name: fig:02-series
:figclass: figure

类型为字符串的 `pandas` 序列示例。
```

```{index} 数据类型; 字符串 (str), 数据类型; 整数 (int), 数据类型; 浮点数 (float), 数据类型; 布尔值 (bool), 数据类型; NoneType (none)
```

```{index} see: str; 数据类型
```

```{index} see: int; 数据类型
```

```{index} see: float; 数据类型
```

```{index} see: bool; 数据类型
```

```{index} see: NoneType; 数据类型
```

```{table} Python 的基本数据类型
:name: tab:datatype-table
| 数据类型              | 缩写         | 说明                                          | 示例                                       |
| :-------------------- | :----------- | :-------------------------------------------- | :----------------------------------------- |
| 整数                  | `int`        | 正整数、负整数或零                            | `42`                                       |
| 浮点数                | `float`      | 十进制形式表示的实数                          | `3.14159`                                  |
| 布尔值                | `bool`       | 真或假                                        | `True`                                     |
| 字符串                | `str`        | 文本                                          | `"Hello World"`                            |
| 空值                  | `NoneType`   | 表示没有取值                                  | `None`                                     |
```

+++

在 Python 中，务必用正确的类型来表示数据。本书用到的许多
`pandas` 函数对不同的数据类型有不同的处理方式。你应该用 `int` 和 `float` 类型
表示数值，并用它们做算术运算。`int` 类型用于没有小数点的整数，
而 `float` 类型用于带小数点的数。
`bool` 类型表示布尔变量，只能取两个值之一：`True` 或 `False`。
`string` 类型用来表示应当被看作“文本”的数据，
例如单词、名称、路径和 URL 等等。
`NoneType` 是 Python 中的一种特殊类型，用来表示没有取值；例如，
数据缺失时就可能出现这种情况。Python 还有其他基本数据类型，但本书
一般不会用到。


### 这与数据框有什么关系？

+++

```{index} 数据框; 定义
```

数据框其实就是若干序列拼在一起形成的集合，
其中每个序列对应一列，而且所有序列的长度必须相同。
不过，数据框中的列不必都是同一类型。
{numref}`fig:02-dataframe` 展示了一个数据框，其中各列是不同类型的序列。
但同一列*内部*的每个元素通常应该是同一类型，因为同一个变量的取值
通常都是同一类型。例如，如果变量是城市名称，
这个名称应该是字符串；如果变量是年份，那它应该是整数。
所以，尽管序列允许你放不同类型的数据，最常见的做法
（也是良好实践！）仍是每列只用一种类型。

+++ {"tags": []}

```{figure} img/wrangling/pandas_dataframe_series-3.png
:name: fig:02-dataframe
:figclass: figure

数据框与序列的类型。
```


```{index} 类型
```

```{note}
你可以对数据对象使用 `type` 函数。
例如，我们可以检查前几章用过的那份加拿大语言数据集
`can_lang` 属于哪个类，可以看到它是 `pandas.core.frame.DataFrame`。
```


```{code-cell} ipython3
can_lang = pd.read_csv("data/can_lang.csv")
type(can_lang)
```

### Python 中的数据结构

`Series` 和 `DataFrame` 是 Python 中的*数据结构*，
它们对大多数数据分析来说都是核心概念。
我们用到的 `pandas` 函数往往根据具体操作返回 `DataFrame`
或 `Series`。由于
`Series` 本质上就是简单的 `DataFrames`，本书正文里会把
`DataFrames` 和 `Series` 都称作“数据框”。
Python 中还有其他表示数据结构的类型。
最常见的几种汇总在 {numref}`tab:datastruc-table` 中。

```{index} 数据结构; 列表, 数据结构; 集合, 数据结构; 字典 (dict), 数据结构; 元组
```

```{index} see: dict; 数据结构
```

```{table} Python 的基本数据结构
:name: tab:datastruc-table
| 数据结构 | 说明 |
| ---            | ----------- |
| list | 一种有序的取值集合，可以同时存放多种数据类型。 |
| dict | 一种带标签的数据结构，其中 `keys` 与 `values` 成对出现 |
| Series | 一种*带标签*的有序取值集合，可以同时存放多种数据类型。 |
| DataFrame | 一种带标签的数据结构，其 `Series` 列可以有不同的类型。 |
```

`list`（列表）是一种有序的取值集合。创建列表时，把列表的内容放在
方括号 `[]` 之间，各项之间用逗号隔开。`list` 可以包含
不同类型的取值。下面的例子包含六个 `str` 条目。

```{code-cell} ipython3
cities = ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Winnipeg"]
cities
```
列表可以直接转换成 pandas 的 `Series`。
```{code-cell} ipython3
cities_series = pd.Series(cities)
cities_series
```

`dict`，也就是字典（dictionary），包含成对的“键”和“取值”。
你用键来查找与之对应的取值。字典用花括号 `{}` 创建。
每个条目左边是键，接着是一个冒号 `:`，然后是取值。
一个字典可以包含多组键值对（key–value pair），各组之间用逗号隔开。
键可以是很多种类型（常用的是 `int` 和 `str`），取值可以是任意类型；
同一个字典里各组键值对的类型也都可以不同。
下面的例子创建了一个有两个键的字典：`"cities"` 和 `"population"`。
与每个键对应的取值都是列表。

```{code-cell} ipython3
population_in_2016 = {
  "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Winnipeg"],
  "population": [2235145, 1027613, 1823281, 544870, 571146, 321484]
}
population_in_2016
```

字典可以转换成数据框。键
会成为列名，取值会成为相应列中的条目。
字典本身是很简单的对象；最好改用数据框，
因为这样才能用上 `pandas` 内置的功能（例如 `loc[]`、`[]`，
以及后面几节会讲到的许多函数）！

```{code-cell} ipython3
population_in_2016_df = pd.DataFrame(population_in_2016)
population_in_2016_df
```

当然，不必先单独给字典命名再传给
`pd.DataFrame`；我们也可以直接在调用中构造字典。
这往往是创建新数据框最方便的方式。

```{code-cell} ipython3
population_in_2016_df = pd.DataFrame({
  "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Winnipeg"],
  "population": [2235145, 1027613, 1823281, 544870, 571146, 321484]
})
population_in_2016_df
```

+++

## 整洁数据

```{index} 整洁数据; 定义
```

表格型数据集可以有多种组织方式。我们前面看过的数据框
采用的都是**整洁数据**这种组织格式。
本章将重点介绍整洁数据格式，
以及如何把原始（而且很可能混乱）的数据整理整洁。整洁数据框满足
以下三条标准 {cite:p}`wickham2014tidy`：

  - 每一行是一条观测，
  - 每一列是一个变量，
  - 每个取值只占一个单元格（也就是说，它在数据框中的
    条目不与别的取值共用）。

{numref}`fig:02-tidy-image` 展示了一份满足这三条标准的整洁数据集。

+++ {"tags": []}

```{figure} img/wrangling/tidy_data.001.png
:name: fig:02-tidy-image
:figclass: figure

整洁数据满足三条标准。
```

+++

```{index} 整洁数据; 理由
```

在分析的第一步就确保数据整洁，有很多充分的理由。
最重要的理由是：整洁数据是一种统一、一致的格式，
`pandas` 中几乎每个函数都能识别它。无论数据中的变量和观测
代表什么，只要数据框是整洁的，
你就可以用同一套工具去操作它、绘制图形并分析它。
如果数据*不*整洁，你在分析中就必须写专门的定制代码，
这类代码很容易出错，别人也很难看懂。
除了让分析更容易被别人理解、更不容易出错之外，整洁数据
通常也便于人解读。既然有这些好处，
事先花时间把数据整理成整洁格式就很值得。好在 `pandas` 提供了
许多设计良好的数据清洗与整理工具，能帮你轻松地把数据整理整洁。
下面我们就来看看它们！

```{note}
对一份给定的数据集来说，整洁数据只有一种形状吗？不一定！
这取决于你提的统计问题，以及该问题涉及哪些变量。
对整洁数据而言，每个变量都应该单独占一列。
因此，正如必须让统计问题与合适的数据分析工具相匹配一样，
你也必须让统计问题与合适的变量相匹配，
并确保这些变量各自表示为单独的列，从而使数据整洁。
```

+++

### 整理数据：用 `melt` 从宽格式变成长格式

```{index} DataFrame; melt
```

要让数据变成整洁格式，一项常见的操作
是把分别存在不同列里、但实际上属于同一个变量的取值合并到一列。
数据常常以这种方式存储，
因为这种格式有时更直观，便于人阅读和理解，而数据集正是由人创建的。
在 {numref}`fig:02-wide-to-long` 中，
左边的表格采用不整洁的“宽”格式（wide format），
因为年份取值
（2006、2011、2016）被存成了列名。
随之而来的后果是，
各个城市在这些年份的人口取值
也被拆到了好几列里。

对人来说，这张表很容易读，所以你经常会看到数据
以这种宽格式存储。不过，要用 Python 做数据可视化或统计分析时，
这种格式就很难处理。例如，
我们想找出最新的年份，就会很棘手，因为年份取值被存成了列名，
而不是某一列里的取值。所以，在用函数找出最新年份（例如
用 `max`）之前，我们必须先把列名提取出来组成一个列表，
再用函数从中找出最新的年份。
如果你想找出某个地区在最新年份的人口取值，问题只会更麻烦。
数据整理整洁之后，这两项任务都会大大简化。

这种格式的另一个问题是，我们并不知道
每个年份下面那些数字究竟代表什么。这些数字代表
人口规模吗？还是土地面积？并不清楚。
要同时解决这两个问题，
我们可以创建名为“year”的列和名为“population”的列，
把这份数据集重塑成整洁数据格式。
这一变换让数据变得更“长”，即成为长格式（long format）；
结果就是 {numref}`fig:02-wide-to-long` 中右边的表格。注意，经过这次变换，
数据框中的条目数可能会变。“不整洁”的数据有 5 行 3 列，
共 15 个条目；而右边“整洁”的数据有 15 行 2 列，
共 30 个条目。

+++ {"tags": []}

```{figure} img/wrangling/pivot_functions.001.png
:name: fig:02-wide-to-long
:figclass: figure



用 `melt` 把数据从宽格式转为长格式。
```

+++

```{index} 加拿大语言
```

在 Python 中，我们可以用 `pandas` 包里的 `melt` 函数实现这一效果。
`melt` 函数会把多列合并起来，
通常在我们需要让数据框变长变窄、整理数据时使用。
为了学会使用 `melt`，我们来看一个使用
`region_lang_top5_cities_wide.csv` 数据集的例子。这份数据集给出
2016 年加拿大人口普查中，多伦多、蒙特利尔、温哥华、卡尔加里和
埃德蒙顿五个加拿大主要城市里，有多少加拿大人把每种语言列为母语的计数。
开始之前，
我们先用 `pd.read_csv` 读入这份（不整洁的）数据。

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_wide = pd.read_csv("data/region_lang_top5_cities_wide.csv")
lang_wide
```

上面这种不整洁格式有什么问题？
{numref}`fig:img-pivot-longer-with-table` 中左边的表格
以“宽”（混乱）格式表示数据。
从数据分析的角度看，这种格式并不理想，因为
*region* 变量（多伦多、蒙特利尔、温哥华、卡尔加里和埃德蒙顿）的取值
被存成了列名。因此，
我们要对数据集使用的那些数据分析函数无法方便地取到这些取值。
另外，*母语*变量的取值
分散在多列中，在我们把它们合并成一列之前，就无法完成
任何想要的可视化或统计任务。
举例来说，假设我们想知道在全部五个地区中，
被最多加拿大人作为母语报告的语言是哪些。
用当前格式的数据回答这个问题会很困难。
用这种格式的数据我们*确实*能找到答案，
但如果先把数据整理整洁，回答起来会容易得多。
假如母语改存成一列，
如 {numref}`fig:img-pivot-longer-with-table` 右边整洁数据所示，
我们只需一行代码（`df["mother_tongue"].max()`）
就能得到最大值。

+++ {"tags": []}

```{figure} img/wrangling/pandas_melt_wide-long.png
:name: fig:img-pivot-longer-with-table
:figclass: figure

用 `melt` 函数把数据从宽格式转为长格式。
```
