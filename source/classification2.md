---
jupytext:
  formats: py:percent,md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(classification2)=
# 分类 II：评估与调优

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
```

## 概述
本章继续介绍用分类进行预测建模。上一章讲解了模型训练与数据预处理，本章则聚焦于如何评估分类器的性能，以及如何在可能时改进分类器，把它的准确率（accuracy）提到最高。

## 本章学习目标
学完本章后，你将能够：

- 说明什么是训练集、验证集和测试集，以及它们在分类中如何使用。
- 把数据划分为训练集、验证集和测试集。
- 说明什么是随机种子，以及它在可复现的数据分析中有多重要。
- 使用 `numpy.random.seed` 函数在 Python 中设置随机种子。
- 说明并解读准确率、精确率（precision）、召回率（recall）和混淆矩阵。
- 在 Python 中用测试集、单个验证集和交叉验证来评估分类的准确率、精确率和召回率。
- 在 Python 中生成混淆矩阵。
- 通过最大化交叉验证准确率估计值，选择 K 近邻分类器中的近邻个数。
- 说明欠拟合与过拟合，并把它们与 K 近邻分类中的近邻个数联系起来。
- 说明 K 近邻分类算法的优点和缺点。

+++

## 评估性能

```{index} 乳腺癌
```

有时分类器会给出错误的预测。分类器不必 100\% 的时间都正确才算有用，不过我们也不希望它错得太多。那么，怎样衡量分类器有多“好”呢？我们回到[乳腺癌图像数据](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29) {cite:p}`streetbreastcancer`，想一想分类器在实践中会怎样使用。医生会为一位*新*患者的肿瘤做活检，对得到的图像加以分析，再让分类器判断这个肿瘤是良性还是恶性。这里的关键词是*新*：如果分类器能对*训练期间未曾见过*的数据给出准确的预测，我们就认为它是“好”的，因为这说明它确实学到了预测变量与响应变量之间的关系，而不是简单地记住每一条训练数据的标签。可是，如果不跑一趟医院去收集更多肿瘤图像，我们又该怎么评估分类器呢？


```{index} 训练集, 测试集
```

办法是把数据划分为**训练集**和**测试集**（{numref}`fig:06-training-test`），并且只用**训练集**来构建分类器。接下来，为了评估分类器的性能，我们先把**测试集**的标签放到一边，再用分类器预测**测试集**中的标签。如果预测结果与**测试集**中观测的实际标签相符，我们就有了一些信心：这个分类器或许也能准确预测那些类别标签未知的新观测的类别标签。

```{index} 机器学习黄金法则
```

```{note}
如果说机器学习有一条黄金法则，那大概就是：*不能拿测试数据来构建模型*！一旦这么做，模型就会提前“看到”测试数据，于是显得比实际更准确。想想看，在判断患者的肿瘤是恶性还是良性时高估了分类器的准确率，后果会有多糟！
```

+++

```{figure} img/classification2/training_test.png
:name: fig:06-training-test

把数据划分为训练集和测试集。
```

+++

```{index} see: 预测准确率; 准确率
```

```{index} 准确率
```

那么，究竟怎样判断预测结果与测试集中观测的实际标签有多吻合呢？一种做法是计算预测**准确率**。它是指分类器给出正确预测的样本所占的比例：用预测正确的数量除以预测的总数即可。判断预测结果是否与测试集中的实际标签相符的过程，见{numref}`fig:06-ML-paradigm-test`。

$$\mathrm{accuracy} = \frac{\mathrm{number \; of  \; correct  \; predictions}}{\mathrm{total \;  number \;  of  \; predictions}}$$

+++

```{figure} img/classification2/ML-paradigm-test.png
:name: fig:06-ML-paradigm-test

划分数据并计算预测准确率的过程。
```

```{index} 混淆矩阵
```

准确率能用单个数字概括分类器的性能，方便且通用。但预测准确率本身说明不了全部问题。准确率只反映分类器总体上出错的频率，却不涉及它犯的是*哪一类*错误。要想更全面地了解性能，还可以进一步考察**混淆矩阵**。混淆矩阵列出测试集中每一类标签有多少条预测正确、多少条预测错误，从而更清楚地看出分类器容易犯哪种错误。{numref}`confusion-matrix-table` 给出了肿瘤图像数据的一个混淆矩阵示例，其中测试集包含 65 条观测。

```{list-table} 肿瘤图像数据的混淆矩阵示例。
:header-rows: 1
:name: confusion-matrix-table

* -
  - 预测为恶性
  - 预测为良性
* - **实际为恶性**
  - 1
  - 3
* - **实际为良性**
  - 4
  - 57
```

在{numref}`confusion-matrix-table` 的例子中，有 1 条恶性观测被正确判为恶性（左上角），57 条良性观测被正确判为良性（右下角）。不过也能看出分类器犯了一些错误：它把 3 条恶性观测判成了良性，把 4 条良性观测判成了恶性。由下面的公式可以算出，这个分类器的准确率约为 89%：

$$\mathrm{accuracy} = \frac{\mathrm{number \; of  \; correct  \; predictions}}{\mathrm{total \;  number \;  of  \; predictions}} = \frac{1+57}{1+57+4+3} = 0.892.$$

但我们还会发现，数据集中共有 4 个恶性肿瘤，分类器只识别出其中 1 个；换句话说，它把 75% 的恶性病例判错了！在这个例子里，把恶性肿瘤误判可能造成灾难性后果，因为需要治疗的患者可能因此得不到治疗。既然我们特别关心能否找出恶性病例，那么即便准确率达到 89%，这个分类器恐怕也难以接受。

```{index} 正类标签, 负类标签, 真阳性, 真阴性, 假阳性, 假阴性
```

在分类问题中，人们常常更关注某一类标签，而不是另一类。这时，我们通常把更想识别出来的那一类标签称为*正类*标签，另一类称为*负类*标签。在肿瘤这个例子里，恶性观测就是*正类*，良性观测则是*负类*。分类器能做出的四种预测，正好对应混淆矩阵中的四个单元格，可以用以下术语来称呼：

- **真阳性（True Positive）**：恶性观测被判为恶性（{numref}`confusion-matrix-table` 左上角）。
- **假阳性（False Positive）**：良性观测被判为恶性（{numref}`confusion-matrix-table` 左下角）。
- **真阴性（True Negative）**：良性观测被判为良性（{numref}`confusion-matrix-table` 右下角）。
- **假阴性（False Negative）**：恶性观测被判为良性（{numref}`confusion-matrix-table` 右上角）。

```{index} 精确率, 召回率
```

完美分类器不会有假阴性，也不会有假阳性（因此准确率为 100%）。然而，实际中的分类器几乎总会犯一些错误。所以，你应当想清楚在自己的应用里哪种错误最要紧，并用混淆矩阵把它们量化、报告出来。利用混淆矩阵可以算出两个常用指标：分类器的**精确率**和**召回率**，它们常与准确率一起报告。*精确率*衡量分类器判为正类的预测中有多少确实是正类。直观地说，我们希望分类器的精确率*高*：精确率高的分类器如果报告某个新观测为正类，我们就可以相信这个新观测确实是正类。用混淆矩阵中的各项，可以按下面的公式计算分类器的精确率：

$$\mathrm{precision} = \frac{\mathrm{number \; of  \; correct \; positive \; predictions}}{\mathrm{total \;  number \;  of \; positive  \; predictions}}.$$

*召回率*衡量测试集中的正类观测有多少被识别为正类。直观地说，我们希望分类器的召回率*高*：召回率高的分类器只要测试数据中存在正类观测，我们就可以相信它能找出来。同样用混淆矩阵中的各项，可以按下面的公式计算分类器的召回率：

$$\mathrm{recall} = \frac{\mathrm{number \; of  \; correct  \; positive \; predictions}}{\mathrm{total \;  number \;  of  \; positive \; test \; set \; observations}}.$$

在{numref}`confusion-matrix-table` 给出的例子里，精确率和召回率分别是

$$\mathrm{precision} = \frac{1}{1+4} = 0.20, \quad \mathrm{recall} = \frac{1}{1+3} = 0.25.$$

可见，即使准确率达到 89%，这个分类器的精确率和召回率都相当低。就这项数据分析而言，召回率尤其重要：如果有人患了恶性肿瘤，我们当然希望能把它识别出来。召回率只有 25% 恐怕是不能接受的！

```{note}
要让精确率和召回率同时都很高是很难的：精确率高的模型往往召回率低，反之亦然。举个例子，我们可以轻松做出一个*召回率完美*的分类器：*一律*猜正类就行了！它当然能找出测试集中的每一个正类观测，但一路上会产生大量假阳性预测，精确率很低。同样，我们也可以轻松做出一个*精确率完美*的分类器：*从不*猜正类！它绝不会把观测错判为正类，但一路上会产生大量假阴性预测。事实上，这个分类器的召回率为 0%！当然，大多数真实分类器都落在这两个极端之间。但这些例子说明，当某一类正是我们关心的类别时（也就是说，存在*正类*标签），设计分类器就必须在精确率与召回率之间做出权衡取舍。
```

+++

(randomseeds)=
## 随机性与种子

```{index} 随机
```

从本章开始，我们的数据分析会经常用到*随机性*。只要分析中需要做出一项公平、无偏、不受人为影响的决定，我们就会借助随机性。例如，本章需要把数据集划分为训练集和测试集，以便评估分类器。我们当然不想亲手决定怎样划分数据，因为要避免无意中影响评估结果。于是，我们让 Python *随机*划分数据。后续各章还会以许多其他方式使用随机性，例如从较大的数据集中选出一小部分数据、抽取数据的分组，等等。

```{index} 可复现, 种子
```

```{index} see: 随机种子; 种子
```

```{index} 种子; numpy.random.seed
```

不过，使用随机性与良好数据分析实践的一条主要原则相抵触：*可复现性*。回想一下，可复现的分析每次运行都会产生相同的结果；如果分析中包含随机性，岂不是每次结果都不一样？窍门在于，在 Python——以及其他编程语言——里，随机性其实并不随机！Python 使用的是一个*随机数生成器*，它产生的一串数字完全由一个*种子值*决定。一旦设定种子值，此后的一切也许*看起来*随机，实际上完全可复现。只要选取同一个种子值，你得到的结果就完全相同！

```{index} sample, to_list
```

我们用一个例子来看看随机性在 Python 中是怎样起作用的。假设有一个 Series（序列），其中包含从 0 到 9 的整数。我们想从里面随机抽出 10 个数，同时希望这个过程可复现。在抽取这 10 个数之前，先调用 `numpy` 包中的 `seed` 函数，把任意一个整数作为参数传给它。下面用到的种子数是 `1`。这样设置之后，Python 会跟踪此后代码中出现的随机性。例如，我们可以对这个 Series 调用 `sample` 方法，传入参数 `n=10`，表示想要 10 个样本。`to_list` 方法会把结果 Series 转换成基本的 Python 列表，让输出更容易阅读。

```{code-cell} ipython3
import numpy as np
import pandas as pd

np.random.seed(1)

nums_0_to_9 = pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

random_numbers1 = nums_0_to_9.sample(n=10).to_list()
random_numbers1
```
可以看到，`random_numbers1` 是由 0 到 9 这 10 个数组成的一个列表，从表面上看完全是随机的。如果再次运行 `sample` 方法，我们会得到新的一批 10 个数，看起来同样随机。

```{code-cell} ipython3
random_numbers2 = nums_0_to_9.sample(n=10).to_list()
random_numbers2
```

如果想让 Python 生成相同的随机数序列，只要再次调用 `np.random.seed` 函数，传入与前面一样的种子值 `1`，然后再调用一次 `sample` 方法即可。

```{code-cell} ipython3
np.random.seed(1)
random_numbers1_again = nums_0_to_9.sample(n=10).to_list()
random_numbers1_again
```

```{code-cell} ipython3
random_numbers2_again = nums_0_to_9.sample(n=10).to_list()
random_numbers2_again
```

注意，调用 `np.random.seed` 之后，我们得到的两串数字完全相同，顺序也一样。`random_numbers1` 与 `random_numbers1_again` 得到的是同一串数字，`random_numbers2` 与 `random_numbers2_again` 也是如此。而如果换一个种子值——比如 4235——得到的随机数序列就不同了。

```{code-cell} ipython3
np.random.seed(4235)
random_numbers1_different = nums_0_to_9.sample(n=10).to_list()
random_numbers1_different
```

```{code-cell} ipython3
random_numbers2_different = nums_0_to_9.sample(n=10).to_list()
random_numbers2_different
```

换句话说，尽管 Python 生成的数字序列*看起来*是随机的，但只要设定了种子值，它们就完全确定了！

那么，这对数据分析意味着什么呢？`sample` 当然不是 Python 中唯一用到随机性的地方。我们在 `scikit-learn` 乃至其他包中用到的许多函数都会用到随机性——有些甚至不会告诉你。还要注意，Python 启动时会自己创建一个种子。因此，如果你没有显式调用 `np.random.seed` 函数，结果很可能不可复现。最后要注意，种子只应在数据分析开始时设置*一次*。每设置一次种子，你就注入了一分人为输入，从而影响分析结果。例如，如果分析中多次使用 `sample`，却每次都设置种子，那么 Python 所用的随机性就不会像它应有的那样随机。

总之，如果你希望分析可复现，也就是每次运行都产生*相同的结果*，务必在分析开始时只调用 `np.random.seed` 一次。`np.random.seed` 的参数取值不同，随机性的模式也会不同；但只要选取同一个值，分析结果就相同。在本书余下的部分，我们会在每章开头设置一次种子。

```{index} RandomState
```

```{index} see: RandomState; 种子
```

````{note}
使用 `np.random.seed` 时，你设置的其实是 `numpy` 包的*默认随机数生成器*的种子。使用全局默认随机数生成器比其他方法更简单，但也有一些潜在缺点。例如，你可能没有注意到的其他代码（比如藏在某个包内部的代码）有可能*也*调用 `np.random.seed`，从而以你不希望的方式改变分析结果。此外，并非*所有*函数都使用 `numpy` 的随机数生成器，有些可能用的是完全不同的生成器。这种情况下，设置 `np.random.seed` 也许并不能让整个分析可复现。

在本书中，我们一般只使用能与 `numpy` 默认随机数生成器很好配合的包，所以沿用 `np.random.seed` 即可。如果你希望对分析中的随机性有更精细的控制，可以在分析开始时创建一个 `numpy` 的 [`Generator` 对象](https://numpy.org/doc/stable/reference/random/generator.html)，再把它传给许多 `pandas` 和 `scikit-learn` 函数都提供的 `random_state` 参数。这些函数会用你的 `Generator` 生成随机数，而不用 `numpy` 的默认生成器。例如，用一个 `seed` 值设为 1 的 `Generator` 对象就能重现前面的例子，我们再次得到相同的数字列表。（译注：to_list() 返回的是 Python 列表，原文此处把输出误写成了 array([...])，译文已改为列表形式。）
```python
from numpy.random import Generator, PCG64
rng = Generator(PCG64(seed=1))
random_numbers1_third = nums_0_to_9.sample(n=10, random_state=rng).to_list()
random_numbers1_third
```
```text
[2, 9, 6, 4, 0, 3, 1, 7, 8, 5]
```
```python
random_numbers2_third = nums_0_to_9.sample(n=10, random_state=rng).to_list()
random_numbers2_third
```
```text
[9, 5, 3, 0, 8, 4, 2, 1, 6, 7]
```

````

## 使用 `scikit-learn` 评估性能

```{index} scikit-learn, 可视化; 散点图
```

现在回到评估分类器上来！在 Python 中，`scikit-learn` 包既能做 K 近邻分类，也能评估分类结果的好坏。我们用一个例子来看看，如何借助 `scikit-learn` 中的工具、使用上一章的乳腺癌数据集来评估分类器。分析从加载所需的包、读入乳腺癌数据开始，然后快速画一张肿瘤细胞凹度（Concavity）与光滑度（Smoothness）的散点图，颜色表示诊断结果，如{numref}`fig:06-precode` 所示。你还会注意到，我们按照{numref}`randomseeds`中的说明，用 `np.random.seed` 函数设置了随机种子。

```{code-cell} ipython3
:tags: ["remove-output"]
# load packages
import altair as alt
import pandas as pd
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")

# set the seed
np.random.seed(1)

# load data
cancer = pd.read_csv("data/wdbc_unscaled.csv")
# re-label Class "M" as "Malignant", and Class "B" as "Benign"
cancer["Class"] = cancer["Class"].replace({
    "M" : "Malignant",
    "B" : "Benign"
})

# create scatter plot of tumor cell concavity versus smoothness,
# labeling the points be diagnosis class

perim_concav = alt.Chart(cancer).mark_circle().encode(
    x=alt.X("Smoothness").scale(zero=False),
    y="Concavity",
    color=alt.Color("Class").title("Diagnosis")
)
perim_concav
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("fig:06-precode", perim_concav)
```

:::{glue:figure} fig:06-precode
:name: fig:06-precode

肿瘤细胞凹度与光滑度的散点图，颜色表示诊断标签。
:::



+++

### 划分训练集与测试集

一旦确定了要回答的预测性问题，并做了一些初步探索，接下来就要把数据划分为训练集和测试集。通常训练集占数据的 50% 到 95%，测试集则是剩下的 5% 到 50%；这样做的道理是，你需要在训练出准确的模型（使用更大的训练集）与获得准确的性能评估（使用更大的测试集）之间做出权衡取舍。这里我们用 75% 的数据训练，25% 的数据测试。

+++

```{index} scikit-learn; train_test_split, 打乱, 分层
```

`scikit-learn` 的 `train_test_split` 函数会替我们完成划分数据的过程。使用 `train_test_split` 时，我们可以指定两个很重要的参数，以确保由测试数据得到的准确率估计值合理。第一，设置 `shuffle=True`（这是默认值）表示划分之前会先打乱数据，这样数据中存在的任何顺序都不会影响最终进入训练集和测试集的数据。第二，把 `stratify` 参数指定为训练集中的响应变量，函数就会按类别标签对数据**分层**，以保证各个类别进入训练集和测试集的比例大致相同。例如，在我们的数据集中，约 63% 的观测来自良性类别（`Benign`），37% 来自恶性类别（`Malignant`）；因此把 `stratify` 指定为类别列，就能保证训练数据中约 63% 是良性的、37% 是恶性的，测试数据中也存在同样的比例。

下面我们用 `train_test_split` 函数来创建训练集和测试集。首先需要从 `sklearn` 包中导入这个函数。然后指定 `train_size=0.75`，让原始数据集的 75% 进入训练集。我们还会把 `stratify` 参数设为类别型标签变量（这里就是 `cancer["Class"]`），以保证训练子集和测试子集中每一类观测的比例都正确。

```{code-cell} ipython3
:tags: [remove-cell]
# seed hacking
np.random.seed(3)
```

```{code-cell} ipython3
from sklearn.model_selection import train_test_split

cancer_train, cancer_test = train_test_split(
    cancer, train_size=0.75, stratify=cancer["Class"]
)
cancer_train.info()
```

```{code-cell} ipython3
cancer_test.info()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cancer_train_nrow", "{:d}".format(len(cancer_train)))
glue("cancer_test_nrow", "{:d}".format(len(cancer_test)))
```

```{index} DataFrame; info
```

从上方的 `info` 方法可以看出，训练集包含 {glue:text}`cancer_train_nrow` 条观测，而测试集包含 {glue:text}`cancer_test_nrow` 条观测。这对应 75% / 25% 的训练/测试划分，正是我们想要的。回忆{numref}`第 %s 章 <classification1>`可知，我们用 `info` 方法来预览数据框的行数、变量名、数据类型以及缺失项。

```{index} Series; value_counts
```

把 `value_counts` 方法的 `normalize` 参数设为 `True`，就能求出 `cancer_train` 中恶性和良性类别所占的百分比。可以看到，训练数据中约有 {glue:text}`cancer_train_b_prop`% 是良性的，{glue:text}`cancer_train_m_prop`% 是恶性的，这说明划分数据时各类别的比例大致得到了保留。

```{code-cell} ipython3
cancer_train["Class"].value_counts(normalize=True)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cancer_train_b_prop", "{:0.0f}".format(cancer_train["Class"].value_counts(normalize=True)["Benign"]*100))
glue("cancer_train_m_prop", "{:0.0f}".format(cancer_train["Class"].value_counts(normalize=True)["Malignant"]*100))
```

### 预处理数据

正如上一章所说，K 近邻对预测变量的标度很敏感，所以我们应该先做一些预处理，把它们标准化。此外还要注意一点：构建标准化预处理器时**只能使用训练数据**。这样就能保证测试数据不会影响模型训练的任何环节。标准化预处理器建好之后，我们再把它分别应用到训练数据集和测试数据集上。

+++

```{index} scikit-learn; Pipeline, scikit-learn; make_column_transformer, scikit-learn; StandardScaler
```

好在只要把各个分析步骤包进 `Pipeline`，`scikit-learn` 就会帮我们正确处理这件事，就像{numref}`第 %s 章 <classification1>`中那样。所以下面我们和之前一样，用 `make_column_transformer` 来构造并准备好预处理器。

```{code-cell} ipython3
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer

cancer_preprocessor = make_column_transformer(
    (StandardScaler(), ["Smoothness", "Concavity"]),
)
```

### 训练分类器

现在我们已经把原始数据集划分成训练集和测试集，可以借助上一章学到的技术，只用训练集来构建 K 近邻分类器。这里先把近邻个数 $K$ 取为 3，并且只从 `cancer_train` 数据框中选取凹度和光滑度这两个预测变量。首先从 `sklearn` 中导入 `KNeighborsClassifier` 模型和 `make_pipeline`。然后和之前一样创建模型对象，用 `make_pipeline` 函数把模型对象和预处理器组合成 `Pipeline`，最后用 `fit` 方法构建分类器。

```{code-cell} ipython3
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline

knn = KNeighborsClassifier(n_neighbors=3)

X = cancer_train[["Smoothness", "Concavity"]]
y = cancer_train["Class"]

knn_pipeline = make_pipeline(cancer_preprocessor, knn)
knn_pipeline.fit(X, y)

knn_pipeline
```

### 预测测试集中的标签

```{index} scikit-learn; predict
```

现在我们已经有了 K 近邻分类器对象，可以用它来预测测试集的类别标签，并在原始测试数据中添加一列预测结果。`Class` 变量存放的是实际诊断结果，而 `predicted` 存放的是分类器给出的预测诊断结果。请注意，下面输出的数据框中只打印了 `ID`、`Class` 和 `predicted` 这三个变量。

```{code-cell} ipython3
cancer_test["predicted"] = knn_pipeline.predict(cancer_test[["Smoothness", "Concavity"]])
cancer_test[["ID", "Class", "predicted"]]
```

(eval-performance-clasfcn2)=
### 评估性能

```{index} scikit-learn; score, scikit-learn; precision_score, scikit-learn; recall_score
```

最后，我们来评估分类器的性能。首先看准确率。为此要使用 `score` 方法，并指定两个参数：预测变量和实际标签。预测变量传入我们之前调用 `predict` 做预测时所用的同一份测试数据，实际标签则用 `cancer_test["Class"]` Series 给出。

```{code-cell} ipython3
knn_pipeline.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
```

```{code-cell} ipython3
:tags: [remove-cell]
from sklearn.metrics import recall_score, precision_score

cancer_acc_1 = knn_pipeline.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
cancer_prec_1 = precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label="Malignant"
)
cancer_rec_1 = recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label="Malignant"
)

glue("cancer_acc_1", "{:0.0f}".format(100*cancer_acc_1))
glue("cancer_prec_1", "{:0.0f}".format(100*cancer_prec_1))
glue("cancer_rec_1", "{:0.0f}".format(100*cancer_rec_1))
```

+++

输出显示，分类器在测试数据上的估计准确率为 {glue:text}`cancer_acc_1`%。要计算精确率和召回率，可以使用 `scikit-learn` 的 `precision_score` 和 `recall_score` 函数。我们把 `Class` 变量中的真实标签作为 `y_true` 参数，把 `predicted` 变量中的预测标签作为 `y_pred` 参数，再用 `pos_label` 参数指定应把哪个标签视为正类。
```{code-cell} ipython3
from sklearn.metrics import recall_score, precision_score

precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label="Malignant"
)
```

```{code-cell} ipython3
recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label="Malignant"
)
```
输出显示，分类器在测试数据上的估计精确率和召回率分别为 {glue:text}`cancer_prec_1`% 和 {glue:text}`cancer_rec_1`%。最后，我们可以用 `pandas` 的 `crosstab` 函数查看分类器的*混淆矩阵*。`crosstab` 函数接收两个参数：先是实际标签，然后是预测标签。请注意，`crosstab` 会按字母顺序排列各列，但正类标签仍然是 `Malignant`，即使它并不像本章前面那个示例混淆矩阵那样位于左上角。

```{index} crosstab
```

```{code-cell} ipython3
pd.crosstab(
    cancer_test["Class"],
    cancer_test["predicted"]
)
```

```{code-cell} ipython3
:tags: [remove-cell]
_ctab = pd.crosstab(cancer_test["Class"],
            cancer_test["predicted"]
           )

c11 = _ctab["Malignant"]["Malignant"]
c00 = _ctab["Benign"]["Benign"]
c10 = _ctab["Benign"]["Malignant"] # classify benign, true malignant
c01 = _ctab["Malignant"]["Benign"] # classify malignant, true benign

glue("confu11", "{:d}".format(c11))
glue("confu00", "{:d}".format(c00))
glue("confu10", "{:d}".format(c10))
glue("confu01", "{:d}".format(c01))
glue("confu11_00", "{:d}".format(c11 + c00))
glue("confu10_11", "{:d}".format(c10 + c11))
glue("confu_fal_neg", "{:0.0f}".format(100 * c10 / (c10 + c11)))
glue("confu_accuracy", "{:.2f}".format(100*(c00+c11)/(c00+c11+c01+c10)))
glue("confu_precision", "{:.2f}".format(100*c11/(c11+c01)))
glue("confu_recall", "{:.2f}".format(100*c11/(c11+c10)))
glue("confu_precision_0", "{:0.0f}".format(100*c11/(c11+c01)))
glue("confu_recall_0", "{:0.0f}".format(100*c11/(c11+c10)))
```

混淆矩阵显示，有 {glue:text}`confu11` 条观测被正确预测为恶性，{glue:text}`confu00` 条被正确预测为良性。矩阵还显示分类器犯了一些错误：它把 {glue:text}`confu10` 条实际为恶性的观测判成了良性，把 {glue:text}`confu01` 条实际为良性的观测判成了恶性。用前面给出的公式可以算出，准确率、精确率和召回率的数值与 Python 报告的结果一致。

```{code-cell} ipython3
:tags: [remove-cell]

from IPython.display import display, Math
# accuracy string
acc_eq_str = r"\mathrm{accuracy} = \frac{\mathrm{number \; of  \; correct  \; predictions}}{\mathrm{total \;  number \;  of  \; predictions}} = \frac{"
acc_eq_str += str(c00) + "+" + str(c11) + "}{" + str(c00) + "+" + str(c11) + "+" + str(c01) + "+" + str(c10) + "} = " + str( np.round(100*(c00+c11)/(c00+c11+c01+c10),2))
acc_eq_math = Math(acc_eq_str)
glue("acc_eq_math_glued", acc_eq_math)

prec_eq_str = r"\mathrm{precision} = \frac{\mathrm{number \; of  \; correct  \; positive \; predictions}}{\mathrm{total \;  number \;  of  \; positive \; predictions}} = \frac{"
prec_eq_str += str(c11) + "}{" + str(c11) + "+" + str(c01) + "} = " + str( np.round(100*c11/(c11+c01), 2))
prec_eq_math = Math(prec_eq_str)
glue("prec_eq_math_glued", prec_eq_math)

rec_eq_str = r"\mathrm{recall} = \frac{\mathrm{number \; of  \; correct  \; positive \; predictions}}{\mathrm{total \;  number \;  of  \; positive \; test \; set \; observations}} = \frac{"
rec_eq_str += str(c11) + "}{" + str(c11) + "+" + str(c10) + "} = " + str( np.round(100*c11/(c11+c10), 2))
rec_eq_math = Math(rec_eq_str)
glue("rec_eq_math_glued", rec_eq_math)
```

```{glue:math} acc_eq_math_glued
```	

```{glue:math} prec_eq_math_glued
```	

```{glue:math} rec_eq_math_glued
```	

+++

### 批判性地分析性能

现在我们知道，分类器在测试数据集上的准确率为 {glue:text}`cancer_acc_1`%，精确率为 {glue:text}`cancer_prec_1`%，召回率为 {glue:text}`cancer_rec_1`%。听起来相当不错！等等，这*真的*好吗？还是说我们需要更高的数值？

```{index} 准确率; 评估, 精确率; 评估, 召回率; 评估
```

一般来说，准确率（以及适用时的精确率和召回率）多高才算*好*，取决于具体应用；你必须结合自己正在解决的问题，批判性地分析准确率。举例来说，假如我们要为一种 99% 的时间都是良性的肿瘤构建分类器，那么准确率为 99% 的分类器也算不上多惊人（一直猜良性就行了！）。除了准确率，我们还要考虑精确率和召回率：前面提到过，分类器所犯错误的*种类*在许多应用中同样重要。在前面那个 99% 的观测都是良性的例子里，实际类别是“恶性”时分类器却预测“良性”（假阴性），后果可能非常严重，因为病人可能因此得不到应有的医疗照护。反过来，实际类别是“良性”时分类器却猜“恶性”（假阳性），后果可能没那么严重，因为病人接下来很可能会去看医生，由医生给出专业诊断。换句话说，为了获得高召回率，我们愿意牺牲一些精确率。这就是为什么除了准确率，还要看混淆矩阵。

```{index} 分类; 多数类
```

不过，任何分类问题都有一个方便的基准可供比较：*多数类分类器*。多数类分类器*总是*猜测训练数据中的多数类标签，完全不看预测变量的取值。在考虑准确率时，它能帮你对数值规模有个大致概念。如果多数类分类器在某个问题上得到 90% 的准确率，那你就会希望自己的 K 近邻分类器做得比这更好。如果你的分类器比多数类分类器有明显提升，这就说明至少你的方法从预测变量中提取出了一些有用的信息。不过要小心：比多数类分类器表现更好，并不*必然*意味着这个分类器对你的应用来说已经足够好。

举个例子，在乳腺癌数据中，回忆一下训练数据里良性和恶性观测的比例：

```{code-cell} ipython3
cancer_train["Class"].value_counts(normalize=True)
```

由于良性类别占训练数据的大多数，多数类分类器会*总是*预测新观测为良性。多数类分类器的估计准确率通常与训练数据中多数类的比例相当接近。在这个例子里，我们会猜测多数类分类器的准确率大约为 {glue:text}`cancer_train_b_prop`%。而我们构建的 K 近邻分类器比它好不少，准确率为 {glue:text}`cancer_acc_1`%。这意味着从准确率的角度看，K 近邻分类器比基本的多数类分类器提升了很多。太棒了！但我们仍要谨慎：在这个应用中，不让任何恶性肿瘤被误诊很可能至关重要，以免漏掉真正需要治疗的病人。上面的混淆矩阵显示，这个分类器确实把相当多的恶性肿瘤误诊成了良性（{glue:text}`confu10_11` 个恶性肿瘤中有 {glue:text}`confu10` 个，也就是 {glue:text}`confu_fal_neg`%！）。所以，尽管准确率比多数类分类器有所提升，我们的批判性分析表明，这个分类器在这个应用中的性能可能并不合适。

+++

## 调优分类器

```{index} 参数
```

```{index} see: 调优参数; 参数
```

统计学和机器学习中的绝大多数预测模型都有*超参数（hyperparameter）*。*超参数*是必须事先选定、并决定模型某方面行为方式的数值。例如，在 K 近邻分类算法中，$K$ 就是我们必须选定的超参数，它决定有多少个近邻参与类别投票。选取不同的 $K$ 值，就会得到做出不同预测的不同分类器。

那么，我们该如何选取 $K$ 的*最佳*取值，也就是*调优*模型呢？能不能用一套有章可循的方法来完成这个选择？本书将专注于最大化分类器的准确率。理想情况下，我们希望设法让分类器在*它尚未见过*的数据上取得最高准确率。但在构建模型的过程中，我们不能使用测试数据集。所以我们会沿用之前评估分类器时的同一个技巧：把*训练数据本身*拆成两个子集，用其中一个训练模型，再用另一个评估模型。本节将介绍这一过程的细节，以及如何借助它为自己的分类器挑选一个好的超参数取值。

**还要记住**：在调优过程中不要碰测试集。调优是模型训练的一部分！

+++

### 交叉验证

```{index} 验证集
```

选择超参数 $K$ 的第一步，是能够只用训练数据就评估分类器。如果这一点做得到，我们就能仅凭训练数据比较分类器在不同 $K$ 取值下的性能，并挑出最好的那一个。正如本节开头所说，做法是把训练数据划分开，用其中一部分训练，用另一部分评估。用来评估的那部分训练数据，通常称为**验证集（validation set）**。

不过，它与前面做过的训练/测试划分有一个关键区别。具体来说，那时我们只能对数据做*一次划分*。因为归根到底，我们要产出的只是一个分类器；要是我们对数据做了多种不同的训练/测试划分，就会造出多个不同的分类器。而在调优分类器的过程中，我们完全可以基于训练数据的多种划分造出多个分类器，逐一评估，再根据*全部*结果选择一个超参数取值。如果只对整体训练数据划分*一次*，那么选出的最佳超参数就会严重依赖哪些数据碰巧落进了验证集。改用多种不同的训练/验证划分，也许能得到更准确的准确率估计值，从而为整体训练数据选出更好的近邻个数 $K$。

我们用 Python 来试试这个想法！具体来说，对整体训练数据生成五组不同的训练/验证划分，训练五个不同的 K 近邻模型，并评估它们的准确率。先从只划分一次开始。

```{code-cell} ipython3
# create the 25/75 split of the *training data* into sub-training and validation
cancer_subtrain, cancer_validation = train_test_split(
    cancer_train, train_size=0.75, stratify=cancer_train["Class"]
)

# fit the model on the sub-training data
knn = KNeighborsClassifier(n_neighbors=3)
X = cancer_subtrain[["Smoothness", "Concavity"]]
y = cancer_subtrain["Class"]
knn_pipeline = make_pipeline(cancer_preprocessor, knn)
knn_pipeline.fit(X, y)

# compute the score on validation data
acc = knn_pipeline.score(
    cancer_validation[["Smoothness", "Concavity"]],
    cancer_validation["Class"]
)
acc
```

```{code-cell} ipython3
:tags: [remove-cell]

accuracies = [acc]
for i in range(1, 5):
    # create the 25/75 split of the training data into training and validation
    cancer_subtrain, cancer_validation = train_test_split(
        cancer_train, test_size=0.25
    )

    # fit the model on the sub-training data
    knn = KNeighborsClassifier(n_neighbors=3)
    X = cancer_subtrain[["Smoothness", "Concavity"]]
    y = cancer_subtrain["Class"]
    knn_pipeline = make_pipeline(cancer_preprocessor, knn).fit(X, y)

    # compute the score on validation data
    accuracies.append(knn_pipeline.score(
        cancer_validation[["Smoothness", "Concavity"]],
        cancer_validation["Class"]
       ))
avg_accuracy = np.round(np.array(accuracies).mean()*100,1)
accuracies = list(np.round(np.array(accuracies)*100, 1))
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("acc_seed1", "{:0.1f}".format(100 * acc))
glue("avg_5_splits", "{:0.1f}".format(avg_accuracy))
glue("accuracies", "[" + "%, ".join(["{:0.1f}".format(acc) for acc in accuracies]) + "%]")
```
```{code-cell} ipython3
:tags: [remove-cell]

```

用这次划分得到的准确率估计值是 {glue:text}`acc_seed1`%。下面把上面的代码再重复 4 次，就又得到 4 组划分。于是我们有了五种不同的数据打乱方式，也就有了五个不同的准确率取值：{glue:text}`accuracies`。这些取值未必有哪一个比别的“更正确”；它们只是用整体训练数据构建的分类器真实内在准确率的五个估计值。把这些估计值取平均（这里是 {glue:text}`avg_5_splits`%），就能对分类器的准确率得到一个总的判断；这样做可以削弱某一个（不）走运的验证集对估计值的影响。

```{index} 交叉验证
```

实践中我们并不用随机划分，而是采用更讲章法的划分流程，让数据集中的每条观测只在验证集中出现一次。这种策略叫作**交叉验证（cross-validation）**。在**交叉验证**中，我们把**整体训练数据**均分成 $C$ 个等份。接着依次把 $1$ 个等份用作**验证集**，把剩下的 $C-1$ 个等份合起来作**训练集**。该流程见{numref}`fig:06-cv-image`。这里用了数据集里 $C=5$ 个不同的等份，于是**验证集**有 5 种不同的取法；我们称之为 *5 折*交叉验证。

+++

```{figure} img/classification2/cv.png
:name: fig:06-cv-image

5 折交叉验证。
```


+++

```{index} 交叉验证; cross_validate, scikit-learn; cross_validate
```

要在 Python 中用 `scikit-learn` 做 5 折交叉验证，得用另一个函数：`cross_validate`。这个函数要求我们把建模用的 `Pipeline` 作为 `estimator` 参数传入，把折数作为 `cv` 参数传入，把训练数据的预测变量和标签作为 `X` 和 `y` 参数传入。`cross_validate` 的输出是一个字典，所以我们用 `pd.DataFrame` 把它转成 `pandas` 数据框，以便查看得更清楚。请注意，`cross_validate` 会自动对每个训练折和验证折中的类别做分层。

```{code-cell} ipython3
from sklearn.model_selection import cross_validate

knn = KNeighborsClassifier(n_neighbors=3)
cancer_pipe = make_pipeline(cancer_preprocessor, knn)
X = cancer_train[["Smoothness", "Concavity"]]
y = cancer_train["Class"]
cv_5_df = pd.DataFrame(
    cross_validate(
        estimator=cancer_pipe,
        cv=5,
        X=X,
        y=y
    )
)

cv_5_df
```

```{index} see: sem;标准误
```

```{index} 标准误, DataFrame;agg
```

我们关心的验证得分在 `test_score` 列里。接着可以对各折上分类器的验证准确率聚合出*均值*和*标准误（standard error）*。把均值（`mean`）看作准确率的估计值，标准误（`sem`）则衡量这个均值有多不确定。详细讨论超出本章范围；大致说来，如果估计均值为 {glue:text}`cv_5_mean`、标准误为 {glue:text}`cv_5_std`，就可以指望分类器的*真实*平均准确率大致落在 {glue:text}`cv_5_lower`% 到 {glue:text}`cv_5_upper`% 之间（当然也可能落在这个范围之外）。指标数据框中的其他列可以忽略。

```{code-cell} ipython3
cv_5_metrics = cv_5_df.agg(["mean", "sem"])
cv_5_metrics
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cv_5_mean", "{:.2f}".format(cv_5_metrics.loc["mean", "test_score"]))
glue("cv_5_std", "{:.2f}".format(cv_5_metrics.loc["sem", "test_score"]))
glue("cv_5_upper",
    "{:0.0f}".format(
        100
        * (
            round(cv_5_metrics.loc["mean", "test_score"], 2)
            + round(cv_5_metrics.loc["sem", "test_score"], 2)
        )
    )
)
glue("cv_5_lower",
    "{:0.0f}".format(
        100
        * (
            round(cv_5_metrics.loc["mean", "test_score"], 2)
            - round(cv_5_metrics.loc["sem", "test_score"], 2)
        )
    )
)
```

折数可以任选，通常用得越多，准确率估计值就越好（标准误越小）。不过我们受算力限制：折数越多，计算量越大，跑完分析也就越费时间。所以做交叉验证时，需要权衡数据规模、算法的速度（例如 K 近邻）以及你电脑的速度。实践中这是个反复试错的过程，不过通常把 $C$ 取成 5 或 10。下面我们试试 10 折交叉验证，看标准误会不会小一些。

```{code-cell} ipython3
:tags: [remove-output]
cv_10 = pd.DataFrame(
    cross_validate(
        estimator=cancer_pipe,
        cv=10,
        X=X,
        y=y
    )
)

cv_10_df = pd.DataFrame(cv_10)
cv_10_metrics = cv_10_df.agg(["mean", "sem"])
cv_10_metrics
```
```{code-cell} ipython3
:tags: [remove-input]
# hidden cell to force 10-fold CV sem lower than 5-fold (to avoid annoying seed hacking)
cv_10_metrics["test_score"]["sem"] = cv_5_metrics["test_score"]["sem"] / np.sqrt(2)
cv_10_metrics
```

```{index} 交叉验证; 折
```

在这个例子里，用 10 折代替 5 折交叉验证，标准误确实略微下降了。其实由于数据划分的随机性，增加折数时标准误有时反而会*升高*！把折数大幅增加，可以让标准误的下降更明显。下面的代码展示了 $C = 50$ 时的结果；选这么大的折数，实际运行可能要很久，所以我们一般还是用 5 或 10。

```{code-cell} ipython3
:tags: [remove-output]
cv_50_df = pd.DataFrame(
    cross_validate(
        estimator=cancer_pipe,
        cv=50,
        X=X,
        y=y
    )
)
cv_50_metrics = cv_50_df.agg(["mean", "sem"])
cv_50_metrics
```

```{code-cell} ipython3
:tags: [remove-input]
# hidden cell to force 10-fold CV sem lower than 5-fold (to avoid annoying seed hacking)
cv_50_metrics["test_score"]["sem"] = cv_5_metrics["test_score"]["sem"] / np.sqrt(10)
cv_50_metrics
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cv_10_mean", "{:0.0f}".format(100 * cv_10_metrics.loc["mean", "test_score"]))
```

### 超参数取值选择

用 5 折和 10 折交叉验证，我们估计出分类器的预测准确率大约在 {glue:text}`cv_10_mean`% 上下。这个结果好不好，完全取决于数据分析的下游应用。就当前情形而言，我们要预测的是肿瘤诊断，一旦误判，代价可能是昂贵且有伤害性的化疗/放疗，甚至患者死亡。所以在这个应用里，我们希望能做得比 {glue:text}`cv_10_mean`% 更好。

要改进分类器，我们有一个超参数可选：近邻个数 $K$。既然交叉验证能帮我们评估分类器的准确率，就可以用它在一个合理范围内为每个 $K$ 取值算出准确率，再挑出准确率最高的那个 $K$。`scikit-learn` 包集合提供了名为 `GridSearchCV` 的内置功能，能自动帮我们处理这些细节。使用 `GridSearchCV` 之前，需要新建一条流水线，其中的 `KNeighborsClassifier` 不指定近邻个数。

```{index} see: make_pipeline; scikit-learn
```
```{index} scikit-learn;make_pipeline
```

```{code-cell} ipython3
knn = KNeighborsClassifier()
cancer_tune_pipe = make_pipeline(cancer_preprocessor, knn)
```

+++

接下来指定要为每个可调超参数尝试的取值网格。这用一个 Python 字典来做：键是待调优超参数的标识符，值是调优时要尝试的超参数取值列表。用流水线上的 `get_params` 方法可以查出参数的“标识符”。
```{code-cell} ipython3
cancer_tune_pipe.get_params()
```
哇，这里面的东西*真不少*！稍微翻一翻这堆东西，会看到一个格外显眼的超参数标识符：`"kneighborsclassifier__n_neighbors"`。这个标识符把流水线中 K 近邻分类步骤的名字 `kneighborsclassifier` 与参数名 `n_neighbors` 拼在一起。现在我们构造 `parameter_grid` 字典，由它来告诉 `GridSearchCV` 该尝试哪些超参数取值。注意，想要指定多个待调优的超参数，只要在字典里写多个键值对；不过这里只需调优近邻个数。
```{code-cell} ipython3
parameter_grid = {
    "kneighborsclassifier__n_neighbors": range(1, 100, 5),
}
```
前面用到的 Python `range` 函数可以用来指定一串取值。第一个参数是起始数字（这里是 `1`），第二个参数*比最后一个数字大 1*（这里为 `100`），第三个参数是序列的步长，也就是相邻两项之差（这里是 `5`）（译注：原文此处误作“要跳过的数字个数”，实际跳过 4 个数）。所以这里生成的序列是 1, 6, 11, 16, ..., 96。如果改成 `range(0, 100, 5)`，得到的序列是 0, 5, 10, 15, ..., 90, 95。100 不包含在序列内，因为第二个参数*比序列中最后一个可能的数字大 1*（译注：原文此处误作“第三个参数”）。`range` 还有两种有用的用法。只给 `range` 传一个参数时，Python 从 0 开始数到这个数字。所以 `range(4)` 等同于 `range(0, 4, 1)`，生成的序列是 0, 1, 2, 3。给 `range` 传两个参数时，Python 从第一个数字开始数到第二个数字。所以 `range(1, 4)` 等同于 `range(1, 4, 1)`，生成的序列是 `1, 2, 3`。

```{index} 交叉验证; GridSearchCV, scikit-learn; GridSearchCV, scikit-learn; RandomizedSearchCV
```

好了！终于可以创建 `GridSearchCV` 对象了。先从 `sklearn` 包导入它。然后把 `cancer_tune_pipe` 流水线传给 `estimator` 参数，把 `parameter_grid` 传给 `param_grid` 参数，并指定 `cv=10` 折。注意此时还不会真正开始调优；和前面一样，我们还得调用 `fit` 方法。

```{code-cell} ipython3
from sklearn.model_selection import GridSearchCV

cancer_tune_grid = GridSearchCV(
    estimator=cancer_tune_pipe,
    param_grid=parameter_grid,
    cv=10
)
```

现在对 `GridSearchCV` 对象调用 `fit` 方法，开始调优。照例把训练数据的预测变量和标签作为两个参数传给 `fit`。输出的 `cv_results_` 属性里，有每个 `n_neighbors` 取值对应的交叉验证准确率估计值，但格式不便使用。我们用 `pd.DataFrame` 把它包起来，让结果更容易看懂，然后打印结果的 `info`。

```{code-cell} ipython3
cancer_tune_grid.fit(
    cancer_train[["Smoothness", "Concavity"]],
    cancer_train["Class"]
)
accuracies_grid = pd.DataFrame(cancer_tune_grid.cv_results_)
accuracies_grid.info()
```

这里的信息很多，不过我们最关心三个量：近邻个数（`param_kneighbors_classifier__n_neighbors`）（译注：原文这里的列名有误，多写了一个下划线，实际应为 param_kneighborsclassifier__n_neighbors）、交叉验证准确率估计值（`mean_test_score`）以及准确率估计值的标准误。遗憾的是，`GridSearchCV` 并不直接输出每个交叉验证准确率的标准误；但它*确实*会输出标准*差*（`std_test_score`）。把标准差除以折数的平方根，就得到标准误，即

$$\text{Standard Error} = \frac{\text{Standard Deviation}}{\sqrt{\text{Number of Folds}}}.$$

我们还会把参数名列重命名得更易读，并删掉已不再使用的 `std_test_score` 列。

```{code-cell} ipython3
accuracies_grid["sem_test_score"] = accuracies_grid["std_test_score"] / 10**(1/2)
accuracies_grid = (
    accuracies_grid[[
        "param_kneighborsclassifier__n_neighbors",
        "mean_test_score",
        "sem_test_score"
    ]]
    .rename(columns={"param_kneighborsclassifier__n_neighbors": "n_neighbors"})
)
accuracies_grid
```

画出准确率随 $K$ 变化的图，就能判断哪个近邻个数最好，如{numref}`fig:06-find-k` 所示。这里用简写 `point=True`，把散点与折线叠加在同一张图里。

```{code-cell} ipython3
:tags: [remove-output]

accuracy_vs_k = alt.Chart(accuracies_grid).mark_line(point=True).encode(
    x=alt.X("n_neighbors").title("Neighbors"),
    y=alt.Y("mean_test_score")
        .scale(zero=False)
        .title("Accuracy estimate")
)

accuracy_vs_k
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:06-find-k", accuracy_vs_k)
glue("best_k_unique", "{:d}".format(accuracies_grid["n_neighbors"][accuracies_grid["mean_test_score"].idxmax()]))
glue("best_acc", "{:.1f}".format(accuracies_grid["mean_test_score"].max()*100))
```

:::{glue:figure} fig:06-find-k
:name: fig:06-find-k

估计准确率随近邻个数变化的图。
:::

也可以通过访问拟合后的 `GridSearchCV` 对象的 `best_params_` 属性，用代码取出准确率最高的近邻个数。注意，像上面那样把结果画出来仍然有用，因为这能额外提供模型性能如何变化的信息。
```{code-cell} ipython3
cancer_tune_grid.best_params_
```

+++

把近邻个数设为 $K =$ {glue:text}`best_k_unique`，得到的交叉验证准确率估计值最高（{glue:text}`best_acc`%）。但这里并没有精确或完美的答案；从 $K = 30$ 到 $80$ 左右，选哪个都还说得过去，因为这些取值下分类器准确率的差异很小。记住：你在图上看到的取值都只是分类器真实准确率的*估计值*。虽然 $K =$ {glue:text}`best_k_unique` 在图上的确比别的取值高，但这并不意味着分类器在这个超参数取值下确实更准确！一般来说，选择 $K$（以及其他预测模型的其他超参数）时，我们要找的取值应当满足：

- 准确率大致达到最优，这样模型的预测大体上是准确的；
- 把取值换成邻近的某个值（例如加上或减去一个很小的数），准确率不会下降太多，这样即便存在不确定性，我们的选择依然可靠；
- 模型训练的成本不至于高得无法承受（例如在我们的情形里，$K$ 太大时预测会变得很昂贵！）。

我们知道，$K =$ {glue:text}`best_k_unique` 给出的估计准确率最高。而且{numref}`fig:06-find-k` 显示，在 $K =$ {glue:text}`best_k_unique` 附近增大或减小 $K$，估计准确率的变化都很小。最后，$K =$ {glue:text}`best_k_unique` 带来的训练计算成本也不至于高得无法承受。综合这三点，我们确实会为分类器选择 $K =$ {glue:text}`best_k_unique`。

+++

### 欠拟合与过拟合

为了再多建立一点直觉：如果我们不断增大近邻个数 $K$，会发生什么？事实上，交叉验证准确率估计值反而会开始下降！我们不妨在 `GridSearchCV` 的 `param_grid` 参数中指定大得多的 $K$ 取值范围来试。{numref}`fig:06-lots-of-ks` 展示了 $K$ 从 1 一直变到接近数据集观测个数时，估计准确率变化的图形。

```{code-cell} ipython3
:tags: [remove-output]

large_param_grid = {
    "kneighborsclassifier__n_neighbors": range(1, 385, 10),
}

large_cancer_tune_grid = GridSearchCV(
    estimator=cancer_tune_pipe,
    param_grid=large_param_grid,
    cv=10
)

large_cancer_tune_grid.fit(
    cancer_train[["Smoothness", "Concavity"]],
    cancer_train["Class"]
)

large_accuracies_grid = pd.DataFrame(large_cancer_tune_grid.cv_results_)

large_accuracy_vs_k = alt.Chart(large_accuracies_grid).mark_line(point=True).encode(
    x=alt.X("param_kneighborsclassifier__n_neighbors").title("Neighbors"),
    y=alt.Y("mean_test_score")
        .scale(zero=False)
        .title("Accuracy estimate")
)

large_accuracy_vs_k
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:06-lots-of-ks", large_accuracy_vs_k)
```

:::{glue:figure} fig:06-lots-of-ks
:name: fig:06-lots-of-ks

许多 K 取值下，准确率估计值随近邻个数变化的图形。
:::

+++

```{index} 欠拟合; 分类
```

**欠拟合（underfitting）**：分类器到底发生了什么，才导致这种结果？随着近邻个数增大，越来越多的训练观测（以及离目标点越来越远的那些观测）都能对新观测的类别“发表意见”。这就产生了一种“平均效应”，使分类器判别肿瘤为恶性还是良性的边界变得平滑，也*更简单*。如果走极端，把 $K$ 设为整个训练集的大小，那么无论新观测长什么样，分类器都会预测同一个标签。一般来说，如果模型*受到训练数据的影响不够*，就说它对数据**欠拟合**。

```{index} 过拟合; 分类
```

**过拟合（overfitting）**：反过来，减小近邻个数时，每个数据点对附近点的表决权都越来越强。由于数据本身带有噪声，判别边界会变得更加“锯齿状”，对应着一个*不那么简单*的模型。如果走极端，令 $K = 1$，那么分类器实际上就是把每个新观测匹配到训练数据集中离它最近的邻居。这和 $K$ 很大的情形一样成问题，因为分类器在新数据上变得不可靠：如果换一个训练集，预测结果会完全不同。一般来说，如果模型*受到训练数据的影响过多*，就说它对数据**过拟合**。

```{code-cell} ipython3
:tags: [remove-cell]
alt.data_transformers.disable_max_rows()

cancer_plot = (
    alt.Chart(
        cancer_train,
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X(
            "Smoothness",
            scale=alt.Scale(
                domain=(
                    cancer_train["Smoothness"].min() * 0.95,
                    cancer_train["Smoothness"].max() * 1.05,
                )
            ),
        ),
        y=alt.Y(
            "Concavity",
            scale=alt.Scale(
                domain=(
                    cancer_train["Concavity"].min() -0.025,
                    cancer_train["Concavity"].max() * 1.05,
                )
            ),
        ),
        color=alt.Color("Class", title="Diagnosis"),
    )
)

X = cancer_train[["Smoothness", "Concavity"]]
y = cancer_train["Class"]

# create a prediction pt grid
smo_grid = np.linspace(
    cancer_train["Smoothness"].min() * 0.95, cancer_train["Smoothness"].max() * 1.05, 100
)
con_grid = np.linspace(
    cancer_train["Concavity"].min() - 0.025, cancer_train["Concavity"].max() * 1.05, 100
)
scgrid = np.array(np.meshgrid(smo_grid, con_grid)).reshape(2, -1).T
scgrid = pd.DataFrame(scgrid, columns=["Smoothness", "Concavity"])

plot_list = []
for k in [1, 7, 20, 300]:
    cancer_pipe = make_pipeline(cancer_preprocessor, KNeighborsClassifier(n_neighbors=k))
    cancer_pipe.fit(X, y)

    knnPredGrid = cancer_pipe.predict(scgrid)
    prediction_table = scgrid.copy()
    prediction_table["Class"] = knnPredGrid

    # add a prediction layer
    prediction_plot = (
        alt.Chart(
            prediction_table,
            title=f"K = {k}"
        )
        .mark_point(opacity=0.2, filled=True, size=20)
        .encode(
            x=alt.X(
                "Smoothness",
                scale=alt.Scale(
                    domain=(
                        cancer_train["Smoothness"].min() * 0.95,
                        cancer_train["Smoothness"].max() * 1.05
                    ),
                    nice=False
                )
            ),
            y=alt.Y(
                "Concavity",
                scale=alt.Scale(
                    domain=(
                        cancer_train["Concavity"].min() -0.025,
                        cancer_train["Concavity"].max() * 1.05
                    ),
                    nice=False
                )
            ),
            color=alt.Color("Class", title="Diagnosis"),
        )
    )
    plot_list.append(cancer_plot + prediction_plot)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue(
    "fig:06-decision-grid-K",
    ((plot_list[0] | plot_list[1])
    & (plot_list[2] | plot_list[3])).configure_legend(
        orient="bottom", titleAnchor="middle"
    ),
)
```

:::{glue:figure} fig:06-decision-grid-K
:name: fig:06-decision-grid-K

K 取值对过拟合与欠拟合的影响。
:::

+++

过拟合和欠拟合都有问题，都会使模型难以很好地泛化到新数据。拟合模型时，我们需要在两者之间取得平衡。这两个效应可以在{numref}`fig:06-decision-grid-K` 中看到，图中展示了把近邻个数 $K$ 分别设为 1、7、20 和 300 时分类器的变化。

+++

### 在测试集上评估

现在 K 近邻分类器已经调好，并设 $K =$ {glue:text}`best_k_unique`，模型构建到此结束，接下来要评估它在留出的测试数据上预测的质量，就像前面在{numref}`eval-performance-clasfcn2`中做的那样。我们首先要用选定的近邻个数，在整个训练数据集上重新训练 K 近邻分类器。好在不必手动完成，`scikit-learn` 会自动帮我们做。要在测试数据上做出预测并评估最优模型的估计准确率，可以用拟合好的 `GridSearchCV` 对象的 `score` 和 `predict` 方法。然后把这些预测传给 `precision`、`recall` 和 `crosstab` 函数，评估估计的精确率与召回率，并打印混淆矩阵（译注：原文把前两个函数写作 precision 和 recall，scikit-learn 中实际的函数名是 precision_score 和 recall_score）。

```{index} scikit-learn;predict, scikit-learn;score, scikit-learn;precision_score, scikit-learn;recall_score, crosstab
```

```{code-cell} ipython3
cancer_test["predicted"] = cancer_tune_grid.predict(
    cancer_test[["Smoothness", "Concavity"]]
)

cancer_tune_grid.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
```

```{code-cell} ipython3
precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
```

```{code-cell} ipython3
recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
```

```{code-cell} ipython3
pd.crosstab(
    cancer_test["Class"],
    cancer_test["predicted"]
)
```
```{code-cell} ipython3
:tags: [remove-cell]
cancer_prec_tuned = precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
cancer_rec_tuned = recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
cancer_acc_tuned = cancer_tune_grid.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
glue("cancer_acc_tuned", "{:0.0f}".format(100*cancer_acc_tuned))
glue("cancer_prec_tuned", "{:0.0f}".format(100*cancer_prec_tuned))
glue("cancer_rec_tuned", "{:0.0f}".format(100*cancer_rec_tuned))
glue("mean_acc_ks", "{:0.0f}".format(100*accuracies_grid["mean_test_score"].mean()))
glue("std3_acc_ks", "{:0.0f}".format(3*100*accuracies_grid["mean_test_score"].std()))
glue("mean_sem_acc_ks", "{:0.0f}".format(100*accuracies_grid["sem_test_score"].mean()))
glue("n_neighbors_max", "{:0.0f}".format(accuracies_grid["n_neighbors"].max()))
glue("n_neighbors_min", "{:0.0f}".format(accuracies_grid["n_neighbors"].min()))
```

乍看之下这有点出人意料：尽管调了近邻个数，分类器的准确率并没有太大变化！我们最初那个 $K =$ 3 的模型（那时我们还不会调优）估计准确率是 {glue:text}`cancer_acc_1`%，而调优后的模型 $K =$ {glue:text}`best_k_unique` 的估计准确率是 {glue:text}`cancer_acc_tuned`%。再看一眼{numref}`fig:06-find-k` 中一系列近邻个数对应的交叉验证准确率估计值，这个结果就不那么让人意外了。从 {glue:text}`n_neighbors_min` 个近邻到大约 {glue:text}`n_neighbors_max` 个近邻，交叉验证准确率估计值的变化只有约 {glue:text}`std3_acc_ks`%，而每个估计值的标准误约为 {glue:text}`mean_sem_acc_ks`%。既然交叉验证准确率估计的是测试集准确率，测试集准确率同样变化不大就是意料之中的事。还要注意，$K =$ 3 的模型精确率为 {glue:text}`cancer_prec_1`%、召回率为 {glue:text}`cancer_rec_1`%，而调优后的模型精确率为 {glue:text}`cancer_prec_tuned`%、召回率为 {glue:text}`cancer_rec_tuned`%。考虑到召回率下降了——请记住，在这个应用里，召回率对于确保找出所有恶性肿瘤患者至关重要——调优后的模型在这种情形下其实可能*更不*受青睐。无论如何，都要对调优结果做批判性分析。为最大化准确率而调优的模型，对某个具体应用来说未必更好。

## 小结

分类算法用一个或多个定量变量来预测另一个类别型变量的取值。具体来说，K 近邻算法先找出训练数据中离新观测最近的 $K$ 个点，再返回这些训练观测的多数类投票结果。把数据随机划分为训练集和测试集，就能对分类器进行调优和评估。训练集用来构建分类器；我们可以通过交叉验证最大化估计准确率，从而对分类器调优（例如选择 K 近邻中的近邻个数）。模型调好之后，再用测试集估计它的准确率。{numref}`fig:06-overview` 总结了整个流程。

+++

```{figure} img/classification2/train-test-overview.png
:name: fig:06-overview

K 近邻分类概述。
```

+++

```{index} scikit-learn;Pipeline, 交叉验证, K 近邻; 分类, 分类
```

使用 `scikit-learn` 完成 K 近邻分类的整体工作流如下：

1. 用 `train_test_split` 函数把数据划分为训练集和测试集。把 `stratify` 参数设为数据框的类别标签列。暂时把测试集放到一边。
2. 创建一个 `Pipeline`，指明预处理步骤和分类器。
3. 给出你想要调优的一组 $K$ 取值，定义参数网格。
4. 用 `GridSearchCV` 估计一系列 $K$ 取值下分类器的准确率。把第 2 步和第 3 步定义的流水线和参数网格分别作为 `estimator` 参数和 `param_grid` 参数传入（译注：原文此处把两个参数的顺序写反了）。
5. 把训练数据传给第 4 步创建的 `GridSearchCV` 实例的 `fit` 方法，执行网格搜索。
6. 选一个 $K$，使交叉验证准确率估计值较高，且把 $K$ 换成邻近取值时该估计值变化不大。
7. 针对最优超参数取值（即 $K$）新建一个模型对象，并调用 `fit` 方法重新训练分类器（译注：原文要求新建模型对象并重新拟合，但 GridSearchCV 的 refit 默认为 True，会自动用最优超参数在整个训练集上重新训练，因此这一步通常不必手动完成）。
8. 用 `score` 方法在测试集上评估分类器的估计准确率。

最近两章我们一直围绕 K 近邻算法展开，但可以用来预测类别标签的方法还有很多。每种算法都各有长短，下面把 K 近邻的这些优缺点总结一下。

**优点：** K 近邻分类

1. 算法简单、直观；
2. 对数据形态几乎没有假设；
3. 既适用于二分类（binary classification，即两类）问题，也适用于多分类（multiclass classification，即类别多于 2 类）问题。

**缺点：** K 近邻分类

1. 训练数据变大时速度会变得很慢；
2. 预测变量很多时可能表现不好；
3. 类别不平衡时可能表现不好。

+++

## 预测变量选择

```{note}
本节不是后续章节的必读内容。收录在此，是给那些有兴趣了解无关变量会如何影响分类器性能、以及如何挑选一部分有用变量充当预测变量的读者。
```

```{index} 无关预测变量
```

调优分类器时，另一个可能很重要的环节，是决定数据中的哪些变量用作预测变量。从只用一个预测变量，到用上数据中的每一个变量，技术上都可以选；K 近邻算法接受任意个数的预测变量。不过，**并非**预测变量越多，预测效果就一定越好！事实上，有时把无关变量也算进来，反而会拉低分类器的性能。

+++ {"toc-hr-collapsed": true}

### 无关预测变量的影响

我们来看一个例子：给 K 近邻算法提供更多预测变量，它的表现反而更差。在这个例子中，我们修改了乳腺癌数据，只保留原始数据里的 `Smoothness`、`Concavity` 和 `Perimeter` 三个变量。随后又用随机数生成器自己造了一些无关变量。对每条观测来说，这些无关变量都以相同的概率取 0 或 1，与 `Class` 变量的取值无关。换句话说，无关变量与 `Class` 变量之间没有任何实质关系。

```{code-cell} ipython3
:tags: [remove-cell]

np.random.seed(4)
cancer_irrelevant = cancer[["Class", "Smoothness", "Concavity", "Perimeter"]]
d = {
    f"Irrelevant{i+1}": np.random.choice(
        [0, 1], size=len(cancer_irrelevant), replace=True
    )
    for i in range(40)  ## in R textbook, it is 500, but the downstream analysis only uses up to 40
}
cancer_irrelevant = pd.concat((cancer_irrelevant, pd.DataFrame(d)), axis=1)
```

```{code-cell} ipython3
cancer_irrelevant[
    ["Class", "Smoothness", "Concavity", "Perimeter", "Irrelevant1", "Irrelevant2"]
]
```

接下来我们构建一系列 K 近邻分类器，它们的预测变量除了 `Smoothness`、`Concavity` 和 `Perimeter`，还包含越来越多的无关变量。具体来说，我们创建 6 个数据集，其中的无关预测变量分别为 0、5、10、15、20 和 40 个。然后为每个数据集构建一个模型，并用 5 折交叉验证调优。{numref}`fig:06-performance-irrelevant-features` 给出了交叉验证准确率估计值随无关预测变量个数的变化。随着无关预测变量增多，分类器的估计准确率不断下降。原因在于，无关变量会为每两条观测之间的距离增加一个随机的量；无关变量越多，这种（随机）影响就越大，也就越会破坏为待预测新观测的类别投票的那组最近邻。

```{code-cell} ipython3
:tags: [remove-cell]

# get accuracies after including k irrelevant features
ks = [0, 5, 10, 15, 20, 40]
fixedaccs = list()
accs = list()
nghbrs = list()

for i in range(len(ks)):
    cancer_irrelevant_subset = cancer_irrelevant.iloc[:, : (4 + ks[i])]
    cancer_preprocessor = make_column_transformer(
        (
            StandardScaler(),
            list(cancer_irrelevant_subset.drop(columns=["Class"]).columns),
        ),
    )
    cancer_tune_pipe = make_pipeline(cancer_preprocessor, KNeighborsClassifier())
    param_grid = {
        "kneighborsclassifier__n_neighbors": range(1, 21),
    }  
    cancer_tune_grid = GridSearchCV(
        estimator=cancer_tune_pipe,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        return_train_score=True,
    )

    X = cancer_irrelevant_subset.drop(columns=["Class"])
    y = cancer_irrelevant_subset["Class"]

    cancer_model_grid = cancer_tune_grid.fit(X, y)
    accuracies_grid = pd.DataFrame(cancer_model_grid.cv_results_)
    sorted_accuracies = accuracies_grid.sort_values(
        by="mean_test_score", ascending=False
    )

    res = sorted_accuracies.iloc[0, :]
    accs.append(res["mean_test_score"])
    nghbrs.append(res["param_kneighborsclassifier__n_neighbors"])

    ## Use fixed n_neighbors=3
    cancer_fixed_pipe = make_pipeline(
        cancer_preprocessor, KNeighborsClassifier(n_neighbors=3)
    )

    cv_5 = cross_validate(estimator=cancer_fixed_pipe, X=X, y=y, cv=5)
    cv_5_metrics = pd.DataFrame(cv_5).agg(["mean", "sem"])
    fixedaccs.append(cv_5_metrics.loc["mean", "test_score"])
```

```{code-cell} ipython3
:tags: [remove-cell]

summary_df = pd.DataFrame(
    {"ks": ks, "nghbrs": nghbrs, "accs": accs, "fixedaccs": fixedaccs}
)
plt_irrelevant_accuracies = (
    alt.Chart(summary_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "accs",
            title="Model Accuracy Estimate",
            scale=alt.Scale(zero=False),
        ),
    )
)
glue("fig:06-performance-irrelevant-features", plt_irrelevant_accuracies)
```

:::{glue:figure} fig:06-performance-irrelevant-features
:name: fig:06-performance-irrelevant-features

纳入无关预测变量的影响。
:::

准确率确实如预期那样下降了，但{numref}`fig:06-performance-irrelevant-features` 有一点出人意料：即使有 40 个无关变量，这个方法仍然优于基准的多数类分类器（准确率约为 {glue:text}`cancer_train_b_prop`%）。这怎么可能？{numref}`fig:06-neighbors-irrelevant-features` 给出了答案：K 近邻分类器的调优过程会靠增加近邻个数，来抵消无关变量带来的额外随机性。当然，由于无关变量给数据带来了大量额外噪声，近邻个数并不会平滑地增加，但总体趋势是上升的。{numref}`fig:06-fixed-irrelevant-features` 印证了这一证据：如果把近邻个数固定为 $K=3$，准确率下降得更快。

```{code-cell} ipython3
:tags: [remove-cell]

plt_irrelevant_nghbrs = (
    alt.Chart(summary_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "nghbrs",
            title="Tuned number of neighbors",
        ),
    )
)
glue("fig:06-neighbors-irrelevant-features", plt_irrelevant_nghbrs)
```

:::{glue:figure} fig:06-neighbors-irrelevant-features
:name: fig:06-neighbors-irrelevant-features

无关预测变量个数不同时调优得到的近邻个数。
:::

```{code-cell} ipython3
:tags: [remove-cell]

melted_summary_df = summary_df.melt(
            id_vars=["ks", "nghbrs"], var_name="Type", value_name="Accuracy"
        )
melted_summary_df["Type"] = melted_summary_df["Type"].apply(lambda x: "Tuned K" if x=="accs" else "K = 3")

plt_irrelevant_nghbrs_fixed = (
    alt.Chart(
        melted_summary_df
    )
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "Accuracy",
            scale=alt.Scale(zero=False),
        ),
        color=alt.Color("Type"),
    )
)
glue("fig:06-fixed-irrelevant-features", plt_irrelevant_nghbrs_fixed)
```

:::{glue:figure} fig:06-fixed-irrelevant-features
:name: fig:06-fixed-irrelevant-features

近邻个数调优与未调优时，准确率随无关预测变量个数的变化。
:::

+++

### 寻找好的预测变量子集

那么，既然不加考虑地把所有变量都当作预测变量并不理想，我们该怎样挑选*应该*使用的变量呢？一个简单办法是依靠你对数据的专业理解，判断哪些变量不太可能是有用的预测变量。例如，我们一直在研究的这份癌症数据中，`ID` 变量只是观测的唯一标识符。它与细胞的任何测量属性都无关，因此不应把 `ID` 变量当作预测变量。当然，这是非常明确的情形。但其余变量就没那么好判断了，它们看起来都是合理的候选。究竟哪个子集能造出最好的分类器，并不清楚。你可以借助可视化和其他探索性分析，帮助判断哪些变量可能有用，但要考虑的变量一多，这个过程既费时又容易出错。因此我们需要一种更系统、更程序化的变量选择方法。总的来说，这个问题很难解决，人们已经针对一些特定的应用场景提出了不少方法。这里我们讨论两种基本的选择方法，作为这一主题的入门。想进一步了解变量选择（包括更高级的方法），可以查看本章末尾的拓展资源。

```{index} 变量选择; 最优子集
```

```{index} see: 预测变量选择; 变量选择
```

要系统地选择预测变量，你首先想到的办法可能是：把所有可能的预测变量子集都试一遍，然后挑出能得到“最好”分类器的那个集合。这个做法确实是一种著名的变量选择方法，叫作*最优子集选择*（best subset selection）{cite:p}`bealesubset,hockingsubset`。具体来说，你要

1. 为预测变量的每一个可能子集分别建立一个模型，
2. 用交叉验证对每个模型调优，
3. 选出交叉验证准确率最高的那个预测变量子集。

最优子集选择适用于任何分类方法（K 近邻或其它方法）。不过，只要可供选择的预测变量稍微多一点（比如 10 个左右），它就会变得非常慢。原因在于，可能的预测变量子集个数随预测变量个数增长得极快，而每个子集都得训练一次模型（训练本身就很慢！）。例如，如果只有 2 个预测变量——把它们叫作 A 和 B——那么有 3 种变量组合可试：只用 A、只用 B，以及 A 和 B 一起用。如果有 3 个预测变量——A、B 和 C——那么有 7 种可试：A、B、C、AB、BC、AC 和 ABC。一般来说，$m$ 个预测变量需要训练的模型个数是 $2^m-1$；换句话说，到了 10 个预测变量，要训练的模型就超过*一千*个，而到了 20 个预测变量，要训练的模型超过*一百万*个！所以，最优子集选择虽然方法简单，但在实践中往往计算成本太高，用不起来。

```{index} 变量选择; 前向
```

另一种思路是每次加入一个预测变量，逐步把模型搭建起来。这种方法叫作*前向选择*（forward selection）{cite:p}`forwardefroymson,forwarddraper`，同样适用范围很广，而且相当直观。它包含以下步骤：

1. 从一个不含任何预测变量的模型开始。
2. 重复以下 3 个步骤，直到没有预测变量可用：
    1. 对每个尚未使用的预测变量，把它加入模型，组成一个*候选模型*。
    2. 调优所有候选模型。
    3. 把交叉验证准确率最高的候选模型更新为当前模型。
3. 选出在准确率与简洁性之间权衡取舍最佳的模型。

假设总共有 $m$ 个预测变量可用。第一轮迭代要建立 $m$ 个候选模型，每个含 1 个预测变量。第二轮迭代要建立 $m-1$ 个候选模型，每个含 2 个预测变量（一个是上一轮选中的，另一个是新增的）。你想迭代多少轮，这个规律就延续多少轮。如果一直做到没有预测变量可选，最终要训练的模型个数是 $\frac{1}{2}m(m+1)$。相比最优子集选择所需的 $2^m-1$ 个模型，这是*很大*的改进！例如，10 个预测变量时，最优子集选择要训练 1000 多个候选模型，而前向选择只需训练 55 个候选模型。因此本节余下的部分都用前向选择。

```{note}
继续之前先提醒一句。你每多训练一个模型，就越可能运气不好，撞上一个模型：它的交叉验证准确率估计值很高，但在测试数据和其他未来观测上的真实准确率却很低。前向选择要训练大量模型，所以出现这种情况的风险相当高。要把风险压下来，只有在数据量很大、预测变量总数相对较少时才使用前向选择。更高级的方法受这个问题的影响要小得多；想进一步了解高级的预测变量选择方法，可以查看本章末尾的拓展资源。
```

+++

### 用 Python 实现前向选择

```{index} 变量选择; 实现
```

下面我们动手用 Python 实现前向选择。先在这个示例中取出较小的一组预测变量——`Smoothness`、`Concavity`、`Perimeter`、`Irrelevant1`、`Irrelevant2` 和 `Irrelevant3`——以及作为标签的 `Class` 变量。我们还会取出全部预测变量的列名。

```{code-cell} ipython3
cancer_subset = cancer_irrelevant[
    [
        "Class",
        "Smoothness",
        "Concavity",
        "Perimeter",
        "Irrelevant1",
        "Irrelevant2",
        "Irrelevant3",
    ]
]

names = list(cancer_subset.drop(
    columns=["Class"]
).columns.values)

cancer_subset
```

要实现前向选择，本可以使用 `scikit-learn` 的 [`SequentialFeatureSelector`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html)，但很难把这个做法与超参数调优结合起来，为每一组特征找到合适的近邻个数。所以我们改为手写前向选择算法。具体来说，我们需要这样的代码：尝试把每个可用的预测变量加入模型，找出其中最好的，然后继续迭代。如果你还记得数据整理那一章的末尾，我们提过有时需要比前面用过的更灵活的迭代形式，这时通常要借助 *for 循环*；参见《Python for Data Analysis》{cite:p}`mckinney2012python` 中的[控制流一节](https://wesmckinney.com/book/python-basics.html#control_for)。这里我们会用两个 for 循环：一个遍历不断增大的预测变量集合规模（就是下面 `for i in range(1, n_total + 1):` 那一行），另一个检查每一轮该加入哪个预测变量（就是下面 `for j in range(len(names))` 那一行）。对每一组待尝试的预测变量，我们取出对应的预测变量子集，把它送入预处理器，构建一个用 10 折交叉验证调优 K 近邻分类器的 `Pipeline`，最后记录估计准确率。

```{code-cell} ipython3
from sklearn.compose import make_column_selector

accuracy_dict = {"size": [], "selected_predictors": [], "accuracy": []}

# store the total number of predictors
n_total = len(names)

# start with an empty list of selected predictors
selected = []

# create the pipeline and CV grid search objects
param_grid = {
    "kneighborsclassifier__n_neighbors": range(1, 61, 5),
}
cancer_preprocessor = make_column_transformer(
    (StandardScaler(), make_column_selector(dtype_include="number"))
)
cancer_tune_pipe = make_pipeline(cancer_preprocessor, KNeighborsClassifier())
cancer_tune_grid = GridSearchCV(
    estimator=cancer_tune_pipe,
    param_grid=param_grid,
    cv=10,
    n_jobs=-1
)

# for every possible number of predictors
for i in range(1, n_total + 1):
    accs = np.zeros(len(names))
    # for every possible predictor to add
    for j in range(len(names)):
        # Add remaining predictor j to the model
        X = cancer_subset[selected + [names[j]]]
        y = cancer_subset["Class"]

        # Find the best K for this set of predictors
        cancer_tune_grid.fit(X, y)
        accuracies_grid = pd.DataFrame(cancer_tune_grid.cv_results_)

        # Store the tuned accuracy for this set of predictors
        accs[j] = accuracies_grid["mean_test_score"].max()

    # get the best new set of predictors that maximize cv accuracy
    best_set = selected + [names[accs.argmax()]]

    # store the results for this round of forward selection
    accuracy_dict["size"].append(i)
    accuracy_dict["selected_predictors"].append(", ".join(best_set))
    accuracy_dict["accuracy"].append(accs.max())

    # update the selected & available sets of predictors
    selected = best_set
    del names[accs.argmax()]

accuracies = pd.DataFrame(accuracy_dict)
accuracies
```

```{index} 变量选择; 肘部法则
```

有意思！前向选择过程首先加入了三个有意义的变量 `Perimeter`、`Concavity` 和 `Smoothness`，随后才轮到无关变量。{numref}`fig:06-fwdsel-3` 把准确率随模型中预测变量个数的变化画了出来。可以看到，随着有意义的预测变量被加入，估计准确率大幅上升；而加入无关变量时，准确率要么小幅波动，要么因为模型试图调整近邻个数以应对额外噪声而下降。要从这一串模型中挑出合适的那个，你得在准确率高与模型简洁（即预测变量更少、过拟合机会更小）之间取得平衡。找到这种平衡的办法，是在{numref}`fig:06-fwdsel-3` 中寻找*肘部*（elbow），也就是图上准确率不再急剧上升、趋于平稳或开始下降的位置。{numref}`fig:06-fwdsel-3` 里的肘部看起来出现在含 3 个预测变量的模型处；过了这一点，准确率就趋于平稳。所以在这里，准确率与预测变量个数之间的最佳权衡出现在 3 个变量上：`Perimeter, Concavity, Smoothness`。换句话说，我们成功地把无关预测变量从模型中剔除了！不过，永远要记得：交叉验证给出的是真实准确率的*估计值*；看图判断肘部落在哪里、判断加入某个变量是否带来准确率的实质性提升，都要靠你自己拿主意。

```{code-cell} ipython3
:tags: [remove-cell]

fwd_sel_accuracies_plot = (
    alt.Chart(accuracies)
    .mark_line(point=True)
    .encode(
        x=alt.X("size", title="Number of Predictors"),
        y=alt.Y(
            "accuracy",
            title="Estimated Accuracy",
            scale=alt.Scale(zero=False),
        ),
    )
)
glue("fig:06-fwdsel-3", fwd_sel_accuracies_plot)
```

:::{glue:figure} fig:06-fwdsel-3
:name: fig:06-fwdsel-3

用前向选择构建的模型序列中，估计准确率随预测变量个数的变化。
:::

+++

```{note}
选择哪些变量作为预测变量，本身就属于分类器调优的一部分，所以你*不能在这个过程里使用测试数据*！
```

## 习题

本章内容的练习题见配套的[练习册仓库](https://worksheets.python.datasciencebook.ca)，在“Classification II: evaluation and tuning（分类 II：评估与调优）”这一行。点击“查看练习册（view worksheet）”可以预览本章练习册的非交互版本。如果想交互式地做这些习题，请按练习册仓库中的说明下载全部练习册，并按{numref}`第 %s 章 <move-to-your-own-machine>`中的说明配置计算机环境。这样才能保证练习册提供的自动反馈与指导按预期工作。

+++

## 拓展资源

+++

- [`scikit-learn` 网站](https://scikit-learn.org/stable/)是查阅前两章各项函数与包的更多细节以及进阶用法时极好的参考资料。除此之外，网站还提供了许多实用的[用户指南](https://scikit-learn.org/stable/user_guide.html)，帮助你快速上手。值得注意的是，`scikit-learn` 包能做的事情远不止分类，因此网站上的示例同样不局限于分类。接下来两章你会学到另一种预测性建模场景，所以不妨先读完那两章，再来访问这个网站。
- [《An Introduction to Statistical Learning》](https://www.statlearning.com/) {cite:p}`james2013introduction`
  是学习分类过程中极好的下一站。第 4 章还讨论了本书没有涉及的一些基础分类方法，例如逻辑回归、线性判别分析和朴素贝叶斯。第 5 章对交叉验证的讲解要详细得多。第 8 章和第 9 章介绍决策树与支持向量机，这两种分类方法很流行，但更为进阶。最后，第 6 章介绍了若干种选择预测变量的方法。需要注意的是，该书虽然仍是一本很易读的入门教材，但它对数学基础的要求比本书稍高一些。


+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
