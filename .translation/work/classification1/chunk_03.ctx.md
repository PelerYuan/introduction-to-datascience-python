    glue("fig:05-more", fig)
```

```{figure} data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
:name: fig:05-more
:figclass: caption-hack

3D scatter plot of the standardized symmetry, concavity, and perimeter
variables. Note that in general we recommend against using 3D visualizations;
here we show the data in 3D only to illustrate what higher dimensions and
nearest neighbors look like, for learning purposes.
```

+++

### Summary of K-nearest neighbors algorithm

In order to classify a new observation using a K-nearest neighbors classifier, we have to do the following:

1. Compute the distance between the new observation and each observation in the training set.
2. Find the $K$ rows corresponding to the $K$ smallest distances.
3. Classify the new observation based on a majority vote of the neighbor classes.

+++

