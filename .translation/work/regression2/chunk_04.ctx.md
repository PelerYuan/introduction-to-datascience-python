
curve_plt2 = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x=alt.X("z", title="z = x³" ,scale=alt.Scale(zero=False)),
        y=alt.Y(
            "y",
            scale=alt.Scale(zero=False),
        ),
    )
)


curve_plt2 += curve_plt2.transform_regression("z", "y").mark_line(color="#ff7f0e")

glue("fig:08-predictor-design-2", curve_plt2)
```

:::{glue:figure} fig:08-predictor-design-2
:name: fig:08-predictor-design-2

Relationship between the transformed predictor and the response.
:::

