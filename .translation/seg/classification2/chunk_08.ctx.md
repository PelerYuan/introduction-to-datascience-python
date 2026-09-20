melted_summary_df["Type"] = melted_summary_df["Type"].apply(lambda x: "Tuned K" if x=="accs" else "K = 3")

plt_irrelevant_nghbrs_fixed = (
    alt.Chart(
        melted_summary_df
    )
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "Accuracy",
            scale=alt.Scale(zero=False),
        ),
        color=alt.Color("Type"),
    )
)
glue("fig:06-fixed-irrelevant-features", plt_irrelevant_nghbrs_fixed)
```

:::{glue:figure} fig:06-fixed-irrelevant-features
:name: fig:06-fixed-irrelevant-features

Accuracy versus number of irrelevant predictors for tuned and untuned number of neighbors.
:::

