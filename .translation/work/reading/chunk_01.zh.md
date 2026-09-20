
(reading)=
# 从本地和网络读取数据


## 概述

```{index} see: 加载; 读取
```

```{index} 读取; 定义
```

本章将教你如何从本地设备（例如你自己的笔记本电脑）和网络，把各种格式的表格型数据（tabular data）读入 Python。“读取”（或称“加载”）指的是把数据（以纯文本、数据库、HTML 等形式存储）转换成 Python 能方便访问和操作的对象，例如数据框（data frame）。因此，读取数据是通往任何数据分析的门户：不先把数据加载进来，你就无法分析数据。又因为存储数据的方式很多，把数据读入 Python 的方式也同样很多。你越是提前把读取方法与手头数据的类型匹配好，之后需要花在重新格式化、清洗和整理数据上的时间就越少（这是所有数据分析的第二步）。这就好比跑步前先把鞋带系紧，免得跑到半路被绊倒！

## 本章学习目标
学完本章后，你将能够：

- 定义路径的类型，并用它们定位文件：
    - 绝对文件路径
    - 相对文件路径
    - 统一资源定位符（Uniform Resource Locator，URL）
- 用下列函数从不同类型的路径把数据读入 Python：
    - `read_csv`
    - `read_excel`
- 比较 `read_csv` 与 `read_excel` 的异同。
- 说明在什么情形下使用下列 `read_csv` 函数参数：
    - `skiprows`
    - `sep`
    - `header`
    - `names`
- 针对给定的纯文本表格型数据集，选择合适的 `read_csv` 函数参数把它读入 Python。
- 用 `rename` 函数给数据框的列重命名。
- 用 `pandas` 包的 `read_excel` 函数及其参数，把 Excel 文件中的工作表读入 Python。
- 用 `ibis` 包中的函数操作数据库：
    - 用 `connect` 连接数据库。
    - 用 `list_tables` 列出数据库中的表。
    - 用 `table` 创建对数据库表的引用。
    - 用 `execute` 把数据库中的数据取回 Python。
- 用 `to_csv` 把数据框保存为 `.csv` 文件。
- （*可选*）用网页抓取和应用程序编程接口（application programming interface，API）从网络获取数据：
    - 用 `BeautifulSoup` 包从 URL 读取 HTML 源代码。
    - 用 `requests` 包读取 NASA 的 “Astronomy Picture of the Day” 数据。
    - 比较以下三种做法：从纯文本文件（例如 `.csv`）下载表格型数据、从 API 访问数据，以及抓取网站的 HTML 源代码。

## 绝对路径与相对路径

```{index} see: 位置; 路径
```

```{index} 路径; 本地, 路径; 远程, 路径; 相对, 路径; 绝对
```

本章会讨论把数据导入 Python 的各种函数。不过，在讲这些函数*如何*把数据读入 Python 之前，我们先要说清数据*存在哪里*。把数据集载入 Python 时，你首先需要告诉 Python 这些文件在哪里。文件可能存放在你的电脑上（*本地*），也可能存放在互联网上的某个地方（*远程*）。

文件在电脑上的存放位置称为它的“路径”。你可以把路径理解为通往该文件的路线。路径分两种：*相对*路径和*绝对*路径。相对路径（relative path）说明文件相对于电脑上*工作目录*（也就是“你当前所在的位置”）的位置。绝对路径（absolute path）说明的则是文件相对于计算机文件系统根部（即*根*文件夹）的位置，与你在哪里工作无关。

假设我们电脑的文件系统如 {numref}`Filesystem` 所示。我们正在编辑的文件是 `project3.ipynb`，当前工作目录是 `project3`；通常情况下（本例正是如此），工作目录就是存放你当前正在处理的文件的目录。

```{figure} img/reading/filesystem.png
---
name: Filesystem
---
文件系统示例
```

假设我们要打开 `happiness_report.csv` 文件。要指明文件的位置，有两种选择：用相对路径，或者用绝对路径。文件的绝对路径总以斜杠 `/` 开头——它代表计算机上的根文件夹——然后依次列出到达该文件所须逐层进入的文件夹，每层之间再用一个斜杠 `/` 隔开。因此在本例中，要到达 `happiness_report.csv`，得从根文件夹出发，先进入 `home` 文件夹，再进入 `dsci-100` 文件夹，然后是 `project3` 文件夹，最后进入 `data` 文件夹。所以它的绝对路径是 `/home/dsci-100/project3/data/happiness_report.csv`。我们可以把绝对路径当作字符串传给 `pandas` 的 `read_csv` 函数，用它加载这个文件。
```{code-cell} ipython3
:tags: ["remove-output"]
happy_data = pd.read_csv("/home/dsci-100/project3/data/happiness_report.csv")
```
如果改用相对路径，就需要依次列出从当前工作目录走到该文件所需的每一步，各步之间用斜杠 `/` 隔开。由于我们当前就在 `project3` 文件夹里，只需再进入 `data` 文件夹就能到达目标文件。因此相对路径是 `data/happiness_report.csv`，把它当作字符串传给 `read_csv` 即可加载文件。
```{code-cell} ipython3
:tags: ["remove-output"]
happy_data = pd.read_csv("data/happiness_report.csv")
```
请注意，相对路径的开头没有正斜杠；如果不小心写成 `"/data/happiness_report.csv"`，Python 就会去计算机的根文件夹里找名为 `data` 的文件夹——可它并不存在！

```{index} 路径; 上一级, 路径; 当前
```

```{index} see: ..; 路径
```

```{index} see: .; 路径
```

除了用文件夹名（如 `data` 和 `project3`）在路径中指明要走到哪里，我们还可以指明两个特殊位置：*当前目录*和*上一级目录*。当前工作目录用单个点 `.` 表示，上一级目录用两个点 `..` 表示。举例来说，如果要从 `project3` 文件夹到达 `bike_share.csv` 文件，可以用相对路径 `../project2/bike_share.csv`。这两个符号还能组合使用；例如下面这条（相当傻的）路径也能到达 `bike_share.csv`：`../project2/../project2/./bike_share.csv`，它绕了不少冤枉路——先退回上一层文件夹，再打开 `project2`，然后又退回上一层，再打开 `project2`，接着留在当前目录，最后才到达 `bike_share.csv`。呼，好长的一段路！

那么该用哪种路径：相对路径，还是绝对路径？一般来说，应该用相对路径。用相对路径有助于保证你的代码能在另一台电脑上运行（附带的好处是，相对路径往往更短——敲起来更省事！）。这是因为同一个文件的相对路径在不同电脑上往往相同，而文件的绝对路径（即计算机根目录——用 `/` 表示——与该文件之间所有文件夹的名称）在不同电脑上通常并不相同。例如，假设 Fatima 和 Jayden 在合作一个项目，用的数据是 `happiness_report.csv`。Fatima 的文件存放在

```text
/home/Fatima/project3/data/happiness_report.csv
```

而 Jayden 的文件存放在

```text
/home/Jayden/project3/data/happiness_report.csv
```

尽管 Fatima 和 Jayden 把文件存放在各自电脑上的相同位置（都在自己的主文件夹里），但由于用户名不同，绝对路径并不一样。如果 Jayden 有一段用绝对路径加载 `happiness_report.csv` 数据的代码，这段代码在 Fatima 的电脑上就跑不通。但从 `project3` 文件夹内部看，相对路径（`data/happiness_report.csv`）在两台电脑上完全相同；凡是用相对路径的代码，两台电脑上都能运行！在拓展资源一节中，我们附上了一个短视频的链接，讲的是绝对路径与相对路径的区别。

```{index} URL
```

除了存放在你电脑上的文件（即*本地*文件），我们还需要一种办法来定位存放在互联网别处的资源（即*远程*资源）。为此我们使用*统一资源定位符（URL）*，也就是形如 https://python.datasciencebook.ca/ 的网址。URL 指明资源在互联网上的位置：它以网络域名开头，接着是一个正斜杠 `/`，然后是指向该资源在远程机器上所在位置的路径。

## 从纯文本文件把表格型数据读入 Python

(readcsv)=
### 用 `read_csv` 读取逗号分隔值文件

```{index} csv, 读取; 分隔符, 读取函数; read_csv
```

我们已经了解了数据可能*在哪里*，接下来学习*如何*用各种函数把数据导入 Python。具体来说，我们要学会把纯文本文件（只含文本的文档）中的表格型数据*读入* Python，以及把表格型数据*写出*到文件中。用哪个函数取决于文件的格式。例如上一章我们学过，读取 `.csv`（**c**omma-**s**eparated **v**alues，逗号分隔值）文件时要使用 `pandas` 的 `read_csv` 函数。那时，分隔各列的*分隔符*（separator）是逗号（`,`）。我们当时只学了数据符合 `read_csv` 函数默认预期的情况（文件含列名，且以逗号作为列间分隔符）。本节要学习如何读取那些不满足 `read_csv` 默认预期的文件。

```{index} 加拿大语言; canlang 数据
```

在进入数据不符合 `pandas` 与 `read_csv` 默认格式的那些情形之前，我们先回顾一个更简单的情形：默认预期成立，我们只需给函数一个参数，也就是文件的路径 `data/can_lang.csv`。`can_lang` 数据集包含 2016 年加拿大人口普查的语言数据。加载这份数据集时，我们在文件名前加上 `data/`，因为相对于运行 Python 代码的位置，该数据集位于名为 `data` 的子文件夹中。文件 `data/can_lang.csv` 的内容如下。

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

```{index} pandas
```

下面回顾一下怎样用 `read_csv` 把它加载到 Python 中。首先加载 `pandas` 包，以便使用其中读取数据的实用函数。

```{code-cell} ipython3
import pandas as pd
```

接着用 `read_csv` 把数据加载到 Python 中，并在调用时指定文件的相对路径。

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv("data/can_lang.csv")
canlang_data
```

### 读取数据时跳过若干行

数据文件的顶部常常会带有关于数据收集方式的信息，或者其他一些信息。这类信息通常以句子和段落的形式书写，各字段之间没有分隔符，因为它并没有按列组织。下面是一个例子。这些信息为数据科学家提供了理解数据的背景和线索，但它的格式并不规整，也不应该和文件后面那些表格型数据一起读入数据框的单元格中。

```text
Data source: https://ttimbers.github.io/canlang/
Data originally published in: Statistics Canada Census of Population 2016.
Reproduced and distributed on an as-is basis with their permission.
category,language,mother_tongue,most_at_home,most_at_work,lang_known
Aboriginal languages,"Aboriginal languages, n.o.s.",590,235,30,665
Non-Official & Non-Aboriginal languages,Afrikaans,10260,4785,85,23415
Non-Official & Non-Aboriginal languages,"Afro-Asiatic languages, n.i.e.",1150,445,10,2775
Non-Official & Non-Aboriginal languages,Akan (Twi),13460,5985,25,22150
Non-Official & Non-Aboriginal languages,Albanian,26895,13135,345,31930
Aboriginal languages,"Algonquian languages, n.i.e.",45,10,0,120
Aboriginal languages,Algonquin,1260,370,40,2480
Non-Official & Non-Aboriginal languages,American Sign Language,2685,3020,1145,21930
Non-Official & Non-Aboriginal languages,Amharic,22465,12785,200,33670
```

文件顶部多了这些信息之后，像刚才那样使用 `read_csv` 就无法把数据正确加载到 Python 中。对这个文件来说，Python 只会打印一条 `ParserError` 报错信息，表示它读不了这个文件。

```{code-cell} ipython3
:tags: ["remove-output"]
canlang_data = pd.read_csv("data/can_lang_meta-data.csv")
```
```{code-cell} ipython3
:tags: ["remove-input"]
print("ParserError: Error tokenizing data. C error: Expected 1 fields in line 4, saw 6")
```

```{index} ParserError
```

```{index} 读取函数; skiprows 参数
```

要顺利地把这类数据读入 Python，可以用 `skiprows` 参数告诉 Python 在开始读取数据之前先跳过多少行。在上面的例子里，把它设为 3 就能正确读取并加载数据。

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv("data/can_lang_meta-data.csv", skiprows=3)
canlang_data
```

我们怎么知道要跳过三行？看看数据就知道了！数据的前三行是我们不需要导入的信息：

```text
Data source: https://ttimbers.github.io/canlang/
Data originally published in: Statistics Canada Census of Population 2016.
Reproduced and distributed on an as-is basis with their permission.
```

列名从第 4 行开始，所以我们跳过了前三行。

### 用 `sep` 参数处理不同的分隔符

另一种常见的数据存储方式是用制表符作分隔符。可以看到，数据文件 `can_lang.tsv` 的列与列之间用的是制表符，而不是逗号。

```text
category	language	mother_tongue	most_at_home	most_at_work	lang_known
Aboriginal languages	Aboriginal languages, n.o.s.	590	235	30	665
Non-Official & Non-Aboriginal languages	Afrikaans	10260	4785	85	23415
Non-Official & Non-Aboriginal languages	Afro-Asiatic languages, n.i.e.	1150	445	10	2775
Non-Official & Non-Aboriginal languages	Akan (Twi)	13460	5985	25	22150
Non-Official & Non-Aboriginal languages	Albanian	26895	13135	345	31930
Aboriginal languages	Algonquian languages, n.i.e.	45	10	0	120
Aboriginal languages	Algonquin	1260	370	40	2480
Non-Official & Non-Aboriginal languages	American Sign Language	2685	3020	1145	21930
Non-Official & Non-Aboriginal languages	Amharic	22465	12785	200	33670
```
```{index} 读取函数; sep 参数
```

```{index} see: 制表符分隔值; tsv
```

```{index} tsv
```

要读取 `.tsv`（**t**ab **s**eparated **v**alues，制表符分隔值）文件，可以把 `read_csv` 函数的 `sep` 参数设为*制表符*（tab character） `\t`。

```{index} 转义字符
```

```{note}
`\t` 是一个*转义字符*（escaped character），它总以反斜杠（`\`）开头。
转义字符用来表示不可打印的字符（如制表符），
或者具有特殊含义的字符（如引号）。
```


```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv("data/can_lang.tsv", sep="\t")
canlang_data
```

把这里的数据框与我们在 {numref}`readcsv` 中用 `read_csv` 得到的数据框比较一下，你会发现它们看起来完全一样：列数和行数相同，列名相同，每个单元格的取值也相同！所以，尽管文件格式不同、需要用到的参数也不同，两种做法得到的数据框（`canlang_data`）是一样的。

### 用 `header` 参数处理缺少列名的情况

```{index} 读取函数; header 参数, 读取; 分隔符
```

`can_lang_no_names.tsv` 文件是这份数据集的另一个版本，略有不同：它没有列名，并用制表符作分隔符。在文本编辑器中，该文件的内容如下：

```text
Aboriginal languages	Aboriginal languages, n.o.s.	590	235	30	665
Non-Official & Non-Aboriginal languages	Afrikaans	10260	4785	85	23415
Non-Official & Non-Aboriginal languages	Afro-Asiatic languages, n.i.e.	1150	445	10	2775
Non-Official & Non-Aboriginal languages	Akan (Twi)	13460	5985	25	22150
Non-Official & Non-Aboriginal languages	Albanian	26895	13135	345	31930
Aboriginal languages	Algonquian languages, n.i.e.	45	10	0	120
Aboriginal languages	Algonquin	1260	370	40	2480
Non-Official & Non-Aboriginal languages	American Sign Language	2685	3020	1145	21930
Non-Official & Non-Aboriginal languages	Amharic	22465	12785	200	33670

```

Python 中的数据框必须有列名。因此，如果读入的数据没有列名，Python 会自动指派名称。在这个例子里，Python 指派的列名是 `0, 1, 2, 3, 4, 5`。要把这份数据读入 Python，我们把第一个参数指定为文件的路径（与 `read_csv` 的用法一致），再给 `sep` 参数赋值（这里是制表符，写作 `"\t"`），最后设置 `header = None`，告诉 `pandas` 这个数据文件本身不含列名。

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv(
    "data/can_lang_no_names.tsv",
    sep="\t",
    header=None
)
canlang_data
```

```{index} DataFrame; rename, pandas
```

这种情况下，最好还是手动给各列重命名。现在的列名（`0, 1` 等）有两个问题：一是这些名字说明不了什么，会让你的分析难以理解；二是列名一般应该是*字符串*，而它们现在是*整数*。要给列重命名，可以使用 [pandas 包](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html#) 中的 `rename` 函数。`rename` 函数的参数是 `columns`，它接收旧列名与新列名之间的映射。这里我们想把 `canlang_data` 数据框中的旧列名（`0, 1, ..., 5`）改成更能说明含义的名字。

要指定映射关系，我们创建一个*字典*（dictionary）：它是 Python 的一种对象，表示从*键*（key）到*取值*（value）的映射。创建字典时用一对花括号 `{ }`，括号内放入若干 `key : value` 对，彼此用逗号分隔。下面我们创建一个名为 `col_map` 的字典，把 `canlang_data` 中的旧列名映射到新列名，然后把它传给 `rename` 函数。

```{code-cell} ipython3
:tags: ["output_scroll"]
col_map = {
    0 : "category",
    1 : "language",
    2 : "mother_tongue",
    3 : "most_at_home",
    4 : "most_at_work",
    5 : "lang_known"
}
canlang_data_renamed = canlang_data.rename(columns=col_map)
canlang_data_renamed
```

```{index} 读取函数; names 参数
```

也可以在读文件时就把列名赋给数据框：向 `read_csv` 的 `names` 参数传入一个列名列表（list）即可。

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv(
    "data/can_lang_no_names.tsv",
    sep="\t",
    header=None,
    names=[
        "category",
        "language",
        "mother_tongue",
        "most_at_home",
        "most_at_work",
        "lang_known",
    ],
)
canlang_data
```

### 直接从 URL 读取表格型数据

```{index} URL; 从 URL 读取
```

我们还可以用 `read_csv` 直接从 URL（**U**niform **R**esource **L**ocator）读取含有表格型数据的内容。这时传给 `read_csv` 的是远程文件的 URL，而不是本机文件的路径。和指定本机路径时一样，URL 也要用引号括起来。除此之外，其他参数与读取本机文件时完全相同。

```{code-cell} ipython3
:tags: ["output_scroll"]
url = "https://raw.githubusercontent.com/UBC-DSCI/introduction-to-datascience-python/reading/source/data/can_lang.csv"
pd.read_csv(url)
canlang_data = pd.read_csv(url)

canlang_data
```

### 读入 Python 之前先预览数据文件

上面不少例子中，我们都在把数据读入 Python 之前先给你看了数据文件的预览。预览数据很重要：它能让你看出有没有列名、分隔符是什么、有没有需要跳过的行。你自己读取数据文件时也应该这样做：先用你喜欢的文本编辑器打开文件，看清内容之后再读入 Python。
