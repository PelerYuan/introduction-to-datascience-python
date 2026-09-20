```{index} see: tuning parameter; parameter
```

The vast majority of predictive models in statistics and machine learning have
*parameters*. A *parameter*
is a number you have to pick in advance that determines
some aspect of how the model behaves. For example, in the K-nearest neighbors
classification algorithm, $K$ is a parameter that we have to pick
that determines how many neighbors participate in the class vote.
By picking different values of $K$, we create different classifiers
that make different predictions.

So then, how do we pick the *best* value of $K$, i.e., *tune* the model?
And is it possible to make this selection in a principled way?  In this book,
we will focus on maximizing the accuracy of the classifier. Ideally,
we want somehow to maximize the accuracy of our classifier on data *it
hasn't seen yet*. But we cannot use our test data set in the process of building
our model. So we will play the same trick we did before when evaluating
our classifier: we'll split our *training data itself* into two subsets,
use one to train the model, and then use the other to evaluate it.
In this section, we will cover the details of this procedure, as well as
how to use it to help you pick a good parameter value for your classifier.

**And remember:** don't touch the test set during the tuning process. Tuning is a part of model training!

