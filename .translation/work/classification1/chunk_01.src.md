
```{code-cell} ipython3
:tags: [remove-cell]
from chapter_preamble import *
from IPython.display import HTML
from IPython.display import Image
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
```

(classification1)=
# Classification I: training & predicting

## Overview
In previous chapters, we focused solely on descriptive and exploratory
data analysis questions.
This chapter and the next together serve as our first
foray into answering *predictive* questions about data. In particular, we will
focus on *classification*, i.e., using one or more
variables to predict the value of a categorical variable of interest. This chapter
will cover the basics of classification, how to preprocess data to make it
suitable for use in a classifier, and how to use our observed data to make
predictions. The next chapter will focus on how to evaluate how accurate the
predictions from our classifier are, as well as how to improve our classifier
(where possible) to maximize its accuracy.

## Chapter learning objectives

By the end of the chapter, readers will be able to do the following:

- Recognize situations where a classifier would be appropriate for making predictions.
- Describe what a training data set is and how it is used in classification.
- Interpret the output of a classifier.
- Compute, by hand, the straight-line (Euclidean) distance between points on a graph when there are two predictor variables.
- Explain the K-nearest neighbors classification algorithm.
- Perform K-nearest neighbors classification in Python using `scikit-learn`.
- Use methods from `scikit-learn` to center, scale, balance, and impute data as a preprocessing step.
- Combine preprocessing and model training into a `Pipeline` using `make_pipeline`.

+++

## The classification problem

```{index} predictive question, classification, class, categorical variable
```

```{index} see: feature ; predictor
```

In many situations, we want to make predictions based on the current situation
as well as past experiences. For instance, a doctor may want to diagnose a
patient as either diseased or healthy based on their symptoms and the doctor's
past experience with patients; an email provider might want to tag a given
email as "spam" or "not spam" based on the email's text and past email text data;
or a credit card company may want to predict whether a purchase is fraudulent based
on the current purchase item, amount, and location as well as past purchases.
These tasks are all examples of **classification**, i.e., predicting a
categorical class (sometimes called a *label*) for an observation given its
other variables (sometimes called *features*).

```{index} training set
```

Generally, a classifier assigns an observation without a known class (e.g., a new patient)
to a class (e.g., diseased or healthy) on the basis of how similar it is to other observations
for which we do know the class (e.g., previous patients with known diseases and
symptoms). These observations with known classes that we use as a basis for
prediction are called a **training set**; this name comes from the fact that
we use these data to train, or teach, our classifier. Once taught, we can use
the classifier to make predictions on new data for which we do not know the class.

```{index} K-nearest neighbors, classification; binary
```

There are many possible methods that we could use to predict
a categorical class/label for an observation. In this book, we will
focus on the widely used **K-nearest neighbors** algorithm {cite:p}`knnfix,knncover`.
In your future studies, you might encounter decision trees, support vector machines (SVMs),
logistic regression, neural networks, and more; see the additional resources
section at the end of the next chapter for where to begin learning more about
these other methods. It is also worth mentioning that there are many
variations on the basic classification problem. For example,
we focus on the setting of **binary classification** where only two
classes are involved (e.g., a diagnosis of either healthy or diseased), but you may
also run into multiclass classification problems with more than two
categories (e.g., a diagnosis of healthy, bronchitis, pneumonia, or a common cold).

## Exploring a data set

```{index} breast cancer, question; classification
```

In this chapter and the next, we will study a data set of
[digitized breast cancer image features](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29),
created by Dr. William H. Wolberg, W. Nick Street, and Olvi L. Mangasarian {cite:p}`streetbreastcancer`.
Each row in the data set represents an
image of a tumor sample, including the diagnosis (benign or malignant) and
several other measurements (nucleus texture, perimeter, area, and more).
Diagnosis for each image was conducted by physicians.

As with all data analyses, we first need to formulate a precise question that
we want to answer. Here, the question is *predictive*: can
we use the tumor
image measurements available to us to predict whether a future tumor image
(with unknown diagnosis) shows a benign or malignant tumor? Answering this
question is important because traditional, non-data-driven methods for tumor
diagnosis are quite subjective and dependent upon how skilled and experienced
the diagnosing physician is. Furthermore, benign tumors are not normally
dangerous; the cells stay in the same place, and the tumor stops growing before
it gets very large. By contrast, in malignant tumors, the cells invade the
surrounding tissue and spread into nearby organs, where they can cause serious
damage {cite:p}`stanfordhealthcare`.
Thus, it is important to quickly and accurately diagnose the tumor type to
guide patient treatment.

+++

### Loading the cancer data

Our first step is to load, wrangle, and explore the data using visualizations
in order to better understand the data we are working with. We start by
loading the `pandas` and `altair` packages needed for our analysis.

```{code-cell} ipython3
import pandas as pd
import altair as alt
```

In this case, the file containing the breast cancer data set is a `.csv`
file with headers. We'll use the `read_csv` function with no additional
arguments, and then inspect its contents:

```{index} read function; read_csv
```

```{code-cell} ipython3
:tags: ["output_scroll"]
cancer = pd.read_csv("data/wdbc.csv")
cancer
```

### Describing the variables in the cancer data set

Breast tumors can be diagnosed by performing a *biopsy*, a process where
tissue is removed from the body and examined for the presence of disease.
Traditionally these procedures were quite invasive; modern methods such as fine
needle aspiration, used to collect the present data set, extract only a small
amount of tissue and are less invasive. Based on a digital image of each breast
tissue sample collected for this data set, ten different variables were measured
for each cell nucleus in the image (items 3&ndash;12 of the list of variables below), and then the mean
 for each variable across the nuclei was recorded. As part of the
data preparation, these values have been *standardized (centered and scaled)*; we will discuss what this
means and why we do it later in this chapter. Each image additionally was given
a unique ID and a diagnosis by a physician.  Therefore, the
total set of variables per image in this data set is:

1. ID: identification number
2. Class: the diagnosis (M = malignant or B = benign)
3. Radius: the mean of distances from center to points on the perimeter
4. Texture: the standard deviation of gray-scale values
5. Perimeter: the length of the surrounding contour
6. Area: the area inside the contour
7. Smoothness: the local variation in radius lengths
8. Compactness: the ratio of squared perimeter and area
9. Concavity: severity of concave portions of the contour
10. Concave Points: the number of concave portions of the contour
11. Symmetry: how similar the nucleus is when mirrored
12. Fractal Dimension: a measurement of how "rough" the perimeter is

+++

```{index} DataFrame; info
```

Below we use the `info` method to preview the data frame. This method can
make it easier to inspect the data when we have a lot of columns:
it prints only the column names down the page (instead of across),
as well as their data types and the number of non-missing entries.

```{code-cell} ipython3
cancer.info()
```

```{index} Series; unique
```

From the summary of the data above, we can see that `Class` is of type `object`.
We can use the `unique` method on the `Class` column to see all unique values
present in that column. We see that there are two diagnoses:
benign, represented by `"B"`, and malignant, represented by `"M"`.

```{code-cell} ipython3
cancer["Class"].unique()
```

We will improve the readability of our analysis
by renaming `"M"` to `"Malignant"` and `"B"` to `"Benign"` using the `replace`
method. The `replace` method takes one argument: a dictionary that maps
previous values to desired new values.
We will verify the result using the `unique` method.

```{index} Series; replace
```

```{code-cell} ipython3
cancer["Class"] = cancer["Class"].replace({
    "M" : "Malignant",
    "B" : "Benign"
})

cancer["Class"].unique()
```

### Exploring the cancer data

```{index} DataFrame; groupby, Series;size
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("benign_count", "{:0.0f}".format(cancer["Class"].value_counts()["Benign"]))
glue("benign_pct", "{:0.0f}".format(100*cancer["Class"].value_counts(normalize=True)["Benign"]))
glue("malignant_count", "{:0.0f}".format(cancer["Class"].value_counts()["Malignant"]))
glue("malignant_pct", "{:0.0f}".format(100*cancer["Class"].value_counts(normalize=True)["Malignant"]))
```

Before we start doing any modeling, let's explore our data set. Below we use
the `groupby` and `size` methods to find the number and percentage
of benign and malignant tumor observations in our data set. When paired with
`groupby`, `size` counts the number of observations for each value of the `Class`
variable. Then we calculate the percentage in each group by dividing by the total
number of observations and multiplying by 100.
The total number of observations equals the number of rows in the data frame,
which we can access via the `shape` attribute of the data frame
(`shape[0]` is the number of rows and `shape[1]` is the number of columns).
We have
{glue:text}`benign_count` ({glue:text}`benign_pct`\%) benign and
{glue:text}`malignant_count` ({glue:text}`malignant_pct`\%) malignant
tumor observations.

```{code-cell} ipython3
100 * cancer.groupby("Class").size() / cancer.shape[0]
```

```{index} Series; value_counts
```

The `pandas` package also has a more convenient specialized `value_counts` method for
counting the number of occurrences of each value in a column. If we pass no arguments
to the method, it outputs a series containing the number of occurences
of each value. If we instead pass the argument `normalize=True`, it instead prints the fraction
of occurrences of each value.

```{code-cell} ipython3
cancer["Class"].value_counts()
```

```{code-cell} ipython3
cancer["Class"].value_counts(normalize=True)
```

```{index} visualization; scatter
```

Next, let's draw a colored scatter plot to visualize the relationship between the
perimeter and concavity variables. Recall that the default palette in `altair`
is colorblind-friendly, so we can stick with that here.

```{code-cell} ipython3
:tags: ["remove-output"]
perim_concav = alt.Chart(cancer).mark_circle().encode(
    x=alt.X("Perimeter").title("Perimeter (standardized)"),
    y=alt.Y("Concavity").title("Concavity (standardized)"),
    color=alt.Color("Class").title("Diagnosis")
)
perim_concav
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("fig:05-scatter", perim_concav)
```

:::{glue:figure} fig:05-scatter
:name: fig:05-scatter

Scatter plot of concavity versus perimeter colored by diagnosis label.
:::

+++

In {numref}`fig:05-scatter`, we can see that malignant observations typically fall in
the upper right-hand corner of the plot area. By contrast, benign
observations typically fall in the lower left-hand corner of the plot. In other words,
benign observations tend to have lower concavity and perimeter values, and malignant
ones tend to have larger values. Suppose we
obtain a new observation not in the current data set that has all the variables
measured *except* the label (i.e., an image without the physician's diagnosis
for the tumor class). We could compute the standardized perimeter and concavity values,
resulting in values of, say, 1 and 1. Could we use this information to classify
that observation as benign or malignant? Based on the scatter plot, how might
you classify that new observation? If the standardized concavity and perimeter
values are 1 and 1 respectively, the point would lie in the middle of the
orange cloud of malignant points and thus we could probably classify it as
malignant. Based on our visualization, it seems like
it may be possible to make accurate predictions of the `Class` variable (i.e., a diagnosis) for
tumor images with unknown diagnoses.

+++

## Classification with K-nearest neighbors

```{code-cell} ipython3
:tags: [remove-cell]

new_point = [2, 4]
glue("new_point_1_0", "{:.1f}".format(new_point[0]))
glue("new_point_1_1", "{:.1f}".format(new_point[1]))
attrs = ["Perimeter", "Concavity"]
points_df = pd.DataFrame(
    {"Perimeter": new_point[0], "Concavity": new_point[1], "Class": ["Unknown"]}
)
perim_concav_with_new_point_df = pd.concat((cancer, points_df), ignore_index=True)
# Find the euclidean distances from the new point to each of the points
# in the orginal data set
my_distances = euclidean_distances(perim_concav_with_new_point_df[attrs])[
    len(cancer)
][:-1]
```

```{index} K-nearest neighbors; classification
```

In order to actually make predictions for new observations in practice, we
will need a classification algorithm.
In this book, we will use the K-nearest neighbors classification algorithm.
To predict the label of a new observation (here, classify it as either benign
or malignant), the K-nearest neighbors classifier generally finds the $K$
"nearest" or "most similar" observations in our training set, and then uses
their diagnoses to make a prediction for the new observation's diagnosis. $K$
is a number that we must choose in advance; for now, we will assume that someone has chosen
$K$ for us. We will cover how to choose $K$ ourselves in the next chapter.

To illustrate the concept of K-nearest neighbors classification, we
will walk through an example.  Suppose we have a
new observation, with standardized perimeter
of {glue:text}`new_point_1_0` and standardized concavity
of {glue:text}`new_point_1_1`, whose
diagnosis "Class" is unknown. This new observation is
depicted by the red, diamond point in {numref}`fig:05-knn-2`.

```{code-cell} ipython3
:tags: [remove-cell]

perim_concav_with_new_point = (
    alt.Chart(perim_concav_with_new_point_df)
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Perimeter").title("Perimeter (standardized)"),
        y=alt.Y("Concavity").title("Concavity (standardized)"),
        color=alt.Color("Class").title("Diagnosis"),
        shape=alt.Shape("Class").scale(range=["circle", "circle", "diamond"]),
        size=alt.condition("datum.Class == 'Unknown'", alt.value(100), alt.value(30)),
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None)),
    )
)
glue('fig:05-knn-2', perim_concav_with_new_point, display=True)
```

:::{glue:figure} fig:05-knn-2
:name: fig:05-knn-2

Scatter plot of concavity versus perimeter with new observation represented as a red diamond.
:::

```{code-cell} ipython3
:tags: [remove-cell]

near_neighbor_df = pd.concat([
    cancer.loc[[np.argmin(my_distances)], attrs],
    perim_concav_with_new_point_df.loc[[cancer.shape[0]], attrs],
])
glue("1-neighbor_per", "{:.1f}".format(near_neighbor_df.iloc[0, :]["Perimeter"]))
glue("1-neighbor_con", "{:.1f}".format(near_neighbor_df.iloc[0, :]["Concavity"]))
```

{numref}`fig:05-knn-3` shows that the nearest point to this new observation is
**malignant** and located at the coordinates ({glue:text}`1-neighbor_per`,
{glue:text}`1-neighbor_con`). The idea here is that if a point is close to another
in the scatter plot, then the perimeter and concavity values are similar,
and so we may expect that they would have the same diagnosis.

```{code-cell} ipython3
:tags: [remove-cell]

line = (
    alt.Chart(near_neighbor_df)
    .mark_line()
    .encode(x="Perimeter", y="Concavity", color=alt.value("black"))
)

glue('fig:05-knn-3', (perim_concav_with_new_point + line), display=True)
```

:::{glue:figure} fig:05-knn-3
:name: fig:05-knn-3

Scatter plot of concavity versus perimeter. The new observation is represented
as a red diamond with a line to the one nearest neighbor, which has a malignant
label.
:::

```{code-cell} ipython3
:tags: [remove-cell]

new_point = [0.2, 3.3]
attrs = ["Perimeter", "Concavity"]
points_df2 = pd.DataFrame(
    {"Perimeter": new_point[0], "Concavity": new_point[1], "Class": ["Unknown"]}
)
perim_concav_with_new_point_df2 = pd.concat((cancer, points_df2), ignore_index=True)
# Find the euclidean distances from the new point to each of the points
# in the orginal data set
my_distances2 = euclidean_distances(perim_concav_with_new_point_df2[attrs])[
    len(cancer)
][:-1]
glue("new_point_2_0", "{:.1f}".format(new_point[0]))
glue("new_point_2_1", "{:.1f}".format(new_point[1]))
```

```{code-cell} ipython3
:tags: [remove-cell]

perim_concav_with_new_point2 = (
    alt.Chart(
        perim_concav_with_new_point_df2,
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
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None)),
    )
)

near_neighbor_df2 = pd.concat([
    cancer.loc[[np.argmin(my_distances2)], attrs],
    perim_concav_with_new_point_df2.loc[[cancer.shape[0]], attrs],
])
line2 = alt.Chart(near_neighbor_df2).mark_line().encode(
    x="Perimeter",
    y="Concavity",
    color=alt.value("black")
)

glue("2-neighbor_per", "{:.1f}".format(near_neighbor_df2.iloc[0, :]["Perimeter"]))
glue("2-neighbor_con", "{:.1f}".format(near_neighbor_df2.iloc[0, :]["Concavity"]))
glue('fig:05-knn-4', (perim_concav_with_new_point2 + line2), display=True)
```

Suppose we have another new observation with standardized perimeter
{glue:text}`new_point_2_0` and concavity of {glue:text}`new_point_2_1`. Looking at the
scatter plot in {numref}`fig:05-knn-4`, how would you classify this red,
diamond observation? The nearest neighbor to this new point is a
**benign** observation at ({glue:text}`2-neighbor_per`, {glue:text}`2-neighbor_con`).
Does this seem like the right prediction to make for this observation? Probably
not, if you consider the other nearby points.

