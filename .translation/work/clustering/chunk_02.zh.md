+++

### 聚类算法

```{index} K-means; 算法
```

```{code-cell} ipython3
:tags: [remove-cell]

# Set up the initial "random" label assignment the same as in the R book
penguins_standardized['label'] = [
    2, 2, 1, 1, 0, 0, 0, 1,
    2, 2, 1, 2, 1, 2,
    0, 1, 2, 2
]
points_kmeans_init = alt.Chart(penguins_standardized).mark_point(size=75, filled=True, opacity=1).encode(
    alt.X("flipper_length_standardized").title("Flipper Length (standardized)"),
    alt.Y("bill_length_standardized").title("Bill Length (standardized)"),
    alt.Color('label:N').legend(None),
    alt.Shape('label:N').legend(None).scale(range=['square', 'circle', 'triangle']),
    alt.Size('label:O').legend(None).scale(type='ordinal', range=[50, 50, 100]),
)

glue('toy-kmeans-init-1', points_kmeans_init, display=True)
```

我们开始 K-means 算法，先选定 K，
再把数量大致相等的观测随机分配到
这 K 个簇中。
一个随机初始化的例子见 {numref}`toy-kmeans-init-1`。


:::{glue:figure} toy-kmeans-init-1
:figwidth: 700px
:name: toy-kmeans-init-1

标签的随机初始化。
每个簇用不同的颜色和形状表示。
:::

```{code-cell} ipython3
:tags: [remove-cell]

from sklearn.metrics import euclidean_distances

def plot_kmean_iterations(iterations, data, centroid_init):
    """Plot kmeans cluster and label updates for multiple iterations"""
    dfs = []
    centroid_inits = []
    for i in range(1, iterations+1):
        data['iteration'] = f'Iteration {i}'
        data['update_type'] = 'Center Update'
        data['flipper_centroid'] = data['label'].map(centroid_init['flipper_length_standardized'])
        data['bill_centroid'] = data['label'].map(centroid_init['bill_length_standardized'])
        dfs.append(data.copy())

        data['iteration'] = f'Iteration {i}'
        data['update_type'] = 'Label Update'
        cluster_columns = ['bill_length_standardized', 'flipper_length_standardized']
        data['label'] = np.argmin(euclidean_distances(data[cluster_columns], centroid_init), axis=1)
        data['flipper_centroid'] = data['label'].map(centroid_init['flipper_length_standardized'])
        data['bill_centroid'] = data['label'].map(centroid_init['bill_length_standardized'])
        dfs.append(data.copy())

        centroid_init = data.groupby('label')[cluster_columns].mean()

    points = alt.Chart(
        pd.concat(dfs),
        width=200,
        height=200
    ).mark_point(filled=True, size=50, opacity=1).encode(
        alt.X("flipper_length_standardized").scale(domain=(-2, 2)),
        alt.Y("bill_length_standardized").scale(domain=(-2, 2)),
        alt.Color('label:N').legend(None),
        alt.Shape('label:N').legend(None).scale(range=['square', 'circle', 'triangle']),
        alt.Size('label:O').legend(None).scale(type='ordinal', range=[50, 50, 100]),
    )

    centroids = points.mark_point(filled=True, stroke='black', strokeWidth=1.25).encode(
        alt.X("mean(flipper_centroid)")
            .scale(domain=(-2, 2))
            .title("Flipper Length (standardized)"),
        alt.Y("mean(bill_centroid)")
            .scale(domain=(-2, 2))
            .title("Bill Length (standardized)"),
        size=alt.value(200)
    )

    return (points + centroids).facet(
        row=alt.Row('iteration', header=alt.Header(title='', labelFontSize=18)),
        column=alt.Column('update_type', header=alt.Header(title='', labelFontSize=18))
    )
```

```{code-cell} ipython3
:tags: [remove-cell]

centroid_init = penguins_standardized.groupby('label').mean()

glue('toy-kmeans-iter-1', plot_kmean_iterations(3, penguins_standardized.copy(), centroid_init.copy()), display=True)
```

```{index} WSSD; 总计
```

接下来，K-means 包含两个主要步骤，它们都力求最小化
所有簇的簇内平方距离和（WSSD）之和，即*总 WSSD*：

1. **中心更新：** 计算每个簇的中心。
2. **标签更新：** 把每个数据点重新分配到簇中心离它最近的那个簇。

这两个步骤反复执行，直到簇归属不再发生变化。
K-means 前三轮迭代的情形见
{numref}`toy-kmeans-iter-1`。每一行对应一轮迭代：
其中左列展示中心更新，
右列展示标签更新（也就是把数据重新分配到各簇）。

:::{glue:figure} toy-kmeans-iter-1
:figwidth: 700px
:name: toy-kmeans-iter-1

在 `penguins_standardized` 示例数据集上做 K-means 聚类的前三轮迭代。每一对图对应一轮迭代。每对图中，第一幅图展示中心更新，第二幅图展示把数据重新分配到簇的结果。簇中心用带黑色描边的较大点表示。
:::

+++

请注意，此时我们就可以终止算法了，因为第三轮迭代中没有任何归属发生变化；
从此往后，簇中心和标签都将保持不变。

```{index} K-means; 终止
```

```{note}
K-means *一定*会在某个时刻停下来吗，还是会永远迭代下去？令人欣慰的是，
答案是一定的：K-means 保证在*若干*轮迭代之后停止。有兴趣的读者可以看看
背后的推理，它分三步：（1）每一轮迭代中，标签更新和中心更新都会让总 WSSD 下降；
（2）总 WSSD 总是大于或等于 0；（3）把数据分配到簇的方式只有有限多种。
因此到了某个时刻，总 WSSD 必然不再下降，这意味着没有任何归属在发生变化，
算法也就终止了。
```

### 随机重启

```{index} K-means; 重启
```

与前面几章学过的分类和回归模型不同，K-means 可能会“卡”在劣质解里。
例如，{numref}`toy-kmeans-bad-init-1` 展示了 K-means 一次运气不佳的随机初始化。

```{code-cell} ipython3
:tags: [remove-cell]

# Set up the initial "random" label assignment the same as in the R book
penguins_standardized['label'] = [1, 1, 2, 2, 0, 2, 0, 2, 2, 2, 1, 2, 0, 0, 0, 1, 1, 1]
centroid_init = penguins_standardized.groupby('label').mean()

points_kmeans_init = alt.Chart(penguins_standardized).mark_point(size=75, filled=True, opacity=1).encode(
    alt.X("flipper_length_standardized").title("Flipper Length (standardized)"),
    alt.Y("bill_length_standardized").title("Bill Length (standardized)"),
    alt.Color('label:N').legend(None),
    alt.Shape('label:N').legend(None).scale(range=['square', 'circle', 'triangle']),
    alt.Size('label:O').legend(None).scale(type='ordinal', range=[50, 50, 100]),
)

glue('toy-kmeans-bad-init-1', points_kmeans_init, display=True)
```

:::{glue:figure} toy-kmeans-bad-init-1
:figwidth: 700px
:name: toy-kmeans-bad-init-1

标签的随机初始化。
:::

```{code-cell} ipython3
:tags: [remove-cell]

glue('toy-kmeans-bad-iter-1', plot_kmean_iterations(4, penguins_standardized.copy(), centroid_init.copy()), display=True)
```

{numref}`toy-kmeans-bad-iter-1` 展示了在采用 {numref}`toy-kmeans-bad-init-1` 中那种运气不佳的随机初始化时，K-means 的迭代过程会是什么样子


:::{glue:figure} toy-kmeans-bad-iter-1
:figwidth: 700px
:name: toy-kmeans-bad-iter-1

随机初始化效果很差时，在 `penguins_standardized` 示例数据集上做 K-means 聚类的前四轮迭代。每一对图对应一轮迭代。每对图中，第一幅图展示中心更新，第二幅图展示把数据重新分配到簇的结果。簇中心用带黑色描边的较大点表示。
:::

这个聚类结果看起来相对较差，但 K-means 无法改进它。
用 K-means 聚类数据时，要解决这个问题，我们应该把标签随机重新初始化几次，对每次初始化各运行一遍 K-means，
然后选出最终总 WSSD 最低的那个聚类结果。

### 选择 K

要用 K-means 对数据聚类，
我们还必须选定簇数 K。
但与分类不同，这里没有响应变量，
也无法用某种模型预测误差指标来做交叉验证。
此外，K 选得太小，多个簇就会被合并到一起；
K 选得太大，簇又会被细分。
无论哪种情况，我们都可能漏掉数据中有趣的结构。
{numref}`toy-kmeans-vary-k-1` 展示了 K 的取值
对这份企鹅翼长与喙长数据做 K-means 聚类的影响：
图中给出了 K 从 1 到 9 时各不相同的聚类结果。

```{code-cell} ipython3
:tags: [remove-cell]

from sklearn.cluster import KMeans

penguins_standardized = penguins_standardized.drop(columns=["label"])

dfs = []
inertias = []
for i in range(1, 10):
    data = penguins_standardized.copy()
    knn = KMeans(n_clusters=i, n_init='auto')
    knn.fit(data)
    data['n_clusters'] = f'{i} Cluster' + ('' if i == 1 else 's')
    data['label'] = knn.labels_
    dfs.append(data)
    inertias.append(knn.inertia_)

points = alt.Chart(pd.concat(dfs), width=200, height=200).mark_point(filled=True, opacity=1).encode(
    alt.X('bill_length_standardized')
        .scale(zero=False)
        .title("Flipper Length (standardized)"),
    alt.Y('flipper_length_standardized')
        .scale(zero=False)
        .title("Bill Length (standardized)"),
    alt.Color('label:N').legend(None),
    alt.Shape('label:N').legend(None).scale(range=['square', 'circle', 'triangle', 'cross', 'diamond', 'triangle-right', 'triangle-down', 'triangle-left']),
    alt.Size('label:O').legend(None).scale(type='ordinal', range=[50, 50, 100, 100, 100, 100, 100, 100]),
    # alt.Shape('label:N').legend(None),
)

vary_k = alt.layer(
    points,
    points.mark_point(filled=True, stroke='black', strokeWidth=1.25).encode(
        alt.X('mean(bill_length_standardized)'),
        alt.Y('mean(flipper_length_standardized)'),
        size=alt.value(200)
    )
).facet(
    alt.Facet(
        'n_clusters:N',
        header=alt.Header(title='', labelFontSize=16)
    ),
    columns=3
)
glue('toy-kmeans-vary-k-1', vary_k, display=True)
```



:::{glue:figure} toy-kmeans-vary-k-1
:figwidth: 700px
:name: toy-kmeans-vary-k-1

K 从 1 到 9 时企鹅数据的聚类结果。簇中心用带黑色描边的较大点表示。
:::


```{index} 肘部法则
```

如果把 K 设得小于 3，聚类就会把本来分开的几组数据合并到一起；这会导致很大的
总 WSSD，因为簇中心（图中用带黑色描边的较大形状表示）离簇内任何一个数据点都不近。
反过来，如果把 K 设得大于 3，聚类就会把数据中的子组进一步细分；这样做确实仍能让
总 WSSD 下降，但下降的幅度*越来越小*。如果把总 WSSD 对簇数作图，就会看到：当我们取到
大致合适的簇数时，总 WSSD 的下降趋于平缓，或者形成一个“肘部形状”（{numref}`toy-kmeans-elbow`）。

```{code-cell} ipython3
:tags: [remove-cell]

elbow_plot = alt.layer(
    alt.Chart(
        pd.DataFrame({
            'wssd': inertias,
            'k': range(1, len(inertias) + 1)
        })
    ).mark_line(point=True).encode(
        x=alt.X("k").title("Number of clusters"),
        y=alt.Y("wssd").title("Total within-cluster sum of squares"),
    ),
    alt.Chart().mark_text(size=22, align='left', baseline='bottom').encode(
        x=alt.datum(3.3),
        y=alt.datum(9.8),
        text=alt.datum('Elbow')
    ),
    alt.Chart().mark_text(size=50, align='left', baseline='bottom', fontWeight=100, angle=25).encode(
        x=alt.datum(2.8),
        y=alt.datum(5),
        text=alt.datum('🠃')
    )
)

glue('toy-kmeans-elbow', elbow_plot, display=True)
```

:::{glue:figure} toy-kmeans-elbow
:figwidth: 700px
:name: toy-kmeans-elbow

K 从 1 到 9 时各簇数下的总 WSSD。
:::

