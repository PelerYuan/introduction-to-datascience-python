+++

1. Randomly select an observation from the original sample, which was drawn from the population.
2. Record the observation's value.
3. Replace that observation.
4. Repeat steps 1&ndash;3 (sampling *with* replacement) until you have $n$ observations, which form a bootstrap sample.
5. Calculate the bootstrap point estimate (e.g., mean, median, proportion, slope, etc.) of the $n$ observations in your bootstrap sample.
6. Repeat steps 1&ndash;5 many times to create a distribution of point estimates (the bootstrap distribution).
7. Calculate the plausible range of values around our observed point estimate.

+++

```{figure} img/inference/intro-bootstrap.jpeg
:name: fig:11-intro-bootstrap-image

Overview of the bootstrap process.
```

+++

### Bootstrapping in Python

Let’s continue working with our Airbnb example to illustrate how we might create
and use a bootstrap distribution using just a single sample from the population.
Once again, suppose we are
interested in estimating the population mean price per night of all Airbnb
listings in Vancouver, Canada, using a single sample size of 40.
Recall our point estimate was \${glue:text}`estimate_mean`. The
histogram of prices in the sample is displayed in {numref}`fig:11-bootstrapping1`.

```{code-cell} ipython3
one_sample
```

```{code-cell} ipython3
:tags: ["remove-output"]
one_sample_dist = alt.Chart(one_sample).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()").title("Count"),
)

one_sample_dist
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping1", one_sample_dist)
```

:::{glue:figure} fig:11-bootstrapping1
:name: fig:11-bootstrapping1

Histogram of price per night (dollars) for one sample of size 40.
:::

+++

The histogram for the sample is skewed, with a few observations out to the right. The
mean of the sample is \${glue:text}`estimate_mean`.
Remember, in practice, we usually only have this one sample from the population. So
this sample and estimate are the only data we can work with.

```{index} bootstrap; in Python, DataFrame; sample (bootstrap)
```

We now perform steps 1&ndash;5 listed above to generate a single bootstrap
sample in Python and calculate a point estimate from that bootstrap sample. We will
continue using the `sample` function of our dataframe,
Critically, note that we now
set `frac=1` ("fraction") to indicate that we want to draw as many samples as there are rows in the dataframe
(we could also have set `n=40` but then we would need to manually keep track of how many rows there are).
Since we need to sample with replacement when bootstrapping,
we change the `replace` parameter to `True`.

```{code-cell} ipython3
:tags: ["remove-output"]

boot1 = one_sample.sample(frac=1, replace=True)
boot1_dist = alt.Chart(boot1).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()", title="Count"),
)

boot1_dist
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping3", boot1_dist)
```

:::{glue:figure} fig:11-bootstrapping3
:name: fig:11-bootstrapping3

Bootstrap distribution.
:::

```{code-cell} ipython3
boot1["price"].mean()
```

Notice in {numref}`fig:11-bootstrapping3` that the histogram of our bootstrap sample
has a similar shape to the original sample histogram. Though the shapes of
the distributions are similar, they are not identical. You'll also notice that
the original sample mean and the bootstrap sample mean differ. How might that
happen? Remember that we are sampling with replacement from the original
sample, so we don't end up with the same sample values again. We are *pretending*
that our single sample is close to the population, and we are trying to
mimic drawing another sample from the population by drawing one from our original
sample.

Let's now take 20,000 bootstrap samples from the original sample (`one_sample`)
and calculate the means for
each of those replicates. Recall that this assumes that `one_sample` *looks like*
our original population; but since we do not have access to the population itself,
this is often the best we can do.
Note that here we break the list comprehension over multiple lines
so that it is easier to read.

```{code-cell} ipython3
boot20000 = pd.concat([
    one_sample.sample(frac=1, replace=True).assign(replicate=n)
    for n in range(20_000)
])
boot20000
```

Let's take a look at the histograms of the first six replicates of our bootstrap samples.

```{code-cell} ipython3
:tags: ["remove-output"]

six_bootstrap_samples = boot20000.query("replicate < 6")
six_bootstrap_fig = alt.Chart(six_bootstrap_samples, height=150).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=20)
        .title("Price per night (dollars)"),
    y=alt.Y("count()").title("Count")
).facet(
    "replicate:N",  # Recall that `:N` converts the variable to a categorical type
    columns=2
)
six_bootstrap_fig
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping-six-bootstrap-samples", six_bootstrap_fig)
```

:::{glue:figure} fig:11-bootstrapping-six-bootstrap-samples
:name: fig:11-bootstrapping-six-bootstrap-samples

Histograms of the first six replicates of the bootstrap samples.
:::

+++

We see in {numref}`fig:11-bootstrapping-six-bootstrap-samples` how the distributions of the
bootstrap samples differ. If we calculate the sample mean for each of
these six samples, we can see that these are also different between samples.
To compute the mean for each sample,
we first group by the "replicate" which is the column containing the sample/replicate number.
Then we compute the mean of the `price` column and rename it to `mean_price`
for it to be more descriptive.
Finally we use `reset_index` to get the `replicate` values back as a column in the dataframe.

```{code-cell} ipython3
(
    six_bootstrap_samples
    .groupby("replicate")
    ["price"]
    .mean()
    .reset_index()
    .rename(columns={"price": "mean_price"})
)
```

The distributions and the means differ between the bootstrapped samples
because we are sampling *with replacement*.
If we instead would have sampled *without replacement*,
we would end up with the exact same values in the sample each time.

We will now calculate point estimates of the mean for our 20,000 bootstrap samples and
generate a bootstrap distribution of these point estimates. The bootstrap
distribution ({numref}`fig:11-bootstrapping5`) suggests how we might expect
our point estimate to behave if we take multiple samples.

```{index} DataFrame;reset_index, DataFrame;rename, DataFrame;groupby, Series;mean
```

```{code-cell} ipython3
boot20000_means = (
    boot20000
    .groupby("replicate")
    ["price"]
    .mean()
    .reset_index()
    .rename(columns={"price": "mean_price"})
)

boot20000_means
```

```{code-cell} ipython3
:tags: ["remove-output"]

boot_est_dist = alt.Chart(boot20000_means).mark_bar().encode(
    x=alt.X("mean_price")
        .bin(maxbins=20)
        .title("Sample mean price per night (dollars)"),
    y=alt.Y("count()").title("Count"),
)

boot_est_dist
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping5", boot_est_dist)
```

:::{glue:figure} fig:11-bootstrapping5
:name: fig:11-bootstrapping5

Distribution of the bootstrap sample means.
:::

+++

Let's compare the bootstrap distribution&mdash;which we construct by taking many samples from our original sample of size 40&mdash;with
the true sampling distribution&mdash;which corresponds to taking many samples from the population.

```{code-cell} ipython3
:tags: [remove-cell]

sampling_distribution.encoding.x["bin"]["extent"] = (90, 250)
bootstr6fig = alt.vconcat(
    alt.layer(
        sampling_distribution,
        alt.Chart(sample_estimates).mark_rule(color="black", size=1.5, strokeDash=[6]).encode(x="mean(mean_price)"),
        alt.Chart(sample_estimates).mark_text(color="black", size=12, align="left", dx=16, fontWeight="bold").encode(
            x="mean(mean_price)",
            y=alt.value(7),
            text=alt.value(f"Mean = {sampling_distribution['data']['mean_price'].mean().round(1)}")
        )
    ).properties(title="Sampling distribution", height=150),
    alt.layer(
        boot_est_dist,
        alt.Chart(boot20000_means).mark_rule(color="black", size=1.5, strokeDash=[6]).encode(x="mean(mean_price)"),
        alt.Chart(boot20000_means).mark_text(color="black", size=12, align="left", dx=18, fontWeight="bold").encode(
            x="mean(mean_price)",
            y=alt.value(7),
            text=alt.value(f"Mean = {boot_est_dist['data']['mean_price'].mean().round(1)}")
        )
    ).properties(title="Bootstrap distribution", height=150)
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping6", bootstr6fig)
```

:::{glue:figure} fig:11-bootstrapping6
:name: fig:11-bootstrapping6

Comparison of the distribution of the bootstrap sample means and sampling distribution.
:::



```{code-cell} ipython3
:tags: [remove-cell]

glue("one_sample_mean", "{:.2f}".format(one_sample["price"].mean()))
```

```{index} sampling distribution; compared to bootstrap distribution
```

There are two essential points that we can take away from
{numref}`fig:11-bootstrapping6`. First, the shape and spread of the true sampling
distribution and the bootstrap distribution are similar; the bootstrap
distribution lets us get a sense of the point estimate's variability. The
second important point is that the means of these two distributions are
slightly different. The sampling distribution is centered at
\${glue:text}`population_mean`, the population mean value. However, the bootstrap
distribution is centered at the original sample's mean price per night,
\${glue:text}`one_sample_mean`. Because we are resampling from the
original sample repeatedly, we see that the bootstrap distribution is centered
at the original sample's mean value (unlike the sampling distribution of the
sample mean, which is centered at the population parameter value).

{numref}`fig:11-bootstrapping7` summarizes the bootstrapping process.
The idea here is that we can use this distribution of bootstrap sample means to
approximate the sampling distribution of the sample means when we only have one
sample. Since the bootstrap distribution pretty well approximates the sampling
distribution spread, we can use the bootstrap spread to help us develop a
plausible range for our population parameter along with our estimate!

```{figure} img/inference/11-bootstrapping7-1.png
:name: fig:11-bootstrapping7

Summary of bootstrapping process.
```

+++

### Using the bootstrap to calculate a plausible range

```{index} confidence interval
```

Now that we have constructed our bootstrap distribution, let's use it to create
an approximate 95\% percentile bootstrap confidence interval.
A **confidence interval** is a range of plausible values for the population parameter. We will
find the range of values covering the middle 95\% of the bootstrap
distribution, giving us a 95\% confidence interval.  You may be wondering, what
does "95\% confidence" mean? If we took 100 random samples and calculated 100
95\% confidence intervals, then about 95\% of the ranges would capture the
population parameter's value.  Note there's nothing special about 95\%. We
could have used other levels, such as 90\% or 99\%. There is a balance between
our level of confidence and precision. A higher confidence level corresponds to
a wider range of the interval, and a lower confidence level corresponds to a
narrower range. Therefore the level we choose is based on what chance we are
willing to take of being wrong based on the implications of being wrong for our
application. In general, we choose confidence levels to be comfortable with our
level of uncertainty but not so strict that the interval is unhelpful. For
instance, if our decision impacts human life and the implications of being
wrong are deadly, we may want to be very confident and choose a higher
confidence level.

To calculate a 95\% percentile bootstrap confidence interval, we will do the following:

1. Arrange the observations in the bootstrap distribution in ascending order.
2. Find the value such that 2.5\% of observations fall below it (the 2.5\% percentile). Use that value as the lower bound of the interval.
3. Find the value such that 97.5\% of observations fall below it (the 97.5\% percentile). Use that value as the upper bound of the interval.

To do this in Python, we can use the `quantile` function of our DataFrame.
Quantiles are expressed in proportions rather than percentages,
so the 2.5th and 97.5th percentiles
would be the 0.025 and 0.975 quantiles, respectively.

```{index} DataFrame; [], DataFrame;quantile
```

```{index} percentile
```

```{code-cell} ipython3
ci_bounds = boot20000_means["mean_price"].quantile([0.025, 0.975])
ci_bounds
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("ci_lower", "{:.2f}".format(ci_bounds[0.025]))
glue("ci_upper", "{:.2f}".format(ci_bounds[0.975]))
```

Our interval, \${glue:text}`ci_lower` to \${glue:text}`ci_upper`, captures
the middle 95\% of the sample mean prices in the bootstrap distribution. We can
visualize the interval on our distribution in {numref}`fig:11-bootstrapping9`.

```{code-cell} ipython3
:tags: [remove-cell]
# Create the annotation for for the 2.5th percentile
rule_025 = alt.Chart().mark_rule(color="black", size=1.5, strokeDash=[6]).encode(
    x=alt.datum(ci_bounds[0.025])
).properties(
    width=500
)
text_025 = rule_025.mark_text(
    color="black",
    size=12,
    fontWeight="bold",
    dy=-160
).encode(
    text=alt.datum(f"2.5th percentile ({ci_bounds[0.025].round(1)})")
)

# Create the annotation for for the 97.5th percentile
text_975 = text_025.encode(
    x=alt.datum(ci_bounds[0.975]),
    text=alt.datum(f"97.5th percentile ({ci_bounds[0.975].round(1)})")
)
rule_975 = rule_025.encode(x=alt.datum(ci_bounds[0.975]))

# Layer the annotations on top of the distribution plot
bootstr9fig = boot_est_dist + rule_025 + text_025 + rule_975 + text_975
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping9", bootstr9fig)
```

:::{glue:figure} fig:11-bootstrapping9
:name: fig:11-bootstrapping9

Distribution of the bootstrap sample means with percentile lower and upper bounds.
:::



+++

To finish our estimation of the population parameter, we would report the point
estimate and our confidence interval's lower and upper bounds. Here the sample
mean price-per-night of 40 Airbnb listings was
\${glue:text}`one_sample_mean`, and we are 95\% "confident" that the true
population mean price-per-night for all Airbnb listings in Vancouver is between
\${glue:text}`ci_lower` and \${glue:text}`ci_upper`.
Notice that our interval does indeed contain the true
population mean value, \${glue:text}`population_mean`\! However, in
practice, we would not know whether our interval captured the population
parameter or not because we usually only have a single sample, not the entire
population. This is the best we can do when we only have one sample!

This chapter is only the beginning of the journey into statistical inference.
We can extend the concepts learned here to do much more than report point
estimates and confidence intervals, such as testing for real differences
between populations, tests for associations between variables, and so much
more. We have just scratched the surface of statistical inference; however, the
material presented here will serve as the foundation for more advanced
statistical techniques you may learn about in the future!

+++

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the two "Statistical inference" rows. You can preview a
non-interactive version of each worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.


+++

## Additional resources

- Chapters 4 to 7 of *OpenIntro Statistics* {cite:p}`openintro`
  provide a good next step in learning about inference. Although it is still certainly
  an introductory text, things get a bit more mathematical here. Depending on
  your background, you may actually want to start going through Chapters 1 to 3
  first, where you will learn some fundamental concepts in probability theory.
  Although it may seem like a diversion, probability theory is *the language of
  statistics*; if you have a solid grasp of probability, more advanced statistics
  will come naturally to you!

+++

## References

```{bibliography}
:filter: docname in docnames
```
