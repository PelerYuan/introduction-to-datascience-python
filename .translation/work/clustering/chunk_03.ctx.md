        x=alt.X("k").title("Number of clusters"),
        y=alt.Y("wssd").title("Total within-cluster sum of squares"),
    ),
    alt.Chart().mark_text(size=22, align='left', baseline='bottom').encode(
        x=alt.datum(3.3),
        y=alt.datum(9.8),
        text=alt.datum('Elbow')
    ),
    alt.Chart().mark_text(size=50, align='left', baseline='bottom', fontWeight=100, angle=25).encode(
        x=alt.datum(2.8),
        y=alt.datum(5),
        text=alt.datum('🠃')
    )
)

glue('toy-kmeans-elbow', elbow_plot, display=True)
```

:::{glue:figure} toy-kmeans-elbow
:figwidth: 700px
:name: toy-kmeans-elbow

Total WSSD for K clusters ranging from 1 to 9.
:::

