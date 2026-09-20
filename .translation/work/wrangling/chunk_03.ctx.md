```{code-cell} ipython3
tidy_lang.info()
```

Now we see `most_at_home` and `most_at_work` columns are of `int64` data types,
indicating they are integer data types (i.e., numbers)!

+++

## Using `[]` to extract rows or columns

Now that the `tidy_lang` data is indeed *tidy*, we can start manipulating it
using the powerful suite of functions from the `pandas`.
We will first revisit the `[]` from {numref}`Chapter %s <intro>`,
which lets us obtain a subset of either the rows **or** the columns of a data frame.
This section will highlight more advanced usage of the `[]` function,
including an in-depth treatment of the variety of logical statements
one can use in the `[]` to select subsets of rows.

```{index} DataFrame; [], logical statement
```

```{index} see: logical statement; logical operator
```

