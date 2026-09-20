+++

We see that the predictions from linear regression with two predictors form a
flat plane. This is the hallmark of linear regression, and differs from the
wiggly, flexible surface we get from other methods such as K-NN regression.
 As discussed, this can be advantageous in one aspect, which is that for each
predictor, we can get slopes/intercept from linear regression, and thus describe the
plane mathematically. We can extract those slope values from the `coef_` property
of our model object, and the intercept from the `intercept_` property,
as shown below.

```{code-cell} ipython3
mlm.coef_
```

```{code-cell} ipython3
mlm.intercept_
```

When we have multiple predictor variables, it is not easy to
know which variable goes with which coefficient in `mlm.coef_`. In particular,
you will see that `mlm.coef_` above is just an array of values without any variable names.
Unfortunately you have to do this mapping yourself: the coefficients in `mlm.coef_` appear
in the *same order* as the columns of the predictor data frame you used when training.
So since we used `sacramento_train[["sqft", "beds"]]` when training,
we have that `mlm.coef_[0]` corresponds to `sqft`, and `mlm.coef_[1]` corresponds to `beds`.
Once you sort out the correspondence, you can then use those slopes to write a mathematical equation to describe the prediction plane:

```{index} plane equation
```



$$\text{house sale price} = \beta_0 + \beta_1\cdot(\text{house size}) + \beta_2\cdot(\text{number of bedrooms}),$$
where:

- $\beta_0$ is the *vertical intercept* of the hyperplane (the price when both house size and number of bedrooms are 0)
- $\beta_1$ is the *slope* for the first predictor (how quickly the price increases as you increase house size)
- $\beta_2$ is the *slope* for the second predictor (how quickly the price increases as you increase the number of bedrooms)

Finally, we can fill in the values for $\beta_0$, $\beta_1$ and $\beta_2$ from the model output above
to create the equation of the plane of best fit to the data:

```{code-cell} ipython3
:tags: [remove-cell]

icept = "{0:,.0f}".format(mlm.intercept_)
sqftc = "{0:,.0f}".format(mlm.coef_[0])
bedsc = "{0:,.0f}".format(mlm.coef_[1])
glue("icept", icept)
glue("sqftc", sqftc)
glue("bedsc", bedsc)
```

$\text{house sale price} =$ {glue:text}`icept` $+$ {glue:text}`sqftc` $\cdot (\text{house size})$ {glue:text}`bedsc` $\cdot (\text{number of bedrooms})$

This model is more interpretable than the multivariable K-NN
regression model; we can write a mathematical equation that explains how
each predictor is affecting the predictions. But as always, we should
question how well multivariable linear regression is doing compared to
the other tools we have, such as simple linear regression
and multivariable K-NN regression. If this comparison is part of
the model tuning process&mdash;for example, if we are trying
 out many different sets of predictors for multivariable linear
and K-NN regression&mdash;we must perform this comparison using
cross-validation on only our training data. But if we have already
decided on a small number (e.g., 2 or 3) of tuned candidate models and
we want to make a final comparison, we can do so by comparing the prediction
error of the methods on the test data.

```{code-cell} ipython3
lm_mult_test_RMSPE
```

```{index} RMSPE
```

We obtain an RMSPE for the multivariable linear regression model
of \${glue:text}`sacr_mult_RMSPE`. This prediction error
 is less than the prediction error for the multivariable K-NN regression model,
indicating that we should likely choose linear regression for predictions of
house sale price on this data set. Revisiting the simple linear regression model
with only a single predictor from earlier in this chapter, we see that the RMSPE for that model was
\${glue:text}`sacr_RMSPE`,
which is slightly higher than that of our more complex model. Our model with two predictors
provided a slightly better fit on test data than our model with just one.
As mentioned earlier, this is not always the case: sometimes including more
predictors can negatively impact the prediction performance on unseen
test data.

+++

## Multicollinearity and outliers

What can go wrong when performing (possibly multivariable) linear regression?
This section will introduce two common issues&mdash;*outliers* and *collinear predictors*&mdash;and
illustrate their impact on predictions.

+++

### Outliers

```{index} outliers
```

Outliers are data points that do not follow the usual pattern of the rest of the data.
In the setting of linear regression, these are points that
 have a vertical distance to the line of best fit that is either much higher or much lower
than you might expect based on the rest of the data. The problem with outliers is that
they can have *too much influence* on the line of best fit. In general, it is very difficult
to judge accurately which data are outliers without advanced techniques that are beyond
the scope of this book.

But to illustrate what can happen when you have outliers, {numref}`fig:08-lm-outlier`
shows a small subset of the Sacramento housing data again, except we have added a *single* data point (highlighted
in red). This house is 5,000 square feet in size, and sold for only \$50,000. Unbeknownst to the
data analyst, this house was sold by a parent to their child for an absurdly low price. Of course,
this is not representative of the real housing market values that the other data points follow;
the data point is an *outlier*. In orange we plot the original line of best fit, and in red
we plot the new line of best fit including the outlier. You can see how different the red line
is from the orange line, which is entirely caused by that one extra outlier data point.

```{code-cell} ipython3
:tags: [remove-cell]

sacramento_train_small = sacramento_train.sample(100, random_state=2)
sacramento_outlier = pd.DataFrame({"sqft": [5000], "price": [50000]})
sacramento_concat_df = pd.concat((sacramento_train_small, sacramento_outlier))

lm_plot_outlier = (
    alt.Chart(sacramento_train_small)
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
lm_plot_outlier += lm_plot_outlier.transform_regression("sqft", "price").mark_line(
    color="#ff7f0e"
)

outlier_pt = (
    alt.Chart(sacramento_outlier)
    .mark_circle(color="#d62728", size=100)
    .encode(x="sqft", y="price")
)

outlier_line = (
    (
        alt.Chart(sacramento_concat_df)
        .mark_circle()
        .encode(
            x=alt.X(
                "sqft", title="House size (square feet)", scale=alt.Scale(zero=False)
            ),
            y=alt.Y(
                "price",
                title="Price (USD)",
                axis=alt.Axis(format="$,.0f"),
                scale=alt.Scale(zero=False),
            ),
        )
    )
    .transform_regression("sqft", "price")
    .mark_line(color="#d62728")
)

lm_plot_outlier += outlier_pt + outlier_line

glue("fig:08-lm-outlier", lm_plot_outlier)
```

:::{glue:figure} fig:08-lm-outlier
:name: fig:08-lm-outlier

Scatter plot of a subset of the data, with outlier highlighted in red.
:::

+++

Fortunately, if you have enough data, the inclusion of one or two
outliers&mdash;as long as their values are not *too* wild&mdash;will
typically not have a large effect on the line of best fit. {numref}`fig:08-lm-outlier-2` shows how that same outlier data point from earlier
influences the line of best fit when we are working with the entire original
Sacramento training data. You can see that with this larger data set, the line
changes much less when adding the outlier.
Nevertheless, it is still important when working with linear regression to critically
think about how much any individual data point is influencing the model.

```{code-cell} ipython3
:tags: [remove-cell]

sacramento_concat_df = pd.concat((sacramento_train, sacramento_outlier))

lm_plot_outlier_large = (
    alt.Chart(sacramento_train)
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
lm_plot_outlier_large += lm_plot_outlier_large.transform_regression(
    "sqft", "price"
).mark_line(color="#ff7f0e")

outlier_line = (
    (
        alt.Chart(sacramento_concat_df)
        .mark_circle()
        .encode(
            x=alt.X(
                "sqft", title="House size (square feet)", scale=alt.Scale(zero=False)
            ),
            y=alt.Y(
                "price",
                title="Price (USD)",
                axis=alt.Axis(format="$,.0f"),
                scale=alt.Scale(zero=False),
            ),
        )
    )
    .transform_regression("sqft", "price")
    .mark_line(color="#d62728")
)

lm_plot_outlier_large += outlier_pt + outlier_line

glue("fig:08-lm-outlier-2", lm_plot_outlier_large)
```

:::{glue:figure} fig:08-lm-outlier-2
:name: fig:08-lm-outlier-2

Scatter plot of the full data, with outlier highlighted in red.
:::

+++

### Multicollinearity

```{index} multicollinearity
```

The second, and much more subtle, issue can occur when performing multivariable
linear regression.  In particular, if you include multiple predictors that are
strongly linearly related to one another, the coefficients that describe the
plane of best fit can be very unreliable&mdash;small changes to the data can
result in large changes in the coefficients. Consider an extreme example using
the Sacramento housing data where the house was measured twice by two people.
Since the two people are each slightly inaccurate, the two measurements might
not agree exactly, but they are very strongly linearly related to each other,
as shown in {numref}`fig:08-lm-multicol`.

```{code-cell} ipython3
:tags: [remove-cell]

np.random.seed(1)
sacramento_train = sacramento_train.assign(
    sqft1=sacramento_train["sqft"]
    + 100
    * np.random.choice(range(1000000), size=len(sacramento_train), replace=True)
    / 1000000
)
sacramento_train = sacramento_train.assign(
    sqft2=sacramento_train["sqft"]
    + 100
    * np.random.choice(range(1000000), size=len(sacramento_train), replace=True)
    / 1000000
)
sacramento_train = sacramento_train.assign(
    sqft3=sacramento_train["sqft"]
    + 100
    * np.random.choice(range(1000000), size=len(sacramento_train), replace=True)
    / 1000000
)
sacramento_train

lm_plot_multicol_1 = (
    alt.Chart(sacramento_train)
    .mark_circle()
    .encode(
        x=alt.X("sqft", title="House size measurement 1 (square feet)"),
        y=alt.Y("sqft1", title="House size measurement 2 (square feet)"),
    )
)

glue("fig:08-lm-multicol", lm_plot_multicol_1)
```

:::{glue:figure} fig:08-lm-multicol
:name: fig:08-lm-multicol

Scatter plot of house size (in square feet) measured by person 1 versus house size (in square feet) measured by person 2.
:::

```{code-cell} ipython3
:tags: [remove-cell]

# first LM
lm_fit1 = LinearRegression()
X_train = sacramento_train[["sqft", "sqft1"]]
y_train = sacramento_train[["price"]]

lm_fit1.fit(X_train, y_train)

icept1 = "{0:,.0f}".format(lm_fit1.intercept_[0])
sqft1 = "{0:,.0f}".format(lm_fit1.coef_[0][0])
sqft11 = "{0:,.0f}".format(lm_fit1.coef_[0][1])
glue("icept1", icept1)
glue("sqft1", sqft1)
glue("sqft11", sqft11)

# second LM
lm_fit2 = LinearRegression()
X_train = sacramento_train[["sqft", "sqft2"]]
y_train = sacramento_train[["price"]]

lm_fit2.fit(X_train, y_train)

icept2 = "{0:,.0f}".format(lm_fit2.intercept_[0])
sqft2 = "{0:,.0f}".format(lm_fit2.coef_[0][0])
sqft22 = "{0:,.0f}".format(lm_fit2.coef_[0][1])
glue("icept2", icept2)
glue("sqft2", sqft2)
glue("sqft22", sqft22)

# third LM
lm_fit3 = LinearRegression()
X_train = sacramento_train[["sqft", "sqft3"]]
y_train = sacramento_train[["price"]]

lm_fit3.fit(X_train, y_train)

icept3 = "{0:,.0f}".format(lm_fit3.intercept_[0])
sqft3 = "{0:,.0f}".format(lm_fit3.coef_[0][0])
sqft33 = "{0:,.0f}".format(lm_fit3.coef_[0][1])
glue("icept3", icept3)
glue("sqft3", sqft3)
glue("sqft33", sqft33)
```

 If we again fit the multivariable linear regression model on this data, then the plane of best fit
has regression coefficients that are very sensitive to the exact values in the data. For example,
if we change the data ever so slightly&mdash;e.g., by running cross-validation, which splits
up the data randomly into different chunks&mdash;the coefficients vary by large amounts:

Best Fit 1: $\text{house sale price} =$ {glue:text}`icept1` $+$ {glue:text}`sqft1` $\cdot (\text{house size 1}$ $(\text{ft}^2)) +$ {glue:text}`sqft11` $\cdot (\text{house size 2}$ $(\text{ft}^2)).$

Best Fit 2: $\text{house sale price} =$ {glue:text}`icept2` $+$ {glue:text}`sqft2` $\cdot (\text{house size 1}$ $(\text{ft}^2)) +$ {glue:text}`sqft22` $\cdot (\text{house size 2}$ $(\text{ft}^2)).$

Best Fit 3: $\text{house sale price} =$ {glue:text}`icept3` $+$ {glue:text}`sqft3` $\cdot (\text{house size 1}$ $(\text{ft}^2)) +$ {glue:text}`sqft33` $\cdot (\text{house size 2}$ $(\text{ft}^2)).$

 Therefore, when performing multivariable linear regression, it is important to avoid including very
linearly related predictors. However, techniques for doing so are beyond the scope of this
book; see the list of additional resources at the end of this chapter to find out where you can learn more.

+++

## Designing new predictors

We were quite fortunate in our initial exploration to find a predictor variable (house size)
that seems to have a meaningful and nearly linear relationship with our response variable (sale price).
But what should we do if we cannot immediately find such a nice variable?
Well, sometimes it is just a fact that the variables in the data do not have enough of
a relationship with the response variable to provide useful predictions. For example,
if the only available predictor was "the current house owner's favorite ice cream flavor",
we likely would have little hope of using that variable to predict the house's sale price
(barring any future remarkable scientific discoveries about the relationship between
the housing market and homeowner ice cream preferences). In cases like these,
the only option is to obtain measurements of more useful variables.

There are, however, a wide variety of cases where the predictor variables do have a
meaningful relationship with the response variable, but that relationship does not fit
the assumptions of the regression method you have chosen. For example, a data frame `df`
with two variables&mdash;`x` and `y`&mdash;with a nonlinear relationship between the two variables
will not be fully captured by simple linear regression, as shown in {numref}`fig:08-predictor-design`.

```{code-cell} ipython3
:tags: [remove-cell]

np.random.seed(3)
df = pd.DataFrame({"x": np.random.choice(range(10000), size=100, replace=True) / 10000})
df = df.assign(
    y=df["x"] ** 3
    + 0.2 * np.random.choice(range(10000), size=100, replace=True) / 10000
    - 0.1
)
```

```{code-cell} ipython3
df
```

```{code-cell} ipython3
:tags: [remove-cell]

curve_plt = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x=alt.X("x", scale=alt.Scale(zero=False)),
        y=alt.Y(
            "y",
            scale=alt.Scale(zero=False),
        ),
    )
)


curve_plt += curve_plt.transform_regression("x", "y").mark_line(color="#ff7f0e")

glue("fig:08-predictor-design", curve_plt)
```

:::{glue:figure} fig:08-predictor-design
:name: fig:08-predictor-design

Example of a data set with a nonlinear relationship between the predictor and the response.
:::

+++

```{index} predictor design
```

Instead of trying to predict the response `y` using a linear regression on `x`,
we might have some scientific background about our problem to suggest that `y`
should be a cubic function of `x`. So before performing regression,
we might *create a new predictor variable* `z`:

```{code-cell} ipython3
df["z"] = df["x"] ** 3
```

Then we can perform linear regression for `y` using the predictor variable `z`,
as shown in {numref}`fig:08-predictor-design-2`.
Here you can see that the transformed predictor `z` helps the
linear regression model make more accurate predictions.
Note that none of the `y` response values have changed between {numref}`fig:08-predictor-design`
and {numref}`fig:08-predictor-design-2`; the only change is that the `x` values
have been replaced by `z` values.

```{code-cell} ipython3
:tags: [remove-cell]

curve_plt2 = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x=alt.X("z", title="z = x³" ,scale=alt.Scale(zero=False)),
        y=alt.Y(
            "y",
            scale=alt.Scale(zero=False),
        ),
    )
)


curve_plt2 += curve_plt2.transform_regression("z", "y").mark_line(color="#ff7f0e")

glue("fig:08-predictor-design-2", curve_plt2)
```

:::{glue:figure} fig:08-predictor-design-2
:name: fig:08-predictor-design-2

Relationship between the transformed predictor and the response.
:::

