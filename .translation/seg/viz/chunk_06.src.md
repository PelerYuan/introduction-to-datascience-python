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

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Effective data visualization" row. You can preview a
non-interactive version of the worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.

## Additional resources

- The [altair documentation](https://altair-viz.github.io/) {cite:p}`altair` is
  where you should look if you want to learn more about the functions in this
  chapter, the full set of arguments you can use, and other related functions.
- The [*Fundamentals of Data Visualization*](https://clauswilke.com/dataviz/) {cite:p}`wilkeviz` has
  a wealth of information on designing effective visualizations. It is not
  specific to any particular programming language or library. If you want to
  improve your visualization skills, this is the next place to look.
- The [dates and times](https://wesmckinney.com/book/time-series.html) chapter
  of [*Python for Data Analysis*](https://wesmckinney.com/book/) {cite:p}`mckinney2012python`
  is where you should look if you want to learn about `date` and `time`, including
  how to create them, and how to use them to effectively handle durations, etc

+++

## References

```{bibliography}
:filter: docname in docnames
```
