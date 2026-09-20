+++

```{index} see: feature engineering; predictor design
```

The process of
transforming predictors (and potentially combining multiple predictors in the process)
is known as *feature engineering*. In real data analysis
problems, you will need to rely on
a deep understanding of the problem&mdash;as well as the wrangling tools
from previous chapters&mdash;to engineer useful new features that improve
predictive performance.

```{note}
Feature engineering
is *part of tuning your model*, and as such you must not use your test data
to evaluate the quality of the features you produce. You are free to use
cross-validation, though!
```

+++

## The other sides of regression

So far in this textbook we have used regression only in the context of
prediction. However, regression can also be seen as a method to understand and
quantify the effects of individual variables on a response variable of interest.
In the housing example from this chapter, beyond just using past data
to predict future sale prices,
we might also be interested in describing the
individual relationships of house size and the number of bedrooms with house price,
quantifying how strong each of these relationships are, and assessing how accurately we
can estimate their magnitudes. And even beyond that, we may be interested in
understanding whether the predictors *cause* changes in the price.
These sides of regression are well beyond the scope of this book; but
the material you have learned here should give you a foundation of knowledge
that will serve you well when moving to more advanced books on the topic.

+++

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Regression II: linear regression" row. You can preview a
non-interactive version of the worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.



+++

## Additional resources

- The [`scikit-learn` website](https://scikit-learn.org/stable/) is an excellent
  reference for more details on, and advanced usage of, the functions and
  packages in the past two chapters. Aside from that, it also offers many
  useful [tutorials](https://scikit-learn.org/stable/tutorial/index.html) and [an extensive list
  of more advanced examples](https://scikit-learn.org/stable/auto_examples/index.html#general-examples)
  that you can use to continue learning beyond the scope of this book.
- *An Introduction to Statistical Learning* {cite:p}`james2013introduction` provides
  a great next stop in the process of
  learning about regression. Chapter 3 covers linear regression at a slightly
  more mathematical level than we do here, but it is not too large a leap and so
  should provide a good stepping stone. Chapter 6 discusses how to pick a subset
  of "informative" predictors when you have a data set with many predictors, and
  you expect only a few of them to be relevant. Chapter 7 covers regression
  models that are more flexible than linear regression models but still enjoy the
  computational efficiency of linear regression. In contrast, the K-NN methods we
  covered earlier are indeed more flexible but become very slow when given lots
  of data.

+++

## References

```{bibliography}
:filter: docname in docnames
```
