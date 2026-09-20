
+++

```{index} bootstrap; distribution
```

In the previous section, we took many samples of the same size *from our
population* to get a sense of the variability of a sample estimate. But if our
sample is big enough that it looks like our population, we can pretend that our
sample *is* the population, and take more samples (with replacement) of the
same size from it instead! This very clever technique is
called **the bootstrap**.  Note that by taking many samples from our single, observed
sample, we do not obtain the true sampling distribution, but rather an
approximation that we call **the bootstrap distribution**.

```{note}
We must sample *with* replacement when using the bootstrap.
Otherwise, if we had a sample of size $n$, and obtained a sample from it of
size $n$ *without* replacement, it would just return our original sample!
```

This section will explore how to create a bootstrap distribution from a single
sample using Python.  The process is visualized in {numref}`fig:11-intro-bootstrap-image`.
For a sample of size $n$, you would do the following:

