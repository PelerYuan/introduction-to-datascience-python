)

near_neighbor_df2 = pd.concat([
    cancer.loc[[np.argmin(my_distances2)], attrs],
    perim_concav_with_new_point_df2.loc[[cancer.shape[0]], attrs],
])
line2 = alt.Chart(near_neighbor_df2).mark_line().encode(
    x="Perimeter",
    y="Concavity",
    color=alt.value("black")
)

glue("2-neighbor_per", "{:.1f}".format(near_neighbor_df2.iloc[0, :]["Perimeter"]))
glue("2-neighbor_con", "{:.1f}".format(near_neighbor_df2.iloc[0, :]["Concavity"]))
glue('fig:05-knn-4', (perim_concav_with_new_point2 + line2), display=True)
```

Suppose we have another new observation with standardized perimeter
{glue:text}`new_point_2_0` and concavity of {glue:text}`new_point_2_1`. Looking at the
scatter plot in {numref}`fig:05-knn-4`, how would you classify this red,
diamond observation? The nearest neighbor to this new point is a
**benign** observation at ({glue:text}`2-neighbor_per`, {glue:text}`2-neighbor_con`).
Does this seem like the right prediction to make for this observation? Probably
not, if you consider the other nearby points.

