
(intro)=
# Python 与 Pandas

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
```

## 概述

本章介绍数据科学与 Python 编程语言。我们的目标是让你从一开始就动手实干！我们会完整走一遍数据分析的流程，并在过程中介绍不同类型的数据分析问题、Python 中的一些基本编程概念，以及读取、清洗和可视化数据的基础知识。后续各章会逐一深入讲解这些步骤；不过现在，我们先直接上手，看看用数据科学能做多少事情！

## 本章学习目标

学完本章后，你将能够：

- 识别数据分析问题的不同类型，并把一个问题归入正确的类型。
- 把 `pandas` 包导入 Python。
- 用 `read_csv` 读取表格型数据（tabular data）。
- 使用赋值符号在 Python 中创建新的变量和对象。
- 使用 `[]`、`loc[]`、`sort_values` 和 `head` 创建并整理表格型数据的子集。
- 使用列赋值在表格型数据中添加和修改列。
- 把多个操作依次串联起来。
- 用 `altair` 条形图可视化数据。
- 使用 `help()` 和 `?` 访问 Python 的帮助与文档工具。



## 加拿大语言数据集

```{index} 加拿大语言
```

本章会完整分析一份数据集，其中记录的是加拿大居民在家使用的语言（{numref}`canadamap`）。加拿大生活着许多原住民，他们有自己的文化和语言；这些语言往往为加拿大所独有，世界上其他地方并不使用 {cite:p}`statcan2018mothertongue`。令人痛心的是，殖民化导致其中许多语言消亡。例如，在加拿大的寄宿学校（residential schools）里，一代又一代儿童被禁止说自己的母语（母语是一个人幼年最先学会的语言）。殖民者还把他们“发现”的地方重新命名 {cite:p}`wilson2018`。这类行为严重损害了加拿大原住民语言的延续，有些语言因为报告会说的人很少，已被视为“濒危”。要了解更多内容，请参看《Canadian Geographic》杂志的文章《Mapping Indigenous Languages in Canada》{cite:p}`walker2017`、《他们为孩子而来：加拿大、原住民与寄宿学校》（*They Came for the Children: Canada, Aboriginal peoples, and Residential Schools*）{cite:p}`children2012`，以及加拿大真相与和解委员会（Truth and Reconciliation Commission）的《行动呼吁》（*Calls to Action*）{cite:p}`calls2015`。

```{figure} img/intro/canada_map.png
---
name: canadamap
---
加拿大地图。
```

本章要研究的数据集取自 [`canlang` R 数据包](https://ttimbers.github.io/canlang/) {cite:p}`timbers2020canlang`，其中包含 2016 年加拿大人口普查 {cite:p}`cancensus2016` 收集的人口语言数据。这份数据记录了 214 种语言，每种语言有六个不同的属性：

1. `category`：更高层级的语言类别，说明该语言是加拿大官方语言、原住民（Aboriginal，即 Indigenous）语言，还是非官方且非原住民的语言。
2. `language`：语言的名称。
3. `mother_tongue`：报告该语言为自己母语的加拿大居民人数。母语一般定义为一个人自出生起就接触的语言。
4. `most_at_home`：报告该语言为家中最常用语言的加拿大居民人数。
5. `most_at_work`：报告工作中最常使用该语言的加拿大居民人数。
6. `lang_known`：报告掌握该语言的加拿大居民人数。

据人口普查，在加拿大报告使用的原住民语言超过 60 种。假设我们想知道哪些语言最为常见，那么我们可能会提出下面这个问题，并希望用数据来回答它：

*2016 年在加拿大被报告为母语最多的十种原住民语言是哪些，每种语言各有多少人使用？*

```{index} 数据科学; 良好实践
```

```{note}
要做好数据科学，就必须深入理解数据和问题所在的领域。本书为了聚焦方法与基本概念，简化了示例中使用的数据集。但在现实生活中，没有领域专家，你无法也不应该做数据科学。换个角度说，在自己擅长的领域里做数据科学也很常见！请记住，处理数据时，务必思考数据是*如何*收集来的，这会影响你能得出什么结论。数据有偏差，结论就会有偏差！
```

## 提出问题

每一次出色的数据分析都始于一个*问题*——就像上面那个——你希望用数据来回答它。事实上，围绕数据的问题确实有若干不同的*类型*：描述性、探索性、预测性、推断性、因果性和机理性，{numref}`questions-table` 给出了它们的定义。{cite:p}`leek2015question,peng2015art` 在分析中尽早、审慎地提出问题——同时正确判断它属于哪一类——会决定你分析的整体思路，也会影响你选用哪些工具。

```{index} 问题; 数据分析, 描述性问题; 定义, 探索性问题; 定义
```

```{index} 预测性问题; 定义, 推断性问题; 定义, 因果性问题; 定义, 机理性问题; 定义
```

```{list-table} 数据分析问题的类型。
:header-rows: 1
:name: questions-table

* - 问题类型
  - 说明
  - 示例
* - 描述性
  - 针对数据集的汇总特征提问，但不作解释（即报告一个事实）。
  - 加拿大各省和地区分别有多少人居住？
* - 探索性
  - 询问单个数据集内部是否存在模式、趋势或关系。常用于为后续研究提出假设。
  - 在一份针对 2,000 名加拿大居民收集的数据中，政党投票会随财富指标变化吗？
* - 预测性
  - 询问如何预测个体（人或物）的测量值或标签。关注点在于哪些事物能预测某种结果，而不在于结果由什么造成。
  - 在下一届加拿大选举中，某人会把票投给哪个政党？
* - 推断性
  - 在单个数据集中寻找模式、趋势或关系，**并且**要求量化这些发现对更大人群的适用程度。
  - 对全体加拿大居民而言，政党投票会随财富指标变化吗？
* - 因果性
  - 询问在更大人群中，改变一个因素平均而言是否会导致另一个因素发生变化。
  - 在加拿大选举中，财富会导致人们投票给某个政党吗？
* - 机理性
  - 询问观察到的模式、趋势或关系背后的机制（即它是如何发生的？）。
  - 在加拿大选举中，财富是如何导致人们投票给某个政党的？

```


本书会教你回答前四类问题的方法：描述性、探索性、预测性和推断性问题；因果性与机理性问题超出了本书的范围。具体来说，你将学会使用下面这些分析工具：

```{index} 汇总; 概述, 可视化; 概述, 分类; 概述, 回归; 概述
```

```{index} 聚类; 概述, 估计; 概述
```

1. **汇总：** 计算并报告数据集的汇总值。
汇总最常用于回答描述性问题，
偶尔也有助于回答探索性问题。
例如，你可以用汇总来回答下面这个问题：
*这份数据集中，跑者的平均比赛用时是多少？*
汇总工具会在 {numref}`第 %s 章 <reading>` 和 {numref}`第 %s 章 <wrangling>` 中详细讲解，不过在全书正文中会经常用到。
1. **可视化：** 用图形展示数据。
可视化通常用于回答描述性问题和探索性问题，
但在回答 {numref}`questions-table` 中所有类型的问题时，都起着关键的辅助作用。
例如，你可以用可视化来回答下面这个问题：
*这份数据集中，跑者的比赛用时和年龄之间有关系吗？*
{numref}`第 %s 章 <viz>` 会详细讲解可视化，不过它在全书中同样会经常出现。
3. **分类：** 为一个新观测预测类别。
分类用于回答预测性问题。
例如，你可以用分类来回答下面这个问题：
*已知某个肿瘤的平均细胞面积和周长的测量值，该肿瘤是良性的还是恶性的？*
分类将在 {numref}`第 %s 章 <classification1>` 和 {numref}`第 %s 章 <classification2>` 中讲解。
4. **回归：** 为一个新观测预测定量取值。
回归也用于回答预测性问题。
例如，你可以用回归来回答下面这个问题：
*一名 20 岁、体重 50kg 的跑者，比赛用时会是多少？*
回归将在 {numref}`第 %s 章 <regression1>` 和 {numref}`第 %s 章 <regression2>` 中讲解。
5. **聚类：** 在数据集中找出此前未知或未标注的子组。聚类常用于回答探索性问题。
例如，你可以用聚类来回答下面这个问题：
*在 Amazon 上，哪些商品经常被一起购买？*
聚类将在 {numref}`第 %s 章 <clustering>` 中讲解。
6. **估计：** 从一个大群体中取少量个体进行测量，
并对该大群体的均值或比例作出合理推断。估计
用于回答推断性问题。
例如，你可以用估计来回答下面这个问题：
*在一项针对 100 名加拿大人手机持有情况的调查中，全体加拿大人口中拥有 Android 手机的比例是多少？*
估计将在 {numref}`第 %s 章 <inference>` 中讲解。

对照 {numref}`questions-table`，我们关于原住民语言的问题属于*描述性问题*：我们是在汇总一个数据集的各项特征，而不作进一步解释。再看一看上面的清单，看来我们应该用可视化，也许再加上一些汇总来回答这个问题。因此在本章余下的部分里，我们将着手制作一张可视化图形，展示 2016 年人口普查中加拿大最常见的十种原住民语言以及它们对应的计数。

## 读入表格型数据集

```{index} 表格型数据
```

数据集从本质上说就是一组有结构的数字和字符。除此之外，其实没有什么严格的规则；数据集可以有各种不同的形式！不过，你在实践中遇到的最常见的数据集形式大概是*表格型数据*。想想 Microsoft Excel 里的电子表格：表格型数据呈矩形，与电子表格很像，如 {numref}`img-spreadsheet-vs-data frame` 所示。本书主要关注表格型数据。

```{index} 数据框; 概述, 观测, 变量
```

本书用 Python 做数据分析，所以第一步是把数据读入 Python。把表格型数据读入 Python 后，它会表示为一个*数据框*（data frame）对象。{numref}`img-spreadsheet-vs-data frame` 说明 Python 数据框与电子表格非常相似。我们把行称为**观测**，那是我们收集数据的各个对象。在 {numref}`img-spreadsheet-vs-data frame` 中，观测就是各种语言。我们把列称为**变量**，那是每个观测的特征。在 {numref}`img-spreadsheet-vs-data frame` 中，变量是语言的类别、名称、母语使用者人数等。

```{figure} img/intro/spreadsheet_vs_df.png
---
height: 500px
name: img-spreadsheet-vs-data frame
---
Python 中的电子表格与数据框。
```

```{index} see: 逗号分隔值; csv
```

```{index} csv
```

我们要学习读入 Python 并转成数据框的第一种数据文件，是*逗号分隔值*格式（简称 `.csv`）。这类文件的文件名以 `.csv` 结尾，可以用 Microsoft Excel、Google Sheets 等常见电子表格程序打开和保存。例如，名为 `can_lang.csv` 的 `.csv` 文件就随[本书的代码](https://github.com/UBC-DSCI/introduction-to-datascience-python/tree/main/source/data)一同提供。如果用纯文本编辑器（比如记事本这种只显示文本、不带任何格式的程序）打开这份数据，我们会看到每一行数据都单独占一行，表格中的每一项用逗号分隔：

```text
category,language,mother_tongue,most_at_home,most_at_work,lang_known
Aboriginal languages,"Aboriginal languages, n.o.s.",590,235,30,665
Non-Official & Non-Aboriginal languages,Afrikaans,10260,4785,85,23415
Non-Official & Non-Aboriginal languages,"Afro-Asiatic languages, n.i.e.",1150,44
Non-Official & Non-Aboriginal languages,Akan (Twi),13460,5985,25,22150
Non-Official & Non-Aboriginal languages,Albanian,26895,13135,345,31930
Aboriginal languages,"Algonquian languages, n.i.e.",45,10,0,120
Aboriginal languages,Algonquin,1260,370,40,2480
Non-Official & Non-Aboriginal languages,American Sign Language,2685,3020,1145,21
Non-Official & Non-Aboriginal languages,Amharic,22465,12785,200,33670
```

```{index} 函数, 参数, 读取函数; read_csv
```

要把这些数据读入 Python，以便对它做各种事情（例如进行分析或制作数据可视化图形），我们需要用到*函数*。函数是 Python 中的一个特殊单词，它接收一些指令（我们称之为*参数*），然后做某件事。我们用来把 `.csv` 文件读入 Python 的函数叫 `read_csv`。在最基本的用法下，`read_csv` 要求数据文件：

- 有列名，也就是*表头*（header），
- 用逗号（`,`）分隔各列，并且
- 不含行名。

+++

```{index} 包, 导入, pandas
```

下面你会看到用 `read_csv` 函数把数据读入 Python 的代码。请注意，`read_csv` 函数并不包含在 Python 的基础安装中，也就是说，安装 Python 时它并不是可以直接使用的基本函数之一。因此，你需要先把它从别处导入，然后才能使用。我们从中导入它的地方称为 Python *包*。Python 包是一组函数的集合，导入之后，它们可以和 Python 内置包中的函数一起使用。具体来说，只要用 `import` 命令导入 [Python 的 `pandas` 包](https://pypi.org/project/pandas/) {cite:p}`reback2020pandas,mckinney-proc-scipy-2010`，就能使用 `read_csv` 函数。`pandas` 包中有很多函数，本书从头到尾都会用它们来读取、清洗、整理和可视化数据。

+++

```{code-cell} ipython3
import pandas as pd
```

这条命令分两部分。第一部分是 `import pandas`，用来导入 `pandas` 包；第二部分是 `as pd`，给 `pandas` 包起一个短得多的*别名*（即另一个名字）`pd`。现在只要写 `pd.read_csv`，就能使用 `read_csv` 函数，也就是先写包名，再写一个点，然后写函数名。你能看出为什么要给 `pandas` 起个更短的别名：如果每用一个函数都要在前面敲一遍 `pandas.`，代码就会变得又长又难读！

现在 `pandas` 包已经导入，我们只要给 `read_csv` 函数传入一个参数，就能使用它：文件名 `"can_lang.csv"`。代码中的文件名以及其他字母和单词都要加上引号，以便与构成 Python 编程语言的那些特殊单词（比如函数！）区分开。我们只需要提供文件名这一个参数，因为在默认用法下，我们的文件已经满足了 `read_csv` 函数要求的其他所有条件。{numref}`img-read-csv` 说明了如何用 `read_csv` 把数据读入 Python。

```{figure} img/intro/read_csv_function.png
---
name: img-read-csv
---
`read_csv` 函数的语法。
```


+++
```{code-cell} ipython3
:tags: ["output_scroll"]
pd.read_csv("data/can_lang.csv")

```



## 在 Python 中命名

我们用 `read_csv` 读入 2016 年加拿大人口普查的语言数据时，并没有给这个数据框起名字。因此数据只是打印在屏幕上，我们无法再对它做别的事情。这样用处不大。更有用的做法，是给 `read_csv` 输出的数据框起一个名字，这样以后分析数据和做可视化时就能引用它。

```{index} see: =; 赋值符号
```

```{index} 赋值符号, 字符串
```

在 Python 中给取值起名字要用*赋值符号*（assignment symbol），即等号 `=`。赋值符号左边写你想用的名字，右边写你希望这个名字指向的取值。在 Python 中，名字几乎可以用来指向任何东西，比如数字、单词（也就是由字符组成的*字符串*），以及数据框！下面我们把 `my_number` 设为 `3`（`1+2` 的结果），把 `name` 设为字符串 `"Alice"`。

```{code-cell} ipython3
my_number = 1 + 2
name = "Alice"
```

注意，用赋值符号 `=` 在 Python 中给东西命名时，不需要给要创建的名字加引号。因为我们是在明确告诉 Python，这个特殊单词代表右侧那个取值。只有赋值符号右侧充当*取值*的字符和单词——例如前面指定的文件名 `"data/can_lang.csv"`，或者上面的 `"Alice"`——才需要用引号括起来。

完成赋值之后，我们就可以用创建的特殊名字来代替它们对应的取值。例如，如果之后想对取值 `3` 做点什么，直接写 `my_number` 就行。我们来试着给 `my_number` 加上 2；你会看到 Python 把它理解为 2 加 3：

```{code-cell} ipython3
my_number + 2
```

```{index} 对象
```

对象名可以由字母、数字和下划线（`_`）组成。其他符号不行，因为它们在 Python 中各有自己的含义。例如，`-` 是减号；如果用 `-` 来命名，Python 会报错，我们就会得到一个错误！

```{code-cell} ipython3
:tags: ["remove-output"]
my-number = 1
```
```{code-cell} ipython3
:tags: ["remove-input"]
print("SyntaxError: cannot assign to expression here. Maybe you meant '==' instead of '='?")
```

```{index} 对象; 命名约定
```

Python 中对对象命名有一些约定。给对象命名时，我们建议只用小写字母、数字和下划线 `_` 来分隔名字中的单词。Python 区分大小写，也就是说 `Letter` 和 `letter` 在 Python 中是两个不同的对象。你还应该尽量给对象起有意义的名字。例如，你*可以*把一个数据框命名为 `x`。不过，改用 `language_data` 这类更有意义的名称，能帮你记住代码中每个名字代表什么。我们建议遵循 *[PEP 8](https://peps.python.org/pep-0008/)* 中列出的 **PEP 8** 命名约定 {cite:p}`pep8-style-guide`。下面我们用赋值符号，把从 `read_csv` 得到的 2016 年加拿大人口普查语言数据框命名为 `can_lang`。

```{code-cell} ipython3
can_lang = pd.read_csv("data/can_lang.csv")
```

等一下，这次什么都没发生！我们的数据呢？其实确实发生了事情：数据已经读入，并且现在与名字 `can_lang` 关联起来了。我们可以用这个名字来访问数据框，对它做各种事情。例如，只要输入数据框的名字，就会同时打印出开头几行和末尾几行。三个点（`...`）表示还有未打印出来的行。你还会看到，观测的个数（即行数）和变量的个数（即列数）就打印在数据框的下方（这里是 214 行、6 列）。像这样打印数据框的几行，是快速了解其中内容的好办法。

```{code-cell} ipython3
:tags: ["output_scroll"]
can_lang
```

<<TERM>>
race time = 比赛用时
runner = 跑者
summarization = 汇总
comma-separated values = 逗号分隔值
domain expert = 领域专家
<<END>>
