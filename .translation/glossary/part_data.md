# 术语表：数据结构、数据整理、可视化

> 覆盖范围：`intro.md`、`reading.md`、`wrangling.md`、`viz.md`。已见于 `GLOSSARY_CORE.md` 的术语不再重复收录。
> 格式：三列，依次为英文术语、中文译法、备注

## 一、数据与数据结构

data set | 数据集 | 本书指一份以表格形式组织的数据；与 data frame 区分：后者是它在 Python 中的表示
tabular data | 表格型数据 | 首见加注（tabular data）
tabular data set | 表格型数据集 | 与 tabular data 同义，指具体的一份数据
entity | 实体 | 一条观测所对应的对象
data structure | 数据结构 |
list | 列表 | 首见加注（list）
dictionary | 字典 | 首见加注（dictionary）；代码中写作 dict
dict | dict | [保留英文]
key | 键 | 与 value（取值）配对，用于查找
key–value pair | 键值对 | 首见加注（key–value pair）
object (dtype) | object | [保留英文]；字符串列或混合类型列的 dtype
int64 | int64 | [保留英文]
float64 | float64 | [保留英文]
datetime64 | datetime64 | [保留英文]；日期时间类型，正文也写作 datetime
NoneType | NoneType | [保留英文]；表示"无取值"
numeric column | 数值列 | 与字符串列相对
string column | 字符串列 |
cell | 单元格 |
row name | 行名 | read_csv 默认要求数据文件不含行名
column label | 列标签 | 强调列名可作为 loc[] 的标签使用
spreadsheet | 电子表格 |
wide format | 宽格式 | 首见加注（wide format）；取值被存成了列名
long format | 长格式 | 首见加注（long format）；取值被存成了行
untidy data | 不整洁数据 | 与整洁数据（tidy data）相对
messy data | 混乱数据 |
raw data | 原始数据 |
shape | 形状 | 指数据框的行数与列数
data file | 数据文件 |
plain text file | 纯文本文件 |
file format | 文件格式 |
file extension | 文件扩展名 |
file name | 文件名 |
absolute path | 绝对路径 | 首见加注（absolute path）；从根文件夹开始写起
relative path | 相对路径 | 首见加注（relative path）
root folder | 根文件夹 |
current directory | 当前目录 | 路径中用单个点表示
previous directory | 上一级目录 | 路径中用两个点表示
Uniform Resource Locator (URL) | 统一资源定位符 | 首见加注（Uniform Resource Locator）；缩写 URL 保留英文
URL | URL | [保留英文]
proportion | 比例 |
subgroup | 子组 | 分组结果内部更小的一组

## 二、数据整理与 pandas 操作

pandas | pandas | [保留英文]
read_csv | read_csv | [保留英文]
read_excel | read_excel | [保留英文]
read_html | read_html | [保留英文]
to_csv | to_csv | [保留英文]
skiprows | skiprows | [保留英文]；指定读取时跳过的行数
sep | sep | [保留英文]；指定列分隔符的参数
header argument | header 参数 | [保留英文]；header=None 表示文件本身没有列名；叙述语境"表头"见核心术语表
names | names | [保留英文]；读取时直接指定列名的参数
sheet_name | sheet_name | [保留英文]
usecols | usecols | [保留英文]
parse_dates | parse_dates | [保留英文]；把日期列解析成日期时间类型
separator | 分隔符 | 首见加注（separator）
tab character | 制表符 | 代码中写成 \t
escaped character | 转义字符 | 首见加注（escaped character）
reading (loading) data | 读取数据 | 书中 reading 与 loading 同义
drop | drop | [保留英文]；删除列或行
melt | melt | [保留英文]；把多列合并为一列，使数据由宽变长
pivot | pivot | [保留英文]；增加列数、减少行数，使数据由长变宽
reset_index | reset_index | [保留英文]；pivot 之后恢复整数行索引
str.split | str.split | [保留英文]；按分隔符拆开整列的字符串
astype | astype | [保留英文]；转换列的数据类型
assign | assign | [保留英文]；返回添加或修改列之后的新数据框
groupby | groupby | [保留英文]
agg | agg | [保留英文]；一次计算多个统计量
on | on | [保留英文]；merge 中指定用于匹配的列
DataFrameGroupBy | DataFrameGroupBy | [保留英文]；groupby 返回的中间对象
loc[] | loc[] | [保留英文]；按标签筛选行并选取列
iloc[] | iloc[] | [保留英文]；按位置索引行和列
[] operation | [] 操作 | [保留英文]；一次只能筛选行或选取列
isin | isin | [保留英文]；判断元素是否属于某个列表
query (DataFrame method) | query | [保留英文]；与数据库的"查询（query）"区分
head | head | [保留英文]
tail | tail | [保留英文]
info | info | [保留英文]；打印数据框的结构信息
describe | describe | [保留英文]；一次给出多个常用汇总统计量
value_counts | value_counts | [保留英文]
nlargest | nlargest | [保留英文]
nsmallest | nsmallest | [保留英文]
sort_values | sort_values | [保留英文]
max / min / sum / mean / median / std | max / min / sum / mean / median / std | [保留英文]；正文叙述用最大／最小／求和／均值／中位数／标准差
count | 计数 | 统计量译"计数"；方法名 count 保留英文，altair 中的 count() 同样保留英文
normalize (value_counts argument) | normalize | [保留英文]；与机器学习中的归一化（normalization）不是同一概念
axis=1 | axis=1 | [保留英文]；表示按行计算
logical statement | 逻辑表达式 | 首见加注（logical statement）
logical operator | 逻辑运算符 |
equivalency operator | 相等运算符 | 首见加注（equivalency operator）；代码写作 ==
inequivalency operator | 不等运算符 | 首见加注（inequivalency operator）；代码写作 !=
ampersand | 逻辑与运算符 | 首见加注（ampersand）；即 & 符号
vertical pipe | 逻辑或运算符 | 首见加注（vertical pipe）
column assignment | 列赋值 | 首见加注（column assignment）
regular column assignment | 常规列赋值 | 与 assign 方法相对
column range | 列范围 | 首见加注（column range）；用冒号语法表示
subsetting | 取子集 | 动词形式；名词 subset 见核心术语表
position | 位置 | iloc[] 按位置、loc[] 按标签，两者需区分
temporary object | 临时对象 |
chaining | 链式调用 | 首见加注（chaining）；也作"链式操作"
chained method call | 链式方法调用 | 备选：方法链
chained assignment | 链式赋值 | 出现在 SettingWithCopyWarning 的说明中
multiline expression | 多行表达式 | 首见加注（multiline expression）
SettingWithCopyWarning | SettingWithCopyWarning | [保留英文]
missing data | 缺失数据 | 与 missing value（缺失值）区分：前者指整体现象
row-wise | 按行 | 首见加注（row-wise）；与 column-wise（按列）相对
column-wise | 按列 |

## 三、可视化与 altair

altair | altair | [保留英文]
alt | alt | [保留英文]；altair 的常用别名
Chart | Chart | [保留英文]；altair 中的基本图形对象
alt.Chart | alt.Chart | [保留英文]
encode | encode | [保留英文]；把数据列映射到图形属性
encoding channel | 编码通道 | 首见加注（encoding channel）
encoding channels x / y / color / shape / tooltip | 编码通道 | 通道名一律保留英文；tooltip 见核心术语表"提示框"
graphical mark | 图形标记 | 首见加注（graphical mark）
mark_bar | mark_bar | [保留英文]；条形图的图形标记
mark_point | mark_point | [保留英文]；散点图的默认图形标记
mark_line | mark_line | [保留英文]
mark_circle | mark_circle | [保留英文]；填充圆点，不支持 shape 通道
mark_rule | mark_rule | [保留英文]；画水平或垂直参考线
alt.X | alt.X | [保留英文]
alt.Y | alt.Y | [保留英文]
alt.Color | alt.Color | [保留英文]
alt.Legend | alt.Legend | [保留英文]
alt.Scale | alt.Scale | [保留英文]
alt.Tooltip | alt.Tooltip | [保留英文]
alt.datum | alt.datum | [保留英文]；表示单个数值，而不是数据框中的某一列
configure_axis | configure_axis | [保留英文]
titleFontSize | titleFontSize | [保留英文]
properties | properties | [保留英文]；设置图形的高度、宽度等
sort("x") | sort("x") | [保留英文]；按 x 通道的取值给条形排序
scale(zero=False) | scale(zero=False) | [保留英文]；坐标轴下界不必取 0
domain | 取值范围 | 与 range（极差）区分：标度语境中指坐标轴的上下界
clip | 裁剪 | 代码 clip=True 保留英文
scheme | scheme | [保留英文]；color 标度中指定配色方案的参数
color scheme | 配色方案 | 备选：调色板
tableau10 | tableau10 | [保留英文]；altair 的默认配色方案
logarithmic (log) scale | 对数标度 | 首见加注（logarithmic scale）；正文也作 log 标度
bin width | 箱宽 | 核心术语表作"分箱（bin）"；此处指单个箱的宽度
maxbins | maxbins | [保留英文]；分箱数的上限
bucket | 分组区间 | 书中与 bin 同义；备选：桶
stack(False) | stack(False) | [保留英文]；条形不互相堆叠
stacked bars | 堆叠条形图 |
opacity | 不透明度 | 代码 opacity=0.5 保留英文
strokeDash | strokeDash | [保留英文]；把实线改成虚线
layering | 图层叠加 | 用 + 运算符叠加图层；名词 layer 见核心术语表
subplot | 子图 |
gridlines | 网格线 |
axis label | 坐标轴标签 |
plot title | 图形标题 |
overplotting | 标记重叠 | 首见加注（overplotting）；指标记互相遮盖导致看不清；备选：过度重叠绘制
visual noise | 视觉噪声 |
trend | 趋势 |
periodic oscillation | 周期性振荡 |
noisy | 有噪声的 | 与 smooth（平滑的）相对
positive relationship | 正相关关系 | 首见加注（positive relationship）；备选：正向关系
negative relationship | 负相关关系 |
strong relationship | 强相关关系 |
weak relationship | 弱相关关系 |
linear relationship | 线性关系 |
nonlinear relationship | 非线性关系 |
direction / strength / shape | 方向／强度／形状 | 书中评估两个变量关系的三个方面
cluster (in a distribution) | 簇 | 与 clustering（聚类）区分：此处指直方图中成堆出现的取值
bump (in a histogram) | 峰 | 指直方图中出现的多个峰
pie chart | 饼图 |
raster graphics | 栅格图 | 首见加注（raster graphics）；备选：位图
vector graphics | 矢量图 |
lossy | 有损的 |
lossless | 无损的 |
pixel | 像素 |
PNG | PNG | [保留英文]
SVG | SVG | [保留英文]
save (method) | save | [保留英文]；把图形存成图片文件

## 四、其他

SQL | SQL | [保留英文]
structured query language | 结构化查询语言 | 首见加注（structured query language）；缩写 SQL 保留英文
SQLite | SQLite | [保留英文]
PostgreSQL | PostgreSQL | [保留英文]
database table | 数据库表 |
table (in a database) | 表 | 与数据框（data frame）区分：数据库中的表需先查询才能取回本地
reference | 引用 | ibis 返回的是表引用，数据仍留在数据库中
ibis | ibis | [保留英文]
connect | connect | [保留英文]
list_tables | list_tables | [保留英文]
conn.table | conn.table | [保留英文]
execute | execute | [保留英文]；真正把查询结果取回 Python
compile | compile | [保留英文]；查看 ibis 生成的 SQL 语句
DatabaseTable | DatabaseTable | [保留英文]
order_by | order_by | [保留英文]
lazy evaluation | 惰性求值 | 指 ibis 在调用 execute 之前不真正取数
requests | requests | [保留英文]
BeautifulSoup | BeautifulSoup | [保留英文]
get_text | get_text | [保留英文]
select (method) | select | [保留英文]；BeautifulSoup 的方法，按 CSS 选择器取出节点；与核心术语表的"选取（select）"区分
node | 节点 | 一对 HTML 标签连同中间的内容
HTML tag | HTML 标签 |
opening tag / closing tag | 开始标签／结束标签 |
class (HTML attribute) | class 属性 | 与 DataFrame 的属性（attribute）区分
source code | 源代码 |
web server | 网络服务器 |
CSS selector | CSS 选择器 |
HTML | HTML | [保留英文]
CSS | CSS | [保留英文]
robots.txt | robots.txt | [保留英文]
Terms of Service | 服务条款 |
API key | API 密钥 | 首见加注（API key）；缩写 API 保留英文
API token | API 令牌 |
quota | 配额 |
endpoint | 端点 | 首见加注（endpoint）
assignment symbol | 赋值符号 | 首见加注（assignment symbol）；即等号
dot syntax | 点语法 | 首见加注（dot syntax）
attribute | 属性 | 与图形属性（aesthetic）区分
comment | 注释 | 代码中的注释一律保留原文，不翻译
for loop | for 循环 |
apply a function across columns | 跨列应用函数 |
functional programming | 函数式编程 | 本书未直接使用该说法；相关概念见"跨列应用函数"
