    )
)

fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=1),
    template="plotly_white",
)

# if HTML, use the plotly 3d image; if PDF, use static image
if "BOOK_BUILD_TYPE" in os.environ and os.environ["BOOK_BUILD_TYPE"] == "PDF":
    glue("fig:08-3DlinReg", Image("img/regression2/plot3d_linear_regression.png"))
else:
    glue("fig:08-3DlinReg", fig)
```

```{figure} data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
:name: fig:08-3DlinReg
:figclass: caption-hack

Linear regression plane of best fit overlaid on top of the data (using price,
house size, and number of bedrooms as predictors). Note that in general we
recommend against using 3D visualizations; here we use a 3D visualization only
to illustrate what the regression plane looks like for learning purposes.
```

