+++

```{code-cell} ipython3
:tags: []

barplot_mother_tongue = (
  alt.Chart(ten_lang).mark_bar().encode(x="language", y="mother_tongue")
)


```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("barplot-mother-tongue", barplot_mother_tongue, display=True)

```

:::{glue:figure} barplot-mother-tongue
:figwidth: 700px
:name: barplot-mother-tongue

加拿大居民最常报告为母语的十种原住民语言的条形图。
:::

+++

```{index} see: .; 链式调用
```

### 设置 `altair` 图表的格式

我们已经能给数据做可视化，用来帮助回答自己的问题，这当然令人兴奋，不过我们的工作还没有做完！我们还能（也应该）做更多事情，提升自己所创建数据可视化的可解释性。例如，Python 默认把列名当作坐标轴标签。而这些列名通常并没有提供足够的信息来说明列中的变量。我们真该把这个默认标签换成信息量更大的标签。在上面的例子里，Python 把列名 `mother_tongue` 用作 y 轴标签，但多数人并不知道那是什么意思；即便他们知道，也不知道这个变量是如何测量的，更不知道测量对象是哪些人。如果坐标轴标签写成“Mother Tongue (Number of Canadian Residents)”，信息量就大得多。为了让代码更易读，我们把它拆成多行来写，就像上一节使用 pandas 时那样。

```{index} 图形; 标签, 图形; 坐标轴标签, altair; alt.X, altair; alt.Y, altair; 标题
```

给我们在 `altair` 中创建的图形添加更多标签，是改进和完善数据可视化的一种常见而简便的做法。我们可以用 `alt.X` 和 `alt.Y` 配合 `title` 方法为 `altair` 对象的坐标轴添加标题，让轴标题包含更多信息（关于 `alt.X` 和 `alt.Y` 的更多内容，见 {numref}`第 %s 章 <viz>`）。同样，由于我们是把文字（例如 `"Mother Tongue (Number of Canadian Residents)"`）作为参数传给 `title` 方法，所以要用引号把它们括起来。我们还能做许多其他修改来进一步美化图形，这些内容将在 {numref}`第 %s 章 <viz>` 中介绍。

```{code-cell} ipython3
barplot_mother_tongue = alt.Chart(ten_lang).mark_bar().encode(
    x=alt.X("language").title("Language"),
    y=alt.Y("mother_tongue").title("Mother Tongue (Number of Canadian Residents)")
)
```


```{code-cell} ipython3
:tags: ["remove-cell"]

glue("barplot-mother-tongue-labs", barplot_mother_tongue, display=True)

```


:::{glue:figure} barplot-mother-tongue-labs
:figwidth: 700px
:name: barplot-mother-tongue-labs

加拿大居民最常报告为母语的十种原住民语言的条形图，其中标注了 x 轴和 y 轴标签。注意，这个可视化还没有完成，仍有需要改进的地方。
:::


结果见 {numref}`barplot-mother-tongue-labs`。这已经是相当大的改进了！接下来处理 {numref}`barplot-mother-tongue-labs` 中可视化的下一个主要问题：竖直方向的 x 轴标签目前让人很难读清各个语言名称。一个解决办法是旋转图形，让条形变成水平方向，而不是竖直方向。为此，我们把 x 轴和 y 轴对调：


```{code-cell} ipython3
barplot_mother_tongue_axis = alt.Chart(ten_lang).mark_bar().encode(
    x=alt.X("mother_tongue").title("Mother Tongue (Number of Canadian Residents)"),
    y=alt.Y("language").title("Language")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("barplot-mother-tongue-labs-axis", barplot_mother_tongue_axis, display=True)

```

:::{glue:figure} barplot-mother-tongue-labs-axis
:figwidth: 700px
:name: barplot-mother-tongue-labs-axis

加拿大居民最常报告为母语的十种原住民语言的水平条形图。这个可视化已经没有严重问题，但还可以进一步打磨。
:::

```{index} altair; 排序
```

如图所示 {numref}`barplot-mother-tongue-labs-axis`，我们又向前迈了一大步！这个可视化已经没有严重问题了。现在该对图形做进一步打磨，让它更适合回答我们在本章前面提出的问题。例如，如果按报告每种语言的加拿大居民人数来排列条形，而不是按字母顺序排列，图形就会更容易读懂。我们可以用 `sort` 方法重新排列条形，它根据变量（`mother_tongue`）在 `x-axis` 上的取值，给变量（这里是 `language`）排序。

```{code-cell} ipython3
ordered_barplot_mother_tongue = alt.Chart(ten_lang).mark_bar().encode(
    x=alt.X("mother_tongue").title("Mother Tongue (Number of Canadian Residents)"),
    y=alt.Y("language").sort("x").title("Language")
)
```

+++

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("barplot-mother-tongue-reorder", ordered_barplot_mother_tongue, display=True)

```


:::{glue:figure} barplot-mother-tongue-reorder
:figwidth: 700px
:name: barplot-mother-tongue-reorder

加拿大居民最常报告为母语的十种原住民语言的条形图，其中的条形已重新排列。
:::


{numref}`barplot-mother-tongue-reorder` 为我们最初的问题提供了非常清晰、条理分明的答案：根据 2016 年加拿大人口普查，我们可以看到最常报告的原住民语言是哪十种，以及每种语言有多少人使用。例如，可以看到最常报告的原住民语言是 Cree n.o.s.，有超过 60,000 名加拿大居民把它报告为母语。

```{note}
“n.o.s.”表示“not otherwise specified”（未另行指明），所以 Cree n.o.s. 指的是那些把母语
报告为克里语（Cree）的人。在这个数据集中，克里语各语言包含以下类别：Cree n.o.s.、Swampy
Cree、Plains Cree、Woods Cree，以及一个“Cree not included elsewhere”（未在别处列出）类别
（该类别包含 Moose Cree、Northern East Cree 和 Southern East Cree）
{cite:p}`language2016`。
```

### 融会贯通

```{index} 注释
```

```{index} see: #; 注释
```

下面这段代码把本章的全部内容整合到一起，并做了几处改动。具体来说，我们把所有步骤合并成一个表达式，并用左右圆括号符号 `(` 和 `)` 把它拆成多行书写。我们还用井号 `#` 在下面许多代码行旁边写了*注释*。Python 遇到 `#` 号时，会忽略该行中这个符号之后的所有文字。因此你可以用注释向别人解释代码，而且也许更重要的是，向未来的自己解释！养成给代码写注释的习惯能提高代码的可读性，这是很好的做法。

这个练习展示了 Python 的强大之处。我们只用了相对很少的几行代码，就完成了一整套数据科学工作流，还做出了效果很好的数据可视化！我们提出了问题，把数据读入 Python，整理了数据（用到 `[]`、`loc[]`、`sort_values` 和 `head`），并创建数据可视化来帮助回答这个问题。本章让你初步体验了数据科学工作流；请继续学习后面几章，更深入地了解其中的每一个步骤！

```{code-cell} ipython3
# load the data set
can_lang = pd.read_csv("data/can_lang.csv")

# obtain the 10 most common Aboriginal languages
ten_lang = (
    can_lang.loc[can_lang["category"] == "Aboriginal languages", ["language", "mother_tongue"]]
    .sort_values(by="mother_tongue", ascending=False)
    .head(10)
)

# create the visualization
ten_lang_plot = alt.Chart(ten_lang).mark_bar().encode(
    x=alt.X("mother_tongue").title("Mother Tongue (Number of Canadian Residents)"),
    y=alt.Y("language").sort("x").title("Language")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("final_plot", ten_lang_plot, display=True)

```


:::{glue:figure} final_plot
:figwidth: 700px
:name: final_plot

加拿大居民最常报告为母语的十种原住民语言的条形图。
:::

## 查阅文档

```{index} 文档
```

```{index} see: help; 文档
```

```{index} see: __doc__; 文档
```

`pandas` 包（以及其他包！）里的 Python 函数非常多，没有人能记住每一个函数的作用，也记不住我们必须传给它们的全部参数。好在 Python 提供了 `help` 函数，可以方便地快速调出大多数函数的文档。要用 `help` 函数查阅文档，只需把你感兴趣的函数名作为参数放进 `help` 函数即可。例如，如果你忘了 `pd.read_csv` 函数做什么，或者忘了到底该传入哪些参数，就可以运行下面的代码：

```{code-cell} ipython3
:tags: ["remove-output"]
help(pd.read_csv)
```

{numref}`help_read_csv` 展示了将会弹出的文档，其中包括函数的高层描述、它的参数、每个参数的说明，等等。注意，你现在可能会觉得文档里有些文字过于专业。别担心：随着你一步步读完本书，这些术语中有许多都会陆续介绍给你，你会慢慢学会理解和查阅像 {numref}`help_read_csv` 那样的文档。不过请记住，文档并不是为了*教*你某个函数而写的，它只是一个参考，用来*提醒*你已经从别处学过的函数的各种参数和用法。

+++

```{figure} img/intro/help_read_csv.png
---
height: 700px
name: help_read_csv
---
read_csv 函数的文档，其中包括高层描述、参数列表及每个参数的含义，等等。
```

+++

如果你在 JupyterLab 环境中工作，还有一些便利功能可以帮助你查找函数名、查阅文档。首先，除了 `help`，你还可以使用更简洁的 `?` 字符。例如，想查看 `pd.read_csv` 函数的文档，可以运行下面的代码：
```{code-cell} ipython3
:tags: ["remove-output"]
?pd.read_csv
```
你也可以先输入想用的函数的前几个字符，然后按 <kbd>Tab</kbd> 键，就会弹出一个小菜单，列出所有以这些字符开头的可用函数。这既有助于记住函数名，也能防止输入错误。

+++

```{figure} img/intro/completion_menu.png
---
height: 400px
name: completion_menu
---
输入 `pd.read` 并按下 <kbd>Tab</kbd> 键后显示的建议列表。
```

+++

想进一步了解要使用的函数，你可以输入完整名称，然后按住 <kbd>Shift</kbd> 不放再按 <kbd>Tab</kbd>，就会弹出帮助对话框，其中包含的信息与使用 `help()` 时相同。

+++

```{figure} img/intro/help_dialog.png
---
height: 400px
name: help_dialog
---
输入 `pd.read_csv` 后再按 <kbd>Shift</kbd> + <kbd>Tab</kbd> 所显示的帮助对话框。
```

+++

最后，让这个帮助对话框一直开着会很有用，尤其是在你刚开始学习编程和数据科学的时候。要做到这一点，可以点击顶部菜单栏中的 `Help`，然后选择 `Show Contextual Help`。

## 习题

本章内容的练习题可以在配套的[练习册仓库](https://worksheets.python.datasciencebook.ca)中“Python and Pandas”那一行找到。点击“查看练习册”（view worksheet）即可预览本章练习册的非交互版本。如果想以交互方式做这些习题，请按练习册仓库中的说明下载所有练习册，并按照 {numref}`第 %s 章 <move-to-your-own-machine>` 中给出的计算机配置说明操作。这样才能保证练习册提供的自动反馈和指导按预期工作。



+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```

