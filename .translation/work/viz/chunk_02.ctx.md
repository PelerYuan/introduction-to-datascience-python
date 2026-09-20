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

