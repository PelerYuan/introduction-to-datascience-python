## K-means in Python

```{index} K-means, scikit-learn; KMeans
```

```{index} see: KMeans; scikit-learn
```

We can perform K-means in Python using a workflow similar to those
in the earlier classification and regression chapters.
Returning to the original (unstandardized) `penguins` data,
recall that K-means clustering uses straight-line distance to decide which points are similar to
each other. Therefore, the *scale* of each of the variables in the data
will influence which cluster data points end up being assigned.
Variables with a large scale will have a much larger
effect on deciding cluster assignment than variables with a small scale.
To address this problem, we typically standardize our data before clustering,
which ensures that each variable has a mean of 0 and standard deviation of 1.
The `StandardScaler` function in `scikit-learn` can be used to do this.

```{index} scikit-learn; StandardScaler, scikit-learn;KMeans, standardization;K-means, K-means;standardization
```

```{code-cell} ipython3
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")

preprocessor = make_column_transformer(
    (StandardScaler(), ["bill_length_mm", "flipper_length_mm"]),
    verbose_feature_names_out=False,
)
preprocessor
```

To indicate that we are performing K-means clustering, we will create a `KMeans`
model object. It takes at
least one argument: the number of clusters `n_clusters`, which we set to 3.

```{index} KMeans;n_clusters
```

```{code-cell} ipython3
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
kmeans
```

```{index} scikit-learn;make_pipeline, scikit-learn;Pipeline, scikit-learn;fit
```

To actually run the K-means clustering, we combine the preprocessor and model object
in a `Pipeline`, and use the `fit` function. Note that the K-means
algorithm uses a random initialization of assignments, but since we set
the random seed in the beginning of this chapter, the clustering will be reproducible.

```{code-cell} ipython3
from sklearn.pipeline import make_pipeline

penguin_clust = make_pipeline(preprocessor, kmeans)
penguin_clust.fit(penguins)
penguin_clust
```

```{index} KMeans; labels_, KMeans; inertia_
```

The fit `KMeans` object&mdash;which is the second item in the
pipeline, and can be accessed as `penguin_clust[1]`&mdash;has a lot of information
that can be used to visualize the clusters, pick K, and evaluate the total WSSD.
Let's start by visualizing the clusters as a colored scatter plot! In
order to do that, we first need to augment our
original `penguins` data frame with the cluster assignments.
We can access these using the `labels_` attribute of the clustering object
("labels" is a common alternative term to "assignments" in clustering), and
add them to the data frame.

```{code-cell} ipython3
penguins["cluster"] = penguin_clust[1].labels_
penguins
```

Now that we have the cluster assignments included in the `penguins` data frame, we can
visualize them as shown in {numref}`cluster_plot`.
Note that we are plotting the *un-standardized* data here; if we for some reason wanted to
visualize the *standardized* data, we would need to use the `fit` and `transform` functions
on the `StandardScaler` preprocessor directly to obtain that first.
As in {numref}`Chapter %s <viz>`,
adding the `:N` suffix ensures that `altair`
will treat the `cluster` variable as a nominal/categorical variable, and
hence use a discrete color map for the visualization.

```{index} altair; :N
```

```{code-cell} ipython3
cluster_plot=alt.Chart(penguins).mark_circle().encode(
    x=alt.X("flipper_length_mm").title("Flipper Length").scale(zero=False),
    y=alt.Y("bill_length_mm").title("Bill Length").scale(zero=False),
    color=alt.Color("cluster:N").title("Cluster"),
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cluster_plot", cluster_plot, display=True)
```

:::{glue:figure} cluster_plot
:figwidth: 700px
:name: cluster_plot

The data colored by the cluster assignments returned by K-means.
:::

```{index} WSSD; total, KMeans; inertia_
```

```{index} see: WSSD; KMeans
```

As mentioned above,
we also need to select K
by finding where the "elbow" occurs in the plot of total WSSD versus the number of clusters.
The total WSSD is stored in the `.inertia_` attribute
of the clustering object ("inertia" is the term `scikit-learn` uses to denote WSSD).

```{code-cell} ipython3
penguin_clust[1].inertia_
```

To calculate the total WSSD for a variety of Ks, we will
create a data frame that contains different values of `k`
and the WSSD of running K-means with each values of k.
To create this dataframe,
we will use what is called a "list comprehension" in Python,
where we repeat an operation multiple times
and return a list with the result.
Here is an examples of a list comprehension that stores the numbers 0-2 in a list:

```{index} list comprehension
```

```{code-cell} ipython3
[n for n in range(3)]
```

We can change the variable `n` to be called whatever we prefer
and we can also perform any operation we want as part of the list comprehension.
For example,
we could square all the numbers from 1-4 and store them in a list:

```{code-cell} ipython3
[number**2 for number in range(1, 5)]
```

Next, we will use this approach to compute the WSSD for the K-values 1 through 9.
For each value of K,
we create a new `KMeans` model
and wrap it in a `scikit-learn` pipeline
with the preprocessor we created earlier.
We store the WSSD values in a list that we will use to create a dataframe
of both the K-values and their corresponding WSSDs.

```{note}
We are creating the variable `ks` to store the range of possible k-values,
so that we only need to change this range in one place
if we decide to change which values of k we want to explore.
Otherwise it would be easy to forget to update it
in either the list comprehension or in the data frame assignment.
If you are using a value multiple times,
it is always the safest to assign it to a variable name for reuse.
```

```{code-cell} ipython3
ks = range(1, 10)
wssds = [
    make_pipeline(
    	preprocessor,
    	KMeans(n_clusters=k)  # Create a new KMeans model with `k` clusters
    ).fit(penguins)[1].inertia_
    for k in ks
]

penguin_clust_ks = pd.DataFrame({
    "k": ks,
    "wssd": wssds,
})

penguin_clust_ks
```

Now that we have `wssd` and `k` as columns in a data frame, we can make a line plot
({numref}`elbow_plot`) and search for the "elbow" to find which value of K to use.

```{code-cell} ipython3
elbow_plot = alt.Chart(penguin_clust_ks).mark_line(point=True).encode(
    x=alt.X("k").title("Number of clusters"),
    y=alt.Y("wssd").title("Total within-cluster sum of squares"),
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("elbow_plot", elbow_plot, display=True)
```

:::{glue:figure} elbow_plot
:figwidth: 700px
:name: elbow_plot

A plot showing the total WSSD versus the number of clusters.
:::

It looks like three clusters is the right choice for this data,
since that is where the "elbow" of the line is the most distinct.
In the plot,
you can also see that the WSSD is always decreasing,
as we would expect when we add more clusters.
However,
it is possible to have an elbow plot
where the WSSD increases at one of the steps,
causing a small bump in the line.
This is because K-means can get "stuck" in a bad solution
due to an unlucky initialization of the initial center positions
as we mentioned earlier in the chapter.

```{index} KMeans; n_init
```

```{note}
It is rare that the implementation of K-means from `scikit-learn`
gets stuck in a bad solution, because `scikit-learn` tries to choose
the initial centers carefully to prevent this from happening.
If you still find yourself in a situation where you have a bump in the elbow plot,
you can increase the `n_init` parameter
when creating the `KMeans` object, e.g., `KMeans(n_clusters=k, n_init=10)`, to try more different random center initializations.
The larger the value the better from an analysis perspective,
but there is a trade-off that doing many clusterings could take a long time.
```

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Clustering" row. You can preview a
non-interactive version of the worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.

## Additional resources

- Chapter 10 of *An Introduction to Statistical
  Learning* {cite:p}`james2013introduction` provides a
  great next stop in the process of learning about clustering and unsupervised
  learning in general. In the realm of clustering specifically, it provides a
  great companion introduction to K-means, but also covers *hierarchical*
  clustering for when you expect there to be subgroups, and then subgroups within
  subgroups, etc., in your data. In the realm of more general unsupervised
  learning, it covers *principal components analysis (PCA)*, which is a very
  popular technique for reducing the number of predictors in a data set.

+++

## References

```{bibliography}
:filter: docname in docnames
```
