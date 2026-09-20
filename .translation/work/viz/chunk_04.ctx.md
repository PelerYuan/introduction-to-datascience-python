can influence how Python and `altair` treats it. Here, we indeed have an issue
with the data types in the `morley` data frame. In particular, the `Expt` column
is currently an *integer*---specifically, an `int64` type. But we want to treat it as a
*category*, i.e., there should be one category per type of experiment.
```{code-cell} ipython3
morley_df.info()
```

```{index} nominal, altair; :N
```

To fix this issue we can convert the `Expt` variable into a `nominal`
(i.e., categorical) type variable by adding a suffix `:N`
to the `Expt` variable. Adding the `:N` suffix ensures that `altair`
will treat a variable as a categorical variable, and
hence use a discrete color map in visualizations
([read more about data types in the altair documentation](https://altair-viz.github.io/user_guide/encodings/index.html#encoding-data-types)).
We also add the `stack(False)` method on the `y` encoding so
that the bars are not stacked on top of each other,
but instead share the same baseline.
We try to ensure that the different colors can be seen
despite them sitting in front of each other
by setting the `opacity` argument in `mark_bar` to `0.5`
to make the bars slightly translucent.

