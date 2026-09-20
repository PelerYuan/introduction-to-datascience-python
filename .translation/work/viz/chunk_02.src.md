+++

### Axis transformation and colored scatter plots: the Canadian languages data set

```{index} Canadian languages
```

Recall the `can_lang` data set {cite:p}`timbers2020canlang` from {numref}`Chapters %s <intro>`, {numref}`%s <reading>`, and {numref}`%s <wrangling>`.
It contains counts of languages from the 2016
Canadian census.

```{index} question; visualization
```

**Question:** Is there a relationship between
the percentage of people who speak a language as their mother tongue and
the percentage for whom that is the primary language spoken at home?
And is there a pattern in the strength of this relationship in the
higher-level language categories (Official languages, Aboriginal languages, or
non-official and non-Aboriginal languages)?

To get started, we will read and inspect the data:

```{code-cell} ipython3
:tags: ["output_scroll"]
can_lang = pd.read_csv("data/can_lang.csv")
can_lang
```

```{code-cell} ipython3
:tags: ["remove-cell"]
# use only nonzero entries (to avoid issues with log scale), and wrap in a pd.DataFrame to prevent copy/view warnings later
can_lang = pd.DataFrame(can_lang[(can_lang["most_at_home"] > 0) & (can_lang["mother_tongue"] > 0)])
```

```{index} altair; mark_circle
```

We will begin with a scatter plot of the `mother_tongue` and `most_at_home` columns from our data frame.
As we have seen in the scatter plots in the previous section,
the default behavior of `mark_point` is to draw the outline of each point.
If we would like to fill them in,
we can pass the argument `filled=True` to `mark_point`
or use the shortcut `mark_circle`.
Whether to fill points or not is mostly a matter of personal preferences,
although hollow points can make it easier to see individual points
when there are many overlapping points in a chart.
The resulting plot is shown in {numref}`can_lang_plot`.

```{code-cell} ipython3
can_lang_plot = alt.Chart(can_lang).mark_circle().encode(
    x="most_at_home",
    y="mother_tongue"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("can_lang_plot", can_lang_plot, display=False)
```

:::{glue:figure} can_lang_plot
:figwidth: 700px
:name: can_lang_plot

Scatter plot of number of Canadians reporting a language as their mother tongue vs the primary language at home
:::

To make an initial improvement in the interpretability
of {numref}`can_lang_plot`, we should
replace the default axis
names with more informative labels.
To make the axes labels on the plots more readable,
we can print long labels over multiple lines.
To achieve this, we specify the title as a list of strings
where each string in the list will correspond to a new line of text.
We can also increase the font size to further
improve readability.

```{index} altair; multiline labels
```

```{code-cell} ipython3
can_lang_plot_labels = alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home")
        .title(["Language spoken most at home", "(number of Canadian residents)"]),
    y=alt.Y("mother_tongue")
        .scale(zero=False)
        .title(["Mother tongue", "(number of Canadian residents)"])
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("can_lang_plot_labels", can_lang_plot_labels, display=False)
```

:::{glue:figure} can_lang_plot_labels
:figwidth: 700px
:name: can_lang_plot_labels

Scatter plot of number of Canadians reporting a language as their mother tongue vs the primary language at home with x and y labels.
:::


```{code-cell} ipython3
:tags: ["remove-cell"]
import numpy as np
numlang_speakers_max=int(max(can_lang["mother_tongue"]))
print(numlang_speakers_max)
numlang_speakers_min = int(min(can_lang["mother_tongue"]))
print(numlang_speakers_min)
log_result = int(np.floor(np.log10(numlang_speakers_max/numlang_speakers_min)))
print(log_result)
glue("numlang_speakers_max", "{0:,.0f}".format(numlang_speakers_max))
glue("numlang_speakers_min", "{0:,.0f}".format(numlang_speakers_min))
glue("log_result", log_result)
```

Okay! The axes and labels in {numref}`can_lang_plot_labels` are
much more readable and interpretable now. However, the scatter points themselves could use
some work; most of the 214 data points are bunched
up in the lower left-hand side of the visualization. The data is clumped because
many more people in Canada speak English or French (the two points in
the upper right corner) than other languages.
In particular, the most common mother tongue language
has {glue:text}`numlang_speakers_max` speakers,
while the least common has only {glue:text}`numlang_speakers_min`.
That's a six-decimal-place difference
in the magnitude of these two numbers!
We can confirm that the two points in the upper right-hand corner correspond
to Canada's two official languages by filtering the data:

```{index} DataFrame; loc[]
```

```{code-cell} ipython3
:tags: ["output_scroll"]
can_lang.loc[
    (can_lang["language"]=="English")
    | (can_lang["language"]=="French")
]
```

```{index} logarithmic scale, altair; logarithmic scaling
```

Recall that our question about this data pertains to *all* languages;
so to properly answer our question,
we will need to adjust the scale of the axes so that we can clearly
see all of the scatter points.
In particular, we will improve the plot by adjusting the horizontal
and vertical axes so that they are on a **logarithmic** (or **log**) scale.
Log scaling is useful when your data take both *very large* and *very small* values,
because it helps space out small values and squishes larger values together.
For example, $\log_{10}(1) = 0$, $\log_{10}(10) = 1$, $\log_{10}(100) = 2$, and $\log_{10}(1000) = 3$;
on the logarithmic scale,
the values 1, 10, 100, and 1000 are all the same distance apart!
So we see that applying this function is moving big values closer together
and moving small values farther apart.
Note that if your data can take the value 0, logarithmic scaling may not
be appropriate (since `log10(0)` is `-inf` in Python). There are other ways to transform
the data in such a case, but these are beyond the scope of the book.

We can accomplish logarithmic scaling in the `altair` visualization
using the argument `type="log"` in the scale method.

```{code-cell} ipython3
can_lang_plot_log = alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home")
        .scale(type="log")
        .title(["Language spoken most at home", "(number of Canadian residents)"]),
    y=alt.Y("mother_tongue")
        .scale(type="log")
        .title(["Mother tongue", "(number of Canadian residents)"])
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("can_lang_plot_log", can_lang_plot_log, display=False)
```

:::{glue:figure} can_lang_plot_log
:figwidth: 700px
:name: can_lang_plot_log

Scatter plot of number of Canadians reporting a language as their mother tongue vs the primary language at home with log-adjusted x and y axes.
:::

You will notice two things in the chart above,
changing the axis to log creates many axis ticks and gridlines,
which makes the appearance of the chart rather noisy
and it is hard to focus on the data.
You can also see that the second last tick label is missing on the x-axis;
Altair dropped it because there wasn't space to fit in all the large numbers next to each other.
It is also hard to see if the label for 100,000,000 is for the last or second last tick.
To fix these issue,
we can limit the number of ticks and gridlines to only include the seven major ones,
and change the number formatting to include a suffix which makes the labels shorter.

```{index} altair; tick count, altair; tick formatting
```

```{code-cell} ipython3
can_lang_plot_log_revised = alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home")
        .scale(type="log")
        .title(["Language spoken most at home", "(number of Canadian residents)"])
        .axis(tickCount=7, format="s"),
    y=alt.Y("mother_tongue")
        .scale(type="log")
        .title(["Mother tongue", "(number of Canadian residents)"])
        .axis(tickCount=7, format="s")
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("can_lang_plot_log_revised", can_lang_plot_log_revised, display=False)
```

:::{glue:figure} can_lang_plot_log_revised
:figwidth: 700px
:name: can_lang_plot_log_revised

Scatter plot of number of Canadians reporting a language as their mother tongue vs the primary language at home with log-adjusted x and y axes. Only the major gridlines are shown. The suffix "k" indicates 1,000 ("kilo"), while the suffix "M" indicates 1,000,000 ("million").
:::


```{code-cell} ipython3
:tags: ["remove-cell"]
english_mother_tongue = can_lang.loc[can_lang["language"]=="English"].mother_tongue.values[0]
census_popn = int(35151728)
result = round((english_mother_tongue/census_popn)*100,2)
glue("english_mother_tongue", "{0:,.0f}".format(english_mother_tongue))
glue("census_popn", "{0:,.0f}".format(census_popn))
glue("result", "{:.2f}".format(result))

```

Similar to some of the examples in {numref}`Chapter %s <wrangling>`,
we can convert the counts to percentages to give them context
and make them easier to understand.
We can do this by dividing the number of people reporting a given language
as their mother tongue or primary language at home
by the number of people who live in Canada and multiplying by 100\%.
For example,
the percentage of people who reported that their mother tongue was English
in the 2016 Canadian census
was {glue:text}`english_mother_tongue` / {glue:text}`census_popn` $\times$
100\% = {glue:text}`result`\%

Below we assign the percentages of people reporting a given
language as their mother tongue and primary language at home
to two new columns in the `can_lang` data frame. Since the new columns are appended to the
end of the data table, we selected the new columns after the transformation so
you can clearly see the mutated output from the table.
Note that we formatted the number for the Canadian population
using `_` so that it is easier to read;
this does not affect how Python interprets the number
and is just added for readability.

```{index} DataFrame; column assignment, DataFrame; []
```

```{code-cell} ipython3
canadian_population = 35_151_728
can_lang["mother_tongue_percent"] = can_lang["mother_tongue"]/canadian_population*100
can_lang["most_at_home_percent"] = can_lang["most_at_home"]/canadian_population*100
can_lang[["mother_tongue_percent", "most_at_home_percent"]]
```

Next, we will edit the visualization to use the percentages we just computed
(and change our axis labels to reflect this change in
units). {numref}`can_lang_plot_percent` displays
the final result.
Here all the tick labels fit by default so we are not changing the labels to include suffixes.
Note that suffixes can also be harder to understand,
so it is often advisable to avoid them (particularly for small quantities)
unless you are communicating to a technical audience.

```{code-cell} ipython3
can_lang_plot_percent = alt.Chart(can_lang).mark_circle().encode(
    x=alt.X("most_at_home_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Language spoken most at home", "(percentage of Canadian residents)"]),
    y=alt.Y("mother_tongue_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Mother tongue", "(percentage of Canadian residents)"]),
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
# Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
glue("can_lang_plot_percent", can_lang_plot_percent.properties(height=320, width=420), display=False)
```

:::{glue:figure} can_lang_plot_percent
:figwidth: 700px
:name: can_lang_plot_percent

Scatter plot of percentage of Canadians reporting a language as their mother tongue vs the primary language at home.
:::

{numref}`can_lang_plot_percent` is the appropriate
visualization to use to answer the first question in this section, i.e.,
whether there is a relationship between the percentage of people who speak
a language as their mother tongue and the percentage for whom that
is the primary language spoken at home.
To fully answer the question, we need to use
 {numref}`can_lang_plot_percent`
to assess a few key characteristics of the data:

```{index} relationship; positive, relationship; negative, relationship; none
```

- **Direction:** if the y variable tends to increase when the x variable increases, then y has a **positive** relationship with x. If
  y tends to decrease when x increases, then y has a **negative** relationship with x. If y does not meaningfully increase or decrease
  as x increases, then y has **little or no** relationship with x.

```{index} relationship; strong, relationship; weak
```

- **Strength:** if the y variable *reliably* increases, decreases, or stays flat as x increases,
  then the relationship is **strong**. Otherwise, the relationship is **weak**. Intuitively,
  the relationship is strong when the scatter points are close together and look more like a "line" or "curve" than a "cloud."

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

