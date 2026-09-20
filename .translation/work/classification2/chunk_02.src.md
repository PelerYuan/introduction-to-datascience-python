+++

```{index} scikit-learn; train_test_split, shuffling, stratification
```

The `train_test_split` function from `scikit-learn` handles the procedure of splitting
the data for us. We can specify two very important parameters when using `train_test_split` to ensure
that the accuracy estimates from the test data are reasonable. First,
setting `shuffle=True` (which is the default) means the data will be shuffled before splitting,
which ensures that any ordering present
in the data does not influence the data that ends up in the training and testing sets.
Second, by specifying the `stratify` parameter to be the response variable in the training set,
it **stratifies** the data by the class label, to ensure that roughly
the same proportion of each class ends up in both the training and testing sets. For example,
in our data set, roughly 63% of the
observations are from the benign class (`Benign`), and 37% are from the malignant class (`Malignant`),
so specifying `stratify` as the class column ensures that roughly 63% of the training data are benign,
37% of the training data are malignant,
and the same proportions exist in the testing data.

Let's use the `train_test_split` function to create the training and testing sets.
We first need to import the function from the `sklearn` package. Then
we will specify that `train_size=0.75` so that 75% of our original data set ends up
in the training set. We will also set the `stratify` argument to the categorical label variable
(here, `cancer["Class"]`) to ensure that the training and testing subsets contain the
right proportions of each category of observation.

```{code-cell} ipython3
:tags: [remove-cell]
# seed hacking
np.random.seed(3)
```

```{code-cell} ipython3
from sklearn.model_selection import train_test_split

cancer_train, cancer_test = train_test_split(
    cancer, train_size=0.75, stratify=cancer["Class"]
)
cancer_train.info()
```

```{code-cell} ipython3
cancer_test.info()
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cancer_train_nrow", "{:d}".format(len(cancer_train)))
glue("cancer_test_nrow", "{:d}".format(len(cancer_test)))
```

```{index} DataFrame; info
```

We can see from the `info` method above that the training set contains {glue:text}`cancer_train_nrow` observations,
while the test set contains {glue:text}`cancer_test_nrow` observations. This corresponds to
a train / test split of 75% / 25%, as desired. Recall from {numref}`Chapter %s <classification1>`
that we use the `info` method to preview the number of rows, the variable names, their data types, and
missing entries of a data frame.

```{index} Series; value_counts
```

We can use the `value_counts` method with the `normalize` argument set to `True`
to find the percentage of malignant and benign classes
in `cancer_train`. We see about {glue:text}`cancer_train_b_prop`% of the training
data are benign and {glue:text}`cancer_train_m_prop`%
are malignant, indicating that our class proportions were roughly preserved when we split the data.

```{code-cell} ipython3
cancer_train["Class"].value_counts(normalize=True)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("cancer_train_b_prop", "{:0.0f}".format(cancer_train["Class"].value_counts(normalize=True)["Benign"]*100))
glue("cancer_train_m_prop", "{:0.0f}".format(cancer_train["Class"].value_counts(normalize=True)["Malignant"]*100))
```

### Preprocess the data

As we mentioned in the last chapter, K-nearest neighbors is sensitive to the scale of the predictors,
so we should perform some preprocessing to standardize them. An
additional consideration we need to take when doing this is that we should
create the standardization preprocessor using **only the training data**. This ensures that
our test data does not influence any aspect of our model training. Once we have
created the standardization preprocessor, we can then apply it separately to both the
training and test data sets.

+++

```{index} scikit-learn; Pipeline, scikit-learn; make_column_transformer, scikit-learn; StandardScaler
```

Fortunately, `scikit-learn` helps us handle this properly as long as we wrap our
analysis steps in a `Pipeline`, as in {numref}`Chapter %s <classification1>`.
So below we construct and prepare
the preprocessor using `make_column_transformer` just as before.

```{code-cell} ipython3
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer

cancer_preprocessor = make_column_transformer(
    (StandardScaler(), ["Smoothness", "Concavity"]),
)
```

### Train the classifier

Now that we have split our original data set into training and test sets, we
can create our K-nearest neighbors classifier with only the training set using
the technique we learned in the previous chapter. For now, we will just choose
the number $K$ of neighbors to be 3, and use only the concavity and smoothness predictors by
selecting them from the `cancer_train` data frame.
We will first import the `KNeighborsClassifier` model and `make_pipeline` from `sklearn`.
Then as before we will create a model object, combine
the model object and preprocessor into a `Pipeline` using the `make_pipeline` function, and then finally
use the `fit` method to build the classifier.

```{code-cell} ipython3
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline

knn = KNeighborsClassifier(n_neighbors=3)

X = cancer_train[["Smoothness", "Concavity"]]
y = cancer_train["Class"]

knn_pipeline = make_pipeline(cancer_preprocessor, knn)
knn_pipeline.fit(X, y)

knn_pipeline
```

### Predict the labels in the test set

```{index} scikit-learn; predict
```

Now that we have a K-nearest neighbors classifier object, we can use it to
predict the class labels for our test set and
augment the original test data with a column of predictions.
The `Class` variable contains the actual
diagnoses, while the `predicted` contains the predicted diagnoses from the
classifier. Note that below we print out just the `ID`, `Class`, and `predicted`
variables in the output data frame.

```{code-cell} ipython3
cancer_test["predicted"] = knn_pipeline.predict(cancer_test[["Smoothness", "Concavity"]])
cancer_test[["ID", "Class", "predicted"]]
```

(eval-performance-clasfcn2)=
### Evaluate performance

```{index} scikit-learn; score, scikit-learn; precision_score, scikit-learn; recall_score
```

Finally, we can assess our classifier's performance. First, we will examine accuracy.
To do this we will use the `score` method, specifying two arguments:
predictors and the actual labels. We pass the same test data
for the predictors that we originally passed into `predict` when making predictions,
and we provide the actual labels via the `cancer_test["Class"]` series.

```{code-cell} ipython3
knn_pipeline.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
```

```{code-cell} ipython3
:tags: [remove-cell]
from sklearn.metrics import recall_score, precision_score

cancer_acc_1 = knn_pipeline.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
cancer_prec_1 = precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label="Malignant"
)
cancer_rec_1 = recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label="Malignant"
)

glue("cancer_acc_1", "{:0.0f}".format(100*cancer_acc_1))
glue("cancer_prec_1", "{:0.0f}".format(100*cancer_prec_1))
glue("cancer_rec_1", "{:0.0f}".format(100*cancer_rec_1))
```

+++

The output shows that the estimated accuracy of the classifier on the test data
was {glue:text}`cancer_acc_1`%. To compute the precision and recall, we can use the
`precision_score` and `recall_score` functions from `scikit-learn`. We specify
the true labels from the `Class` variable as the `y_true` argument, the predicted
labels from the `predicted` variable as the `y_pred` argument,
and which label should be considered to be positive via the `pos_label` argument.
```{code-cell} ipython3
from sklearn.metrics import recall_score, precision_score

precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label="Malignant"
)
```

```{code-cell} ipython3
recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label="Malignant"
)
```
The output shows that the estimated precision and recall of the classifier on the test
data was {glue:text}`cancer_prec_1`% and {glue:text}`cancer_rec_1`%, respectively.
Finally, we can look at the *confusion matrix* for the classifier
using the `crosstab` function from `pandas`. The `crosstab` function takes two
arguments: the actual labels first, then the predicted labels second. Note that
`crosstab` orders its columns alphabetically, but the positive label is still `Malignant`,
even if it is not in the top left corner as in the example confusion matrix earlier in this chapter.

```{index} crosstab
```

```{code-cell} ipython3
pd.crosstab(
    cancer_test["Class"],
    cancer_test["predicted"]
)
```

```{code-cell} ipython3
:tags: [remove-cell]
_ctab = pd.crosstab(cancer_test["Class"],
            cancer_test["predicted"]
           )

c11 = _ctab["Malignant"]["Malignant"]
c00 = _ctab["Benign"]["Benign"]
c10 = _ctab["Benign"]["Malignant"] # classify benign, true malignant
c01 = _ctab["Malignant"]["Benign"] # classify malignant, true benign

glue("confu11", "{:d}".format(c11))
glue("confu00", "{:d}".format(c00))
glue("confu10", "{:d}".format(c10))
glue("confu01", "{:d}".format(c01))
glue("confu11_00", "{:d}".format(c11 + c00))
glue("confu10_11", "{:d}".format(c10 + c11))
glue("confu_fal_neg", "{:0.0f}".format(100 * c10 / (c10 + c11)))
glue("confu_accuracy", "{:.2f}".format(100*(c00+c11)/(c00+c11+c01+c10)))
glue("confu_precision", "{:.2f}".format(100*c11/(c11+c01)))
glue("confu_recall", "{:.2f}".format(100*c11/(c11+c10)))
glue("confu_precision_0", "{:0.0f}".format(100*c11/(c11+c01)))
glue("confu_recall_0", "{:0.0f}".format(100*c11/(c11+c10)))
```

The confusion matrix shows {glue:text}`confu11` observations were correctly predicted
as malignant, and {glue:text}`confu00` were correctly predicted as benign.
It also shows that the classifier made some mistakes; in particular,
it classified {glue:text}`confu10` observations as benign when they were actually malignant,
and {glue:text}`confu01` observations as malignant when they were actually benign.
Using our formulas from earlier, we see that the accuracy, precision, and recall agree with what Python reported.

```{code-cell} ipython3
:tags: [remove-cell]

from IPython.display import display, Math
# accuracy string
acc_eq_str = r"\mathrm{accuracy} = \frac{\mathrm{number \; of  \; correct  \; predictions}}{\mathrm{total \;  number \;  of  \; predictions}} = \frac{"
acc_eq_str += str(c00) + "+" + str(c11) + "}{" + str(c00) + "+" + str(c11) + "+" + str(c01) + "+" + str(c10) + "} = " + str( np.round(100*(c00+c11)/(c00+c11+c01+c10),2))
acc_eq_math = Math(acc_eq_str)
glue("acc_eq_math_glued", acc_eq_math)

prec_eq_str = r"\mathrm{precision} = \frac{\mathrm{number \; of  \; correct  \; positive \; predictions}}{\mathrm{total \;  number \;  of  \; positive \; predictions}} = \frac{"
prec_eq_str += str(c11) + "}{" + str(c11) + "+" + str(c01) + "} = " + str( np.round(100*c11/(c11+c01), 2))
prec_eq_math = Math(prec_eq_str)
glue("prec_eq_math_glued", prec_eq_math)

rec_eq_str = r"\mathrm{recall} = \frac{\mathrm{number \; of  \; correct  \; positive \; predictions}}{\mathrm{total \;  number \;  of  \; positive \; test \; set \; observations}} = \frac{"
rec_eq_str += str(c11) + "}{" + str(c11) + "+" + str(c10) + "} = " + str( np.round(100*c11/(c11+c10), 2))
rec_eq_math = Math(rec_eq_str)
glue("rec_eq_math_glued", rec_eq_math)
```

```{glue:math} acc_eq_math_glued
```	

```{glue:math} prec_eq_math_glued
```	

```{glue:math} rec_eq_math_glued
```	

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

