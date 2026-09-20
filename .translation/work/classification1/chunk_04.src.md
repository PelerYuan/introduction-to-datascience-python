+++

### Balancing

```{index} balance, imbalance
```

Another potential issue in a data set for a classifier is *class imbalance*,
i.e., when one label is much more common than another. Since classifiers like
the K-nearest neighbors algorithm use the labels of nearby points to predict
the label of a new point, if there are many more data points with one label
overall, the algorithm is more likely to pick that label in general (even if
the "pattern" of data suggests otherwise). Class imbalance is actually quite a
common and important problem: from rare disease diagnosis to malicious email
detection, there are many cases in which the "important" class to identify
(presence of disease, malicious email) is much rarer than the "unimportant"
class (no disease, normal email).

```{index} concat
```

To better illustrate the problem, let's revisit the scaled breast cancer data,
`cancer`; except now we will remove many of the observations of malignant tumors, simulating
what the data would look like if the cancer was rare. We will do this by
picking only 3 observations from the malignant group, and keeping all
of the benign observations. We choose these 3 observations using the `.head()`
method, which takes the number of rows to select from the top.
We will then use the [`concat`](https://pandas.pydata.org/docs/reference/api/pandas.concat.html)
function from `pandas` to glue the two resulting filtered
data frames back together. The `concat` function *concatenates* data frames
along an axis. By default, it concatenates the data frames vertically along `axis=0` yielding a single
*taller* data frame, which is what we want to do here. If we instead wanted to concatenate horizontally
to produce a *wider* data frame, we would specify `axis=1`.
The new imbalanced data is shown in {numref}`fig:05-unbalanced`,
and we print the counts of the classes using the `value_counts` function.

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

Imbalanced data.
:::

```{code-cell} ipython3
rare_cancer["Class"].value_counts()
```

+++

Suppose we now decided to use $K = 7$ in K-nearest neighbors classification.
With only 3 observations of malignant tumors, the classifier
will *always predict that the tumor is benign, no matter what its concavity and perimeter
are!* This is because in a majority vote of 7 observations, at most 3 will be
malignant (we only have 3 total malignant observations), so at least 4 must be
benign, and the benign vote will always win. For example, {numref}`fig:05-upsample`
shows what happens for a new tumor observation that is quite close to three observations
in the training data that were tagged as malignant.

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

Imbalanced data with 7 nearest neighbors to a new observation highlighted.
:::

+++

{numref}`fig:05-upsample-2` shows what happens if we set the background color of
each area of the plot to the prediction the K-nearest neighbors
classifier would make for a new observation at that location. We can see that the decision is
always "benign," corresponding to the blue color.

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

Imbalanced data with background color indicating the decision of the classifier and the points represent the labeled data.
:::

+++

```{index} oversampling, DataFrame; sample
```

Despite the simplicity of the problem, solving it in a statistically sound manner is actually
fairly nuanced, and a careful treatment would require a lot more detail and mathematics than we will cover in this textbook.
For the present purposes, it will suffice to rebalance the data by *oversampling* the rare class.
In other words, we will replicate rare observations multiple times in our data set to give them more
voting power in the K-nearest neighbors algorithm. In order to do this, we will
first separate the classes out into their own data frames by filtering.
Then, we will
use the `sample` method on the rare class data frame to increase the number of `Malignant` observations to be the same as the number
of `Benign` observations. We set the `n` argument to be the number of `Malignant` observations we want, and set `replace=True`
to indicate that we are sampling with replacement.
Finally, we use the `value_counts` method to see that our classes are now balanced.
Note that `sample` picks which data to replicate *randomly*; we will learn more about properly handling randomness
in data analysis in {numref}`Chapter %s <classification2>`.

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

Now suppose we train our K-nearest neighbors classifier with $K=7$ on this *balanced* data.
{numref}`fig:05-upsample-plot` shows what happens now when we set the background color
of each area of our scatter plot to the decision the K-nearest neighbors
classifier would make. We can see that the decision is more reasonable; when the points are close
to those labeled malignant, the classifier predicts a malignant tumor, and vice versa when they are
closer to the benign tumor observations.

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

Upsampled data with background color indicating the decision of the classifier.
:::

### Missing data

```{index} missing data
```

One of the most common issues in real data sets in the wild is *missing data*,
i.e., observations where the values of some of the variables were not recorded.
Unfortunately, as common as it is, handling missing data properly is very
challenging and generally relies on expert knowledge about the data, setting,
and how the data were collected. One typical challenge with missing data is
that missing entries can be *informative*: the very fact that an entries were
missing is related to the values of other variables.  For example, survey
participants from a marginalized group of people may be less likely to respond
to certain kinds of questions if they fear that answering honestly will come
with negative consequences. In that case, if we were to simply throw away data
with missing entries, we would bias the conclusions of the survey by
inadvertently removing many members of that group of respondents.  So ignoring
this issue in real problems can easily lead to misleading analyses, with
detrimental impacts.  In this book, we will cover only those techniques for
dealing with missing entries in situations where missing entries are just
"randomly missing", i.e., where the fact that certain entries are missing
*isn't related to anything else* about the observation.

Let's load and examine a modified subset of the tumor image data
that has a few missing entries:

```{code-cell} ipython3
missing_cancer = pd.read_csv("data/wdbc_missing.csv")[["Class", "Radius", "Texture", "Perimeter"]]
missing_cancer["Class"] = missing_cancer["Class"].replace({
   "M" : "Malignant",
   "B" : "Benign"
})
missing_cancer
```

Recall that K-nearest neighbors classification makes predictions by computing
the straight-line distance to nearby training observations, and hence requires
access to the values of *all* variables for *all* observations in the training
data.  So how can we perform K-nearest neighbors classification in the presence
of missing data?  Well, since there are not too many observations with missing
entries, one option is to simply remove those observations prior to building
the K-nearest neighbors classifier. We can accomplish this by using the
`dropna` method prior to working with the data.

```{index} missing data; dropna
```

```{code-cell} ipython3
no_missing_cancer = missing_cancer.dropna()
no_missing_cancer
```

However, this strategy will not work when many of the rows have missing
entries, as we may end up throwing away too much data. In this case, another
possible approach is to *impute* the missing entries, i.e., fill in synthetic
values based on the other observations in the data set. One reasonable choice
is to perform *mean imputation*, where missing entries are filled in using the
mean of the present entries in each variable. To perform mean imputation, we
use a `SimpleImputer` transformer with the default arguments, and use
`make_column_transformer` to indicate which columns need imputation.

```{index} scikit-learn; SimpleImputer, missing data;mean imputation
```

```{code-cell} ipython3
from sklearn.impute import SimpleImputer

preprocessor = make_column_transformer(
    (SimpleImputer(), ["Radius", "Texture", "Perimeter"]),
    verbose_feature_names_out=False
)
preprocessor
```

To visualize what mean imputation does, let's just apply the transformer directly to the `missing_cancer`
data frame using the `fit` and `transform` functions.  The imputation step fills in the missing
entries with the mean values of their corresponding variables.

```{code-cell} ipython3
preprocessor.fit(missing_cancer)
imputed_cancer = preprocessor.transform(missing_cancer)
imputed_cancer
```

Many other options for missing data imputation can be found in
[the `scikit-learn` documentation](https://scikit-learn.org/stable/modules/impute.html).  However
you decide to handle missing data in your data analysis, it is always crucial
to think critically about the setting, how the data were collected, and the
question you are answering.

+++

(08:puttingittogetherworkflow)=
