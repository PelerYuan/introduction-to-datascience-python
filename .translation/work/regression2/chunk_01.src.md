
(regression2)=
# Regression II: linear regression

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
from IPython.display import HTML
from IPython.display import Image
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
```

## Overview
Up to this point, we have solved all of our predictive problems&mdash;both classification
and regression&mdash;using K-nearest neighbors (K-NN)-based approaches. In the context of regression,
there is another commonly used method known as *linear regression*. This chapter provides an introduction
to the basic concept of linear regression, shows how to use `scikit-learn` to perform linear regression in Python,
and characterizes its strengths and weaknesses compared to K-NN regression. The focus is, as usual,
on the case where there is a single predictor and single response variable of interest; but the chapter
concludes with an example using *multivariable linear regression* when there is more than one
predictor.

## Chapter learning objectives
By the end of the chapter, readers will be able to do the following:

- Use Python to fit simple and multivariable linear regression models on training data.
- Evaluate the linear regression model on test data.
- Compare and contrast predictions obtained from K-nearest neighbors regression to those obtained using linear regression from the same data set.
- Describe how linear regression is affected by outliers and multicollinearity.

+++

## Simple linear regression

```{index} regression; linear
```

At the end of the previous chapter, we noted some limitations of K-NN regression.
While the method is simple and easy to understand, K-NN regression does not
predict well beyond the range of the predictors in the training data, and
the method gets significantly slower as the training data set grows.
Fortunately, there is an alternative to K-NN regression&mdash;*linear regression*&mdash;that addresses
both of these limitations. Linear regression is also very commonly
used in practice because it provides an interpretable mathematical equation that describes
the relationship between the predictor and response variables. In this first part of the chapter, we will focus on *simple* linear regression,
which involves only one predictor variable and one response variable; later on, we will consider
 *multivariable* linear regression, which involves multiple predictor variables.
 Like K-NN regression, simple linear regression involves
predicting a numerical response variable (like race time, house price, or height);
but *how* it makes those predictions for a new observation is quite different from K-NN regression.
 Instead of looking at the K nearest neighbors and averaging
over their values for a prediction, in simple linear regression, we create a
straight line of best fit through the training data and then
"look up" the prediction using the line.

+++

```{index} regression; logistic
```

```{note}
Although we did not cover it in earlier chapters, there
is another popular method for classification called *logistic
regression* (it is used for classification even though the name, somewhat confusingly,
has the word "regression" in it). In logistic regression&mdash;similar to linear regression&mdash;you
"fit" the model to the training data and then "look up" the prediction for each new observation.
Logistic regression and K-NN classification have an advantage/disadvantage comparison
similar to that of linear regression and K-NN
regression. It is useful to have a good understanding of linear regression before learning about
logistic regression. After reading this chapter, see the "Additional Resources" section at the end of the
classification chapters to learn more about logistic regression.
```

+++

```{index} Sacramento real estate, question; regression
```

Let's return to the Sacramento housing data from {numref}`Chapter %s <regression1>` to learn
how to apply linear regression and compare it to K-NN regression. For now, we
will consider
a smaller version of the housing data to help make our visualizations clear.
Recall our predictive question: can we use the size of a house in the Sacramento, CA area to predict
its sale price? In particular, recall that we have come across a new 2,000 square-foot house we are interested
in purchasing with an advertised list price of
\$350,000. Should we offer the list price, or is that over/undervalued?
To answer this question using simple linear regression, we use the data we have
to draw the straight line of best fit through our existing data points.
The small subset of data as well as the line of best fit are shown
in {numref}`fig:08-lin-reg1`.

```{code-cell} ipython3
:tags: [remove-cell]

import pandas as pd

np.random.seed(2)

sacramento = pd.read_csv("data/sacramento.csv")

small_sacramento = sacramento.sample(n=30)

small_plot = (
    alt.Chart(small_sacramento)
    .mark_circle(opacity=1)
    .encode(
        x=alt.X("sqft")
            .scale(zero=False)
            .title("House size (square feet)"),
        y=alt.Y("price")
            .axis(format="$,.0f")
            .scale(zero=False)
            .title("Price (USD)"),
    )
)


# create df_lines with one fake/empty line (for starting at 2nd color later)
df_lines = {"x": [500, 500], "y": [100000, 100000], "number": ["-1", "-1"]}

# set the domains (range of x values) of lines
min_x = small_sacramento["sqft"].min()
max_x = small_sacramento["sqft"].max()

# add the line of best fit
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(small_sacramento[["sqft"]], small_sacramento[["price"]])
pred_min = float(lm.predict(pd.DataFrame({"sqft": [min_x]})))
pred_max = float(lm.predict(pd.DataFrame({"sqft": [max_x]})))

df_lines["x"].extend([min_x, max_x])
df_lines["y"].extend([pred_min, pred_max])
df_lines["number"].extend(["0", "0"])

# add other similar looking lines
intercept_l = [-64542.23, -6900, -64542.23]
slope_l = [190, 175, 160]
for i in range(len(slope_l)):
    df_lines["x"].extend([min_x, max_x])
    df_lines["y"].extend([
                        intercept_l[i] + slope_l[i] * min_x,
                        intercept_l[i] + slope_l[i] * max_x,
                    ])
    df_lines["number"].extend([f"{i+1}", f"{i+1}"])

df_lines = pd.DataFrame(df_lines)

# plot the bogus line to skip the same color as the scatter
small_plot += alt.Chart(
    df_lines[df_lines["number"] == "-1"]
).mark_line().encode(
    x="x", y="y", color=alt.Color("number", legend=None)
)
# plot the real line with 2nd color
small_plot += alt.Chart(
    df_lines[df_lines["number"] == "0"]
).mark_line().encode(
    x="x", y="y", color=alt.Color("number", legend=None)
)

small_plot
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("fig:08-lin-reg1", small_plot)
```

:::{glue:figure} fig:08-lin-reg1
:name: fig:08-lin-reg1

Scatter plot of sale price versus size with line of best fit for subset of the Sacramento housing data.
:::

+++

```{index} straight line; equation
```

```{index} see: line; straight line
```

The equation for the straight line is:

$$\text{house sale price} = \beta_0 + \beta_1 \cdot (\text{house size}),$$
where

- $\beta_0$ is the *vertical intercept* of the line (the price when house size is 0)
- $\beta_1$ is the *slope* of the line (how quickly the price increases as you increase house size)

Therefore using the data to find the line of best fit is equivalent to finding coefficients
$\beta_0$ and $\beta_1$ that *parametrize* (correspond to) the line of best fit.
Now of course, in this particular problem, the idea of a 0 square-foot house is a bit silly;
but you can think of $\beta_0$ here as the "base price," and
$\beta_1$ as the increase in price for each square foot of space.
Let's push this thought even further: what would happen in the equation for the line if you
tried to evaluate the price of a house with size 6 *million* square feet?
Or what about *negative* 2,000 square feet? As it turns out, nothing in the formula breaks; linear
regression will happily make predictions for crazy predictor values if you ask it to. But even though
you *can* make these wild predictions, you shouldn't. You should only make predictions roughly within
the range of your original data, and perhaps a bit beyond it only if it makes sense. For example,
the data in {numref}`fig:08-lin-reg1` only reaches around 600 square feet on the low end, but
it would probably be reasonable to use the linear regression model to make a prediction at 500 square feet, say.

Back to the example! Once we have the coefficients $\beta_0$ and $\beta_1$, we can use the equation
above to evaluate the predicted sale price given the value we have for the
predictor variable&mdash;here 2,000 square feet. {numref}`fig:08-lin-reg2` demonstrates this process.

```{code-cell} ipython3
:tags: [remove-cell]
from sklearn.linear_model import LinearRegression

lm = LinearRegression()
lm.fit(small_sacramento[["sqft"]], small_sacramento[["price"]])
prediction = float(lm.predict(pd.DataFrame({"sqft": [2000]})))

# the vertical dotted line
line_df = pd.DataFrame({"x": [2000]})
rule = alt.Chart(line_df).mark_rule(strokeDash=[6], size=1.5).encode(x="x")

# the red point
point_df = pd.DataFrame({"x": [2000], "y": [prediction]})
point = alt.Chart(point_df).mark_circle(color="red", size=80, opacity=1).encode(x="x", y="y")

# overlay all plots
small_plot_2000_pred = (
    small_plot
    + rule
    + point
    # add the text
    + alt.Chart(
        pd.DataFrame(
            {
                "x": [2450],
                "y": [prediction - 41000],
                "prediction": ["$" + "{0:,.0f}".format(prediction)],
            }
        )
    )
    .mark_text(dy=-5, size=15)
    .encode(x="x", y="y", text="prediction")
)

small_plot_2000_pred
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-lin-reg2", small_plot_2000_pred)
glue("pred_2000", "{0:,.0f}".format(prediction))
```

:::{glue:figure} fig:08-lin-reg2
:name: fig:08-lin-reg2

Scatter plot of sale price versus size with line of best fit and a red dot at the predicted sale price for a 2,000 square-foot home.
:::

+++

By using simple linear regression on this small data set to predict the sale price
for a 2,000 square-foot house, we get a predicted value of
\${glue:text}`pred_2000`. But wait a minute...how
exactly does simple linear regression choose the line of best fit? Many
different lines could be drawn through the data points.
Some plausible examples are shown in {numref}`fig:08-several-lines`.

```{code-cell} ipython3
:tags: [remove-cell]

several_lines_plot = small_plot.copy()

several_lines_plot += alt.Chart(
    df_lines[df_lines["number"] != "0"]
).mark_line().encode(x="x", y="y", color=alt.Color("number",legend=None))

several_lines_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-several-lines", several_lines_plot)
```

:::{glue:figure} fig:08-several-lines
:name: fig:08-several-lines

Scatter plot of sale price versus size with many possible lines that could be drawn through the data points.
:::

+++

```{index} RMSPE
```

Simple linear regression chooses the straight line of best fit by choosing
the line that minimizes the **average squared vertical distance** between itself and
each of the observed data points in the training data (equivalent to minimizing the RMSE). {numref}`fig:08-verticalDistToMin` illustrates
these vertical distances as lines. Finally, to assess the predictive
accuracy of a simple linear regression model,
we use RMSPE&mdash;the same measure of predictive performance we used with K-NN regression.

```{code-cell} ipython3
:tags: [remove-cell]

small_sacramento_pred = small_sacramento
# get prediction
small_sacramento_pred = small_sacramento_pred.assign(
    predicted=lm.predict(small_sacramento[["sqft"]])
)
# melt the dataframe to create separate df to create lines
small_sacramento_pred = small_sacramento_pred[["sqft", "price", "predicted"]].melt(
    id_vars=["sqft"]
)

v_lines = []
for i in range(len(small_sacramento)):
    sqft_val = small_sacramento.iloc[i]["sqft"]
    line_df = small_sacramento_pred.query("sqft == @sqft_val")
    v_lines.append(alt.Chart(line_df).mark_line(color="black").encode(x="sqft", y="value"))

error_plot = alt.layer(*v_lines, small_plot).configure_circle(opacity=1)
error_plot
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:08-verticalDistToMin", error_plot)
```

:::{glue:figure} fig:08-verticalDistToMin
:name: fig:08-verticalDistToMin

Scatter plot of sale price versus size with lines denoting the vertical distances between the predicted values and the observed data points.
:::

+++

## Linear regression in Python

+++

```{index} scikit-learn
```

We can perform simple linear regression in Python using `scikit-learn` in a
very similar manner to how we performed K-NN regression.
To do this, instead of creating a `KNeighborsRegressor` model object,
we use a `LinearRegression` model object;
and as usual, we first have to import it from `sklearn`.
Another difference is that we do not need to choose $K$ in the
context of linear regression, and so we do not need to perform cross-validation.
Below we illustrate how we can use the usual `scikit-learn` workflow to predict house sale
price given house size. We use a simple linear regression approach on the full
Sacramento real estate data set.

```{index} seed; numpy.random.seed
```

As usual, we start by loading packages, setting the seed, loading data, and
putting some test data away in a lock box that we
can come back to after we choose our final model. Let's take care of that now.

```{code-cell} ipython3
import numpy as np
import altair as alt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")

np.random.seed(1)

sacramento = pd.read_csv("data/sacramento.csv")

sacramento_train, sacramento_test = train_test_split(
    sacramento, train_size=0.75
)
```

Now that we have our training data, we will create
and fit the linear regression model object.
We will also extract the slope of the line
via the `coef_[0]` property, as well as the
intercept of the line via the `intercept_` property.

```{index} scikit-learn; fit
```

```{code-cell} ipython3
# fit the linear regression model
lm = LinearRegression()
lm.fit(
   sacramento_train[["sqft"]],  # A single-column data frame
   sacramento_train["price"]  # A series
)

# make a dataframe containing slope and intercept coefficients
pd.DataFrame({"slope": [lm.coef_[0]], "intercept": [lm.intercept_]})
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("train_lm_slope", "{:0.0f}".format(lm.coef_[0]))
glue("train_lm_intercept", "{:0.0f}".format(lm.intercept_))
glue("train_lm_slope_f", "{0:,.0f}".format(lm.coef_[0]))
glue("train_lm_intercept_f", "{0:,.0f}".format(lm.intercept_))
```

```{index} standardization
```

```{note}
An additional difference that you will notice here is that we do
not standardize (i.e., scale and center) our
predictors. In K-nearest neighbors models, recall that the model fit changes
depending on whether we standardize first or not. In linear regression,
standardization does not affect the fit (it *does* affect the coefficients in
the equation, though!).  So you can standardize if you want&mdash;it won't
hurt anything&mdash;but if you leave the predictors in their original form,
the best fit coefficients are usually easier to interpret afterward.
```

