+++

Our coefficients are
(intercept) $\beta_0=$ {glue:text}`train_lm_intercept`
and (slope) $\beta_1=$ {glue:text}`train_lm_slope`.
This means that the equation of the line of best fit is

$\text{house sale price} =$ {glue:text}`train_lm_intercept` $+$ {glue:text}`train_lm_slope` $\cdot (\text{house size}).$

In other words, the model predicts that houses
start at \${glue:text}`train_lm_intercept_f` for 0 square feet, and that
every extra square foot increases the cost of
the house by \${glue:text}`train_lm_slope_f`. Finally,
we predict on the test data set to assess how well our model does.

```{code-cell} ipython3
# make predictions
sacramento_test["predicted"] = lm.predict(sacramento_test[["sqft"]])

# calculate RMSPE
RMSPE = mean_squared_error(
    y_true=sacramento_test["price"],
    y_pred=sacramento_test["predicted"]
)**(1/2)

RMSPE
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("sacr_RMSPE", "{0:,.0f}".format(RMSPE))
```

```{index} RMSPE
```

Our final model's test error as assessed by RMSPE
is \${glue:text}`sacr_RMSPE`.
Remember that this is in units of the response variable, and here that
is US Dollars (USD). Does this mean our model is "good" at predicting house
sale price based off of the predictor of home size? Again, answering this is
tricky and requires knowledge of how you intend to use the prediction.

To visualize the simple linear regression model, we can plot the predicted house
sale price across all possible house sizes we might encounter.
Since our model is linear,
we only need to compute the predicted price of the minimum and maximum house size,
and then connect them with a straight line.
We superimpose this prediction line on a scatter
plot of the original housing price data,
so that we can qualitatively assess if the model seems to fit the data well.
{numref}`fig:08-lm-predict-all` displays the result.

```{code-cell} ipython3
:tags: [remove-output]
sqft_prediction_grid = sacramento[["sqft"]].agg(["min", "max"])
sqft_prediction_grid["predicted"] = lm.predict(sqft_prediction_grid)

all_points = alt.Chart(sacramento).mark_circle().encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .scale(zero=False)
        .title("Price (USD)")
)

sacr_preds_plot = all_points + alt.Chart(sqft_prediction_grid).mark_line(
    color="#ff7f0e"
).encode(
    x="sqft",
    y="predicted"
)

sacr_preds_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-lm-predict-all", sacr_preds_plot)
```

:::{glue:figure} fig:08-lm-predict-all
:name: fig:08-lm-predict-all

Scatter plot of sale price versus size with line of best fit for the full Sacramento housing data.
:::

## Comparing simple linear and K-NN regression

```{index} regression; comparison of methods
```

Now that we have a general understanding of both simple linear and K-NN
regression, we can start to compare and contrast these methods as well as the
predictions made by them. To start, let's look at the visualization of the
simple linear regression model predictions for the Sacramento real estate data
(predicting price from house size) and the "best" K-NN regression model
obtained from the same problem, shown in {numref}`fig:08-compareRegression`.

```{code-cell} ipython3
:tags: [remove-cell]
from sklearn.model_selection import GridSearchCV
from sklearn.compose import make_column_transformer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# preprocess the data, make the pipeline
sacr_preprocessor = make_column_transformer((StandardScaler(), ["sqft"]))
sacr_pipeline_knn = make_pipeline(
    sacr_preprocessor, KNeighborsRegressor(n_neighbors=55)
)  # 55 is the best parameter obtained through cross validation in regression1 chapter

sacr_pipeline_knn.fit(sacramento_train[["sqft"]], sacramento_train[["price"]])

# knn in-sample predictions (on training split)
sacr_preds_knn = sacramento_train
sacr_preds_knn = sacr_preds_knn.assign(
    knn_predicted=sacr_pipeline_knn.predict(sacramento_train)
)

# knn out-of-sample predictions (on test split)
sacr_preds_knn_test = sacramento_test
sacr_preds_knn_test = sacr_preds_knn_test.assign(
    knn_predicted=sacr_pipeline_knn.predict(sacramento_test)
)

sacr_rmspe_knn = np.sqrt(
    mean_squared_error(
        y_true=sacr_preds_knn_test["price"], y_pred=sacr_preds_knn_test["knn_predicted"]
    )
)

# plot knn in-sample predictions overlaid on scatter plot
knn_plot_final = (
    alt.Chart(sacr_preds_knn, title="K-NN regression")
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size (square feet)", scale=alt.Scale(zero=False)),
        y=alt.Y(
            "price",
            title="Price (USD)",
            axis=alt.Axis(format="$,.0f"),
            scale=alt.Scale(zero=False),
        ),
    )
)

knn_plot_final = (
    knn_plot_final
    + knn_plot_final.mark_line(color="#ff7f0e").encode(x="sqft", y="knn_predicted")
    + alt.Chart(  # add the text
        pd.DataFrame(
            {
                "x": [3500],
                "y": [100000],
                "rmspe": [f"RMSPE = {round(sacr_rmspe_knn)}"],
            }
        )
    )
    .mark_text(dy=-5, size=15)
    .encode(x="x", y="y", text="rmspe")
)


# add more components to lm_plot_final
lm_plot_final = (
    alt.Chart(sacramento_train, title="linear regression")
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size (square feet)", scale=alt.Scale(zero=False)),
        y=alt.Y(
            "price",
            title="Price (USD)",
            axis=alt.Axis(format="$,.0f"),
            scale=alt.Scale(zero=False),
        ),
    )
)

lm_plot_final = (
    lm_plot_final
    + lm_plot_final.transform_regression("sqft", "price").mark_line(color="#ff7f0e")
    + alt.Chart(  # add the text
        pd.DataFrame(
            {
                "x": [3500],
                "y": [100000],
                "rmspe": [f"RMSPE = {round(RMSPE)}"],
            }
        )
    )
    .mark_text(dy=-5, size=15)
    .encode(x="x", y="y", text="rmspe")
)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-compareRegression", (lm_plot_final | knn_plot_final))
```

:::{glue:figure} fig:08-compareRegression
:name: fig:08-compareRegression

Comparison of simple linear regression and K-NN regression.
:::

+++

What differences do we observe in {numref}`fig:08-compareRegression`? One obvious
difference is the shape of the orange lines. In simple linear regression we are
restricted to a straight line, whereas in K-NN regression our line is much more
flexible and can be quite wiggly. But there is a major interpretability advantage in limiting the
model to a straight line. A
straight line can be defined by two numbers, the
vertical intercept and the slope. The intercept tells us what the prediction is when
all of the predictors are equal to 0; and the slope tells us what unit increase in the response
variable we predict given a unit increase in the predictor
variable. K-NN regression, as simple as it is to implement and understand, has no such
interpretability from its wiggly line.

```{index} underfitting; regression
```

There can, however, also be a disadvantage to using a simple linear regression
model in some cases, particularly when the relationship between the response variable and
the predictor is not linear, but instead some other shape (e.g., curved or oscillating). In
these cases the prediction model from a simple linear regression
will underfit, meaning that model/predicted values do not
match the actual observed values very well. Such a model would probably have a
quite high RMSE when assessing model goodness of fit on the training data and
a quite high RMSPE when assessing model prediction quality on a test data
set. On such a data set, K-NN regression may fare better. Additionally, there
are other types of regression you can learn about in future books that may do
even better at predicting with such data.

How do these two models compare on the Sacramento house prices data set? In
{numref}`fig:08-compareRegression`, we also printed the RMSPE as calculated from
predicting on the test data set that was not used to train/fit the models. The RMSPE for the simple linear
regression model is slightly lower than the RMSPE for the K-NN regression model.
Considering that the simple linear regression model is also more interpretable,
if we were comparing these in practice we would likely choose to use the simple
linear regression model.

```{index} extrapolation
```

Finally, note that the K-NN regression model becomes "flat"
at the left and right boundaries of the data, while the linear model
predicts a constant slope. Predicting outside the range of the observed
data is known as *extrapolation*; K-NN and linear models behave quite differently
when extrapolating. Depending on the application, the flat
or constant slope trend may make more sense. For example, if our housing
data were slightly different, the linear model may have actually predicted
a *negative* price for a small house (if the intercept $\beta_0$ was negative),
which obviously does not match reality. On the other hand, the trend of increasing
house size corresponding to increasing house price probably continues for large houses,
so the "flat" extrapolation of K-NN likely does not match reality.

+++

## Multivariable linear regression

+++

```{index} regression; multivariable linear, regression; multivariable linear equation
```

```{index} see: multivariable linear equation; plane equation
```

As in K-NN classification and K-NN regression, we can move beyond the simple
case of only one predictor to the case with multiple predictors,
known as *multivariable linear regression*.
To do this, we follow a very similar approach to what we did for
K-NN regression: we just specify the training data by adding more predictors.
But recall that we do not need to use cross-validation to choose any parameters,
nor do we need to standardize (i.e., center and scale) the data for linear regression.
Note once again that we have the same concerns regarding multiple predictors
 as in the settings of multivariable K-NN regression and classification: having more predictors is **not** always
better. But because the same predictor selection
algorithm from {numref}`Chapter %s <classification2>` extends to the setting of linear regression,
it will not be covered again in this chapter.

```{index} Sacramento real estate
```

We will demonstrate multivariable linear regression using the Sacramento real estate
data with both house size
(measured in square feet) as well as number of bedrooms as our predictors, and
continue to use house sale price as our response variable.
The `scikit-learn` framework makes this easy to do: we just need to set
both the `sqft` and `beds` variables as predictors, and then use the `fit`
method as usual.

```{code-cell} ipython3

mlm = LinearRegression()
mlm.fit(
    sacramento_train[["sqft", "beds"]],
    sacramento_train["price"]
)
```
Finally, we make predictions on the test data set to assess the quality of our model.

```{index} scikit-learn;predict, scikit-learn;mean_squared_error
```
```{index} see: mean_squared_error;scikit-learn
```
```{index} see: predict;scikit-learn
```

```{code-cell} ipython3
sacramento_test["predicted"] = mlm.predict(sacramento_test[["sqft","beds"]])

lm_mult_test_RMSPE = mean_squared_error(
    y_true=sacramento_test["price"],
    y_pred=sacramento_test["predicted"]
)**(1/2)
lm_mult_test_RMSPE
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("sacr_mult_RMSPE", "{0:,.0f}".format(lm_mult_test_RMSPE))
```

Our model's test error as assessed by RMSPE
is \${glue:text}`sacr_mult_RMSPE`.
In the case of two predictors, we can plot the predictions made by our linear regression creates a *plane* of best fit, as
shown in {numref}`fig:08-3DlinReg`.

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
mlmPredGrid = mlm.predict(xygrid)

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
        z=mlmPredGrid.reshape(50, -1),
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
    glue("fig:08-3DlinReg", Image("img/regression2/plot3d_linear_regression.png"))
else:
    glue("fig:08-3DlinReg", fig)
```

```{figure} data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
:name: fig:08-3DlinReg
:figclass: caption-hack

Linear regression plane of best fit overlaid on top of the data (using price,
house size, and number of bedrooms as predictors). Note that in general we
recommend against using 3D visualizations; here we use a 3D visualization only
to illustrate what the regression plane looks like for learning purposes.
```

