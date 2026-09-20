For example, suppose we want to know the maximum value between `mother_tongue`,
and `lang_known` for each language and region in the `region_lang_nums` data set.
In other words, we want to apply the `max` function *row-wise.*
In order to tell `max` that we want to work row-wise (as opposed to acting on each column
individually, which is the default behavior), we just specify the argument `axis=1`.

```{code-cell} ipython3
region_lang_nums.max(axis=1)
```

We see that we obtain a series containing the maximum value between `mother_tongue`,
`most_at_home`, `most_at_work` and `lang_known` for each row in the data frame. It
is often the case that we want to include a column result
from a row-wise operation as a new column in the data frame, so that we can make
plots or continue our analysis. To make this happen,
we will use column assignment or the `assign` function to create a new column.
This is discussed in the next section.

```{note}
While `pandas` provides many methods (like `max`, `astype`, etc.) that can be applied to a data frame,
sometimes you may want to apply your own function to multiple columns in a data frame. In this case
you can use the more general [`apply`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html) method.
```

(pandas-assign)=
