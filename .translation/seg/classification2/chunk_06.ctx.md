
accuracy_vs_k
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:06-find-k", accuracy_vs_k)
glue("best_k_unique", "{:d}".format(accuracies_grid["n_neighbors"][accuracies_grid["mean_test_score"].idxmax()]))
glue("best_acc", "{:.1f}".format(accuracies_grid["mean_test_score"].max()*100))
```

:::{glue:figure} fig:06-find-k
:name: fig:06-find-k

Plot of estimated accuracy versus the number of neighbors.
:::

We can also obtain the number of neighbours with the highest accuracy programmatically by accessing
the `best_params_` attribute of the fit `GridSearchCV` object. Note that it is still useful to visualize
the results as we did above since this provides additional information on how the model performance varies.
```{code-cell} ipython3
cancer_tune_grid.best_params_
```

