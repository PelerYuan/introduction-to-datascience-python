## Creating subsets of data frames with `[]` & `loc[]`

```{index} see: []; DataFrame
```

```{index} see: loc[]; DataFrame
```

```{index} DataFrame; [], DataFrame; loc[], selecting columns
```

Now that we've loaded our data into Python, we can start wrangling the data to
find the ten Aboriginal languages that were most often reported
in 2016 as mother tongues in Canada. In particular, we want to construct
a table with the ten Aboriginal languages that have the largest
counts in the `mother_tongue` column. The first step is to extract
from our `can_lang` data only those rows that correspond to Aboriginal languages,
and then the second step is to keep only the `language` and `mother_tongue` columns.
The `[]` and `loc[]` operations on the `pandas` data frame will help us
here. The `[]` allows you to obtain a subset of (i.e., *filter*) the rows of a data frame,
or to obtain a subset of (i.e., *select*) the columns of a data frame.
The `loc[]` operation allows you to both filter rows *and* select columns
at the same time. We will first investigate filtering rows and selecting
columns with the `[]` operation,
and then use `loc[]` to do both in our analysis of the Aboriginal languages data.

```{note}
The `[]` and `loc[]` operations, and related operations, in `pandas`
are much more powerful than we describe in this chapter.
You will learn more sophisticated ways to index data frames later on
in {numref}`Chapter %s <wrangling>`.
```

### Using `[]` to filter rows
Looking at the `can_lang` data above, we see the column `category` contains different
high-level categories of languages, which include "Aboriginal languages",
"Non-Official & Non-Aboriginal languages" and "Official languages".  To answer
our question we want to filter our data set so we restrict our attention
to only those languages in the "Aboriginal languages" category.

```{index} DataFrame; [], filtering rows, logical statement, logical operator; equivalency (==), string
```

We can use the `[]` operation to obtain the subset of rows with desired values
from a data frame. {numref}`img-filter` shows the syntax we need to use to filter
rows with the `[]` operation. First, we type the name of the data frame---here, `can_lang`---followed
by square brackets. Inside the square brackets, we write a *logical statement* to
use when filtering the rows. A logical statement evaluates to either `True` or `False`
for each row in the data frame; the `[]` operation keeps only those rows
for which the logical statement evaluates to `True`. For example, in our analysis,
we are interested in keeping only languages in the `"Aboriginal languages"` higher-level
category. We can use the *equivalency operator* `==` to compare the values of the `category`
column---denoted by `can_lang["category"]`---with the value `"Aboriginal languages"`.
You will learn about many other kinds of logical
statement in {numref}`Chapter %s <wrangling>`. Similar to when we loaded the data file and put quotes
around the file name, here we need to put quotes around both `"Aboriginal languages"` and `"category"`. Using
quotes tells Python that this is a *string value* (e.g., a column name, or word data)
and not one of the special words that make up the Python programming language,
or one of the names we have given to objects in the code we have already written.

```{note}
In Python, single quotes (`'`) and double quotes (`"`) are generally
treated the same. So we could have written `'Aboriginal languages'` instead
of `"Aboriginal languages"` above, or `'category'` instead of `"category"`.
Try both out for yourself!
```

```{figure} img/intro/filter_rows.png
---
name: img-filter
---
Syntax for using the `[]` operation to filter rows.
```

This operation returns a data frame that has all the columns of the input data frame,
but only those rows corresponding to Aboriginal languages that we asked for in the logical statement.

```{code-cell} ipython3
:tags: ["output_scroll"]
can_lang[can_lang["category"] == "Aboriginal languages"]
```

### Using `[]` to select columns


```{index} DataFrame; [], selecting columns
```

We can also use the `[]` operation to select columns from a data frame.
{numref}`img-select` displays the syntax needed to select columns.
We again first type the name of the data frame---here, `can_lang`---followed
by square brackets. Inside the square brackets, we provide a *list* of
column names. In Python, we denote a *list* using square brackets, where
each item is separated by a comma (`,`). So if we are interested in
selecting only the `language` and `mother_tongue` columns from our original
`can_lang` data frame, we put the list `["language", "mother_tongue"]`
containing those two column names inside the square brackets of the `[]` operation.

```{figure} img/intro/select_columns.png
---
name: img-select
---
Syntax for using the `[]` operation to select columns.
```

This operation returns a data frame that has all the rows of the input data frame,
but only those columns that we named in the selection list.

```{code-cell} ipython3
can_lang[["language", "mother_tongue"]]
```

### Using `loc[]` to filter rows and select columns

```{index} DataFrame; loc[], selecting columns
```

The `[]` operation is only used when you want to filter rows *or* select columns;
it cannot be used to do both operations at the same time. But in order to answer
our original data analysis question in this chapter, we need to *both* filter the rows
for Aboriginal languages, *and* select the `language` and `mother_tongue` columns.
Fortunately, `pandas` provides the `loc[]` operation, which lets us do just that.
The syntax is very similar to the `[]` operation we have already covered: we will
essentially combine both our row filtering and column selection steps from before.
In particular, we first write the name of the data frame---`can_lang` again---then follow
that with the `.loc[]` operation. Inside the square brackets,
we write our row filtering logical statement,
then a comma, then our list of columns to select.

```{figure} img/intro/filter_rows_and_columns.png
---
name: img-loc
---
Syntax for using the `loc[]` operation to filter rows and select columns.
```

```{code-cell} ipython3
aboriginal_lang = can_lang.loc[can_lang["category"] == "Aboriginal languages", ["language", "mother_tongue"]]
```
There is one very important thing to notice in this code example.
The first is that we used the `loc[]` operation on the `can_lang` data frame by
writing `can_lang.loc[]`---first the data frame name, then a dot, then `loc[]`.
There's that dot again! If you recall, earlier in this chapter we used the `read_csv` function from `pandas` (aliased as `pd`),
and wrote `pd.read_csv`. The dot means that the thing on the left (`pd`, i.e., the `pandas` package) *provides* the
thing on the right (the `read_csv` function). In the case of `can_lang.loc[]`, the thing on the left (the `can_lang` data frame)
*provides* the thing on the right (the `loc[]` operation). In Python,
both packages (like `pandas`) *and* objects (like our `can_lang` data frame) can provide functions
and other objects that we access using the dot syntax.

```{note}
A note on terminology: when an object `obj` provides a function `f` with the
dot syntax (as in `obj.f()`), sometimes we call that function `f` a *method* of `obj` or an *operation* on `obj`.
Similarly, when an object `obj` provides another object `x` with the dot syntax (as in `obj.x`), sometimes we call the object `x` an *attribute* of `obj`.
We will use all of these terms throughout the book, as you will see them used commonly in the community.
And just because we programmers like to be confusing for no apparent reason: we *don't* use the "method", "operation", or "attribute" terminology
when referring to functions and objects from packages, like `pandas`. So for example, `pd.read_csv`
would typically just be referred to as a function, but not as a method or operation, even though it uses the dot syntax.
```

At this point, if we have done everything correctly, `aboriginal_lang` should be a data frame
containing *only* rows where the `category` is `"Aboriginal languages"`,
and containing *only* the `language` and `mother_tongue` columns.
Any time you take a step in a data analysis, it's good practice to check the output
by printing the result.
```{code-cell} ipython3
aboriginal_lang
```
We can see the original `can_lang` data set contained 214 rows
with multiple kinds of `category`. The data frame
`aboriginal_lang` contains only 67 rows, and looks like it only contains Aboriginal languages.
So it looks like the `loc[]` operation gave us the result we wanted!

## Using `sort_values` and `head` to select rows by ordered values

```{index} DataFrame; sort_values, DataFrame; head
```

We have used the `[]` and `loc[]` operations on a data frame to obtain a table
with only the Aboriginal languages in the data set and their associated counts.
However, we want to know the **ten** languages that are spoken most often. As a
next step, we will order the `mother_tongue` column from largest to smallest
value and then extract only the top ten rows. This is where the `sort_values`
and `head` functions come to the rescue!

The `sort_values` function allows us to order the rows of a data frame by the
values of a particular column.  We need to specify the column name
by which we want to sort the data frame by passing it to the argument `by`.
Since we want to choose the ten Aboriginal languages most often reported as a mother tongue
language, we will use the `sort_values` function to order the rows in our
`selected_lang` data frame by the `mother_tongue` column. We want to
arrange the rows in descending order (from largest to smallest),
so we specify the argument `ascending` as `False`.

```{figure} img/intro/sort_values.png
---
name: img-sort-values
---
Syntax for using `sort_values` to arrange rows in decending order.
```

```{code-cell} ipython3
arranged_lang = aboriginal_lang.sort_values(by="mother_tongue", ascending=False)
arranged_lang
```

Next, we will obtain the ten most common Aboriginal languages by selecting only
the first ten rows of the `arranged_lang` data frame.
We do this using the `head` function, and specifying the argument
`10`.


```{code-cell} ipython3
ten_lang = arranged_lang.head(10)
ten_lang
```

(ch1-adding-modifying)=
## Adding and modifying columns

```{index} adding columns, modifying columns
```

Recall that our data analysis question referred to the *count* of Canadians
that speak each of the top ten most commonly reported Aboriginal languages as
their mother tongue, and the `ten_lang` data frame indeed contains those
counts... But perhaps, seeing these numbers, we became curious about the
*percentage* of the population of Canada associated with each count. It is
common to come up with new data analysis questions in the process of answering
a first one&mdash;so fear not and explore! To answer this small
question along the way, we need to divide each count in the `mother_tongue`
column by the total Canadian population according to the 2016
census&mdash;i.e., 35,151,728&mdash;and multiply it by 100. We can perform
this computation using the code `100 * ten_lang["mother_tongue"] / canadian_population`.
Then to store the result in a new column (or
overwrite an existing column), we specify the name of the new
column to create (or old column to modify), then the assignment symbol `=`,
and then the computation to store in that column. In this case, we will opt to
create a new column called `mother_tongue_percent`.

```{note}
You will see below that we write the Canadian population in
Python as `35_151_728`. The underscores (`_`) are just there for readability,
and do not affect how Python interprets the number. In other words,
`35151728` and `35_151_728` are treated identically in Python,
although the latter is much clearer!
```

```{code-cell} ipython3
:tags: [remove-cell]
# disable setting with copy warning
# it's not important for this chapter and just distracting
# only occurs here because we did a much earlier .loc operation that is being picked up below by the coln assignment
pd.options.mode.chained_assignment = None
```

```{code-cell} ipython3
canadian_population = 35_151_728
ten_lang["mother_tongue_percent"] = 100 * ten_lang["mother_tongue"] / canadian_population
ten_lang
```

The `ten_lang_percent` data frame shows that
the ten Aboriginal languages in the `ten_lang` data frame were spoken
as a mother tongue by between 0.008% and 0.18% of the Canadian population.

## Combining steps with chaining and multiline expressions

It took us 3 steps to find the ten Aboriginal languages most often reported in
2016 as mother tongues in Canada. Starting from the `can_lang` data frame, we:

1) used `loc` to filter the rows so that only the
   `Aboriginal languages` category remained, and selected the
   `language` and `mother_tongue` columns,
2) used `sort_values` to sort the rows by `mother_tongue` in descending order, and
3) obtained only the top 10 values using `head`.

One way of performing these steps is to just write
multiple lines of code, storing temporary, intermediate objects as you go.
```{code-cell} ipython3
aboriginal_lang = can_lang.loc[can_lang["category"] == "Aboriginal languages", ["language", "mother_tongue"]]
arranged_lang_sorted = aboriginal_lang.sort_values(by="mother_tongue", ascending=False)
ten_lang = arranged_lang_sorted.head(10)
```

```{index} multi-line expression
```

You might find that code hard to read. You're not wrong; it is!
There are two main issues with readability here. First, each line of code is quite long.
It is hard to keep track of what methods are being called, and what arguments were used.
Second, each line introduces a new temporary object. In this case, both `aboriginal_lang` and `arranged_lang_sorted`
are just temporary results on the way to producing the `ten_lang` data frame.
This makes the code hard to read, as one has to trace where each temporary object
goes, and hard to understand, since introducing many named objects also suggests that they
are of some importance, when really they are just intermediates.
The need to call multiple methods in a sequence to process a data frame is
quite common, so this is an important issue to address!

To solve the first problem, we can actually split the long expressions above across
multiple lines. Although in most cases, a single expression in Python must be contained
in a single line of code, there are a small number of situations where lets us do this.
Let's rewrite this code in a more readable format using multiline expressions.

```{code-cell} ipython3
aboriginal_lang = can_lang.loc[
    can_lang["category"] == "Aboriginal languages",
    ["language", "mother_tongue"]
]
arranged_lang_sorted = aboriginal_lang.sort_values(
    by="mother_tongue",
    ascending=False
)
ten_lang = arranged_lang_sorted.head(10)
```

This code is the same as the code we showed earlier; you can see the same
sequence of methods and arguments is used. But long expressions are split
across multiple lines when they would otherwise get long and unwieldy,
improving the readability of the code.
How does Python know when to keep
reading on the next line for a single expression?
For the line starting with `aboriginal_lang = ...`, Python sees that the line ends with a left
bracket symbol `[`, and knows that our
expression cannot end until we close it with an appropriate corresponding right bracket symbol `]`.
We put the same two arguments as we did before, and then
the corresponding right bracket appears after `["language", "mother_tongue"]`).
For the line starting with `arranged_lang_sorted = ...`, Python sees that the line ends with a left parenthesis symbol `(`,
and knows the expression cannot end until we close it with the corresponding right parenthesis symbol `)`.
Again we use the same two arguments as before, and then the
corresponding right parenthesis appears right after `ascending=False`.
In both cases, Python keeps reading the next line to figure out
what the rest of the expression is. We could, of course,
put all of the code on one line of code, but splitting it across
multiple lines helps a lot with code readability.

```{index} chaining
```

We still have to handle the issue that each line of code---i.e., each step in the analysis---introduces
a new temporary object. To address this issue, we can *chain* multiple operations together without
assigning intermediate objects. The key idea of chaining is that the *output* of
each step in the analysis is a data frame, which means that you can just directly keep calling methods
that operate on the output of each step in a sequence! This simplifies the code and makes it
easier to read. The code below demonstrates the use of both multiline expressions and chaining together.
The code is now much cleaner, and the `ten_lang` data frame that we get is equivalent to the one
from the messy code above!

```{code-cell} ipython3
# obtain the 10 most common Aboriginal languages
ten_lang = (
    can_lang.loc[
       can_lang["category"] == "Aboriginal languages",
       ["language", "mother_tongue"]
    ]
    .sort_values(by="mother_tongue", ascending=False)
    .head(10)
)
ten_lang
```

Let's parse this new block of code piece by piece.
The code above starts with a left parenthesis, `(`, and so Python
knows to keep reading to subsequent lines until it finds the corresponding
right parenthesis symbol `)`. The `loc` method performs the filtering and selecting steps as before. The line after this
starts with a period (`.`) that "chains" the output of the `loc` step with the next operation,
`sort_values`. Since the output of `loc` is a data frame, we can use the `sort_values` method on it
without first giving it a name! That is what the `.sort_values` does on the next line.
Finally, we once again "chain" together the output of `sort_values` with `head` to ask for the 10
most common languages. Finally, the right parenthesis `)` corresponding to the very first left parenthesis
appears on the second last line, completing the multiline expression.
Instead of creating intermediate objects, with chaining, we take the output of
one operation and use that to perform the next operation. In doing so, we remove the need to create and
store intermediates. This can help with readability by simplifying the code.

Now that we've shown you chaining as an alternative to storing
temporary objects and composing code, does this mean you should *never* store
temporary objects or compose code? Not necessarily!
There are times when temporary objects are handy to keep around.
For example, you might store a temporary object before feeding it into a plot function
so you can iteratively change the plot without having to
redo all of your data transformations.
Chaining many functions can be overwhelming and difficult to debug;
you may want to store a temporary object midway through to inspect your result
before moving on with further steps.

## Exploring data with visualizations

```{index} visualization
```
The `ten_lang` table answers our initial data analysis question.
Are we done? Well, not quite; tables are almost never the best way to present
the result of your analysis to your audience. Even the `ten_lang` table with
only two columns presents some difficulty: for example, you have to scrutinize
the table quite closely to get a sense for the relative numbers of speakers of
each language. When you move on to more complicated analyses, this issue only
gets worse. In contrast, a *visualization* would convey this information in a much
more easily understood format.
Visualizations are a great tool for summarizing information to help you
effectively communicate with your audience, and creating effective data visualizations
is an essential component of any data
analysis. In this section we will develop a visualization of the
 ten Aboriginal languages that were most often reported in 2016 as mother tongues in
Canada, as well as the number of people that speak each of them.

### Using `altair` to create a bar plot

```{index} altair, visualization; bar
```

In our data set, we can see that `language` and `mother_tongue` are in separate
columns (or variables). In addition, there is a single row (or observation) for each language.
The data are, therefore, in what we call a *tidy data* format. Tidy data is a
fundamental concept and will be a significant focus in the remainder of this
book: many of the functions from `pandas` require tidy data, as does the
`altair` package that we will use shortly for our visualization. We will
formally introduce tidy data in {numref}`Chapter %s <wrangling>`.

```{index} see: plot; visualization
```

```{index} see: visualization; altair
```

We will make a bar plot to visualize our data. A bar plot is a chart where the
lengths of the bars represent certain values, like counts or proportions. We
will make a bar plot using the `mother_tongue` and `language` columns from our
`ten_lang` data frame. To create a bar plot of these two variables using the
`altair` package, we must specify the data frame, which variables
to put on the x and y axes, and what kind of plot to create.
First, we need to import the `altair` package.

```{code-cell} ipython3
import altair as alt
```

```{index} altair; mark_bar, altair; encoding channel
```

+++

The fundamental object in `altair` is the `Chart`, which takes a data frame as an argument: `alt.Chart(ten_lang)`.
With a chart object in hand, we can now specify how we would like the data to be visualized.
We first indicate what kind of graphical *mark* we want to use to represent the data. Here we set the mark attribute
of the chart object using the `Chart.mark_bar` function, because we want to create a bar chart.
Next, we need to *encode* the variables of the data frame using
the `x` and `y` *channels* (which represent the x-axis and y-axis position of the points). We use the `encode()`
function to handle this: we specify that the `language` column should correspond to the x-axis,
and that the `mother_tongue` column should correspond to the y-axis.

```{figure} img/intro/altair_syntax.png
---
name: img-altair
---
Syntax for using `altair` to make a bar chart.
```

