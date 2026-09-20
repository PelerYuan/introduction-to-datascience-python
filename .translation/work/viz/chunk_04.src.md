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

## Saving the visualization

<font size="5">*Choose the right output format for your needs*</font>

```{index} see: bitmap; raster graphics
```

```{index} raster graphics, vector graphics
```

Just as there are many ways to store data sets, there are many ways to store
visualizations and images.  Which one you choose can depend on several factors,
such as file size/type limitations (e.g., if you are submitting your
visualization as part of a conference paper or to a poster printing shop) and
where it will be displayed (e.g., online, in a paper, on a poster, on a
billboard, in talk slides).  Generally speaking, images come in two flavors:
*raster* formats
and *vector* formats.

```{index} raster graphics; file types
```

**Raster** images are represented as a 2-D grid of square pixels, each
with its own color. Raster images are often *compressed* before storing so they
take up less space. A compressed format is *lossy* if the image cannot be
perfectly re-created when loading and displaying, with the hope that the change
is not noticeable. *Lossless* formats, on the other hand, allow a perfect
display of the original image.

- *Common file types:*
    - [JPEG](https://en.wikipedia.org/wiki/JPEG) (`.jpg`, `.jpeg`): lossy, usually used for photographs
    - [PNG](https://en.wikipedia.org/wiki/Portable_Network_Graphics) (`.png`): lossless, usually used for plots / line drawings
    - [BMP](https://en.wikipedia.org/wiki/BMP_file_format) (`.bmp`): lossless, raw image data, no compression (rarely used)
    - [TIFF](https://en.wikipedia.org/wiki/TIFF) (`.tif`, `.tiff`): typically lossless, no compression, used mostly in graphic arts, publishing
- *Open-source software:* [GIMP](https://www.gimp.org/)

```{index} vector graphics; file types
```

**Vector** images are represented as a collection of mathematical
objects (lines, surfaces, shapes, curves). When the computer displays the image, it
redraws all of the elements using their mathematical formulas.

- *Common file types:*
    - [SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) (`.svg`): general-purpose use
    - [EPS](https://en.wikipedia.org/wiki/Encapsulated_PostScript) (`.eps`), general-purpose use (rarely used)
- *Open-source software:* [Inkscape](https://inkscape.org/)

Raster and vector images have opposing advantages and disadvantages. A raster
image of a fixed width / height takes the same amount of space and time to load
regardless of what the image shows (the one caveat is that the compression algorithms may
shrink the image more or run faster for certain images). A vector image takes
space and time to load corresponding to how complex the image is, since the
computer has to draw all the elements each time it is displayed. For example,
if you have a scatter plot with 1 million points stored as an SVG file, it may
take your computer some time to open the image. On the other hand, you can zoom
into / scale up vector graphics as much as you like without the image looking
bad, while raster images eventually start to look "pixelated."

```{index} PDF
```

```{index} see: portable document format; PDF
```

```{note}
The portable document format [PDF](https://en.wikipedia.org/wiki/PDF) (`.pdf`) is commonly used to
store *both* raster and vector formats. If you try to open a PDF and it's taking a long time
to load, it may be because there is a complicated vector graphics image that your computer is rendering.
```

Let's learn how to save plot images to `.png` and `.svg` file formats using the
`faithful_scatter_labels` scatter plot of the [Old Faithful data set](https://www.stat.cmu.edu/~larry/all-of-statistics/=data/faithful.dat)
{cite:p}`faithfuldata` that we created earlier, shown in {numref}`faithful_scatter_labels`.
To save the plot to a file, we can use the `save`
method. The `save` method takes the path to the filename where you would like to
save the file (e.g., `img/viz/filename.png` to save a file named `filename.png` to the `img/viz/` directory).
The kind of image to save is specified by the file extension.  For example, to
create a PNG image file, we specify that the file extension is `.png`.  Below
we demonstrate how to save PNG and SVG file types for the
`faithful_scatter_labels` plot.

```{code-cell} ipython3
faithful_scatter_labels.save("img/viz/faithful_plot.png")
faithful_scatter_labels.save("img/viz/faithful_plot.svg")
```

```{code-cell} ipython3
:tags: [remove-cell]

import os
import numpy as np
png_size = np.round(os.path.getsize("img/viz/faithful_plot.png")/(1024*1024), 2)
svg_size = np.round(os.path.getsize("img/viz/faithful_plot.svg")/(1024*1024), 2)

glue("png_size", "{:.2f}".format(png_size))
glue("svg_size", "{:.2f}".format(svg_size))
```

```{list-table} File sizes of the scatter plot of the Old Faithful data set when saved as different file formats.
:header-rows: 1
:name: png-vs-svg-table

* - Image type
  - File type
  - Image size
* - Raster
  - PNG
  - {glue:text}`png_size` MB
* - Vector
  - SVG
  - {glue:text}`svg_size` MB
```

Take a look at the file sizes in {numref}`png-vs-svg-table`.
Wow, that's quite a difference! In this case, the `.png` image is almost 4 times
smaller than the `.svg` image. Since there are a decent number of points in the plot,
the vector graphics format image (`.svg`) is bigger than the raster image (`.png`), which
just stores the image data itself.
In {numref}`png-vs-svg`, we show what
the images look like when we zoom in to a rectangle with only 3 data points.
You can see why vector graphics formats are so useful: because they're just
based on mathematical formulas, vector graphics can be scaled up to arbitrary
sizes.  This makes them great for presentation media of all sizes, from papers
to posters to billboards.

```{figure} img/viz/png-vs-svg.png
---
height: 400px
name: png-vs-svg
---
Zoomed in `faithful`, raster (PNG, left) and vector (SVG, right) formats.
```

