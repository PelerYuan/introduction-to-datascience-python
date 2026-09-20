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

