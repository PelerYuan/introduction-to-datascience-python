
(wrangling)=
# Cleaning and wrangling data

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
import pandas as pd
pd.set_option("display.max_rows", 20)
```

## Overview

This chapter is centered around defining tidy data&mdash;a data format that is
suitable for analysis&mdash;and the tools needed to transform raw data into this
format. This will be presented in the context of a real-world data science
application, providing more practice working through a whole case study.

+++

## Chapter learning objectives

By the end of the chapter, readers will be able to do the following:

- Define the term "tidy data".
- Discuss the advantages of storing data in a tidy data format.
- Define what series and data frames are in Python, and describe how they relate to
  each other.
- Describe the common types of data in Python and their uses.
- Use the following functions for their intended data wrangling tasks:
    - `melt`
    - `pivot`
    - `reset_index`
    - `str.split`
    - `agg`
    - `assign` and regular column assignment
    - `groupby`
    - `merge`
- Use the following operators for their intended data wrangling tasks:
    - `==`, `!=`, `<`, `>`, `<=`, and `>=`
    - `isin`
    - `&` and `|`
    - `[]`, `loc[]`, and `iloc[]`

## Data frames and series

In {numref}`Chapters %s <intro>` and {numref}`%s <reading>`, *data frames* were the focus:
we learned how to import data into Python as a data frame, and perform basic operations on data frames in Python.
In the remainder of this book, this pattern continues. The vast majority of tools we use will require
that data are represented as a `pandas` **data frame** in Python. Therefore, in this section,
we will dig more deeply into what data frames are and how they are represented in Python.
This knowledge will be helpful in effectively utilizing these objects in our data analyses.

+++

### What is a data frame?

```{index} data frame; definition
```

```{index} see: data frame; DataFrame
```

```{index} DataFrame
```

A data frame is a table-like structure for storing data in Python. Data frames are
important to learn about because most data that you will encounter in practice
can be naturally stored as a table.  In order to define data frames precisely,
we need to introduce a few technical terms:

```{index} variable, observation, value
```

- **variable:** a characteristic, number, or quantity that can be measured.
- **observation:** all of the measurements for a given entity.
- **value:** a single measurement of a single variable for a given entity.

Given these definitions, a **data frame** is a tabular data structure in Python
that is designed to store observations, variables, and their values.
Most commonly, each column in a data frame corresponds to a variable,
and each row corresponds to an observation. For example,
{numref}`fig:02-obs` displays a data set of city populations. Here, the variables
are "region, year, population"; each of these are properties that can be
collected or measured.  The first observation is "Toronto, 2016, 2235145";
these are the values that the three variables take for the first entity in the
data set. There are 13 entities in the data set in total, corresponding to the
13 rows in {numref}`fig:02-obs`.

+++

```{figure} img/wrangling/data_frame_slides_cdn.004.png
:name: fig:02-obs
:figclass: figure

A data frame storing data regarding the population of various regions in Canada. In this example data frame, the row that corresponds to the observation for the city of Vancouver is colored yellow, and the column that corresponds to the population variable is colored blue.
```

### What is a series?

```{index} Series 
```

In Python, `pandas` **series** are objects that can contain one or more elements (like a list).
They are a single column, are ordered, can be indexed, and can contain any data type.
The `pandas` package uses `Series` objects to represent the columns in a data frame.
`Series` can contain a mix of data types, but it is good practice to only include a single type in a series
because all observations of one variable should be the same type.
Python has several different basic data types, as shown in
{numref}`tab:datatype-table`. You can create a `pandas` series using the
`pd.Series()` function.  For example, to create the series `region` as shown
in {numref}`fig:02-series`, you can write the following.

```{code-cell} ipython3
import pandas as pd

region = pd.Series(["Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa"])
region
```

+++ {"tags": []}

```{figure} img/wrangling/pandas_dataframe_series.png
:name: fig:02-series
:figclass: figure

Example of a `pandas` series whose type is string.
```

```{index} data types; string (str), data types; integer (int), data types; floating point number (float), data types; boolean (bool), data types; NoneType (none)
```

```{index} see: str; data types
```

```{index} see: int; data types
```

```{index} see: float; data types
```

```{index} see: bool; data types
```

```{index} see: NoneType; data types
```

```{table} Basic data types in Python
:name: tab:datatype-table
| Data type             | Abbreviation | Description                                   | Example                                    |
| :-------------------- | :----------- | :-------------------------------------------- | :----------------------------------------- |
| integer               | `int`        | positive/negative/zero whole numbers          | `42`                                       |
| floating point number | `float`      | real number in decimal form                   | `3.14159`                                  |
| boolean               | `bool`       | true or false                                 | `True`                                     |
| string                | `str`        | text                                          | `"Hello World"`                            |
| none                  | `NoneType`   | represents no value                           | `None`                                     |
```

+++

It is important in Python to make sure you represent your data with the correct type.
Many of the `pandas` functions we use in this book treat
the various data types differently. You should use `int` and `float` types
to represent numbers and perform arithmetic. The `int` type is for integers that have no decimal point,
while the `float` type is for numbers that have a decimal point.
The `bool` type are boolean variables that can only take on one of two values: `True` or `False`.
The `string` type is used to represent data that should
be thought of as "text", such as words, names, paths, URLs, and more.
A `NoneType` is a special type in Python that is used to indicate no value; this can occur,
for example, when you have missing data.
There are other basic data types in Python, but we will generally
not use these in this textbook.


### What does this have to do with data frames?

+++

```{index} data frame; definition
```

A data frame is really just a collection of series that are stuck together,
where each series corresponds to one column and all must have the same length.
But not all columns in a data frame need to be of the same type.
{numref}`fig:02-dataframe` shows a data frame where
the columns are series of different types. But each element *within*
one column should usually be the same type, since the values for a single variable
are usually all of the same type. For example, if the variable is the name of a city,
that name should be a string, whereas if the variable is a year, that should be an
integer. So even though series let you put different types in them, it is most common
(and good practice!) to have just one type per column.

+++ {"tags": []}

```{figure} img/wrangling/pandas_dataframe_series-3.png
:name: fig:02-dataframe
:figclass: figure

Data frame and series types.
```


```{index} type
```

```{note}
You can use the function `type` on a data object.
For example we can check the class of the Canadian languages data set,
`can_lang`, we worked with in the previous chapters and we see it is a `pandas.core.frame.DataFrame`.
```


```{code-cell} ipython3
can_lang = pd.read_csv("data/can_lang.csv")
type(can_lang)
```

### Data structures in Python

The `Series` and `DataFrame` types are *data structures* in Python, which
are core to most data analyses.
The functions from `pandas` that we use often give us back a `DataFrame`
or a `Series` depending on the operation. Because
`Series` are essentially simple `DataFrames`, we will refer
to both `DataFrames` and `Series` as "data frames" in the text.
There are other types that represent data structures in Python.
We summarize the most common ones in {numref}`tab:datastruc-table`.

```{index} data structures; list, data structures; set, data structures; dictionary (dict), data structures; tuple
```

```{index} see: dict; data structures
```

```{table} Basic data structures in Python
:name: tab:datastruc-table
| Data Structure | Description |
| ---            | ----------- |
| list | An ordered collection of values that can store multiple data types at once. |
| dict | A labeled data structure where `keys` are paired with `values` |
| Series | An ordered collection of values *with labels* that can store multiple data types at once. |
| DataFrame | A labeled data structure with `Series` columns of potentially different types. |
```

A `list` is an ordered collection of values. To create a list, we put the contents of the list in between
square brackets `[]`, where each item of the list is separated by a comma. A `list` can contain values
of different types. The example below contains six `str` entries.

```{code-cell} ipython3
cities = ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Winnipeg"]
cities
```
A list can directly be converted to a pandas `Series`.
```{code-cell} ipython3
cities_series = pd.Series(cities)
cities_series
```

A `dict`, or dictionary, contains pairs of "keys" and "values."
You use a key to look up its corresponding value. Dictionaries are created
using curly brackets `{}`. Each entry starts with the
key on the left, followed by a colon symbol `:`, and then the value.
A dictionary can have multiple key-value pairs, each separted by a comma.
Keys can take a wide variety of types (`int` and `str` are commonly used), and values can take any type;
the key-value pairs in a dictionary can all be of different types, too.
 In the example below,
we create a dictionary that has two keys: `"cities"` and `"population"`.
The values associated with each are lists.

```{code-cell} ipython3
population_in_2016 = {
  "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Winnipeg"],
  "population": [2235145, 1027613, 1823281, 544870, 571146, 321484]
}
population_in_2016
```

A dictionary can be converted to a data frame. Keys
become the column names, and the values become the entries in
those columns. Dictionaries on their own are quite simple objects; it is preferable to work with a data frame
because then we have access to the built-in functionality in
`pandas` (e.g. `loc[]`, `[]`, and many functions that we will discuss in the upcoming sections)!

```{code-cell} ipython3
population_in_2016_df = pd.DataFrame(population_in_2016)
population_in_2016_df
```

Of course, there is no need to name the dictionary separately before passing it to
`pd.DataFrame`; we can instead construct the dictionary right inside the call.
This is often the most convenient way to create a new data frame.

```{code-cell} ipython3
population_in_2016_df = pd.DataFrame({
  "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Winnipeg"],
  "population": [2235145, 1027613, 1823281, 544870, 571146, 321484]
})
population_in_2016_df
```

+++

## Tidy data

```{index} tidy data; definition
```

There are many ways a tabular data set can be organized.  The data frames we
have looked at so far have all been using the **tidy data** format of
organization.  This chapter will focus on introducing the tidy data format and
how to make your raw (and likely messy) data tidy. A tidy data frame satisfies
the following three criteria {cite:p}`wickham2014tidy`:

  - each row is a single observation,
  - each column is a single variable, and
  - each value is a single cell (i.e., its entry in the data
    frame is not shared with another value).

{numref}`fig:02-tidy-image` demonstrates a tidy data set that satisfies these
three criteria.

+++ {"tags": []}

```{figure} img/wrangling/tidy_data.001.png
:name: fig:02-tidy-image
:figclass: figure

Tidy data satisfies three criteria.
```

+++

```{index} tidy data; arguments for
```

There are many good reasons for making sure your data are tidy as a first step in your analysis.
The most important is that it is a single, consistent format that nearly every function
in the `pandas` recognizes. No matter what the variables and observations
in your data represent, as long as the data frame
is tidy, you can manipulate it, plot it, and analyze it using the same tools.
If your data is *not* tidy, you will have to write special bespoke code
in your analysis that will not only be error-prone, but hard for others to understand.
Beyond making your analysis more accessible to others and less error-prone, tidy data
is also typically easy for humans to interpret. Given these benefits,
it is well worth spending the time to get your data into a tidy format
upfront. Fortunately, there are many well-designed `pandas` data
cleaning/wrangling tools to help you easily tidy your data. Let's explore them
below!

```{note}
Is there only one shape for tidy data for a given data set? Not
necessarily! It depends on the statistical question you are asking and what
the variables are for that question. For tidy data, each variable should be
its own column. So, just as it's essential to match your statistical question
with the appropriate data analysis tool, it's important to match your
statistical question with the appropriate variables and ensure they are
represented as individual columns to make the data tidy.
```

+++

### Tidying up: going from wide to long using `melt`

```{index} DataFrame; melt
```

One task that is commonly performed to get data into a tidy format
is to combine values that are stored in separate columns,
but are really part of the same variable, into one.
Data is often stored this way
because this format is sometimes more intuitive for human readability
and understanding, and humans create data sets.
In {numref}`fig:02-wide-to-long`,
the table on the left is in an untidy, "wide" format because the year values
(2006, 2011, 2016) are stored as column names.
And as a consequence,
the values for population for the various cities
over these years are also split across several columns.

For humans, this table is easy to read, which is why you will often find data
stored in this wide format.  However, this format is difficult to work with
when performing data visualization or statistical analysis using Python.  For
example, if we wanted to find the latest year it would be challenging because
the year values are stored as column names instead of as values in a single
column.  So before we could apply a function to find the latest year (for
example, by using `max`), we would have to first extract the column names
to get them as a list and then apply a function to extract the latest year.
The problem only gets worse if you would like to find the value for the
population for a given region for the latest year.  Both of these tasks are
greatly simplified once the data is tidied.

Another problem with data in this format is that we don't know what the
numbers under each year actually represent. Do those numbers represent
population size? Land area? It's not clear.
To solve both of these problems,
we can reshape this data set to a tidy data format
by creating a column called "year" and a column called
"population." This transformation&mdash;which makes the data
"longer"&mdash;is shown as the right table in
{numref}`fig:02-wide-to-long`. Note that the number of entries in our data frame
can change in this transformation. The "untidy" data has 5 rows and 3 columns for
a total of 15 entries, whereas the "tidy" data on the right has 15 rows and 2 columns
for a total of 30 entries.

+++ {"tags": []}

```{figure} img/wrangling/pivot_functions.001.png
:name: fig:02-wide-to-long
:figclass: figure



Melting data from a wide to long data format.
```

+++

```{index} Canadian languages
```

We can achieve this effect in Python using the `melt` function from the `pandas` package.
The `melt` function combines columns,
and is usually used during tidying data
when we need to make the data frame longer and narrower.
To learn how to use `melt`, we will work through an example with the
`region_lang_top5_cities_wide.csv` data set. This data set contains the
counts of how many Canadians cited each language as their mother tongue for five
major Canadian cities (Toronto, Montréal, Vancouver, Calgary, and Edmonton) from
the 2016 Canadian census.
To get started,
we will use `pd.read_csv` to load the (untidy) data.

```{code-cell} ipython3
:tags: ["output_scroll"]
lang_wide = pd.read_csv("data/region_lang_top5_cities_wide.csv")
lang_wide
```

What is wrong with the untidy format above?
The table on the left in {numref}`fig:img-pivot-longer-with-table`
represents the data in the "wide" (messy) format.
From a data analysis perspective, this format is not ideal because the values of
the variable *region* (Toronto, Montréal, Vancouver, Calgary, and Edmonton)
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

