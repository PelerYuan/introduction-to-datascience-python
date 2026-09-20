(classification2)=
# 分类 II：评估与调优

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
```

## 概述
本章继续介绍用分类做预测建模。上一章讲解了模型训练与数据预处理，本章则聚焦于如何评估分类器的性能，以及如何在可能时改进分类器，把它的准确率（accuracy）提到最高。

## 本章学习目标
学完本章后，你将能够：

- 说明什么是训练集、验证集和测试集，以及它们在分类中如何使用。
- 把数据划分为训练集、验证集和测试集。
- 说明什么是随机种子，以及它在可复现的数据分析中有多重要。
- 使用 `numpy.random.seed` 函数在 Python 中设置随机种子。
- 说明并解读准确率、精确率（precision）、召回率（recall）和混淆矩阵。
- 在 Python 中用测试集、单个验证集和交叉验证来评估分类的准确率、精确率和召回率。
- 在 Python 中生成混淆矩阵。
- 通过最大化交叉验证准确率估计值，选择 k 近邻分类器中的近邻个数。
- 说明欠拟合与过拟合，并把它们与 k 近邻分类中的近邻个数联系起来。
- 说明 k 近邻分类算法的优点和缺点。

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
如果说机器学习有一条黄金法则，那大概就是：*不能拿测试数据来构建模型！* 一旦这么做，模型就会提前“看到”测试数据，于是显得比实际更准确。想想看，在判断患者的肿瘤是恶性还是良性时高估了分类器的准确率，后果会有多糟！
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

那么，究竟怎样判断预测结果与测试集中观测的实际标签有多吻合呢？一种做法是计算预测**准确率**。它是指分类器给出正确预测的样本所占的比例：用预测正确的数量除以预测的总数即可。判断预测结果是否与测试集中的实际标签相符的过程，见 {numref}`fig:06-ML-paradigm-test`。

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

在 {numref}`confusion-matrix-table` 的例子中，有 1 条恶性观测被正确判为恶性（左上角），57 条良性观测被正确判为良性（右下角）。不过也能看出分类器犯了一些错误：它把 3 条恶性观测判成了良性，把 4 条良性观测判成了恶性。由下面的公式可以算出，这个分类器的准确率约为 89%：

$$\mathrm{accuracy} = \frac{\mathrm{number \; of  \; correct  \; predictions}}{\mathrm{total \;  number \;  of  \; predictions}} = \frac{1+57}{1+57+4+3} = 0.892.$$

但我们还会发现，数据集中共有 4 个恶性肿瘤，分类器只识别出其中 1 个；换句话说，它把 75% 的恶性病例判错了！在这个例子里，把恶性肿瘤误判可能造成灾难性后果，因为需要治疗的患者可能因此得不到治疗。既然我们特别关心能否找出恶性病例，那么即便准确率达到 89%，这个分类器恐怕也难以接受。

```{index} 正类标签, 负类标签, 真阳性, 真阴性, 假阳性, 假阴性
```

在分类问题中，人们常常更关注某一类标签，而不是另一类。这时，我们通常把更想识别出来的那一类标签称为*正类*标签，另一类称为*负类*标签。在肿瘤这个例子里，恶性观测就是*正类*，良性观测则是*负类*。分类器能做出的四种预测，正好对应混淆矩阵中的四个单元格，可以用以下术语来称呼：

- **真阳性（True Positive）：** 恶性观测被判为恶性（{numref}`confusion-matrix-table` 左上角）。
- **假阳性（False Positive）：** 良性观测被判为恶性（{numref}`confusion-matrix-table` 左下角）。
- **真阴性（True Negative）：** 良性观测被判为良性（{numref}`confusion-matrix-table` 右下角）。
- **假阴性（False Negative）：** 恶性观测被判为良性（{numref}`confusion-matrix-table` 右上角）。

```{index} 精确率, 召回率
```

完美分类器不会有假阴性，也不会有假阳性（因此准确率为 100%）。然而，实际中的分类器几乎总会犯一些错误。所以，你应当想清楚在自己的应用里哪种错误最要紧，并用混淆矩阵把它们量化、报告出来。利用混淆矩阵可以算出两个常用指标：分类器的**精确率**和**召回率**，它们常与准确率一起报告。*精确率*衡量分类器判为正类的预测中有多少确实是正类。直观地说，我们希望分类器的精确率*高*：精确率高的分类器如果报告某个新观测为正类，我们就可以相信这个新观测确实是正类。用混淆矩阵中的各项，可以按下面的公式计算分类器的精确率：

$$\mathrm{precision} = \frac{\mathrm{number \; of  \; correct \; positive \; predictions}}{\mathrm{total \;  number \;  of \; positive  \; predictions}}.$$

*召回率*衡量测试集中的正类观测有多少被识别为正类。直观地说，我们希望分类器的召回率*高*：召回率高的分类器只要测试数据中存在正类观测，我们就可以相信它能找出来。同样用混淆矩阵中的各项，可以按下面的公式计算分类器的召回率：

$$\mathrm{recall} = \frac{\mathrm{number \; of  \; correct  \; positive \; predictions}}{\mathrm{total \;  number \;  of  \; positive \; test \; set \; observations}}.$$

在 {numref}`confusion-matrix-table` 给出的例子里，精确率和召回率分别是

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

我们用一个例子来看看随机性在 Python 中是怎样起作用的。假设有一个序列对象，其中包含从 0 到 9 的整数。我们想从里面随机抽出 10 个数，同时希望这个过程可复现。在抽取这 10 个数之前，先调用 `numpy` 包中的 `seed` 函数，把任意一个整数作为参数传给它。下面用到的种子数是 `1`。这样设置之后，Python 会持续记录代码中出现的随机过程。例如，我们可以对数字序列调用 `sample` 方法，传入参数 `n=10`，表示想要 10 个样本。`to_list` 方法会把结果序列转换成基本的 Python 列表，让输出更容易阅读。

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

在本书中，我们一般只使用能与 `numpy` 默认随机数生成器很好配合的包，所以沿用 `np.random.seed` 即可。如果你希望对分析中的随机性有更精细的控制，可以在分析开始时创建一个 `numpy` 的 [`Generator` 对象](https://numpy.org/doc/stable/reference/random/generator.html)，再把它传给许多 `pandas` 和 `scikit-learn` 函数都提供的 `random_state` 参数。这些函数会用你的 `Generator` 生成随机数，而不用 `numpy` 的默认生成器。例如，用一个 `seed` 值设为 1 的 `Generator` 对象就能重现前面的例子，我们再次得到相同的数字列表。
```python
from numpy.random import Generator, PCG64
rng = Generator(PCG64(seed=1))
random_numbers1_third = nums_0_to_9.sample(n=10, random_state=rng).to_list()
random_numbers1_third
```
```text
array([2, 9, 6, 4, 0, 3, 1, 7, 8, 5])
```
```python
random_numbers2_third = nums_0_to_9.sample(n=10, random_state=rng).to_list()
random_numbers2_third
```
```text
array([9, 5, 3, 0, 8, 4, 2, 1, 6, 7])
```

````

## 使用 `scikit-learn` 评估性能

```{index} scikit-learn, 可视化; 散点图
```

现在回到评估分类器上来！在 Python 中，`scikit-learn` 包既能做 k 近邻分类，也能评估分类结果的好坏。我们用一个例子来看看，如何借助 `scikit-learn` 中的工具、使用上一章的乳腺癌数据集来评估分类器。分析从加载所需的包、读入乳腺癌数据开始，然后快速画一张肿瘤细胞凹度（Concavity）与光滑度（Smoothness）的散点图，颜色表示诊断结果，见图 {numref}`fig:06-precode`。你还会注意到，我们按照 {numref}`randomseeds` 中的说明，用 `np.random.seed` 函数设置了随机种子。

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
<<TERM>>
concavity = 凹度
smoothness = 光滑度
biopsy = 活检
tumor = 肿瘤
diagnosis = 诊断
random seed = 随机种子
<<END>>
