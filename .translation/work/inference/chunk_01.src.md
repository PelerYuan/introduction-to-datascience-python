
(inference)=
# Statistical inference

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
```

## Overview

A typical data analysis task in practice is to draw conclusions about some
unknown aspect of a population of interest based on observed data sampled from
that population; we typically do not get data on the *entire* population.  Data
analysis questions regarding how summaries, patterns, trends, or relationships
in a data set extend to the wider population are called *inferential
questions*. This chapter will start with the fundamental ideas of sampling from
populations and then introduce two common techniques in statistical inference:
*point estimation* and *interval estimation*.

## Chapter learning objectives

By the end of the chapter, readers will be able to do the following:

- Describe real-world examples of questions that can be answered with statistical inference.
- Define common population parameters (e.g., mean, proportion, standard deviation) that are often estimated using sampled data, and estimate these from a sample.
- Define the following statistical sampling terms: population, sample, population parameter, point estimate, and sampling distribution.
- Explain the difference between a population parameter and a sample point estimate.
- Use Python to draw random samples from a finite population.
- Use Python to create a sampling distribution from a finite population.
- Describe how sample size influences the sampling distribution.
- Define bootstrapping.
- Use Python to create a bootstrap distribution to approximate a sampling distribution.
- Contrast the bootstrap and sampling distributions.

+++

## Why do we need sampling?

We often need to understand how quantities we observe in a subset
of data relate to the same quantities in the broader population. For example, suppose a
retailer is considering selling iPhone accessories, and they want to estimate
how big the market might be. Additionally, they want to strategize how they can
market their products on North American college and university campuses. This
retailer might formulate the following question:

*What proportion of all undergraduate students in North America own an iPhone?*

```{index} population, population; parameter
```

In the above question, we are interested in making a conclusion about *all*
undergraduate students in North America; this is referred to as the **population**. In
general, the population is the complete collection of individuals or cases we
are interested in studying.  Further, in the above question, we are interested
in computing a quantity&mdash;the proportion of iPhone owners&mdash;based on
the entire population. This proportion is referred to as a **population parameter**. In
general, a population parameter is a numerical characteristic of the entire
population. To compute this number in the example above, we would need to ask
every single undergraduate in North America whether they own an iPhone. In
practice, directly computing population parameters is often time-consuming and
costly, and sometimes impossible.

```{index} sample, sample; estimate, inference
```

```{index} see: statistical inference; inference
```

A more practical approach would be to make measurements for a **sample**, i.e., a
subset of individuals collected from the population. We can then compute a
**sample estimate**&mdash;a numerical characteristic of the sample&mdash;that
estimates the population parameter. For example, suppose we randomly selected
ten undergraduate students across North America (the sample) and computed the
proportion of those students who own an iPhone (the sample estimate). In that
case, we might suspect that proportion is a reasonable estimate of the
proportion of students who own an iPhone in the entire population.
{numref}`fig:11-population-vs-sample` illustrates this process.
In general, the process of using a sample to make a conclusion about the
broader population from which it is taken is referred to as **statistical inference**.

+++

```{figure} img/inference/population_vs_sample.png
:name: fig:11-population-vs-sample

The process of using a sample from a broader population to obtain a point estimate of a
population parameter. In this case, a sample of 10 individuals yielded 6 who own an iPhone, resulting
in an estimated population proportion of 60% iPhone owners. The actual population proportion in this example
illustration is 53.8%.
```

+++

Note that proportions are not the *only* kind of population parameter we might
be interested in. For example, suppose an undergraduate student studying at the University
of British Columbia in Canada is looking for an apartment
to rent. They need to create a budget, so they want to know something about
studio apartment rental prices in Vancouver, BC. This student might
formulate the following question:

*What is the average price-per-month of studio apartment rentals in Vancouver, Canada?*

In this case, the population consists of all studio apartment rentals in Vancouver, and the
population parameter is the *average price-per-month*. Here we used the average
as a measure of the center to describe the "typical value" of studio apartment
rental prices. But even within this one example, we could also be interested in
many other population parameters. For instance, we know that not every studio
apartment rental in Vancouver will have the same price per month. The student
might be interested in how much monthly prices vary and want to find a measure
of the rentals' spread (or variability), such as the standard deviation. Or perhaps the
student might be interested in the fraction of studio apartment rentals that
cost more than \$1000 per month. The question we want to answer will help us
determine the parameter we want to estimate. If we were somehow able to observe
the whole population of studio apartment rental offerings in Vancouver, we
could compute each of these numbers exactly; therefore, these are all
population parameters. There are many kinds of observations and population
parameters that you will run into in practice, but in this chapter, we will
focus on two settings:

1. Using categorical observations to estimate the proportion of a category
2. Using quantitative observations to estimate the average (or mean)

+++

## Sampling distributions

### Sampling distributions for proportions

```{index} Airbnb
```

We will look at an example using data from
[Inside Airbnb](http://insideairbnb.com/) {cite:p}`insideairbnb`. Airbnb is an online
marketplace for arranging vacation rentals and places to stay. The data set
contains listings for Vancouver, Canada, in September 2020. Our data
includes an ID number, neighborhood, type of room, the number of people the
rental accommodates, number of bathrooms, bedrooms, beds, and the price per
night.

```{code-cell} ipython3
import pandas as pd

airbnb = pd.read_csv("data/listings.csv")
airbnb
```

Suppose the city of Vancouver wants information about Airbnb rentals to help
plan city bylaws, and they want to know how many Airbnb places are listed as
entire homes and apartments (rather than as private or shared rooms). Therefore
they may want to estimate the true proportion of all Airbnb listings where the
room type is listed as "entire home or apartment." Of course, we usually
do not have access to the true population, but here let's imagine (for learning
purposes) that our data set represents the population of all Airbnb rental
listings in Vancouver, Canada.
We can find the proportion of listings for each room type
by using the `value_counts` function with the `normalize` parameter
as we did in previous chapters.

```{index} DataFrame; [], DataFrame; value_counts
```

```{code-cell} ipython3
airbnb["room_type"].value_counts(normalize=True)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("population_proportion", "{:.3f}".format(airbnb["room_type"].value_counts(normalize=True)["Entire home/apt"]))
```

We can see that the proportion of `Entire home/apt` listings in
the data set is {glue:text}`population_proportion`. This
value, {glue:text}`population_proportion`, is the population parameter. Remember, this
parameter value is usually unknown in real data analysis problems, as it is
typically not possible to make measurements for an entire population.

```{index} DataFrame; sample, seed;numpy.random.seed
```

Instead, perhaps we can approximate it with a small subset of data!
To investigate this idea, let's try randomly selecting 40 listings (*i.e.,* taking a random sample of
size 40 from our population), and computing the proportion for that sample.
We will use the `sample` method of the `DataFrame`
object to take the sample. The argument `n` of `sample` is the size of the sample to take
and since we are starting to use randomness here,
we are also setting the random seed via numpy to make the results reproducible.

```{code-cell} ipython3
import numpy as np


np.random.seed(155)

airbnb.sample(n=40)["room_type"].value_counts(normalize=True)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("sample_1_proportion", "{:.3f}".format(airbnb.sample(n=40, random_state=155)["room_type"].value_counts(normalize=True)["Entire home/apt"]))
```

```{index} DataFrame; value_counts
```

Here we see that the proportion of entire home/apartment listings in this
random sample is {glue:text}`sample_1_proportion`. Wow&mdash;that's close to our
true population value! But remember, we computed the proportion using a random sample of size 40.
This has two consequences. First, this value is only an *estimate*, i.e., our best guess
of our population parameter using this sample.
Given that we are estimating a single value here, we often
refer to it as a **point estimate**.  Second, since the sample was random,
if we were to take *another* random sample of size 40 and compute the proportion for that sample,
we would not get the same answer:

```{code-cell} ipython3
airbnb.sample(n=40)["room_type"].value_counts(normalize=True)
```

Confirmed! We get a different value for our estimate this time.
That means that our point estimate might be unreliable. Indeed, estimates vary from sample to
sample due to **sampling variability**. But just how much
should we expect the estimates of our random samples to vary?
Or in other words, how much can we really trust our point estimate based on a single sample?

```{index} sampling distribution
```

To understand this, we will simulate many samples (much more than just two)
of size 40 from our population of listings and calculate the proportion of
entire home/apartment listings in each sample. This simulation will create
many sample proportions, which we can visualize using a histogram. The
distribution of the estimate for all possible samples of a given size (which we
commonly refer to as $n$) from a population is called
a **sampling distribution**. The sampling distribution will help us see how much we would
expect our sample proportions from this population to vary for samples of size 40.

```{index} DataFrame; sample
```

We again use the `sample` to take samples of size 40 from our
population of Airbnb listings. But this time we use a list comprehension
to repeat the operation multiple times (as we did previously in {numref}`Chapter %s <clustering>`).
In this case we repeat the operation 20,000 times to obtain 20,000 samples of size 40.
To make it clear which rows in the data frame come
which of the 20,000 samples, we also add a column called `replicate` with this information using the `assign` function,
introduced previously in {numref}`Chapter %s <wrangling>`.
The call to `concat` concatenates all the 20,000 data frames
returned from the list comprehension into a single big data frame.

```{code-cell} ipython3
samples = pd.concat([
    airbnb.sample(40).assign(replicate=n)
    for n in range(20_000)
])
samples
```

Since the column `replicate` indicates the replicate/sample number,
we can verify that we indeed seem to have 20,0000 samples
starting at sample 0 and ending at sample 19,999.

+++

Now that we have obtained the samples, we need to compute the
proportion of entire home/apartment listings in each sample.
We first group the data by the `replicate` variable&mdash;to group the
set of listings in each sample together&mdash;and then use `value_counts`
with `normalize=True` to compute the proportion in each sample.
Both the first and last few entries of the resulting data frame are printed
below to show that we end up with 20,000 point estimates, one for each of the 20,000 samples.

```{index} DataFrame;groupby, DataFrame;reset_index
```

```{code-cell} ipython3
(
    samples
    .groupby("replicate")
    ["room_type"]
    .value_counts(normalize=True)
)
```

The returned object is a series,
and as we have previously learned
we can use `reset_index` to change it to a data frame.
However,
there is one caveat here:
when we use the `value_counts` function
on a grouped series and try to `reset_index`
we will end up with two columns with the same name
and therefore get an error
(in this case, `room_type` will occur twice).
Fortunately,
there is a simple solution:
when we call `reset_index`,
we can specify the name of the new column
with the `name` parameter:

```{code-cell} ipython3
(
    samples
    .groupby("replicate")
    ["room_type"]
    .value_counts(normalize=True)
    .reset_index(name="sample_proportion")
)
```

Below we put everything together
and also filter the data frame to keep only the room types
that we are interested in.

```{code-cell} ipython3
sample_estimates = (
    samples
    .groupby("replicate")
    ["room_type"]
    .value_counts(normalize=True)
    .reset_index(name="sample_proportion")
)

sample_estimates = sample_estimates[sample_estimates["room_type"] == "Entire home/apt"]
sample_estimates
```

We can now visualize the sampling distribution of sample proportions
for samples of size 40 using a histogram in {numref}`fig:11-example-proportions7`. Keep in mind: in the real world,
we don't have access to the full population. So we
can't take many samples and can't actually construct or visualize the sampling distribution.
We have created this particular example
such that we *do* have access to the full population, which lets us visualize the
sampling distribution directly for learning purposes.

```{code-cell} ipython3
:tags: [remove-output]

sampling_distribution = alt.Chart(sample_estimates).mark_bar().encode(
    x=alt.X("sample_proportion")
        .bin(maxbins=20)
        .title("Sample proportions"),
    y=alt.Y("count()").title("Count"),
)

sampling_distribution
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:11-example-proportions7", sampling_distribution)
```

:::{glue:figure} fig:11-example-proportions7
:name: fig:11-example-proportions7

Sampling distribution of the sample proportion for sample size 40.
:::

```{code-cell} ipython3
:tags: [remove-cell]

glue("sample_proportion_center", "{:.2f}".format(sample_estimates["sample_proportion"].mean()))
glue("sample_proportion_min", "{:.2f}".format(sample_estimates["sample_proportion"].quantile(0.004)))
glue("sample_proportion_max", "{:.2f}".format(sample_estimates["sample_proportion"].quantile(0.9997)))
```

```{index} sampling distribution; shape
```

The sampling distribution in {numref}`fig:11-example-proportions7` appears
to be bell-shaped, is roughly symmetric, and has one peak. It is centered
around {glue:text}`sample_proportion_center` and the sample proportions
range from about {glue:text}`sample_proportion_min` to about
{glue:text}`sample_proportion_max`. In fact, we can
calculate the mean of the sample proportions.

```{code-cell} ipython3
sample_estimates["sample_proportion"].mean()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("sample_proportion_mean", "{:.3f}".format(sample_estimates["sample_proportion"].mean()))
```

We notice that the sample proportions are centered around the population
proportion value, {glue:text}`sample_proportion_mean`! In general, the mean of
the sampling distribution should be equal to the population proportion.
This is great news because it means that the sample proportion is neither an overestimate nor an
underestimate of the population proportion.
In other words, if you were to take many samples as we did above, there is no tendency
towards over or underestimating the population proportion.
In a real data analysis setting where you just have access to your single
sample, this implies that you would suspect that your sample point estimate is
roughly equally likely to be above or below the true population proportion.

+++

### Sampling distributions for means

In the previous section, our variable of interest&mdash;`room_type`&mdash;was
*categorical*, and the population parameter was a proportion. As mentioned in
the chapter introduction, there are many choices of the population parameter
for each type of variable. What if we wanted to infer something about a
population of *quantitative* variables instead? For instance, a traveler
visiting Vancouver, Canada may wish to estimate the
population *mean* (or average) price per night of Airbnb listings. Knowing
the average could help them tell whether a particular listing is overpriced.
We can visualize the population distribution of the price per night with a histogram.

```{code-cell} ipython3
:tags: [remove-output]

population_distribution = alt.Chart(airbnb).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()", title="Count"),
)

population_distribution
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:11-example-means2", population_distribution)
```

:::{glue:figure} fig:11-example-means2
:name: fig:11-example-means2

Population distribution of price per night (dollars) for all Airbnb listings in Vancouver, Canada.
:::

