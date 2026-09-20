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

