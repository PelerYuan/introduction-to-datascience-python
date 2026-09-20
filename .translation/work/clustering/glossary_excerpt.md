# 本章术语表（clustering）

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
list | 列表 | 首见加注（list）
dict | dict | [保留英文]
object (dtype) | object | [保留英文]；字符串列或混合类型列的 dtype
cell | 单元格 |
shape | 形状 | 指数据框的行数与列数
subgroup | 子组 | 分组结果内部更小的一组
pandas | pandas | [保留英文]
read_csv | read_csv | [保留英文]
sep | sep | [保留英文]；指定列分隔符的参数
names | names | [保留英文]；读取时直接指定列名的参数
drop | drop | [保留英文]；删除列或行
assign | assign | [保留英文]；返回添加或修改列之后的新数据框
groupby | groupby | [保留英文]
on | on | [保留英文]；merge 中指定用于匹配的列
head | head | [保留英文]
tail | tail | [保留英文]
info | info | [保留英文]；打印数据框的结构信息
describe | describe | [保留英文]；一次给出多个常用汇总统计量
count | 计数 | 统计量译"计数"；方法名 count 保留英文，altair 中的 count() 同样保留英文
axis=1 | axis=1 | [保留英文]；表示按行计算
position | 位置 | iloc[] 按位置、loc[] 按标签，两者需区分
altair | altair | [保留英文]
alt | alt | [保留英文]；altair 的常用别名
Chart | Chart | [保留英文]；altair 中的基本图形对象
alt.Chart | alt.Chart | [保留英文]
encode | encode | [保留英文]；把数据列映射到图形属性
mark_point | mark_point | [保留英文]；散点图的默认图形标记
mark_line | mark_line | [保留英文]
mark_circle | mark_circle | [保留英文]；填充圆点，不支持 shape 通道
mark_rule | mark_rule | [保留英文]；画水平或垂直参考线
alt.X | alt.X | [保留英文]
alt.Y | alt.Y | [保留英文]
alt.Color | alt.Color | [保留英文]
alt.datum | alt.datum | [保留英文]；表示单个数值，而不是数据框中的某一列
scale(zero=False) | scale(zero=False) | [保留英文]；坐标轴下界不必取 0
domain | 取值范围 | 与 range（极差）区分：标度语境中指坐标轴的上下界
opacity | 不透明度 | 代码 opacity=0.5 保留英文
reference | 引用 | ibis 返回的是表引用，数据仍留在数据库中
select (method) | select | [保留英文]；BeautifulSoup 的方法，按 CSS 选择器取出节点；与核心术语表的"选取（select）"区分
attribute | 属性 | 与图形属性（aesthetic）区分

## part_ml（本章相关条目）

data set | 数据集 |
data point | 数据点 |
measurement | 测量值 | 指对观测某个特征的量测结果
prediction error | 预测误差 |
model object | 模型对象 | 首见加注（model object）
test data | 测试数据 |
algorithm | 算法 |
assumption | 假设 | 指模型前提；与假设检验中的"原假设"不是一回事
trade-off | 权衡取舍 |
reproducible | 可复现的 | 修饰 analysis 时译"可复现的分析"
randomness | 随机性 |
underlying structure | 潜在结构 | 指数据中未被标注出来的分组结构
subgroup | 子组 |
pattern | 模式 |
labeled data | 有标签数据 |
unlabeled data | 无标签数据 |
preprocessor | 预处理器 | 首见加注（preprocessor）
center | 中心 | 名词，指变量的中心位置
quantitative variable | 定量变量 |
categorical variable | 分类变量 | 与 categorical（类别型）同义，正文两词都出现
supervised task | 有监督任务 |
unsupervised task | 无监督任务 |
distance | 距离 |
straight-line distance | 直线距离 | 首见加注（straight-line distance）
Euclidean distance | 欧氏距离 | 首见加注（Euclidean distance）
influence | 影响 | 指单个数据点对拟合直线的拉动程度
cluster | 簇 | 首见加注（cluster）；与 clustering（聚类）区分，前者指一个分组，后者指方法或结果
clustering algorithm | 聚类算法 |
cluster center | 簇中心 | 代码中的变量名写作 centroid
centroid | 质心 | 与 cluster center 同义；代码变量名 centroid 保留英文
cluster label | 簇标签 |
cluster assignment | 簇归属 | 正文亦称 assignment，指数据点被分到哪个簇
initial centers | 初始中心 |
random initialization | 随机初始化 |
random restart | 随机重启 | 本书小节标题 Random restarts
bad solution | 劣质解 | 原文指 k 均值因初始化不佳而"卡住"的较差结果
center update | 中心更新 | k 均值算法两步之一
label update | 标签更新 | k 均值算法两步之一
WSSD | 簇内平方距离和 | 缩写 WSSD 保留英文；全称 within-cluster sum-of-squared-distances
within-cluster sum-of-squared-distances | 簇内平方距离和 | 首见加注（within-cluster sum-of-squared-distances）
total WSSD | 总 WSSD | 所有簇的 WSSD 之和，k 均值的目标即最小化该量；图中亦称 total within-cluster sum of squares
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
performance | 性能 |
baseline | 基准 | 指便于比较的简单方法，如多数类分类器
number of predictors | 预测变量个数 |
scikit-learn | scikit-learn | [保留英文]；在 Python 中导入名为 sklearn
KMeans | KMeans | [保留英文]
make_pipeline | make_pipeline | [保留英文]
make_column_transformer | make_column_transformer | [保留英文]
StandardScaler | StandardScaler | [保留英文]
set_config | set_config | [保留英文]；其参数 transform_output 亦保留英文
transform | 变换 | 方法名 transform 保留英文；与 fit 配对使用
labels_ | labels_ | [保留英文]
inertia_ | inertia_ | [保留英文]
n_clusters | n_clusters | [保留英文]
n_init | n_init | [保留英文]
euclidean_distances | euclidean_distances | [保留英文]
verbose_feature_names_out | verbose_feature_names_out | [保留英文]

## part_tools（本章相关条目）

spread | 离散程度 | 备选：波动程度
quantitative | 定量的 | 与 categorical 相对；备选：数值型
case | 研究个体 | 与核心表 case study（案例分析）区分
restart | 重启 |
list comprehension | 列表推导式 | 首见加注（list comprehension）
tag | 标签 | Docker 镜像版本标签
pip | pip | [保留英文]
changed | 已修改 | Jupyter Git 面板分组名
add | 添加 | 指把文件加入暂存区，与 GitHub 的 Add file 菜单区分
PAT | PAT | [保留英文]
worksheet | 练习册 | 指配套的 Jupyter 笔记本习题文件，首见加注（worksheet）
worksheets repository | 练习册仓库 |
exercise | 习题 | 章节小节名 Exercises 译"习题"
non-interactive version | 非交互版本 |
automated feedback | 自动反馈 |
MIT | 麻省理工学院 | 正文可写"麻省理工学院（MIT）"
