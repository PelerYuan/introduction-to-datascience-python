+++

首先，你需要访问 [NASA API 页面](https://api.nasa.gov/)，生成一个 API 密钥（API key），也就是访问 API 时用来标识你身份的密码。
请注意，密钥必须关联一个有效的电子邮箱地址。
注册表单大致如 {numref}`fig:NASA-API-signup` 所示。
填完基本信息后，你会通过电子邮件收到令牌。
请把密钥保存在安全的地方，并且不要外泄。


```{figure} img/reading/NASA-API-signup.png
:name: fig:NASA-API-signup

为 NASA API 生成访问令牌。
```

**注意：请慎重考虑你的 API 使用方式！**

访问 API 时，你实际上是在把数据从网络服务器传输到自己的计算机上。运行网络服务器开销很大，而且服务器并没有无限的资源。
如果一次性索取*过多数据*，就可能占掉服务器的大量带宽。
如果索取数据的*频率过高*——比如在很短时间内连续向服务器发出许多请求——同样会把服务器拖垮，使它无法再响应其他用户。
如果你不够谨慎，多数服务器都有机制撤销你的访问权限；但你应该尽量从一开始就避免问题发生，格外小心地编写和运行代码。
还要记住：网站所有者授予你 API 访问权限时，通常还会规定你可以索取多少数据的上限（也就是*配额*）。
注意不要超出配额！所以，在尝试使用 API *之前*，我们先访问 [NASA 网站](https://api.nasa.gov/)，看看使用 API 时应当遵守哪些限制。
这些限制在图 {numref}`fig:NASA-API-limits` 中列出。

```{figure} img/reading/NASA-API-limits.png
:name: fig:NASA-API-limits

NASA 网站规定每小时最多 1,000 次请求。
```

看过 NASA 网站后，看来我们每小时最多可以发送 1,000 次请求。
对本节的目标来说，这应该远远足够了。

+++

#### 访问 NASA API

```{index} API; HTTP, API; 查询参数, API; 端点
```

NASA API 属于所谓的 *HTTP API*：这类 API 十分常见，你只要像访问普通网站那样访问某个特定的 URL，就能取得数据。
向 NASA API 发出查询时，我们需要指定三样东西。
第一，指定 API 的 URL *端点*（endpoint），它就是一个 URL，用来让远程服务器知道你打算访问哪个 API。
NASA 提供多种 API，每种都有自己的端点；就 NASA 的“Astronomy Picture of the Day”API 而言，URL 端点是 `https://api.nasa.gov/planetary/apod`。
第二，写上 `?`，表示后面会跟上一串*查询参数*。
第三，给出一系列形如 `parameter=value` 的查询参数，参数之间用 `&` 分隔。
NASA 的“Astronomy Picture of the Day”API 接受的参数如图 {numref}`fig:NASA-API-parameters` 所示。

```{figure} img/reading/NASA-API-parameters.png
:name: fig:NASA-API-parameters

查询 NASA 的“Astronomy Picture of the Day”API 时可以指定的参数集合，以及每个参数的语法、默认设置和说明。
```

比如，要获取 2023 年 7 月 13 日的每日图片，这个 API 查询会有两个参数：`api_key=YOUR_API_KEY`
和 `date=2023-07-13`。记得把 `YOUR_API_KEY` 换成你通过邮件从 NASA 收到的 API 密钥！把这些组合起来，查询就长这样：
```
https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY&date=2023-07-13
```
如果你把这个 URL 输入网页浏览器，会发现服务器真的用一段文本回应了你的请求：

```json
{"date":"2023-07-13","explanation":"A mere 390 light-years away, Sun-like stars
and future planetary systems are forming in the Rho Ophiuchi molecular cloud
complex, the closest star-forming region to our fair planet. The James Webb
Space Telescope's NIRCam peered into the nearby natal chaos to capture this
infrared image at an inspiring scale. The spectacular cosmic snapshot was
released to celebrate the successful first year of Webb's exploration of the
Universe. The frame spans less than a light-year across the Rho Ophiuchi region
and contains about 50 young stars. Brighter stars clearly sport Webb's
characteristic pattern of diffraction spikes. Huge jets of shocked molecular
hydrogen blasting from newborn stars are red in the image, with the large,
yellowish dusty cavity carved out by the energetic young star near its center.
Near some stars in the stunning image are shadows cast by their protoplanetary
disks.","hdurl":"https://apod.nasa.gov/apod/image/2307/STScI-01_RhoOph.png",
"media_type":"image","service_version":"v1","title":"Webb's
Rho Ophiuchi","url":"https://apod.nasa.gov/apod/image/2307/STScI-01_RhoOph1024.png"}
```

```{index} see: JavaScript Object Notation; JSON
```

```{index} JSON, requests; get, requests; json
```

很妙吧！这里确实有数据，只是不太容易看清它到底是什么。原来这是一种常见的数据格式，叫做
*JSON*（JavaScript Object Notation）。本书不会经常遇到这类数据，
不过现在你可以像解读 Python 字典那样解读它：这些是用逗号分隔的 `key : value` 键值对（key–value pair）。
例如，仔细看就会发现，第一项是
`"date":"2023-07-13"`，说明我们确实成功取到了
2023 年 7 月 13 日对应的数据。

所以，接下来的任务是用 Python 以编程方式完成上述操作。我们先加载
`requests` 包，再用 `get` 函数发出查询，它只接受一个 URL 参数；
你应该认得这个前面粘贴到浏览器里的查询 URL。
然后，我们用 `json` 方法取得响应的 JSON 表示。

<!-- we have disabled the below code for reproducibility, with hidden setting
of the nasa_data object. But you can reproduce this using the DEMO_KEY key -->
```{code-cell} ipython3
:tags: ["remove-output"]
import requests

nasa_data_single = requests.get(
    "https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY&date=2023-07-13"
).json()
nasa_data_single
```

```{code-cell} ipython3
:tags: [remove-input]
import json
with open("data/nasa.json", "r") as f:
    nasa_data = json.load(f)
# the last entry in the stored data is July 13, 2023, so print that
nasa_data[-1]
```

使用 `start_date` 和 `end_date` 参数可以一次取得更多记录，这两个参数同样列在 {numref}`fig:NASA-API-parameters` 的参数表中。
接下来我们取出 2023 年 5 月 1 日到 2023 年 7 月 13 日之间的全部记录，把结果存进一个名为 `nasa_data` 的对象；
这一次响应会以 Python 列表的形式给出。列表中的每一项对应一天的记录（就像 `nasa_data_single` 对象那样），
总共有 74 项，起始日期到结束日期之间的每一天各占一项：

```{code-cell} ipython3
:tags: ["remove-output"]
nasa_data = requests.get(
    "https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY&start_date=2023-05-01&end_date=2023-07-13"
    ).json()
len(nasa_data)
```

```{code-cell} ipython3
:tags: [remove-input]
# need to secretly re-load the nasa data again because the above running code destroys it
# see PR 341 for why we need to do things this way (essentially due to PDF build)
with open("data/nasa.json", "r") as f:
    nasa_data = json.load(f)
len(nasa_data)
```

如果想用本书后面的技术继续处理这份数据，你需要把这个字典列表变成 `pandas` 数据框。
下面我们从 JSON 数据中抽取出 `date`、`title`、`copyright` 和 `url` 这几个变量，
再用抽出的信息构造一个 `pandas` DataFrame。

```{note}
理解这段代码不是读懂本书后续内容的必要条件。这里把它列出来，是给那些希望在自己的数据分析中把 JSON 数据解析成 `pandas` 数据框的读者参考。
```

```{code-cell} ipython3
data_dict = {
    "date":[],
    "title": [],
    "copyright" : [],
    "url": []
}

for item in nasa_data:
    if "copyright" not in item:
        item["copyright"] = None
    for entry in ["url", "title", "date", "copyright"]:
        data_dict[entry].append(item[entry])

nasa_df = pd.DataFrame(data_dict)
nasa_df
```

成功了——我们用 NASA API 创建了一个小数据集！
这份数据与网页抓取得到的结果也很不一样：
抽出的信息本身就是 JSON 格式，而不是原始的 HTML 代码（不过并非*每一种* API 都会提供这么漂亮的数据格式）。
从这一刻起，`nasa_df` 数据框就存在你的机器上，你可以尽情地摆弄它。
例如，可以用 `pandas.to_csv` 把它保存到文件，以后再用 `pandas.read_csv` 读回 Python；
读完接下来几章之后，你就有能力做更有意思的事情！
如果你还想向 NASA 的各种 API 索取更多数据
（可做的事情有哪些，[这里有一份 NASA API 精选列表](https://api.nasa.gov/)
给出了更多例子），那么请像往常一样留意自己索取了多少数据、请求的频率有多高。

+++

## 习题

本章内容的练习题可以在配套的 [练习册仓库](https://worksheets.python.datasciencebook.ca) 中
“Reading in data locally and
from the web”一行找到。点击“查看练习册”即可预览
本章练习册的非交互版本。若要以交互方式做这些习题，请按
练习册仓库中的说明下载全部练习册，再按
{numref}`第 %s 章 <move-to-your-own-machine>` 中的说明配置计算机环境。这样才能保证
练习册提供的自动反馈与指导按预期工作。



## 拓展资源

- [`pandas` 文档](https://pandas.pydata.org/docs/getting_started/index.html)
  给出了本章所讲各个函数的说明。
  如果你想进一步了解这些函数、可以使用的全部参数以及其他相关函数，就应该查阅这份文档。
- 有时你会遇到质量太差的数据，本章介绍的读取函数处理不了。
  遇到这种情况，可以查阅 [*Python for Data Analysis*](https://wesmckinney.com/book/) 中的
  [数据加载一章](https://wesmckinney.com/book/accessing-data.html#io_flat_files) {cite:p}`mckinney2012python`，
  其中更详细地讲述了 Python 如何把文件中的文本解析成数据框。
- Udacity 课程 *Linux Command Line Basics* 中有一段[视频](https://www.youtube.com/embed/ephId3mYu9o)，
  很好地讲解了绝对路径与相对路径的区别。
- 如果你读过通过网页抓取和 API 从网络获取数据那一小节，我们还提供了两个配套的教学视频，
  讲解如何用 SelectorGadget 工具取得所需的 CSS 选择器：
    - [抓取 Craigslist 上的公寓房源数据](https://www.youtube.com/embed/YdIWI6K64zo)，以及
    - [从 Wikipedia 抓取加拿大城市名称与人口数](https://www.youtube.com/embed/O9HKbdhqYzk)。

+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
