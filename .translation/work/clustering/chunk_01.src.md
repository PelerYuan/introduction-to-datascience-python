
(clustering)=
# Clustering

```{code-cell} ipython3
:tags: [remove-cell]

# get rid of futurewarnings from sklearn kmeans
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from chapter_preamble import *
```

## Overview

As part of exploratory data analysis, it is often helpful to see if there are
meaningful subgroups (or *clusters*) in the data.
This grouping can be used for many purposes,
such as generating new questions or improving predictive analyses.
This chapter provides an introduction to clustering
using the K-means algorithm,
including techniques to choose the number of clusters.

## Chapter learning objectives

By the end of the chapter, readers will be able to do the following:

- Describe a situation in which clustering is an appropriate technique to use,
and what insight it might extract from the data.
- Explain the K-means clustering algorithm.
- Interpret the output of a K-means analysis.
- Differentiate between clustering, classification, and regression.
- Identify when it is necessary to scale variables before clustering, and do this using Python.
- Perform K-means clustering in Python using `scikit-learn`.
- Use the elbow method to choose the number of clusters for K-means.
- Visualize the output of K-means clustering in Python using a colored scatter plot.
- Describe advantages, limitations and assumptions of the K-means clustering algorithm.


## Clustering

```{index} clustering
```

Clustering is a data analysis task
involving separating a data set into subgroups of related data.
For example, we might use clustering to separate a
data set of documents into groups that correspond to topics, a data set of
human genetic information into groups that correspond to ancestral
subpopulations, or a data set of online customers into groups that correspond
to purchasing behaviors.  Once the data are separated, we can, for example,
use the subgroups to generate new questions about the data and follow up with a
predictive modeling exercise. In this course, clustering will be used only for
exploratory analysis, i.e., uncovering patterns in the data.

```{index} classification, regression, supervised, unsupervised
```

Note that clustering is a fundamentally different kind of task than
classification or regression.  In particular, both classification and
regression are *supervised tasks* where there is a *response variable* (a
category label or value), and we have examples of past data with labels/values
that help us predict those of future data.  By contrast, clustering is an
*unsupervised task*, as we are trying to understand and examine the structure
of data without any response variable labels or values to help us.  This
approach has both advantages and disadvantages.  Clustering requires no
additional annotation or input on the data.  For example, while it would be
nearly impossible to annotate all the articles on Wikipedia with human-made
topic labels, we can cluster the articles without this information to find
groupings corresponding to topics automatically.  However, given that there is
no response variable, it is not as easy to evaluate the "quality" of a
clustering.  With classification, we can use a test data set to assess
prediction performance. In clustering, there is not a single good choice for
evaluation. In this book, we will use visualization to ascertain the quality of
a clustering, and leave rigorous evaluation for more advanced courses.

Given that there is no response variable, it is not as easy to evaluate
the "quality" of a clustering.  With classification, we can use a test data set
to assess prediction performance. In clustering, there is not a single good
choice for evaluation. In this book, we will use visualization to ascertain the
quality of a clustering, and leave rigorous evaluation for more advanced
courses.

```{index} K-means
```

As in the case of classification,
there are many possible methods that we could use to cluster our observations
to look for subgroups.
In this book, we will focus on the widely used K-means algorithm {cite:p}`kmeans`.
In your future studies, you might encounter hierarchical clustering,
principal component analysis, multidimensional scaling, and more;
see the additional resources section at the end of this chapter
for where to begin learning more about these other methods.

```{index} semisupervised
```

```{note}
There are also so-called *semisupervised* tasks,
where only some of the data come with response variable labels/values,
but the vast majority don't.
The goal is to try to uncover underlying structure in the data
that allows one to guess the missing labels.
This sort of task is beneficial, for example,
when one has an unlabeled data set that is too large to manually label,
but one is willing to provide a few informative example labels as a "seed"
to guess the labels for all the data.
```

## An illustrative example

```{index} Palmer penguins
```

In this chapter we will focus on a data set from
[the `palmerpenguins` R package](https://allisonhorst.github.io/palmerpenguins/) {cite:p}`palmerpenguins`. This
data set was collected by Dr. Kristen Gorman and
the Palmer Station, Antarctica Long Term Ecological Research Site, and includes
measurements for adult penguins ({numref}`09-penguins`) found near there {cite:p}`penguinpaper`.
Our goal will be to use two
variables&mdash;penguin bill and flipper length, both in millimeters&mdash;to determine whether
there are distinct types of penguins in our data.
Understanding this might help us with species discovery and classification in a data-driven
way. Note that we have reduced the size of the data set to 18 observations and 2 variables;
this will help us make clear visualizations that illustrate how clustering works for learning purposes.

```{figure} img/clustering/gentoo.jpg
---
height: 400px
name: 09-penguins
---
A Gentoo penguin.
```

Before we get started, we will set a random seed.
This will ensure that our analysis will be reproducible.
As we will learn in more detail later in the chapter,
setting the seed here is important
because the K-means clustering algorithm uses randomness
when choosing a starting position for each cluster.

```{index} seed; numpy.random.seed
```

```{code-cell} ipython3
import numpy as np

np.random.seed(6)
```

```{index} read function; read_csv
```

Now we can load and preview the `penguins` data.

```{code-cell} ipython3
import pandas as pd

penguins = pd.read_csv("data/penguins.csv")
penguins
```

We will begin by using a version of the data that we have standardized, `penguins_standardized`,
to illustrate how K-means clustering works (recall standardization from {numref}`Chapter %s <classification1>`).
Later in this chapter, we will return to the original `penguins` data to see how to include standardization automatically
in the clustering pipeline.

```{code-cell} ipython3
:tags: [remove-cell]
penguins_standardized = penguins.assign(
	bill_length_standardized=(penguins["bill_length_mm"] - penguins["bill_length_mm"].mean())/penguins["bill_length_mm"].std(),
    flipper_length_standardized=(penguins["flipper_length_mm"] - penguins["flipper_length_mm"].mean())/penguins["flipper_length_mm"].std()
).drop(
    columns=["bill_length_mm", "flipper_length_mm"]
)
```

```{code-cell} ipython3
penguins_standardized
```

Next, we can create a scatter plot using this data set
to see if we can detect subtypes or groups in our data set.

```{code-cell} ipython3
import altair as alt

scatter_plot = alt.Chart(penguins_standardized).mark_circle().encode(
    x=alt.X("flipper_length_standardized").title("Flipper Length (standardized)"),
    y=alt.Y("bill_length_standardized").title("Bill Length (standardized)")
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("scatter_plot", scatter_plot, display=True)
```

:::{glue:figure} scatter_plot
:figwidth: 700px
:name: scatter_plot

Scatter plot of standardized bill length versus standardized flipper length.
:::

```{index} altair, altair; mark_circle
```

Based on the visualization in {numref}`scatter_plot`,
we might suspect there are a few subtypes of penguins within our data set.
We can see roughly 3 groups of observations in {numref}`scatter_plot`,
including:

1. a small flipper and bill length group,
2. a small flipper length, but large bill length group, and
3. a large  flipper and bill length group.

```{index} K-means, elbow method
```

Data visualization is a great tool to give us a rough sense of such patterns
when we have a small number of variables.
But if we are to group data&mdash;and select the number of groups&mdash;as part of
a reproducible analysis, we need something a bit more automated.
Additionally, finding groups via visualization becomes more difficult
as we increase the number of variables we consider when clustering.
The way to rigorously separate the data into groups
is to use a clustering algorithm.
In this chapter, we will focus on the *K-means* algorithm,
a widely used and often very effective clustering method,
combined with the *elbow method*
for selecting the number of clusters.
This procedure will separate the data into groups;
{numref}`colored_scatter_plot` shows these groups
denoted by colored scatter points.

```{code-cell} ipython3
:tags: [remove-cell]
from sklearn import set_config
from sklearn.cluster import KMeans

# Output dataframes instead of arrays
set_config(transform_output="pandas")

kmeans = KMeans(n_clusters=3)

penguin_clust = kmeans.fit(penguins_standardized)

penguins_clustered = penguins_standardized.assign(cluster=penguin_clust.labels_)

colored_scatter_plot = alt.Chart(penguins_clustered).mark_circle().encode(
    x=alt.X("flipper_length_standardized", title="Flipper Length (standardized)"),
    y=alt.Y("bill_length_standardized", title="Bill Length (standardized)"),
    color=alt.Color("cluster:N")
)

glue("colored_scatter_plot", colored_scatter_plot, display=True)
```

:::{glue:figure} colored_scatter_plot
:figwidth: 700px
:name: colored_scatter_plot

Scatter plot of standardized bill length versus standardized flipper length with colored groups.
:::


What are the labels for these groups? Unfortunately, we don't have any. K-means,
like almost all clustering algorithms, just outputs meaningless "cluster labels"
that are typically whole numbers: 0, 1, 2, 3, etc. But in a simple case like this,
where we can easily visualize the clusters on a scatter plot, we can give
human-made labels to the groups using their positions on
the plot:

- small flipper length and small bill length (<font color="#f59518">orange cluster</font>),
- small flipper length and large bill length (<font color="#4c78a8">blue cluster</font>).
- and large flipper length and large bill  length (<font color="#e45756">red cluster</font>).

Once we have made these determinations, we can use them to inform our species
classifications or ask further questions about our data. For example, we might
be interested in understanding the relationship between flipper length and bill
length, and that relationship may differ depending on the type of penguin we
have.

## K-means

### Measuring cluster quality

```{code-cell} ipython3
:tags: [remove-cell]

clus = penguins_clustered[penguins_clustered["cluster"] == 0][["bill_length_standardized", "flipper_length_standardized"]]
```

```{index} see: within-cluster sum of squared distances; WSSD
```

```{index} WSSD
```

The K-means algorithm is a procedure that groups data into K clusters.
It starts with an initial clustering of the data, and then iteratively
improves it by making adjustments to the assignment of data
to clusters until it cannot improve any further. But how do we measure
the "quality" of a clustering, and what does it mean to improve it?
In K-means clustering, we measure the quality of a cluster by its
*within-cluster sum-of-squared-distances* (WSSD), also called *inertia*. Computing this involves two steps.
First, we find the cluster centers by computing the mean of each variable
over data points in the cluster. For example, suppose we have a
cluster containing four observations, and we are using two variables, $x$ and $y$, to cluster the data.
Then we would compute the coordinates, $\mu_x$ and $\mu_y$, of the cluster center via


$$
\mu_x = \frac{1}{4}(x_1+x_2+x_3+x_4) \quad \mu_y = \frac{1}{4}(y_1+y_2+y_3+y_4)
$$

```{code-cell} ipython3
:tags: [remove-cell]

clus_rows = clus.shape[0]

mean_flipper_len_std = round(np.mean(clus["flipper_length_standardized"]),2)
mean_bill_len_std = round(np.mean(clus["bill_length_standardized"]),2)

glue("clus_rows_glue", "{:d}".format(clus_rows))
glue("mean_flipper_len_std_glue","{:.2f}".format(mean_flipper_len_std))
glue("mean_bill_len_std_glue", "{:.2f}".format(mean_bill_len_std))
```

```{code-cell} ipython3
:tags: [remove-cell]

toy_example_clus1_center = alt.layer(
    alt.Chart(clus).mark_circle(size=75, opacity=1, color='steelblue').encode(
        x=alt.X("flipper_length_standardized"),
        y=alt.Y("bill_length_standardized")
    ),
    alt.Chart(clus).mark_circle(color='steelblue', size=300, opacity=1, stroke='black').encode(
        x=alt.X("mean(flipper_length_standardized)")
            .scale(zero=False, padding=20)
            .title("Flipper Length (standardized)"),
        y=alt.Y("mean(bill_length_standardized)")
            .scale(zero=False, padding=30)
            .title("Bill Length (standardized)"),
    )
)

glue('toy-example-clus1-center', toy_example_clus1_center, display=True)
```

In the first cluster from the example, there are {glue:text}`clus_rows_glue` data points. These are shown with their cluster center
(standardized flipper length {glue:text}`mean_flipper_len_std_glue`, standardized bill length {glue:text}`mean_bill_len_std_glue`) highlighted
in {numref}`toy-example-clus1-center`

:::{glue:figure} toy-example-clus1-center
:figwidth: 700px
:name: toy-example-clus1-center

Cluster 0 from the `penguins_standardized` data set example. Observations are small blue points, with the cluster center highlighted as a large blue point with a black outline.
:::

```{code-cell} ipython3
:tags: [remove-cell]

centroid_lines = alt.Chart(
    clus.assign(
        mean_bill_length=clus['bill_length_standardized'].mean(),
        mean_flipper_length=clus['flipper_length_standardized'].mean()
    )
).mark_rule(size=1.5).encode(
    alt.Y('bill_length_standardized'),
    alt.Y2('mean_bill_length'),
    alt.X('flipper_length_standardized'),
    alt.X2('mean_flipper_length')
)
toy_example_clus1_dists = centroid_lines + toy_example_clus1_center

glue('toy-example-clus1-dists', toy_example_clus1_dists, display=True)
```

```{index} distance; K-means
```

The second step in computing the WSSD is to add up the squared distance
between each point in the cluster
and the cluster center.
We use the straight-line / Euclidean distance formula
that we learned about in {numref}`Chapter %s <classification1>`.
In the {glue:text}`clus_rows_glue`-observation cluster example above,
we would compute the WSSD $S^2$ via

$$
S^2 = \left((x_1 - \mu_x)^2 + (y_1 - \mu_y)^2\right) + \left((x_2 - \mu_x)^2 + (y_2 - \mu_y)^2\right)\\
 + \left((x_3 - \mu_x)^2 + (y_3 - \mu_y)^2\right)  +  \left((x_4 - \mu_x)^2 + (y_4 - \mu_y)^2\right)
$$

These distances are denoted by lines in {numref}`toy-example-clus1-dists` for the first cluster of the penguin data example.

:::{glue:figure} toy-example-clus1-dists
:figwidth: 700px
:name: toy-example-clus1-dists

Cluster 0 from the `penguins_standardized` data set example. Observations are small blue points, with the cluster center highlighted as a large blue point with a black outline. The distances from the observations to the cluster center are represented as black lines.
:::

```{code-cell} ipython3
:tags: [remove-cell]

toy_example_all_clus_dists = alt.layer(
    alt.Chart(
        penguins_clustered.assign(
            mean_bill_length=penguins_clustered.groupby('cluster')['bill_length_standardized'].transform('mean'),
            mean_flipper_length=penguins_clustered.groupby('cluster')['flipper_length_standardized'].transform('mean')
        )
    ).mark_rule(size=1.25).encode(
        alt.Y('bill_length_standardized'),
        alt.Y2('mean_bill_length'),
        alt.X('flipper_length_standardized'),
        alt.X2('mean_flipper_length')
    ),
    alt.Chart(penguins_clustered).mark_circle(size=40, opacity=1).encode(
        alt.X("flipper_length_standardized"),
        alt.Y("bill_length_standardized"),
        alt.Color('cluster:N')
    ),
    alt.Chart(penguins_clustered).mark_circle(size=200, opacity=1, stroke = "black").encode(
        alt.X("mean(flipper_length_standardized)")
          .scale(zero=False)
          .title("Flipper Length (standardized)"),
        alt.Y("mean(bill_length_standardized)")
          .scale(zero=False)
          .title("Bill Length (standardized)"),
        alt.Detail('cluster:N'),
        alt.Color('cluster:N')
    )
)
glue('toy-example-all-clus-dists', toy_example_all_clus_dists, display=True)
```

The larger the value of $S^2$, the more spread out the cluster is, since large $S^2$ means
that points are far from the cluster center. Note, however, that "large" is relative to *both* the
scale of the variables for clustering *and* the number of points in the cluster. A cluster where points
are very close to the center might still have a large $S^2$ if there are many data points in the cluster.

After we have calculated the WSSD for all the clusters,
we sum them together to get the *total WSSD*. For our example,
this means adding up all the squared distances for the 18 observations.
These distances are denoted by black lines in
{numref}`toy-example-all-clus-dists`.

:::{glue:figure} toy-example-all-clus-dists
:figwidth: 700px
:name: toy-example-all-clus-dists

All clusters from the `penguins_standardized` data set example. Observations are small orange, blue, and yellow points with cluster centers denoted by larger points with a black outline. The distances from the observations to each of the respective cluster centers are represented as black lines.
:::

Since K-means uses the straight-line distance to measure the quality of a clustering,
it is limited to clustering based on quantitative variables.
However, note that there are variants of the K-means algorithm,
as well as other clustering algorithms entirely,
that use other distance metrics
to allow for non-quantitative data to be clustered.
These are beyond the scope of this book.

