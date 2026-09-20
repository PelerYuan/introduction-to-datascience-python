```{code-cell} ipython3
:tags: [remove-output]

population_distribution = alt.Chart(airbnb).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()", title="Count"),
)

population_distribution
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:11-example-means2", population_distribution)
```

:::{glue:figure} fig:11-example-means2
:name: fig:11-example-means2

Population distribution of price per night (dollars) for all Airbnb listings in Vancouver, Canada.
:::

