+++

{numref}`fig:img-pivot-longer` details the arguments that we need to specify
in the `melt` function to accomplish this data transformation.

+++ {"tags": []}

```{figure} img/wrangling/pandas_melt_args_labels.png
:name: fig:img-pivot-longer
:figclass: figure

Syntax for the `melt` function.
```

+++

```{index} column range
```

```{index} see: :; column range
```

We use `melt` to combine the Toronto, Montréal,
Vancouver, Calgary, and Edmonton columns into a single column called `region`,
and create a column called `mother_tongue` that contains the count of how many
Canadians report each language as their mother tongue for each metropolitan
area

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_mother_tidy = lang_wide.melt(
    id_vars=["category", "language"],
    var_name="region",
    value_name="mother_tongue",
)
lang_mother_tidy
```

```{note}
In the code above, the call to the
`melt` function is split across several lines. Recall from
{numref}`Chapter %s <intro>` that this is allowed in
certain cases. For example, when calling a function as above, the input
arguments are between parentheses `()` and Python knows to keep reading on
the next line. Each line ends with a comma `,` making it easier to read.
Splitting long lines like this across multiple lines is encouraged
as it helps significantly with code readability. Generally speaking, you should
limit each line of code to about 80 characters.
```

The data above is now tidy because all three criteria for tidy data have now
been met:

1.  All the variables (`category`, `language`, `region` and `mother_tongue`) are
    now their own columns in the data frame.
2.  Each observation, i.e., each `category`, `language`, `region`, and count of
    Canadians where that language is the mother tongue, are in a single row.
3.  Each value is a single cell, i.e., its row, column position in the data
    frame is not shared with another value.

+++

(pivot-wider)=
### Tidying up: going from long to wide using `pivot`

```{index} DataFrame; pivot
```

Suppose we have observations spread across multiple rows rather than in a single
row. For example, in {numref}`fig:long-to-wide`, the table on the left is in an
untidy, long format because the `count` column contains three variables
(population, commuter, and incorporated count) and information about each observation
(here, population, commuter, and incorporated counts for a region) is split across three rows.
Remember: one of the criteria for tidy data
is that each observation must be in a single row.

Using data in this format&mdash;where two or more variables are mixed together
in a single column&mdash;makes it harder to apply many usual `pandas` functions.
For example, finding the maximum number of commuters
would require an additional step of filtering for the commuter values
before the maximum can be computed.
In comparison, if the data were tidy,
all we would have to do is compute the maximum value for the commuter column.
To reshape this untidy data set to a tidy (and in this case, wider) format,
we need to create columns called "population", "commuters", and "incorporated."
This is illustrated in the right table of {numref}`fig:long-to-wide`.

+++ {"tags": []}

```{figure} img/wrangling/pivot_functions.002.png
:name: fig:long-to-wide
:figclass: figure

Going from long to wide data.
```

+++

To tidy this type of data in Python, we can use the `pivot` function.
The `pivot` function generally increases the number of columns (widens)
and decreases the number of rows in a data set.
To learn how to use `pivot`,
we will work through an example
with the `region_lang_top5_cities_long.csv` data set.
This data set contains the number of Canadians reporting
the primary language at home and work for five
major cities (Toronto, Montréal, Vancouver, Calgary, and Edmonton).

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_long = pd.read_csv("data/region_lang_top5_cities_long.csv")
lang_long
```

What makes the data set shown above untidy?
In this example, each observation is a language in a region.
However, each observation is split across multiple rows:
one where the count for `most_at_home` is recorded,
and the other where the count for `most_at_work` is recorded.
Suppose the goal with this data was to
visualize the relationship between the number of
Canadians reporting their primary language at home and work.
Doing that would be difficult with this data in its current form,
since these two variables are stored in the same column.
{numref}`fig:img-pivot-wider-table` shows how this data
will be tidied using the `pivot` function.

+++ {"tags": []}

```{figure} img/wrangling/pandas_pivot_long-wide.png
:name: fig:img-pivot-wider-table
:figclass: figure

Going from long to wide with the `pivot` function.
```

+++

{numref}`fig:img-pivot-wider` details the arguments that we need to specify in the `pivot` function.

+++ {"tags": []}

```{figure} img/wrangling/pandas_pivot_args_labels.png
:name: fig:img-pivot-wider
:figclass: figure

Syntax for the `pivot` function.
```

+++

We will apply the function as detailed in {numref}`fig:img-pivot-wider`, and then
rename the columns.

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_home_tidy = lang_long.pivot(
    index=["region", "category", "language"],
    columns=["type"],
    values=["count"]
).reset_index()

lang_home_tidy.columns = [
    "region",
    "category",
    "language",
    "most_at_home",
    "most_at_work",
]
lang_home_tidy
```

```{index} DataFrame; reset_index
```

In the first step, note that we added a call to `reset_index`. When `pivot` is called with
multiple column names passed to the `index`, those entries become the "name" of each row that
would be used when you filter rows with `[]` or `loc` rather than just simple numbers. This
can be confusing... What `reset_index` does is sets us back with the usual expected behaviour
where each row is "named" with an integer. This is a subtle point, but the main take-away is that
when you call `pivot`, it is a good idea to call `reset_index` afterwards.

The second operation we applied is to rename the columns. When we perform the `pivot`
operation, it keeps the original column name `"count"` and adds the `"type"` as a second column name.
Having two names for a column can be confusing! So we rename giving each column only one name.

```{index} DataFrame; info
```

We can print out some useful information about our data frame using the `info` function.
In the first row it tells us the `type` of `lang_home_tidy` (it is a `pandas` `DataFrame`). The second
row tells us how many rows there are: 1070, and to index those rows, you can use numbers between
0 and 1069 (remember that Python starts counting at 0!). Next, there is a print out about the data
colums. Here there are 5 columns total. The little table it prints out tells you the name of each
column, the number of non-null values (e.g. the number of entries that are not missing values), and
the type of the entries. Finally the last two rows summarize the types of each column and how much
memory the data frame is using on your computer.
```{code-cell} ipython3
lang_home_tidy.info()
```

The data is now tidy! We can go through the three criteria again to check
that this data is a tidy data set.

1.  All the statistical variables are their own columns in the data frame (i.e.,
    `most_at_home`, and `most_at_work` have been separated into their own
    columns in the data frame).
2.  Each observation, (i.e., each language in a region) is in a single row.
3.  Each value is a single cell (i.e., its row, column position in the data
    frame is not shared with another value).

You might notice that we have the same number of columns in the tidy data set as
we did in the messy one. Therefore `pivot` didn't really "widen" the data.
This is just because the original `type` column only had
two categories in it. If it had more than two, `pivot` would have created
more columns, and we would see the data set "widen."


+++

(str-split)=
### Tidying up: using `str.split` to deal with multiple separators

```{index} Series; str.split, separator
```

```{index} see: delimiter; separator
```

Data are also not considered tidy when multiple values are stored in the same
cell. The data set we show below is even messier than the ones we dealt with
above: the `Toronto`, `Montréal`, `Vancouver`, `Calgary`, and `Edmonton` columns
contain the number of Canadians reporting their primary language at home and
work in one column separated by the separator (`/`). The column names are the
values of a variable, *and* each value does not have its own cell! To turn this
messy data into tidy data, we'll have to fix these issues.

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_messy = pd.read_csv("data/region_lang_top5_cities_messy.csv")
lang_messy
```

First we’ll use `melt` to create two columns, `region` and `value`,
similar to what we did previously.
The new `region` columns will contain the region names,
and the new column `value` will be a temporary holding place for the
data that we need to further separate, i.e., the
number of Canadians reporting their primary language at home and work.

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_messy_longer = lang_messy.melt(
    id_vars=["category", "language"],
    var_name="region",
    value_name="value",
)

lang_messy_longer
```

Next we'll split the `value` column into two columns.
In basic Python, if we wanted to split the string `"50/0"` into two numbers `["50", "0"]`
we would use the  `split` method on the string, and specify that the split should be made
on the slash character `"/"`.
```{code-cell} ipython3
"50/0".split("/")
```

The `pandas` package provides similar functions that we can access
by using the `str` method. So to split all of the entries for an entire
column in a data frame, we will use the `str.split` method.
The output of this method is a data frame with two columns:
one containing only the counts of Canadians
that speak each language most at home,
and the other containing only the counts of Canadians
that speak each language most at work for each region.
We drop the no-longer-needed `value` column from the `lang_messy_longer`
data frame, and then assign the two columns from `str.split` to two new columns.
{numref}`fig:img-separate`
outlines what we need to specify to use `str.split`.

+++ {"tags": []}

```{figure} img/wrangling/str-split_args_labels.png
:name: fig:img-separate
:figclass: figure

Syntax for the `str.split` function.
```

```{code-cell} ipython3
tidy_lang = lang_messy_longer.drop(columns=["value"])
tidy_lang[["most_at_home", "most_at_work"]] = lang_messy_longer["value"].str.split("/", expand=True)
tidy_lang
```

Is this data set now tidy? If we recall the three criteria for tidy data:

  - each row is a single observation,
  - each column is a single variable, and
  - each value is a single cell.

We can see that this data now satisfies all three criteria, making it easier to
analyze. But we aren't done yet! Although we can't see it in the data frame above, all of the variables are actually
`object` data types. We can check this using the `info` method.
```{code-cell} ipython3
tidy_lang.info()
```

Object columns in `pandas` data frames are columns of strings or columns with
mixed types. In the previous example in {numref}`pivot-wider`, the
`most_at_home` and `most_at_work` variables were `int64` (integer), which is a type of numeric data.
This change is due to the separator (`/`) when we read in this messy data set.
Python read these columns in as string types, and by default, `str.split` will
return columns with the `object` data type.

It makes sense for `region`, `category`, and `language` to be stored as an
`object` type since they hold categorical values. However, suppose we want to apply any functions that treat the
`most_at_home` and `most_at_work` columns as a number (e.g., finding rows
above a numeric threshold of a column).
That won't be possible if the variable is stored as an `object`.
Fortunately, the `astype` method from `pandas` provides a natural way to fix problems
like this: it will convert the column to a selected data type. In this case, we choose the `int`
data type to indicate that these variables contain integer counts. Note that below
we *assign* the new numerical series to the `most_at_home` and `most_at_work` columns
in `tidy_lang`; we have seen this syntax before in {numref}`ch1-adding-modifying`,
and we will discuss it in more depth later in this chapter in {numref}`pandas-assign`.

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang["most_at_home"] = tidy_lang["most_at_home"].astype("int")
tidy_lang["most_at_work"] = tidy_lang["most_at_work"].astype("int")
tidy_lang
```

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

