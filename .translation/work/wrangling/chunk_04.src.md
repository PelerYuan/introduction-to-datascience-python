+++

We will start by showing how to compute the minimum and maximum number of Canadians reporting a particular
language as their primary language at home. First, a reminder of what `region_lang` looks like:

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang = pd.read_csv("data/region_lang.csv")
region_lang
```

```{index} Series; min, Series; max
```

We use `.min` to calculate the minimum
and `.max` to calculate maximum number of Canadians
reporting a particular language as their primary language at home,
for any region.

```{code-cell} ipython3
region_lang["most_at_home"].min()
```

```{code-cell} ipython3
region_lang["most_at_home"].max()
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("lang_most_people", "{0:,.0f}".format(int(region_lang["most_at_home"].max())))
```

From this we see that there are some languages in the data set that no one speaks
as their primary language at home. We also see that the most commonly spoken
primary language at home is spoken by
{glue:text}`lang_most_people` people. If instead we wanted to know the
total number of people in the survey, we could use the `sum` summary statistic method.
```{code-cell} ipython3
region_lang["most_at_home"].sum()
```

```{index} Series; sum, Series; mean, Series; median, Series; std, summary statistic
```

Other handy summary statistics include the `mean`, `median` and `std` for
computing the mean, median, and standard deviation of observations, respectively.
We can also compute multiple statistics at once using `agg` to "aggregate" results.
For example, if we wanted to
compute both the `min` and `max` at once, we could use `agg` with the argument `["min", "max"]`.
Note that `agg` outputs a `Series` object.

```{code-cell} ipython3
region_lang["most_at_home"].agg(["min", "max"])
```

The `pandas` package also provides the `describe` method,
which is a handy function that computes many common summary statistics at once; it
gives us a *summary* of a variable.

```{code-cell} ipython3
region_lang["most_at_home"].describe()
```

In addition to the summary methods we introduced earlier, the `describe` method
outputs a `count` (the total number of observations, or rows, in our data frame),
as well as the 25th, 50th, and 75th percentiles.
{numref}`tab:basic-summary-statistics` provides an overview of some of the useful
summary statistics that you can compute with `pandas`.

```{table} Basic summary statistics
:name: tab:basic-summary-statistics
| Function | Description |
| -------- | ----------- |
| `count` | The number of observations (rows) |
| `mean` | The mean of the observations |
| `median` | The median value of the observations |
| `std` | The standard deviation of the observations |
| `max` | The largest value in a column |
| `min` | The smallest value in a column |
| `sum` | The sum of all observations |
| `agg` | Aggregate multiple statistics together |
| `describe` | a summary |
```

+++
+++

```{index} see: NaN; missing data
```

```{index} missing data
```


```{note}
In `pandas`, the value `NaN` is often used to denote missing data.
By default, when `pandas` calculates summary statistics (e.g., `max`, `min`, `sum`, etc),
it ignores these values. If you look at the documentation for these functions, you will
see an input variable `skipna`, which by default is set to `skipna=True`. This means that
`pandas` will skip `NaN` values when computing statistics.
```

### Calculating summary statistics on data frames

What if you want to calculate summary statistics on an entire data frame? Well,
it turns out that the functions in {numref}`tab:basic-summary-statistics`
can be applied to a whole data frame!
For example, we can ask for the maximum value of each each column has using `max`.

```{code-cell} ipython3
region_lang.max()
```

We can see that for columns that contain string data
with words like `"Vancouver"` and `"Halifax"`,
the maximum value is determined by sorting the string alphabetically
and returning the last value.
If we only want the maximum value for
numeric columns,
we can provide `numeric_only=True`:

```{code-cell} ipython3
region_lang.max(numeric_only=True)
```

We could also ask for the `mean` for each columns in the dataframe.
It does not make sense to compute the mean of the string columns,
so in this case we *must* provide the keyword `numeric_only=True`
so that the mean is only computed on columns with numeric values.

```{code-cell} ipython3
region_lang.mean(numeric_only=True)
```

If there are only some columns for which you would like to get summary statistics,
you can first use `[]` or `.loc[]` to select those columns,
and then ask for the summary statistic
as we did for a single column previously.
For example, if we want to know
the mean and standard deviation of all of the columns between `"mother_tongue"` and `"lang_known"`,
we use `.loc[]` to select those columns and then `agg` to ask for both the `mean` and `std`.
```{code-cell} ipython3
region_lang.loc[:, "mother_tongue":"lang_known"].agg(["mean", "std"])
```

## Performing operations on groups of rows using `groupby`

+++

```{index} DataFrame; groupby
```
What happens if we want to know how languages vary by region? In this case,
we need a new tool that lets us group rows by region. This can be achieved
using the `groupby` function in `pandas`. Pairing summary functions
with `groupby` lets you summarize values for subgroups within a data set,
as illustrated in {numref}`fig:summarize-groupby`.
For example, we can use `groupby` to group the regions of the `tidy_lang` data
frame and then calculate the minimum and maximum number of Canadians
reporting the language as the primary language at home
for each of the regions in the data set.

+++ {"tags": []}

```{figure} img/wrangling/summarize.002.png
:name: fig:summarize-groupby
:figclass: figure

A summary statistic function paired with `groupby` is useful for calculating that statistic
on one or more column(s) for each group. It
creates a new data frame with one row for each group
and one column for each summary statistic. The darker, top row of each table
represents the column headers. The orange, blue, and green colored rows
correspond to the rows that belong to each of the three groups being
represented in this cartoon example.
```

+++

The `groupby` function takes at least one argument&mdash;the columns to use in the
grouping. Here we use only one column for grouping (`region`).

```{code-cell} ipython3
region_lang.groupby("region")
```

Notice that `groupby` converts a `DataFrame` object to a `DataFrameGroupBy`
object, which contains information about the groups of the data frame. We can
then apply aggregating functions to the `DataFrameGroupBy` object. Here we first
select the `most_at_home` column, and then summarize the grouped data by their
minimum and maximum values using `agg`.

```{code-cell} ipython3
region_lang.groupby("region")["most_at_home"].agg(["min", "max"])
```

The resulting dataframe has `region` as an index name.
This is similar to what happened when we used the `pivot` function
in {numref}`pivot-wider`;
and just as we did then,
you can use `reset_index` to get back to a regular dataframe
with `region` as a column name.

```{code-cell} ipython3
region_lang.groupby("region")["most_at_home"].agg(["min", "max"]).reset_index()
```
You can also pass multiple column names to `groupby`. For example, if we wanted to
know about how the different categories of languages (Aboriginal, Non-Official &
Non-Aboriginal, and  Official) are spoken at home in different regions, we would pass a
list including `region` and `category` to `groupby`.

```{code-cell} ipython3
region_lang.groupby(["region", "category"])["most_at_home"].agg(["min", "max"]).reset_index()
```

You can also ask for grouped summary statistics on the whole data frame.

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.groupby("region").agg(["min", "max"]).reset_index()
```

If you want to ask for only some columns, for example
the columns between `"most_at_home"` and `"lang_known"`,
you might think about first applying `groupby` and then `["most_at_home":"lang_known"]`;
but `groupby` returns a `DataFrameGroupBy` object, which does not
work with ranges inside `[]`.
The other option is to do things the other way around:
first use  `["most_at_home":"lang_known"]`, then use `groupby`.
This can work, but you have to be careful! For example,
in our case, we get an error.

```{code-cell} ipython3
:tags: [remove-output]
region_lang["most_at_home":"lang_known"].groupby("region").max()
```

```{code-cell} ipython3
:tags: ["remove-input"]
print('KeyError: "region"')
```

This is because when we use `[]` we selected only the columns between
`"most_at_home"` and `"lang_known"`, which doesn't include `"region"`!
Instead, we need to use `groupby` first
and then call `[]` with a list of column names that includes `region`;
this approach always works.

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.groupby("region")[["most_at_home", "most_at_work", "lang_known"]].max().reset_index()
```

To see how many observations there are in each group,
we can use `value_counts`.

```{index} DataFrame; value_counts
```

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.value_counts("region")
```

Which takes the `normalize` parameter to show the output as proportion
instead of a count.

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.value_counts("region", normalize=True)
```

+++

## Apply functions across multiple columns

Computing summary statistics is not the only situation in which we need
to apply a function across columns in a data frame. There are two other
common wrangling tasks that require the application of a function across columns.
The first is when we want to apply a transformation, such as a conversion of measurement units, to multiple columns.
We illustrate such a data transformation in {numref}`fig:mutate-across`; note that it does not
change the shape of the data frame.

```{figure} img/wrangling/summarize.005.png
:name: fig:mutate-across
:figclass: figure

A transformation applied across many columns. The darker, top row of each table represents the column headers.
```

For example, imagine that we wanted to convert all the numeric columns
in the `region_lang` data frame from `int64` type to `int32` type
using the `.astype` function.
When we revisit the `region_lang` data frame,
we can see that this would be the columns from `mother_tongue` to `lang_known`.

```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang
```

```{index} DataFrame; apply, DataFrame; loc[]
```

We can simply call the `.astype` function to apply it across the desired range of columns.

```{index} DataFrame; astype, Series; astype
```

```{code-cell} ipython3
region_lang_nums = region_lang.loc[:, "mother_tongue":"lang_known"].astype("int32")
region_lang_nums.info()
```
You can now see that the columns from `mother_tongue` to `lang_known` are type `int32`,
and that we have obtained a data frame with the same number of columns and rows
as the input data frame.

The second situation occurs when you want to apply a function across columns within each individual
row, i.e., *row-wise*. This operation, illustrated in {numref}`fig:rowwise`,
will produce a single column whose entries summarize each row in the original data frame;
this new column can be added back into the original data.

```{figure} img/wrangling/summarize.004.png
:name: fig:rowwise
:figclass: figure

A function applied row-wise across a data frame, producing a new column. The
darker, top row of each table represents the column headers.
```

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
