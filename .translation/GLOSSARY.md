# 《数据科学：Python 入门》翻译术语表（GLOSSARY）

> 本表是全书术语一致性的唯一依据。**翻译与审校时必须逐条遵守。**
> 第一节为核心术语（总协调人确定，优先级最高，不得更改）；其余各节由领域术语抽取生成。
> **凡后文条目与第一部分（核心术语）冲突，一律以第一部分为准；同一条目在同一节内出现多次时，取第一次出现的译法。**
> 标记 `[保留英文]` 的词在任何情况下都不翻译；标记 `[保留原文]` 的词保留原语言写法。

---

## 第一部分：核心术语（最高优先级）

# 核心术语表（权威，不得改动）

> 本文件中的译法由总协调人确定，**具有最高优先级**。扩充术语表时不得与本表冲突。
> 格式：`English | 中文 | 备注`

## A. 数据结构与 pandas

```
data frame | 数据框 | 首见加注（data frame）
DataFrame | DataFrame | [保留英文]
series | Series | 首见写「Series（序列）」，其后一律写 Series；不译作“序列”；正文中不加反引号
Series | Series | [保留英文]
variable | 变量 |
observation | 观测 |
value | 取值 |
tidy data | 整洁数据 | 首见加注（tidy data）
data wrangling | 数据整理 | 与 data cleaning 并称时"数据清洗与整理"
data cleaning | 数据清洗 |
tibble | 数据框 | 本书为 Python 版，一般出现于 R 版对照，译"数据框"
row | 行 |
column | 列 |
index | 索引 |
indexing | 索引 |
subset | 子集 |
filter | 筛选 |
select | 选取 |
sort | 排序 |
group | 分组 |
aggregate / aggregation | 聚合 |
summary statistic | 汇总统计量 |
column name | 列名 |
data type | 数据类型 |
string | 字符串 |
integer | 整数 |
float | 浮点数 |
boolean | 布尔值 |
categorical | 类别型变量 | 名词形式一律作“类别型变量”，不译作“分类变量”
missing value | 缺失值 |
NaN | NaN | [保留英文]
```

## B. 统计学与推断

```
population | 总体 |
sample | 样本 |
sampling | 抽样 |
random sample | 随机样本 |
estimation | 估计 |
estimate | 估计值 |
estimator | 估计量 |
parameter | 参数 |
point estimate | 点估计 |
bootstrap / bootstrapping | 自助法 | 首见加注（bootstrap）
bootstrap sample | 自助样本 |
bootstrap distribution | 自助分布 |
sampling distribution | 抽样分布 |
confidence interval | 置信区间 |
confidence level | 置信水平 |
statistical inference | 统计推断 |
hypothesis test | 假设检验 |
null hypothesis | 原假设 |
alternative hypothesis | 备择假设 |
p-value | p 值 |
significance level | 显著性水平 |
test statistic | 检验统计量 |
mean | 均值 |
average | 平均数 |
median | 中位数 |
mode | 众数 |
standard deviation | 标准差 |
variance | 方差 |
quartile | 四分位数 |
quantile | 分位数 |
percentile | 百分位数 |
range | 极差 |
interquartile range | 四分位距 |
distribution | 分布 |
normal distribution | 正态分布 |
probability | 概率 |
random variable | 随机变量 |
independent | 独立 |
simulation | 模拟 |
seed | 种子 |
resample | 重抽样 |
population parameter | 总体参数 |
causal | 因果的 |
mechanistic | 机理的 |
descriptive | 描述性的 |
exploratory | 探索性的 |
predictive | 预测性的 |
inferential | 推断性的 |
```

## C. 机器学习

```
machine learning | 机器学习 |
classification | 分类 |
classifier | 分类器 |
regression | 回归 |
clustering | 聚类 |
supervised learning | 有监督学习 |
unsupervised learning | 无监督学习 |
training set | 训练集 |
test set | 测试集 |
validation set | 验证集 |
cross-validation | 交叉验证 |
predictor | 预测变量 | 在回归语境中一律用"预测变量"；特征工程语境可用"特征"
explanatory variable | 解释变量 |
response variable | 响应变量 |
target | 目标变量 |
feature | 特征 |
observation | 观测 |
k-nearest neighbours | K 近邻 | 全书写法统一为 K 近邻（大写 K，与公式 $K$ 对应）；方法名 k-nearest neighbours 保留英文
k-means | K 均值 | 算法名 k-means 保留英文，叙述中用“K 均值聚类”
tuning parameter | 调优参数 |
hyperparameter | 超参数 |
overfitting | 过拟合 |
underfitting | 欠拟合 |
model | 模型 |
prediction | 预测 |
predicted value | 预测值 |
estimate | 估计值 |
accuracy | 准确率 |
precision | 精确率 |
recall | 召回率 |
sensitivity | 灵敏度 |
specificity | 特异度 |
confusion matrix | 混淆矩阵 |
true positive | 真阳性 |
true negative | 真阴性 |
false positive | 假阳性 |
false negative | 假阴性 |
threshold | 阈值 |
odds | 几率 |
odds ratio | 几率比 |
class | 类别 |
label | 标签 |
majority class | 多数类 |
minority class | 少数类 |
preprocessing | 预处理 |
standardization | 标准化 |
normalization | 归一化 |
scaling | 缩放 |
missing data imputation | 缺失值插补 |
outlier | 离群值 |
out-of-sample | 样本外 |
workflow | 工作流 |
pipeline | 流水线 |
fit | 拟合 |
predict | 预测 |
```

## D. 可视化

```
visualization | 可视化 |
scatter plot | 散点图 |
bar plot | 条形图 |
histogram | 直方图 |
boxplot | 箱线图 |
density plot | 密度图 |
violin plot | 小提琴图 |
line plot | 折线图 |
heatmap | 热力图 |
axis | 坐标轴 |
x-axis | x 轴 |
y-axis | y 轴 |
legend | 图例 |
aesthetic / aesthetic mapping | 图形属性／图形属性映射 | 首见加注（aesthetic mapping）
layer | 图层 |
facet | 分面 |
bin / binning | 箱／分箱 |
smoothing | 平滑 |
mark | 标记 |
scale | 标度 |
theme | 主题 |
tooltip | 提示框 |
```

## E. 编程、工具与环境

```
function | 函数 |
argument | 参数 | 与 parameter 区分：函数参数用"参数"，统计参数也用"参数"，靠语境
keyword argument | 关键字参数 |
method | 方法 |
object | 对象 |
operand | 操作数 |
operator | 运算符 |
syntax | 语法 |
error message | 报错信息 |
package | 包 |
library | 库 |
module | 模块 |
import | 导入 |
code cell | 代码单元格 |
markdown cell | Markdown 单元格 |
notebook | 笔记本 |
kernel | 内核 |
JupyterLab | JupyterLab | [保留英文]
Jupyter Notebook | Jupyter Notebook | [保留英文]
interactive | 交互式 |
output | 输出 |
script | 脚本 |
console | 控制台 |
terminal | 终端 |
command line | 命令行 |
file path | 文件路径 |
directory | 目录 |
folder | 文件夹 |
working directory | 工作目录 |
web scraping | 网页抓取 |
API | API | [保留英文]
JSON | JSON | [保留英文]
CSV | CSV | [保留英文]
database | 数据库 |
query | 查询 |
relational database | 关系数据库 |
```

## F. 版本控制与协作

```
version control | 版本控制 |
repository | 仓库 |
commit | 提交 |
branch | 分支 |
merge | 合并 |
merge conflict | 合并冲突 |
conflict | 冲突 |
clone | 克隆 |
push | 推送 |
pull | 拉取 |
remote | 远程仓库 |
repository host | 仓库托管平台 |
GitHub | GitHub | [保留英文]
Git | Git | [保留英文]
pull request | 拉取请求 | 首见加注（pull request）
issue | 议题 |
fork | 派生 | 首见加注（fork）
collaborator | 协作者 |
feature branch | 功能分支 |
staging area | 暂存区 |
workflow | 工作流 |
```

## G. 固定短语

```
Chapter learning objectives | 本章学习目标 |
Overview | 概述 |
Additional resources | 拓展资源 |
Putting it all together | 融会贯通 |
move-to-your-own-machine | 在你自己的机器上操作 | 该 label 名保留英文
Front Matter | 前言部分 |
Chapters | 正文章节 |
learning objective | 学习目标 |
good practices | 良好实践 |
case study | 案例分析 |
worksheets repository | 练习册仓库 | 练习册行名格式统一为「英文原名（中文）」，如「Cleaning and wrangling data（数据清洗与整理）」；中文括注须与本书该章标题一致
界面按钮／菜单项 | 中文（English） | **每次出现**都保留英文，加粗用 **中文**（English）；写成 **中文（English）**菜单 会因右边界规则失效
```

## H. 跨节冲突裁决（强制，优先级高于后续任何章节的术语条目）

以下词在不同语境下译法不同，**按语境选择，不要混用**：

```
merge | 合并 | 叙述动作用「合并」。作为 pandas 函数名出现时写 `merge`，不翻译
scale | 标度 | 图形语法（altair 的 scale）语境用「标度」
scale（动词） | 缩放 | 数据预处理语境「scale the data」→「对数据做缩放」
header | 表头 | 叙述语境用「表头」（header row → 表头行）。作为参数名或 HTML 概念时写 `header`
rename | 重命名 | 叙述语境用「重命名」。作为 pandas 函数名时写 `rename`
iteration | 迭代 | 泛称用「迭代」；明确计数时用「迭代轮次」或「第 N 轮迭代」
Pipeline | Pipeline | scikit-learn 的类名保留英文；一般概念的流水线用「流水线」
```

**裁决原则**：凡「代码标识符 / 函数名 / 类名」与「同一词的叙述性中译」并存时，**代码标识符永远保留英文**，叙事文字用中译。这不是术语冲突。

## I. 总协调人裁决（针对术语抽取过程中上报的争议）

```
University of British Columbia | 不列颠哥伦比亚大学 | 简称 UBC 保留英文；不采用「英属哥伦比亚大学」
Indigenous peoples / Aboriginal | 原住民 | 不用「土著」；Aboriginal 为加拿大统计局用语，首见加注
First Nations | 第一民族 | 首见加注（First Nations）
residential schools | 寄宿学校 | 指加拿大原住民寄宿学校，首见加注（residential schools）
sample distribution | 样本分布 | 与「抽样分布」（sampling distribution）严格区分
界面菜单项 | 中文（English） | 如「运行全部单元格（Run All Cells）」；**每次出现**都保留英文（GitHub 无中文界面，JupyterLab 默认也是英文）
multivariable linear regression | 多元线性回归 | 中文统计学界通行译法（多元回归分析）；不采用「多变量线性回归」
multivariate | 多变量 | 与 multivariable 区分：multivariate 指多个响应/多个变量并存，multivariable 指多个预测变量
```

**界面菜单项规则**：书中截图是英文界面（GitHub 没有中文界面，JupyterLab 默认也是英文）。菜单项、按钮名译成中文，**每次出现**都以「中文（English）」形式保留英文原文，不要只在首次出现时括注。加粗时用 `**中文**（English）` 的形式，不要写成 `**中文（English）**菜单`（收尾 `**` 之后紧跟汉字会触发右边界规则，星号原样显示）。例：

- `Run All Cells` → `**运行全部单元格**（Run All Cells）`
- `Restart Kernel and Run All Cells` → `**重启内核并运行全部单元格**（Restart Kernel and Run All Cells）`
- `Commit changes` → `**提交更改**（Commit changes）`

## J. 第二轮裁定（FIX_SPEC_2，优先级高于上表）

```
series / Series 正文 | 首次写「Series（序列）」，其后一律写 Series；不译作「序列」；正文中不加反引号
categorical / categorical variable | 一律作「类别型变量」，不译作「分类变量」
k-nearest neighbours / k-means 正文 | 一律作「K 近邻」「K 均值」（大写 K，与公式 $K$ 对应）
练习册行名 | 一律作「英文原名（中文）」（英文在前），如「Classification I: training and prediction（分类 I：训练与预测）」；中文括注须与本书该章标题一致
界面按钮／菜单项 | **每次出现**都写「中文（English）」，加粗用 **中文**（English）；练习册这类文档链接保持不加粗
译注引号 | 译注中一律用 “ ”，不用 「」；译注内不用行内代码
```

---

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

---

# 术语表：机器学习（分类、回归、聚类、模型评估）

## 一、通用机器学习概念
data set | 数据集 |
data point | 数据点 |
measurement | 测量值 | 指对观测某个特征的量测结果
predictive question | 预测性问题 | 首见加注（predictive question）；与描述性、探索性问题相对
prediction error | 预测误差 |
model object | 模型对象 | 首见加注（model object）
model training | 模型训练 |
train | 训练 | 动词；与测试、验证三个阶段对应
training data | 训练数据 |
test data | 测试数据 |
retrain | 重新训练 |
algorithm | 算法 |
assumption | 假设 | 指模型前提；与假设检验中的"原假设"不是一回事
candidate model | 候选模型 |
generalization | 泛化 | 首见加注（generalization）；动词形式 generalize 译"泛化到"
interpretability | 可解释性 |
trade-off | 权衡取舍 |
reproducible | 可复现的 | 修饰 analysis 时译"可复现的分析"
randomness | 随机性 |
random number generator | 随机数生成器 | 缩写 RNG 保留英文
default random number generator | 默认随机数生成器 |
noise | 噪声 |
underlying structure | 潜在结构 | 指数据中未被标注出来的分组结构
subgroup | 子组 |
pattern | 模式 |
labeled data | 有标签数据 |
unlabeled data | 无标签数据 |
irrelevant predictor | 无关预测变量 |
informative predictor | 有信息量的预测变量 |
predictor variable selection | 预测变量选择 | 本书小节标题；亦称 variable selection
variable selection | 变量选择 |
best subset selection | 最优子集选择 | 首见加注（best subset selection）
forward selection | 前向选择 | 首见加注（forward selection）
feature engineering | 特征工程 | 首见加注（feature engineering）；特征与预测变量指同一对象，按语境择一
predictor design | 预测变量设计 | 本书中与 feature engineering 同义
preprocessor | 预处理器 | 首见加注（preprocessor）
centering | 中心化 |
center | 中心 | 名词，指变量的中心位置
unstandardized data | 未标准化数据 |
standardized data | 标准化数据 |
unscaled data | 未缩放数据 |
impute | 插补 |
mean imputation | 均值插补 |
missing entries | 缺失项 |
randomly missing | 随机缺失 | 原文指缺失与观测的其它方面无关
informative missingness | 有信息量的缺失 | 原文指缺失本身可能与其它变量取值相关
synthetic values | 合成取值 |
numerical variable | 数值变量 |
quantitative variable | 定量变量 |
categorical variable | 类别型变量 | 与 categorical 同一条目，一律作“类别型变量”，不译作“分类变量”
K-NN | K 近邻 | 叙述中一律作 K 近邻；英文串 K-NN 仅作首见括注出现一次
supervised task | 有监督任务 |
unsupervised task | 无监督任务 |

## 二、分类
classification problem | 分类问题 |
binary classification | 二分类 | 首见加注（binary classification）
multiclass classification | 多分类 | 首见加注（multiclass classification）
class label | 类别标签 | 与 label（标签）同义，正文两词混用
predicted label | 预测标签 |
actual label | 实际标签 | 正文亦称 true label（真实标签）
positive label | 正类标签 | 与 negative label 相对；是理解精确率与召回率的关键
negative label | 负类标签 |
positive observation | 正类观测 |
misclassification | 误分类 | 动词 misclassify 同译
majority vote | 多数投票 |
majority classifier | 多数类分类器 | 备选：多数投票分类器；与 majority class（多数类）区分，前者是模型，后者是类别
ties | 平局 | 原文指投票票数相同的平局情形
distance | 距离 |
straight-line distance | 直线距离 | 首见加注（straight-line distance）
Euclidean distance | 欧氏距离 | 首见加注（Euclidean distance）
nearest neighbour | 最近邻 | 本书用英式拼写；美式写作 nearest neighbor
number of neighbors | 近邻个数 | 即 K 近邻算法中的参数 K
new observation | 新观测 |
decision | 判别 | 指分类器对新观测给出的类别判定
boundary | 边界 | 指分类判别边界；K 过小时呈锯齿状
class proportions | 类别比例 |
class imbalance | 类别不平衡 | 首见加注（class imbalance）
imbalanced data | 不平衡数据 |
rare class | 稀有类 |
rebalance | 重新平衡 |
balanced data | 平衡数据 |
oversampling | 过采样 | 首见加注（oversampling）
upsampled data | 上采样后的数据 | 本书用 sample 方法复制稀有类观测实现
voting power | 表决权 |
precision and recall | 精确率与召回率 | 与 accuracy 区分：accuracy 看整体正确比例，precision 只看预测为正的观测中真正为正的比例
decision tree | 决策树 | 拓展资源中提及，本书未展开
support vector machine | 支持向量机 | 拓展资源中提及，缩写 SVM 保留英文
logistic regression | 逻辑回归 | 用于分类而非回归，原文特别提醒名称容易混淆
neural network | 神经网络 |
linear discriminant analysis | 线性判别分析 |
naive Bayes | 朴素贝叶斯 |
benign | 良性的 | 乳腺癌案例的类别名；数据列取值 Benign 保留英文，搭配译"良性肿瘤"
malignant | 恶性的 | 乳腺癌案例的类别名；数据列取值 Malignant 保留英文，搭配译"恶性肿瘤"

## 三、回归
regression problem | 回归问题 |
K-NN regression | K 近邻回归 |
linear regression | 线性回归 |
simple linear regression | 简单线性回归 |
multivariable linear regression | 多变量线性回归 | 首见加注（multivariable linear regression）；指含多个预测变量的情形，备选：多元线性回归
regression equation | 回归方程 |
line of best fit | 最优拟合直线 | 备选：最佳拟合线
plane of best fit | 最优拟合平面 |
vertical intercept | 纵截距 |
intercept | 截距 |
slope | 斜率 |
coefficient | 系数 |
linear relationship | 线性关系 |
non-linear relationship | 非线性关系 |
flexible | 灵活的 | 形容 K 近邻拟合线可随数据起伏；原文亦用 wiggly
extrapolation | 外推 | 首见加注（extrapolation）
average squared vertical distance | 纵向距离平方的平均值 | 原文对最小二乘拟合的直观解释
RMSPE | 均方根预测误差 | 首见加注（root mean squared prediction error）；缩写 RMSPE 保留英文，备选：根均方预测误差
RMSE | 均方根误差 | 缩写 RMSE 保留英文；计算式与 RMSPE 完全相同，区别只在用于训练数据还是测试数据
mean squared error | 均方误差 | 首见加注（mean squared error）
training error | 训练误差 | 样本内误差；与 test error 区分
test error | 测试误差 | 样本外误差
in-sample prediction | 样本内预测 |
multicollinearity | 多重共线性 | 首见加注（multicollinearity）；指预测变量之间高度线性相关，此类变量译"共线预测变量"
goodness of fit | 拟合优度 | 本书亦写 model goodness of fit，同译
influence | 影响 | 指单个数据点对拟合直线的拉动程度
transformed predictor | 变换后的预测变量 |
regression tree | 回归树 | 拓展资源中提及，本书未展开
spline | 样条 | 拓展资源中提及，本书未展开
local regression | 局部回归 | 拓展资源中提及，本书未展开

## 四、聚类
cluster | 簇 | 首见加注（cluster）；与 clustering（聚类）区分，前者指一个分组，后者指方法或结果
clustering algorithm | 聚类算法 |
cluster center | 簇中心 | 代码中的变量名写作 centroid
centroid | 质心 | 与 cluster center 同义；代码变量名 centroid 保留英文
cluster label | 簇标签 |
cluster assignment | 簇归属 | 正文亦称 assignment，指数据点被分到哪个簇
initial centers | 初始中心 |
random initialization | 随机初始化 |
random restart | 随机重启 | 本书小节标题 Random restarts
bad solution | 劣质解 | 原文指 K 均值因初始化不佳而“卡住”的较差结果
center update | 中心更新 | K 均值算法两步之一
label update | 标签更新 | K 均值算法两步之一
WSSD | 簇内平方距离和 | 缩写 WSSD 保留英文；全称 within-cluster sum-of-squared-distances
within-cluster sum-of-squared-distances | 簇内平方距离和 | 首见加注（within-cluster sum-of-squared-distances）
total WSSD | 总 WSSD | 所有簇的 WSSD 之和，K 均值的目标即最小化该量；图中亦称 total within-cluster sum of squares
inertia | 惯性 | scikit-learn 中 inertia_ 属性即总 WSSD；属性名保留英文
cluster quality | 聚类质量 |
elbow method | 肘部法则 | 首见加注（elbow method）
elbow | 肘部 | 指总 WSSD 曲线由陡降转为平缓的拐弯处
number of clusters | 簇数 |
subdivide | 细分 | 与合并相对；K 过大时子组被细分
semisupervised | 半监督 | 首见加注（semisupervised）
hierarchical clustering | 层次聚类 | 本书仅在拓展资源中提及
principal component analysis | 主成分分析 | 缩写 PCA 保留英文
multidimensional scaling | 多维标度法 | 本书仅在拓展资源中提及
silhouette | 轮廓系数 | 本书正文未出现，作为聚类质量评估的通用指标收录

## 五、模型评估与调优
evaluating performance | 评估性能 |
performance | 性能 |
estimated accuracy | 估计准确率 | 交叉验证给出的准确率估计亦称 accuracy estimate（准确率估计值）
prediction accuracy | 预测准确率 | 与 precision（精确率）区分：前者是整体正确比例
estimated cross-validation accuracy | 交叉验证准确率估计值 |
validation accuracy | 验证准确率 |
perfect classifier | 完美分类器 |
trade-off between precision and recall | 精确率与召回率之间的权衡 |
baseline | 基准 | 指便于比较的简单方法，如多数类分类器
standard error | 标准误 | 首见加注（standard error）；与 standard deviation（标准差）区分
folds | 折 | 交叉验证中的等份；单数 fold 同译
number of folds | 折数 |
5-fold cross-validation | 5 折交叉验证 |
chunks | 等份 | 原文指把训练数据均分成的若干等份
train/test split | 训练/测试划分 |
train/validation split | 训练/验证划分 |
split the data | 划分数据 |
shuffle | 打乱 |
stratification | 分层 | 首见加注（stratification）；动词 stratify 同译
stratified split | 分层划分 |
held out | 留出 | 指调优期间不使用、最后才评估的数据
lock box | 保险箱 | 原文比喻，指把测试集暂时封存起来
golden rule of machine learning | 机器学习黄金法则 | 原文强调绝不能用测试数据来建模
tuning | 调优 | 动词 tune 与分词 tuning 同译
tuning process | 调优过程 |
parameter tuning | 参数调优 |
model selection | 模型选择 | 本书表述为调优与评估的整体流程
parameter value | 参数取值 |
parameter grid | 参数网格 |
grid search | 网格搜索 |
model simplicity | 模型简洁性 |
number of predictors | 预测变量个数 |
computational cost | 计算成本 |
critical analysis | 批判性分析 |
downstream application | 下游应用 |

## 六、scikit-learn API
scikit-learn | scikit-learn | [保留英文]；在 Python 中导入名为 sklearn
KNeighborsClassifier | KNeighborsClassifier | [保留英文]
KNeighborsRegressor | KNeighborsRegressor | [保留英文]
LinearRegression | LinearRegression | [保留英文]
Ridge | Ridge | [保留英文]；本书未直接使用，与 LinearRegression 同属回归模型名
KMeans | KMeans | [保留英文]
GridSearchCV | GridSearchCV | [保留英文]
RandomizedSearchCV | RandomizedSearchCV | [保留英文]；本书仅在索引中出现
SequentialFeatureSelector | SequentialFeatureSelector | [保留英文]
train_test_split | train_test_split | [保留英文]
cross_validate | cross_validate | [保留英文]
make_pipeline | make_pipeline | [保留英文]
make_column_transformer | make_column_transformer | [保留英文]
ColumnTransformer | ColumnTransformer | [保留英文]
make_column_selector | make_column_selector | [保留英文]
StandardScaler | StandardScaler | [保留英文]
SimpleImputer | SimpleImputer | [保留英文]
set_config | set_config | [保留英文]；其参数 transform_output 亦保留英文
transform | 变换 | 方法名 transform 保留英文；与 fit 配对使用
score | 得分 | 方法名 score 保留英文；分类器默认给出准确率
get_params | 获取参数 | 方法名 get_params 保留英文
labels_ | labels_ | [保留英文]
inertia_ | inertia_ | [保留英文]
n_clusters | n_clusters | [保留英文]
n_init | n_init | [保留英文]
n_neighbors | n_neighbors | [保留英文]
random_state | random_state | [保留英文]
cv | cv | [保留英文]；交叉验证折数参数
cv_results_ | cv_results_ | [保留英文]
best_params_ | best_params_ | [保留英文]
coef_ | coef_ | [保留英文]
intercept_ | intercept_ | [保留英文]
estimator argument | estimator 参数 | scikit-learn 中指传入的模型对象；与统计学的"估计量"estimator 区分
param_grid | param_grid | [保留英文]
scoring | scoring | [保留英文]
neg_root_mean_squared_error | neg_root_mean_squared_error | [保留英文]；scikit-learn 用负 RMSPE 以便统一按最大化处理
pos_label | pos_label | [保留英文]
y_true | y_true | [保留英文]
y_pred | y_pred | [保留英文]
crosstab | crosstab | [保留英文]
precision_score | precision_score | [保留英文]
recall_score | recall_score | [保留英文]
mean_squared_error | mean_squared_error | [保留英文]
euclidean_distances | euclidean_distances | [保留英文]
train_size | train_size | [保留英文]
test_size | test_size | [保留英文]
shuffle argument | shuffle 参数 | 参数名保留英文；控制划分前是否打乱数据
stratify argument | stratify 参数 | 参数名保留英文；按类别标签分层划分
remainder | remainder | [保留英文]
passthrough | passthrough | [保留英文]
verbose_feature_names_out | verbose_feature_names_out | [保留英文]
dtype_include | dtype_include | [保留英文]
weights | weights | [保留英文]

---

# 术语表：统计推断、工具与环境、版本控制

## 一、统计推断
inferential question | 推断性问题 | 首见加注（inferential question）
interval estimation | 区间估计 | 与点估计 point estimate 相对
sample estimate | 样本估计值 | 与点估计同指，正文互见
proportion | 比例 |
population proportion | 总体比例 |
sample proportion | 样本比例 |
sampling variability | 抽样变异性 | 备选：抽样波动
sample size | 样本量 |
sample mean | 样本均值 |
population mean | 总体均值 |
sample distribution | 样本分布 | 与抽样分布 sampling distribution 严格区分
population distribution | 总体分布 |
sampling distribution of the mean | 均值的抽样分布 |
sampling distribution of the proportion | 比例的抽样分布 |
bell-shaped | 钟形的 | 首见加注（bell-shaped）
symmetric | 对称的 |
skewed | 偏斜的 | 首见加注（skewed）；备选：偏态的
long tail | 长尾 |
right tail | 右侧长尾 | 备选：右尾
one peak | 单峰 |
measure of center | 集中趋势度量 | 备选：位置的度量
spread | 离散程度 | 备选：波动程度
measure of spread | 离散程度度量 |
variability | 变异性 |
quantitative | 定量的 | 与 categorical 相对；备选：数值型
case | 研究个体 | 与核心表 case study（案例分析）区分
with replacement | 有放回 | 首见加注（with replacement）
without replacement | 无放回 |
bootstrap process | 自助过程 |
percentile bootstrap confidence interval | 百分位数自助置信区间 | 首见加注（percentile bootstrap confidence interval）
lower bound | 下限 |
upper bound | 上限 |
plausible range of values | 合理取值范围 | 置信区间定义用语
capture the population parameter | 覆盖总体参数 | 指区间包含参数真值
uncertainty | 不确定性 |
estimate accuracy | 估计的准确程度 | 与机器学习的准确率 accuracy 区分
finite population | 有限总体 |
rule of thumb | 经验法则 |
replicate | 重复 | 指第几次抽样，代码列名 `replicate` 保留英文

## 二、Jupyter 与开发环境
Jupyter | Jupyter | [保留英文]
JupyterHub | JupyterHub | [保留英文]
JupyterLab Desktop | JupyterLab Desktop | [保留英文]
Jupyter Git extension | Jupyter Git 扩展 | 扩展名保留英文
jupyterlab-git | jupyterlab-git | [保留英文]
Jupyter file browser | Jupyter 文件浏览器 |
Launcher | 启动器 | JupyterLab 界面标签页
Python session | Python 会话 |
restart | 重启 |
interrupt | 中断 |
idle | 空闲 | 内核状态
linear order | 线性顺序 | 指从上到下依次执行
nonlinear notebook | 非线性笔记本 | 指单元格执行顺序被打乱
out-of-order execution | 乱序执行 |
best practice | 最佳实践 | 与核心表 good practices（良好实践）并用
toolbar | 工具栏 |
autosave | 自动保存 | 首见加注（autosave）
rich text | 富文本 | 首见加注（rich text）
rendered | 已渲染 |
unrendered | 未渲染 | 首见加注（unrendered）
Markdown language | Markdown 语言 | [保留英文]
plain text file | 纯文本文件 |
separator | 分隔符 |
file extension | 文件扩展名 |
hidden dependency | 隐含依赖 | 备选：隐藏依赖
list comprehension | 列表推导式 | 首见加注（list comprehension）
web browser | 网页浏览器 | Firefox、Safari、Chrome、Edge 等名称保留英文
Run All Cells | 运行全部单元格 | 界面菜单项，**每次出现**都写「运行全部单元格（Run All Cells）」
Restart Kernel and Run All Cells | 重启内核并运行全部单元格 | 界面菜单项，**每次出现**都保留英文
Interrupt Kernel | 中断内核 | 界面菜单项，**每次出现**都保留英文
Restart Kernel | 重启内核 | 界面菜单项，**每次出现**都保留英文
Save Notebook | 保存笔记本 | 界面菜单项，**每次出现**都保留英文
Docker | Docker | [保留英文]
Docker Desktop | Docker Desktop | [保留英文]
container | 容器 | 首见加注（container）
image | 镜像 | Docker 语境，勿与"图片"混淆
tag | 标签 | Docker 镜像版本标签
Dockerfile | Dockerfile | [保留英文]
conda | conda | [保留英文]
pip | pip | [保留英文]
environment.yml | environment.yml | [保留英文]
Python environment | Python 环境 |
autograder test | 自动评分测试 |
WSL-2 / Hyper-V | 保留英文 | [保留英文]
Ubuntu Linux | Ubuntu Linux | [保留英文]
MacOS | MacOS | [保留英文]
Windows | Windows | [保留英文]

## 三、版本控制与 GitHub
version control system | 版本控制系统 |
local repository | 本地仓库 | 与核心表 remote（远程仓库）配套
repository history | 仓库历史 |
version history | 版本历史 |
snapshot | 快照 | 首见加注（snapshot）
commit message | 提交信息 |
commit hash | 提交哈希值 |
revert | 回退 | 备选：还原
track changes | 跟踪更改 |
untracked | 未跟踪 | Jupyter Git 面板分组名
changed | 已修改 | Jupyter Git 面板分组名
staged | 已暂存 | Jupyter Git 面板分组名
add | 添加 | 指把文件加入暂存区，与 GitHub 的 Add file 菜单区分
checkpoint file | 检查点文件 | 首见加注（checkpoint file）
auto-generated file | 自动生成的文件 |
plain text editor | 纯文本编辑器 |
merge conflict marker | 合并冲突标记 | 指 `<<<<<<< HEAD` 一类标记
resolve a merge conflict | 解决合并冲突 |
write access | 写权限 | 首见加注（write access）
personal access token | 个人访问令牌 | 首见加注（personal access token）
PAT | PAT | [保留英文]
authentication | 身份验证 |
credentials | 凭据 |
public repository | 公开仓库 |
private repository | 私有仓库 |
README.md | README.md | [保留英文]
Git pane | Git 面板 | Jupyter Git 扩展界面
issue thread | 议题讨论串 |
collaborator access | 协作者访问权限 |
negative results | 负面结果 | 指未能成功的分析尝试
bug | 缺陷 | 首见加注（bug）
HTTPS method | HTTPS 方式 | [保留英文]
GitLab | GitLab | [保留英文]
pen tool | 铅笔工具 | GitHub 界面工具，**每次出现**都保留英文（pen tool）
Commit changes | 提交更改 | GitHub 界面按钮，**每次出现**都写「提交更改（Commit changes）」
Add file | 添加文件 | GitHub 界面菜单，**每次出现**都保留英文
Upload files | 上传文件 | GitHub 界面菜单项，**每次出现**都保留英文
Manage access | 管理访问权限 | GitHub 界面，**每次出现**都保留英文
Invite a collaborator | 邀请协作者 | GitHub 界面按钮，**每次出现**都保留英文
New issue | 新建议题 | GitHub 界面按钮，**每次出现**都保留英文
Close issue | 关闭议题 | GitHub 界面按钮，**每次出现**都保留英文
Generate new token | 生成新令牌 | GitHub 界面按钮，**每次出现**都保留英文

## 四、课程组织与教学用语
worksheet | 练习册 | 指配套的 Jupyter 笔记本习题文件，首见加注（worksheet）
worksheets repository | 练习册仓库 | 行名格式统一为「英文原名（中文）」，如「Reading in data locally and from the web（从本地和网络读取数据）」；中文括注须与本书该章标题一致
view worksheet | 查看练习册 | 文档链接按钮，**不加粗**；每次出现都写「查看练习册（view worksheet）」
exercise | 习题 | 章节小节名 Exercises 译"习题"
non-interactive version | 非交互版本 |
automated feedback | 自动反馈 |
autograder | 自动评分程序 | 备选：自动评分器
course setup | 课程环境配置 |
introductory course | 入门课程 |
instructor | 授课教师 |
first-year student | 一年级学生 |
undergraduate student | 本科生 |
graduate course | 研究生课程 |
curriculum | 课程体系 |
open textbook | 开源教材 |
open educational resource | 开放教育资源 | 缩写 OER 保留英文
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License | 知识共享 署名—非商业性使用—相同方式共享 4.0 国际许可协议 | 首见加注（Creative Commons）
table of contents | 目录 |
Preface | 前言 | 与核心表 Front Matter（前言部分）区分
Foreword | 序言 |
Acknowledgments | 致谢 |
About the authors | 作者简介 |
reviewer | 审稿人 |
mentorship | 指导 |
Associate Professor of Teaching | 教学系列副教授 | UBC 教学岗；备选：教学副教授
Assistant Professor of Teaching | 教学系列助理教授 |
postdoctoral associate | 博士后研究员 |

## 五、机构、人名与专有名词（保留原文）
University of British Columbia | 不列颠哥伦比亚大学 | 简称 UBC 保留英文；备选：英属哥伦比亚大学；卑诗大学
British Columbia | 不列颠哥伦比亚省 | 备选：卑诗省
Department of Statistics | 统计系 | UBC 统计系
Department of Earth, Ocean, and Atmospheric Sciences | 地球、海洋与大气科学系 |
University of Toronto | 多伦多大学 |
MIT | 麻省理工学院 | 正文可写"麻省理工学院（MIT）"
Johns Hopkins Bloomberg School of Public Health | 约翰斯·霍普金斯大学布隆伯格公共卫生学院 | 备选：约翰霍普金斯大学
Statistics Canada | 加拿大统计局 |
Census of Population 2016 | 2016 年加拿大人口普查 |
mother tongue | 母语 | 加拿大人口普查用语
Indigenous peoples | 原住民 | 加拿大语境用"原住民"，不用"土著"
Indigenous languages | 原住民语言 |
First Nations | 第一民族 | 首见加注（First Nations）
Métis | 梅蒂人 | 备选：梅蒂斯人
Inuit | 因纽特人 |
Aboriginal | 原住民 | 加拿大统计局用语，与 Indigenous 同指
residential schools | 寄宿学校 | 指加拿大原住民寄宿学校，首见加注（residential schools）
colonization | 殖民化 |
endangered language | 濒危语言 |
Truth and Reconciliation Commission of Canada | 加拿大真相与和解委员会 | 首见加注（Truth and Reconciliation Commission）
Calls to Action | 《行动呼吁》 | 真相与和解委员会文件，保留英文原名
They Came for the Children | 《他们为孩子而来：加拿大、原住民与寄宿学校》 | 书名首见保留英文原名
Pulling Together: Foundations Guide | 《Pulling Together：基础指南》 | 保留英文书名
Canadian Geographic | 《Canadian Geographic》 | [保留英文]
Airbnb | Airbnb | [保留英文]
OpenIntro Statistics | 《OpenIntro Statistics》 | [保留英文] 书名
Data Science: A First Introduction with Python | 《Data Science: A First Introduction with Python》 | 书名保留英文原名
Tiffany Timbers | Tiffany Timbers | [保留原文]；如需音译可作"蒂法尼·廷伯斯"
Trevor Campbell | Trevor Campbell | [保留原文]
Melissa Lee | Melissa Lee | [保留原文]
Joel Ostblom | Joel Ostblom | [保留原文]
Lindsey Heagy | Lindsey Heagy | [保留原文]
Roger D. Peng | Roger D. Peng | [保留原文] 序言作者
Gabriela Cohen Freue | Gabriela Cohen Freue | [保留原文]
Hadley Wickham | Hadley Wickham | [保留原文]；备选音译：哈德利·威克姆
Mark T. Holder | Mark T. Holder | [保留原文] 章节题词作者
Navya Dahiya | Navya Dahiya | [保留原文]
Gloria Ye | Gloria Ye | [保留原文]
Philip Austin | Philip Austin | [保留原文]
Jim Zidek | Jim Zidek | [保留原文]
Kory Wilson | Kory Wilson | [保留原文]；《Pulling Together》作者
book reviewers | 审稿人 | Rohan Alexander、Isabella Ghement、Virgilio Gómez Rubio、Albert Kim、Adam Loy、Maria Prokofieva、Emily Riederer、Greg Wilson 均 [保留原文]

---
