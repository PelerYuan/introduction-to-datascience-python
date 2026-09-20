# 本章术语表（reading）

> 这是从全书术语表按本章语料抽取的子集，**已包含全部核心术语**。
> 需要查证未列出的词时，再打开 `.translation/GLOSSARY.md` 全文。
> 格式：`English | 中文 | 备注`

## 一、核心术语（最高优先级，含跨节裁决）

data frame | 数据框 | 首见加注（data frame）
DataFrame | DataFrame | [保留英文]
series | 序列 | 首见加注（series）；特指 pandas 对象时写 `Series`
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
categorical | 分类的／类别型 |
missing value | 缺失值 |
NaN | NaN | [保留英文]
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
k-nearest neighbours | k 近邻 | 全书写法统一为 k 近邻，方法名 k-nearest neighbours 保留英文
k-means | k 均值 | 算法名 k-means 保留英文，叙述中用"k 均值聚类"
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
merge | 合并 | 叙述动作用「合并」。作为 pandas 函数名出现时写 `merge`，不翻译
scale | 标度 | 图形语法（altair 的 scale）语境用「标度」
scale（动词） | 缩放 | 数据预处理语境「scale the data」→「对数据做缩放」
header | 表头 | 叙述语境用「表头」（header row → 表头行）。作为参数名或 HTML 概念时写 `header`
rename | 重命名 | 叙述语境用「重命名」。作为 pandas 函数名时写 `rename`
iteration | 迭代 | 泛称用「迭代」；明确计数时用「迭代轮次」或「第 N 轮迭代」
Pipeline | Pipeline | scikit-learn 的类名保留英文；一般概念的流水线用「流水线」
University of British Columbia | 不列颠哥伦比亚大学 | 简称 UBC 保留英文；不采用「英属哥伦比亚大学」
Indigenous peoples / Aboriginal | 原住民 | 不用「土著」；Aboriginal 为加拿大统计局用语，首见加注
First Nations | 第一民族 | 首见加注（First Nations）
residential schools | 寄宿学校 | 指加拿大原住民寄宿学校，首见加注（residential schools）
sample distribution | 样本分布 | 与「抽样分布」（sampling distribution）严格区分
界面菜单项 | 中文（English） | 如「运行全部单元格（Run All Cells）」；同一章内首见处括注英文，其后只用中文
multivariable linear regression | 多元线性回归 | 中文统计学界通行译法（多元回归分析）；不采用「多变量线性回归」
multivariate | 多变量 | 与 multivariable 区分：multivariate 指多个响应/多个变量并存，multivariable 指多个预测变量

## part_data（本章相关条目）

data set | 数据集 | 本书指一份以表格形式组织的数据；与 data frame 区分：后者是它在 Python 中的表示
tabular data | 表格型数据 | 首见加注（tabular data）
tabular data set | 表格型数据集 | 与 tabular data 同义，指具体的一份数据
list | 列表 | 首见加注（list）
dictionary | 字典 | 首见加注（dictionary）；代码中写作 dict
dict | dict | [保留英文]
key | 键 | 与 value（取值）配对，用于查找
object (dtype) | object | [保留英文]；字符串列或混合类型列的 dtype
int64 | int64 | [保留英文]
float64 | float64 | [保留英文]
numeric column | 数值列 | 与字符串列相对
cell | 单元格 |
spreadsheet | 电子表格 |
shape | 形状 | 指数据框的行数与列数
data file | 数据文件 |
plain text file | 纯文本文件 |
file format | 文件格式 |
file name | 文件名 |
absolute path | 绝对路径 | 首见加注（absolute path）；从根文件夹开始写起
relative path | 相对路径 | 首见加注（relative path）
root folder | 根文件夹 |
current directory | 当前目录 | 路径中用单个点表示
previous directory | 上一级目录 | 路径中用两个点表示
Uniform Resource Locator (URL) | 统一资源定位符 | 首见加注（Uniform Resource Locator）；缩写 URL 保留英文
URL | URL | [保留英文]
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
separator | 分隔符 | 首见加注（separator）
tab character | 制表符 | 代码中写成 \t
escaped character | 转义字符 | 首见加注（escaped character）
drop | drop | [保留英文]；删除列或行
assign | assign | [保留英文]；返回添加或修改列之后的新数据框
on | on | [保留英文]；merge 中指定用于匹配的列
query (DataFrame method) | query | [保留英文]；与数据库的"查询（query）"区分
head | head | [保留英文]
tail | tail | [保留英文]
info | info | [保留英文]；打印数据框的结构信息
describe | describe | [保留英文]；一次给出多个常用汇总统计量
count | 计数 | 统计量译"计数"；方法名 count 保留英文，altair 中的 count() 同样保留英文
logical statement | 逻辑表达式 | 首见加注（logical statement）
alt | alt | [保留英文]；altair 的常用别名
encode | encode | [保留英文]；把数据列映射到图形属性
properties | properties | [保留英文]；设置图形的高度、宽度等
domain | 取值范围 | 与 range（极差）区分：标度语境中指坐标轴的上下界
PNG | PNG | [保留英文]
save (method) | save | [保留英文]；把图形存成图片文件
SQL | SQL | [保留英文]
structured query language | 结构化查询语言 | 首见加注（structured query language）；缩写 SQL 保留英文
SQLite | SQLite | [保留英文]
PostgreSQL | PostgreSQL | [保留英文]
database table | 数据库表 |
reference | 引用 | ibis 返回的是表引用，数据仍留在数据库中
ibis | ibis | [保留英文]
connect | connect | [保留英文]
list_tables | list_tables | [保留英文]
conn.table | conn.table | [保留英文]
execute | execute | [保留英文]；真正把查询结果取回 Python
compile | compile | [保留英文]；查看 ibis 生成的 SQL 语句
DatabaseTable | DatabaseTable | [保留英文]
order_by | order_by | [保留英文]
requests | requests | [保留英文]
BeautifulSoup | BeautifulSoup | [保留英文]
get_text | get_text | [保留英文]
select (method) | select | [保留英文]；BeautifulSoup 的方法，按 CSS 选择器取出节点；与核心术语表的"选取（select）"区分
node | 节点 | 一对 HTML 标签连同中间的内容
HTML tag | HTML 标签 |
source code | 源代码 |
web server | 网络服务器 |
CSS selector | CSS 选择器 |
HTML | HTML | [保留英文]
CSS | CSS | [保留英文]
robots.txt | robots.txt | [保留英文]
Terms of Service | 服务条款 |
API key | API 密钥 | 首见加注（API key）；缩写 API 保留英文
quota | 配额 |
endpoint | 端点 | 首见加注（endpoint）

## part_ml（本章相关条目）

data set | 数据集 |
pattern | 模式 |
center | 中心 | 名词，指变量的中心位置
ties | 平局 | 原文指投票票数相同的平局情形
score | 得分 | 方法名 score 保留英文；分类器默认给出准确率
remainder | remainder | [保留英文]

## part_tools（本章相关条目）

spread | 离散程度 | 备选：波动程度
case | 研究个体 | 与核心表 case study（案例分析）区分
toolbar | 工具栏 |
plain text file | 纯文本文件 |
separator | 分隔符 |
web browser | 网页浏览器 | Firefox、Safari、Chrome、Edge 等名称保留英文
image | 镜像 | Docker 语境，勿与"图片"混淆
tag | 标签 | Docker 镜像版本标签
snapshot | 快照 | 首见加注（snapshot）
changed | 已修改 | Jupyter Git 面板分组名
add | 添加 | 指把文件加入暂存区，与 GitHub 的 Add file 菜单区分
plain text editor | 纯文本编辑器 |
PAT | PAT | [保留英文]
worksheet | 练习册 | 指配套的 Jupyter 笔记本习题文件，首见加注（worksheet）
worksheets repository | 练习册仓库 |
exercise | 习题 | 章节小节名 Exercises 译"习题"
non-interactive version | 非交互版本 |
automated feedback | 自动反馈 |
MIT | 麻省理工学院 | 正文可写"麻省理工学院（MIT）"
Statistics Canada | 加拿大统计局 |
Census of Population 2016 | 2016 年加拿大人口普查 |
Aboriginal | 原住民 | 加拿大统计局用语，与 Indigenous 同指
