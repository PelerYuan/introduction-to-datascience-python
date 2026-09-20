+++

### Critically analyze performance

We now know that the classifier was {glue:text}`cancer_acc_1`% accurate
on the test data set, and had a precision of {glue:text}`cancer_prec_1`% and
a recall of {glue:text}`cancer_rec_1`%.
That sounds pretty good! Wait, *is* it good?
Or do we need something higher?

```{index} accuracy;assessment, precision;assessment, recall;assessment
```

In general, a *good* value for accuracy (as well as precision and recall, if applicable)
depends on the application; you must critically analyze your accuracy in the context of the problem
you are solving. For example, if we were building a classifier for a kind of tumor that is benign 99%
of the time, a classifier with 99% accuracy is not terribly impressive (just always guess benign!).
And beyond just accuracy, we need to consider the precision and recall: as mentioned
earlier, the *kind* of mistake the classifier makes is
important in many applications as well. In the previous example with 99% benign observations, it might be very bad for the
classifier to predict "benign" when the actual class is "malignant" (a false negative), as this
might result in a patient not receiving appropriate medical attention. In other
words, in this context, we need the classifier to have a *high recall*. On the
other hand, it might be less bad for the classifier to guess "malignant" when
the actual class is "benign" (a false positive), as the patient will then likely see a doctor who
can provide an expert diagnosis. In other words, we are fine with sacrificing
some precision in the interest of achieving high recall. This is why it is
important not only to look at accuracy, but also the confusion matrix.


```{index} classification; majority
```

However, there is always an easy baseline that you can compare to for any
classification problem: the *majority classifier*. The majority classifier
*always* guesses the majority class label from the training data, regardless of
the predictor variables' values.  It helps to give you a sense of
scale when considering accuracies. If the majority classifier obtains a 90%
accuracy on a problem, then you might hope for your K-nearest neighbors
classifier to do better than that. If your classifier provides a significant
improvement upon the majority classifier, this means that at least your method
is extracting some useful information from your predictor variables.  Be
careful though: improving on the majority classifier does not *necessarily*
mean the classifier is working well enough for your application.

As an example, in the breast cancer data, recall the proportions of benign and malignant
observations in the training data are as follows:

```{code-cell} ipython3
cancer_train["Class"].value_counts(normalize=True)
```

Since the benign class represents the majority of the training data,
the majority classifier would *always* predict that a new observation
is benign. The estimated accuracy of the majority classifier is usually
fairly close to the majority class proportion in the training data.
In this case, we would suspect that the majority classifier will have
an accuracy of around {glue:text}`cancer_train_b_prop`%.
The K-nearest neighbors classifier we built does quite a bit better than this,
with an accuracy of {glue:text}`cancer_acc_1`%.
This means that from the perspective of accuracy,
the K-nearest neighbors classifier improved quite a bit on the basic
majority classifier. Hooray! But we still need to be cautious; in
this application, it is likely very important not to misdiagnose any malignant tumors to avoid missing
patients who actually need medical care. The confusion matrix above shows
that the classifier does, indeed, misdiagnose a significant number of
malignant tumors as benign ({glue:text}`confu10` out of {glue:text}`confu10_11` malignant tumors, or {glue:text}`confu_fal_neg`%!).
Therefore, even though the accuracy improved upon the majority classifier,
our critical analysis suggests that this classifier may not have appropriate performance
for the application.

+++

## Tuning the classifier

```{index} parameter
```

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

+++

### Cross-validation

```{index} validation set
```

The first step in choosing the parameter $K$ is to be able to evaluate the
classifier using only the training data. If this is possible, then we can compare
the classifier's performance for different values of $K$&mdash;and pick the best&mdash;using
only the training data. As suggested at the beginning of this section, we will
accomplish this by splitting the training data, training on one subset, and evaluating
on the other. The subset of training data used for evaluation is often called the **validation set**.

There is, however, one key difference from the train/test split
that we performed earlier. In particular, we were forced to make only a *single split*
of the data. This is because at the end of the day, we have to produce a single classifier.
If we had multiple different splits of the data into training and testing data,
we would produce multiple different classifiers.
But while we are tuning the classifier, we are free to create multiple classifiers
based on multiple splits of the training data, evaluate them, and then choose a parameter
value based on __*all*__ of the different results. If we just split our overall training
data *once*, our best parameter choice will depend strongly on whatever data
was lucky enough to end up in the validation set. Perhaps using multiple
different train/validation splits, we'll get a better estimate of accuracy,
which will lead to a better choice of the number of neighbors $K$ for the
overall set of training data.

Let's investigate this idea in Python! In particular, we will generate five different train/validation
splits of our overall training data, train five different K-nearest neighbors
models, and evaluate their accuracy. We will start with just a single
split.

```{code-cell} ipython3
# create the 25/75 split of the *training data* into sub-training and validation
cancer_subtrain, cancer_validation = train_test_split(
    cancer_train, train_size=0.75, stratify=cancer_train["Class"]
)

# fit the model on the sub-training data
knn = KNeighborsClassifier(n_neighbors=3)
X = cancer_subtrain[["Smoothness", "Concavity"]]
y = cancer_subtrain["Class"]
knn_pipeline = make_pipeline(cancer_preprocessor, knn)
knn_pipeline.fit(X, y)

# compute the score on validation data
acc = knn_pipeline.score(
    cancer_validation[["Smoothness", "Concavity"]],
    cancer_validation["Class"]
)
acc
```

```{code-cell} ipython3
:tags: [remove-cell]

accuracies = [acc]
for i in range(1, 5):
    # create the 25/75 split of the training data into training and validation
    cancer_subtrain, cancer_validation = train_test_split(
        cancer_train, test_size=0.25
    )

    # fit the model on the sub-training data
    knn = KNeighborsClassifier(n_neighbors=3)
    X = cancer_subtrain[["Smoothness", "Concavity"]]
    y = cancer_subtrain["Class"]
    knn_pipeline = make_pipeline(cancer_preprocessor, knn).fit(X, y)

    # compute the score on validation data
    accuracies.append(knn_pipeline.score(
        cancer_validation[["Smoothness", "Concavity"]],
        cancer_validation["Class"]
       ))
avg_accuracy = np.round(np.array(accuracies).mean()*100,1)
accuracies = list(np.round(np.array(accuracies)*100, 1))
```

```{code-cell} ipython3
:tags: [remove-cell]
glue("acc_seed1", "{:0.1f}".format(100 * acc))
glue("avg_5_splits", "{:0.1f}".format(avg_accuracy))
glue("accuracies", "[" + "%, ".join(["{:0.1f}".format(acc) for acc in accuracies]) + "%]")
```
```{code-cell} ipython3
:tags: [remove-cell]

```

The accuracy estimate using this split is {glue:text}`acc_seed1`%.
Now we repeat the above code 4 more times, which generates 4 more splits.
Therefore we get five different shuffles of the data, and therefore five different values for
accuracy: {glue:text}`accuracies`. None of these values are
necessarily "more correct" than any other; they're
just five estimates of the true, underlying accuracy of our classifier built
using our overall training data. We can combine the estimates by taking their
average (here {glue:text}`avg_5_splits`%) to try to get a single assessment of our
classifier's accuracy; this has the effect of reducing the influence of any one
(un)lucky validation set on the estimate.

```{index} cross-validation
```

In practice, we don't use random splits, but rather use a more structured
splitting procedure so that each observation in the data set is used in a
validation set only a single time. The name for this strategy is
**cross-validation**.  In **cross-validation**, we split our **overall training
data** into $C$ evenly sized chunks. Then, iteratively use $1$ chunk as the
**validation set** and combine the remaining $C-1$ chunks
as the **training set**.
This procedure is shown in {numref}`fig:06-cv-image`.
Here, $C=5$ different chunks of the data set are used,
resulting in 5 different choices for the **validation set**; we call this
*5-fold* cross-validation.

+++

```{figure} img/classification2/cv.png
:name: fig:06-cv-image

5-fold cross-validation.
```


