that points are far from the cluster center. Note, however, that "large" is relative to *both* the
scale of the variables for clustering *and* the number of points in the cluster. A cluster where points
are very close to the center might still have a large $S^2$ if there are many data points in the cluster.

After we have calculated the WSSD for all the clusters,
we sum them together to get the *total WSSD*. For our example,
this means adding up all the squared distances for the 18 observations.
These distances are denoted by black lines in
{numref}`toy-example-all-clus-dists`.

:::{glue:figure} toy-example-all-clus-dists
:figwidth: 700px
:name: toy-example-all-clus-dists

All clusters from the `penguins_standardized` data set example. Observations are small orange, blue, and yellow points with cluster centers denoted by larger points with a black outline. The distances from the observations to each of the respective cluster centers are represented as black lines.
:::

Since K-means uses the straight-line distance to measure the quality of a clustering,
it is limited to clustering based on quantitative variables.
However, note that there are variants of the K-means algorithm,
as well as other clustering algorithms entirely,
that use other distance metrics
to allow for non-quantitative data to be clustered.
These are beyond the scope of this book.

