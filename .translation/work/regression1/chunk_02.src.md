+++

```{note}
We are not specifying the `stratify` argument here like we did in
{numref}`Chapter %s <classification2>`, since
the `train_test_split` function cannot stratify based on a
quantitative variable.
```

```{code-cell} ipython3
:tags: [remove-cell]
# fix seed right before train/test split for reproducibility with next chapter
# make sure this seed is always the same as the one used before the split in Regression 2
np.random.seed(1)
```

```{code-cell} ipython3
sacramento_train, sacramento_test = train_test_split(
    sacramento, train_size=0.75
)
```

```{index} cross-validation, RMSPE
```

```{index} see: root mean square prediction error; RMSPE
```

Next, we'll use cross-validation to choose $K$. In K-NN classification, we used
accuracy to see how well our predictions matched the true labels. We cannot use
the same metric in the regression setting, since our predictions will almost never
*exactly* match the true response variable values. Therefore in the
context of K-NN regression we will use root mean square prediction error (RMSPE) instead.
The mathematical formula for calculating RMSPE is:

$$\text{RMSPE} = \sqrt{\frac{1}{n}\sum\limits_{i=1}^{n}(y_i - \hat{y}_i)^2}$$

where:

- $n$ is the number of observations,
- $y_i$ is the observed value for the $i^\text{th}$ observation, and
- $\hat{y}_i$ is the forecasted/predicted value for the $i^\text{th}$ observation.

In other words, we compute the *squared* difference between the predicted and true response
value for each observation in our test (or validation) set, compute the average, and then finally
take the square root. The reason we use the *squared* difference (and not just the difference)
is that the differences can be positive or negative, i.e., we can overshoot or undershoot the true
response value. {numref}`fig:07-verticalerrors` illustrates both positive and negative differences
between predicted and true response values.
So if we want to measure error&mdash;a notion of distance between our predicted and true response values&mdash;we
want to make sure that we are only adding up positive values, with larger positive values representing larger
mistakes.
If the predictions are very close to the true values, then
RMSPE will be small. If, on the other-hand, the predictions are very
different from the true values, then RMSPE will be quite large. When we
use cross-validation, we will choose the $K$ that gives
us the smallest RMSPE.

```{code-cell} ipython3
:tags: [remove-cell]

from sklearn.neighbors import KNeighborsRegressor

# (synthetic) new prediction points
pts = pd.DataFrame({"sqft": [1200, 1850, 2250], "price": [300000, 200000, 500000]})
finegrid = pd.DataFrame({"sqft": np.arange(600, 3901, 10)})

# preprocess the data, make the pipeline
sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft"]))
sacr_pipeline = make_pipeline(sacr_preprocessor, KNeighborsRegressor(n_neighbors=4))

# fit the model
X = small_sacramento[["sqft"]]
y = small_sacramento[["price"]]
sacr_pipeline.fit(X, y)

# predict on the full grid and new data pts
sacr_full_preds_hid = pd.concat(
    (finegrid, pd.DataFrame(sacr_pipeline.predict(finegrid), columns=["predicted"])),
    axis=1,
)

sacr_new_preds_hid = pd.concat(
    (small_sacramento[["sqft", "price"]].reset_index(), pd.DataFrame(sacr_pipeline.predict(small_sacramento[["sqft", "price"]]), columns=["predicted"])),
    axis=1,
).drop(columns=["index"])

# to make altair mark_line works, need to create separate dataframes for each vertical error line
errors_plot = (
    small_plot
    + alt.Chart(sacr_full_preds_hid).mark_line(color="#ff7f0e").encode(x="sqft", y="predicted")
    + alt.Chart(sacr_new_preds_hid)
    .mark_circle(opacity=1)
    .encode(x="sqft", y="price")
)
sacr_new_preds_melted_df = sacr_new_preds_hid.melt(id_vars=["sqft"])
v_lines = []
for i in sacr_new_preds_hid["sqft"]:
    line_df = sacr_new_preds_melted_df.query(f"sqft == {i}")
    v_lines.append(alt.Chart(line_df).mark_line(color="black").encode(x="sqft", y="value"))

errors_plot = alt.layer(*v_lines, errors_plot)
errors_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-verticalerrors", errors_plot, display=False)
```

:::{glue:figure} fig:07-verticalerrors
:name: fig:07-verticalerrors

Scatter plot of price (USD) versus house size (square feet) with example predictions (orange line) and the error in those predictions compared with true response values (vertical lines).
:::

+++

```{index} RMSPE; comparison with RMSE
```

```{note}
When using many code packages, the evaluation output
we will get to assess the prediction quality of
our K-NN regression models is labeled "RMSE", or "root mean squared
error". Why is this so, and why not RMSPE?
In statistics, we try to be very precise with our
language to indicate whether we are calculating the prediction error on the
training data (*in-sample* prediction) versus on the testing data
(*out-of-sample* prediction). When predicting and evaluating prediction quality on the training data, we
say RMSE. By contrast, when predicting and evaluating prediction quality
on the testing or validation data, we say RMSPE.
The equation for calculating RMSE and RMSPE is exactly the same; all that changes is whether the $y$s are
training or testing data. But many people just use RMSE for both,
and rely on context to denote which data the root mean squared error is being calculated on.
```

```{index} scikit-learn, scikit-learn; Pipeline, scikit-learn; make_pipeline, scikit-learn; make_column_transformer
```

Now that we know how we can assess how well our model predicts a numerical
value, let's use Python to perform cross-validation and to choose the optimal
$K$.  First, we will create a column transformer for preprocessing our data.  Note
that we include standardization in our preprocessing to build good habits, but
since we only have one predictor, it is technically not necessary; there is no
risk of comparing two predictors of different scales.  Next we create a model
pipeline for K-nearest neighbors regression. Note that we use the
`KNeighborsRegressor` model object now to denote a regression problem, as
opposed to the classification problems from the previous chapters.  The use of
`KNeighborsRegressor` essentially tells `scikit-learn` that we need to use
different metrics (instead of accuracy) for tuning and evaluation.  Next we
specify a parameter grid containing numbers of neighbors
ranging from 1 to 200.  Then we create a 5-fold `GridSearchCV` object, and
pass in the pipeline and parameter grid.
There is one additional slight complication: unlike classification models in `scikit-learn`---which
by default use accuracy for tuning, as desired---regression models in `scikit-learn`
do not use the RMSPE for tuning by default.
So we need to specify that we want to use the RMSPE for tuning by setting the
`scoring` argument to `"neg_root_mean_squared_error"`.

```{note}
We obtained the identifier of the parameter representing the number
of neighbours, `"kneighborsregressor__n_neighbors"` by examining the output
of `sacr_pipeline.get_params()`, as we did in {numref}`Chapter %s <classification1>`.
```

```{index} scikit-learn; GridSearchCV
```

```{code-cell} ipython3
# import the K-NN regression model
from sklearn.neighbors import KNeighborsRegressor

# preprocess the data, make the pipeline
sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft"]))
sacr_pipeline = make_pipeline(sacr_preprocessor, KNeighborsRegressor())

# create the 5-fold GridSearchCV object
param_grid = {
    "kneighborsregressor__n_neighbors": range(1, 201, 3),
}
sacr_gridsearch = GridSearchCV(
    estimator=sacr_pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="neg_root_mean_squared_error",
)
```

Next, we use the run cross validation by calling the `fit` method
on `sacr_gridsearch`. Note the use of two brackets for the input features
(`sacramento_train[["sqft"]]`), which creates a data frame with a single column.
As we learned in {numref}`Chapter %s <wrangling>`, we can obtain a data frame with a
subset of columns by passing a list of column names; `["sqft"]` is a list with one
item, so we obtain a data frame with one column. If instead we used
just one bracket (`sacramento_train["sqft"]`), we would obtain a series.
In `scikit-learn`, it is easier to work with the input features as a data frame
rather than a series, so we opt for two brackets here. On the other hand, the response variable
can be a series, so we use just one bracket there (`sacramento_train["price"]`).

As in {numref}`Chapter %s <classification2>`, once the model has been fit
we will wrap the `cv_results_` output in a data frame, extract
only the relevant columns, compute the standard error based on 5 folds,
and rename the parameter column to be more readable.


```{code-cell} ipython3
# fit the GridSearchCV object
sacr_gridsearch.fit(
    sacramento_train[["sqft"]],  # A single-column data frame
    sacramento_train["price"]  # A series
)

# Retrieve the CV scores
sacr_results = pd.DataFrame(sacr_gridsearch.cv_results_)
sacr_results["sem_test_score"] = sacr_results["std_test_score"] / 5**(1/2)
sacr_results = (
    sacr_results[[
        "param_kneighborsregressor__n_neighbors",
        "mean_test_score",
        "sem_test_score"
    ]]
    .rename(columns={"param_kneighborsregressor__n_neighbors": "n_neighbors"})
)
sacr_results
```

In the `sacr_results` results data frame, we see that the
`n_neighbors` variable contains the values of $K$,
and `mean_test_score` variable contains the value of the RMSPE estimated via
cross-validation...Wait a moment! Isn't the RMSPE supposed to be nonnegative?
Recall that when we specified the `scoring` argument in the `GridSearchCV` object,
we used the value `"neg_root_mean_squared_error"`. See the `neg_` at the start?
That stands for *negative*! As it turns out, `scikit-learn` always tries to *maximize* a score
when it tunes a model. But we want to *minimize* the RMSPE when we tune a regression
model. So `scikit-learn` gets around this by working with the *negative* RMSPE instead.
It is a little convoluted, but we need to add one more step to convert the negative
RMSPE back to the regular RMSPE.

```{code-cell} ipython3
sacr_results["mean_test_score"] = -sacr_results["mean_test_score"]
sacr_results
```

Alright, now the `mean_test_score` variable actually has values of the RMSPE
for different numbers of neighbors. Finally, the `sem_test_score` variable
contains the standard error of our cross-validation RMSPE estimate, which
is a measure of how uncertain we are in the mean value. Roughly, if
your estimated mean RMSPE is \$100,000 and standard error is \$1,000, you can expect the
*true* RMSPE to be somewhere roughly between \$99,000 and \$101,000 (although it
may fall outside this range).

{numref}`fig:07-choose-k-knn-plot` visualizes how the RMSPE varies with the number of neighbors $K$.
We take the *minimum* RMSPE to find the best setting for the number of neighbors.
The smallest RMSPE occurs when $K$ is {glue:text}`best_k_sacr`.

```{code-cell} ipython3
:tags: [remove-cell]
best_k_sacr = sacr_results["n_neighbors"][sacr_results["mean_test_score"].idxmin()]
best_cv_RMSPE = min(sacr_results["mean_test_score"])
glue("best_k_sacr", "{:d}".format(best_k_sacr))
glue("cv_RMSPE", "{0:,.0f}".format(best_cv_RMSPE))
```

```{code-cell} ipython3
:tags: [remove-cell]

sacr_tunek_plot = alt.Chart(sacr_results).mark_line(point=True).encode(
    x=alt.X("n_neighbors:Q", title="Neighbors"),
    y=alt.Y("mean_test_score", scale=alt.Scale(zero=False), title="Cross-Validation RMSPE Estimate")
)

sacr_tunek_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-choose-k-knn-plot", sacr_tunek_plot, display=False)
```

:::{glue:figure} fig:07-choose-k-knn-plot
:name: fig:07-choose-k-knn-plot

Effect of the number of neighbors on the RMSPE.
:::

To see which parameter value corresponds to the minimum RMSPE,
we can also access the `best_params_` attribute of the original fit `GridSearchCV` object.
Note that it is still useful to visualize the results as we did above
since this provides additional information on how the model performance varies.

```{code-cell} ipython3
sacr_gridsearch.best_params_
```

+++

## Underfitting and overfitting
Similar to the setting of classification, by setting the number of neighbors
to be too small or too large, we cause the RMSPE to increase, as shown in
{numref}`fig:07-choose-k-knn-plot`. What is happening here?

{numref}`fig:07-howK` visualizes the effect of different settings of $K$ on the
regression model. Each plot shows the predicted values for house sale price from
our K-NN regression model for 6 different values for $K$: 1, 3, 25, {glue:text}`best_k_sacr`, 250, and 699 (i.e., all of the training data).
For each model, we predict prices for the range of possible home sizes we
observed in the data set (here 500 to 5,000 square feet) and we plot the
predicted prices as a orange line.

```{code-cell} ipython3
:tags: [remove-cell]

gridvals = [
    1,
    3,
    25,
    best_k_sacr,
    250,
    len(sacramento_train),
]

plots = list()

sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft"]))
X = sacramento_train[["sqft"]]
y = sacramento_train[["price"]]

base_plot = (
    alt.Chart(sacramento_train)
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size (square feet)", scale=alt.Scale(zero=False)),
        y=alt.Y("price", title="Price (USD)", axis=alt.Axis(format="$,.0f")),
    )
)
for i in range(len(gridvals)):
    # make the pipeline based on n_neighbors
    sacr_pipeline = make_pipeline(
        sacr_preprocessor, KNeighborsRegressor(n_neighbors=gridvals[i])
    )
    sacr_pipeline.fit(X, y)
    # predictions
    sacr_preds = sacramento_train
    sacr_preds = sacr_preds.assign(predicted=sacr_pipeline.predict(sacramento_train))
    # overlay the plots
    plots.append(
        base_plot
        + alt.Chart(sacr_preds, title=f"K = {gridvals[i]}")
        .mark_line(color="#ff7f0e")
        .encode(x="sqft", y="predicted")
    )
```

```{code-cell} ipython3
:tags: [remove-cell]

glue(
    "fig:07-howK", (plots[0] | plots[1]) & (plots[2] | plots[3]) & (plots[4] | plots[5])
)
```

:::{glue:figure} fig:07-howK
:name: fig:07-howK

Predicted values for house price (represented as a orange line) from K-NN regression models for six different values for $K$.
:::

+++

```{index} overfitting; regression
```

{numref}`fig:07-howK` shows that when $K$ = 1, the orange line runs perfectly
through (almost) all of our training observations.
This happens because our
predicted values for a given region (typically) depend on just a single observation.
In general, when $K$ is too small, the line follows the training data quite
closely, even if it does not match it perfectly.
If we used a different training data set of house prices and sizes
from the Sacramento real estate market, we would end up with completely different
predictions. In other words, the model is *influenced too much* by the data.
Because the model follows the training data so closely, it will not make accurate
predictions on new observations which, generally, will not have the same fluctuations
as the original training data.
Recall from the classification
chapters that this behavior&mdash;where the model is influenced too much
by the noisy data&mdash;is called *overfitting*; we use this same term
in the context of regression.

```{index} underfitting; regression
```

What about the plots in {numref}`fig:07-howK` where $K$ is quite large,
say, $K$ = 250 or 699?
In this case the orange line becomes extremely smooth, and actually becomes flat
once $K$ is equal to the number of datapoints in the entire data set.
This happens because our predicted values for a given x value (here, home
size), depend on many neighboring observations; in the case where $K$ is equal
to the size of the data set, the prediction is just the mean of the house prices
in the data set (completely ignoring the house size).
In contrast to the $K=1$ example,
the smooth, inflexible orange line does not follow the training observations very closely.
In other words, the model is *not influenced enough* by the training data.
Recall from the classification
chapters that this behavior is called *underfitting*; we again use this same
term in the context of regression.

Ideally, what we want is neither of the two situations discussed above. Instead,
we would like a model that (1) follows the overall "trend" in the training data, so the model
actually uses the training data to learn something useful, and (2) does not follow
the noisy fluctuations, so that we can be confident that our model will transfer/generalize
well to other new data. If we explore
the other values for $K$, in particular $K$ = {glue:text}`best_k_sacr` (as suggested by cross-validation),
we can see it achieves this goal: it follows the increasing trend of house price
versus house size, but is not influenced too much by the idiosyncratic variations
in price. All of this is similar to how
the choice of $K$ affects K-nearest neighbors classification, as discussed in the previous
chapter.

