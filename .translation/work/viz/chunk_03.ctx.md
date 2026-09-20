
```{code-cell} ipython3
can_lang_plot_theme = alt.Chart(can_lang).mark_point(filled=True).encode(
    x=alt.X("most_at_home_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Language spoken most at home", "(percentage of Canadian residents)"]),
    y=alt.Y("mother_tongue_percent")
        .scale(type="log")
        .axis(tickCount=7)
        .title(["Mother tongue", "(percentage of Canadian residents)"]),
    color=alt.Color("category")
        .legend(orient="top")
        .title("")
        .scale(scheme="dark2"),
    shape="category"
).configure_axis(titleFontSize=12)
```

```{code-cell} ipython3
:tags: ["remove-cell"]
# Increasing the dimensions makes all the ticks fit in jupyter book (the fit with the default dimensions in jupyterlab)
glue("can_lang_plot_theme", can_lang_plot_theme.properties(height=320, width=420), display=False)
```

