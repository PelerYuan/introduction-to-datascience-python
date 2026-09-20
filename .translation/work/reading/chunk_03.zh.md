## 从 Python 把数据写入 `.csv` 文件

```{index} 写入函数; to_csv, DataFrame; to_csv
```

在数据分析的中途和末尾，我们常常需要把已经改动过的数据框（例如选取了列、筛选了行等之后）写入文件，以便与他人共享，或者留到分析的后续步骤使用。最直接的做法是使用 `pandas` 包中的 `to_csv` 函数。它的默认参数是用逗号（`,`）作为分隔符，并在第一行写出列名。我们还指定 `index = False`，让 `pandas` 不要在 `.csv` 文件中打印行号。下面我们演示如何依据 2016 年加拿大人口普查，生成一份不含 “Official languages” 类别的加拿大语言数据集新版本，再把它写入 `.csv` 文件：

```{code-cell} ipython3
no_official_lang_data = canlang_data[canlang_data["category"] != "Official languages"]
no_official_lang_data.to_csv("data/no_official_languages.csv", index=False)
```

## 从网上获取数据

```{note}
本节不是本书其余部分的必读内容。我们把它保留在这里，是给那些想多了解一点如何从网上获取不同类型数据的人看的。
```

```{index} see: 应用程序编程接口; API
```

```{index} API
```

数据不会凭空出现在你的电脑上，总得从某个地方取得。本章前面已经演示过，如何用 `pandas` 的 `read_csv` 函数从某个 URL 读取以纯文本、类似电子表格的格式（例如用逗号或制表符分隔）存储的数据。但随着时间的推移，能从 URL 直接下载这种格式的数据（尤其是大数据）已经越来越少见。取而代之的是，网站现在常常提供一种称为应用程序编程接口（**a**pplication **p**rogramming **i**nterface，API）的东西，它给出了用程序请求数据集子集的途径。这样，网站所有者就能控制*谁*有权访问数据、他们能访问数据的*哪一部分*，以及他们能访问*多少*数据。通常，网站所有者会给你一个*令牌*或*密钥*（一串类似密码的保密字符），访问 API 时必须提供。

```{index} 网页抓取, CSS, HTML
```

```{index} see: 超文本标记语言; HTML
```

```{index} see: 层叠样式表; CSS
```

还有一个有意思的想法：网站本身*就是*数据！在浏览器窗口里输入一个 URL 后，浏览器会向*网络服务器*（互联网上另一台负责响应网站请求的计算机）索取网站的数据，再把数据转换成你能看到的样子。如果网站显示了你感兴趣的信息，你也可以把那些信息复制粘贴到一个文件里，为自己*创建*一份数据集。这种直接从网页显示的内容中取信息的做法，叫作*网页抓取*（有时也叫*屏幕抓取*）。当然，手动复制粘贴既费力又容易出错，要收集的信息一多更是如此。所以，与其让浏览器把网络服务器提供的信息转换成你能看到的样子，不如用程序去收集这些数据——也就是 **h**yper**t**ext **m**arkup **l**anguage（HTML）和 **c**ascading **s**tyle **s**heet（CSS）代码——再对它们做处理，提取出有用的信息。HTML 提供网站的基本结构，告诉网页如何显示内容（例如标题、段落、项目符号列表等）；CSS 则帮助设计内容的样式，告诉网页应该如何呈现 HTML 元素（例如颜色、布局、字体等）。

本小节将介绍两项基础知识：用 [Python 包 `BeautifulSoup`](https://beautiful-soup-4.readthedocs.io/en/latest/) {cite:p}`beautifulsoup` 做网页抓取，以及用 [Python 包 `requests`](https://requests.readthedocs.io/en/latest/) {cite:p}`requests` 访问 NASA 的 “Astronomy Picture of the Day” API。

+++

### 网页抓取

#### HTML 和 CSS 选择器

```{index} 网页抓取, HTML; 选择器, CSS; 选择器, Craiglist
```

在浏览器里输入一个 URL 时，浏览器会连接到该 URL 上的网络服务器，索要网站的*源代码*。浏览器就是把这些数据转换成你能看到的样子。所以，如果我们打算通过抓取网站来自己造数据，就必须先弄明白这些数据长什么样！举个例子，假设我们想知道 [Craiglist](https://vancouver.craigslist.org) 上温哥华最新挂出的一居室公寓的平均租金（按每平方英尺计）。访问温哥华 Craigslist 网站并搜索一居室公寓时，我们应该会看到与 {numref}`fig:craigslist-human` 类似的内容。

+++

```{figure} img/reading/craigslist_human.png
:name: fig:craigslist-human

Craigslist 上的一居室公寓出租广告网页。
```

+++

从浏览器显示给我们的内容来看，找出每条房源的面积和价格相当容易。但我们希望用 Python 取得这些信息，不需要任何人工操作，也不用复制粘贴。为此，我们要查看网络服务器实际发送给浏览器、供其显示的*源代码*。下面展示其中的一小段；完整的源码[随本书代码一并提供](https://github.com/UBC-DSCI/introduction-to-datascience-python/blob/main/source/data/website_source.txt)：

```html
<span class="result-meta">
        <span class="result-price">$800</span>
        <span class="housing">
            1br -
        </span>
        <span class="result-hood"> (13768 108th Avenue)</span>
        <span class="result-tags">
            <span class="maptag" data-pid="6786042973">map</span>
        </span>
        <span class="banish icon icon-trash" role="button">
            <span class="screen-reader-text">hide this posting</span>
        </span>
    <span class="unbanish icon icon-trash red" role="button"></span>
    <a href="#" class="restore-link">
        <span class="restore-narrow-text">restore</span>
        <span class="restore-wide-text">restore this posting</span>
    </a>
    <span class="result-price">$2285</span>
</span>
```

唉……看得出来，网页的源代码并不是为了让人轻松读懂而设计的。不过，只要仔细看，你就会发现我们感兴趣的信息就藏在这一团杂乱之中。例如，在上面那段代码的靠前位置，你能看到这样一行：

```html
<span class="result-price">$800</span>
```

这一小段代码存放的显然是某套公寓的价格。再多找找，你还能找到房源发布的日期和时间、房源地址等信息。所以，这份源代码很可能包含我们感兴趣的全部信息！

```{index} HTML; 标签
```

我们来仔细看看上面那一行。可以看到，这小段代码有一个*开始标签*（`<` 和 `>` 之间的词，如 `<span>`）和一个*结束标签*（写法相同，只是多一个斜杠，如 `</span>`）。HTML 源代码一般把数据存放在这样一对开始标签与结束标签之间。标签是一些关键字，用来告诉网页浏览器如何显示或排版内容。在上面那段代码里，我们想要的信息（`$800`）就存放在一对开始标签和结束标签（`<span>` 和 `</span>`）之间。在开始标签里，你还能看到一个很有用的 “class”（有时会写在开始标签里的一种特殊词）：`class="result-price"`。既然我们想让 Python 用程序把网站的全部源代码过一遍，找出公寓价格，那么不妨找出所有 class 为 `"result-price"` 的标签，把开始标签与结束标签之间的信息取出来。没错，再看看上面那段代码里的另一行：

```html
<span class="result-price">$2285</span>
```

这是另一套房源的价格，而包住它的标签正是 `"result-price"` 这个 class。太好了！既然已经知道要找的模式——夹在 class 为 `"result-price"` 的开始标签与结束标签之间的一个美元金额——就应该能用代码把源代码中所有匹配这一模式的内容提取出来，得到我们需要的数据。这种“模式”叫作 *CSS 选择器*（CSS 是 **c**ascading **s**tyle **s**heet 的缩写）。

上面只是一个“找出要查找的模式”的简单例子；许多网站要大得多、也复杂得多，它们的源代码同样如此。好在有一些工具能让这个过程更容易一些。例如，[SelectorGadget](https://selectorgadget.com/) 就是一个开源工具，可以简化 CSS 选择器的生成与查找。本章末尾的拓展资源部分给出了一段短视频的链接，讲解如何安装并使用 SelectorGadget 工具，得到可供网页抓取使用的 CSS 选择器。安装并启用该工具后，你可以点击网页上想要获取合适选择器的元素。例如，点击某套房源的价格，就会看到 SelectorGadget 在工具栏中显示出选择器 `.result-price`，并把用这个选择器能取得的所有其他公寓价格都高亮标出（{numref}`fig:sg1`）。

```{figure} img/reading/sg1.png
:name: fig:sg1

在 Craigslist 网页上使用 SelectorGadget，得到可用于获取公寓价格的 CCS 选择器。
```

如果我们接着点击某套房源的面积，SelectorGadget 会显示出 `span` 选择器，并高亮页面上的许多行；这说明 `span` 选择器不够具体，无法只取到公寓面积（{numref}`fig:sg3`）。

```{figure} img/reading/sg3.png
:name: fig:sg3

在 Craigslist 网页上使用 SelectorGadget，得到可用于获取公寓面积的 CCS 选择器。
```

要缩小选择器的范围，我们可以点击某个被高亮、但我们*不*想要的元素。例如，取消选中 “pic/map” 链接，结果就只有我们想要的数据被高亮，此时用的是 `.housing` 选择器（{numref}`fig:sg2`）。

```{figure} img/reading/sg2.png
:name: fig:sg2

在 Craigslist 网页上使用 SelectorGadget，把 CCS 选择器细化为最适合获取公寓面积的那一个。
```

因此，要抓取房源的面积和租金信息，我们需要分别使用 `.housing` 和 `.result-price` 这两个 CSS 选择器。选择器工具会把它们以逗号分隔的列表形式返回给我们（这里是 `.housing , .result-price`）；如果我们要使用不止一个 CSS 选择器，这正是需要提供给 Python 的格式。

**注意：这个网站允许你抓取吗？**

```{index} 网页抓取; 许可
```

+++

从网上抓取数据*之前*，你应该先确认自己*是否有权*抓取！有两份文件很重要：`robots.txt` 文件和服务条款文档。如果我们去看 [Craigslist 的服务条款文档](https://www.craigslist.org/about/terms.of.use)，会找到下面这段文字：*“你同意不使用机器人、蜘蛛程序、脚本、抓取器、爬网程序，也不以任何自动化或人工的等效方式（例如手工操作）复制或收集 CL 内容。”* 所以很遗憾，没有明确许可，我们不允许抓取这个网站。

```{index} Wikipedia
```

那现在该怎么办？我们*可以*向 Craigslist 的所有者申请抓取许可。但我们不太可能收到回复，即使收到了，对方多半也不会同意。更现实的答案是：Craigslist 就是不能抓。如果我们仍然想要温哥华的租金数据，就只能另找来源。为了继续学习如何抓取网上的数据，我们改为抓取维基百科上加拿大城市的人口数据。我们查过[服务条款文档](https://foundation.wikimedia.org/wiki/Terms_of_Use/en)，其中没有提到禁止网页抓取。我们将使用 SelectorGadget 工具选中感兴趣的元素（城市名和人口数），并取消选中其他元素，表示对它们不感兴趣（省份名），如 {numref}`fig:sg4` 所示。

```{figure} img/reading/sg4.png
:name: fig:sg4

在维基百科网页上使用 SelectorGadget。
```

本章末尾的拓展资源部分给出了一个短视频教程的链接，讲解这一过程。SelectorGadget 在工具栏中给出了下面这组可供使用的 CSS 选择器：

```text
td:nth-child(8) ,
td:nth-child(4) ,
.largestCities-cell-background+ td a
```

现在，我们有了描述目标元素特征的 CSS 选择器，就可以用它们在网页中找出特定元素并提取数据。


#### 用 `BeautifulSoup` 抓取

```{index} BeautifulSoup, requests
```

我们将使用 `requests` 和 `BeautifulSoup` 这两个 Python 包，从维基百科页面上抓取数据。加载这两个包之后，我们把要抓取页面的 URL 用引号括起来，交给 `requests.get` 函数，以此告诉 Python 要抓哪个页面。该函数会取得页面的原始 HTML，我们再把它传给 `BeautifulSoup` 函数解析：

```{code-cell} ipython3
:tags: ["remove-output"]
import requests
import bs4

wiki = requests.get("https://en.wikipedia.org/wiki/Canada")
page = bs4.BeautifulSoup(wiki.content, "html.parser")
```

```{code-cell} ipython3
:tags: [remove-cell]
import bs4

# the above cell doesn't actually run; this one does run
# and loads the html data from a local, static file

with open("data/canada_wiki.html", "r") as f:
    wiki_hidden = f.read()
page = bs4.BeautifulSoup(wiki_hidden, "html.parser")
```

`requests.get` 函数会把你指定 URL 上页面的 HTML 源代码下载下来，就像你用浏览器访问该网站时一样。但 `requests.get` 函数不会把网站显示给你，而是直接返回 HTML 源代码本身——存放在 `wiki.content` 变量里——我们再把它交给 `BeautifulSoup` 解析，并存到 `page` 变量中。接下来，我们把从 SelectorGadget 得到的那组 CSS 选择器传给 `page` 对象的 `select` 方法。注意要用引号把选择器括起来，因为 `select` 要求这个参数是字符串。我们把 `select` 函数的结果存到 `population_nodes` 变量里。请注意 `select` 返回的是一个列表；为了清楚起见，下面我们对列表做切片，只打印前 5 个元素。

```{code-cell} ipython3
population_nodes = page.select(
    "td:nth-child(8) , td:nth-child(4) , .largestCities-cell-background+ td a"
)
population_nodes[:5]
```

`population_nodes` 列表中的每一项，都是 HTML 文档中匹配你所指定 CSS 选择器的一个*节点*。*节点*就是一对 HTML 标签（例如定义表格单元格的 `<td>` 和 `</td>`），再加上存放在这对标签之间的内容。对于 CSS 选择器 `td:nth-child(4)`，一个会被选中的示例节点是：

```html
<td style="text-align:left;">
<a href="/wiki/London,_Ontario" title="London, Ontario">London</a>
</td>
```

接下来，我们用 `get_text` 函数从节点中提取有意义的数据——也就是说，去掉 HTML 的代码语法和标签。对于上面那个示例节点，`get_text` 函数返回 `"London"`。这里同样为了清楚起见，只展示前 5 个元素。

```{code-cell} ipython3
[row.get_text() for row in population_nodes[:5]]
```

太好了！看来我们已经从原始 HTML 源代码中提取出了感兴趣的数据。但事情还没完：这些数据的格式还不适合直接做数据分析。城市名和人口都被编码成字符，放在同一个向量里，而不是放在一个数据框中——城市占一个字符串列、人口占一个数值列（就像电子表格那样）。此外，人口数字中带有逗号（不利于用程序处理数字），有些末尾还有换行符（`\n`）。在 {numref}`第 %s 章 <wrangling>` 中，我们将进一步学习如何用 Python 把这类数据*整理*成更适合数据分析的格式。

+++

#### 用 `read_html` 抓取

用 `requests` 和 `BeautifulSoup` 按 CSS 选择器提取数据，是一种非常通用的网页抓取方式，只是可能稍微复杂一点。好在 `pandas` 提供了 [`read_html`](https://pandas.pydata.org/docs/reference/api/pandas.read_html.html) 函数；如果网页上的数据本来就是表格形式，用这个函数会更省事。`read_html` 函数只接受一个参数——要抓取页面的 URL——并返回一个数据框列表，对应它在那个 URL 上找到的所有表格。从下面可以看到，`read_html` 在维基百科的加拿大页面上找到了 17 个表格。

```{index} 读取函数; read_html
```

```{code-cell} ipython3
:tags: ["remove-output"]
canada_wiki_tables = pd.read_html("https://en.wikipedia.org/wiki/Canada")
len(canada_wiki_tables)
```

```{code-cell} ipython3
:tags: [remove-input]
canada_wiki_tables = pd.read_html("data/canada_wiki.html")
len(canada_wiki_tables)
```

逐一查看这些表格后，我们发现包含加拿大最大都市区人口数的表格位于索引 1 处。我们用 `droplevel` 方法简化结果数据框的列名：

```{code-cell} ipython3
canada_wiki_df = canada_wiki_tables[1]
canada_wiki_df.columns = canada_wiki_df.columns.droplevel()
canada_wiki_df
```

我们又一次从原始 HTML 源代码中提取出了感兴趣的数据——只不过这一次用的是更方便的 `read_html` 函数，不必显式使用 CSS 选择器！不过同样地，这个结果还需要做一些清洗。回头再看 {numref}`fig:sg4`，可以看到表格用两组列（例如 `Name` 和 `Name.1`）来排版，我们需要设法把它们合并起来。在 {numref}`第 %s 章 <wrangling>` 中，我们将进一步学习如何把数据*整理*成适合数据分析的格式。

### 使用 API

```{index} API
```

如今，许多网站不再把一个数据文件放在 URL 上供你下载，而是提供可以通过 Python 这类编程语言访问的 API。使用 API 的好处是，数据所有者对提供给用户的数据有更大的控制权。不过，和网页抓取不同，各网站访问 API 的方式并不统一：每个网站通常都有一套自己的 API，专为自己的使用场景而设计。因此，本书只给出一个通过 API 访问数据的例子，希望它能让你掌握足够的基础概念，在需要时学会使用别的 API。具体来说，本书将演示如何用 Python 的 `requests` 包访问 NASA 的 “Astronomy Picture of the Day” API 的基础知识（顺便说一句，这也是桌面背景的绝佳来源——不妨看看 2023 年 7 月 13 日那张令人惊叹的蛇夫座 ρ 云复合体照片 {cite:p}`rhoophiuchi`，见 {numref}`fig:NASA-API-Rho-Ophiuchi`！）。

```{index} requests, NASA, API; 令牌
```

```{figure} img/reading/NASA-API-Rho-Ophiuchi.png
:name: fig:NASA-API-Rho-Ophiuchi
:width: 400px

詹姆斯·韦布空间望远镜的 NIRCam 拍摄的蛇夫座 ρ 分子云复合体图像。
```