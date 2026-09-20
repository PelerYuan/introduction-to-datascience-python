Bar plot of size for Earth's largest 12 landmasses.
:::


The plot in {numref}`islands_bar_top` is definitely clearer now,
and allows us to answer our initial questions:
"Are the seven continents Earth's largest landmasses?"
and "Which are the next few largest landmasses?".
However, we could still improve this visualization
by coloring the bars based on whether they correspond to a continent, and
by organizing the bars by landmass size rather than by alphabetical order.
The data for coloring the bars is stored in the `landmass_type` column, so
we set the `color` encoding to `landmass_type`.
To organize the landmasses by their `size` variable,
we will use the altair `sort` function
in the y-encoding of the chart.
Since the `size` variable is encoded in the x channel of the chart,
we specify `sort("x")` on `alt.Y`.
This plots the values on `y` axis
in the ascending order of `x` axis values.
This creates a chart where the largest bar is the closest to the axis line,
which is generally the most visually appealing when sorting bars.
If instead we wanted to sort the values on `y-axis` in descending order of `x-axis`,
we could add a minus sign to reverse the order and specify `sort="-x"`.

```{index} altair; sort
```

To finalize this plot we will customize the axis and legend labels using the `title` method,
and add a title to the chart by specifying the `title` argument of `alt.Chart`.
Plot titles are not always required, especially when it would be redundant with an already-existing
caption or surrounding context (e.g., in a slide presentation with annotations).
But if you decide to include one, a good plot title should provide the take home message
that you want readers to focus on, e.g., "Earth's seven largest landmasses are continents,"
or a more general summary of the information displayed, e.g., "Earth's twelve largest landmasses."

```{code-cell} ipython3
islands_plot_sorted = alt.Chart(
	islands_top12,
	title="Earth's seven largest landmasses are continents"
).mark_bar().encode(
    x=alt.X("size").title("Size (1000 square mi)"),
    y=alt.Y("landmass").sort("x").title("Landmass"),
    color=alt.Color("landmass_type").title("Type")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("islands_plot_sorted", islands_plot_sorted, display=True)
```

:::{glue:figure} islands_plot_sorted
:figwidth: 700px
:name: islands_plot_sorted

Bar plot of size for Earth's largest 12 landmasses, colored by landmass type, with clearer axes and labels.
:::


The plot in {numref}`islands_plot_sorted` is now an effective
visualization for answering our original questions. Landmasses are organized by
their size, and continents are colored differently than other landmasses,
making it quite clear that all the seven largest landmasses are continents.

(histogramsviz)=
### Histograms: the Michelson speed of light data set

```{index} Michelson speed of light
```

The `morley` data set
contains measurements of the speed of light
collected in experiments performed in 1879.
Five experiments were performed,
and in each experiment, 20 runs were performed&mdash;meaning that
20 measurements of the speed of light were collected
in each experiment {cite:p}`lightdata`.
Because the speed of light is a very large number
(the true value is 299,792.458 km/sec), the data is coded
to be the measured speed of light minus 299,000.
This coding allows us to focus on the variations in the measurements, which are generally
much smaller than 299,000.
If we used the full large speed measurements, the variations in the measurements
would not be noticeable, making it difficult to study the differences between the experiments.

```{index} question; visualization
```

**Question:** Given what we know now about the speed of
light (299,792.458 kilometres per second), how accurate were each of the experiments?

First, we read in the data.

```{code-cell} ipython3
morley_df = pd.read_csv("data/morley.csv")
morley_df
```

```{index} distribution, altair; histogram, altair; count
```

```{index} see: count; altair
```

In this experimental data,
Michelson was trying to measure just a single quantitative number
(the speed of light).
The data set contains many measurements of this single quantity.
To tell how accurate the experiments were,
we need to visualize the distribution of the measurements
(i.e., all their possible values and how often each occurs).
We can do this using a *histogram*.
A histogram
helps us visualize how a particular variable is distributed in a data set
by grouping the values into bins,
and then using vertical bars to show how many data points fell in each bin.

To understand how to create a histogram in `altair`,
let's start by creating a bar chart
just like we did in the previous section.
Note that this time,
we are setting the `y` encoding to `"count()"`.
There is no `"count()"` column-name in `morley_df`;
we use `"count()"` to tell `altair`
that we want to count the number of occurrences of each value in along the x-axis
(which we encoded as the `Speed` column).

```{code-cell} ipython3
morley_bars = alt.Chart(morley_df).mark_bar().encode(
    x="Speed",
    y="count()"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_bars", morley_bars, display=False)
```

:::{glue:figure} morley_bars
:figwidth: 700px
:name: morley_bars

A bar chart of Michelson's speed of light data.
:::

The bar chart above gives us an indication of
which values are more common than others,
but because the bars are so thin it's hard to get a sense for the
overall distribution of the data.
We don't really care about how many occurrences there are of each exact `Speed` value,
but rather where most of the `Speed` values fall in general.
To more effectively communicate this information
we can group the x-axis into bins (or "buckets") using the `bin` method
and then count how many `Speed` values fall within each bin.
A bar chart that represent the count of values
for a binned quantitative variable is called a histogram.

```{code-cell} ipython3
morley_hist = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X("Speed").bin(),
    y="count()"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist", morley_hist, display=False)
```

:::{glue:figure} morley_hist
:figwidth: 700px
:name: morley_hist

Histogram of Michelson's speed of light data.
:::

#### Adding layers to an `altair` chart

```{index} altair; +, altair; mark_rule, altair; layers
```

{numref}`morley_hist` is a great start.
However,
we cannot tell how accurate the measurements are using this visualization
unless we can see the true value.
In order to visualize the true speed of light,
we will add a vertical line with the `mark_rule` function.
To draw a vertical line with `mark_rule`,
we need to specify where on the x-axis the line should be drawn.
We can do this by providing `x=alt.datum(792.458)`,
where the value `792.458` is the true speed of light minus 299,000
and `alt.datum` tells altair that we have a single datum
(number) that we would like plotted (rather than a column in the data frame).
Similarly, a horizontal line can be plotted using the `y` axis encoding and
the dataframe with one value, which would act as the be the y-intercept.
Note that
*vertical lines* are used to denote quantities on the *horizontal axis*,
while *horizontal lines* are used to denote quantities on the *vertical axis*.

To fine tune the appearance of this vertical line,
we can change it from a solid to a dashed line with `strokeDash=[5]`,
where `5` indicates the length of each dash. We also
change the thickness of the line by specifying `size=2`.
To add the dashed line on top of the histogram, we
**add** the `mark_rule` chart to the `morley_hist`
using the `+` operator.
Adding features to a plot using the `+` operator is known as *layering* in `altair`.
This is a powerful feature of `altair`; you
can continue to iterate on a single chart, adding and refining
one layer at a time. If you stored your chart as a variable
using the assignment symbol (`=`), you can add to it using the `+` operator.
Below we add a vertical line created using `mark_rule`
to the `morley_hist` we created previously.

```{note}
Technically we could have left out the data argument
when creating the rule chart
since we're not using any values from the `morley_df` data frame,
but we will need it later when we facet this layered chart,
so we are including it here already.
```

```{code-cell} ipython3
v_line = alt.Chart(morley_df).mark_rule(strokeDash=[6], size=1.5).encode(
    x=alt.datum(792.458)
)

morley_hist_line = morley_hist + v_line
```


```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_line", morley_hist_line, display=False)
```

:::{glue:figure} morley_hist_line
:figwidth: 700px
:name: morley_hist_line

Histogram of Michelson's speed of light data with vertical line indicating the true speed of light.
:::

In {numref}`morley_hist_line`,
we still cannot tell which experiments (denoted by the `Expt` column)
led to which measurements;
perhaps some experiments were more accurate than others.
To fully answer our question,
we need to separate the measurements from each other visually.
We can try to do this using a *colored* histogram,
where counts from different experiments are stacked on top of each other
in different colors.
We can create a histogram colored by the `Expt` variable
by adding it to the `color` argument.

```{code-cell} ipython3
morley_hist_colored = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X("Speed").bin(),
    y="count()",
    color="Expt"
)

morley_hist_colored = morley_hist_colored + v_line

```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_colored", morley_hist_colored, display=True)
```

:::{glue:figure} morley_hist_colored
:figwidth: 700px
:name: morley_hist_colored

Histogram of Michelson's speed of light data colored by experiment.
:::

```{index} integer
```

Alright great, {numref}`morley_hist_colored` looks... wait a second! We are not able to easily distinguish
between the colors of the different Experiments in the histogram! What is going on here? Well, if you
recall from {numref}`Chapter %s <wrangling>`, the *data type* you use for each variable
can influence how Python and `altair` treats it. Here, we indeed have an issue
with the data types in the `morley` data frame. In particular, the `Expt` column
is currently an *integer*---specifically, an `int64` type. But we want to treat it as a
*category*, i.e., there should be one category per type of experiment.
```{code-cell} ipython3
morley_df.info()
```

```{index} nominal, altair; :N
```

To fix this issue we can convert the `Expt` variable into a `nominal`
(i.e., categorical) type variable by adding a suffix `:N`
to the `Expt` variable. Adding the `:N` suffix ensures that `altair`
will treat a variable as a categorical variable, and
hence use a discrete color map in visualizations
([read more about data types in the altair documentation](https://altair-viz.github.io/user_guide/encodings/index.html#encoding-data-types)).
We also add the `stack(False)` method on the `y` encoding so
that the bars are not stacked on top of each other,
but instead share the same baseline.
We try to ensure that the different colors can be seen
despite them sitting in front of each other
by setting the `opacity` argument in `mark_bar` to `0.5`
to make the bars slightly translucent.

```{code-cell} ipython3
morley_hist_categorical = alt.Chart(morley_df).mark_bar(opacity=0.5).encode(
    x=alt.X("Speed").bin(),
    y=alt.Y("count()").stack(False),
    color="Expt:N"
)

morley_hist_categorical = morley_hist_categorical + v_line
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_categorical", morley_hist_categorical, display=True)
```

:::{glue:figure} morley_hist_categorical
:figwidth: 700px
:name: morley_hist_categorical

