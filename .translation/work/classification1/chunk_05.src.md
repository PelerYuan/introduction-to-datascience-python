## Putting it together in a `Pipeline`

```{index} scikit-learn; Pipeline
```

The `scikit-learn` package collection also provides the [`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html?highlight=pipeline#sklearn.pipeline.Pipeline),
a  way to chain together multiple data analysis steps without a lot of otherwise necessary code for intermediate steps.
To illustrate the whole workflow, let's start from scratch with the `wdbc_unscaled.csv` data.
First we will load the data, create a model, and specify a preprocessor for the data.

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

Next we place these steps in a `Pipeline` using
the [`make_pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.make_pipeline.html#sklearn.pipeline.make_pipeline) function.
The `make_pipeline` function takes a list of steps to apply in your data analysis; in this
case, we just have the `preprocessor` and `knn` steps.
Finally, we call `fit` on the pipeline.
Notice that we do not need to separately call `fit` and `transform` on the `preprocessor`; the
pipeline handles doing this properly for us.
Also notice that when we call `fit` on the pipeline, we can pass
the whole `unscaled_cancer` data frame to the `X` argument, since the preprocessing
step drops all the variables except the two we listed: `Area` and `Smoothness`.
For the `y` response variable argument, we pass the `unscaled_cancer["Class"]` series as before.

```{code-cell} ipython3
from sklearn.pipeline import make_pipeline

knn_pipeline = make_pipeline(preprocessor, knn)
knn_pipeline.fit(
    X=unscaled_cancer,
    y=unscaled_cancer["Class"]
)
knn_pipeline
```

As before, the fit object lists the function that trains the model. But now the fit object also includes information about
the overall workflow, including the standardization preprocessing step.
In other words, when we use the `predict` function with the `knn_pipeline` object to make a prediction for a new
observation, it will first apply the same preprocessing steps to the new observation.
As an example, we will predict the class label of two new observations:
one with `Area = 500` and `Smoothness = 0.075`, and one with `Area = 1500` and `Smoothness = 0.1`.

```{code-cell} ipython3
new_observation = pd.DataFrame({"Area": [500, 1500], "Smoothness": [0.075, 0.1]})
prediction = knn_pipeline.predict(new_observation)
prediction
```

The classifier predicts that the first observation is benign, while the second is
malignant. {numref}`fig:05-workflow-plot` visualizes the predictions that this
trained K-nearest neighbors model will make on a large range of new observations.
Although you have seen colored prediction map visualizations like this a few times now,
we have not included the code to generate them, as it is a little bit complicated.
For the interested reader who wants a learning challenge, we now include it below.
The basic idea is to create a grid of synthetic new observations using the `meshgrid` function from `numpy`,
predict the label of each, and visualize the predictions with a colored scatter having a very high transparency
(low `opacity` value) and large point radius. See if you can figure out what each line is doing!

```{note}
Understanding this code is not required for the remainder of the
textbook. It is included for those readers who would like to use similar
visualizations in their own data analyses.
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

Scatter plot of smoothness versus area where background color indicates the decision of the classifier.
:::

+++

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Classification I: training and predicting" row. You can preview a
non-interactive version of the worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.


+++

## References

```{bibliography}
:filter: docname in docnames
```
