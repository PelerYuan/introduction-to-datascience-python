### Calculating summary statistics on individual columns

```{index} summarize
```

As a part of many data analyses, we need to calculate a summary value for the
data (a *summary statistic*).
Examples of summary statistics we might want to calculate
are the number of observations, the average/mean value for a column,
the minimum value, etc.
Oftentimes,
this summary statistic is calculated from the values in a data frame column,
or columns, as shown in {numref}`fig:summarize`.

+++ {"tags": []}

```{figure} img/wrangling/summarize.001.png
:name: fig:summarize
:figclass: figure

Calculating summary statistics on one or more column(s) in `pandas` generally
creates a series or data frame containing the summary statistic(s) for each column
being summarized. The darker, top row of each table represents column headers.
```

