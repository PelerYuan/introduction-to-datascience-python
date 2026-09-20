## K-nearest neighbors with `scikit-learn`

```{index} scikit-learn
```

Coding the K-nearest neighbors algorithm in Python ourselves can get complicated,
especially if we want to handle multiple classes, more than two variables,
or predict the class for multiple new observations. Thankfully, in Python,
the K-nearest neighbors algorithm is
implemented in [the `scikit-learn` Python package](https://scikit-learn.org/stable/index.html) {cite:p}`sklearn_api` along with
many [other models](https://scikit-learn.org/stable/user_guide.html) that you will encounter in this and future chapters of the book. Using the functions
in the `scikit-learn` package (named `sklearn` in Python) will help keep our code simple, readable and accurate; the
less we have to code ourselves, the fewer mistakes we will likely make.
Before getting started with K-nearest neighbors, we need to tell the `sklearn` package
that we prefer using `pandas` data frames over regular arrays via the `set_config` function.
```{note}
You will notice a new way of importing functions in the code below: `from ... import ...`. This lets us
import *just* `set_config` from `sklearn`, and then call `set_config` without any package prefix.
We will import functions using `from` extensively throughout
this and subsequent chapters to avoid very long names from `scikit-learn`
that clutter the code
(like `sklearn.neighbors.KNeighborsClassifier`, which has 38 characters!).
```

```{code-cell} ipython3
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")
```

We can now get started with K-nearest neighbors. The first step is to
 import the `KNeighborsClassifier` from the `sklearn.neighbors` module.

```{code-cell} ipython3
from sklearn.neighbors import KNeighborsClassifier
```

Let's walk through how to use `KNeighborsClassifier` to perform K-nearest neighbors classification.
We will use the `cancer` data set from above, with
perimeter and concavity as predictors and $K = 5$ neighbors to build our classifier. Then
we will use the classifier to predict the diagnosis label for a new observation with
perimeter 0, concavity 3.5, and an unknown diagnosis label. Let's pick out our two desired
predictor variables and class label and store them with the name `cancer_train`:

```{code-cell} ipython3
cancer_train = cancer[["Class", "Perimeter", "Concavity"]]
cancer_train
```

```{index} scikit-learn; model object, scikit-learn; KNeighborsClassifier
```

Next, we create a *model object* for K-nearest neighbors classification
by creating a `KNeighborsClassifier` instance, specifying that we want to use $K = 5$ neighbors;
we will discuss how to choose $K$ in the next chapter.

```{note}
You can specify the `weights` argument in order to control
how neighbors vote when classifying a new observation. The default is `"uniform"`, where
each of the $K$ nearest neighbors gets exactly 1 vote as described above. Other choices,
which weigh each neighbor's vote differently, can be found on
[the `scikit-learn` website](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html?highlight=kneighborsclassifier#sklearn.neighbors.KNeighborsClassifier).
```

```{code-cell} ipython3
knn = KNeighborsClassifier(n_neighbors=5)
knn
```

```{index} scikit-learn; fit, scikit-learn; predictors, scikit-learn; response
```

In order to fit the model on the breast cancer data, we need to call `fit` on
the model object. The `X` argument is used to specify the data for the predictor
variables, while the `y` argument is used to specify the data for the response variable.
So below, we set `X=cancer_train[["Perimeter", "Concavity"]]` and
`y=cancer_train["Class"]` to specify that `Class` is the response
variable (the one we want to predict), and both `Perimeter` and `Concavity` are
to be used as the predictors. Note that the `fit` function might look like it does not
do much from the outside, but it is actually doing all the heavy lifting to train
the K-nearest neighbors model, and modifies the `knn` model object.

```{code-cell} ipython3
knn.fit(X=cancer_train[["Perimeter", "Concavity"]], y=cancer_train["Class"]);
```

```{index} scikit-learn; predict
```

After using the `fit` function, we can make a prediction on a new observation
by calling `predict` on the classifier object, passing the new observation
itself. As above, when we ran the K-nearest neighbors classification
algorithm manually, the `knn` model object classifies the new observation as
"Malignant". Note that the `predict` function outputs an `array` with the
model's prediction; you can actually make multiple predictions at the same
time using the `predict` function, which is why the output is stored as an `array`.

```{code-cell} ipython3
new_obs = pd.DataFrame({"Perimeter": [0], "Concavity": [3.5]})
knn.predict(new_obs)
```

Is this predicted malignant label the actual class for this observation?
Well, we don't know because we do not have this
observation's diagnosis&mdash; that is what we were trying to predict! The
classifier's prediction is not necessarily correct, but in the next chapter, we will
learn ways to quantify how accurate we think our predictions are.

+++

## Data preprocessing with `scikit-learn`

### Centering and scaling

```{index} scaling
```

When using K-nearest neighbors classification, the *scale* of each variable
(i.e., its size and range of values) matters. Since the classifier predicts
classes by identifying observations nearest to it, any variables with
a large scale will have a much larger effect than variables with a small
scale. But just because a variable has a large scale *doesn't mean* that it is
more important for making accurate predictions. For example, suppose you have a
data set with two features, salary (in dollars) and years of education, and
you want to predict the corresponding type of job. When we compute the
neighbor distances, a difference of \$1000 is huge compared to a difference of
10 years of education. But for our conceptual understanding and answering of
the problem, it's the opposite; 10 years of education is huge compared to a
difference of \$1000 in yearly salary!

+++

```{index} centering
```

In many other predictive models, the *center* of each variable (e.g., its mean)
matters as well. For example, if we had a data set with a temperature variable
measured in degrees Kelvin, and the same data set with temperature measured in
degrees Celsius, the two variables would differ by a constant shift of 273
(even though they contain exactly the same information). Likewise, in our
hypothetical job classification example, we would likely see that the center of
the salary variable is in the tens of thousands, while the center of the years
of education variable is in the single digits. Although this doesn't affect the
K-nearest neighbors classification algorithm, this large shift can change the
outcome of using many other predictive models.

```{index} standardization; K-nearest neighbors
```

To scale and center our data, we need to find
our variables' *mean* (the average, which quantifies the "central" value of a
set of numbers) and *standard deviation* (a number quantifying how spread out values are).
For each observed value of the variable, we subtract the mean (i.e., center the variable)
and divide by the standard deviation (i.e., scale the variable). When we do this, the data
is said to be *standardized*, and all variables in a data set will have a mean of 0
and a standard deviation of 1. To illustrate the effect that standardization can have on the K-nearest
neighbors algorithm, we will read in the original, unstandardized Wisconsin breast
cancer data set; we have been using a standardized version of the data set up
until now. We will apply the same initial wrangling steps as we did earlier,
and to keep things simple we will just use the `Area`, `Smoothness`, and `Class`
variables:

```{code-cell} ipython3
unscaled_cancer = pd.read_csv("data/wdbc_unscaled.csv")[["Class", "Area", "Smoothness"]]
unscaled_cancer["Class"] = unscaled_cancer["Class"].replace({
   "M" : "Malignant",
   "B" : "Benign"
})
unscaled_cancer
```

Looking at the unscaled and uncentered data above, you can see that the differences
between the values for area measurements are much larger than those for
smoothness. Will this affect predictions? In order to find out, we will create a scatter plot of these two
predictors (colored by diagnosis) for both the unstandardized data we just
loaded, and the standardized version of that same data. But first, we need to
standardize the `unscaled_cancer` data set with `scikit-learn`.

```{index} see: Pipeline; scikit-learn
```

```{index} see: make_column_transformer; scikit-learn
```

```{index} scikit-learn;Pipeline, scikit-learn; make_column_transformer
```

The `scikit-learn` framework provides a collection of *preprocessors* used to manipulate
data in the [`preprocessing` module](https://scikit-learn.org/stable/modules/preprocessing.html).
Here we will use the `StandardScaler` transformer to standardize the predictor variables in
the `unscaled_cancer` data. In order to tell the `StandardScaler` which variables to standardize,
we wrap it in a
[`ColumnTransformer`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html#sklearn.compose.ColumnTransformer) object
using the [`make_column_transformer`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.make_column_transformer.html#sklearn.compose.make_column_transformer) function.
`ColumnTransformer` objects also enable the use of multiple preprocessors at
once, which is especially handy when you want to apply different preprocessing to each of the predictor variables.
The primary argument of the `make_column_transformer` function is a sequence of
pairs of (1) a preprocessor, and (2) the columns to which you want to apply that preprocessor.
In the present case, we just have the one `StandardScaler` preprocessor to apply to the `Area` and `Smoothness` columns.

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

You can see that the preprocessor includes a single standardization step
that is applied to the `Area` and `Smoothness` columns.
Note that here we specified which columns to apply the preprocessing step to
by individual names; this approach can become quite difficult, e.g., when we have many
predictor variables. Rather than writing out the column names individually,
we can instead use the
[`make_column_selector`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.make_column_selector.html#sklearn.compose.make_column_selector) function. For
example, if we wanted to standardize all *numerical* predictors,
we would use `make_column_selector` and specify the `dtype_include` argument to be `"number"`.
This creates a preprocessor equivalent to the one we created previously.

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

We are now ready to standardize the numerical predictor columns in the `unscaled_cancer` data frame.
This happens in two steps. We first use the `fit` function to compute the values necessary to apply
the standardization (the mean and standard deviation of each variable), passing the `unscaled_cancer` data as an argument.
Then we use the `transform` function to actually apply the standardization.
It may seem a bit unnecessary to use two steps---`fit` *and* `transform`---to standardize the data.
However, we do this in two steps so that we can specify a different data set in the `transform` step if we want.
This enables us to compute the quantities needed to standardize using one data set, and then
apply that standardization to another data set.

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
It looks like our `Smoothness` and `Area` variables have been standardized. Woohoo!
But there are two important things to notice about the new `scaled_cancer` data frame. First, it only keeps
the columns from the input to `transform` (here, `unscaled_cancer`) that had a preprocessing step applied
to them. The default behavior of the `ColumnTransformer` that we build using `make_column_transformer`
is to *drop* the remaining columns. This default behavior works well with the rest of `sklearn` (as we will see below
in {numref}`08:puttingittogetherworkflow`), but for visualizing the result of preprocessing it can be useful to keep the other columns
in our original data frame, such as the `Class` variable here.
To keep other columns, we need to set the `remainder` argument to `"passthrough"` in the `make_column_transformer` function.
Furthermore, you can see that the new column names---{glue:text}`scaled-cancer-column-0`
and {glue:text}`scaled-cancer-column-1`---include the name
of the preprocessing step separated by underscores. This default behavior is useful in `sklearn` because we sometimes want to apply
multiple different preprocessing steps to the same columns; but again, for visualization it can be useful to preserve
the original column names. To keep original column names, we need to set the `verbose_feature_names_out` argument to `False`.

```{note}
Only specify the `remainder` and `verbose_feature_names_out` arguments when you want to examine the result
of your preprocessing step. In most cases, you should leave these arguments at their default values.
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

You may wonder why we are doing so much work just to center and
scale our variables. Can't we just manually scale and center the `Area` and
`Smoothness` variables ourselves before building our K-nearest neighbors model? Well,
technically *yes*; but doing so is error-prone.  In particular, we might
accidentally forget to apply the same centering / scaling when making
predictions, or accidentally apply a *different* centering / scaling than what
we used while training. Proper use of a `ColumnTransformer` helps keep our code simple,
readable, and error-free. Furthermore, note that using `fit` and `transform` on
the preprocessor is required only when you want to inspect the result of the
preprocessing steps
yourself. You will see further on in
{numref}`08:puttingittogetherworkflow` that `scikit-learn` provides tools to
automatically streamline the preprocesser and the model so that you can call `fit`
and `transform` on the `Pipeline` as necessary without additional coding effort.

{numref}`fig:05-scaling-plt` shows the two scatter plots side-by-side&mdash;one for `unscaled_cancer` and one for
`scaled_cancer`. Each has the same new observation annotated with its $K=3$ nearest neighbors.
In the original unstandardized data plot, you can see some odd choices
for the three nearest neighbors. In particular, the "neighbors" are visually
well within the cloud of benign observations, and the neighbors are all nearly
vertically aligned with the new observation (which is why it looks like there
is only one black line on this plot). {numref}`fig:05-scaling-plt-zoomed`
shows a close-up of that region on the unstandardized plot. Here the computation of nearest
neighbors is dominated by the much larger-scale area variable. The plot for standardized data
on the right in {numref}`fig:05-scaling-plt` shows a much more intuitively reasonable
selection of nearest neighbors. Thus, standardizing the data can change things
in an important way when we are using predictive algorithms.
Standardizing your data should be a part of the preprocessing you do
before predictive modeling and you should always think carefully about your problem domain and
whether you need to standardize your data.

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

Comparison of K = 3 nearest neighbors with unstandardized and standardized data.
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

Close-up of three nearest neighbors for unstandardized data.
:::

