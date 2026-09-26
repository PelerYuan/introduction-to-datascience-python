---
jupytext:
  formats: py:percent,md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

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
前面几章只讨论了描述性和探索性的数据分析问题。本章与下一章一起，是我们第一次尝试回答关于数据的*预测性*问题（predictive question）。具体来说，我们关注*分类*（classification），也就是用一个或多个变量去预测我们关心的某个类别型变量的取值。本章会介绍分类的基础知识、如何预处理数据才能用于分类器，以及如何用观测到的数据做出预测。下一章则讨论如何评估分类器给出的预测有多准确，以及如何（只要条件允许）改进分类器，把准确率提到最高。

## 本章学习目标

学完本章后，你将能够：

- 识别适合用分类器做预测的情形。
- 说明什么是训练数据集，以及它在分类中如何使用。
- 解读分类器的输出。
- 当图上只有两个预测变量时，手算两点之间的直线距离（欧氏距离）。
- 解释 K 近邻（k-nearest neighbours）分类算法。
- 使用 `scikit-learn` 在 Python 中完成 K 近邻分类。
- 作为预处理步骤，用 `scikit-learn` 中的方法对数据做中心化、缩放、平衡和插补。
- 用 `make_pipeline` 把预处理与模型训练组合成一个 `Pipeline`。

+++

## 分类问题

```{index} 预测性问题, 分类, 类别, 类别型变量
```

```{index} see: 特征 ; 预测变量
```

很多时候，我们希望依据当前的情况以及过去的经验做出预测。例如，医生可能想根据病人的症状和自己以往诊治病人的经验，判断这位病人是患病还是健康；邮件服务商可能想根据某封邮件的正文和以往的邮件文本数据，把它标记为“垃圾邮件”或“非垃圾邮件”；信用卡公司则可能想根据当前消费的商品、金额、地点以及以往的消费记录，预测某笔消费是否存在欺诈。这些任务都是**分类**的例子：已知一条观测的其他变量（有时称为*特征*，feature），预测它所属的类别（有时称为*标签*，label）。

```{index} 训练集
```

一般来说，分类器会把一条类别未知的观测（例如一位新病人）归入某个类别（例如患病或健康），依据是它与类别已知的其他观测（例如以往症状明确、诊断已知的病人）有多相似。这些类别已知、被我们用作预测依据的观测称为**训练集**（training set）；这个名字来自我们用这些数据来训练（也就是“教”）分类器这一事实。教好之后，我们就可以用这个分类器，对类别未知的新数据做出预测。

```{index} K 近邻, 分类; 二分类
```

可以用来预测一条观测所属类别或标签的方法有很多。本书聚焦于应用广泛的
**K 近邻**算法 {cite:p}`knnfix,knncover`。在以后的学习中，你可能会遇到决策树、支持向量机（SVM）、逻辑回归、神经网络等更多方法；这些方法该从哪里学起，可以看下一章末尾的拓展资源一节。另外值得一提的是，基本分类问题还有许多变体。例如，我们关注只涉及两个类别的**二分类**（binary classification）情形（例如诊断为健康或患病），但你也可能遇到类别多于两个的多分类（multiclass classification）问题（例如诊断为健康、支气管炎、肺炎或普通感冒）。

## 探索数据集

```{index} 乳腺癌, 问题; 分类
```

本章和下一章将研究一份[数字化乳腺癌图像特征](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29)数据集，它由 William H. Wolberg 博士、W. Nick Street 和 Olvi L. Mangasarian
创建 {cite:p}`streetbreastcancer`。数据集中的每一行代表一张肿瘤样本图像，其中包含诊断结果（良性或恶性）以及若干其他测量值（细胞核纹理、周长、面积等）。每张图像的诊断都由医生完成。

和所有数据分析一样，我们首先要精确地表述自己想回答的问题。这里的问题是*预测性*的：能否用我们手头的肿瘤图像测量值，预测未来某张诊断未知的肿瘤图像是良性还是恶性？回答这个问题很重要，因为传统的、非数据驱动的肿瘤诊断方法相当主观，取决于诊断医生的技术水平和经验。此外，良性肿瘤通常并不危险：细胞停留在原处，肿瘤在长得很大之前就停止生长。相比之下，恶性肿瘤的细胞会侵入周围组织，扩散到邻近器官，造成严重损害
{cite:p}`stanfordhealthcare`。因此，快速而准确地判断肿瘤类型，对指导患者治疗十分重要。

+++

### 读取癌症数据

第一步是读取、整理数据，并通过可视化探索数据，以便更好地理解手上的这份数据。我们先载入分析所需的 `pandas` 和 `altair` 包。

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

乳腺肿瘤可以通过*活检*（biopsy）来诊断。活检是把组织从体内取出、检查其中是否有病变的过程。传统上这类操作侵入性相当强；而现代方法，例如收集本数据集时采用的细针穿刺（fine needle aspiration），只取少量组织，侵入性较小。研究人员以本数据集收集的每份乳腺组织样本的数字图像为依据，对图像中的每个细胞核测量了十个不同的变量（即下面变量清单中的第 3 至 12 项），然后记录每个变量在所有细胞核上的均值。作为数据准备的一部分，这些取值已经过*标准化*（standardized，中心化和缩放）处理；它的含义以及我们为什么要这样做，本章后面会讨论。此外，每张图像还有唯一编号，并带有医生的诊断结果。因此，本数据集中每张图像的变量全集为：

1. ID：编号
2. Class：诊断结果（M = 恶性，B = 良性）
3. Radius（半径）：从中心到周界上各点距离的均值
4. Texture（纹理）：灰度值的标准差
5. Perimeter（周长）：周围轮廓的长度
6. Area（面积）：轮廓内的面积
7. Smoothness（光滑度）：半径长度的局部变化
8. Compactness（紧密度）：周长平方与面积之比
9. Concavity（凹度）：轮廓凹陷部分的严重程度
10. Concave Points（凹点）：轮廓凹陷部分的数目
11. Symmetry（对称性）：细胞核镜像后的相似程度
12. Fractal Dimension（分形维数）：周界“粗糙”程度的度量

+++

```{index} DataFrame; info
```

下面我们用 `info` 方法预览数据框（data frame）。当列数很多时，用这个方法查看数据会更容易：它把列名纵向排列打印出来（而不是横向排列），同时给出各列的数据类型和非缺失项的个数。

```{code-cell} ipython3
cancer.info()
```

```{index} Series; unique
```

从上面的数据摘要可以看到，`Class` 的类型是 `object`。我们可以对 `Class`
列使用 `unique` 方法，查看该列中出现的所有不同取值。可以看到，这里有两种诊断结果：用 `"B"` 表示的良性，以及用 `"M"` 表示的恶性。

```{code-cell} ipython3
cancer["Class"].unique()
```

为了提高分析结果的可读性，我们用 `replace` 方法把 `"M"` 重命名为
`"Malignant"`、把 `"B"` 重命名为 `"Benign"`。`replace` 方法只接受一个参数：一个把原取值映射到新取值的字典。我们再用 `unique` 方法验证结果。

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

在开始建模之前，我们先探索一下数据集。下面用 `groupby` 和 `size` 方法统计数据集中良性肿瘤观测和恶性肿瘤观测的条数与百分比。`size` 与 `groupby`
搭配使用时，会统计 `Class` 变量每个取值对应的观测条数。然后我们把各组的观测条数除以观测总数，再乘以 100，算出该组所占的百分比。观测总数等于数据框的行数，可以通过数据框的 `shape` 属性获取（`shape[0]` 是行数，`shape[1]` 是列数）。我们的数据中有
{glue:text}`benign_count`（{glue:text}`benign_pct`\%）条良性肿瘤观测和
{glue:text}`malignant_count`（{glue:text}`malignant_pct`\%）条恶性肿瘤观测。

```{code-cell} ipython3
100 * cancer.groupby("Class").size() / cancer.shape[0]
```

```{index} Series; value_counts
```

`pandas` 包还提供了更方便的专用方法 `value_counts`，用来统计一列中每个取值出现的次数。不给它传参数时，它输出一个 Series（序列），其中包含每个取值出现的次数；如果传入参数 `normalize=True`，它输出的则是每个取值出现的比例。

```{code-cell} ipython3
cancer["Class"].value_counts()
```

```{code-cell} ipython3
cancer["Class"].value_counts(normalize=True)
```

```{index} 可视化; 散点图
```

接下来，我们画一张彩色散点图，展示周长与凹度这两个变量之间的关系。回想一下，`altair` 的默认配色方案对色盲友好，所以这里沿用默认配色即可。

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

凹度与周长的散点图，按诊断标签着色。
:::

+++

在{numref}`fig:05-scatter` 中可以看到，恶性肿瘤观测通常落在绘图区的右上角，而良性肿瘤观测通常落在绘图区的左下角。换句话说，良性肿瘤观测的凹度和周长取值往往较小，恶性肿瘤观测的取值往往较大。假设我们拿到一条不在当前数据集中的新观测，它的所有变量都已测得，*只有*标签未知（也就是说，这是一张没有医生给出肿瘤类别诊断的图像）。我们可以算出它的标准化周长和凹度，比如结果分别为 1 和 1。能否用这些信息把这条观测判为良性或恶性？看这张散点图，你会怎样给这条新观测分类？如果标准化凹度和标准化周长分别为 1 和 1，这个点会落在橙色恶性肿瘤点云的正中间，因此我们大概可以把它判为恶性。从这张图来看，对于诊断未知的肿瘤图像，我们似乎有可能准确预测 `Class` 变量（也就是诊断结果）。

+++

## 用 K 近邻做分类

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

```{index} K 近邻; 分类
```

要在实践中真正对新观测做出预测，我们需要一个分类算法。本书使用 K 近邻分类算法。为了预测一条新观测的标签（在这里，就是把它判为良性还是恶性），K 近邻分类器一般会在训练集中找出 $K$ 条“最近”或“最相似”的观测，再根据它们的诊断结果，为新观测的诊断做出预测。$K$ 是一个我们必须事先选定的数；目前先假设 $K$ 已经由别人替我们选好。如何自己选择 $K$，我们会在下一章介绍。

为了说明 K 近邻分类的思路，我们来看一个例子。假设有一条新观测，标准化周长为 {glue:text}`new_point_1_0`，标准化凹度为 {glue:text}`new_point_1_1`，它的“Class”诊断未知。这条新观测在{numref}`fig:05-knn-2` 中用红色菱形点表示。

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

凹度与周长的散点图，新观测用红色菱形表示。
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

{numref}`fig:05-knn-3` 显示，离这条新观测最近的是一条**恶性**观测，位于坐标（{glue:text}`1-neighbor_per`，{glue:text}`1-neighbor_con`）。这里的思路是：如果散点图中有两个点靠得很近，它们的周长和凹度取值就相似，因此可以期望它们属于同一种诊断。

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

凹度与周长的散点图。新观测用红色菱形表示，并有一条线段连到离它最近的那一个近邻，该最近邻的标签是恶性。
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

假设我们又有了一条新观测，标准化周长为 {glue:text}`new_point_2_0`，凹度为 {glue:text}`new_point_2_1`。看{numref}`fig:05-knn-4` 中的散点图，你会把这条红色菱形观测判为哪一类？离这个新点最近的是一条位于（{glue:text}`2-neighbor_per`，{glue:text}`2-neighbor_con`）的**良性**观测。对这个观测来说，这个预测合适吗？如果再考虑附近的其他点，答案恐怕是否定的。

+++

:::{glue:figure} fig:05-knn-4
:name: fig:05-knn-4

凹度与周长的散点图。新观测用红色菱形表示，并有一条连线连到离它最近的那一个近邻，该近邻的标签为良性。
:::

```{code-cell} ipython3
:tags: [remove-cell]

# The index of 3 rows that has smallest distance to the new point
min_3_idx = np.argpartition(my_distances2, 3)[:3]
near_neighbor_df3 = pd.concat([
    cancer.loc[[min_3_idx[1]], attrs],
    perim_concav_with_new_point_df2.loc[[cancer.shape[0]], attrs],
])
near_neighbor_df4 = pd.concat([
    cancer.loc[[min_3_idx[2]], attrs],
    perim_concav_with_new_point_df2.loc[[cancer.shape[0]], attrs],
])
```


```{code-cell} ipython3
:tags: [remove-cell]

line3 = alt.Chart(near_neighbor_df3).mark_line().encode(
    x="Perimeter",
    y="Concavity",
    color=alt.value("black")
)
line4 = alt.Chart(near_neighbor_df4).mark_line().encode(
    x="Perimeter",
    y="Concavity",
    color=alt.value("black")
)
glue("fig:05-knn-5", (perim_concav_with_new_point2 + line2 + line3 + line4), display=True)
```


为了提高预测效果，我们可以考虑离新观测最近的若干个邻点，比如取 $K = 3$，用它们来预测新观测的诊断类别。在这 3 个最近的邻点中，我们取*多数类*（majority class）作为新观测的预测结果。如{numref}`fig:05-knn-5` 所示，新观测的 3 个最近邻中有 2 个的诊断结果是恶性。因此我们采用多数投票，把这个新的红色菱形观测判为恶性。

+++

:::{glue:figure} fig:05-knn-5
:name: fig:05-knn-5

带三个最近邻的凹度与周长散点图。
:::

+++

这里我们选的是最近的 $K=3$ 个观测，但 $K=3$ 并没有什么特别之处。我们也可以用 $K=4, 5$ 或更多（不过为了避免平局，最好选奇数）。关于如何选择 $K$，我们会在下一章进一步讨论。

+++

### 点与点之间的距离

```{index} 距离; K 近邻, 直线; 距离
```

我们依据*直线距离*（straight-line distance）——它也叫*欧氏距离*（Euclidean distance）——判断哪些点是新观测的 $K$ 个“最近”邻点（后文常直接简称为*距离*）。假设有两个观测 $a$ 和 $b$，各自都有两个预测变量 $x$ 和 $y$。记 $a_x$ 和 $a_y$ 为观测 $a$ 在变量 $x$ 和 $y$ 上的取值；$b_x$ 和 $b_y$ 的含义与观测 $b$ 类似。那么观测 $a$ 与 $b$ 在 x-y 平面上的直线距离可以用下面的公式计算：

$$\mathrm{Distance} = \sqrt{(a_x -b_x)^2 + (a_y - b_y)^2}$$

+++

要找出新观测的 $K$ 个最近邻，我们先计算新观测到训练数据中每个观测的距离，再选出与 $K$ 个*最小*距离取值相对应的 $K$ 个观测。例如，假设我们要用 $K=5$ 个近邻来判断一个新观测的类别，它的周长为 {glue:text}`3-new_point_0`，凹度为 {glue:text}`3-new_point_1`，在{numref}`fig:05-multiknn-1` 中用红色菱形表示。下面我们计算新点与训练集中每个观测的距离，找出离新点最近的 $K=5$ 个近邻。在下面的代码中你会看到，我们按上面的公式计算直线距离：先把两个观测的周长之差与凹度之差分别平方，再把两个平方结果相加，最后开平方。为了找出 $K=5$ 个最近邻，我们使用 `pandas` 中的 `nsmallest` 函数。

```{index} nsmallest
```

```{code-cell} ipython3
:tags: [remove-cell]

new_point = [0, 3.5]
attrs = ["Perimeter", "Concavity"]
points_df3 = pd.DataFrame(
    {"Perimeter": new_point[0], "Concavity": new_point[1], "Class": ["Unknown"]}
)
perim_concav_with_new_point_df3 = pd.concat((cancer, points_df3), ignore_index=True)
perim_concav_with_new_point3 = (
    alt.Chart(
        perim_concav_with_new_point_df3,
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

glue("3-new_point_0", "{:.1f}".format(new_point[0]))
glue("3-new_point_1", "{:.1f}".format(new_point[1]))
glue("fig:05-multiknn-1", perim_concav_with_new_point3)
```


:::{glue:figure} fig:05-multiknn-1
:name: fig:05-multiknn-1

凹度与周长的散点图，其中新观测用红色菱形表示。
:::


```{code-cell} ipython3
new_obs_Perimeter = 0
new_obs_Concavity = 3.5
cancer["dist_from_new"] = (
       (cancer["Perimeter"] - new_obs_Perimeter) ** 2
     + (cancer["Concavity"] - new_obs_Concavity) ** 2
)**(1/2)
cancer.nsmallest(5, "dist_from_new")[[
    "Perimeter",
    "Concavity",
    "Class",
    "dist_from_new"
]]
```


```{code-cell} ipython3
:tags: [remove-cell]
# code needed to render the latex table with distance calculations
from IPython.display import Latex
five_neighbors = (
    cancer
   [["Perimeter", "Concavity", "Class"]]
   .assign(dist_from_new = (
       (cancer["Perimeter"] - new_obs_Perimeter) ** 2
     + (cancer["Concavity"] - new_obs_Concavity) ** 2
   )**(1/2))
   .nsmallest(5, "dist_from_new")
).reset_index()

for i in range(5):
    glue(f"gn{i}_perim", "{:0.2f}".format(five_neighbors["Perimeter"][i]))
    glue(f"gn{i}_concav", "{:0.2f}".format(five_neighbors["Concavity"][i]))
    glue(f"gn{i}_class", five_neighbors["Class"][i])

    # typeset perimeter,concavity with parentheses if negative for latex
    nperim = f"{five_neighbors['Perimeter'][i]:.2f}" if five_neighbors['Perimeter'][i] > 0 else f"({five_neighbors['Perimeter'][i]:.2f})"
    nconcav = f"{five_neighbors['Concavity'][i]:.2f}" if five_neighbors['Concavity'][i] > 0 else f"({five_neighbors['Concavity'][i]:.2f})"

    glue(f"gdisteqn{i}", Latex(f"\sqrt{{(0-{nperim})^2+(3.5-{nconcav})^2}}={five_neighbors['dist_from_new'][i]:.2f}"))
```


{numref}`tab:05-multiknn-mathtable` 用数学细节展示了我们如何为训练数据中 5 个最近邻逐一计算 `dist_from_new` 变量（即到新观测的距离）。

```{table} 评估新观测到其 5 个最近邻的距离
:name: tab:05-multiknn-mathtable
| Perimeter | Concavity | Distance            | Class |
|-----------|-----------|----------------------------------------|-------|
| {glue:text}`gn0_perim`  | {glue:text}`gn0_concav`  | {glue:}`gdisteqn0` | {glue:text}`gn0_class`     |
| {glue:text}`gn1_perim`  | {glue:text}`gn1_concav`  | {glue:}`gdisteqn1` | {glue:text}`gn1_class`     |
| {glue:text}`gn2_perim`  | {glue:text}`gn2_concav`  | {glue:}`gdisteqn2` | {glue:text}`gn2_class`     |
| {glue:text}`gn3_perim`  | {glue:text}`gn3_concav`  | {glue:}`gdisteqn3` | {glue:text}`gn3_class`     |
| {glue:text}`gn4_perim`  | {glue:text}`gn4_concav`  | {glue:}`gdisteqn4` | {glue:text}`gn4_class`     |
```

+++

计算结果表明，新观测的 5 个最近邻中有 3 个是恶性；既然恶性占多数，我们就把新观测判为恶性。这 5 个近邻在{numref}`fig:05-multiknn-3` 中用圆圈标出。

```{code-cell} ipython3
:tags: [remove-cell]

circle_path_df = pd.DataFrame(
    {
        "Perimeter": new_point[0] + 1.4 * np.cos(np.linspace(0, 2 * np.pi, 100)),
        "Concavity": new_point[1] + 1.4 * np.sin(np.linspace(0, 2 * np.pi, 100)),
    }
)
circle = alt.Chart(circle_path_df.reset_index()).mark_line(color="black").encode(
    x="Perimeter",
    y="Concavity",
    order="index"
)

glue("fig:05-multiknn-3", (perim_concav_with_new_point3 + circle))
```


:::{glue:figure} fig:05-multiknn-3
:name: fig:05-multiknn-3

凹度与周长的散点图，其中 5 个最近邻用圆圈标出。
:::

+++

### 多于两个预测变量

上面的介绍针对的是两个预测变量，但预测变量更多时，完全相同的 K 近邻算法同样适用。每个预测变量都可能提供新信息，帮助我们建立分类器。唯一的区别在于点与点之间的距离公式。假设两个观测 $a$ 和 $b$ 各有 $m$ 个预测变量，即 $a = (a_{1}, a_{2}, \dots, a_{m})$ 和 $b = (b_{1}, b_{2}, \dots, b_{m})$。

```{index} 距离; 多于两个变量
```

距离公式变为

$$\mathrm{Distance} = \sqrt{(a_{1} -b_{1})^2 + (a_{2} - b_{2})^2 + \dots + (a_{m} - b_{m})^2}.$$

这个公式仍然对应直线距离，只不过是在维数更多的空间里。假设我们要计算新观测与另一个观测之间的距离：新观测的周长为 0、凹度为 3.5、对称性为 1，另一个观测的周长、凹度和对称性分别为 0.417、2.31 和 0.837。这两个观测都有三个预测变量：周长、凹度和对称性。前面只有两个变量时，我们把（两个）变量各自之差的平方相加，再开平方。现在做法相同，只是变量换成了三个。距离的计算如下

$$\mathrm{Distance} =\sqrt{(0 - 0.417)^2 + (3.5 - 2.31)^2 + (1 - 0.837)^2} = 1.27.$$

下面我们计算新观测与训练集中每个观测的距离，找出在这三个预测变量下离新观测最近的 $K=5$ 个近邻。

```{code-cell} ipython3
new_obs_Perimeter = 0
new_obs_Concavity = 3.5
new_obs_Symmetry = 1
cancer["dist_from_new"] = (
      (cancer["Perimeter"] - new_obs_Perimeter) ** 2
    + (cancer["Concavity"] - new_obs_Concavity) ** 2
    + (cancer["Symmetry"] - new_obs_Symmetry) ** 2
)**(1/2)
cancer.nsmallest(5, "dist_from_new")[[
    "Perimeter",
    "Concavity",
    "Symmetry",
    "Class",
    "dist_from_new"
]]
```


在这三个预测变量下，$K=5$ 个最近邻中有 4 个属于恶性类别，因此我们会把新观测判为恶性。{numref}`fig:05-more` 展示了把这些数据画成三维散点图、并从新观测连向五个最近邻时的样子。

```{code-cell} ipython3
:tags: [remove-cell]

new_point = [0, 3.5, 1]
attrs = ["Perimeter", "Concavity", "Symmetry"]
points_df4 = pd.DataFrame(
    {
        "Perimeter": new_point[0],
        "Concavity": new_point[1],
        "Symmetry": new_point[2],
        "Class": ["Unknown"],
    }
)
perim_concav_with_new_point_df4 = pd.concat((cancer, points_df4), ignore_index=True)
# Find the euclidean distances from the new point to each of the points
# in the orginal data set
my_distances4 = euclidean_distances(perim_concav_with_new_point_df4[attrs])[
    len(cancer)
][:-1]
```


```{code-cell} ipython3
:tags: [remove-cell]

# The index of 5 rows that has smallest distance to the new point
min_5_idx = np.argpartition(my_distances4, 5)[:5]

neighbor_df_list = []
for idx in min_5_idx:
    neighbor_df = pd.concat(
        (
            cancer.loc[idx, attrs + ["Class"]],
            perim_concav_with_new_point_df4.loc[len(cancer), attrs + ["Class"]],
        ),
        axis=1,
    ).T
    neighbor_df_list.append(neighbor_df)
```


```{code-cell} ipython3
:tags: [remove-input]

fig = px.scatter_3d(
    perim_concav_with_new_point_df4,
    x="Perimeter",
    y="Concavity",
    z="Symmetry",
    color="Class",
    symbol="Class",
    opacity=0.5,
)
# specify trace names and symbols in a dict
symbols = {"Malignant": "circle", "Benign": "circle", "Unknown": "diamond"}

# set all symbols in fig
for i, d in enumerate(fig.data):
    fig.data[i].marker.symbol = symbols[fig.data[i].name]

# specify trace names and colors in a dict
colors = {"Malignant": "#ff7f0e", "Benign": "#1f77b4", "Unknown": "red"}

# set all colors in fig
for i, d in enumerate(fig.data):
    fig.data[i].marker.color = colors[fig.data[i].name]

# set a fixed custom marker size
fig.update_traces(marker={"size": 5})

# add lines
for neighbor_df in neighbor_df_list:
    fig.add_trace(
        go.Scatter3d(
            x=neighbor_df["Perimeter"],
            y=neighbor_df["Concavity"],
            z=neighbor_df["Symmetry"],
            line_color=colors[neighbor_df.iloc[0]["Class"]],
            name=neighbor_df.iloc[0]["Class"],
            mode="lines",
            line=dict(width=2),
            showlegend=False,
        )
    )


# tight layout
fig.update_layout(margin=dict(l=0, r=0, b=0, t=1), template="plotly_white")

# if HTML, use the plotly 3d image; if PDF, use static image
if "BOOK_BUILD_TYPE" in os.environ and os.environ["BOOK_BUILD_TYPE"] == "PDF":
    glue("fig:05-more", Image("img/classification1/plot3d_knn_classification.png"))
else:
    glue("fig:05-more", fig)
```


```{figure} data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
:name: fig:05-more
:figclass: caption-hack

标准化后的对称性、凹度和周长变量的三维散点图。请注意，一般情况下我们并不建议使用三维可视化；这里以三维方式展示数据，只是为了说明高维空间与最近邻是什么样子，供学习之用。
```

+++

### K 近邻算法小结

要用 K 近邻分类器判断一个新观测的类别，需要完成以下步骤：

1. 计算新观测与训练集中每个观测之间的距离。
2. 找出与 $K$ 个最小距离相对应的 $K$ 行。
3. 根据各近邻类别的多数投票，判定新观测的类别。

+++

## 用 `scikit-learn` 实现 K 近邻

```{index} scikit-learn
```

自己动手用 Python 编写 K 近邻算法会变得相当复杂，尤其是在还想处理多个类别、两个以上的变量，或者要为多个新观测预测类别时。好在 Python 里的
[`scikit-learn` Python 包](https://scikit-learn.org/stable/index.html) {cite:p}`sklearn_api`
已经实现了 K 近邻算法，这个包还提供了许多[其他模型](https://scikit-learn.org/stable/user_guide.html)，你在本章和本书后续各章都会遇到。使用 `scikit-learn` 包（在 Python 中名为 `sklearn`）里的函数，能让代码更简单、更易读、也更准确；我们自己要写的代码越少，犯的错误通常也越少。开始使用 K 近邻之前，需要先用 `set_config` 函数告诉 `sklearn` 包：我们希望使用 `pandas` 数据框，而不是普通的数组。
```{note}
你会发现下面代码里有一种新的函数导入写法：`from ... import ...`。这样我们就能从 `sklearn` 中*只*导入 `set_config`，之后调用 `set_config` 时也不必写包名前缀。本章和后续各章会大量使用 `from`
来导入函数，免得 `scikit-learn` 那些很长的名字把代码弄得杂乱不堪（比如 `sklearn.neighbors.KNeighborsClassifier`，足足有 38 个字符！）。
```

```{code-cell} ipython3
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")
```

现在可以开始使用 K 近邻了。第一步是从 `sklearn.neighbors` 模块导入 `KNeighborsClassifier`。

```{code-cell} ipython3
from sklearn.neighbors import KNeighborsClassifier
```

下面我们来看看如何用 `KNeighborsClassifier` 完成 K 近邻分类。我们沿用前面的 `cancer` 数据集，以周长和凹度作为预测变量、取 $K = 5$ 个近邻来构建分类器。然后用这个分类器预测一个新观测的诊断标签：该观测的周长为 0、凹度为 3.5，诊断标签未知。我们先选出需要的两个预测变量和类别标签，存成 `cancer_train`：

```{code-cell} ipython3
cancer_train = cancer[["Class", "Perimeter", "Concavity"]]
cancer_train
```

```{index} scikit-learn; 模型对象, scikit-learn; KNeighborsClassifier
```

接下来，我们创建一个 `KNeighborsClassifier` 实例，得到用于 K 近邻分类的*模型对象*（model object），并指定使用 $K = 5$ 个近邻；如何选择 $K$ 留到下一章讨论。

```{note}
你可以指定 `weights` 参数，来控制分类新观测时近邻如何投票。默认取值是 `"uniform"`，也就是前面说的：$K$ 个最近邻每个各投 1 票。其他取值会让每个近邻的投票权重有所不同，具体见
[`scikit-learn` 网站](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html?highlight=kneighborsclassifier#sklearn.neighbors.KNeighborsClassifier)。
```

```{code-cell} ipython3
knn = KNeighborsClassifier(n_neighbors=5)
knn
```

```{index} scikit-learn; fit, scikit-learn; 预测变量, scikit-learn; 响应变量
```

要在乳腺癌数据上拟合模型，需要调用模型对象的 `fit` 方法。`X` 参数用来指定预测变量的数据，`y` 参数用来指定响应变量的数据。所以下面我们设置 `X=cancer_train[["Perimeter", "Concavity"]]` 和
`y=cancer_train["Class"]`，表示 `Class` 是响应变量（也就是我们要预测的变量），而 `Perimeter` 和
`Concavity` 都作为预测变量。注意，`fit` 函数从外面看似乎没做什么，实际上训练 K 近邻模型的苦活累活全是它干的，它还会修改 `knn` 模型对象。

```{code-cell} ipython3
knn.fit(X=cancer_train[["Perimeter", "Concavity"]], y=cancer_train["Class"]);
```

```{index} scikit-learn; predict
```

用过 `fit` 函数之后，只要把新观测本身传给分类器对象并调用 `predict`，就能对它做出预测。和前面手工运行 K 近邻分类算法一样，`knn` 模型对象把这个新观测判为“Malignant”。注意，`predict` 函数输出的是装着模型预测结果的 `array`；你其实可以用 `predict` 一次预测多个观测，输出之所以存成 `array` 就是这个原因。

```{code-cell} ipython3
new_obs = pd.DataFrame({"Perimeter": [0], "Concavity": [3.5]})
knn.predict(new_obs)
```

这个预测出的恶性肿瘤标签，是这个观测的真实类别吗？我们并不知道，因为这个观测的诊断结果我们根本没有——我们要预测的正是它！分类器的预测不一定正确，但下一章我们会学习一些方法，来量化我们认为自己的预测有多准确。

+++

## 用 `scikit-learn` 做数据预处理

### 中心化与缩放

```{index} 缩放
```

使用 K 近邻分类时，每个变量的*标度*（即取值的大小与范围）都起作用。分类器靠找出离新观测最近的观测来判定类别，所以标度大的变量，影响会远大于标度小的变量。但变量标度大，*并不意味着*它对做出准确预测更重要。举个例子，假设有个数据集包含两个特征：工资（以美元计）和受教育年限，你想预测相应的工作类型。计算近邻距离时，1000 美元的差别与 10 年受教育年限的差别相比要大得多。但就理解问题、回答问题的需要而言，情况恰恰相反：与年薪相差 1000 美元相比，10 年的受教育年限差别才是巨大的！

+++

```{index} 中心化
```

在许多其他预测模型里，每个变量的*中心*（例如它的均值）同样重要。举例来说，假设有一份数据集，其中的温度以开尔文（Kelvin）为单位；另有一份内容相同的数据集，温度以摄氏度为单位，这两个变量就相差一个常数 273（尽管它们包含的信息完全相同）。同样，在前面那个假设的工作分类例子里，我们多半会看到工资变量的中心在数万这一量级，而受教育年限变量的中心只有个位数。这一点虽然不影响
K 近邻分类算法，但这么大的平移却会改变许多其他预测模型的结果。

```{index} 标准化; K 近邻
```

要对数据做缩放和中心化，需要先求出变量的*均值*（也就是平均数，用来刻画一组数值的“中心”位置）和*标准差*（用来衡量取值有多分散）。对变量的每个观测值，都减去均值（即对变量做中心化），再除以标准差（即对变量做缩放）。做完这一步，数据就称为*标准化*数据，数据集中所有变量的均值都是 0、标准差都是 1。为了展示标准化会给 K 近邻算法带来什么影响，我们读取未经标准化的原始威斯康星乳腺癌数据集；在此之前，我们用的都是标准化之后的版本。我们采用与前面相同的初始整理步骤，并且为了简单起见，只用 `Area`、`Smoothness` 和 `Class` 这三个变量：

```{code-cell} ipython3
unscaled_cancer = pd.read_csv("data/wdbc_unscaled.csv")[["Class", "Area", "Smoothness"]]
unscaled_cancer["Class"] = unscaled_cancer["Class"].replace({
   "M" : "Malignant",
   "B" : "Benign"
})
unscaled_cancer
```

看看上面这份既未缩放、也未中心化的数据，你会看到面积测量值之间的差异远大于光滑度（smoothness）测量值之间的差异。这会影响预测吗？为了弄清楚，我们要为这两个预测变量画散点图（按诊断结果着色），一份用刚刚读入的未标准化数据，一份用同一份数据标准化后的版本。但首先，我们需要用 `scikit-learn` 把 `unscaled_cancer` 数据集标准化。

```{index} see: Pipeline; scikit-learn
```

```{index} see: make_column_transformer; scikit-learn
```

```{index} scikit-learn;Pipeline, scikit-learn; make_column_transformer
```

`scikit-learn` 框架提供了一组*预处理器*（preprocessor），用来加工数据，它们都位于 [`preprocessing` 模块](https://scikit-learn.org/stable/modules/preprocessing.html)中。这里我们用 `StandardScaler` 变换器把 `unscaled_cancer` 数据中的预测变量标准化。要告诉 `StandardScaler` 该标准化哪些变量，需要用
[`make_column_transformer`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.make_column_transformer.html#sklearn.compose.make_column_transformer) 函数把它包进一个 [`ColumnTransformer`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html#sklearn.compose.ColumnTransformer) 对象。`ColumnTransformer` 对象还支持同时使用多个预处理器，当你想对每个预测变量分别做不同的预处理时，这一点特别方便。`make_column_transformer` 函数的主要参数是一串配对：（1）一个预处理器，（2）你想把该预处理器应用到哪些列。在本例中，我们只有 `StandardScaler` 这一个预处理器，把它应用到 `Area` 和 `Smoothness` 两列上。

```{code-cell} ipython3
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer

preprocessor = make_column_transformer(
    (StandardScaler(), ["Area", "Smoothness"]),
)
preprocessor
```

```{index} scikit-learn; make_column_transformer, scikit-learn; StandardScaler 
```

```{index} see: StandardScaler; scikit-learn
```

```{index} scikit-learn; fit, scikit-learn; make_column_selector, scikit-learn; StandardScaler
```

可以看到，这个预处理器只包含一个标准化步骤，应用到 `Area` 和 `Smoothness` 两列。注意，这里我们是逐个写出列名来指定预处理步骤要应用到哪些列的；当预测变量很多时，这种做法会变得相当困难。与其逐一写出列名，我们可以改用
[`make_column_selector`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.make_column_selector.html#sklearn.compose.make_column_selector) 函数。例如，若想把所有*数值型*预测变量都标准化，可以用 `make_column_selector`，并把 `dtype_include` 参数指定为 `"number"`。这样创建的预处理器与前面那个等价。

```{code-cell} ipython3
from sklearn.compose import make_column_selector

preprocessor = make_column_transformer(
    (StandardScaler(), make_column_selector(dtype_include="number")),
)
preprocessor
```

```{index} see: fit ; scikit-learn
```

```{index} scikit-learn; transform
```

现在可以标准化 `unscaled_cancer` 数据框里的数值型预测变量列了。这分两步完成。先调用 `fit` 函数，把 `unscaled_cancer` 数据作为参数传进去，算出实施标准化所需的量（每个变量的均值和标准差）。再用 `transform` 函数真正实施标准化。为了标准化数据而分两步——`fit` *和* `transform`——似乎有点多余。但正因为分两步，我们才能在 `transform` 这一步指定另一份数据。这样就能用一份数据算出标准化所需的量，再把同一套标准化应用到另一份数据上。

```{code-cell} ipython3
preprocessor.fit(unscaled_cancer)
scaled_cancer = preprocessor.transform(unscaled_cancer)
scaled_cancer
```
```{code-cell} ipython3
:tags: [remove-cell]
glue("scaled-cancer-column-0", '"'+scaled_cancer.columns[0]+'"')
glue("scaled-cancer-column-1", '"'+scaled_cancer.columns[1]+'"')
```
看起来 `Smoothness` 和 `Area` 变量已经标准化了。好耶！不过新的 `scaled_cancer` 数据框有两点值得注意。第一，它只保留 `transform` 输入（这里是 `unscaled_cancer`）中经过预处理步骤的那些列。我们用 `make_column_transformer` 构建的 `ColumnTransformer`，默认行为是*丢掉*其余各列。这个默认行为与 `sklearn` 的其他部分配合得很好（下面{numref}`08:puttingittogetherworkflow`就会讲到），但如果想可视化预处理的结果，保留原数据框中的其他列（比如这里的 `Class` 变量）会很有用。要保留其他列，需要在 `make_column_transformer` 函数中把 `remainder` 参数设为 `"passthrough"`。此外你会看到，新的列名——{glue:text}`scaled-cancer-column-0` 和 {glue:text}`scaled-cancer-column-1`——里包含了预处理步骤的名字，两者之间用下划线分隔。这个默认行为在 `sklearn` 中很有用，因为我们有时会对同样的列应用多个不同的预处理步骤；但同样地，为了可视化，保留原来的列名会很有用。要保留原列名，需要把 `verbose_feature_names_out` 参数设为 `False`。

```{note}
只有在你想要查看预处理步骤的结果时，才需要指定 `remainder` 和 `verbose_feature_names_out` 参数。大多数情况下，应当让这两个参数保持默认值。
```

```{code-cell} ipython3
preprocessor_keep_all = make_column_transformer(
    (StandardScaler(), make_column_selector(dtype_include="number")),
    remainder="passthrough",
    verbose_feature_names_out=False
)
preprocessor_keep_all.fit(unscaled_cancer)
scaled_cancer_all = preprocessor_keep_all.transform(unscaled_cancer)
scaled_cancer_all
```

你可能会奇怪：为了给变量做中心化和缩放，何必费这么大劲？难道不能在构建 K 近邻模型之前，自己动手把 `Area` 和 `Smoothness` 变量缩放、中心化吗？严格说，*可以*；但这样做容易出错。特别是，我们可能在预测时忘了套用同样的中心化／缩放，也可能不小心用了与训练时*不同*的中心化／缩放。正确使用 `ColumnTransformer`，能让代码更简单、更易读、也不易出错。另外请注意，只有你想亲自查看预处理步骤的结果时，才需要在预处理器上调用 `fit` 和 `transform`。稍后在{numref}`08:puttingittogetherworkflow`中你会看到，`scikit-learn` 提供了一些工具，可以自动把预处理器和模型衔接好，这样你就能按需在 `Pipeline` 上调用 `fit` 和 `transform`，不必额外写代码。

{numref}`fig:05-scaling-plt` 并排展示了两张散点图——一张对应 `unscaled_cancer`，一张对应 `scaled_cancer`。两张图都标出了同一个新观测以及它的 $K=3$ 个最近邻。在未标准化数据那张图里，三个最近邻选得有些奇怪。这些“近邻”从图上看明显落在良性观测的密集区域内部，而且都与新观测近乎排成一条垂直线（所以这张图看起来只有一条黑线）。{numref}`fig:05-scaling-plt-zoomed` 放大了未标准化图上这一区域的细节。在这里，最近邻的计算被标度大得多的面积变量主导了。{numref}`fig:05-scaling-plt` 右侧标准化数据的图，所选的最近邻就直观合理得多。可见，在使用预测算法时，对数据做标准化可能会带来重要改变。标准化应当成为你预测建模之前预处理工作的一部分，并且你始终要仔细考虑自己面对的问题领域，想清楚是否需要标准化数据。

```{code-cell} ipython3
:tags: [remove-cell]

def class_dscp(x):
    if x == "M":
        return "Malignant"
    elif x == "B":
        return "Benign"
    else:
        return x


attrs = ["Area", "Smoothness"]
new_obs = pd.DataFrame({"Class": ["Unknown"], "Area": 400, "Smoothness": 0.135})
unscaled_cancer["Class"] = unscaled_cancer["Class"].apply(class_dscp)
area_smoothness_new_df = pd.concat((unscaled_cancer, new_obs), ignore_index=True)
my_distances = euclidean_distances(area_smoothness_new_df[attrs])[
    len(unscaled_cancer)
][:-1]
area_smoothness_new_point = (
    alt.Chart(
        area_smoothness_new_df,
        title=alt.TitleParams(text="Unstandardized data", anchor="start"),
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Area"),
        y=alt.Y("Smoothness"),
        color=alt.Color(
            "Class",
            title="Diagnosis",
        ),
        shape=alt.Shape(
            "Class", scale=alt.Scale(range=["circle", "circle", "diamond"])
        ),
        size=alt.condition("datum.Class == 'Unknown'", alt.value(80), alt.value(30)),
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None))
    )
)

# The index of 3 rows that has smallest distance to the new point
min_3_idx = np.argpartition(my_distances, 3)[:3]
neighbor1 = pd.concat([
    unscaled_cancer.loc[[min_3_idx[0]], attrs],
    new_obs[attrs],
])
neighbor2 = pd.concat([
    unscaled_cancer.loc[[min_3_idx[1]], attrs],
    new_obs[attrs],
])
neighbor3 = pd.concat([
    unscaled_cancer.loc[[min_3_idx[2]], attrs],
    new_obs[attrs],
])

line1 = (
    alt.Chart(neighbor1)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)
line2 = (
    alt.Chart(neighbor2)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)
line3 = (
    alt.Chart(neighbor3)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)

area_smoothness_new_point = area_smoothness_new_point + line1 + line2 + line3
```

```{code-cell} ipython3
:tags: [remove-cell]

attrs = ["Area", "Smoothness"]
new_obs_scaled = pd.DataFrame({"Class": ["Unknown"], "Area": -0.72, "Smoothness": 2.8})
scaled_cancer_all["Class"] = scaled_cancer_all["Class"].apply(class_dscp)
area_smoothness_new_df_scaled = pd.concat(
    (scaled_cancer_all, new_obs_scaled), ignore_index=True
)
my_distances_scaled = euclidean_distances(area_smoothness_new_df_scaled[attrs])[
    len(scaled_cancer_all)
][:-1]
area_smoothness_new_point_scaled = (
    alt.Chart(
        area_smoothness_new_df_scaled,
        title=alt.TitleParams(text="Standardized data", anchor="start"),
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Area", title="Area (standardized)"),
        y=alt.Y("Smoothness", title="Smoothness (standardized)"),
        color=alt.Color(
            "Class",
            title="Diagnosis",
        ),
        shape=alt.Shape(
            "Class", scale=alt.Scale(range=["circle", "circle", "diamond"])
        ),
        size=alt.condition("datum.Class == 'Unknown'", alt.value(80), alt.value(30)),
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None))
    )
)
min_3_idx_scaled = np.argpartition(my_distances_scaled, 3)[:3]
neighbor1_scaled = pd.concat([
    scaled_cancer_all.loc[[min_3_idx_scaled[0]], attrs],
    new_obs_scaled[attrs],
])
neighbor2_scaled = pd.concat([
    scaled_cancer_all.loc[[min_3_idx_scaled[1]], attrs],
    new_obs_scaled[attrs],
])
neighbor3_scaled = pd.concat([
    scaled_cancer_all.loc[[min_3_idx_scaled[2]], attrs],
    new_obs_scaled[attrs],
])

line1_scaled = (
    alt.Chart(neighbor1_scaled)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)
line2_scaled = (
    alt.Chart(neighbor2_scaled)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)
line3_scaled = (
    alt.Chart(neighbor3_scaled)
    .mark_line()
    .encode(x="Area", y="Smoothness", color=alt.value("black"))
)

area_smoothness_new_point_scaled = (
    area_smoothness_new_point_scaled + line1_scaled + line2_scaled + line3_scaled
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue(
    "fig:05-scaling-plt",
    area_smoothness_new_point | area_smoothness_new_point_scaled
)
```

:::{glue:figure} fig:05-scaling-plt
:name: fig:05-scaling-plt

未标准化数据与标准化数据下 K = 3 个最近邻的比较。
:::

```{code-cell} ipython3
:tags: [remove-cell]

zoom_area_smoothness_new_point = (
    alt.Chart(
        area_smoothness_new_df,
        title=alt.TitleParams(text="Unstandardized data", anchor="start"),
    )
    .mark_point(clip=True, opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Area", scale=alt.Scale(domain=(395, 405))),
        y=alt.Y("Smoothness", scale=alt.Scale(domain=(0.08, 0.14))),
        color=alt.Color(
            "Class",
            title="Diagnosis",
        ),
        shape=alt.Shape(
            "Class", scale=alt.Scale(range=["circle", "circle", "diamond"])
        ),
        size=alt.condition("datum.Class == 'Unknown'", alt.value(80), alt.value(30)),
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None))
    )
)
zoom_area_smoothness_new_point + line1 + line2 + line3
glue("fig:05-scaling-plt-zoomed", (zoom_area_smoothness_new_point + line1 + line2 + line3))
```

:::{glue:figure} fig:05-scaling-plt-zoomed
:name: fig:05-scaling-plt-zoomed

未标准化数据下三个最近邻的放大图。
:::

+++

### 平衡

```{index} 平衡, 不平衡
```

分类器所用的数据集还可能存在另一个问题：*类别不平衡（class imbalance）*，也就是某个标签比另一个标签常见得多。像 K 近邻算法这样的分类器，会用附近数据点的标签来预测新数据点的标签；因此，如果总体上看带某个标签的数据点数量多得多，算法总体上就更可能选中这个标签（即使数据呈现的“模式”提示的并非如此）。类别不平衡其实相当常见，也很重要：从罕见病诊断到恶意邮件识别，很多场景中真正需要识别出的那个“重要”类别（患病、恶意邮件）都比“不重要”的类别（未患病、正常邮件）稀有得多。

```{index} concat
```

为了更好地说明这个问题，我们再来看看标准化后的乳腺癌数据 `cancer`；只不过这次要删去大量恶性肿瘤观测，模拟癌症罕见时数据会呈现什么样子。具体做法是只从恶性肿瘤一组中挑出 3 条观测，良性观测则全部保留。这 3 条观测用 `.head()` 方法选取，该方法会从数据框顶部取指定的行数。接着，我们用 `pandas` 中的 [`concat`](https://pandas.pydata.org/docs/reference/api/pandas.concat.html) 函数把过滤后得到的两个数据框重新粘合起来。`concat` 函数沿某个轴*拼接*数据框：默认沿 `axis=0` 纵向拼接，把两个数据框合成单个*更高*的数据框，这正是我们这里想要的；如果想横向拼接、得到*更宽*的数据框，就要指定 `axis=1`。新的不平衡数据见{numref}`fig:05-unbalanced`，各类别的计数我们则用 `value_counts` 函数打印出来。

```{code-cell} ipython3
:tags: ["remove-output"]
rare_cancer = pd.concat((
    cancer[cancer["Class"] == "Benign"],
    cancer[cancer["Class"] == "Malignant"].head(3)
))

rare_plot = alt.Chart(rare_cancer).mark_circle().encode(
    x=alt.X("Perimeter").title("Perimeter (standardized)"),
    y=alt.Y("Concavity").title("Concavity (standardized)"),
    color=alt.Color("Class").title("Diagnosis")
)
rare_plot
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("fig:05-unbalanced", rare_plot)
```

:::{glue:figure} fig:05-unbalanced
:name: fig:05-unbalanced

不平衡数据。
:::

```{code-cell} ipython3
rare_cancer["Class"].value_counts()
```

+++

假设现在我们决定在 K 近邻分类中取 $K = 7$。恶性肿瘤只有 3 条观测，于是分类器*无论肿瘤的凹度和周长是多少，都会预测它是良性的*！这是因为在 7 条观测的多数投票中，最多只有 3 条是恶性的（恶性肿瘤观测总共只有 3 条），所以至少 4 条必然是良性的，良性一方总会胜出。例如，{numref}`fig:05-upsample` 展示了一个新肿瘤观测的情形：它与训练数据中被标为恶性的 3 条观测相当接近。

```{code-cell} ipython3
:tags: [remove-cell]

attrs = ["Perimeter", "Concavity"]
new_point = [2, 2]
new_point_df = pd.DataFrame(
    {"Class": ["Unknown"], "Perimeter": new_point[0], "Concavity": new_point[1]}
)
rare_cancer["Class"] = rare_cancer["Class"].apply(class_dscp)
rare_cancer_with_new_df = pd.concat((rare_cancer, new_point_df), ignore_index=True)
my_distances = euclidean_distances(rare_cancer_with_new_df[attrs])[
    len(rare_cancer)
][:-1]

# First layer: scatter plot, with unknwon point labeled as red "unknown" diamond
rare_plot = (
    alt.Chart(
        rare_cancer_with_new_df
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
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None))
    )
)

# Find the 7 NNs
min_7_idx = np.argpartition(my_distances, 7)[:7]

# For loop: each iteration adds a line segment of corresponding color
for i in range(7):
    clr = "#1f77b4"
    if rare_cancer.iloc[min_7_idx[i], :]["Class"] == "Malignant":
        clr = "#ff7f0e"
    neighbor = pd.concat([
        rare_cancer.iloc[[min_7_idx[i]], :][attrs],
        new_point_df[attrs],
    ])
    rare_plot = rare_plot + (
        alt.Chart(neighbor)
        .mark_line(opacity=0.3)
        .encode(x="Perimeter", y="Concavity", color=alt.value(clr))
    )

glue("fig:05-upsample", rare_plot)
```

:::{glue:figure} fig:05-upsample
:name: fig:05-upsample

不平衡数据，其中突出显示了新观测的 7 个最近邻。
:::

+++

{numref}`fig:05-upsample-2` 展示了另一种情形：把图中每个区域的背景颜色设为 K 近邻分类器对该位置的新观测会给出的预测。可以看到，判别结果始终是“良性”，对应蓝色。

```{code-cell} ipython3
:tags: [remove-cell]

knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(X=rare_cancer[["Perimeter", "Concavity"]], y=rare_cancer["Class"])

# create a prediction pt grid
per_grid = np.linspace(
    rare_cancer["Perimeter"].min() * 1.05, rare_cancer["Perimeter"].max() * 1.05, 50
)
con_grid = np.linspace(
    rare_cancer["Concavity"].min() * 1.05, rare_cancer["Concavity"].max() * 1.05, 50
)
pcgrid = np.array(np.meshgrid(per_grid, con_grid)).reshape(2, -1).T
pcgrid = pd.DataFrame(pcgrid, columns=["Perimeter", "Concavity"])
pcgrid

knnPredGrid = knn.predict(pcgrid)
prediction_table = pcgrid.copy()
prediction_table["Class"] = knnPredGrid
prediction_table

# create the scatter plot
rare_plot = (
    alt.Chart(
        rare_cancer,
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Perimeter", title="Perimeter (standardized)"),
        y=alt.Y("Concavity", title="Concavity (standardized)"),
        color=alt.Color("Class", title="Diagnosis"),
    )
)

# add a prediction layer, also scatter plot
prediction_plot = (
    alt.Chart(
        prediction_table,
        title="Imbalanced data",
    )
    .mark_point(opacity=0.05, filled=True, size=300)
    .encode(
        x=alt.X(
            "Perimeter",
            title="Perimeter (standardized)",
            scale=alt.Scale(
                domain=(rare_cancer["Perimeter"].min() * 1.05, rare_cancer["Perimeter"].max() * 1.05),
                nice=False
            ),
        ),
        y=alt.Y(
            "Concavity",
            title="Concavity (standardized)",
            scale=alt.Scale(
                domain=(rare_cancer["Concavity"].min() * 1.05, rare_cancer["Concavity"].max() * 1.05),
                nice=False
            ),
        ),
        color=alt.Color("Class", title="Diagnosis"),
    )
)
#rare_plot + prediction_plot
glue("fig:05-upsample-2", (rare_plot + prediction_plot))
```

:::{glue:figure} fig:05-upsample-2
:name: fig:05-upsample-2

不平衡数据，背景颜色表示分类器的判别结果，点表示有标签数据。
:::

+++

```{index} 过采样, DataFrame; sample
```

这个问题虽然简单，但要把它处理得在统计上站得住脚，其实相当微妙；真要讲清楚，所需的细节和数学远超本书的范围。就目前的目的而言，只要对稀有类做*过采样（oversampling）*来重新平衡数据就足够了。也就是说，我们在数据集中把稀有观测重复若干次，让它们在 K 近邻算法中获得更大的表决权。为此，我们先用筛选把各个类别拆成各自的数据框；然后对稀有类的数据框使用 `sample` 方法，把 `Malignant` 观测的条数增加到与 `Benign` 观测相同：把 `n` 参数设为想要的 `Malignant` 观测条数，并设 `replace=True` 表示有放回抽样（with replacement）。最后用 `value_counts` 方法查看各类别现在是否已经平衡。注意，`sample` 是*随机*挑选要复制哪些数据的；如何正确处理数据分析中的随机性，我们将在{numref}`第 %s 章 <classification2>`中进一步学习。

```{code-cell} ipython3
:tags: [remove-cell]
# hidden seed call to make the below resample reproducible
# we haven't taught students about seeds / prngs yet, so
# for now just hide this.
np.random.seed(1)
```

```{code-cell} ipython3
malignant_cancer = rare_cancer[rare_cancer["Class"] == "Malignant"]
benign_cancer = rare_cancer[rare_cancer["Class"] == "Benign"]
malignant_cancer_upsample = malignant_cancer.sample(
    n=benign_cancer.shape[0], replace=True
)
upsampled_cancer = pd.concat((malignant_cancer_upsample, benign_cancer))
upsampled_cancer["Class"].value_counts()
```

现在假设我们在这个*平衡*数据上用 $K=7$ 训练 K 近邻分类器。这时再把散点图每个区域的背景颜色设为 K 近邻分类器会给出的判别结果，就得到{numref}`fig:05-upsample-plot` 所示的情形。可以看到，判别结果合理多了：点靠近标为恶性的观测时，分类器就预测为恶性肿瘤；反过来，点更接近良性肿瘤观测时，就预测为良性。

```{code-cell} ipython3
:tags: [remove-cell]

knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(
    X=upsampled_cancer[["Perimeter", "Concavity"]], y=upsampled_cancer["Class"]
)

# create a prediction pt grid
knnPredGrid = knn.predict(pcgrid)
prediction_table = pcgrid
prediction_table["Class"] = knnPredGrid

# create the scatter plot
rare_plot = (
    alt.Chart(rare_cancer)
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X(
            "Perimeter",
            title="Perimeter (standardized)",
            scale=alt.Scale(
                domain=(rare_cancer["Perimeter"].min() * 1.05, rare_cancer["Perimeter"].max() * 1.05),
                nice=False
            ),
        ),
        y=alt.Y(
            "Concavity",
            title="Concavity (standardized)",
            scale=alt.Scale(
                domain=(rare_cancer["Concavity"].min() * 1.05, rare_cancer["Concavity"].max() * 1.05),
                nice=False
            ),
        ),
        color=alt.Color("Class", title="Diagnosis"),
    )
)

# add a prediction layer, also scatter plot
upsampled_plot = (
    alt.Chart(prediction_table)
    .mark_point(opacity=0.05, filled=True, size=300)
    .encode(
        x=alt.X("Perimeter", title="Perimeter (standardized)"),
        y=alt.Y("Concavity", title="Concavity (standardized)"),
        color=alt.Color("Class", title="Diagnosis"),
    )
)
#rare_plot + upsampled_plot
glue("fig:05-upsample-plot", (rare_plot + upsampled_plot))
```

:::{glue:figure} fig:05-upsample-plot
:name: fig:05-upsample-plot

过采样（oversampling）后的数据，背景颜色表示分类器的判别结果。
:::

### 缺失数据

```{index} 缺失数据
```

真实世界的数据集最常见的问题之一就是*缺失数据*，也就是某些变量的取值没有被记录下来的那些观测。遗憾的是，缺失数据虽然常见，要妥善处理却非常困难，通常要依靠关于数据本身、数据背景以及数据收集方式的专门知识。缺失数据带来的一个典型难题是：缺失项本身可能*有信息量*，也就是说，某些项之所以缺失，与其他变量的取值有关。例如，来自边缘群体的调查对象如果担心如实回答会带来负面后果，就可能不太愿意回答某类问题。这时，倘若我们干脆把带缺失项的数据丢掉，就会在无意中剔除掉该群体的大量成员，使调查结论产生偏差。因此，在真实问题中忽视这一点，很容易得出误导性的分析结果，造成有害影响。本书只介绍这样一类处理缺失项的技巧：缺失项仅仅是“随机缺失”，即某些项之所以缺失，*与观测的其他方面毫无关系*。

我们加载并查看肿瘤图像数据的一个修改版子集，其中含有少量缺失项：

```{code-cell} ipython3
missing_cancer = pd.read_csv("data/wdbc_missing.csv")[["Class", "Radius", "Texture", "Perimeter"]]
missing_cancer["Class"] = missing_cancer["Class"].replace({
   "M" : "Malignant",
   "B" : "Benign"
})
missing_cancer
```

回想一下，K 近邻分类通过计算到附近训练观测的直线距离来做预测，因此需要用到训练数据中*所有*观测的*所有*变量取值。那么，数据存在缺失时该怎么用 K 近邻分类呢？既然带缺失项的观测并不算多，一种办法就是在构建 K 近邻分类器之前直接把这些观测删掉。要做到这一点，只需在开始处理数据之前使用 `dropna` 方法。

```{index} 缺失数据; dropna
```

```{code-cell} ipython3
no_missing_cancer = missing_cancer.dropna()
no_missing_cancer
```

不过，如果很多行都含有缺失项，这个办法就行不通了，因为最后可能丢掉太多数据。此时另一种可行做法是对缺失项做*插补*（impute），也就是根据数据集中其他观测填上合成取值。一个合理的选择是*均值插补*（mean imputation），即用每个变量中现有取值的均值来填补缺失项。做均值插补时，我们使用 `SimpleImputer` 变换器并采用默认参数，再用 `make_column_transformer` 指明哪些列需要插补。

```{index} scikit-learn; SimpleImputer, 缺失数据; 均值插补
```

```{code-cell} ipython3
from sklearn.impute import SimpleImputer

preprocessor = make_column_transformer(
    (SimpleImputer(), ["Radius", "Texture", "Perimeter"]),
    verbose_feature_names_out=False
)
preprocessor
```

为了直观看出均值插补做了什么，我们直接用 `fit` 和 `transform` 函数把变换器应用到 `missing_cancer` 数据框上。插补这一步会用各变量自身的均值填补相应的缺失项。

```{code-cell} ipython3
preprocessor.fit(missing_cancer)
imputed_cancer = preprocessor.transform(missing_cancer)
imputed_cancer
```

缺失数据插补还有许多其他做法，可参见 [`scikit-learn` 文档](https://scikit-learn.org/stable/modules/impute.html)。无论你在数据分析中决定如何处理缺失数据，批判性地思考数据背景、数据收集方式以及你正要回答的问题，始终都至关重要。

+++

(08:puttingittogetherworkflow)=
## 用 `Pipeline` 把流程串起来

```{index} scikit-learn; Pipeline
```

`scikit-learn` 包集合还提供了 [`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html?highlight=pipeline#sklearn.pipeline.Pipeline)，它可以把多个数据分析步骤串联起来，省去为中间步骤编写大量本来必需的代码。为了演示整个工作流，我们从 `wdbc_unscaled.csv` 数据从头做起。首先读取数据、创建模型，并为数据指定一个预处理器。

```{code-cell} ipython3
# load the unscaled cancer data, make Class readable
unscaled_cancer = pd.read_csv("data/wdbc_unscaled.csv")
unscaled_cancer["Class"] = unscaled_cancer["Class"].replace({
   "M" : "Malignant",
   "B" : "Benign"
})
unscaled_cancer

# create the K-NN model
knn = KNeighborsClassifier(n_neighbors=7)

# create the centering / scaling preprocessor
preprocessor = make_column_transformer(
    (StandardScaler(), ["Area", "Smoothness"]),
)
```

```{index} scikit-learn; make_pipeline, scikit-learn; fit
```

接下来，我们用
[`make_pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.make_pipeline.html#sklearn.pipeline.make_pipeline) 函数把这些步骤放进一个 `Pipeline`。`make_pipeline` 函数接收一个步骤列表，按顺序应用到数据分析中（译注：实际上 make_pipeline 接收的是多个位置参数，例如 make_pipeline(preprocessor, knn)，而不是一个列表）；这里我们只有
`preprocessor` 和 `knn` 两个步骤。最后，我们对流水线调用 `fit`。注意，我们不需要分别对 `preprocessor` 调用 `fit` 和 `transform`，流水线会替我们妥善完成这件事。还请注意，对流水线调用 `fit` 时，可以把整个 `unscaled_cancer` 数据框传给 `X` 参数，因为预处理步骤会丢弃我们列出的两个变量之外的所有变量，也就是 `Area` 和 `Smoothness`。`y` 响应变量参数则和之前一样，传入 `unscaled_cancer["Class"]` Series。

```{code-cell} ipython3
from sklearn.pipeline import make_pipeline

knn_pipeline = make_pipeline(preprocessor, knn)
knn_pipeline.fit(
    X=unscaled_cancer,
    y=unscaled_cancer["Class"]
)
knn_pipeline
```

和之前一样，拟合对象会列出用于训练模型的函数。不过现在，拟合对象还包含了整个工作流的信息，其中包括标准化这一预处理步骤。换句话说，我们用 `predict` 函数配合 `knn_pipeline` 对象对新观测做预测时，它会先对新观测应用同样的预处理步骤。举个例子，我们来预测两个新观测的类别标签：一个是 `Area = 500`、`Smoothness = 0.075`，另一个是 `Area = 1500`、`Smoothness = 0.1`。

```{code-cell} ipython3
new_observation = pd.DataFrame({"Area": [500, 1500], "Smoothness": [0.075, 0.1]})
prediction = knn_pipeline.predict(new_observation)
prediction
```

分类器预测第一个观测为良性，第二个为恶性。{numref}`fig:05-workflow-plot` 展示了这个训练好的 K 近邻模型在大量新观测上会做出的预测。你已经见过好几次这样的彩色预测图了，但我们一直没有提供生成它们的代码，因为代码有点复杂。如果你有兴趣挑战一下自己，我们现在把它列在下面。基本思路是：用 `numpy` 的 `meshgrid` 函数造出由合成新观测构成的网格，预测每个点的标签，再用一张透明度很高（`opacity` 取值很小）、点半径很大的彩色散点图把这些预测画出来。看看你能不能弄明白每一行代码在做什么！

```{note}
理解这段代码并不是读懂本书后续内容的必需条件。把它列在这里，是供那些希望在自己的数据分析中使用类似可视化的人参考。
```

```{code-cell} ipython3
:tags: [remove-output]
import numpy as np

# create the grid of area/smoothness vals, and arrange in a data frame
are_grid = np.linspace(
    unscaled_cancer["Area"].min() * 0.95, unscaled_cancer["Area"].max() * 1.05, 50
)
smo_grid = np.linspace(
    unscaled_cancer["Smoothness"].min() * 0.95, unscaled_cancer["Smoothness"].max() * 1.05, 50
)
asgrid = np.array(np.meshgrid(are_grid, smo_grid)).reshape(2, -1).T
asgrid = pd.DataFrame(asgrid, columns=["Area", "Smoothness"])

# use the fit workflow to make predictions at the grid points
knnPredGrid = knn_pipeline.predict(asgrid)

# bind the predictions as a new column with the grid points
prediction_table = asgrid.copy()
prediction_table["Class"] = knnPredGrid

# plot:
# 1. the colored scatter of the original data
unscaled_plot = alt.Chart(unscaled_cancer).mark_point(
    opacity=0.6,
    filled=True,
    size=40
).encode(
    x=alt.X("Area")
        .scale(
            nice=False,
            domain=(
                unscaled_cancer["Area"].min() * 0.95,
                unscaled_cancer["Area"].max() * 1.05
            )
        ),
    y=alt.Y("Smoothness")
        .scale(
            nice=False,
            domain=(
                unscaled_cancer["Smoothness"].min() * 0.95,
                unscaled_cancer["Smoothness"].max() * 1.05
            )
        ),
    color=alt.Color("Class").title("Diagnosis")
)

# 2. the faded colored scatter for the grid points
prediction_plot = alt.Chart(prediction_table).mark_point(
    opacity=0.05,
    filled=True,
    size=300
).encode(
    x="Area",
    y="Smoothness",
    color=alt.Color("Class").title("Diagnosis")
)
unscaled_plot + prediction_plot
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("fig:05-workflow-plot", (unscaled_plot + prediction_plot))
```

:::{glue:figure} fig:05-workflow-plot
:name: fig:05-workflow-plot

光滑度对面积的散点图，其中背景颜色表示分类器的判别结果。
:::

+++

## 习题

本章内容的练习题可以在配套的[练习册仓库](https://worksheets.python.datasciencebook.ca)的“Classification I: training and predicting（分类 I：训练与预测）”一行中找到。你可以预览本章练习册（worksheet）的非交互版本，只需点击“查看练习册（view worksheet）”。如果要交互式地做习题，请按照练习册仓库中的说明下载所有练习册，并按照{numref}`第 %s 章 <move-to-your-own-machine>`中的计算机环境配置说明操作。这样就能确保练习册提供的自动反馈与引导能按预期正常工作。


+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
