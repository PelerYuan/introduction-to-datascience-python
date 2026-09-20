## Evaluating on the test set

To assess how well our model might do at predicting on unseen data, we will
assess its RMSPE on the test data. To do this, we first need to retrain the
K-NN regression model on the entire training data set using $K =$ {glue:text}`best_k_sacr`
neighbors. As we saw in {numref}`Chapter %s <classification2>` we do not have to do this ourselves manually; `scikit-learn`
does it for us automatically. To make predictions with the best model on the test data,
we can use the `predict` method of the fit `GridSearchCV` object.
We then use the `mean_squared_error` function (with the `y_true` and `y_pred` arguments)
to compute the mean squared prediction error, and finally take the
square root to get the RMSPE. The reason that we do not just use the `score`
method---as in {numref}`Chapter %s <classification2>`---is that the `KNeighborsRegressor`
model uses a different default scoring metric than the RMSPE.

```{code-cell} ipython3
from sklearn.metrics import mean_squared_error

sacramento_test["predicted"] = sacr_gridsearch.predict(sacramento_test)
RMSPE = mean_squared_error(
    y_true=sacramento_test["price"],
    y_pred=sacramento_test["predicted"]
)**(1/2)
RMSPE
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("test_RMSPE", "{0:,.0f}".format(RMSPE))
```

Our final model's test error as assessed by RMSPE
is \${glue:text}`test_RMSPE`.
Note that RMSPE is measured in the same units as the response variable.
In other words, on new observations, we expect the error in our prediction to be
*roughly* \${glue:text}`test_RMSPE`.
From one perspective, this is good news: this is about the same as the cross-validation
RMSPE estimate of our tuned model
(which was \${glue:text}`cv_RMSPE`,
so we can say that the model appears to generalize well
to new data that it has never seen before.
However, much like in the case of K-NN classification, whether this value for RMSPE is *good*&mdash;i.e.,
whether an error of around \${glue:text}`test_RMSPE`
is acceptable&mdash;depends entirely on the application.
In this application, this error
is not prohibitively large, but it is not negligible either;
\${glue:text}`test_RMSPE`
might represent a substantial fraction of a home buyer's budget, and
could make or break whether or not they could afford put an offer on a house.

Finally, {numref}`fig:07-predict-all` shows the predictions that our final
model makes across the range of house sizes we might encounter in the
Sacramento area.
Note that instead of predicting the house price only for those house sizes that happen to appear in our data,
we predict it for evenly spaced values between the minimum and maximum in the data set
(roughly 500 to 5000 square feet).
We superimpose this prediction line on a scatter
plot of the original housing price data,
so that we can qualitatively assess if the model seems to fit the data well.
You have already seen a
few plots like this in this chapter, but here we also provide the code that
generated it as a learning opportunity.

```{code-cell} ipython3
:tags: [remove-output]

# Create a grid of evenly spaced values along the range of the sqft data
sqft_prediction_grid = pd.DataFrame({
    "sqft": np.arange(sacramento["sqft"].min(), sacramento["sqft"].max(), 10)
})
# Predict the price for each of the sqft values in the grid
sqft_prediction_grid["predicted"] = sacr_gridsearch.predict(sqft_prediction_grid)

# Plot all the houses
base_plot = alt.Chart(sacramento).mark_circle(opacity=0.4).encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .title("Price (USD)")
)

# Add the predictions as a line
sacr_preds_plot = base_plot + alt.Chart(
    sqft_prediction_grid,
    title=f"K = {best_k_sacr}"
).mark_line(
    color="#ff7f0e"
).encode(
    x="sqft",
    y="predicted"
)

sacr_preds_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-predict-all", sacr_preds_plot)
```

:::{glue:figure} fig:07-predict-all
:name: fig:07-predict-all

Predicted values of house price (orange line) for the final K-NN regression model.
:::

+++

## Multivariable K-NN regression

As in K-NN classification, we can use multiple predictors in K-NN regression.
In this setting, we have the same concerns regarding the scale of the predictors. Once again,
 predictions are made by identifying the $K$
observations that are nearest to the new point we want to predict; any
variables that are on a large scale will have a much larger effect than
variables on a small scale. Hence, we should re-define the preprocessor in the
pipeline to incorporate all predictor variables.

Note that we also have the same concern regarding the selection of predictors
in K-NN regression as in K-NN classification: having more predictors is **not** always
better, and the choice of which predictors to use has a potentially large influence
on the quality of predictions. Fortunately, we can use the predictor selection
algorithm from {numref}`Chapter %s <classification2>` in K-NN regression as well.
As the algorithm is the same, we will not cover it again in this chapter.

```{index} K-nearest neighbors; multivariable regression, Sacramento real estate
```

We will now demonstrate a multivariable K-NN regression analysis of the
Sacramento real estate data using `scikit-learn`. This time we will use
house size (measured in square feet) as well as number of bedrooms as our
predictors, and continue to use house sale price as our response variable
that we are trying to predict.
It is always a good practice to do exploratory data analysis, such as
visualizing the data, before we start modeling the data. {numref}`fig:07-bedscatter`
shows that the number of bedrooms might provide useful information
to help predict the sale price of a house.

```{code-cell} ipython3
:tags: [remove-output]

plot_beds = alt.Chart(sacramento).mark_circle().encode(
    x=alt.X("beds").title("Number of Bedrooms"),
    y=alt.Y("price").title("Price (USD)").axis(format="$,.0f"),
)

plot_beds
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-bedscatter", plot_beds)
```

:::{glue:figure} fig:07-bedscatter
:name: fig:07-bedscatter

Scatter plot of the sale price of houses versus the number of bedrooms.
:::

+++

{numref}`fig:07-bedscatter` shows that as the number of bedrooms increases,
the house sale price tends to increase as well, but that the relationship
is quite weak. Does adding the number of bedrooms
to our model improve our ability to predict price? To answer that
question, we will have to create a new K-NN regression
model using house size and number of bedrooms, and then we can compare it to
the model we previously came up with that only used house
size. Let's do that now!

First we'll build a new model object and preprocessor for the analysis.
Note that we pass the list `["sqft", "beds"]` into the `make_column_transformer`
function to denote that we have two predictors.  Moreover, we do not specify `n_neighbors` in
`KNeighborsRegressor`, indicating that we want this parameter to be tuned by `GridSearchCV`.

```{code-cell} ipython3
sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft", "beds"]))
sacr_pipeline = make_pipeline(sacr_preprocessor, KNeighborsRegressor())
```

Next, we'll use 5-fold cross-validation with a `GridSearchCV` object
to choose the number of neighbors via the minimum RMSPE:

```{code-cell} ipython3
# create the 5-fold GridSearchCV object
param_grid = {
    "kneighborsregressor__n_neighbors": range(1, 50),
}

sacr_gridsearch = GridSearchCV(
    estimator=sacr_pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="neg_root_mean_squared_error"
)

sacr_gridsearch.fit(
  sacramento_train[["sqft", "beds"]],
  sacramento_train["price"]
)

# retrieve the CV scores
sacr_results = pd.DataFrame(sacr_gridsearch.cv_results_)
sacr_results["sem_test_score"] = sacr_results["std_test_score"] / 5**(1/2)
sacr_results["mean_test_score"] = -sacr_results["mean_test_score"]
sacr_results = (
    sacr_results[[
        "param_kneighborsregressor__n_neighbors",
        "mean_test_score",
        "sem_test_score"
    ]]
    .rename(columns={"param_kneighborsregressor__n_neighbors" : "n_neighbors"})
)

# show only the row of minimum RMSPE
sacr_results.nsmallest(1, "mean_test_score")
```

```{code-cell} ipython3
:tags: [remove-cell]

best_k_sacr_multi = sacr_results["n_neighbors"][sacr_results["mean_test_score"].idxmin()]
min_rmspe_sacr_multi = min(sacr_results["mean_test_score"])
glue("best_k_sacr_multi", "{:d}".format(best_k_sacr_multi))
glue("cv_RMSPE_2pred", "{0:,.0f}".format(min_rmspe_sacr_multi))
```

Here we see that the smallest estimated RMSPE from cross-validation occurs when $K =$ {glue:text}`best_k_sacr_multi`.
If we want to compare this multivariable K-NN regression model to the model with only a single
predictor *as part of the model tuning process* (e.g., if we are running forward selection as described
in the chapter on evaluating and tuning classification models),
then we must compare the RMSPE estimated using only the training data via cross-validation.
Looking back, the estimated cross-validation RMSPE for the single-predictor
model was \${glue:text}`cv_RMSPE`.
The estimated cross-validation RMSPE for the multivariable model is
\${glue:text}`cv_RMSPE_2pred`.
Thus in this case, we did not improve the model
by a large amount by adding this additional predictor.

Regardless, let's continue the analysis to see how we can make predictions with a multivariable K-NN regression model
and evaluate its performance on test data. As previously, we will use the best model to make predictions on the test data
via the `predict` method of the fit `GridSearchCV` object. Finally, we will use the `mean_squared_error` function
to compute the RMSPE.

```{code-cell} ipython3
sacramento_test["predicted"] = sacr_gridsearch.predict(sacramento_test)
RMSPE_mult = mean_squared_error(
    y_true=sacramento_test["price"],
    y_pred=sacramento_test["predicted"]
)**(1/2)
RMSPE_mult

```

```{code-cell} ipython3
:tags: [remove-cell]

glue("RMSPE_mult", "{0:,.0f}".format(RMSPE_mult))
```

This time, when we performed K-NN regression on the same data set, but also
included number of bedrooms as a predictor, we obtained a RMSPE test error
of \${glue:text}`RMSPE_mult`.
{numref}`fig:07-knn-mult-viz` visualizes the model's predictions overlaid on top of the data. This
time the predictions are a surface in 3D space, instead of a line in 2D space, as we have 2
predictors instead of 1.

```{code-cell} ipython3
:tags: [remove-input]

# create a prediction pt grid
xvals = np.linspace(
    sacramento_train["sqft"].min(), sacramento_train["sqft"].max(), 50
)
yvals = np.linspace(
    sacramento_train["beds"].min(), sacramento_train["beds"].max(), 50
)
xygrid = np.array(np.meshgrid(xvals, yvals)).reshape(2, -1).T
xygrid = pd.DataFrame(xygrid, columns=["sqft", "beds"])

# add prediction
knnPredGrid = sacr_gridsearch.predict(xygrid)

fig = px.scatter_3d(
    sacramento_train,
    x="sqft",
    y="beds",
    z="price",
    opacity=0.4,
    labels={"sqft": "Size (sq ft)", "beds": "Bedrooms", "price": "Price (USD)"},
)

fig.update_traces(marker={"size": 2, "color": "red"})

fig.add_trace(
    go.Surface(
        x=xvals,
        y=yvals,
        z=knnPredGrid.reshape(50, -1),
        name="Predictions",
        colorscale="viridis",
        colorbar={"title": "Price (USD)"}
    )
)

fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=1),
    template="plotly_white",
)

# if HTML, use the plotly 3d image; if PDF, use static image
if "BOOK_BUILD_TYPE" in os.environ and os.environ["BOOK_BUILD_TYPE"] == "PDF":
    glue("fig:07-knn-mult-viz", Image("img/regression1/plot3d_knn_regression.png"))
else:
    glue("fig:07-knn-mult-viz", fig)
```

```{figure} data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
:name: fig:07-knn-mult-viz
:figclass: caption-hack

K-NN regression model's predictions represented as a surface in 3D space overlaid on top of the data using three predictors (price, house size, and the number of bedrooms). Note that in general we recommend against using 3D visualizations; here we use a 3D visualization only to illustrate what the surface of predictions looks like for learning purposes.
```

+++

We can see that the predictions in this case, where we have 2 predictors, form
a surface instead of a line. Because the newly added predictor (number of bedrooms) is
related to price (as price changes, so does number of bedrooms)
and is not totally determined by house size (our other predictor),
we get additional and useful information for making our
predictions. For example, in this model we would predict that the cost of a
house with a size of 2,500 square feet generally increases slightly as the number
of bedrooms increases. Without having the additional predictor of number of
bedrooms, we would predict the same price for these two houses.

+++

## Strengths and limitations of K-NN regression

As with K-NN classification (or any prediction algorithm for that matter), K-NN
regression has both strengths and weaknesses. Some are listed here:

**Strengths:** K-nearest neighbors regression

1. is a simple, intuitive algorithm,
2. requires few assumptions about what the data must look like, and
3. works well with non-linear relationships (i.e., if the relationship is not a straight line).

**Weaknesses:** K-nearest neighbors regression

1. becomes very slow as the training data gets larger,
2. may not perform well with a large number of predictors, and
3. may not predict well beyond the range of values input in your training data.

+++

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Regression I: K-nearest neighbors" row. You can preview a
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
