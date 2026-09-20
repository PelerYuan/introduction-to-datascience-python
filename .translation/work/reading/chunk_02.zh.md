## 从 Microsoft Excel 文件中读取表格型数据

```{index} Excel 电子表格
```

```{index} see: Microsoft Excel; Excel 电子表格
```

```{index} see: xlsx; Excel 电子表格
```

除了纯文本文件，存储表格型数据集还有很多其他方式；同样，把这些数据集读入 Python 也有很多办法。例如，以 Microsoft Excel 电子表格形式存储的数据（文件扩展名为 `.xlsx`）十分常见，你也经常需要把它们读入 Python。要做到这一点，有一个关键之处需要了解：把 `.csv` 文件和 `.xlsx` 文件加载到 Excel 中时，两者看起来几乎一模一样，但数据本身的存储方式完全不同。`.csv` 文件是纯文本文件，在文本编辑器中打开文件时看到的字符就是它们所表示的数据；`.xlsx` 文件则不是这样。下面这段内容展示了 `.xlsx` 文件在文本编辑器里大致是什么样子：

+++

```text
,?'O
    _rels/.rels???J1??>E?{7?
<?V????w8?'J???'QrJ???Tf?d??d?o?wZ'???@>?4'?|??hlIo??F
t                                                       8f??3wn
????t??u"/
          %~Ed2??<?w??
                       ?Pd(??J-?E???7?'t(?-GZ?????y???c~N?g[^_r?4
                                                                  yG?O
                                                                      ?K??G?


     ]TUEe??O??c[???????6q??s??d?m???\???H?^????3} ?rZY? ?:L60?^?????XTP+?|?
X?a??4VT?,D?Jq
```

```{index} 读取函数; read_excel
```

```{index} Excel 电子表格; 读取
```


这种文件表示方式让 Excel 文件能够存储 `.csv` 文件里无法存储的额外内容，比如字体、文本格式、图形、多个工作表等等。尽管 Excel 电子表格在纯文本编辑器里看起来很奇怪，我们仍然可以用 `pandas` 包中专门为此开发的 `read_excel` 函数把它读入 Python。

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_excel("data/can_lang.xlsx")
canlang_data
```

如果 `.xlsx` 文件包含多个工作表，你必须用 `sheet_name` 参数指明工作表的编号或名称。一个工作表里放着多张表格时，这个功能就很有用（很多 Excel 电子表格都是这种令人遗憾的情况，因为这让读取数据变得更麻烦）。你还可以用 `usecols` 参数指定单元格区域，比如 `usecols="A:D"` 表示包含从 `A` 到 `D` 的列。

和纯文本文件一样，把数据文件导入 Python 之前，你应该先查看一下它。事先查看数据有助于判断需要哪些参数才能顺利把数据读入 Python。如果你的电脑上没有 Excel 程序，也可以用其他程序预览文件，比如 Google Sheets 和 Libre Office。

在 {numref}`read_func` 中，我们汇总了本章讲过的 `read_csv` 和 `read_excel` 函数，也列出了用分号 `;` 分隔的数据所需的参数。有些数据集用逗号而不是小数点表示小数（比如一些来自欧洲国家的数据集），你可能会遇到这类数据。


```{list-table} read_csv 与 read_excel 小结
:header-rows: 1
:name: read_func

* - 数据文件类型
  - Python 函数
  - 参数
* - 逗号（`,`）分隔的文件
  - `read_csv`
  - 只需给出文件路径
* - 制表符（`\t`）分隔的文件
  - `read_csv`
  - `sep="\t"`
* - 缺少表头
  - `read_csv`
  - `header=None`
* - 欧式数字，用分号（`;`）分隔
  - `read_csv`
  - `sep=";"`, `thousands="."`, `decimal=","`
* - Excel 文件（`.xlsx`）
  - `read_excel`
  - `sheet_name`, `usecols`


```

## 从数据库读取数据

```{index} 数据库
```

另一种很常见的数据存储形式是关系数据库。数据量很大，或者有多个用户一起做同一个项目时，数据库就很有用。关系数据库管理系统有很多，比如 SQLite、MySQL、PostgreSQL、Oracle 等等。这些不同的关系数据库管理系统各有各的优点和局限。它们几乎都用 SQL（*结构化查询语言*，structured query language）从数据库中取数据。不过，要分析数据库中的数据并不需要懂 SQL：已经有人写好了一些包，让你可以连接关系数据库，并用 Python 语言取数据。本书会举例说明如何用 Python 配合 SQLite 和 PostgreSQL 数据库来做这件事。

### 从 SQLite 数据库读取数据

```{index} 数据库; SQLite
```

SQLite 大概是最简单的关系数据库系统，也最容易和 Python 搭配使用。SQLite 数据库是自包含的，通常以 `.db` 扩展名（有时是 `.sqlite` 扩展名）的文件形式存放在某台计算机上，并从本地访问。和 Excel 文件一样，它们不是纯文本文件，无法在纯文本编辑器中读取。

```{index} 数据库; 连接, ibis; connect
```

```{index} see: ibis; 数据库
```

```{index} see: 数据库; ibis
```

要从数据库把数据读入 Python，第一步是连接数据库。对 SQLite 数据库，我们使用 `ibis` 包中 `sqlite` 后端的 `connect` 函数来建立连接。这条命令并不读取数据，只是告诉 Python 数据库在哪里，并打开一条通信通道，让 Python 可以向数据库发送 SQL 命令。

```{note}
Python 中还有一个数据库包叫 `sqlalchemy`。它比 `ibis` 更成熟一些，如果你想更深入地研究如何用 Python 操作数据库，它是很值得接着学习的包。本书使用 `ibis`，因为它提供的语法更现代、更友好，写数据分析代码时更像 `pandas`。
```

```{code-cell} ipython3
import ibis

conn = ibis.sqlite.connect("data/can_lang.db")
```

```{index} 数据库; 表, ibis; list_tables, ibis; sqlite
```

关系数据库往往有很多张表，因此要从数据库中取数据，你需要知道数据存在哪张表里。用 `list_tables` 函数可以获取数据库中所有表的名称：

```{code-cell} ipython3
tables = conn.list_tables()
tables
```

```{index} 表, ibis; table
```

`list_tables` 函数只返回了一个名称——`"can_lang"`——这说明该数据库中只有一张表。要引用数据库中的某张表（这样才能做选取列、筛选行之类的操作），我们使用 `conn` 对象的 `table` 函数。借助 `table` 函数返回的对象，我们可以像操作普通的 `pandas` 数据框那样操作数据库中的数据；不过在后台，`ibis` 会悄悄把你的命令转换成 SQL 查询！

```{code-cell} ipython3
canlang_table = conn.table("can_lang")
canlang_table
```

```{index} ibis; count
```

```{index} see: count; ibis
```

虽然看起来我们好像从数据库里取回了整个数据框，其实并没有！它只是一个*引用*，数据仍然只存在 SQLite 数据库里。`canlang_table` 对象是一个 `DatabaseTable`，打印出来时会告诉你表中有哪些列。但它和常见的 `pandas` 数据框不同，我们无法立刻知道表里有多少行。要知道行数，必须向数据库发送一条 SQL *查询*（也就是命令）。在 `ibis` 中，可以用表对象的 `count` 函数来发送。

```{code-cell} ipython3
canlang_table.count()
```

```{index} ibis; execute
```

等一下……这可不是数据库里的行数。其实，我们还没有真正把 SQL 查询发给数据库！我们需要明确告诉 `ibis` 什么时候发送查询。原因在于，处理大型数据集（也就是选取、筛选、连接等操作）时，数据库往往比 Python 更高效。而且数据库通常根本不在你的电脑上，而是在网络上某台更强大的机器上。所以 `ibis` 很懒，你不明确用 `execute` 函数告诉它，它就不会把数据取进内存。`execute` 函数才真正把 SQL 查询发给数据库，并把结果交给你。下面我们执行 `count` 命令，看看表中有多少行。

```{code-cell} ipython3
canlang_table.count().execute()
```
这就对了！`can_lang` 表中有 214 行。如果你想看看 `ibis` 发给数据库的 SQL 查询*实际*的文本，可以用 `compile` 函数代替 `execute`。但要注意，你得先把 `compile` 的结果传给 `str` 函数，把它变成人类可读的字符串。

```{index} see: compile;ibis
```
```{index} ibis; compile, str
```

```{code-cell} ipython3
str(canlang_table.count().compile())
```

上面的输出显示了发送给数据库的 SQL 代码。我们在 Python 中写 `canlang_table.count().execute()` 时，`execute` 函数会在后台把 Python 代码翻译成 SQL，把 SQL 发给数据库，再把返回结果翻译回来。所以 Python 与 SQL 之间来回翻译这些麻烦事全都由 `ibis` 包办了，我们只管用 Python 就好！

`ibis` 包提供了很多类似 `pandas` 的工具来处理数据库表。例如，我们可以用 `head` 函数查看表的前几行，再接上 `execute` 取回结果。

```{index} ibis; head
```

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_table.head(10).execute()
```

可以看到，执行查询之后 `ibis` 实际上返回给我们的是一个 `pandas` 数据框，这样从数据库取回数据之后再处理就很方便。现在我们手里有了 2016 年加拿大人口普查数据的 `canlang_table` 表引用，接下来基本可以把它当普通数据框用了。例如，我们做一遍 {numref}`第 %s 章 <intro>` 里同样的练习：只取出与原住民语言对应的那些行，并且只保留 `language` 和 `mother_tongue` 两列。用 `[]` 操作配合逻辑表达式可以只取特定的行。下面我们筛选出只包含原住民语言的数据。

```{index} 数据库; 筛选行, ibis; []
```

```{code-cell} ipython3
canlang_table_filtered = canlang_table[canlang_table["category"] == "Aboriginal languages"]
canlang_table_filtered
```
从上面的输出可以看到，这条命令还没有真正执行；`canlang_table_filtered` 只是显示了查询的第一部分（也就是上面以 `Selection[r0]` 开头的那部分）。我们没有调用 `execute`，因为还不想把数据取回 Python。我们仍然可以让数据库先做些工作，只取回我们真正要在本地 Python 中处理的那一小部分数据。下面加上 SQL 查询的第二部分：只选取 `language` 和 `mother_tongue` 两列。

```{index} 数据库; 选取列
```

```{code-cell} ipython3
canlang_table_selected = canlang_table_filtered[["language", "mother_tongue"]]
canlang_table_selected
```
现在可以看到，`ibis` 查询分两步：先找出与原住民语言对应的行，再只提取我们关心的 `language` 和 `mother_tongue` 两列。下面真正执行这条查询，把数据以 `pandas` 数据框的形式取回 Python，并打印结果。
```{code-cell} ipython3
aboriginal_lang_data = canlang_table_selected.execute()
aboriginal_lang_data
```

除了 `[]` 操作，`ibis` 还提供了很多函数，让你在调用 `execute` 把数据取回 Python 之前，先在数据库内部处理数据。不过分析所需的函数 `ibis` 并没有*全部*提供，最终我们还是得调用 `execute`。例如，`ibis` 没有提供查看数据库最后几行的 `tail` 函数，而 `pandas` 有。

```{index} DataFrame; tail
```

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_table_selected.tail(6)
```

```{code-cell} ipython3
aboriginal_lang_data.tail(6)
```

所以，对数据库引用对象做完数据整理之后，最好用 `execute` 函数把它以 `pandas` 数据框的形式取回 Python。但用 `execute` 时要格外小心：数据库往往*非常*大，把整张表读进 Python 可能要运行很久，甚至可能让你的机器崩溃。所以在用 `execute` 把数据读入 Python 之前，一定要先选取和筛选数据库表，把数据缩减到合理的规模！

### 从 PostgreSQL 数据库读取数据

```{index} 数据库; PostgreSQL
```

PostgreSQL（也叫 Postgres）是一种很受欢迎的开源关系数据库软件。与 SQLite 不同，PostgreSQL 采用客户端–服务器（client–server）数据库引擎，因为它最初就是为在网络上使用和访问而设计的。这意味着连接 Postgres 数据库时，你必须向 Python 提供更多信息。调用 `connect` 函数时需要补充的信息如下：

- `database`：数据库的名称（一个 PostgreSQL 实例可以承载多个数据库）
- `host`：指向数据库所在位置的 URL（如果数据库在你本机，就是 `localhost`）
- `port`：Python 与 PostgreSQL 数据库之间的通信端点（通常是 `5432`）
- `user`：访问数据库的用户名
- `password`：访问数据库的密码

下面演示如何连接 `can_mov_db` 数据库的一个版本，其中存放着加拿大电影的信息。请注意，下面这些 `host`（`fakeserver.stat.ubc.ca`）、`user`（`user0001`）和 `password`（`abc123`）都*不是真的*，用这些信息实际上连不上数据库。

```{index} ibis; postgres, ibis; connect
```

```{code-cell} ipython3
:tags: ["remove-output"]
conn = ibis.postgres.connect(
    database="can_mov_db",
    host="fakeserver.stat.ubc.ca",
    port=5432,
    user="user0001",
    password="abc123"
)
```

除了需要补充这些信息，`ibis` 让连接和使用 Postgres 数据库与连接和使用 SQLite 数据库完全一样。例如，我们仍然可以用 `list_tables` 查看 `can_mov_db` 数据库里有哪些表：

```{index} ibis; list_tables
```

```{code-cell} ipython3
:tags: ["remove-output"]
conn.list_tables()
```

```{code-cell} ipython3
:tags: ["remove-input"]
print('["themes", "medium", "titles", "title_aliases", "forms", "episodes", "names", "names_occupations", "occupation", "ratings"]')
```

可以看到，这个数据库里有 10 张表。我们先看看 `"ratings"` 表，找出 `can_mov_db` 数据库中最低的评分。

```{index} ibis; table
```

```{code-cell} ipython3
:tags: ["remove-output"]
ratings_table = conn.table("ratings")
ratings_table
```

```{code-cell} ipython3
:tags: ["remove-input"]
print("""
AlchemyTable: ratings
  title           string
  average_rating  float64
  num_votes       int64
""")
```

```{index} ibis; []
```

要找出数据库中最低的评分，我们首先需要选取 `average_rating` 列：

```{code-cell} ipython3
:tags: ["remove-output"]
avg_rating = ratings_table[["average_rating"]]
avg_rating
```

```{code-cell} ipython3
:tags: ["remove-input"]
print("""
r0 := AlchemyTable: ratings
  title           string
  average_rating  float64
  num_votes       int64

Selection[r0]
  selections:
    average_rating: r0.average_rating
""")
```

```{index} 数据库; 排序, ibis; order_by, ibis; head
```

接下来我们用 `ibis` 的 `order_by` 函数按 `average_rating` 给表排序，再用 `head` 函数取第一行（也就是最低的评分）。

```{code-cell} ipython3
:tags: ["remove-output"]
lowest = avg_rating.order_by("average_rating").head(1)
lowest.execute()
```

```{code-cell} ipython3
:tags: ["remove-input"]
lowest = pd.DataFrame({"average_rating" : [1.0]})
lowest
```

可以看到，电影获得的最低评分是 1，这说明那一定是一部相当糟糕的电影……

### 为什么还要费劲用数据库？

```{index} 数据库; 使用理由
```

打开数据库可比打开 `.csv` 文件或者其他纯文本、Excel 格式麻烦多了。我们得先建立与数据库的连接，再用 `ibis` 把类似 `pandas` 的命令（`[]` 操作、`head` 等）翻译成数据库能看懂的 SQL 查询，最后还要 `execute` 执行。而且目前并不是所有 `pandas` 命令都能通过 `ibis` 翻译成数据库查询。所以你可能会想：那我们为什么还要用数据库呢？

在大规模场景下，数据库有其优势：

- 它们可以把大型数据集分散存储在多台计算机上，并配有备份。
- 它们提供了保证数据完整性和校验输入的机制。
- 它们提供安全性和数据访问控制。
- 它们允许多个用户同时、远程访问数据，而不会产生冲突和错误。
  例如，2021 年每天有数十亿次 Google 搜索 {cite:p}`googlesearches`。
  你能想象 Google 把这些搜索的全部数据都存在一个 `.csv` 文件里吗！？那可就乱套了！
<<TERM>>
sheet (Excel) = 工作表
relational database management system = 关系数据库管理系统
<<END>>
