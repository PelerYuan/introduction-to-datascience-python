+++

### The clustering algorithm

```{index} K-means; algorithm
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

We begin the K-means algorithm by picking K,
and randomly assigning a roughly equal number of observations
to each of the K clusters.
An example random initialization is shown in {numref}`toy-kmeans-init-1`


:::{glue:figure} toy-kmeans-init-1
:figwidth: 700px
:name: toy-kmeans-init-1

Random initialization of labels.
Each cluster is depicted as a different color and shape.
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

```{index} WSSD; total
```

Then K-means consists of two major steps that attempt to minimize the
sum of WSSDs over all the clusters, i.e., the *total WSSD*:

1. **Center update:** Compute the center of each cluster.
2. **Label update:** Reassign each data point to the cluster with the nearest center.

These two steps are repeated until the cluster assignments no longer change.
We show what the first three iterations of K-means would look like in
{numref}`toy-kmeans-iter-1`. Each row corresponds to an iteration,
where the left column depicts the center update,
and the right column depicts the label update (i.e., the reassignment of data to clusters).

:::{glue:figure} toy-kmeans-iter-1
:figwidth: 700px
:name: toy-kmeans-iter-1

First three iterations of K-means clustering on the `penguins_standardized` example data set. Each pair of plots corresponds to an iteration. Within the pair, the first plot depicts the center update, and the second plot depicts the reassignment of data to clusters. Cluster centers are indicated by larger points that are outlined in black.
:::

+++

Note that at this point, we can terminate the algorithm since none of the assignments changed
in the third iteration; both the centers and labels will remain the same from this point onward.

```{index} K-means; termination
```

```{note}
Is K-means *guaranteed* to stop at some point, or could it iterate forever? As it turns out,
thankfully, the answer is that K-means is guaranteed to stop after *some* number of iterations. For the interested reader, the
logic for this has three steps: (1) both the label update and the center update decrease total WSSD in each iteration,
(2) the total WSSD is always greater than or equal to 0, and (3) there are only a finite number of possible
ways to assign the data to clusters. So at some point, the total WSSD must stop decreasing, which means none of the assignments
are changing, and the algorithm terminates.
```

### Random restarts

```{index} K-means; restart
```

Unlike the classification and regression models we studied in previous chapters, K-means can get "stuck" in a bad solution.
For example, {numref}`toy-kmeans-bad-init-1` illustrates an unlucky random initialization by K-means.

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

Random initialization of labels.
:::

```{code-cell} ipython3
:tags: [remove-cell]

glue('toy-kmeans-bad-iter-1', plot_kmean_iterations(4, penguins_standardized.copy(), centroid_init.copy()), display=True)
```

{numref}`toy-kmeans-bad-iter-1` shows what the iterations of K-means would look like with the unlucky random initialization shown in {numref}`toy-kmeans-bad-init-1`


:::{glue:figure} toy-kmeans-bad-iter-1
:figwidth: 700px
:name: toy-kmeans-bad-iter-1

First four iterations of K-means clustering on the `penguins_standardized` example data set with a poor random initialization. Each pair of plots corresponds to an iteration. Within the pair, the first plot depicts the center update, and the second plot depicts the reassignment of data to clusters. Cluster centers are indicated by larger points that are outlined in black.
:::

This looks like a relatively bad clustering of the data, but K-means cannot improve it.
To solve this problem when clustering data using K-means, we should randomly re-initialize the labels a few times, run K-means for each initialization,
and pick the clustering that has the lowest final total WSSD.

### Choosing K

In order to cluster data using K-means,
we also have to pick the number of clusters, K.
But unlike in classification, we have no response variable
and cannot perform cross-validation with some measure of model prediction error.
Further, if K is chosen too small, then multiple clusters get grouped together;
if K is too large, then clusters get subdivided.
In both cases, we will potentially miss interesting structure in the data.
{numref}`toy-kmeans-vary-k-1` illustrates the impact of K
on K-means clustering of our penguin flipper and bill length data
by showing the different clusterings for K's ranging from 1 to 9.

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

Clustering of the penguin data for K clusters ranging from 1 to 9. Cluster centers are indicated by larger points that are outlined in black.
:::


```{index} elbow method
```

If we set K less than 3, then the clustering merges separate groups of data; this causes a large
total WSSD, since the cluster center (denoted by large shapes with black outlines) is not close to any of the data in the cluster. On
the other hand, if we set K greater than 3, the clustering subdivides subgroups of data; this does indeed still
decrease the total WSSD, but by only a *diminishing amount*. If we plot the total WSSD versus the number of
clusters, we see that the decrease in total WSSD levels off (or forms an "elbow shape") when we reach roughly
the right number of clusters ({numref}`toy-kmeans-elbow`).

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

Total WSSD for K clusters ranging from 1 to 9.
:::

