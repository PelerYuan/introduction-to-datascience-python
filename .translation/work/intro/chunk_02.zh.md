## 用 `[]` 和 `loc[]` 创建数据框的子集

```{index} see: []; DataFrame
```

```{index} see: loc[]; DataFrame
```

```{index} DataFrame; [], DataFrame; loc[], 选取列
```

现在数据已经读入 Python，我们可以开始整理它，找出 2016 年在加拿大被报告为母语最多的十种原住民语言。具体来说，我们要构造一张表，列出 `mother_tongue` 列中计数最大的十种原住民语言。第一步，从 `can_lang` 数据中只取出对应原住民语言的那些行；第二步，只保留 `language` 和 `mother_tongue` 两列。`pandas` 数据框上的 `[]` 和 `loc[]` 操作正好能帮上忙。`[]` 可以取数据框行的一个子集（即*筛选*），也可以取数据框列的一个子集（即*选取*）。`loc[]` 操作则允许你*同时*筛选行*并*选取列。我们先考察用 `[]` 操作筛选行和选取列，然后在原住民语言数据的分析中用 `loc[]` 一次完成这两件事。

```{note}
`pandas` 中的 `[]` 和 `loc[]` 操作，以及与之相关的操作，远比本章描述的强大。
以后你会学到更精细的数据框索引方法，见 {numref}`第 %s 章 <wrangling>`。
```

### 用 `[]` 筛选行
观察上面的 `can_lang` 数据，可以看到 `category` 列包含几种高层级的语言类别，其中有“原住民语言”（Aboriginal languages）、“非官方且非原住民语言”（Non-Official & Non-Aboriginal languages）和“官方语言”（Official languages）。要回答我们的问题，就得筛选这份数据集，把注意力限制在属于“原住民语言”这一类别的语言上。

```{index} DataFrame; [], 筛选行, 逻辑表达式, 逻辑运算符; 相等运算符 (==), 字符串
```

我们可以用 `[]` 操作，从数据框中取出取值为所需的那部分行。{numref}`img-filter` 给出了用 `[]` 操作筛选行时要用的语法。先写数据框的名字——这里是 `can_lang`——再写一对方括号。方括号里面写筛选行时要用的*逻辑表达式*（logical statement）。逻辑表达式会对数据框中的每一行求值，结果是 `True` 或 `False`；`[]` 操作只保留逻辑表达式取值为 `True` 的那些行。例如，在我们的分析中，我们只想保留属于 `"Aboriginal languages"` 这个高层级类别的语言。可以用*相等运算符*（equivalency operator）`==` 把 `category` 列的取值——记作 `can_lang["category"]`——与取值 `"Aboriginal languages"` 作比较。你在 {numref}`第 %s 章 <wrangling>` 中还会学到许多其他类型的逻辑表达式。之前读取数据文件时，我们给文件名加了引号；这里同样要给 `"Aboriginal languages"` 和 `"category"` 都加上引号。加引号是告诉 Python，这是一个*字符串取值*（例如列名或文字数据），而不是构成 Python 编程语言的那些特殊单词，也不是我们在已经写过的代码中给对象起的名字。

```{note}
在 Python 中，单引号（`'`）和双引号（`"`）通常没有区别。所以上面的 `"Aboriginal languages"` 也可以写成 `'Aboriginal languages'`，`"category"` 也可以写成 `'category'`。
你自己把两种写法都试一下吧！
```

```{figure} img/intro/filter_rows.png
---
name: img-filter
---
用 `[]` 操作筛选行的语法。
```

该操作返回的数据框包含输入数据框的全部列，但只保留逻辑表达式中指定的那些原住民语言对应的行。

```{code-cell} ipython3
:tags: ["output_scroll"]
can_lang[can_lang["category"] == "Aboriginal languages"]
```

### 用 `[]` 选取列


```{index} DataFrame; [], 选取列
```

我们也可以用 `[]` 操作从数据框中选取列。{numref}`img-select` 给出了选取列所需的语法。同样先写数据框的名字——这里是 `can_lang`——再写一对方括号。方括号里面给出一个列名组成的*列表*（list）。在 Python 中，我们用方括号表示*列表*，其中每个元素用逗号（`,`）分隔。因此，如果只想从原来的 `can_lang` 数据框中选取 `language` 和 `mother_tongue` 两列，就把包含这两个列名的列表 `["language", "mother_tongue"]` 放进 `[]` 操作的方括号中。

```{figure} img/intro/select_columns.png
---
name: img-select
---
用 `[]` 操作选取列的语法。
```

该操作返回的数据框包含输入数据框的全部行，但只保留我们在选取列表中写出的那些列。

```{code-cell} ipython3
can_lang[["language", "mother_tongue"]]
```

### 用 `loc[]` 筛选行并选取列

```{index} DataFrame; loc[], 选取列
```

`[]` 操作只用于筛选行*或*选取列，不能同时完成这两件事。但要回答本章最初的数据分析问题，我们必须*既*按原住民语言筛选行，*又*选取 `language` 和 `mother_tongue` 两列。好在 `pandas` 提供了 `loc[]` 操作，可以一次做到。它的语法和我们刚讲过的 `[]` 操作很像：本质上就是把前面的行筛选和列选取两步合在一起。具体来说，先写数据框的名字——还是 `can_lang`——后面接 `.loc[]` 操作。方括号里面，先写用于筛选行的逻辑表达式，然后写一个逗号，再写要选取的列组成的列表。

```{figure} img/intro/filter_rows_and_columns.png
---
name: img-loc
---
用 `loc[]` 操作筛选行并选取列的语法。
```

```{code-cell} ipython3
aboriginal_lang = can_lang.loc[can_lang["category"] == "Aboriginal languages", ["language", "mother_tongue"]]
```
这段代码里有一点很重要，需要留意。第一，我们在 `can_lang` 数据框上使用 `loc[]` 操作时写的是 `can_lang.loc[]`——先写数据框名，再写一个点，然后写 `loc[]`。又是这个点！回想一下，本章前面我们用过 `pandas` 中的 `read_csv` 函数（别名为 `pd`），当时写的是 `pd.read_csv`。点表示左边的东西（`pd`，即 `pandas` 包）*提供*右边的东西（`read_csv` 函数）。在 `can_lang.loc[]` 这个例子里，左边的东西（`can_lang` 数据框）*提供*右边的东西（`loc[]` 操作）。在 Python 中，包（比如 `pandas`）*和*对象（比如我们的 `can_lang` 数据框）都可以提供函数和其他对象，我们用点语法（dot syntax）来访问它们。

```{note}
关于术语的一点说明：当对象 `obj` 用点语法提供函数 `f` 时（如 `obj.f()`），我们有时把函数 `f` 称为 `obj` 的*方法*，或者说成 `obj` 上的*操作*。类似地，当对象 `obj` 用点语法提供另一个对象 `x` 时（如 `obj.x`），我们有时把对象 `x` 称为 `obj` 的*属性*。本书会一直使用这些术语，你在社区里也会经常看到它们。另外，程序员似乎总喜欢无缘无故地把人搞糊涂：指代来自包（比如 `pandas`）的函数和对象时，我们*不*用“方法”“操作”“属性”这些术语。例如，`pd.read_csv` 通常就只被称为函数，而不叫方法或操作，尽管它也用点语法。
```

到这一步，如果前面都做对了，`aboriginal_lang` 应该是一个数据框，其中*只*包含 `category` 为 `"Aboriginal languages"` 的行，并且*只*包含 `language` 和 `mother_tongue` 两列。在数据分析中每走一步，最好都把结果打印出来检查一下。
```{code-cell} ipython3
aboriginal_lang
```
可以看到，原来的 `can_lang` 数据集有 214 行，包含多种 `category`。数据框 `aboriginal_lang` 只有 67 行，而且看起来只包含原住民语言。看来 `loc[]` 操作给出的正是我们想要的结果！

## 用 `sort_values` 和 `head` 按排序后的取值选取行

```{index} DataFrame; sort_values, DataFrame; head
```

我们已经用数据框上的 `[]` 和 `loc[]` 操作，得到了只含数据集中原住民语言及其对应计数的表。不过，我们想知道说得最频繁的**十种**语言。下一步，我们把 `mother_tongue` 列从大到小排序，然后只取出最前面的十行。`sort_values` 和 `head` 两个函数正好来救场！

`sort_values` 函数可以按某一列的取值给数据框的行排序。要排序的列名通过参数 `by` 传给函数。我们想选出被报告为母语最多的十种原住民语言，所以用 `sort_values` 函数按 `mother_tongue` 列给 `selected_lang` 数据框的行排序。我们要按降序（从大到小）排列，因此把参数 `ascending` 设为 `False`。

```{figure} img/intro/sort_values.png
---
name: img-sort-values
---
用 `sort_values` 按降序排列行的语法。
```

```{code-cell} ipython3
arranged_lang = aboriginal_lang.sort_values(by="mother_tongue", ascending=False)
arranged_lang
```

接下来，我们只选取 `arranged_lang` 数据框的前十行，就能得到最常见的十种原住民语言。这一步用 `head` 函数完成，并把参数指定为 `10`。


```{code-cell} ipython3
ten_lang = arranged_lang.head(10)
ten_lang
```

(ch1-adding-modifying)=
## 添加和修改列

```{index} 添加列, 修改列
```

回想一下，我们的数据分析问题问的是：报告说得最多的前十种原住民语言，每种语言各有多少加拿大居民把它当作母语；`ten_lang` 数据框里确实有这些*计数*……不过，看到这些数字，我们也许会对每个计数对应加拿大人口的*百分比*感到好奇。回答第一个问题时，常常又会冒出新的数据分析问题——所以别害怕，尽管去探索！为了顺便回答这个小问题，我们要用 `mother_tongue` 列中的每个计数除以 2016 年人口普查得到的加拿大总人口——即 35,151,728——再乘以 100。这个计算可以写成 `100 * ten_lang["mother_tongue"] / canadian_population`。然后，要把结果存进一个新列（或覆盖已有的列），就先写出要新建的列名（要修改的旧列名），再写赋值符号 `=`，最后写要存入该列的计算式。这里我们选择新建一列，命名为 `mother_tongue_percent`。

```{note}
下面你会看到，我们在 Python 里把加拿大人口写成 `35_151_728`。下划线（`_`）只是为了便于阅读，并不影响 Python 对这个数字的解释。换句话说，在 Python 中 `35151728` 和 `35_151_728` 完全等价，不过后者清楚得多！
```

```{code-cell} ipython3
:tags: [remove-cell]
# disable setting with copy warning
# it's not important for this chapter and just distracting
# only occurs here because we did a much earlier .loc operation that is being picked up below by the coln assignment
pd.options.mode.chained_assignment = None
```

```{code-cell} ipython3
canadian_population = 35_151_728
ten_lang["mother_tongue_percent"] = 100 * ten_lang["mother_tongue"] / canadian_population
ten_lang
```

`ten_lang_percent` 数据框表明，`ten_lang` 数据框中的十种原住民语言，作为母语使用的人数占加拿大人口的 0.008% 到 0.18%。

## 用链式调用和多行表达式合并步骤

为了找出 2016 年在加拿大被报告为母语最多的十种原住民语言，我们用了 3 步。从 `can_lang` 数据框出发，我们：

1) 用 `loc` 筛选行，只留下 `Aboriginal languages` 类别，并选取
   `language` 和 `mother_tongue` 两列，
2) 用 `sort_values` 按 `mother_tongue` 降序排列这些行，并且
3) 用 `head` 只取前 10 个取值。

完成这些步骤的一种做法，就是直接写多行代码，边走边把中间结果存成临时对象。
```{code-cell} ipython3
aboriginal_lang = can_lang.loc[can_lang["category"] == "Aboriginal languages", ["language", "mother_tongue"]]
arranged_lang_sorted = aboriginal_lang.sort_values(by="mother_tongue", ascending=False)
ten_lang = arranged_lang_sorted.head(10)
```

```{index} 多行表达式
```

你可能觉得这段代码不好读。你没说错，确实不好读！可读性上主要有两个问题。第一，每一行代码都很长。很难看清到底调用了哪些方法、用了哪些参数。第二，每一行都引入一个新的临时对象。这里 `aboriginal_lang` 和 `arranged_lang_sorted` 都只是通往 `ten_lang` 数据框途中的临时结果。这样一来，代码既难读——因为得一步步追查每个临时对象去了哪里，也难懂——因为命名了很多对象，会让人以为它们很重要，其实它们只是中间产物。处理数据框时往往需要依次调用多个方法，所以这个问题很值得解决！

要解决第一个问题，我们可以把上面那些很长的表达式拆到多行。在大多数情况下，Python 中的一个表达式必须写在一行代码里，只有少数几种情形允许我们这样做。接下来我们用多行表达式（multiline expression）把这段代码改写成更好读的形式。

```{code-cell} ipython3
aboriginal_lang = can_lang.loc[
    can_lang["category"] == "Aboriginal languages",
    ["language", "mother_tongue"]
]
arranged_lang_sorted = aboriginal_lang.sort_values(
    by="mother_tongue",
    ascending=False
)
ten_lang = arranged_lang_sorted.head(10)
```

这段代码和前面展示的代码一样；可以看到，方法和参数的顺序完全相同。只是当表达式会变得又长又难读时，就把它拆到多行，从而提高代码的可读性。Python 怎么知道一个表达式还没写完、要接着读下一行呢？对于以 `aboriginal_lang = ...` 开头的那一行，Python 看到这行以左方括号符号 `[` 结尾，就知道在用一个对应的右方括号符号 `]` 把它闭合之前，表达式不会结束。我们放的两个参数和之前一样，对应的右方括号出现在 `["language", "mother_tongue"]` 之后）。对于以 `arranged_lang_sorted = ...` 开头的那一行，Python 看到这行以左圆括号符号 `(` 结尾，就知道在用对应的右圆括号符号 `)` 闭合之前表达式不会结束。这里用的两个参数同样和之前一样，对应的右圆括号就出现在 `ascending=False` 后面。这两种情况下，Python 都会继续读下一行，弄清楚表达式的其余部分是什么。当然，我们也可以把全部代码写在一行里，但拆到多行对代码可读性帮助很大。

```{index} 链式调用
```

还有一个问题要处理：每一行代码——也就是分析中的每一步——都会引入一个新的临时对象。要解决它，我们可以把多个操作*链*在一起，而不给中间对象赋值。链式调用（chaining）的关键在于，分析中每一步的*输出*都是一个数据框，因此你可以直接对每一步的输出来继续调用方法，一环接一环！这样代码更简洁，也更好读。下面的代码同时演示了多行表达式和链式调用。代码现在清爽多了，得到的 `ten_lang` 数据框与上面那段凌乱代码的结果完全等价！

```{code-cell} ipython3
# obtain the 10 most common Aboriginal languages
ten_lang = (
    can_lang.loc[
       can_lang["category"] == "Aboriginal languages",
       ["language", "mother_tongue"]
    ]
    .sort_values(by="mother_tongue", ascending=False)
    .head(10)
)
ten_lang
```

我们把这新的一段代码逐块拆开看。上面的代码以左圆括号 `(` 开头，因此 Python 知道要一直读到后面的行，直到找到对应的右圆括号符号 `)`。`loc` 方法和之前一样完成筛选和选取。接下来的一行以句点（`.`）开头，它把 `loc` 这一步的输出与下一个操作 `sort_values` *链*起来。既然 `loc` 的输出是一个数据框，我们就可以直接在它上面调用 `sort_values` 方法，而不必先给它起名字！下一行中的 `.sort_values` 做的正是这件事。最后，我们再次把 `sort_values` 的输出与 `head` *链*在一起，以取得最常见的 10 种语言。最后，与最开头那个左圆括号对应的右圆括号 `)` 出现在倒数第二行，整个多行表达式就此完成。链式调用不再创建中间对象，而是把一步操作的输出拿去做下一步操作。这样就省去了创建和存储中间对象的必要，代码因此更简洁，可读性也更好。

我们已经把链式调用作为存储临时对象、组合代码之外的另一种选择介绍给你了。那么，是不是就*绝不*该存储临时对象或组合代码呢？未必！有些时候，保留临时对象很方便。例如，你可以先把结果存成临时对象，再把它传给绘图函数，这样就可以反复调整图形，而不必把前面的数据变换全部重做一遍。把许多函数链在一起可能让人吃不消，也不容易调试；你可能希望在中途把结果存成临时对象，检查一下再继续后面的步骤。

## 用可视化探索数据

```{index} 可视化
```
`ten_lang` 这张表回答了最初的数据分析问题。我们做完了吗？还没有。表格几乎从来都不是把分析结果呈现给受众的最好方式。即使 `ten_lang` 只有两列，也还是有些不方便：比如，你得凑近了仔细看，才能大致感觉出各语言使用人数的相对多少。分析变得更复杂时，这个问题只会更严重。相比之下，*可视化*能以容易理解得多的方式传达这些信息。可视化是汇总信息的利器，能帮你有效地与受众沟通；做出有效的数据可视化，是任何数据分析都不可缺少的一环。本节我们要为 2016 年在加拿大被报告为母语最多的十种原住民语言，以及每种语言的使用人数，制作一张可视化图形。

### 用 `altair` 创建条形图

```{index} altair, 可视化; 条形图
```

在这份数据集中，`language` 和 `mother_tongue` 分别位于不同的列（也就是变量），而且每种语言占一行（也就是一个观测）。所以，这份数据属于我们所说的*整洁数据*（tidy data）格式。整洁数据是一个基本概念，也是本书余下部分的重要主题：`pandas` 中的许多函数都要求数据是整洁的，我们马上要用来做可视化的 `altair` 包也是如此。我们会在 {numref}`第 %s 章 <wrangling>` 中正式介绍整洁数据。

```{index} see: 图形; 可视化
```

```{index} see: 可视化; altair
```

我们要用条形图把数据可视化。条形图的条形长度表示某些取值，比如计数或比例。我们用 `ten_lang` 数据框中的 `mother_tongue` 和 `language` 两列做一张条形图。要用 `altair` 包为这两个变量画条形图，必须指明用哪个数据框、把哪些变量放在 x 轴和 y 轴上，以及要画哪种图。第一步，先导入 `altair` 包。

```{code-cell} ipython3
import altair as alt
```

```{index} altair; mark_bar, altair; 编码通道
```

+++

`altair` 中最基本的对象是 `Chart`，它接收一个数据框作为参数：`alt.Chart(ten_lang)`。有了图形对象之后，就可以指定希望数据怎样被可视化。先说明用什么图形*标记*来表示数据。这里我们用 `Chart.mark_bar` 函数设置图形对象的标记属性，因为要画的是条形图。接下来，我们需要用 `x` 和 `y` *编码通道*（encoding channel）来*编码*数据框中的变量（它们分别表示各个点在 x 轴和 y 轴上的位置）。这用 `encode()` 函数完成：我们指定 `language` 列对应 x 轴，`mother_tongue` 列对应 y 轴。

```{figure} img/intro/altair_syntax.png
---
name: img-altair
---
用 `altair` 制作条形图的语法。
```