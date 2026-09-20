
```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
from IPython.display import Image
```

(viz)=
# Effective data visualization

## Overview
This chapter will introduce concepts and tools relating to data visualization
beyond what we have seen and practiced so far.  We will focus on guiding
principles for effective data visualization and explaining visualizations
independent of any particular tool or programming language.  In the process, we
will cover some specifics of creating visualizations (scatter plots, bar
plots, line plots, and histograms) for data using Python.

## Chapter learning objectives

By the end of the chapter, readers will be able to do the following:

- Describe when to use the following kinds of visualizations to answer specific questions using a data set:
    - scatter plots
    - line plots
    - bar plots
    - histogram plots
- Given a data set and a question, select from the above plot types and use Python to create a visualization that best answers the question.
- Evaluate the effectiveness of a visualization and suggest improvements to better answer a given question.
- Referring to the visualization, communicate the conclusions in non-technical terms.
- Identify rules of thumb for creating effective visualizations.
- Use the `altair` library in Python to create and refine the above visualizations using:
    - graphical marks: `mark_point`, `mark_line`, `mark_circle`, `mark_bar`, `mark_rule`
    - encoding channels: `x`, `y`, `color`, `shape`
    - labeling: `title`
    - transformations: `scale`
    - subplots: `facet`
- Define the two key aspects of `altair` charts:
    - graphical marks
    - encoding channels
- Describe the difference in raster and vector output formats.
- Use `chart.save()` to save visualizations in `.png` and `.svg` format.

## Choosing the visualization

<font size="5">*Ask a question, and answer it*</font>

```{index} question; visualization
```

The purpose of a visualization is to answer a question
about a data set of interest. So naturally, the
first thing to do **before** creating a visualization is to formulate the
question about the data you are trying to answer.  A good visualization will
clearly answer your question without distraction; a *great* visualization will
suggest even what the question was itself without additional explanation.
Imagine your visualization as part of a poster presentation for a project; even
if you aren't standing at the poster explaining things, an effective
visualization will convey your message to the audience.

Recall the different data analysis questions
from {numref}`Chapter %s <intro>`.
With the visualizations we will cover in this chapter,
we will be able to answer *only descriptive and exploratory* questions.
Be careful to not answer any *predictive, inferential, causal*
*or mechanistic* questions with the visualizations presented here,
as we have not learned the tools necessary to do that properly just yet.

As with most coding tasks, it is totally fine (and quite common) to make
mistakes and iterate a few times before you find the right visualization for
your data and question. There are many different kinds of plotting
graphics available to use (see Chapter 5 of *Fundamentals of Data Visualization* {cite:p}`wilkeviz` for a directory).
The types of plots that we introduce in this book are shown in {numref}`plot_sketches`;
which one you should select depends on your data
and the question you want to answer.
In general, the guiding principles of when to use each type of plot
are as follows:

```{index} visualization; line, visualization; histogram, visualization; scatter, visualization; bar, distribution
```

- **scatter plots** visualize the relationship between two quantitative variables
- **line plots** visualize trends with respect to an independent, ordered quantity (e.g., time)
- **bar plots** visualize comparisons of amounts
- **histograms** visualize the distribution of one quantitative variable (i.e., all its possible values and how often they occur)

```{figure} img/viz/plot-sketches-1.png
---
height: 400px
name: plot_sketches
---
Examples of scatter, line and bar plots, as well as histograms.
```


All types of visualization have their (mis)uses, but three kinds are usually
hard to understand or are easily replaced with an oft-better alternative.  In
particular, you should avoid **pie charts**; it is generally better to use
bars, as it is easier to compare bar heights than pie slice sizes.  You should
also not use **3-D visualizations**, as they are typically hard to understand
when converted to a static 2-D image format. Finally, do not use tables to make
numerical comparisons; humans are much better at quickly processing visual
information than text and math. Bar plots are again typically a better
alternative.

+++

## Refining the visualization

<font size="5">*Convey the message, minimize noise*</font>

Just being able to make a visualization in Python with `altair` (or any other tool
for that matter) doesn't mean that it effectively communicates your message to
others. Once you have selected a broad type of visualization to use, you will
have to refine it to suit your particular need.  Some rules of thumb for doing
this are listed below. They generally fall into two classes: you want to
*make your visualization convey your message*, and you want to *reduce visual noise*
as much as possible. Humans have limited cognitive ability to process
information; both of these types of refinement aim to reduce the mental load on
your audience when viewing your visualization, making it easier for them to
understand and remember your message quickly.

**Convey the message**

- Make sure the visualization answers the question you have asked most simply and plainly as possible.
- Use legends and labels so that your visualization is understandable without reading the surrounding text.
- Ensure the text, symbols, lines, etc., on your visualization are big enough to be easily read.
- Ensure the data are clearly visible; don't hide the shape/distribution of the data behind other objects (e.g.,  a bar).
- Make sure to use color schemes that are understandable by those with
  colorblindness (a surprisingly large fraction of the overall
  population&mdash;from about 1% to 10%, depending on sex and ancestry {cite:p}`deebblind`).
  For example, [Color Schemes](https://altair-viz.github.io/user_guide/customization.html#customizing-colors)
  provides the ability to pick such color schemes, and you can check
  your visualizations after you have created them by uploading to online tools
  such as a [color blindness simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/).
- Redundancy can be helpful; sometimes conveying the same message in multiple ways reinforces it for the audience.

**Minimize noise**

- Use colors sparingly. Too many different colors can be distracting, create false patterns, and detract from the message.
- Be wary of overplotting. Overplotting is when marks that represent the data
  overlap, and is problematic as it prevents you from seeing how many data
  points are represented in areas of the visualization where this occurs. If your
  plot has too many dots or lines and starts to look like a mess, you need to do
  something different.
- Only make the plot area (where the dots, lines, bars are) as big as needed. Simple plots can be made small.
- Don't adjust the axes to zoom in on small differences. If the difference is small, show that it's small!

+++

## Creating visualizations with `altair`

<font size="5">*Build the visualization iteratively*</font>

```{index} altair
```

This section will cover examples of how to choose and refine a visualization given a data set and a question that you want to answer,
and then how to create the visualization in Python using `altair`.  To use the `altair` package, we need to first import it. We will also import `pandas` to use for reading in the data.

```{code-cell} ipython3
import pandas as pd
import altair as alt
```

```{note}
In this chapter, we will provide example visualizations using relatively small
data sets, so we are fine using the default settings in `altair`. However,
`altair` will raise an error if you try to plot with a data frame that has more
than 5,000 rows. The simplest way to plot larger data sets is to enable the
`vegafusion` data transformer right after you import the `altair` package:
`alt.data_transformers.enable("vegafusion")`. This will allow you to plot up to
100,000 graphical objects (e.g., a scatter plot with 100,000 points). To
visualize *even larger* data sets, see [the `altair` documentation](https://altair-viz.github.io/user_guide/large_datasets).
```

### Scatter plots and line plots: the Mauna Loa CO$_{\text{2}}$ data set

```{index} Mauna Loa
```

The [Mauna Loa CO$_{\text{2}}$ data set](https://www.esrl.noaa.gov/gmd/ccgg/trends/data.html),
curated by Dr. Pieter Tans, NOAA/GML
and Dr. Ralph Keeling, Scripps Institution of Oceanography,
records the atmospheric concentration of carbon dioxide
(CO$_{\text{2}}$, in parts per million)
at the Mauna Loa research station in Hawaii
from 1959 onward {cite:p}`maunadata`.
For this book, we are going to focus on the years 1980-2020.

```{index} question; visualization
```

**Question:** Does the concentration of atmospheric CO$_{\text{2}}$ change over time,
and are there any interesting patterns to note?

```{code-cell} ipython3
:tags: ["remove-cell"]
mauna_loa = pd.read_csv("data/mauna_loa.csv")
mauna_loa["day"]=1
mauna_loa["date_measured"]=pd.to_datetime(mauna_loa[["year", "month", "day"]])
mauna_loa = mauna_loa[["date_measured", "ppm"]].query('ppm>0 and date_measured>"1980-1-1"')
mauna_loa.to_csv("data/mauna_loa_data.csv", index=False)
```

To get started, we will read and inspect the data:

```{code-cell} ipython3
# mauna loa carbon dioxide data
co2_df = pd.read_csv(
    "data/mauna_loa_data.csv",
    parse_dates=["date_measured"]
)
co2_df
```


```{code-cell} ipython3
co2_df.info()
```

We see that there are two columns in the `co2_df` data frame; `date_measured` and `ppm`.
The `date_measured` column holds the date the measurement was taken,
and is of type `datetime64`.
The `ppm` column holds the value of CO$_{\text{2}}$ in parts per million
that was measured on each date, and is type `float64`; this is the usual
type for decimal numbers.

```{index} dates and times
```

```{note}
`read_csv` was able to parse the `date_measured` column into the
`datetime` vector type because it was entered
in the international standard date format,
called ISO 8601, which lists dates as `year-month-day` and we used `parse_dates=True`.
`datetime` vectors are `double` vectors with special properties that allow
them to handle dates correctly.
For example, `datetime` type vectors allow functions like `altair`
to treat them as numeric dates and not as character vectors,
even though they contain non-numeric characters
(e.g., in the `date_measured` column in the `co2_df` data frame).
This means Python will not accidentally plot the dates in the wrong order
(i.e., not alphanumerically as would happen if it was a character vector).
More about dates and times can be viewed [here](https://wesmckinney.com/book/time-series.html).
```

Since we are investigating a relationship between two variables
(CO$_{\text{2}}$ concentration and date),
a scatter plot is a good place to start.
Scatter plots show the data as individual points with `x` (horizontal axis)
and `y` (vertical axis) coordinates.
Here, we will use the measurement date as the `x` coordinate
and the CO$_{\text{2}}$ concentration as the `y` coordinate.
We create a chart with the `alt.Chart()` function.
There are a few basic aspects of a plot that we need to specify:

```{index} altair; graphical mark, altair; encoding channel, altair; mark_point
```

- The name of the **data frame** to visualize.
    - Here, we specify the `co2_df` data frame as an argument to `alt.Chart`
- The **graphical mark**, which specifies how the mapped data should be displayed.
    - To create a graphical mark, we use `Chart.mark_*` methods (see the
      [altair reference](https://altair-viz.github.io/user_guide/marks.html)
      for a list of graphical mark).
    - Here, we use the `mark_point` function to visualize our data as a scatter plot.
- The **encoding channels**, which tells `altair` how the columns in the data frame map to visual properties in the chart.
    - To create an encoding, we use the `encode` function.
    - The `encode` method builds a key-value mapping between encoding channels (such as x, y) to fields in the data set, accessed by field name (column names)
    - Here, we set the `x` axis of the plot to the `date_measured` variable,
      and on the `y` axis, we plot the `ppm` variable.
    - For the y-axis, we also provided the method
      `scale(zero=False)`. By default, `altair` chooses the y-limits
      based on the data and will keep `y=0` in view.
      This is often a helpful default, but here it makes it
      difficult to see any trends in our data since the smallest value is >300
      ppm. So by providing `scale(zero=False)`, we tell altair to
      choose a reasonable lower bound based on our data, and that lower bound
      doesn't have to be zero.
    - To change the properties of the encoding channels,
      we need to leverage the helper functions `alt.Y` and `alt.X`.
      These helpers have the role of customizing things like order, titles, and scales.
      Here, we use `alt.Y` to change the domain of the y-axis,
      so that it starts from the lowest value in the `date_measured` column
      rather than from zero.

```{code-cell} ipython3
co2_scatter = alt.Chart(co2_df).mark_point().encode(
    x="date_measured",
    y=alt.Y("ppm").scale(zero=False)
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("co2_scatter", co2_scatter, display=False)
```

:::{glue:figure} co2_scatter
:figwidth: 700px
:name: co2_scatter

Scatter plot of atmospheric concentration of CO$_{2}$ over time.
:::

The visualization in {numref}`co2_scatter`
shows a clear upward trend
in the atmospheric concentration of CO$_{\text{2}}$ over time.
This plot answers the first part of our question in the affirmative,
but that appears to be the only conclusion one can make
from the scatter visualization.

One important thing to note about this data is that one of the variables
we are exploring is time.
Time is a special kind of quantitative variable
because it forces additional structure on the data&mdash;the
data points have a natural order.
Specifically, each observation in the data set has a predecessor
and a successor, and the order of the observations matters; changing their order
alters their meaning.
In situations like this, we typically use a line plot to visualize
the data. Line plots connect the sequence of `x` and `y` coordinates
of the observations with line segments, thereby emphasizing their order.

```{index} altair; mark_line
```

We can create a line plot in `altair` using the `mark_line` function.
Let's now try to visualize the `co2_df` as a line plot
with just the default arguments:

```{code-cell} ipython3
co2_line = alt.Chart(co2_df).mark_line().encode(
    x="date_measured",
    y=alt.Y("ppm").scale(zero=False)
)
```


```{code-cell} ipython3
:tags: ["remove-cell"]
glue("co2_line", co2_line, display=False)
```

:::{glue:figure} co2_line
:figwidth: 700px
:name: co2_line

Line plot of atmospheric concentration of CO$_{2}$ over time.
:::

```{index} overplotting
```

Aha! {numref}`co2_line` shows us there *is* another interesting
phenomenon in the data: in addition to increasing over time, the concentration
seems to oscillate as well.  Given the visualization as it is now, it is still
hard to tell how fast the oscillation is, but nevertheless, the line seems to
be a better choice for answering the question than the scatter plot was. The
comparison between these two visualizations also illustrates a common issue with
scatter plots: often, the points are shown too close together or even on top of
one another, muddling information that would otherwise be clear
(*overplotting*).

```{index} altair; alt.X, altair; alt.Y, altair; configure_axis
```

Now that we have settled on the rough details of the visualization, it is time
to refine things. This plot is fairly straightforward, and there is not much
visual noise to remove. But there are a few things we must do to improve
clarity, such as adding informative axis labels and making the font a more
readable size.  To add axis labels, we use the `title` method along with `alt.X` and `alt.Y` functions. To
change the font size, we use the `configure_axis` function with the
`titleFontSize` argument.

```{code-cell} ipython3
co2_line_labels = alt.Chart(co2_df).mark_line().encode(
    x=alt.X("date_measured").title("Year"),
    y=alt.Y("ppm").scale(zero=False).title("Atmospheric CO2 (ppm)")
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("co2_line_labels", co2_line_labels, display=False)
```

:::{glue:figure} co2_line_labels
:figwidth: 700px
:name: co2_line_labels

Line plot of atmospheric concentration of CO$_{2}$ over time with clearer axes and labels.
:::

```{note}
The `configure_*` functions in `altair` support additional customization,
such as updating the size of the plot, changing
the font color, and many other options that can be viewed
[here](https://altair-viz.github.io/user_guide/configuration.html).
```

```{index} altair; alt.Scale
```

Finally, let's see if we can better understand the oscillation by changing the
visualization slightly. Note that it is totally fine to use a small number of
visualizations to answer different aspects of the question you are trying to
answer. We will accomplish this by using *scale*,
another important feature of `altair` that easily transforms the different
variables and set limits.
In particular, here, we will use the `alt.Scale` function to zoom in
on just a few years of data (say, 1990-1995). The
`domain` argument takes a list of length two
to specify the upper and lower bounds to limit the axis.
We also added the argument `clip=True` to `mark_line`. This tells `altair`
to "clip" (remove) the data outside of the specified domain that we set so that it doesn't
extend past the plot area.
Since we are using both the `scale` and `title` method on the encodings
we stack them on separate lines to make the code easier to read.

```{code-cell} ipython3
co2_line_scale = alt.Chart(co2_df).mark_line(clip=True).encode(
    x=alt.X("date_measured")
        .scale(domain=["1990", "1995"])
        .title("Measurement Date"),
    y=alt.Y("ppm")
        .scale(zero=False)
        .title("Atmospheric CO2 (ppm)")
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("co2_line_scale", co2_line_scale, display=False)
```

:::{glue:figure} co2_line_scale
:figwidth: 700px
:name: co2_line_scale

Line plot of atmospheric concentration of CO$_{2}$ from 1990 to 1995.
:::

Interesting! It seems that each year, the atmospheric CO$_{\text{2}}$ increases
until it reaches its peak somewhere around April, decreases until around late
September, and finally increases again until the end of the year. In Hawaii,
there are two seasons: summer from May through October, and winter from
November through April.  Therefore, the oscillating pattern in CO$_{\text{2}}$
matches up fairly closely with the two seasons.

A useful analogy to constructing a data visualization is painting a picture.
We start with a blank canvas,
and the first thing we do is prepare the surface
for our painting by adding primer.
In our data visualization this is akin to calling `alt.Chart`
and specifying the data set we will be using.
Next, we sketch out the background of the painting.
In our data visualization,
this would be when we map data to the axes in the `encode` function.
Then we add our key visual subjects to the painting.
In our data visualization,
this would be the graphical marks (e.g., `mark_point`, `mark_line`, etc.).
And finally, we work on adding details and refinements to the painting.
In our data visualization this would be when we fine tune axis labels,
change the font, adjust the point size, and do other related things.



### Scatter plots: the Old Faithful eruption time data set

```{index} Old Faithful
```

The `faithful` data set contains measurements
of the waiting time between eruptions
and the subsequent eruption duration (in minutes) of the Old Faithful
geyser in Yellowstone National Park, Wyoming, United States.
First, we will read the data and then answer the following question:

```{index} question; visualization
```

**Question:** Is there a relationship between the waiting time before an eruption
and the duration of the eruption?

```{code-cell} ipython3
faithful = pd.read_csv("data/faithful.csv")
faithful

```

Here again, we investigate the relationship between two quantitative variables
(waiting time and eruption time).
But if you look at the output of the data frame,
you'll notice that unlike time in the Mauna Loa CO$_{\text{2}}$ data set,
neither of the variables here have a natural order to them.
So a scatter plot is likely to be the most appropriate
visualization. Let's create a scatter plot using the `altair`
package with the `waiting` variable on the horizontal axis, the `eruptions`
variable on the vertical axis, and `mark_point` as the graphical mark.
The result is shown in {numref}`faithful_scatter`.

```{code-cell} ipython3
faithful_scatter = alt.Chart(faithful).mark_point().encode(
    x="waiting",
    y="eruptions"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("faithful_scatter", faithful_scatter, display=False)
```

:::{glue:figure} faithful_scatter
:figwidth: 700px
:name: faithful_scatter

Scatter plot of waiting time and eruption time.
:::

We can see in {numref}`faithful_scatter` that the data tend to fall
into two groups: one with short waiting and eruption times, and one with long
waiting and eruption times. Note that in this case, there is no overplotting:
the points are generally nicely visually separated, and the pattern they form
is clear.
In order to refine the visualization, we need only to add axis
labels and make the font more readable.

```{code-cell} ipython3
faithful_scatter_labels = alt.Chart(faithful).mark_point().encode(
    x=alt.X("waiting").title("Waiting Time (mins)"),
    y=alt.Y("eruptions").title("Eruption Duration (mins)")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("faithful_scatter_labels", faithful_scatter_labels, display=False)
```

:::{glue:figure} faithful_scatter_labels
:figwidth: 700px
:name: faithful_scatter_labels

Scatter plot of waiting time and eruption time with clearer axes and labels.
:::


We can change the size of the point and color of the plot by specifying `mark_point(size=10, color="black")`.

```{code-cell} ipython3
faithful_scatter_labels_black = alt.Chart(faithful).mark_point(size=10, color="black").encode(
    x=alt.X("waiting").title("Waiting Time (mins)"),
    y=alt.Y("eruptions").title("Eruption Duration (mins)")
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("faithful_scatter_labels_black", faithful_scatter_labels_black, display=False)
```

:::{glue:figure} faithful_scatter_labels_black
:figwidth: 700px
:name: faithful_scatter_labels_black

Scatter plot of waiting time and eruption time with black points.
:::

