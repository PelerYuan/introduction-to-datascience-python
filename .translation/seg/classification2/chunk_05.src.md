+++

```{index} cross-validation; cross_validate, scikit-learn; cross_validate
```

To perform 5-fold cross-validation in Python with `scikit-learn`, we use another
function: `cross_validate`. This function requires that we specify
a modelling `Pipeline` as the `estimator` argument,
the number of folds as the `cv` argument,
and the training data predictors and labels as the `X` and `y` arguments.
Since the `cross_validate` function outputs a dictionary, we use `pd.DataFrame` to convert it to a `pandas`
dataframe for better visualization.
Note that the `cross_validate` function handles stratifying the classes in
each train and validate fold automatically.

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

```{index} see: sem;standard error
```

```{index} standard error, DataFrame;agg
```

The validation scores we are interested in are contained in the `test_score` column.
We can then aggregate the *mean* and *standard error*
of the classifier's validation accuracy across the folds.
You should consider the mean (`mean`) to be the estimated accuracy, while the standard
error (`sem`) is a measure of how uncertain we are in that mean value. A detailed treatment of this
is beyond the scope of this chapter; but roughly, if your estimated mean is {glue:text}`cv_5_mean` and standard
error is {glue:text}`cv_5_std`, you can expect the *true* average accuracy of the
classifier to be somewhere roughly between {glue:text}`cv_5_lower`% and {glue:text}`cv_5_upper`% (although it may
fall outside this range). You may ignore the other columns in the metrics data frame.

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

We can choose any number of folds, and typically the more we use the better our
accuracy estimate will be (lower standard error). However, we are limited
by computational power: the
more folds we choose, the  more computation it takes, and hence the more time
it takes to run the analysis. So when you do cross-validation, you need to
consider the size of the data, the speed of the algorithm (e.g., K-nearest
neighbors), and the speed of your computer. In practice, this is a
trial-and-error process, but typically $C$ is chosen to be either 5 or 10. Here
we will try 10-fold cross-validation to see if we get a lower standard error.

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

```{index} cross-validation; folds
```

In this case, using 10-fold instead of 5-fold cross validation did
reduce the standard error very slightly. In fact, due to the randomness in how the data are split, sometimes
you might even end up with a *higher* standard error when increasing the number of folds!
We can make the reduction in standard error more dramatic by increasing the number of folds
by a large amount. In the following code we show the result when $C = 50$;
picking such a large number of folds can take a long time to run in practice,
so we usually stick to 5 or 10.

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

### Parameter value selection

Using 5- and 10-fold cross-validation, we have estimated that the prediction
accuracy of our classifier is somewhere around {glue:text}`cv_10_mean`%.
Whether that is good or not
depends entirely on the downstream application of the data analysis. In the
present situation, we are trying to predict a tumor diagnosis, with expensive,
damaging chemo/radiation therapy or patient death as potential consequences of
misprediction. Hence, we might like to
do better than {glue:text}`cv_10_mean`% for this application.

In order to improve our classifier, we have one choice of parameter: the number of
neighbors, $K$. Since cross-validation helps us evaluate the accuracy of our
classifier, we can use cross-validation to calculate an accuracy for each value
of $K$ in a reasonable range, and then pick the value of $K$ that gives us the
best accuracy. The `scikit-learn` package collection provides built-in
functionality, named `GridSearchCV`, to automatically handle the details for us.
Before we use `GridSearchCV`, we need to create a new pipeline
with a `KNeighborsClassifier` that has the number of neighbors left unspecified.

```{index} see: make_pipeline; scikit-learn
```
```{index} scikit-learn;make_pipeline
```

```{code-cell} ipython3
knn = KNeighborsClassifier()
cancer_tune_pipe = make_pipeline(cancer_preprocessor, knn)
```

+++

Next we specify the grid of parameter values that we want to try for
each tunable parameter. We do this in a Python dictionary: the key is
the identifier of the parameter to tune, and the value is a list of parameter values
to try when tuning. We can find the "identifier" of a parameter by using
the `get_params` method on the pipeline.
```{code-cell} ipython3
cancer_tune_pipe.get_params()
```
Wow, there's quite a bit of *stuff* there! If you sift through the muck
a little bit, you will see one parameter identifier that stands out:
`"kneighborsclassifier__n_neighbors"`. This identifier combines the name
of the K nearest neighbors classification step in our pipeline, `kneighborsclassifier`,
with the name of the parameter, `n_neighbors`.
We now construct the `parameter_grid` dictionary that will tell `GridSearchCV`
what parameter values to try.
Note that you can specify multiple tunable parameters
by creating a dictionary with multiple key-value pairs, but
here we just have to tune the number of neighbors.
```{code-cell} ipython3
parameter_grid = {
    "kneighborsclassifier__n_neighbors": range(1, 100, 5),
}
```
The `range` function in Python that we used above allows us to specify a sequence of values.
The first argument is the starting number (here, `1`),
the second argument is *one greater than* the final number (here, `100`),
and the third argument is the number to values to skip between steps in the sequence (here, `5`).
So in this case we generate the sequence 1, 6, 11, 16, ..., 96.
If we instead specified `range(0, 100, 5)`, we would get the sequence 0, 5, 10, 15, ..., 90, 95.
The number 100 is not included because the third argument is *one greater than* the final possible
number in the sequence. There are two additional useful ways to employ `range`.
If we call `range` with just one argument, Python counts
up to that number starting at 0. So `range(4)` is the same as `range(0, 4, 1)` and generates the sequence 0, 1, 2, 3.
If we call `range` with two arguments, Python counts starting at the first number up to the second number.
So `range(1, 4)` is the same as `range(1, 4, 1)` and generates the sequence `1, 2, 3`.

```{index} cross-validation; GridSearchCV, scikit-learn; GridSearchCV, scikit-learn; RandomizedSearchCV
```

Okay! We are finally ready to create the `GridSearchCV` object.
First we import it from the `sklearn` package.
Then we pass it the `cancer_tune_pipe` pipeline in the `estimator` argument,
the `parameter_grid` in the `param_grid` argument,
and specify `cv=10` folds. Note that this does not actually run
the tuning yet; just as before, we will have to use the `fit` method.

```{code-cell} ipython3
from sklearn.model_selection import GridSearchCV

cancer_tune_grid = GridSearchCV(
    estimator=cancer_tune_pipe,
    param_grid=parameter_grid,
    cv=10
)
```

Now we use the `fit` method on the `GridSearchCV` object to begin the tuning process.
We pass the training data predictors and labels as the two arguments to `fit` as usual.
The `cv_results_` attribute of the output contains the resulting cross-validation
accuracy estimate for each choice of `n_neighbors`, but it isn't in an easily used
format. We will wrap it in a `pd.DataFrame` to make it easier to understand,
and print the `info` of the result.

```{code-cell} ipython3
cancer_tune_grid.fit(
    cancer_train[["Smoothness", "Concavity"]],
    cancer_train["Class"]
)
accuracies_grid = pd.DataFrame(cancer_tune_grid.cv_results_)
accuracies_grid.info()
```

There is a lot of information to look at here, but we are most interested
in three quantities: the number of neighbors (`param_kneighbors_classifier__n_neighbors`),
the cross-validation accuracy estimate (`mean_test_score`),
and the standard error of the accuracy estimate. Unfortunately `GridSearchCV` does
not directly output the standard error for each cross-validation accuracy; but
it *does* output the standard *deviation* (`std_test_score`). We can compute
the standard error from the standard deviation by dividing it by the square
root of the number of folds, i.e.,

$$\text{Standard Error} = \frac{\text{Standard Deviation}}{\sqrt{\text{Number of Folds}}}.$$

We will also rename the parameter name column to be a bit more readable,
and drop the now unused `std_test_score` column.

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

We can decide which number of neighbors is best by plotting the accuracy versus $K$,
as shown in {numref}`fig:06-find-k`.
Here we are using the shortcut `point=True` to layer a point and line chart.

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

Plot of estimated accuracy versus the number of neighbors.
:::

We can also obtain the number of neighbours with the highest accuracy programmatically by accessing
the `best_params_` attribute of the fit `GridSearchCV` object. Note that it is still useful to visualize
the results as we did above since this provides additional information on how the model performance varies.
```{code-cell} ipython3
cancer_tune_grid.best_params_
```

