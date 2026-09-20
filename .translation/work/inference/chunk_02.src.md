+++

```{index} population; distribution
```

In {numref}`fig:11-example-means2`, we see that the population distribution
has one peak. It is also skewed (i.e., is not symmetric): most of the listings are
less than \$250 per night, but a small number of listings cost much more,
creating a long tail on the histogram's right side.
Along with visualizing the population, we can calculate the population mean,
the average price per night for all the Airbnb listings.

```{code-cell} ipython3
airbnb["price"].mean()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("population_mean", "{:.2f}".format(airbnb["price"].mean()))
```

```{index} population; parameter
```

The price per night of all Airbnb rentals in Vancouver, BC
is \${glue:text}`population_mean`, on average. This value is our
population parameter since we are calculating it using the population data.

```{index} DataFrame; sample
```

Now suppose we did not have access to the population data (which is usually the
case!), yet we wanted to estimate the mean price per night. We could answer
this question by taking a random sample of as many Airbnb listings as our time
and resources allow. Let's say we could do this for 40 listings. What would
such a sample look like?  Let's take advantage of the fact that we do have
access to the population data and simulate taking one random sample of 40
listings in Python, again using `sample`.

```{code-cell} ipython3
one_sample = airbnb.sample(n=40)
```

We can create a histogram to visualize the distribution of observations in the
sample ({numref}`fig:11-example-means-sample-hist`), and calculate the mean
of our sample.

```{index} altair;mark_bar
```

```{code-cell} ipython3
:tags: [remove-output]

sample_distribution = alt.Chart(one_sample).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()").title("Count"),
)

sample_distribution
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:11-example-means-sample-hist", sample_distribution)
```

:::{glue:figure} fig:11-example-means-sample-hist
:name: fig:11-example-means-sample-hist

Distribution of price per night (dollars) for sample of 40 Airbnb listings.
:::

```{code-cell} ipython3
one_sample["price"].mean()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("estimate_mean", "{:.2f}".format(one_sample["price"].mean()))
glue("diff_perc", "{:.1f}".format(100 * abs(1 - (one_sample["price"].mean() / airbnb["price"].mean()))))
```

The average value of the sample of size 40
is \${glue:text}`estimate_mean`.  This
number is a point estimate for the mean of the full population.
Recall that the population mean was
\${glue:text}`population_mean`. So our estimate was fairly close to
the population parameter: the mean was about
{glue:text}`diff_perc`%
off.  Note that we usually cannot compute the estimate's accuracy in practice
since we do not have access to the population parameter; if we did, we wouldn't
need to estimate it!

```{index} sampling distribution
```

Also, recall from the previous section that the point estimate can vary; if we
took another random sample from the population, our estimate's value might
change. So then, did we just get lucky with our point estimate above?  How much
does our estimate vary across different samples of size 40 in this example?
Again, since we have access to the population, we can take many samples and
plot the sampling distribution of sample means to get a sense for this variation.
In this case, we'll use the 20,000 samples of size
40 that we already stored in the `samples` variable.
First we will calculate the sample mean for each replicate
and then plot the sampling
distribution of sample means for samples of size 40.

```{code-cell} ipython3
sample_estimates = (
    samples
    .groupby("replicate")
    ["price"]
    .mean()
    .reset_index()
    .rename(columns={"price": "mean_price"})
)
sample_estimates
```

```{code-cell} ipython3
:tags: [remove-output]

sampling_distribution = alt.Chart(sample_estimates).mark_bar().encode(
    x=alt.X("mean_price")
        .bin(maxbins=30)
        .title("Sample mean price per night (dollars)"),
    y=alt.Y("count()").title("Count")
)

sampling_distribution
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:11-example-means4", sampling_distribution)
```

:::{glue:figure} fig:11-example-means4
:name: fig:11-example-means4

Sampling distribution of the sample means for sample size of 40.
:::

```{code-cell} ipython3
:tags: [remove-cell]

glue("quantile_1", "{:0.0f}".format(round(sample_estimates["mean_price"].quantile(0.25), -1)))
glue("quantile_3", "{:0.0f}".format(round(sample_estimates["mean_price"].quantile(0.75), -1)))
```

```{index} sampling distribution; shape
```

In {numref}`fig:11-example-means4`, the sampling distribution of the mean
has one peak and is bell-shaped. Most of the estimates are between
about  \${glue:text}`quantile_1` and
\${glue:text}`quantile_3`; but there is
a good fraction of cases outside this range (i.e., where the point estimate was
not close to the population parameter). So it does indeed look like we were
quite lucky when we estimated the population mean with only
{glue:text}`diff_perc`% error.

```{index} sampling distribution; compared to population distribution
```

Let's visualize the population distribution, distribution of the sample, and
the sampling distribution on one plot to compare them in {numref}`fig:11-example-means5`. Comparing these three distributions, the centers
of the distributions are all around the same price (around \$150). The original
population distribution has a long right tail, and the sample distribution has
a similar shape to that of the population distribution. However, the sampling
distribution is not shaped like the population or sample distribution. Instead,
it has a bell shape, and it has a lower spread than the population or sample
distributions. The sample means vary less than the individual observations
because there will be some high values and some small values in any random
sample, which will keep the average from being too extreme.

<!---
```{r 11-example-means4.5}
sample_estimates |>
  summarize(mean_of_sample_means = mean(sample_mean))
```
Notice that the mean of the sample means is \$`r round(mean(sample_estimates$sample_mean),2)`. Recall that the population mean
was \$`r round(mean(airbnb$price),2)`.
-->

```{code-cell} ipython3
:tags: ["remove-cell"]

glue(
    "fig:11-example-means5",
    alt.vconcat(
        population_distribution.mark_bar(clip=True).encode(
            x=alt.X(
                "price",
                bin=alt.Bin(extent=[0, 660], maxbins=40),
                title="Price per night (dollars)",
                #scale=alt.Scale(domainMax=700)
            )
        ).properties(
            title="Population", height=150
        ),
        sample_distribution.encode(
            x=alt.X("price")
                .bin(extent=[0, 660], maxbins=40)
                .title("Price per night (dollars)")
        ).properties(title="Sample (n = 40)").properties(height=150),
        sampling_distribution.encode(
            x=alt.X("mean_price")
                .bin(extent=[0, 660], maxbins=40)
                .title("Price per night (dollars)")
        ).properties(
            title=alt.TitleParams(
                "Sampling distribution of the mean",
                subtitle="For 20,000 samples of size 40"
            )
        ).properties(height=150)
    ).resolve_scale(
        x="shared"
    )
)
```

:::{glue:figure} fig:11-example-means5
:name: fig:11-example-means5

Comparison of population distribution, sample distribution, and sampling distribution.
:::


+++

Given that there is quite a bit of variation in the sampling distribution of
the sample mean&mdash;i.e., the point estimate that we obtain is not very
reliable&mdash;is there any way to improve the estimate?  One way to improve a
point estimate is to take a *larger* sample. To illustrate what effect this
has, we will take many samples of size 20, 50, 100, and 500, and plot the
sampling distribution of the sample mean. We indicate the mean of the sampling
distribution with a vertical line.

```{code-cell} ipython3
:tags: ["remove-cell"]

# Plot sampling distributions for multiple sample sizes
base = alt.Chart(
    pd.concat([
        pd.concat([
            airbnb.sample(sample_size).assign(sample_size=sample_size, replicate=replicate)
            for sample_size in [20, 50, 100, 500]
        ])
        for replicate in range(20_000)
    ]).groupby(
        ["sample_size", "replicate"],
        as_index=False
    )["price"].mean(),
    height=150
)

glue(
    "fig:11-example-means7",
    alt.layer(
        base.mark_bar().encode(
            alt.X("price", bin=alt.Bin(maxbins=30)),
            alt.Y("count()")
        ),
        base.mark_rule(color="black", size=1.5, strokeDash=[6]).encode(
            x="mean(price)"
        ),
        base.mark_text(align="left", color="black", size=12, fontWeight="bold", dx=10).transform_aggregate(
            mean_price="mean(price)",
        ).transform_calculate(
            label="'Mean = ' + round(datum.mean_price * 10) / 10"
        ).encode(
            x=alt.X("mean_price:Q", title="Sample mean price per night (dollars)"),
            y=alt.value(10),
            text="label:N"
        )
    ).facet(
        alt.Facet(
            "sample_size:N",
            header=alt.Header(
                title="",
                labelFontWeight="bold",
                labelFontSize=12,
                labelPadding=3,
                labelExpr='"Sample size = " + datum.value'
            )
        ),
        columns=1,
    ).resolve_scale(
        y="independent"
    )
)
```

:::{glue:figure} fig:11-example-means7
:name: fig:11-example-means7

Comparison of sampling distributions, with mean highlighted as a vertical line.
:::

+++

```{index} sampling distribution; effect of sample size
```

Based on the visualization in {numref}`fig:11-example-means7`, three points
about the sample mean become clear:

1. The mean of the sample mean (across
   samples) is equal to the population mean. In other words, the sampling
   distribution is centered at the population mean.
2. Increasing the size of
   the sample decreases the spread (i.e., the variability) of the sampling
   distribution. Therefore, a larger sample size results in a more reliable point
   estimate of the population parameter.
3. The distribution of the sample mean is roughly bell-shaped.

```{note}
You might notice that in the `n = 20` case in {numref}`fig:11-example-means7`,
the distribution is not *quite* bell-shaped. There is a bit of skew towards the right!
You might also notice that in the `n = 50` case and larger, that skew seems to disappear.
In general, the sampling distribution&mdash;for both means and proportions&mdash;only
becomes bell-shaped *once the sample size is large enough*.
How large is "large enough?" Unfortunately, it depends entirely on the problem at hand. But
as a rule of thumb, often a sample size of at least 20 will suffice.
```

<!---
```{note}
If random samples of size $n$ are taken from a population, the sample mean
$\bar{x}$ will be approximately Normal with mean $\mu$ and standard deviation
$\frac{\sigma}{\sqrt{n}}$ as long as the sample size $n$ is large enough. $\mu$
is the population mean, $\sigma$ is the population standard deviation,
$\bar{x}$ is the sample mean, and $n$ is the sample size.
If samples are selected from a finite population as we are doing in this
chapter, we should apply a finite population correction. We multiply
$\frac{\sigma}{\sqrt{n}}$ by $\sqrt{\frac{N - n}{N - 1}}$ where $N$ is the
population size and $n$ is the sample size. If our sample size, $n$, is small
relative to the population size, this finite correction factor is less
important.
```
--->

+++

### Summary

1. A point estimate is a single value computed using a sample from a population (e.g., a mean or proportion).
2. The sampling distribution of an estimate is the distribution of the estimate for all possible samples of a fixed size from the same population.
3. The shape of the sampling distribution is usually bell-shaped with one peak and centered at the population mean or proportion.
4. The spread of the sampling distribution is related to the sample size. As the sample size increases, the spread of the sampling distribution decreases.

+++

## Bootstrapping

+++

### Overview

*Why all this emphasis on sampling distributions?*

We saw in the previous section that we could compute a **point estimate** of a
population parameter using a sample of observations from the population. And
since we constructed examples where we had access to the population, we could
evaluate how accurate the estimate was, and even get a sense of how much the
estimate would vary for different samples from the population.  But in real
data analysis settings, we usually have *just one sample* from our population
and do not have access to the population itself. Therefore we cannot construct
the sampling distribution as we did in the previous section. And as we saw, our
sample estimate's value can vary significantly from the population parameter.
So reporting the point estimate from a single sample alone may not be enough.
We also need to report some notion of *uncertainty* in the value of the point
estimate.

```{index} bootstrap, confidence interval
```

```{index} see: interval; confidence interval
```

Unfortunately, we cannot construct the exact sampling distribution without
full access to the population. However, if we could somehow *approximate* what
the sampling distribution would look like for a sample, we could
use that approximation to then report how uncertain our sample
point estimate is (as we did above with the *exact* sampling
distribution). There are several methods to accomplish this; in this book, we
will use the *bootstrap*. We will discuss **interval estimation** and
construct
**confidence intervals** using just a single sample from a population. A
confidence interval is a range of plausible values for our population parameter.

Here is the key idea. First, if you take a big enough sample, it *looks like*
the population. Notice the histograms' shapes for samples of different sizes
taken from the population in {numref}`fig:11-example-bootstrapping0`. We
see that the sample’s distribution looks like that of the population for a
large enough sample.

```{code-cell} ipython3
:tags: [remove-cell]

# plot sample distributions for n = 10, 20, 50, 100, 200 and population distribution
sample_distribution_dict = {}
for sample_n in [10, 20, 50, 100, 200]:
    sample = airbnb.sample(sample_n)
    sample_distribution_dict[f"sample_distribution_{sample_n}"] = (
        alt.Chart(sample, title=f"n = {sample_n}").mark_bar().encode(
            x=alt.X(
                "price",
                bin=alt.Bin(extent=[0, 600], step=20),
                title="Price per night (dollars)",
            ),
            y=alt.Y("count()", title="Count"),
        )
    ).properties(height=150)
# add title and standardize the x axis ticks for population histogram
population_distribution.title = "Population distribution"
population_distribution.encoding["x"]["bin"] = alt.Bin(extent=[0, 600], step=20)

glue(
    "fig:11-example-bootstrapping0",
    (
        (
            sample_distribution_dict["sample_distribution_10"]
            | sample_distribution_dict["sample_distribution_20"]
        )
        & (
            sample_distribution_dict["sample_distribution_50"]
            | sample_distribution_dict["sample_distribution_100"]
        )
        & (
            sample_distribution_dict["sample_distribution_200"]
            | population_distribution.properties(width=350, height=150)
        )
    ),
)
```

:::{glue:figure} fig:11-example-bootstrapping0
:name: fig:11-example-bootstrapping0

Comparison of samples of different sizes from the population.
:::

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

