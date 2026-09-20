+++

### Extracting columns by name

Recall that if we provide a list of column names, `[]` returns the subset of columns with those names as a data frame.
Suppose we wanted to select the columns `language`, `region`,
`most_at_home` and `most_at_work` from the `tidy_lang` data set. Using what we
learned in {numref}`Chapter %s <intro>`, we can pass all of these column
names into the square brackets.

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang[["language", "region", "most_at_home", "most_at_work"]]
```

Likewise,
if we pass a list containing a single column name,
a data frame with this column will be returned.

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang[["language"]]
```

When we need to extract only a single column,
we can also pass the column name as a string rather than a list.
The returned data type will now be a series.
Throughout this textbook,
we will mostly extract single columns this way,
but we will point out a few occasions
where it is advantageous to extract single columns as data frames.

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang["language"]
```


### Extracting rows that have a certain value with `==`

```{index} logical operator; equivalency (==) 
```

```{index} see: ==; logical operator
```

Suppose we are only interested in the subset of rows in `tidy_lang` corresponding to the
official languages of Canada (English and French).
We can extract these rows by using the *equivalency operator* (`==`)
to compare the values of the `category` column
with the value `"Official languages"`.
With these arguments, `[]` returns a data frame with all the columns
of the input data frame
but only the rows we asked for in the logical statement, i.e.,
those where the `category` column holds the value `"Official languages"`.
We name this data frame `official_langs`.

```{code-cell} ipython3
:tags: ["output_scroll"]
official_langs = tidy_lang[tidy_lang["category"] == "Official languages"]
official_langs
```

### Extracting rows that do not have a certain value with `!=`

```{index} logical operator; inequivalency (!=) 
```

```{index} see: !=; logical operator
```

What if we want all the other language categories in the data set *except* for
those in the `"Official languages"` category? We can accomplish this with the `!=`
operator, which means "not equal to". So if we want to find all the rows
where the `category` does *not* equal `"Official languages"` we write the code
below.

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang[tidy_lang["category"] != "Official languages"]
```

(filter-and)=
### Extracting rows satisfying multiple conditions using `&`

```{index} logical operator; and (&)
```

```{index} see: &; logical operator
```

Suppose now we want to look at only the rows
for the French language in Montréal.
To do this, we need to filter the data set
to find rows that satisfy multiple conditions simultaneously.
We can do this with the ampersand symbol (`&`), which
is interpreted by Python as "and".
We write the code as shown below to filter the `official_langs` data frame
to subset the rows where `region == "Montréal"`
*and* `language == "French"`.

```{code-cell} ipython3
tidy_lang[
  (tidy_lang["region"] == "Montréal") &
  (tidy_lang["language"] == "French")
]
```

+++ {"tags": []}

### Extracting rows satisfying at least one condition using `|`

```{index} logical operator; or (|)
```

```{index} see: |; logical operator
```

Suppose we were interested in only those rows corresponding to cities in Alberta
in the `official_langs` data set (Edmonton and Calgary).
We can't use `&` as we did above because `region`
cannot be both Edmonton *and* Calgary simultaneously.
Instead, we can use the vertical pipe (`|`) logical operator,
which gives us the cases where one condition *or*
another condition *or* both are satisfied.
In the code below, we ask Python to return the rows
where the `region` columns are equal to "Calgary" *or* "Edmonton".

```{code-cell} ipython3
official_langs[
    (official_langs["region"] == "Calgary") |
    (official_langs["region"] == "Edmonton")
]
```

### Extracting rows with values in a list using `isin`

```{index} logical operator; containment (isin) 
```

```{index} see: isin; logical operator
```

Next, suppose we want to see the populations of our five cities.
Let's read in the `region_data.csv` file
that comes from the 2016 Canadian census,
as it contains statistics for number of households, land area, population
and number of dwellings for different regions.

```{code-cell} ipython3
:tags: ["output_scroll"]
region_data = pd.read_csv("data/region_data.csv")
region_data
```

To get the population of the five cities
we can filter the data set using the `isin` method.
The `isin` method is used to see if an element belongs to a list.
Here we are filtering for rows where the value in the `region` column
matches any of the five cities we are intersted in: Toronto, Montréal,
Vancouver, Calgary, and Edmonton.

```{code-cell} ipython3
city_names = ["Toronto", "Montréal", "Vancouver", "Calgary", "Edmonton"]
five_cities = region_data[region_data["region"].isin(city_names)]
five_cities
```

```{note}
What's the difference between `==` and `isin`? Suppose we have two
Series, `seriesA` and `seriesB`. If you type `seriesA == seriesB` into Python it
will compare the series element by element. Python checks if the first element of
`seriesA` equals the first element of `seriesB`, the second element of
`seriesA` equals the second element of `seriesB`, and so on. On the other hand,
`seriesA.isin(seriesB)` compares the first element of `seriesA` to all the
elements in `seriesB`. Then the second element of `seriesA` is compared
to all the elements in `seriesB`, and so on. Notice the difference between `==` and
`isin` in the example below.
```

```{code-cell} ipython3
pd.Series(["Vancouver", "Toronto"]) == pd.Series(["Toronto", "Vancouver"])
```

```{code-cell} ipython3
pd.Series(["Vancouver", "Toronto"]).isin(pd.Series(["Toronto", "Vancouver"]))
```

### Extracting rows above or below a threshold using `>` and `<`

```{index} logical operator; greater than (> and >=), logical operator; less than (< and <=)
```

```{index} see: >; logical operator
```

```{index} see: >=; logical operator
```

```{index} see: <; logical operator
```

```{index} see: <=; logical operator
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("census_popn", "{0:,.0f}".format(35151728))
glue("most_french", "{0:,.0f}".format(2669195))
```

We saw in {numref}`filter-and` that
{glue:text}`most_french` people reported
speaking French in Montréal as their primary language at home.
If we are interested in finding the official languages in regions
with higher numbers of people who speak it as their primary language at home
compared to French in Montréal, then we can use `[]` to obtain rows
where the value of `most_at_home` is greater than
{glue:text}`most_french`. We use the `>` symbol to look for values *above* a threshold,
and the `<` symbol to look for values *below* a threshold. The `>=` and `<=`
symbols similarly look for *equal to or above* a threshold and *equal to or below* a threshold.

```{code-cell} ipython3
official_langs[official_langs["most_at_home"] > 2669195]
```

This operation returns a data frame with only one row, indicating that when
considering the official languages,
only English in Toronto is reported by more people
as their primary language at home
than French in Montréal according to the 2016 Canadian census.

### Extracting rows using `query`

```{index} logical statement; query
```

You can also extract rows above, below, equal or not-equal to a threshold using the
`query` method. For example the following gives us the same result as when we used
`official_langs[official_langs["most_at_home"] > 2669195]`.

```{code-cell} ipython3
official_langs.query("most_at_home > 2669195")
```

The query (criteria we are using to select values) is input as a string. The `query` method
is less often used than the earlier approaches we introduced, but it can come in handy
to make long chains of filtering operations a bit easier to read.

(loc-iloc)=
## Using `loc[]` to filter rows and select columns

```{index} DataFrame; loc[]
```

The `[]` operation is only used when you want to either filter rows **or** select columns;
it cannot be used to do both operations at the same time. This is where `loc[]`
comes in. For the first example, recall `loc[]` from {numref}`Chapter %s <intro>`,
which lets us create a subset of the rows and columns in the `tidy_lang` data frame.
In the first argument to `loc[]`, we specify a logical statement that
filters the rows to only those pertaining to the Toronto region,
and the second argument specifies a list of columns to keep by name.

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[
    tidy_lang["region"] == "Toronto",
    ["language", "region", "most_at_home", "most_at_work"]
]
```

In addition to simultaneous subsetting of rows and columns, `loc[]` has two
more special capabilities beyond those of `[]`. First, `loc[]` has the ability to specify *ranges* of rows and columns.
For example, note that the list of columns `language`, `region`, `most_at_home`, `most_at_work`
corresponds to the *range* of columns from `language` to `most_at_work`.
Rather than explicitly listing all of the column names as we did above,
we can ask for the range of columns `"language":"most_at_work"`; the `:`-syntax
denotes a range, and is supported by the `loc[]` function, but not by `[]`.

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[
    tidy_lang["region"] == "Toronto",
    "language":"most_at_work"
]
```

We can pass `:` by itself&mdash;without anything before or after&mdash;to denote that we want to retrieve
everything. For example, to obtain a subset of all rows and only those columns ranging from `language` to `most_at_work`,
we could use the following expression.

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[:, "language":"most_at_work"]
```

We can also omit the beginning or end of the `:` range expression to denote
that we want "everything up to" or "everything after" an element. For example,
if we want all of the columns including and after `language`, we can write the expression:

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[:, "language":]
```
By not putting anything after the `:`, Python reads this as "from `language` until the last column".
Similarly, we can specify that we want everything up to and including `language` by writing
the expression:

```{code-cell} ipython3
:tags: ["output_scroll"]
tidy_lang.loc[:, :"language"]
```

By not putting anything before the `:`, Python reads this as "from the first column until `language`."
Although the notation for selecting a range using `:` is convenient because less code is required,
it must be used carefully. If you were to re-order columns or add a column to the data frame, the
output would change. Using a list is more explicit and less prone to potential confusion, but sometimes
involves a lot more typing.

The second special capability of `.loc[]` over `[]` is that it enables *selecting columns* using
logical statements. The `[]` operator can only use logical statements to filter rows; `.loc[]` can do both!
For example, let's say we wanted only to select the
columns `most_at_home` and `most_at_work`. We could then use the `.str.startswith` method
to choose only the columns that start with the word "most".
The `str.startswith` expression returns a list of `True` or `False` values
corresponding to the column names that start with the desired characters.

```{code-cell} ipython3
tidy_lang.loc[:, tidy_lang.columns.str.startswith("most")]
```

```{index} Series; str.contains
```

We could also have chosen the columns containing an underscore `_` by using the
`.str.contains("_")`, since we notice
the columns we want contain underscores and the others don't.

```{code-cell} ipython3
tidy_lang.loc[:, tidy_lang.columns.str.contains("_")]
```

## Using `iloc[]` to extract rows and columns by position
```{index} DataFrame; iloc[], column range
```
Another approach for selecting rows and columns is to use `iloc[]`,
which provides the ability to index with the position rather than the label of the columns.
For example, the column labels of the `tidy_lang` data frame are
`["category", "language", "region", "most_at_home", "most_at_work"]`.
Using `iloc[]`, you can ask for the `language` column by requesting the
column at index `1` (remember that Python starts counting at `0`, so the second column `"language"`
has index `1`!).

```{code-cell} ipython3
tidy_lang.iloc[:, 1]
```

You can also ask for multiple columns.
We pass `1:` after the comma
indicating we want columns after and including index 1 (*i.e.* `language`).

```{code-cell} ipython3
tidy_lang.iloc[:, 1:]
```

We can also use `iloc[]` to select ranges of rows, or simultaneously select ranges of rows and columns, using a similar syntax.
For example, to select the first five rows and columns after and including index 1, we could use the following:

```{code-cell} ipython3
tidy_lang.iloc[:5, 1:]
```

Note that the `iloc[]` method is not commonly used, and must be used with care.
For example, it is easy to
accidentally put in the wrong integer index! If you did not correctly remember
that the `language` column was index `1`, and used `2` instead, your code
might end up having a bug that is quite hard to track down.

```{index} Series; str.startswith
```

+++ {"tags": []}

## Aggregating data

+++

### Calculating summary statistics on individual columns

```{index} summarize
```

As a part of many data analyses, we need to calculate a summary value for the
data (a *summary statistic*).
Examples of summary statistics we might want to calculate
are the number of observations, the average/mean value for a column,
the minimum value, etc.
Oftentimes,
this summary statistic is calculated from the values in a data frame column,
or columns, as shown in {numref}`fig:summarize`.

+++ {"tags": []}

```{figure} img/wrangling/summarize.001.png
:name: fig:summarize
:figclass: figure

Calculating summary statistics on one or more column(s) in `pandas` generally
creates a series or data frame containing the summary statistic(s) for each column
being summarized. The darker, top row of each table represents column headers.
```

