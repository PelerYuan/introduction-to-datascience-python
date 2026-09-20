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

