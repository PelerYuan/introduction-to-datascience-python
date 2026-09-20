```{index} relationship; linear, relationship; nonlinear
```

- **Shape:** if you can draw a straight line roughly through the data points, the relationship is **linear**. Otherwise, it is **nonlinear**.

In {numref}`can_lang_plot_percent`, we see that
as the percentage of people who have a language as their mother tongue increases,
so does the percentage of people who speak that language at home.
Therefore, there is a **positive** relationship between these two variables.
Furthermore, because the points in {numref}`can_lang_plot_percent`
are fairly close together, and the points look more like a "line" than a "cloud",
we can say that this is a **strong** relationship.
And finally, because drawing a straight line through these points in
{numref}`can_lang_plot_percent`
would fit the pattern we observe quite well, we say that the relationship is **linear**.

Onto the second part of our exploratory data analysis question!
Recall that we are interested in knowing whether the strength
of the relationship we uncovered
in {numref}`can_lang_plot_percent` depends
on the higher-level language category (Official languages, Aboriginal languages,
and non-official, non-Aboriginal languages).
One common way to explore this
is to color the data points on the scatter plot we have already created by
group. For example, given that we have the higher-level language category for
each language recorded in the 2016 Canadian census, we can color the points in
our previous
scatter plot to represent each language's higher-level language category.

Here we want to distinguish the values according to the `category` group with
which they belong.  We can add the argument `color` to the `encode` method, specifying
that the `category` column should color the points. Adding this argument will
color the points according to their group and add a legend at the side of the
plot.
Since the labels of the language category as descriptive of their own,
we can remove the title of the legend to reduce visual clutter without reducing the effectiveness of the chart.

```{code-cell} ipython3
can_lang_plot_category=alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Language spoken most at home", "(percentage of Canadian residents)"]),
    y=alt.Y("mother_tongue_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Mother tongue", "(percentage of Canadian residents)"]),
    color="category"
).configure_axis(titleFontSize=12)

```

```{code-cell} ipython3
:tags: ["remove-cell"]
# Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
glue("can_lang_plot_category", can_lang_plot_category.properties(height=320, width=420), display=False)
```

:::{glue:figure} can_lang_plot_category
:figwidth: 700px
:name: can_lang_plot_category

Scatter plot of percentage of Canadians reporting a language as their mother tongue vs the primary language at home colored by language category.
:::


Another thing we can adjust is the location of the legend.
This is a matter of preference and not critical for the visualization.
We move the legend title using the `alt.Legend` method
and specify that we want it on the top of the chart.
This automatically changes the legend items to be laid out horizontally instead of vertically,
but we could also keep the vertical layout by specifying `direction="vertical"` inside `alt.Legend`.

```{index} altair; alt.Legend
```

```{code-cell} ipython3
can_lang_plot_legend = alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Language spoken most at home", "(percentage of Canadian residents)"]),
    y=alt.Y("mother_tongue_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Mother tongue", "(percentage of Canadian residents)"]),
    color=alt.Color("category")
        .legend(orient="top")
        .title("")
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
# Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
glue("can_lang_plot_legend", can_lang_plot_legend.properties(height=320, width=420), display=False)
```

:::{glue:figure} can_lang_plot_legend
:figwidth: 700px
:name: can_lang_plot_legend

Scatter plot of percentage of Canadians reporting a language as their mother tongue vs the primary language at home colored by language category with the legend edited.
:::

```{index} color palette, color blindness simulator
```

In {numref}`can_lang_plot_legend`, the points are colored with
the default `altair` color scheme, which is called `"tableau10"`. This is an appropriate choice for most situations and is also easy to read for people with reduced color vision.
In general, the color schemes that are used by default in Altair are adapted to the type of data that is displayed and selected to be easy to interpret both for people with good and reduced color vision.
If you are unsure about a certain color combination, you can use
this [color blindness simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/) to check
if your visualizations are color-blind friendly.

All the available color schemes and information on how to create your own can be viewed [in the Altair documentation](https://altair-viz.github.io/user_guide/customization.html#customizing-colors).
To change the color scheme of our chart,
we can add the `scheme` argument in the `scale` of the `color` encoding.
Below we pick the `"dark2"` theme, with the result shown
in {numref}`can_lang_plot_theme`.
We also set the `shape` aesthetic mapping to the `category` variable as well;
this makes the scatter point shapes different for each language category. This kind of
visual redundancy&mdash;i.e., conveying the same information with both scatter point color and shape&mdash;can
further improve the clarity and accessibility of your visualization,
but can add visual noise if there are many different shapes and colors,
so it should be used with care.
Note that we are switching back to the use of `mark_point` here
since `mark_circle` does not support the `shape` encoding
and will always show up as a filled circle.

```{code-cell} ipython3
can_lang_plot_theme = alt.Chart(can_lang).mark_point(filled=True).encode(
    x=alt.X("most_at_home_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Language spoken most at home", "(percentage of Canadian residents)"]),
    y=alt.Y("mother_tongue_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Mother tongue", "(percentage of Canadian residents)"]),
    color=alt.Color("category")
        .legend(orient="top")
        .title("")
        .scale(scheme="dark2"),
    shape="category"
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
# Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
glue("can_lang_plot_theme", can_lang_plot_theme.properties(height=320, width=420), display=False)
```

:::{glue:figure} can_lang_plot_theme
:figwidth: 700px
:name: can_lang_plot_theme

Scatter plot of percentage of Canadians reporting a language as their mother tongue vs the primary language at home colored by language category with custom colors and shapes.
:::

The chart above gives a good indication of how the different language categories differ,
and this information is sufficient to answer our research question.
But what if we want to know exactly which language correspond to which point in the chart?
With a regular visualization library this would not be possible,
as adding text labels for each individual language
would add a lot of visual noise and make the chart difficult to interpret.
However, since Altair is an interactive visualization library we can add information on demand
via the `Tooltip` encoding channel,
so that text labels for each point show up once we hover over it with the mouse pointer.
Here we also add the exact values of the variables on the x and y-axis to the tooltip.

```{index} altair; alt.Tooltip
```

```{code-cell} ipython3
can_lang_plot_tooltip = alt.Chart(can_lang).mark_point(filled=True).encode(
    x=alt.X("most_at_home_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Language spoken most at home", "(percentage of Canadian residents)"]),
    y=alt.Y("mother_tongue_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Mother tongue", "(percentage of Canadian residents)"]),
    color=alt.Color("category")
        .legend(orient="top")
        .title("")
        .scale(scheme="dark2"),
    shape="category",
    tooltip=alt.Tooltip(["language", "mother_tongue", "most_at_home"])
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
if "BOOK_BUILD_TYPE" in os.environ and os.environ["BOOK_BUILD_TYPE"] == "PDF":
    glue("can_lang_plot_tooltip", Image("img/viz/languages_with_mouse.png"), display=False)
else:
    # Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
    glue("can_lang_plot_tooltip", can_lang_plot_tooltip.properties(height=320, width=420), display=False)
```

:::{glue:figure} can_lang_plot_tooltip
:figwidth: 700px
:name: can_lang_plot_tooltip

Scatter plot of percentage of Canadians reporting a language as their mother tongue vs the primary language at home colored by language category with custom colors and mouse hover tooltip.
:::

From the visualization in {numref}`can_lang_plot_tooltip`,
we can now clearly see that the vast majority of Canadians reported one of the official languages
as their mother tongue and as the language they speak most often at home.
What do we see when considering the second part of our exploratory question?
Do we see a difference in the relationship
between languages spoken as a mother tongue and as a primary language
at home across the higher-level language categories?
Based on {numref}`can_lang_plot_tooltip`, there does not
appear to be much of a difference.
For each higher-level language category,
there appears to be a strong, positive, and linear relationship between
the percentage of people who speak a language as their mother tongue
and the percentage who speak it as their primary language at home.
The relationship looks similar regardless of the category.

Does this mean that this relationship is positive for all languages in the
world? And further, can we use this data visualization on its own to predict how many people
have a given language as their mother tongue if we know how many people speak
it as their primary language at home? The answer to both these questions is
"no!" However, with exploratory data analysis, we can create new hypotheses,
ideas, and questions (like the ones at the beginning of this paragraph).
Answering those questions often involves doing more complex analyses, and sometimes
even gathering additional data. We will see more of such complex analyses later on in
this book.

### Bar plots: the island landmass data set

```{index} Island landmasses
```

The `islands.csv` data set contains a list of Earth's landmasses as well as their area (in thousands of square miles) {cite:p}`islandsdata`.

```{index} question; visualization
```

**Question:** Are the continents (North / South America, Africa, Europe, Asia, Australia, Antarctica) Earth's seven largest landmasses? If so, what are the next few largest landmasses after those?

To get started, we will read and inspect the data:

```{code-cell} ipython3
:tags: ["output_scroll"]
islands_df = pd.read_csv("data/islands.csv")
islands_df
```

Here, we have a data frame of Earth's landmasses,
and are trying to compare their sizes.
The right type of visualization to answer this question is a bar plot.
In a bar plot, the height of each bar represents the value of an *amount*
(a size, count, proportion, percentage, etc).
They are particularly useful for comparing counts or proportions across different
groups of a categorical variable. Note, however, that bar plots should generally not be
used to display mean or median values, as they hide important information about
the variation of the data. Instead it's better to show the distribution of
all the individual data points, e.g., using a histogram, which we will discuss further in {numref}`histogramsviz`.

```{index} altair; mark_bar
```

We specify that we would like to use a bar plot
via the `mark_bar` function in `altair`.
The result is shown in {numref}`islands_bar`.

```{code-cell} ipython3
islands_bar = alt.Chart(islands_df).mark_bar().encode(
    x="landmass",
    y="size"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("islands_bar", islands_bar, display=False)
```

:::{glue:figure} islands_bar
:figwidth: 400px
:name: islands_bar

Bar plot of Earth's landmass sizes. The plot is too wide with the default settings.
:::

Alright, not bad! The plot in {numref}`islands_bar` is
definitely the right kind of visualization, as we can clearly see and compare
sizes of landmasses. The major issues are that the smaller landmasses' sizes
are hard to distinguish, and the plot is so wide that we can't compare them all! But remember that the
question we asked was only about the largest landmasses; let's make the plot a
little bit clearer by keeping only the largest 12 landmasses. We do this using
the `nlargest` function: the first argument is the number of rows we want and
the second is the name of the column we want to use for comparing which is
largest. Then to help make the landmass labels easier to read
we'll swap the `x` and `y` variables,
so that the labels are on the y-axis and we don't have to tilt our head to read them.

```{note}
Recall that in {numref}`Chapter %s <intro>`, we used `sort_values` followed by `head` to obtain
the ten rows with the largest values of a variable. We could have instead used the `nlargest` function
from `pandas` for this purpose. The `nsmallest` and `nlargest` functions achieve the same goal
as `sort_values` followed by `head`, but are slightly more efficient because they are specialized for this purpose.
In general, it is good to use more specialized functions when they are available!
```

```{index} DataFrame; nlargest, DataFrame; nsmallest
```

```{code-cell} ipython3
islands_top12 = islands_df.nlargest(12, "size")

islands_bar_top = alt.Chart(islands_top12).mark_bar().encode(
    x="size",
    y="landmass"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("islands_bar_top", islands_bar_top, display=True)
```

:::{glue:figure} islands_bar_top
:figwidth: 700px
:name: islands_bar_top

