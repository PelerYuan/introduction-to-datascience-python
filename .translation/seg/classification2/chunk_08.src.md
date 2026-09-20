+++

### Finding a good subset of predictors

So then, if it is not ideal to use all of our variables as predictors without consideration, how
do we choose which variables we *should* use?  A simple method is to rely on your scientific understanding
of the data to tell you which variables are not likely to be useful predictors. For example, in the cancer
data that we have been studying, the `ID` variable is just a unique identifier for the observation.
As it is not related to any measured property of the cells, the `ID` variable should therefore not be used
as a predictor. That is, of course, a very clear-cut case. But the decision for the remaining variables
is less obvious, as all seem like reasonable candidates. It
is not clear which subset of them will create the best classifier. One could use visualizations and
other exploratory analyses to try to help understand which variables are potentially relevant, but
this process is both time-consuming and error-prone when there are many variables to consider.
Therefore we need a more systematic and programmatic way of choosing variables.
This is a very difficult problem to solve in
general, and there are a number of methods that have been developed that apply
in particular cases of interest. Here we will discuss two basic
selection methods as an introduction to the topic. See the additional resources at the end of
this chapter to find out where you can learn more about variable selection, including more advanced methods.

```{index} variable selection; best subset
```

```{index} see: predictor selection; variable selection
```

The first idea you might think of for a systematic way to select predictors
is to try all possible subsets of predictors and then pick the set that results in the "best" classifier.
This procedure is indeed a well-known variable selection method referred to
as *best subset selection* {cite:p}`bealesubset,hockingsubset`.
In particular, you

1. create a separate model for every possible subset of predictors,
2. tune each one using cross-validation, and
3. pick the subset of predictors that gives you the highest cross-validation accuracy.

Best subset selection is applicable to any classification method (K-NN or otherwise).
However, it becomes very slow when you have even a moderate
number of predictors to choose from (say, around 10). This is because the number of possible predictor subsets
grows very quickly with the number of predictors, and you have to train the model (itself
a slow process!) for each one. For example, if we have 2 predictors&mdash;let's call
them A and B&mdash;then we have 3 variable sets to try: A alone, B alone, and finally A
and B together. If we have 3 predictors&mdash;A, B, and C&mdash;then we have 7
to try: A, B, C, AB, BC, AC, and ABC. In general, the number of models
we have to train for $m$ predictors is $2^m-1$; in other words, when we
get to 10 predictors we have over *one thousand* models to train, and
at 20 predictors we have over *one million* models to train!
So although it is a simple method, best subset selection is usually too computationally
expensive to use in practice.

```{index} variable selection; forward
```

Another idea is to iteratively build up a model by adding one predictor variable
at a time. This method&mdash;known as *forward selection* {cite:p}`forwardefroymson,forwarddraper`&mdash;is also widely
applicable and fairly straightforward. It involves the following steps:

1. Start with a model having no predictors.
2. Run the following 3 steps until you run out of predictors:
    1. For each unused predictor, add it to the model to form a *candidate model*.
    2. Tune all of the candidate models.
    3. Update the model to be the candidate model with the highest cross-validation accuracy.
3. Select the model that provides the best trade-off between accuracy and simplicity.

Say you have $m$ total predictors to work with. In the first iteration, you have to make
$m$ candidate models, each with 1 predictor. Then in the second iteration, you have
to make $m-1$ candidate models, each with 2 predictors (the one you chose before and a new one).
This pattern continues for as many iterations as you want. If you run the method
all the way until you run out of predictors to choose, you will end up training
$\frac{1}{2}m(m+1)$ separate models. This is a *big* improvement from the $2^m-1$
models that best subset selection requires you to train! For example, while best subset selection requires
training over 1000 candidate models with 10 predictors, forward selection requires training only 55 candidate models.
Therefore we will continue the rest of this section using forward selection.

```{note}
One word of caution before we move on. Every additional model that you train
increases the likelihood that you will get unlucky and stumble
on a model that has a high cross-validation accuracy estimate, but a low true
accuracy on the test data and other future observations.
Since forward selection involves training a lot of models, you run a fairly
high risk of this happening. To keep this risk low, only use forward selection
when you have a large amount of data and a relatively small total number of
predictors. More advanced methods do not suffer from this
problem as much; see the additional resources at the end of this chapter for
where to learn more about advanced predictor selection methods.
```

+++

### Forward selection in Python

```{index} variable selection; implementation
```

We now turn to implementing forward selection in Python.
First we will extract a smaller set of predictors to work with in this illustrative example&mdash;`Smoothness`,
`Concavity`, `Perimeter`, `Irrelevant1`, `Irrelevant2`, and `Irrelevant3`&mdash;as well as the `Class` variable as the label.
We will also extract the column names for the full set of predictors.

```{code-cell} ipython3
cancer_subset = cancer_irrelevant[
    [
        "Class",
        "Smoothness",
        "Concavity",
        "Perimeter",
        "Irrelevant1",
        "Irrelevant2",
        "Irrelevant3",
    ]
]

names = list(cancer_subset.drop(
    columns=["Class"]
).columns.values)

cancer_subset
```

To perform forward selection, we could use the
[`SequentialFeatureSelector`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html)
from `scikit-learn`; but it is difficult to combine this approach with parameter tuning to find a good number of neighbors
for each set of features. Instead we will code the forward selection algorithm manually.
In particular, we need code that tries adding each available predictor to a model, finding the best, and iterating.
If you recall the end of the wrangling chapter, we mentioned
that sometimes one needs more flexible forms of iteration than what
we have used earlier, and in these cases one typically resorts to
a *for loop*; see
the [control flow section](https://wesmckinney.com/book/python-basics.html#control_for) in
*Python for Data Analysis* {cite:p}`mckinney2012python`.
Here we will use two for loops: one over increasing predictor set sizes
(where you see `for i in range(1, n_total + 1):` below),
and another to check which predictor to add in each round (where you see `for j in range(len(names))` below).
For each set of predictors to try, we extract the subset of predictors,
pass it into a preprocessor, build a `Pipeline` that tunes
a K-NN classifier using 10-fold cross-validation,
and finally records the estimated accuracy.

```{code-cell} ipython3
from sklearn.compose import make_column_selector

accuracy_dict = {"size": [], "selected_predictors": [], "accuracy": []}

# store the total number of predictors
n_total = len(names)

# start with an empty list of selected predictors
selected = []

# create the pipeline and CV grid search objects
param_grid = {
    "kneighborsclassifier__n_neighbors": range(1, 61, 5),
}
cancer_preprocessor = make_column_transformer(
    (StandardScaler(), make_column_selector(dtype_include="number"))
)
cancer_tune_pipe = make_pipeline(cancer_preprocessor, KNeighborsClassifier())
cancer_tune_grid = GridSearchCV(
    estimator=cancer_tune_pipe,
    param_grid=param_grid,
    cv=10,
    n_jobs=-1
)

# for every possible number of predictors
for i in range(1, n_total + 1):
    accs = np.zeros(len(names))
    # for every possible predictor to add
    for j in range(len(names)):
        # Add remaining predictor j to the model
        X = cancer_subset[selected + [names[j]]]
        y = cancer_subset["Class"]

        # Find the best K for this set of predictors
        cancer_tune_grid.fit(X, y)
        accuracies_grid = pd.DataFrame(cancer_tune_grid.cv_results_)

        # Store the tuned accuracy for this set of predictors
        accs[j] = accuracies_grid["mean_test_score"].max()

    # get the best new set of predictors that maximize cv accuracy
    best_set = selected + [names[accs.argmax()]]

    # store the results for this round of forward selection
    accuracy_dict["size"].append(i)
    accuracy_dict["selected_predictors"].append(", ".join(best_set))
    accuracy_dict["accuracy"].append(accs.max())

    # update the selected & available sets of predictors
    selected = best_set
    del names[accs.argmax()]

accuracies = pd.DataFrame(accuracy_dict)
accuracies
```

```{index} variable selection; elbow method
```

Interesting! The forward selection procedure first added the three meaningful variables `Perimeter`,
`Concavity`, and `Smoothness`, followed by the irrelevant variables. {numref}`fig:06-fwdsel-3`
visualizes the accuracy versus the number of predictors in the model. You can see that
as meaningful predictors are added, the estimated accuracy increases substantially; and as you add irrelevant
variables, the accuracy either exhibits small fluctuations or decreases as the model attempts to tune the number
of neighbors to account for the extra noise. In order to pick the right model from the sequence, you have
to balance high accuracy and model simplicity (i.e., having fewer predictors and a lower chance of overfitting).
The way to find that balance is to look for the *elbow*
in {numref}`fig:06-fwdsel-3`, i.e., the place on the plot where the accuracy stops increasing dramatically and
levels off or begins to decrease. The elbow in {numref}`fig:06-fwdsel-3` appears to occur at the model with
3 predictors; after that point the accuracy levels off. So here the right trade-off of accuracy and number of predictors
occurs with 3 variables: `Perimeter, Concavity, Smoothness`. In other words, we have successfully removed irrelevant
predictors from the model! It is always worth remembering, however, that what cross-validation gives you
is an *estimate* of the true accuracy; you have to use your judgement when looking at this plot to decide
where the elbow occurs, and whether adding a variable provides a meaningful increase in accuracy.

```{code-cell} ipython3
:tags: [remove-cell]

fwd_sel_accuracies_plot = (
    alt.Chart(accuracies)
    .mark_line(point=True)
    .encode(
        x=alt.X("size", title="Number of Predictors"),
        y=alt.Y(
            "accuracy",
            title="Estimated Accuracy",
            scale=alt.Scale(zero=False),
        ),
    )
)
glue("fig:06-fwdsel-3", fwd_sel_accuracies_plot)
```

:::{glue:figure} fig:06-fwdsel-3
:name: fig:06-fwdsel-3

Estimated accuracy versus the number of predictors for the sequence of models built using forward selection.
:::

+++

```{note}
Since the choice of which variables to include as predictors is
part of tuning your classifier, you *cannot use your test data* for this
process!
```

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Classification II: evaluation and tuning" row. You can preview a
non-interactive version of the worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.

+++

## Additional resources

+++

- The [`scikit-learn` website](https://scikit-learn.org/stable/) is an excellent
  reference for more details on, and advanced usage of, the functions and
  packages in the past two chapters. Aside from that, it also offers many
  useful [tutorials](https://scikit-learn.org/stable/tutorial/index.html)
  to get you started. It's worth noting that the `scikit-learn` package
  does a lot more than just classification, and so the
  examples on the website similarly go beyond classification as well. In the next
  two chapters, you'll learn about another kind of predictive modeling setting,
  so it might be worth visiting the website only after reading through those
  chapters.
- [*An Introduction to Statistical Learning*](https://www.statlearning.com/) {cite:p}`james2013introduction` provides
  a great next stop in the process of
  learning about classification. Chapter 4 discusses additional basic techniques
  for classification that we do not cover, such as logistic regression, linear
  discriminant analysis, and naive Bayes. Chapter 5 goes into much more detail
  about cross-validation. Chapters 8 and 9 cover decision trees and support
  vector machines, two very popular but more advanced classification methods.
  Finally, Chapter 6 covers a number of methods for selecting predictor
  variables. Note that while this book is still a very accessible introductory
  text, it requires a bit more mathematical background than we require.


+++

## References

```{bibliography}
:filter: docname in docnames
```
