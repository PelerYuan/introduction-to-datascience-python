
(classification2)=
# Classification II: evaluation & tuning

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
```

## Overview
This chapter continues the introduction to predictive modeling through
classification. While the previous chapter covered training and data
preprocessing, this chapter focuses on how to evaluate the performance of
a classifier, as well as how to improve the classifier (where possible)
to maximize its accuracy.

## Chapter learning objectives
By the end of the chapter, readers will be able to do the following:

- Describe what training, validation, and test data sets are and how they are used in classification.
- Split data into training, validation, and test data sets.
- Describe what a random seed is and its importance in reproducible data analysis.
- Set the random seed in Python using the `numpy.random.seed` function.
- Describe and interpret accuracy, precision, recall, and confusion matrices.
- Evaluate classification accuracy, precision, and recall in Python using a test set, a single validation set, and cross-validation.
- Produce a confusion matrix in Python.
- Choose the number of neighbors in a K-nearest neighbors classifier by maximizing estimated cross-validation accuracy.
- Describe underfitting and overfitting, and relate it to the number of neighbors in K-nearest neighbors classification.
- Describe the advantages and disadvantages of the K-nearest neighbors classification algorithm.

+++

## Evaluating performance

```{index} breast cancer
```

Sometimes our classifier might make the wrong prediction. A classifier does not
need to be right 100\% of the time to be useful, though we don't want the
classifier to make too many wrong predictions. How do we measure how "good" our
classifier is? Let's revisit the
[breast cancer images data](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29) {cite:p}`streetbreastcancer`
and think about how our classifier will be used in practice. A biopsy will be
performed on a *new* patient's tumor, the resulting image will be analyzed,
and the classifier will be asked to decide whether the tumor is benign or
malignant. The key word here is *new*: our classifier is "good" if it provides
accurate predictions on data *not seen during training*, as this implies that
it has actually learned about the relationship between the predictor variables and response variable,
as opposed to simply memorizing the labels of individual training data examples.
But then, how can we evaluate our classifier without visiting the hospital to collect more
tumor images?


```{index} training set, test set
```

The trick is to split the data into a **training set** and **test set** ({numref}`fig:06-training-test`)
and use only the **training set** when building the classifier.
Then, to evaluate the performance of the classifier, we first set aside the labels from the **test set**,
and then use the classifier to predict the labels in the **test set**. If our predictions match the actual
labels for the observations in the **test set**, then we have some
confidence that our classifier might also accurately predict the class
labels for new observations without known class labels.

```{index} golden rule of machine learning
```

```{note}
If there were a golden rule of machine learning, it might be this:
*you cannot use the test data to build the model!* If you do, the model gets to
"see" the test data in advance, making it look more accurate than it really
is. Imagine how bad it would be to overestimate your classifier's accuracy
when predicting whether a patient's tumor is malignant or benign!
```

+++

```{figure} img/classification2/training_test.png
:name: fig:06-training-test

Splitting the data into training and testing sets.
```

+++

```{index} see: prediction accuracy; accuracy
```

```{index} accuracy
```

How exactly can we assess how well our predictions match the actual labels for
the observations in the test set? One way we can do this is to calculate the
prediction **accuracy**. This is the fraction of examples for which the
classifier made the correct prediction. To calculate this, we divide the number
of correct predictions by the number of predictions made.
The process for assessing if our predictions match the actual labels in the
test set is illustrated in {numref}`fig:06-ML-paradigm-test`.

$$\mathrm{accuracy} = \frac{\mathrm{number \; of  \; correct  \; predictions}}{\mathrm{total \;  number \;  of  \; predictions}}$$

+++

```{figure} img/classification2/ML-paradigm-test.png
:name: fig:06-ML-paradigm-test

Process for splitting the data and finding the prediction accuracy.
```

```{index} confusion matrix
```

Accuracy is a convenient, general-purpose way to summarize the performance of a classifier with
a single number.  But prediction accuracy by itself does not tell the whole
story.  In particular, accuracy alone only tells us how often the classifier
makes mistakes in general, but does not tell us anything about the *kinds* of
mistakes the classifier makes.  A more comprehensive view of performance can be
obtained by additionally examining the **confusion matrix**. The confusion
matrix shows how many test set labels of each type are predicted correctly and
incorrectly, which gives us more detail about the kinds of mistakes the
classifier tends to make.  {numref}`confusion-matrix-table` shows an example
of what a confusion matrix might look like for the tumor image data with
a test set of 65 observations.

```{list-table} An example confusion matrix for the tumor image data.
:header-rows: 1
:name: confusion-matrix-table

* -
  - Predicted Malignant
  - Predicted Benign
* - **Actually Malignant**
  - 1
  - 3
* - **Actually Benign**
  - 4
  - 57
```

In the example in {numref}`confusion-matrix-table`, we see that there was
1 malignant observation that was correctly classified as malignant (top left corner),
and 57 benign observations that were correctly classified as benign (bottom right corner).
However, we can also see that the classifier made some mistakes:
it classified 3 malignant observations as benign, and 4 benign observations as
malignant. The accuracy of this classifier is roughly
89%, given by the formula

$$\mathrm{accuracy} = \frac{\mathrm{number \; of  \; correct  \; predictions}}{\mathrm{total \;  number \;  of  \; predictions}} = \frac{1+57}{1+57+4+3} = 0.892.$$

But we can also see that the classifier only identified 1 out of 4 total malignant
tumors; in other words, it misclassified 75% of the malignant cases present in the
data set! In this example, misclassifying a malignant tumor is a potentially
disastrous error, since it may lead to a patient who requires treatment not receiving it.
Since we are particularly interested in identifying malignant cases, this
classifier would likely be unacceptable even with an accuracy of 89%.

```{index} positive label, negative label, true positive, true negative, false positive, false negative
```

Focusing more on one label than the other is
common in classification problems. In such cases, we typically refer to the label we are more
interested in identifying as the *positive* label, and the other as the
*negative* label. In the tumor example, we would refer to malignant
observations as *positive*, and benign observations as *negative*.  We can then
use the following terms to talk about the four kinds of prediction that the
classifier can make, corresponding to the four entries in the confusion matrix:

- **True Positive:** A malignant observation that was classified as malignant (top left in {numref}`confusion-matrix-table`).
- **False Positive:** A benign observation that was classified as malignant (bottom left in {numref}`confusion-matrix-table`).
- **True Negative:** A benign observation that was classified as benign (bottom right in {numref}`confusion-matrix-table`).
- **False Negative:** A malignant observation that was classified as benign (top right in {numref}`confusion-matrix-table`).

```{index} precision, recall
```

A perfect classifier would have zero false negatives and false positives (and
therefore, 100% accuracy). However, classifiers in practice will almost always
make some errors. So you should think about which kinds of error are most
important in your application, and use the confusion matrix to quantify and
report them. Two commonly used metrics that we can compute using the confusion
matrix are the **precision** and **recall** of the classifier. These are often
reported together with accuracy.  *Precision* quantifies how many of the
positive predictions the classifier made were actually positive. Intuitively,
we would like a classifier to have a *high* precision: for a classifier with
high precision, if the classifier reports that a new observation is positive,
we can trust that the new observation is indeed positive. We can compute the
precision of a classifier using the entries in the confusion matrix, with the
formula

$$\mathrm{precision} = \frac{\mathrm{number \; of  \; correct \; positive \; predictions}}{\mathrm{total \;  number \;  of \; positive  \; predictions}}.$$

*Recall* quantifies how many of the positive observations in the test set were
identified as positive. Intuitively, we would like a classifier to have a
*high* recall: for a classifier with high recall, if there is a positive
observation in the test data, we can trust that the classifier will find it.
We can also compute the recall of the classifier using the entries in the
confusion matrix, with the formula

$$\mathrm{recall} = \frac{\mathrm{number \; of  \; correct  \; positive \; predictions}}{\mathrm{total \;  number \;  of  \; positive \; test \; set \; observations}}.$$

In the example presented in {numref}`confusion-matrix-table`, we have that the precision and recall are

$$\mathrm{precision} = \frac{1}{1+4} = 0.20, \quad \mathrm{recall} = \frac{1}{1+3} = 0.25.$$

So even with an accuracy of 89%, the precision and recall of the classifier
were both relatively low. For this data analysis context, recall is
particularly important: if someone has a malignant tumor, we certainly want to
identify it.  A recall of just 25% would likely be unacceptable!

```{note}
It is difficult to achieve both high precision and high recall at
the same time; models with high precision tend to have low recall and vice
versa.  As an example, we can easily make a classifier that has *perfect
recall*: just *always* guess positive! This classifier will of course find
every positive observation in the test set, but it will make lots of false
positive predictions along the way  and have low precision. Similarly, we can
easily make a classifier that has *perfect precision*: *never* guess
positive! This classifier will never incorrectly identify an obsevation as
positive, but it will make a lot of false negative predictions along the way.
In fact, this classifier will have 0% recall! Of course, most real
classifiers fall somewhere in between these two extremes. But these examples
serve to show that in settings where one of the classes is of interest (i.e.,
there is a *positive* label), there is a trade-off between precision and recall that one has to
make when designing a classifier.
```

+++

(randomseeds)=
## Randomness and seeds

```{index} random
```

Beginning in this chapter, our data analyses will often involve the use
of *randomness*. We use randomness any time we need to make a decision in our
analysis that needs to be fair, unbiased, and not influenced by human input.
For example, in this chapter, we need to split
a data set into a training set and test set to evaluate our classifier. We
certainly do not want to choose how to split
the data ourselves by hand, as we want to avoid accidentally influencing the result
of the evaluation. So instead, we let Python *randomly* split the data.
In future chapters we will use randomness
in many other ways, e.g., to help us select a small subset of data from a larger data set,
to pick groupings of data, and more.

```{index} reproducible, seed
```

```{index} see: random seed; seed
```

```{index} seed; numpy.random.seed
```

However, the use of randomness runs counter to one of the main
tenets of good data analysis practice: *reproducibility*. Recall that a reproducible
analysis produces the same result each time it is run; if we include randomness
in the analysis, would we not get a different result each time?
The trick is that in Python&mdash;and other programming languages&mdash;randomness
is not actually random! Instead, Python uses a *random number generator* that
produces a sequence of numbers that
are completely determined by a
 *seed value*. Once you set the seed value, everything after that point may *look* random,
but is actually totally reproducible. As long as you pick the same seed
value, you get the same result!

```{index} sample, to_list
```

Let's use an example to investigate how randomness works in Python. Say we
have a series object containing the integers from 0 to 9. We want
to randomly pick 10 numbers from that list, but we want it to be reproducible.
Before randomly picking the 10 numbers,
we call the `seed` function from the `numpy` package, and pass it any integer as the argument.
Below we use the seed number `1`. At
that point, Python will keep track of the randomness that occurs throughout the code.
For example, we can call the `sample` method
on the series of numbers, passing the argument `n=10` to indicate that we want 10 samples.
The `to_list` method converts the resulting series into a basic Python list to make
the output easier to read.

```{code-cell} ipython3
import numpy as np
import pandas as pd

np.random.seed(1)

nums_0_to_9 = pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

random_numbers1 = nums_0_to_9.sample(n=10).to_list()
random_numbers1
```
You can see that `random_numbers1` is a list of 10 numbers
from 0 to 9 that, from all appearances, looks random. If
we run the `sample` method again,
we will get a fresh batch of 10 numbers that also look random.

```{code-cell} ipython3
random_numbers2 = nums_0_to_9.sample(n=10).to_list()
random_numbers2
```

If we want to force Python to produce the same sequences of random numbers,
we can simply call the `np.random.seed` function with the seed value `1`---the same
as before---and then call the `sample` method again.

```{code-cell} ipython3
np.random.seed(1)
random_numbers1_again = nums_0_to_9.sample(n=10).to_list()
random_numbers1_again
```

```{code-cell} ipython3
random_numbers2_again = nums_0_to_9.sample(n=10).to_list()
random_numbers2_again
```

Notice that after calling `np.random.seed`, we get the same
two sequences of numbers in the same order. `random_numbers1` and `random_numbers1_again`
produce the same sequence of numbers, and the same can be said about `random_numbers2` and
`random_numbers2_again`. And if we choose a different value for the seed---say, 4235---we
obtain a different sequence of random numbers.

```{code-cell} ipython3
np.random.seed(4235)
random_numbers1_different = nums_0_to_9.sample(n=10).to_list()
random_numbers1_different
```

```{code-cell} ipython3
random_numbers2_different = nums_0_to_9.sample(n=10).to_list()
random_numbers2_different
```

In other words, even though the sequences of numbers that Python is generating *look*
random, they are totally determined when we set a seed value!

So what does this mean for data analysis? Well, `sample` is certainly not the
only place where randomness is used in Python. Many of the functions
that we use in `scikit-learn` and beyond use randomness&mdash;some
of them without even telling you about it.  Also note that when Python starts
up, it creates its own seed to use. So if you do not explicitly
call the `np.random.seed` function, your results
will likely not be reproducible. Finally, be careful to set the seed *only once* at
the beginning of a data analysis. Each time you set the seed, you are inserting
your own human input, thereby influencing the analysis. For example, if you use
the `sample` many times throughout your analysis but set the seed each time, the
randomness that Python uses will not look as random as it should.

In summary: if you want your analysis to be reproducible, i.e., produce *the same result*
each time you run it, make sure to use `np.random.seed` exactly once
at the beginning of the analysis. Different argument values
in `np.random.seed` will lead to different patterns of randomness, but as long as you pick the same
value your analysis results will be the same. In the remainder of the textbook,
we will set the seed once at the beginning of each chapter.

```{index} RandomState
```

```{index} see: RandomState; seed
```

````{note}
When you use `np.random.seed`, you are really setting the seed for the `numpy`
package's *default random number generator*. Using the global default random
number generator is easier than other methods, but has some potential drawbacks. For example,
other code that you may not notice (e.g., code buried inside some
other package) could potentially *also* call `np.random.seed`, thus modifying
your analysis in an undesirable way. Furthermore, not *all* functions use
`numpy`'s random number generator; some may use another one entirely.
In that case, setting `np.random.seed` may not actually make your whole analysis
reproducible.

In this book, we will generally only use packages that play nicely with `numpy`'s
default random number generator, so we will stick with `np.random.seed`.
You can achieve more careful control over randomness in your analysis
by creating a `numpy` [`Generator` object](https://numpy.org/doc/stable/reference/random/generator.html)
once at the beginning of your analysis, and passing it to
the `random_state` argument that is available in many `pandas` and `scikit-learn`
functions. Those functions will then use your `Generator` to generate random numbers instead of
`numpy`'s default generator. For example, we can reproduce our earlier example by using a `Generator`
object with the `seed` value set to 1; we get the same lists of numbers once again.
```python
from numpy.random import Generator, PCG64
rng = Generator(PCG64(seed=1))
random_numbers1_third = nums_0_to_9.sample(n=10, random_state=rng).to_list()
random_numbers1_third
```
```text
array([2, 9, 6, 4, 0, 3, 1, 7, 8, 5])
```
```python
random_numbers2_third = nums_0_to_9.sample(n=10, random_state=rng).to_list()
random_numbers2_third
```
```text
array([9, 5, 3, 0, 8, 4, 2, 1, 6, 7])
```

````

## Evaluating performance with `scikit-learn`

```{index} scikit-learn, visualization; scatter
```

Back to evaluating classifiers now!
In Python, we can use the `scikit-learn` package not only to perform K-nearest neighbors
classification, but also to assess how well our classification worked.
Let's work through an example of how to use tools from `scikit-learn` to evaluate a classifier
 using the breast cancer data set from the previous chapter.
We begin the analysis by loading the packages we require,
reading in the breast cancer data,
and then making a quick scatter plot visualization of
tumor cell concavity versus smoothness colored by diagnosis in {numref}`fig:06-precode`.
You will also notice that we set the random seed using the `np.random.seed` function,
as described in {numref}`randomseeds`.

```{code-cell} ipython3
:tags: ["remove-output"]
# load packages
import altair as alt
import pandas as pd
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")

# set the seed
np.random.seed(1)

# load data
cancer = pd.read_csv("data/wdbc_unscaled.csv")
# re-label Class "M" as "Malignant", and Class "B" as "Benign"
cancer["Class"] = cancer["Class"].replace({
    "M" : "Malignant",
    "B" : "Benign"
})

# create scatter plot of tumor cell concavity versus smoothness,
# labeling the points be diagnosis class

perim_concav = alt.Chart(cancer).mark_circle().encode(
    x=alt.X("Smoothness").scale(zero=False),
    y="Concavity",
    color=alt.Color("Class").title("Diagnosis")
)
perim_concav
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("fig:06-precode", perim_concav)
```

:::{glue:figure} fig:06-precode
:name: fig:06-precode

Scatter plot of tumor cell concavity versus smoothness colored by diagnosis label.
:::



+++

### Create the train / test split

Once we have decided on a predictive question to answer and done some
preliminary exploration, the very next thing to do is to split the data into
the training and test sets. Typically, the training set is between 50% and 95% of
the data, while the test set is the remaining 5% to 50%; the intuition is that
you want to trade off between training an accurate model (by using a larger
training data set) and getting an accurate evaluation of its performance (by
using a larger test data set). Here, we will use 75% of the data for training,
and 25% for testing.

