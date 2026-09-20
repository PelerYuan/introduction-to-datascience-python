+++

```{code-cell} ipython3
:tags: []

barplot_mother_tongue = (
  alt.Chart(ten_lang).mark_bar().encode(x="language", y="mother_tongue")
)


```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("barplot-mother-tongue", barplot_mother_tongue, display=True)

```

:::{glue:figure} barplot-mother-tongue
:figwidth: 700px
:name: barplot-mother-tongue

Bar plot of the ten Aboriginal languages most often reported by Canadian residents as their mother tongue
:::

+++

```{index} see: .; chaining
```

### Formatting `altair` charts

It is exciting that we can already visualize our data to help answer our
question, but we are not done yet! We can (and should) do more to improve the
interpretability of the data visualization that we created. For example, by
default, Python uses the column names as the axis labels. Usually these
column names do not have enough information about the variable in the column.
We really should replace this default with a more informative label. For the
example above, Python uses the column name `mother_tongue` as the label for the
y axis, but most people will not know what that is. And even if they did, they
will not know how we measured this variable, or the group of people on which the
measurements were taken. An axis label that reads "Mother Tongue (Number of
Canadian Residents)" would be much more informative. To make the code easier to
read, we're spreading it out over multiple lines just as we did in the previous
section with pandas.

```{index} plot; labels, plot; axis labels, altair; alt.X, altair; alt.Y, altair; title
```

Adding additional labels to our visualizations that we create in `altair` is
one common and easy way to improve and refine our data visualizations. We can add titles for the axes
in the `altair` objects using `alt.X` and `alt.Y` with the `title` method to make
the axes titles more informative (you will learn more about `alt.X` and `alt.Y` in {numref}`Chapter %s <viz>`).
Again, since we are specifying
words (e.g. `"Mother Tongue (Number of Canadian Residents)"`) as arguments to
the `title` method, we surround them with quotation marks. We can do many other modifications
to format the plot further, and we will explore these in {numref}`Chapter %s <viz>`.

```{code-cell} ipython3
barplot_mother_tongue = alt.Chart(ten_lang).mark_bar().encode(
    x=alt.X("language").title("Language"),
    y=alt.Y("mother_tongue").title("Mother Tongue (Number of Canadian Residents)")
)
```


```{code-cell} ipython3
:tags: ["remove-cell"]

glue("barplot-mother-tongue-labs", barplot_mother_tongue, display=True)

```


:::{glue:figure} barplot-mother-tongue-labs
:figwidth: 700px
:name: barplot-mother-tongue-labs

Bar plot of the ten Aboriginal languages most often reported by Canadian residents as their mother tongue with x and y labels. Note that this visualization is not done yet; there are still improvements to be made.
:::


The result is shown in {numref}`barplot-mother-tongue-labs`.
This is already quite an improvement! Let's tackle the next major issue with the visualization
in {numref}`barplot-mother-tongue-labs`: the vertical x axis labels, which are
currently making it difficult to read the different language names.
One solution is to rotate the plot such that the bars are horizontal rather than vertical.
To accomplish this, we will swap the x and y coordinate axes:


```{code-cell} ipython3
barplot_mother_tongue_axis = alt.Chart(ten_lang).mark_bar().encode(
    x=alt.X("mother_tongue").title("Mother Tongue (Number of Canadian Residents)"),
    y=alt.Y("language").title("Language")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("barplot-mother-tongue-labs-axis", barplot_mother_tongue_axis, display=True)

```

:::{glue:figure} barplot-mother-tongue-labs-axis
:figwidth: 700px
:name: barplot-mother-tongue-labs-axis

Horizontal bar plot of the ten Aboriginal languages most often reported by Canadian residents as their mother tongue. There are no more serious issues with this visualization, but it could be refined further.
:::

```{index} altair; sort
```

Another big step forward, as shown in {numref}`barplot-mother-tongue-labs-axis`! There
are no more serious issues with the visualization. Now comes time to refine
the visualization to make it even more well-suited to answering the question
we asked earlier in this chapter. For example, the visualization could be made more transparent by
organizing the bars according to the number of Canadian residents reporting
each language, rather than in alphabetical order. We can reorder the bars using
the `sort` method, which orders a variable (here `language`) based on the
values of the variable(`mother_tongue`) on the `x-axis`.

```{code-cell} ipython3
ordered_barplot_mother_tongue = alt.Chart(ten_lang).mark_bar().encode(
    x=alt.X("mother_tongue").title("Mother Tongue (Number of Canadian Residents)"),
    y=alt.Y("language").sort("x").title("Language")
)
```

+++

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("barplot-mother-tongue-reorder", ordered_barplot_mother_tongue, display=True)

```


:::{glue:figure} barplot-mother-tongue-reorder
:figwidth: 700px
:name: barplot-mother-tongue-reorder

Bar plot of the ten Aboriginal languages most often reported by Canadian residents as their mother tongue with bars reordered.
:::


{numref}`barplot-mother-tongue-reorder` provides a very clear and well-organized
answer to our original question; we can see what the ten most often reported Aboriginal languages
were, according to the 2016 Canadian census, and how many people speak each of them. For
instance, we can see that the Aboriginal language most often reported was Cree
n.o.s. with over 60,000 Canadian residents reporting it as their mother tongue.

```{note}
"n.o.s." means "not otherwise specified", so Cree n.o.s. refers to
individuals who reported Cree as their mother tongue. In this data set, the
Cree languages include the following categories: Cree n.o.s., Swampy Cree,
Plains Cree, Woods Cree, and a 'Cree not included elsewhere' category (which
includes Moose Cree, Northern East Cree and Southern East Cree)
{cite:p}`language2016`.
```

### Putting it all together

```{index} comment
```

```{index} see: #; comment
```

In the block of code below, we put everything from this chapter together, with a few
modifications. In particular, we have combined all of our steps into one expression
split across multiple lines using the left and right parenthesis symbols `(` and `)`.
We have also provided *comments* next to
many of the lines of code below using the
hash symbol `#`. When Python sees a `#` sign, it
will ignore all of the text that
comes after the symbol on that line. So you can use comments to explain lines
of code for others, and perhaps more importantly, your future self!
It's good practice to get in the habit of
commenting your code to improve its readability.

This exercise demonstrates the power of Python. In relatively few lines of code, we
performed an entire data science workflow with a highly effective data
visualization! We asked a question, loaded the data into Python, wrangled the data
(using `[]`, `loc[]`, `sort_values`, and `head`) and created a data visualization to
help answer our question. In this chapter, you got a quick taste of the data
science workflow; continue on with the next few chapters to learn each of
these steps in much more detail!

```{code-cell} ipython3
# load the data set
can_lang = pd.read_csv("data/can_lang.csv")

# obtain the 10 most common Aboriginal languages
ten_lang = (
    can_lang.loc[can_lang["category"] == "Aboriginal languages", ["language", "mother_tongue"]]
    .sort_values(by="mother_tongue", ascending=False)
    .head(10)
)

# create the visualization
ten_lang_plot = alt.Chart(ten_lang).mark_bar().encode(
    x=alt.X("mother_tongue").title("Mother Tongue (Number of Canadian Residents)"),
    y=alt.Y("language").sort("x").title("Language")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("final_plot", ten_lang_plot, display=True)

```


:::{glue:figure} final_plot
:figwidth: 700px
:name: final_plot

Bar plot of the ten Aboriginal languages most often reported by Canadian residents as their mother tongue
:::

## Accessing documentation

```{index} documentation
```

```{index} see: help; documentation
```

```{index} see: __doc__; documentation
```

There are many Python functions in the `pandas` package (and beyond!), and
nobody can be expected to remember what every one of them does
or all of the arguments we have to give them. Fortunately, Python provides
the `help` function, which
provides an easy way to pull up the documentation for
most functions quickly. To use the `help` function to access the documentation, you
just put the name of the function you are curious about as an argument inside the `help` function.
For example, if you had forgotten what the `pd.read_csv` function
did or exactly what arguments to pass in, you could run the following
code:

```{code-cell} ipython3
:tags: ["remove-output"]
help(pd.read_csv)
```

{numref}`help_read_csv` shows the documentation that will pop up,
including a high-level description of the function, its arguments,
a description of each, and more. Note that you may find some of the
text in the documentation a bit too technical right now.
Fear not: as you work through this book, many of these terms will be introduced
to you, and slowly but surely you will become more adept at understanding and navigating
documentation like that shown in {numref}`help_read_csv`. But do keep in mind that the documentation
is not written to *teach* you about a function; it is just there as a reference to *remind*
you about the different arguments and usage of functions that you have already learned about elsewhere.

+++

```{figure} img/intro/help_read_csv.png
---
height: 700px
name: help_read_csv
---
The documentation for the read_csv function including a high-level description, a list of arguments and their meanings, and more.
```

+++

If you are working in a Jupyter Lab environment, there are some conveniences that will help you lookup function names
and access the documentation. First, rather than `help`, you can use the more concise `?` character. So for example,
to read the documentation for the `pd.read_csv` function, you can run the following code:
```{code-cell} ipython3
:tags: ["remove-output"]
?pd.read_csv
```
You can also type the first characters of the function you want to use,
and then press <kbd>Tab</kbd> to bring up small menu
that shows you all the available functions
that starts with those characters.
This is helpful both for remembering function names
and to prevent typos.

+++

```{figure} img/intro/completion_menu.png
---
height: 400px
name: completion_menu
---
The suggestions that are shown after typing `pd.read` and pressing <kbd>Tab</kbd>.
```

+++

To get more info on the function you want to use,
you can type out the full name
and then hold <kbd>Shift</kbd> while pressing <kbd>Tab</kbd>
to bring up a help dialogue including the same information as when using `help()`.

+++

```{figure} img/intro/help_dialog.png
---
height: 400px
name: help_dialog
---
The help dialog that is shown after typing `pd.read_csv` and then pressing <kbd>Shift</kbd> + <kbd>Tab</kbd>.
```

+++

Finally,
it can be helpful to have this help dialog open at all times,
especially when you start out learning about programming and data science.
You can achieve this by clicking on the `Help` text
in the menu bar at the top
and then selecting `Show Contextual Help`.

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Python and Pandas" row.  You can preview a
non-interactive version of the worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.



+++

## References

```{bibliography}
:filter: docname in docnames
```

