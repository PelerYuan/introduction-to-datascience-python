```{code-cell} ipython3
:tags: [remove-cell]
from chapter_preamble import *
from IPython.display import HTML
from IPython.display import Image
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
```

(classification1)=
# 分类 I：训练与预测

## 概述
前面几章只讨论了描述性和探索性的数据分析问题。本章与下一章一起，是我们
第一次尝试回答关于数据的*预测性*问题。具体来说，我们关注*分类*，也就是
用一个或多个变量去预测我们关心的某个分类变量的取值。本章会介绍分类的
基础知识、如何预处理数据才能用于分类器，以及如何用观测到的数据做出预测。
下一章则讨论如何评估分类器给出的预测有多准确，以及如何（只要条件允许）
改进分类器以提高其准确率。

## 本章学习目标

学完本章后，你将能够：

- 识别适合用分类器做预测的情形。
- 说明什么是训练数据集，以及它在分类中如何使用。
- 解读分类器的输出。
- 当图上只有两个预测变量时，手算两点之间的直线距离（欧氏距离）。
- 解释 k 近邻（k-nearest neighbours）分类算法。
- 使用 `scikit-learn` 在 Python 中完成 k 近邻分类。
- 作为预处理步骤，用 `scikit-learn` 中的方法对数据做中心化、缩放、平衡和插补。
- 用 `make_pipeline` 把预处理与模型训练组合成一个 `Pipeline`。

+++

## 分类问题

```{index} 预测性问题, 分类, 类别, 分类变量
```

```{index} see: 特征 ; 预测变量
```

很多时候，我们希望依据当前的情况以及过去的经验做出预测。例如，医生可能
想根据病人的症状和自己以往诊治病人的经验，判断这位病人是患病还是健康；
邮件服务商可能想根据某封邮件的正文和以往的邮件文本数据，把它标记为
“垃圾邮件”或“非垃圾邮件”；信用卡公司则可能想根据当前消费的商品、金额、
地点以及以往的消费记录，预测某笔消费是否存在欺诈。这些任务都是**分类**的
例子：已知一条观测的其他变量（有时称为*特征*），预测它所属的类别
（有时称为*标签*）。

```{index} 训练集
```

一般来说，分类器会把一条类别未知的观测（例如一位新病人）归入某个类别
（例如患病或健康），依据是它与类别已知的其他观测（例如以往症状明确、
诊断已知的病人）有多相似。这些类别已知、被我们用作预测依据的观测称为
**训练集**；这个名字来自我们用这些数据来训练（也就是“教”）分类器这一事实。
教好之后，我们就可以用这个分类器，对类别未知的新数据做出预测。

```{index} k 近邻, 分类; 二分类
```

可以用来预测一条观测所属类别或标签的方法有很多。本书聚焦于应用广泛的
**k 近邻**算法 {cite:p}`knnfix,knncover`。在以后的学习中，你可能会遇到决策树、
支持向量机（SVM）、逻辑回归、神经网络等更多方法；这些方法该从哪里学起，
可以看下一章末尾的拓展资源一节。另外值得一提的是，基本分类问题还有许多
变体。例如，我们关注只涉及两个类别的**二分类（binary classification）**
情形（例如诊断为健康或患病），但你也可能遇到类别多于两个的多分类
（multiclass classification）问题（例如诊断为健康、支气管炎、肺炎或普通感冒）。

## 探索数据集

```{index} 乳腺癌, 问题; 分类
```

本章和下一章将研究一份
[数字化乳腺癌图像特征](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29)
数据集，它由 William H. Wolberg 博士、W. Nick Street 和 Olvi L. Mangasarian
创建 {cite:p}`streetbreastcancer`。数据集中的每一行代表一张肿瘤样本图像，
其中包含诊断结果（良性或恶性）以及若干其他测量值（细胞核纹理、周长、
面积等）。每张图像的诊断都由医生完成。

和所有数据分析一样，我们首先要精确地表述自己想回答的问题。这里的问题是
*预测性*的：能否用我们手头的肿瘤图像测量值，预测未来某张诊断未知的
肿瘤图像是良性还是恶性？回答这个问题很重要，因为传统的、非数据驱动的
肿瘤诊断方法相当主观，取决于诊断医生的技术水平和经验。此外，良性肿瘤
通常并不危险：细胞停留在原处，肿瘤在长得很大之前就停止生长。相比之下，
恶性肿瘤的细胞会侵入周围组织，扩散到邻近器官，造成严重损害
{cite:p}`stanfordhealthcare`。因此，快速而准确地判断肿瘤类型，对指导
患者治疗十分重要。

+++

### 读取癌症数据

第一步是读取、整理数据，并通过可视化探索数据，以便更好地理解手上的
这份数据。我们先载入分析所需的 `pandas` 和 `altair` 包。

```{code-cell} ipython3
import pandas as pd
import altair as alt
```

这里，存放乳腺癌数据集的文件是一个带表头的 `.csv` 文件。我们使用
`read_csv` 函数，不加任何其他参数，然后查看它的内容：

```{index} 读取函数; read_csv
```

```{code-cell} ipython3
:tags: ["output_scroll"]
cancer = pd.read_csv("data/wdbc.csv")
cancer
```

### 描述癌症数据集中的变量

乳腺肿瘤可以通过*活检*来诊断。活检是把组织从体内取出、检查其中是否有
病变的过程。传统上这类操作侵入性相当强；而现代方法，例如收集本数据集时
采用的细针穿刺，只取少量组织，侵入性较小。研究人员以本数据集收集的每份
乳腺组织样本的数字图像为依据，对图像中的每个细胞核测量了十个不同的变量
（即下面变量清单中的第 3 至 12 项），然后记录每个变量在所有细胞核上的
均值。作为数据准备的一部分，这些取值已经过*标准化（中心化和缩放）*
处理；它的含义以及我们为什么要这样做，本章后面会讨论。此外，每张图像
还有唯一编号，并带有医生的诊断结果。因此，本数据集中每张图像的变量
全集为：

1. ID：编号
2. Class：诊断结果（M = 恶性，B = 良性）
3. Radius：从中心到周界上各点距离的均值
4. Texture：灰度值的标准差
5. Perimeter：周围轮廓的长度
6. Area：轮廓内的面积
7. Smoothness：半径长度的局部变化
8. Compactness：周长平方与面积之比
9. Concavity：轮廓凹陷部分的严重程度
10. Concave Points：轮廓凹陷部分的数目
11. Symmetry：细胞核镜像后的相似程度
12. Fractal Dimension：周界“粗糙”程度的度量

+++

```{index} DataFrame; info
```

下面我们用 `info` 方法预览数据框（data frame）。当列数很多时，这个方法
能让查看数据更容易：它把列名纵向排列打印出来（而不是横向排列），同时
给出各列的数据类型和非缺失项的个数。

```{code-cell} ipython3
cancer.info()
```

```{index} Series; unique
```

从上面的数据摘要可以看到，`Class` 的类型是 `object`。我们可以对 `Class`
列使用 `unique` 方法，查看该列中出现的所有不同取值。可以看到，这里有两种
诊断结果：用 `"B"` 表示的良性，以及用 `"M"` 表示的恶性。

```{code-cell} ipython3
cancer["Class"].unique()
```

为了提高分析结果的可读性，我们用 `replace` 方法把 `"M"` 重命名为
`"Malignant"`、把 `"B"` 重命名为 `"Benign"`。`replace` 方法只接受一个
参数：一个把原取值映射到新取值的字典。我们再用 `unique` 方法验证结果。

```{index} Series; replace
```

```{code-cell} ipython3
cancer["Class"] = cancer["Class"].replace({
    "M" : "Malignant",
    "B" : "Benign"
})

cancer["Class"].unique()
```

### 探索癌症数据

```{index} DataFrame; groupby, Series;size
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("benign_count", "{:0.0f}".format(cancer["Class"].value_counts()["Benign"]))
glue("benign_pct", "{:0.0f}".format(100*cancer["Class"].value_counts(normalize=True)["Benign"]))
glue("malignant_count", "{:0.0f}".format(cancer["Class"].value_counts()["Malignant"]))
glue("malignant_pct", "{:0.0f}".format(100*cancer["Class"].value_counts(normalize=True)["Malignant"]))
```

在开始建模之前，我们先探索一下数据集。下面用 `groupby` 和 `size` 方法
统计数据集中良性肿瘤观测和恶性肿瘤观测的条数与百分比。`size` 与 `groupby`
搭配使用时，会统计 `Class` 变量每个取值对应的观测条数。然后我们把各组的
观测条数除以观测总数，再乘以 100，算出该组所占的百分比。观测总数等于
数据框的行数，可以通过数据框的 `shape` 属性获取（`shape[0]` 是行数，
`shape[1]` 是列数）。我们的数据中有
{glue:text}`benign_count`（{glue:text}`benign_pct`\%）条良性肿瘤观测和
{glue:text}`malignant_count`（{glue:text}`malignant_pct`\%）条恶性肿瘤观测。

```{code-cell} ipython3
100 * cancer.groupby("Class").size() / cancer.shape[0]
```

```{index} Series; value_counts
```

`pandas` 包还提供了更方便的专用方法 `value_counts`，用来统计一列中每个
取值出现的次数。不给它传参数时，它输出一个序列（series），其中包含每个
取值出现的次数；如果传入参数 `normalize=True`，它输出的则是每个取值出现的
比例。

```{code-cell} ipython3
cancer["Class"].value_counts()
```

```{code-cell} ipython3
cancer["Class"].value_counts(normalize=True)
```

```{index} 可视化; 散点图
```

接下来，我们画一张彩色散点图，展示周长（perimeter）与凹陷度（concavity）
这两个变量之间的关系。回想一下，`altair` 的默认配色方案对色盲友好，
所以这里沿用默认配色即可。

```{code-cell} ipython3
:tags: ["remove-output"]
perim_concav = alt.Chart(cancer).mark_circle().encode(
    x=alt.X("Perimeter").title("Perimeter (standardized)"),
    y=alt.Y("Concavity").title("Concavity (standardized)"),
    color=alt.Color("Class").title("Diagnosis")
)
perim_concav
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("fig:05-scatter", perim_concav)
```

:::{glue:figure} fig:05-scatter
:name: fig:05-scatter

凹陷度与周长的散点图，按诊断标签着色。
:::

+++

在 {numref}`fig:05-scatter` 中可以看到，恶性肿瘤观测通常落在绘图区的
右上角，而良性肿瘤观测通常落在绘图区的左下角。换句话说，良性肿瘤观测的
凹陷度和周长取值往往较小，恶性肿瘤观测的取值往往较大。假设我们拿到一条
不在当前数据集中的新观测，它的所有变量都已测得，*只有*标签未知（也就是
说，这是一张没有医生给出肿瘤类别诊断的图像）。我们可以算出它的标准化
周长和凹陷度，比如结果分别为 1 和 1。能否用这些信息把这条观测判为良性或
恶性？看这张散点图，你会怎样给这条新观测分类？如果标准化凹陷度和标准化
周长分别为 1 和 1，这个点会落在橙色恶性肿瘤点云的正中间，因此我们大概
可以把它判为恶性。从这张图来看，对于诊断未知的肿瘤图像，我们似乎有可能
准确预测 `Class` 变量（也就是诊断结果）。

+++

## 用 k 近邻做分类

```{code-cell} ipython3
:tags: [remove-cell]

new_point = [2, 4]
glue("new_point_1_0", "{:.1f}".format(new_point[0]))
glue("new_point_1_1", "{:.1f}".format(new_point[1]))
attrs = ["Perimeter", "Concavity"]
points_df = pd.DataFrame(
    {"Perimeter": new_point[0], "Concavity": new_point[1], "Class": ["Unknown"]}
)
perim_concav_with_new_point_df = pd.concat((cancer, points_df), ignore_index=True)
# Find the euclidean distances from the new point to each of the points
# in the orginal data set
my_distances = euclidean_distances(perim_concav_with_new_point_df[attrs])[
    len(cancer)
][:-1]
```

```{index} k 近邻; 分类
```

要在实践中真正对新观测做出预测，我们需要一个分类算法。本书使用 k 近邻
分类算法。为了预测一条新观测的标签（在这里，就是把它判为良性还是恶性），
k 近邻分类器一般会在训练集中找出 $K$ 条“最近”或“最相似”的观测，再根据
它们的诊断结果，为新观测的诊断做出预测。$K$ 是一个我们必须事先选定的数；
目前先假设 $K$ 已经由别人替我们选好。如何自己选择 $K$，我们会在下一章介绍。

为了说明 k 近邻分类的思路，我们来看一个例子。假设有一条新观测，标准化
周长为 {glue:text}`new_point_1_0`，标准化凹陷度为 {glue:text}`new_point_1_1`，
它的“Class”诊断未知。这条新观测在 {numref}`fig:05-knn-2` 中用红色菱形点表示。

```{code-cell} ipython3
:tags: [remove-cell]

perim_concav_with_new_point = (
    alt.Chart(perim_concav_with_new_point_df)
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Perimeter").title("Perimeter (standardized)"),
        y=alt.Y("Concavity").title("Concavity (standardized)"),
        color=alt.Color("Class").title("Diagnosis"),
        shape=alt.Shape("Class").scale(range=["circle", "circle", "diamond"]),
        size=alt.condition("datum.Class == 'Unknown'", alt.value(100), alt.value(30)),
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None)),
    )
)
glue('fig:05-knn-2', perim_concav_with_new_point, display=True)
```

:::{glue:figure} fig:05-knn-2
:name: fig:05-knn-2

凹陷度与周长的散点图，新观测用红色菱形表示。
:::

```{code-cell} ipython3
:tags: [remove-cell]

near_neighbor_df = pd.concat([
    cancer.loc[[np.argmin(my_distances)], attrs],
    perim_concav_with_new_point_df.loc[[cancer.shape[0]], attrs],
])
glue("1-neighbor_per", "{:.1f}".format(near_neighbor_df.iloc[0, :]["Perimeter"]))
glue("1-neighbor_con", "{:.1f}".format(near_neighbor_df.iloc[0, :]["Concavity"]))
```

{numref}`fig:05-knn-3` 显示，离这条新观测最近的是一条**恶性**观测，
位于坐标（{glue:text}`1-neighbor_per`，{glue:text}`1-neighbor_con`）。
这里的思路是：如果散点图中有两个点靠得很近，它们的周长和凹陷度取值就
相似，因此可以期望它们属于同一种诊断。

```{code-cell} ipython3
:tags: [remove-cell]

line = (
    alt.Chart(near_neighbor_df)
    .mark_line()
    .encode(x="Perimeter", y="Concavity", color=alt.value("black"))
)

glue('fig:05-knn-3', (perim_concav_with_new_point + line), display=True)
```

:::{glue:figure} fig:05-knn-3
:name: fig:05-knn-3

凹陷度与周长的散点图。新观测用红色菱形表示，并有一条线段连到它的一个
最近邻，该最近邻的标签是恶性。
:::

```{code-cell} ipython3
:tags: [remove-cell]

new_point = [0.2, 3.3]
attrs = ["Perimeter", "Concavity"]
points_df2 = pd.DataFrame(
    {"Perimeter": new_point[0], "Concavity": new_point[1], "Class": ["Unknown"]}
)
perim_concav_with_new_point_df2 = pd.concat((cancer, points_df2), ignore_index=True)
# Find the euclidean distances from the new point to each of the points
# in the orginal data set
my_distances2 = euclidean_distances(perim_concav_with_new_point_df2[attrs])[
    len(cancer)
][:-1]
glue("new_point_2_0", "{:.1f}".format(new_point[0]))
glue("new_point_2_1", "{:.1f}".format(new_point[1]))
```

```{code-cell} ipython3
:tags: [remove-cell]

perim_concav_with_new_point2 = (
    alt.Chart(
        perim_concav_with_new_point_df2,
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Perimeter", title="Perimeter (standardized)"),
        y=alt.Y("Concavity", title="Concavity (standardized)"),
        color=alt.Color(
            "Class",
            title="Diagnosis",
        ),
        shape=alt.Shape(
            "Class", scale=alt.Scale(range=["circle", "circle", "diamond"])
        ),
        size=alt.condition("datum.Class == 'Unknown'", alt.value(80), alt.value(30)),
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None)),
    )
)

near_neighbor_df2 = pd.concat([
    cancer.loc[[np.argmin(my_distances2)], attrs],
    perim_concav_with_new_point_df2.loc[[cancer.shape[0]], attrs],
])
line2 = alt.Chart(near_neighbor_df2).mark_line().encode(
    x="Perimeter",
    y="Concavity",
    color=alt.value("black")
)

glue("2-neighbor_per", "{:.1f}".format(near_neighbor_df2.iloc[0, :]["Perimeter"]))
glue("2-neighbor_con", "{:.1f}".format(near_neighbor_df2.iloc[0, :]["Concavity"]))
glue('fig:05-knn-4', (perim_concav_with_new_point2 + line2), display=True)
```

假设我们又有了一条新观测，标准化周长为 {glue:text}`new_point_2_0`，
凹陷度为 {glue:text}`new_point_2_1`。看 {numref}`fig:05-knn-4` 中的散点图，
你会把这条红色菱形观测判为哪一类？离这个新点最近的是一条位于
（{glue:text}`2-neighbor_per`，{glue:text}`2-neighbor_con`）的**良性**观测。
对这个观测来说，这个预测合适吗？如果再考虑附近的其他点，答案恐怕是否定的。
<<TERM>>
concavity = 凹陷度
perimeter = 周长
contour = 轮廓
tumor = 肿瘤
biopsy = 活检
fine needle aspiration = 细针穿刺
cell nucleus = 细胞核
radius = 半径
texture = 纹理
smoothness = 平滑度
compactness = 紧密度
symmetry = 对称性
fractal dimension = 分形维数
palette = 配色方案
<<END>>
