Histogram of Michelson's speed of light data colored by experiment as a categorical variable.
:::

Unfortunately, the attempt to separate out the experiment number visually has
created a bit of a mess. All of the colors in {numref}`morley_hist_categorical` are blending together, and although it is
possible to derive *some* insight from this (e.g., experiments 1 and 3 had some
of the most incorrect measurements), it isn't the clearest way to convey our
message and answer the question. Let's try a different strategy of creating
grid of separate histogram plots.

+++

```{index} altair; facet
```

We can use the `facet` function to create a chart
that has multiple subplots arranged in a grid.
The argument to `facet` specifies the variable(s) used to split the plot
into subplots (`Expt` in the code below),
and how many columns there should be in the grid.
In this example, we chose to
arrange our plots in a single column (`columns=1`) since this makes it easier for
us to compare the location of the histograms along the `x`-axis
in the different subplots.
We also reduce the height of each chart
so that they all fit in the same view.
Note that we are re-using the chart we created just above,
instead of re-creating the same chart from scratch.
We also explicitly specify that `facet` is a categorical variable
since faceting should only be done with categorical variables.

```{code-cell} ipython3
morley_hist_facet = morley_hist_categorical.properties(
    height=100
).facet(
    "Expt:N",
    columns=1
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_facet", morley_hist_facet, display=True)
```

:::{glue:figure} morley_hist_facet
:figwidth: 700px
:name: morley_hist_facet

Histogram of Michelson's speed of light data split vertically by experiment.
:::

The visualization in {numref}`morley_hist_facet`
makes it clear how accurate the different experiments were
with respect to one another.
The most variable measurements came from Experiment 1,
where the measurements ranged from about 650&ndash;1050 km/sec.
The least variable measurements came from Experiment 2,
where the measurements ranged from about 750&ndash;950 km/sec.
The most different experiments still obtained quite similar overall results!

```{index} altair; alt.X, altair; alt.Y, altair; configure_axis
```

There are three finishing touches to make this visualization even clearer.
First and foremost, we need to add informative axis labels using the `alt.X`
and `alt.Y` function, and increase the font size to make it readable using the
`configure_axis` function. We can also add a title; for a `facet` plot, this is
done by providing the `title` to the facet function. Finally, and perhaps most
subtly, even though it is easy to compare the experiments on this plot to one
another, it is hard to get a sense of just how accurate all the experiments
were overall. For example, how accurate is the value 800 on the plot, relative
to the true speed of light?  To answer this question, we'll
transform our data to a relative measure of error rather than an absolute measurement.

```{code-cell} ipython3
speed_of_light = 299792.458
morley_df["RelativeError"] = (
    100 * (299000 + morley_df["Speed"] - speed_of_light) / speed_of_light
)
morley_df
```

```{code-cell} ipython3
morley_hist_rel = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X("RelativeError")
        .bin()
        .title("Relative Error (%)"),
    y=alt.Y("count()").title("# Measurements"),
    color=alt.Color("Expt:N").title("Experiment ID")
)

# Recreating v_line to indicate that the speed of light is at 0% relative error
v_line = alt.Chart(morley_df).mark_rule(strokeDash=[6], size=1.5).encode(
    x=alt.datum(0)
)

morley_hist_relative = (morley_hist_rel + v_line).properties(
    height=100
).facet(
    "Expt:N",
    columns=1,
    title="Histogram of relative error of Michelson’s speed of light data"
)

```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_relative", morley_hist_relative, display=True)
```

:::{glue:figure} morley_hist_relative
:figwidth: 700px
:name: morley_hist_relative

Histogram of relative error split vertically by experiment with clearer axes and labels
:::

Wow, impressive! These measurements of the speed of light from 1879 had errors
around *0.05%* of the true speed. {numref}`morley_hist_relative` shows you that
even though experiments 2 and 5 were perhaps the most accurate, all of the
experiments did quite an admirable job given the technology available at the time.

#### Choosing a binwidth for histograms

When you create a histogram in `altair`, it tries to choose a reasonable number of bins.
We can change the number of bins by using the `maxbins` parameter
inside the `bin` method.

```{index} altair; maxbins
```

```{code-cell} ipython3
morley_hist_maxbins = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X("RelativeError").bin(maxbins=30),
    y="count()"
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_maxbins", morley_hist_maxbins, display=False)
```

:::{glue:figure} morley_hist_maxbins
:figwidth: 700px
:name: morley_hist_maxbins

Histogram of Michelson's speed of light data.
:::


But what number of bins is the right one to use?
Unfortunately there is no hard rule for what the right bin number
or width is. It depends entirely on your problem; the *right* number of bins
or bin width is
the one that *helps you answer the question* you asked.
Choosing the correct setting for your problem
is something that commonly takes iteration.
It's usually a good idea to try out several `maxbins` to see which one
most clearly captures your data in the context of the question
you want to answer.

To get a sense for how different bin affect visualizations,
let's experiment with the histogram that we have been working on in this section.
In {numref}`morley_hist_max_bins`,
we compare the default setting with three other histograms where we set the
`maxbins` to 200, 70 and 5.
In this case, we can see that both the default number of bins
and the `maxbins=70` of  are effective for helping to answer our question.
On the other hand, the `maxbins=200` and `maxbins=5` are too small and too big, respectively.

```{code-cell} ipython3
:tags: ["remove-cell"]
morley_hist_default = alt.Chart(morley_df).mark_bar().encode(
    x=alt.X(
        "RelativeError",
        title="Relative error (%)",
        bin=True
    ),
    y=alt.Y(
        "count()",
        stack=False,
        title="# Measurements"
    ),
    color=alt.Color(
        "Expt:N",
        title="Experiment ID",
        legend=None
    )
).properties(height=100, width=250)

morley_hist_max_bins = alt.vconcat(
    alt.hconcat(
        (morley_hist_default + v_line).facet(
            "Expt:N",
            columns=1,
            title=alt.TitleParams("Default (bin=True)", fontSize=16, anchor="middle", dx=15)
        ),
        (morley_hist_default.encode(
            x=alt.X(
                "RelativeError",
                bin=alt.Bin(maxbins=5),
                title="Relative error (%)"
            )
        ) + v_line).facet(
            "Expt:N",
            columns=1,
            title=alt.TitleParams("maxbins=5", fontSize=16, anchor="middle", dx=15)
        ),
    ),
    alt.hconcat(
        (morley_hist_default.encode(
            x=alt.X(
                "RelativeError",
                bin=alt.Bin(maxbins=70),
                title="Relative error (%)"
            )
        ) + v_line).facet(
            "Expt:N",
            columns=1,
            title=alt.TitleParams("maxbins=70", fontSize=16, anchor="middle", dx=15)
        ),
        (morley_hist_default.encode(
            x=alt.X(
                "RelativeError",
                bin=alt.Bin(maxbins=200),
                title="Relative error (%)"
            )
        ) + v_line).facet(
            "Expt:N",
            columns=1,
            title=alt.TitleParams("maxbins=200", fontSize=16, anchor="middle", dx=15)
        )
    ),
    spacing=50
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
glue("morley_hist_max_bins", morley_hist_max_bins, display=True)
```

:::{glue:figure} morley_hist_max_bins
:figwidth: 700px
:name: morley_hist_max_bins

Effect of varying number of max bins on histograms.
:::

## Explaining the visualization
<font size="5">*Tell a story*</font>

Typically, your visualization will not be shown entirely on its own, but rather
it will be part of a larger presentation.  Further, visualizations can provide
supporting information for any aspect of a presentation, from opening to
conclusion.  For example, you could use an exploratory visualization in the
opening of the presentation to motivate your choice of a more detailed data
analysis / model, a visualization of the results of your analysis to show what
your analysis has uncovered, or even one at the end of a presentation to help
suggest directions for future work.

```{index} visualization; explanation
```

Regardless of where it appears, a good way to discuss your visualization is as
a story:

1) Establish the setting and scope, and describe why you did what you did.
2) Pose the question that your visualization answers. Justify why the question is important to answer.
3) Answer the question using your visualization. Make sure you describe *all* aspects of the visualization (including describing the axes). But you
   can emphasize different aspects based on what is important to answer your question:
    - **trends (lines):** Does a line describe the trend well? If so, the trend is *linear*, and if not, the trend is *nonlinear*. Is the trend increasing, decreasing, or neither?
                        Is there a periodic oscillation (wiggle) in the trend? Is the trend noisy (does the line "jump around" a lot) or smooth?
    - **distributions (scatters, histograms):** How spread out are the data? Where are they centered, roughly? Are there any obvious "clusters" or "subgroups", which would be visible as multiple bumps in the histogram?
    - **distributions of two variables (scatters):** Is there a clear / strong relationship between the variables (points fall in a distinct pattern), a weak one (points fall in a pattern but there is some noise), or no discernible
      relationship (the data are too noisy to make any conclusion)?
    - **amounts (bars):** How large are the bars relative to one another? Are there patterns in different groups of bars?
4) Summarize your findings, and use them to motivate whatever you will discuss next.

Below are two examples of how one might take these four steps in describing the example visualizations that appeared earlier in this chapter.
Each of the steps is denoted by its numeral in parentheses, e.g. (3).

```{index} Mauna Loa
```

**Mauna Loa Atmospheric CO$_{\text{2}}$ Measurements:** (1) Many
current forms of energy generation and conversion&mdash;from automotive
engines to natural gas power plants&mdash;rely on burning fossil fuels and produce
greenhouse gases, typically primarily carbon dioxide (CO$_{\text{2}}$), as a
byproduct. Too much of these gases in the Earth's atmosphere will cause it to
trap more heat from the sun, leading to global warming. (2) In order to assess
how quickly the atmospheric concentration of CO$_{\text{2}}$ is increasing over
time, we (3) used a data set from the Mauna Loa observatory in Hawaii,
consisting of CO$_{\text{2}}$ measurements from 1980 to 2020. We plotted the
measured concentration of CO$_{\text{2}}$ (on the vertical axis) over time (on
the horizontal axis). From this plot, you can see a clear, increasing, and
generally linear trend over time. There is also a periodic oscillation that
occurs once per year and aligns with Hawaii's seasons, with an amplitude that
is small relative to the growth in the overall trend. This shows that
atmospheric CO$_{\text{2}}$ is clearly increasing over time, and (4) it is
perhaps worth investigating more into the causes.

```{index} Michelson speed of light
```

**Michelson Light Speed Experiments:** (1) Our
modern understanding of the physics of light has advanced significantly from
the late 1800s when Michelson and Morley's experiments first demonstrated that
it had a finite speed. We now know, based on modern experiments, that it moves at
roughly 299,792.458 kilometers per second. (2) But how accurately were we first
able to measure this fundamental physical constant, and did certain experiments
produce more accurate results than others?  (3) To better understand this, we
plotted data from 5 experiments by Michelson in 1879, each with 20 trials, as
histograms stacked on top of one another. The horizontal axis shows the
error of the measurements relative to the true speed of light as we know it
today, expressed as a percentage.  From this visualization, you can see that
most results had relative errors of at most 0.05%. You can also see that
experiments 1 and 3 had measurements that were the farthest from the true
value, and experiment 5 tended to provide the most consistently accurate
result. (4) It would be worth further investigating the differences between
these experiments to see why they produced different results.

