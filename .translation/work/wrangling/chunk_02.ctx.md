are stored as column names. Thus they
are not easily accessible to the data analysis functions we will apply
to our data set. Additionally, the *mother tongue* variable values are
spread across multiple columns, which will prevent us from doing any desired
visualization or statistical tasks until we combine them into one column. For
instance, suppose we want to know the languages with the highest number of
Canadians reporting it as their mother tongue among all five regions. This
question would be tough to answer with the data in its current format.
We *could* find the answer with the data in this format,
though it would be much easier to answer if we tidy our
data first. If mother tongue were instead stored as one column,
as shown in the tidy data on the right in
{numref}`fig:img-pivot-longer-with-table`,
we could simply use one line of code (`df["mother_tongue"].max()`)
to get the maximum value.

+++ {"tags": []}

```{figure} img/wrangling/pandas_melt_wide-long.png
:name: fig:img-pivot-longer-with-table
:figclass: figure

Going from wide to long with the `melt` function.
```

