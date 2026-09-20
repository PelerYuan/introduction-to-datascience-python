
(regression1)=
# Regression I: K-nearest neighbors

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
from IPython.display import HTML
from IPython.display import Image
import plotly.express as px
import plotly.graph_objects as go
```

## Overview

This chapter continues our foray into answering predictive questions.
Here we will focus on predicting *numerical* variables
and will use *regression* to perform this task.
This is unlike the past two chapters, which focused on predicting categorical
variables via classification. However, regression does have many similarities
to classification: for example, just as in the case of classification,
we will split our data into training, validation, and test sets, we will
use `scikit-learn` workflows, we will use a K-nearest neighbors (K-NN)
approach to make predictions, and we will use cross-validation to choose K.
Because of how similar these procedures are, make sure to read
{numref}`Chapters %s <classification1>` and {numref}`%s <classification2>` before reading
this one&mdash;we will move a little bit faster here with the
concepts that have already been covered.
This chapter will primarily focus on the case where there is a single predictor,
but the end of the chapter shows how to perform
regression with more than one predictor variable, i.e., *multivariable regression*.
It is important to note that regression
can also be used to answer inferential and causal questions,
however that is beyond the scope of this book.

+++

## Chapter learning objectives
By the end of the chapter, readers will be able to do the following:

- Recognize situations where a regression analysis would be appropriate for making predictions.
- Explain the K-nearest neighbors (K-NN) regression algorithm and describe how it differs from K-NN classification.
- Interpret the output of a K-NN regression.
- In a data set with two or more variables, perform K-nearest neighbors regression in Python.
- Evaluate K-NN regression prediction quality in Python using the root mean squared prediction error (RMSPE).
- Estimate the RMSPE in Python using cross-validation or a test set.
- Choose the number of neighbors in K-nearest neighbors regression by minimizing estimated cross-validation RMSPE.
- Describe underfitting and overfitting, and relate it to the number of neighbors in K-nearest neighbors regression.
- Describe the advantages and disadvantages of K-nearest neighbors regression.

+++

## The regression problem

```{index} predictive question, response variable
```

Regression, like classification, is a predictive problem setting where we want
to use past information to predict future observations. But in the case of
regression, the goal is to predict *numerical* values instead of *categorical* values.
The variable that you want to predict is often called the *response variable*.
For example, we could try to use the number of hours a person spends on
exercise each week to predict their race time in the annual Boston marathon. As
another example, we could try to use the size of a house to
predict its sale price. Both of these response variables&mdash;race time and sale price&mdash;are
numerical, and so predicting them given past data is considered a regression problem.

```{index} classification; comparison to regression
```

```{index} regression; comparison to classification
```

Just like in the classification setting, there are many possible methods that we can use
to predict numerical response variables. In this chapter we will
focus on the **K-nearest neighbors** algorithm {cite:p}`knnfix,knncover`, and in the next chapter
we will study **linear regression**.
In your future studies, you might encounter regression trees, splines,
and general local regression methods; see the additional resources
section at the end of the next chapter for where to begin learning more about
these other methods.

Many of the concepts from classification map over to the setting of regression. For example,
a regression model predicts a new observation's response variable based on the response variables
for similar observations in the data set of past observations. When building a regression model,
we first split the data into training and test sets, in order to ensure that we assess the performance
of our method on observations not seen during training. And finally, we can use cross-validation to evaluate different
choices of model parameters (e.g., K in a K-nearest neighbors model). The major difference
is that we are now predicting numerical variables instead of categorical variables.

```{index} categorical variable, numerical variable
```

```{note}
You can usually tell whether a variable is numerical or
categorical&mdash;and therefore whether you need to perform regression or
classification&mdash;by taking the response variable for two observations X and Y from your data,
and asking the question, "is response variable X *more* than response
variable Y?" If the variable is categorical, the question will make no sense.
(Is blue more than red?  Is benign more than malignant?) If the variable is
numerical, it will make sense. (Is 1.5 hours more than 2.25 hours? Is
\$500,000 more than \$400,000?) Be careful when applying this heuristic,
though: sometimes categorical variables will be encoded as numbers in your
data (e.g., "1" represents "benign", and "0" represents "malignant"). In
these cases you have to ask the question about the *meaning* of the labels
("benign" and "malignant"), not their values ("1" and "0").
```

+++

## Exploring a data set

```{index} Sacramento real estate, question; regression
```

In this chapter and the next, we will study
a data set of
[932 real estate transactions in Sacramento, California](https://support.spatialkey.com/spatialkey-sample-csv-data/)
originally reported in the *Sacramento Bee* newspaper.
We first need to formulate a precise question that
we want to answer. In this example, our question is again predictive:
Can we use the size of a house in the Sacramento, CA area to predict
its sale price? A rigorous, quantitative answer to this question might help
a realtor advise a client as to whether the price of a particular listing
is fair, or perhaps how to set the price of a new listing.
We begin the analysis by loading and examining the data,
as well as setting the seed value.

```{index} seed;numpy.random.seed
```

```{code-cell} ipython3
import altair as alt
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")

np.random.seed(10)

sacramento = pd.read_csv("data/sacramento.csv")
sacramento
```

```{index} altair; mark_circle, visualization; scatter
```

The scientific question guides our initial exploration: the columns in the
data that we are interested in are `sqft` (house size, in livable square feet)
and `price` (house sale price, in US dollars (USD)).  The first step is to visualize
the data as a scatter plot where we place the predictor variable
(house size) on the x-axis, and we place the response variable that we
want to predict (sale price) on the y-axis.

```{note}
Given that the y-axis unit is dollars in {numref}`fig:07-edaRegr`,
we format the axis labels to put dollar signs in front of the house prices,
as well as commas to increase the readability of the larger numbers.
We can do this in `altair` by using `.axis(format="$,.0f")` on
the `y` encoding channel.
```

```{code-cell} ipython3
:tags: [remove-output]

scatter = alt.Chart(sacramento).mark_circle().encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .title("Price (USD)")
)

scatter
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("fig:07-edaRegr", scatter)
```

:::{glue:figure} fig:07-edaRegr
:name: fig:07-edaRegr

Scatter plot of price (USD) versus house size (square feet).
:::

+++

The plot is shown in {numref}`fig:07-edaRegr`.
We can see that in Sacramento, CA, as the
size of a house increases, so does its sale price. Thus, we can reason that we
may be able to use the size of a not-yet-sold house (for which we don't know
the sale price) to predict its final sale price. Note that we do not suggest here
that a larger house size *causes* a higher sale price; just that house price
tends to increase with house size, and that we may be able to use the latter to
predict the former.

+++

## K-nearest neighbors regression

```{index} K-nearest neighbors, K-nearest neighbors; regression
```

Much like in the case of classification,
we can use a K-nearest neighbors-based
approach in regression to make predictions.
Let's take a small sample of the data in {numref}`fig:07-edaRegr`
and walk through how K-nearest neighbors (K-NN) works
in a regression context before we dive in to creating our model and assessing
how well it predicts house sale price. This subsample is taken to allow us to
illustrate the mechanics of K-NN regression with a few data points; later in
this chapter we will use all the data.

```{index} DataFrame; sample
```

To take a small random sample of size 30, we'll use the
`sample` method on the `sacramento` data frame, specifying
that we want to select `n=30` rows.

```{code-cell} ipython3
small_sacramento = sacramento.sample(n=30)
```

Next let's say we come across a  2,000 square-foot house in Sacramento we are
interested in purchasing, with an advertised list price of \$350,000. Should we
offer to pay the asking price for this house, or is it overpriced and we should
offer less? Absent any other information, we can get a sense for a good answer
to this question by using the data we have to predict the sale price given the
sale prices we have already observed. But in {numref}`fig:07-small-eda-regr`,
you can see that we have no
observations of a house of size *exactly* 2,000 square feet. How can we predict
the sale price?

```{code-cell} ipython3
:tags: [remove-output]

small_plot = alt.Chart(small_sacramento).mark_circle(opacity=1).encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .title("Price (USD)")
)

# add an overlay to the base plot
line_df = pd.DataFrame({"x": [2000]})
rule = alt.Chart(line_df).mark_rule(strokeDash=[6], size=1.5, color="black").encode(x="x")

small_plot + rule
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-small-eda-regr", (small_plot + rule))
```

:::{glue:figure} fig:07-small-eda-regr
:name: fig:07-small-eda-regr

Scatter plot of price (USD) versus house size (square feet) with vertical line indicating 2,000 square feet on x-axis.
:::

+++

```{index} DataFrame; abs, DataFrame; nsmallest
```

We will employ the same intuition from {numref}`Chapters %s <classification1>` and {numref}`%s <classification2>`, and use the
neighboring points to the new point of interest to suggest/predict what its
sale price might be.
For the example shown in {numref}`fig:07-small-eda-regr`,
we find and label the 5 nearest neighbors to our observation
of a house that is 2,000 square feet.

```{code-cell} ipython3
small_sacramento["dist"] = (2000 - small_sacramento["sqft"]).abs()
nearest_neighbors = small_sacramento.nsmallest(5, "dist")
nearest_neighbors
```

```{code-cell} ipython3
:tags: [remove-cell]

nn_plot = small_plot + rule

# plot horizontal lines which is perpendicular to x=2000
h_lines = []
for i in range(5):
    h_line_df = pd.DataFrame({
        "sqft": [nearest_neighbors.iloc[i, 4], 2000],
        "price": [nearest_neighbors.iloc[i, 6]] * 2
    })
    h_lines.append(alt.Chart(h_line_df).mark_line(color="black").encode(x="sqft", y="price"))

# highlight the nearest neighbors in orange
orange_neighbrs = alt.Chart(nearest_neighbors).mark_circle(opacity=1, color="#ff7f0e").encode(
    x=alt.X("sqft")
        .scale(zero=False)
        .title("House size (square feet)"),
    y=alt.Y("price")
        .axis(format="$,.0f")
        .title("Price (USD)")
)

nn_plot = alt.layer(*h_lines, small_plot, orange_neighbrs, rule)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:07-knn5-example", nn_plot)
```

:::{glue:figure} fig:07-knn5-example
:name: fig:07-knn5-example

Scatter plot of price (USD) versus house size (square feet) with lines to 5 nearest neighbors (highlighted in orange).
:::

+++

{numref}`fig:07-knn5-example` illustrates the difference between the house sizes
of the 5 nearest neighbors (in terms of house size) to our new
2,000 square-foot house of interest. Now that we have obtained these nearest neighbors,
we can use their values to predict the
sale price for the new home.  Specifically, we can take the mean (or
average) of these 5 values as our predicted value, as illustrated by
the red point in {numref}`fig:07-predictedViz-knn`.

```{code-cell} ipython3
prediction = nearest_neighbors["price"].mean()
prediction
```

```{code-cell} ipython3
:tags: [remove-cell]

nn_plot_pred = nn_plot + alt.Chart(
    pd.DataFrame({"sqft": [2000], "price": [prediction]})
).mark_circle(size=80, opacity=1, color="#d62728").encode(x="sqft", y="price")
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("knn-5-pred", "{0:,.0f}".format(prediction))
glue("fig:07-predictedViz-knn", nn_plot_pred)
```

:::{glue:figure} fig:07-predictedViz-knn
:name: fig:07-predictedViz-knn

Scatter plot of price (USD) versus house size (square feet) with predicted price for a 2,000 square-foot house based on 5 nearest neighbors represented as a red dot.
:::

+++

Our predicted price is \${glue:text}`knn-5-pred`
(shown as a red point in {numref}`fig:07-predictedViz-knn`), which is much less than \$350,000; perhaps we
might want to offer less than the list price at which the house is advertised.
But this is only the very beginning of the story. We still have all the same
unanswered questions here with K-NN regression that we had with K-NN
classification: which $K$ do we choose, and is our model any good at making
predictions? In the next few sections, we will address these questions in the
context of K-NN regression.

One strength of the K-NN regression algorithm
that we would like to draw attention to at this point
is its ability to work well with non-linear relationships
(i.e., if the relationship is not a straight line).
This stems from the use of nearest neighbors to predict values.
The algorithm really has very few assumptions
about what the data must look like for it to work.

+++

## Training, evaluating, and tuning the model

```{index} training set, test set
```

As usual, we must start by putting some test data away in a lock box
that we will come back to only after we choose our final model.
Let's take care of that now.
Note that for the remainder of the chapter
we'll be working with the entire Sacramento data set,
as opposed to the smaller sample of 30 points
that we used earlier in the chapter ({numref}`fig:07-small-eda-regr`).

