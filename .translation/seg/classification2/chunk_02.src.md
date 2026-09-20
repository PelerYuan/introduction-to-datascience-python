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

