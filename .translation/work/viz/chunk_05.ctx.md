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

