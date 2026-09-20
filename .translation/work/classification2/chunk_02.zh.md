+++

```{index} scikit-learn; train_test_split, 打乱, 分层
```

`scikit-learn` 的 `train_test_split` 函数会替我们完成划分数据的过程。使用 `train_test_split` 时，我们可以指定两个很重要的参数，以确保由测试数据得到的准确率估计值合理。第一，设置 `shuffle=True`（这是默认值）表示划分之前会先打乱数据，这样数据中存在的任何顺序都不会影响最终进入训练集和测试集的数据。第二，把 `stratify` 参数指定为训练集中的响应变量，函数就会按类别标签对数据**分层**，以保证各个类别进入训练集和测试集的比例大致相同。例如，在我们的数据集中，约 63% 的观测来自良性类别（`Benign`），37% 来自恶性类别（`Malignant`）；因此把 `stratify` 指定为类别列，就能保证训练数据中约 63% 是良性的、37% 是恶性的，测试数据中也存在同样的比例。

下面我们用 `train_test_split` 函数来创建训练集和测试集。首先需要从 `sklearn` 包中导入这个函数。然后指定 `train_size=0.75`，让原始数据集的 75% 进入训练集。我们还会把 `stratify` 参数设为分类标签变量（这里就是 `cancer["Class"]`），以保证训练子集和测试子集中每一类观测的比例都正确。

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

从上方的 `info` 方法可以看出，训练集包含 {glue:text}`cancer_train_nrow` 条观测，而测试集包含 {glue:text}`cancer_test_nrow` 条观测。这对应 75% / 25% 的训练/测试划分，正是我们想要的。回忆 {numref}`第 %s 章 <classification1>` 可知，我们用 `info` 方法来预览数据框的行数、变量名、数据类型以及缺失项。

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

正如上一章所说，k 近邻对预测变量的标度很敏感，所以我们应该先做一些预处理，把它们标准化。此外还要注意一点：构建标准化预处理器时**只能使用训练数据**。这样就能保证测试数据不会影响模型训练的任何环节。标准化预处理器建好之后，我们再把它分别应用到训练数据集和测试数据集上。

+++

```{index} scikit-learn; Pipeline, scikit-learn; make_column_transformer, scikit-learn; StandardScaler
```

好在只要把各个分析步骤包进 `Pipeline`，`scikit-learn` 就会帮我们正确处理这件事，就像 {numref}`第 %s 章 <classification1>` 中那样。所以下面我们和之前一样，用 `make_column_transformer` 来构造并准备好预处理器。

```{code-cell} ipython3
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer

cancer_preprocessor = make_column_transformer(
    (StandardScaler(), ["Smoothness", "Concavity"]),
)
```

### 训练分类器

现在我们已经把原始数据集划分成训练集和测试集，可以借助上一章学到的技术，只用训练集来构建 k 近邻分类器。这里先把近邻个数 $K$ 取为 3，并且只从 `cancer_train` 数据框中选取凹度（concavity）和平滑度（smoothness）这两个预测变量。首先从 `sklearn` 中导入 `KNeighborsClassifier` 模型和 `make_pipeline`。然后和之前一样创建模型对象，用 `make_pipeline` 函数把模型对象和预处理器组合成 `Pipeline`，最后用 `fit` 方法构建分类器。

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

现在我们已经有了 k 近邻分类器对象，可以用它来预测测试集的类别标签，并在原始测试数据中添加一列预测结果。`Class` 变量存放的是实际诊断结果，而 `predicted` 存放的是分类器给出的预测诊断结果。请注意，下面输出的数据框中只打印了 `ID`、`Class` 和 `predicted` 这三个变量。

```{code-cell} ipython3
cancer_test["predicted"] = knn_pipeline.predict(cancer_test[["Smoothness", "Concavity"]])
cancer_test[["ID", "Class", "predicted"]]
```

(eval-performance-clasfcn2)=
### 评估性能

```{index} scikit-learn; score, scikit-learn; precision_score, scikit-learn; recall_score
```

最后，我们来评估分类器的性能。首先看准确率。为此要使用 `score` 方法，并指定两个参数：预测变量和实际标签。预测变量传入我们之前调用 `predict` 做预测时所用的同一份测试数据，实际标签则用 `cancer_test["Class"]` 序列给出。

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

混淆矩阵显示，有 {glue:text}`confu11` 条观测被正确预测为恶性，{glue:text}`confu00` 条被正确预测为良性。它也显示分类器犯了一些错误：它把 {glue:text}`confu10` 条实际为恶性的观测判成了良性，把 {glue:text}`confu01` 条实际为良性的观测判成了恶性。用前面给出的公式可以算出，准确率、精确率和召回率的数值与 Python 报告的结果一致。

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

一般来说，准确率的*好*数值（以及适用时的精确率和召回率）取决于具体应用；你必须结合自己正在解决的问题，批判性地分析准确率。举例来说，假如我们要为一种 99% 的时间都是良性的肿瘤构建分类器，那么准确率为 99% 的分类器也算不上多惊人（一直猜良性就行了！）。除了准确率，我们还要考虑精确率和召回率：前面提到过，分类器所犯错误的*种类*在许多应用中同样重要。在前面那个 99% 的观测都是良性的例子里，实际类别是“恶性”时分类器却预测“良性”（假阴性），后果可能非常严重，因为病人可能因此得不到应有的医疗照护。反过来，实际类别是“良性”时分类器却猜“恶性”（假阳性），后果可能没那么严重，因为病人接下来很可能会去看医生，由医生给出专业诊断。换句话说，为了获得高召回率，我们愿意牺牲一些精确率。这就是为什么除了准确率，还要看混淆矩阵。

```{index} 分类; 多数类
```

不过，任何分类问题都有一个方便的基准可供比较：*多数类分类器*。多数类分类器*总是*猜测训练数据中的多数类标签，完全不看预测变量的取值。在考虑准确率时，它能帮你对数值规模有个大致概念。如果多数类分类器在某个问题上得到 90% 的准确率，那你就会希望自己的 k 近邻分类器做得比这更好。如果你的分类器比多数类分类器有明显提升，这就说明至少你的方法从预测变量中提取出了一些有用的信息。不过要小心：比多数类分类器表现更好，并不*必然*意味着这个分类器对你的应用来说已经足够好。

举个例子，在乳腺癌数据中，回忆一下训练数据里良性和恶性观测的比例：

```{code-cell} ipython3
cancer_train["Class"].value_counts(normalize=True)
```

由于良性类别占训练数据的大多数，多数类分类器会*总是*预测新观测为良性。多数类分类器的估计准确率通常与训练数据中多数类的比例相当接近。在这个例子里，我们会猜测多数类分类器的准确率大约为 {glue:text}`cancer_train_b_prop`%。而我们构建的 k 近邻分类器比它好不少，准确率为 {glue:text}`cancer_acc_1`%。这意味着从准确率的角度看，k 近邻分类器比基本的多数类分类器提升了很多。太棒了！但我们仍要谨慎：在这个应用中，不让任何恶性肿瘤被误诊很可能至关重要，以免漏掉真正需要治疗的病人。上面的混淆矩阵显示，这个分类器确实把相当多的恶性肿瘤误诊成了良性（{glue:text}`confu10_11` 个恶性肿瘤中有 {glue:text}`confu10` 个，也就是 {glue:text}`confu_fal_neg`%！）。所以，尽管准确率比多数类分类器有所提升，我们的批判性分析表明，这个分类器在这个应用中的性能可能并不合适。

+++

## 调优分类器

```{index} 参数
```

```{index} see: 调优参数; 参数
```

统计学和机器学习中的绝大多数预测模型都有*参数*。*参数*是必须事先选定、并决定模型某方面行为方式的数值。例如，在 k 近邻分类算法中，$K$ 就是我们必须选定的参数，它决定有多少个近邻参与类别投票。选取不同的 $K$ 值，就会得到做出不同预测的不同分类器。

那么，我们该如何选取 $K$ 的*最佳*取值，也就是*调优*模型呢？能不能用一套有章可循的方法来完成这个选择？本书将专注于最大化分类器的准确率。理想情况下，我们希望设法让分类器在*它尚未见过*的数据上取得最高准确率。但在构建模型的过程中，我们不能使用测试数据集。所以我们会沿用之前评估分类器时的同一个技巧：把*训练数据本身*拆成两个子集，用其中一个训练模型，再用另一个评估模型。本节将介绍这一过程的细节，以及如何借助它为自己的分类器挑选一个好的参数取值。

**并且记住：** 在调优过程中不要碰测试集。调优是模型训练的一部分！