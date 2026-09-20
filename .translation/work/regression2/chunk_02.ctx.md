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

