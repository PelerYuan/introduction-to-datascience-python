## Modifying and adding columns


```{index} DataFrame; [], column assignment, assign
```

When we compute summary statistics or apply functions,
a new data frame or series is created. But what if we want to append that information
to an existing data frame? For example, say we wanted to compute the
maximum value in each row of the `region_lang_nums` data frame,
and to append that as an additional column of the `region_lang` data frame.
In this case, we have two options: we can either  create a new column within the `region_lang` data
frame itself, or create an entirely new data frame
with the `assign` method. The first option we have seen already in earlier chapters, and is
the more commonly used pattern in practice:
```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang["maximum"] = region_lang_nums.max(axis=1)
region_lang
```
You can see above that the `region_lang` data frame now has an additional column named `maximum`.
The `maximum` column contains
the maximum value between `mother_tongue`,
`most_at_home`, `most_at_work` and `lang_known` for each language
and region, just as we specified!

To instead create an entirely new data frame, we can use the `assign` method and specify one argument for each column we want to create.
In this case we want to create one new column named `maximum`, so the argument
to `assign` begins with `maximum= `.
Then after the `=`, we specify what the contents of that new column
should be. In this case we use `max` just as we did previously to give us the maximum values.
Remember to specify `axis=1` in the `max` method so that we compute the row-wise maximum value.
```{code-cell} ipython3
:tags: ["output_scroll"]
region_lang.assign(
  maximum=region_lang_nums.max(axis=1)
)
```
This data frame looks just like the previous one, except that it is a copy of `region_lang`, not `region_lang` itself; making further
changes to this data frame will not impact the original `region_lang` data frame.


```{code-cell} ipython3
:tags: [remove-cell]

# remove maximum coln from region_lang
region_lang = region_lang.drop(columns=["maximum"])

# get english counts for toronto and glue
number_most_home = int(
    official_langs[
        (official_langs["language"] == "English") &
        (official_langs["region"] == "Toronto")
    ]["most_at_home"]
)

toronto_popn = int(region_data[region_data["region"] == "Toronto"]["population"])

glue("number_most_home", "{0:,.0f}".format(number_most_home))
glue("toronto_popn", "{0:,.0f}".format(toronto_popn))
glue("prop_eng_tor", "{0:.2f}".format(number_most_home / toronto_popn))
```

As another example, we might ask the question: "What proportion of
the population reported English as their primary language at home in the 2016 census?"
For example, in Toronto, {glue:text}`number_most_home` people reported
speaking English as their primary language at home, and the
population of Toronto was reported to be
{glue:text}`toronto_popn` people. So the proportion of people reporting English
as their primary language in Toronto in the 2016 census was {glue:text}`prop_eng_tor`.
How could we figure this out starting from the `region_lang` data frame?

First, we need to filter the `region_lang` data frame
so that we only keep the rows where the language is English.
We will also restrict our attention to the five major cities
in the `five_cities` data frame: Toronto, Montréal, Vancouver, Calgary, and Edmonton.
We will filter to keep only those rows pertaining to the English language
and pertaining to the five aforementioned cities. To combine these two logical statements
we will use the `&` symbol.
and with the `[]` operation,
 `"English"` as the `language` and filter the rows,
and name the new data frame `english_langs`.
```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang = region_lang[
    (region_lang["language"] == "English") &
    (region_lang["region"].isin(five_cities["region"]))
]
english_lang
```

Okay, now we have a data frame that pertains only to the English language
and the five cities mentioned earlier.
In order to compute the proportion of the population speaking English in each of these cities,
we need to add the population data from the `five_cities` data frame.
```{code-cell} ipython3
five_cities
```
The data frame above shows that the populations of the five cities in 2016 were
5928040 (Toronto), 4098927 (Montréal),  2463431 (Vancouver), 1392609 (Calgary), and 1321426 (Edmonton).
Next, we will add this information to a new data frame column called `city_pops`.
Once again, we will illustrate how to do this using both the `assign` method and regular column assignment.
We specify the new column name (`city_pops`) as the argument, followed by the equals symbol `=`,
and finally the data in the column.
Note that the order of the rows in the `english_lang` data frame is Montréal, Toronto, Calgary, Edmonton, Vancouver.
So we will create a column called `city_pops` where we list the populations of those cities in that
order, and add it to our data frame.
And remember that by default, like other `pandas` functions, `assign` does not
modify the original data frame directly, so the `english_lang` data frame is unchanged!
```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang.assign(
  city_pops=[4098927, 5928040, 1392609, 1321426, 2463431]
)
```

Instead of using the `assign` method we can directly modify the `english_lang` data frame using regular column assignment.
This would be a more natural choice in this particular case,
since the syntax is more convenient for simple column modifications and additions.
```{code-cell} ipython3
:tags: [remove-output]
english_lang["city_pops"] = [4098927, 5928040, 1392609, 1321426, 2463431]
english_lang
```
```{code-cell} ipython3
:tags: ["remove-input"]
print("""
/tmp/ipykernel_12/2654974267.py:1: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  english_lang["city_pops"] = [4098927, 5928040, 1392609, 1321426, 2463431]
""")
english_lang
```

```{index} SettingWithCopyWarning
```

Wait a moment...what is that warning message? It seems to suggest that something went wrong, but
if we inspect the `english_lang` data frame above, it looks like the city populations were added
just fine! As it turns out, this is caused by the earlier filtering we did from `region_lang` to
produce the original `english_lang`. The details are a little bit technical, but
`pandas` sometimes does not like it when you subset a data frame using `[]` or `loc[]` followed by
column assignment. For the purposes of your own data analysis, if you ever see a `SettingWithCopyWarning`, just make sure
to double check that the result of your column assignment looks the way you expect it to before proceeding.
For the rest of the book, we will silence that warning to help with readability.
```{code-cell} ipython3
:tags: [remove-cell]
# suppress for the rest of this chapter
pd.options.mode.chained_assignment = None
```

```{index} DataFrame; merge
```

```{note}
Inserting the data column `[4098927, 5928040, ...]` manually as we did above is generally very error-prone and is not recommended.
We do it here to demonstrate another usage of `assign` and regular column assignment.
But in more advanced data wrangling,
one would solve this problem in a less error-prone way using
the `merge` function, which lets you combine two data frames. We will show you an
example using `merge` at the end of the chapter!
```

Now we have a new column with the population for each city. Finally, we can convert all the numerical
columns to proportions of people who speak English by taking the ratio of all the numerical columns
with `city_pops`. Let's modify the `english_lang` column directly; in this case
we can just assign directly to the data frame.
This is similar to what we did in {numref}`str-split`,
when we first read in the `"region_lang_top5_cities_messy.csv"` data and we needed to convert a few
of the variables to numeric types. Here we assign to a range of columns simultaneously using `loc[]`.
Note that it is again possible to instead use the `assign` function to produce a new data
frame when modifying existing columns, although this is not commonly done.
Note also that we use the `div` method with the argument `axis=0` to divide a range of columns in a data frame
by the values in a single column&mdash;the basic division symbol `/` won't work in this case.

```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang.loc[:, "mother_tongue":"lang_known"] = english_lang.loc[
    :,
    "mother_tongue":"lang_known"
    ].div(english_lang["city_pops"], axis=0)
english_lang
```

+++

## Using `merge` to combine data frames

```{index} DataFrame; merge
```

Let's return to the situation right before we added the city populations
of Toronto, Montréal, Vancouver, Calgary, and Edmonton to the `english_lang` data frame. Before adding the new column, we had filtered
`region_lang` to create the `english_lang` data frame containing only English speakers in the five cities
of interest.
```{code-cell} ipython3
:tags: ["remove-cell"]
english_lang = region_lang[
    (region_lang["language"] == "English") &
    (region_lang["region"].isin(five_cities["region"]))
]
```

```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang
```
We then added the populations of these cities as a column
(Toronto: 5928040, Montréal: 4098927, Vancouver: 2463431,
Calgary: 1392609, and Edmonton: 1321426). We had to be careful to add those populations in the
right order; this is an error-prone process. An alternative approach, that we demonstrate here
is to (1) create a new data frame with the city names and populations, and
(2) use `merge` to combine the two data frames, recognizing that the "regions" are the same.

We create a new data frame by calling `pd.DataFrame` with a dictionary
as its argument. The dictionary associates each column name in the data frame to be created
with a list of entries. Here we list city names in a column called `"region"`
and their populations in a column called `"population"`.
```{code-cell} ipython3
city_populations = pd.DataFrame({
  "region" : ["Toronto", "Montréal", "Vancouver", "Calgary", "Edmonton"],
  "population" : [5928040, 4098927, 2463431, 1392609, 1321426]
})
city_populations
```
This new data frame has the same `region` column as the `english_lang` data frame. The order of
the cities is different, but that is okay! We can use the `merge` function in `pandas` to say
we would like to combine the two data frames by matching the `region` between them. The argument
`on="region"` tells pandas we would like to use the `region` column to match up the entries.
```{code-cell} ipython3
:tags: ["output_scroll"]
english_lang = english_lang.merge(city_populations, on="region")
english_lang
```
You can see that the populations for each city are correct (e.g. Montréal: 4098927, Toronto: 5928040),
and we can proceed to with our analysis from here.

## Summary

Cleaning and wrangling data can be a very time-consuming process. However,
it is a critical step in any data analysis. We have explored many different
functions for cleaning and wrangling data into a tidy format.
{numref}`tab:summary-functions-table` summarizes some of the key wrangling
functions we learned in this chapter. In the following chapters, you will
learn how you can take this tidy data and do so much more with it to answer your
burning data science questions!

+++

```{table} Summary of wrangling functions
:name: tab:summary-functions-table

| Function | Description |
| ---      | ----------- |
| `agg` | calculates aggregated summaries of inputs |
| `assign` | adds or modifies columns in a data frame  |
| `groupby` |  allows you to apply function(s) to groups of rows |
| `iloc` | subsets columns/rows of a data frame using integer indices |
| `loc` | subsets columns/rows of a data frame using labels |
| `melt` | generally makes the data frame longer and narrower |
| `merge` | combine two data frames |
| `pivot` | generally makes a data frame wider and decreases the number of rows |
| `str.split` | splits up a string column into multiple columns  |
```

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Cleaning and wrangling data" row. You can preview a
non-interactive version of the worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.

+++ {"tags": []}

## Additional resources

- The [`pandas` package documentation](https://pandas.pydata.org/docs/reference/index.html) is
  another resource to learn more about the functions in this
  chapter, the full set of arguments you can use, and other related functions.
- [*Python for Data Analysis*](https://wesmckinney.com/book/) {cite:p}`mckinney2012python` has a few chapters related to
  data wrangling that go into more depth than this book. For example, the
  [data wrangling chapter](https://wesmckinney.com/book/data-wrangling.html) covers tidy data,
  `melt` and `pivot`, but also covers missing values
  and additional wrangling functions (like `stack`). The [data
  aggregation chapter](https://wesmckinney.com/book/data-aggregation.html) covers
  `groupby`, aggregating functions, `apply`, etc.
- You will occasionally encounter a case where you need to iterate over items
  in a data frame, but none of the above functions are flexible enough to do
  what you want. In that case, you may consider using [a for loop](https://wesmckinney.com/book/python-basics.html#control_for) {cite:p}`mckinney2012python`.


+++

## References

```{bibliography}
:filter: docname in docnames
```
