## Predictor variable selection

```{note}
This section is not required reading for the remainder of the textbook. It is included for those readers
interested in learning how irrelevant variables can influence the performance of a classifier, and how to
pick a subset of useful variables to include as predictors.
```

```{index} irrelevant predictors
```

Another potentially important part of tuning your classifier is to choose which
variables from your data will be treated as predictor variables. Technically, you can choose
anything from using a single predictor variable to using every variable in your
data; the K-nearest neighbors algorithm accepts any number of
predictors. However, it is **not** the case that using more predictors always
yields better predictions! In fact, sometimes including irrelevant predictors can
actually negatively affect classifier performance.

+++ {"toc-hr-collapsed": true}

### The effect of irrelevant predictors

Let's take a look at an example where K-nearest neighbors performs
worse when given more predictors to work with. In this example, we modified
the breast cancer data to have only the `Smoothness`, `Concavity`, and
`Perimeter` variables from the original data. Then, we added irrelevant
variables that we created ourselves using a random number generator.
The irrelevant variables each take a value of 0 or 1 with equal probability for each observation, regardless
of what the value `Class` variable takes. In other words, the irrelevant variables have
no meaningful relationship with the `Class` variable.

```{code-cell} ipython3
:tags: [remove-cell]

np.random.seed(4)
cancer_irrelevant = cancer[["Class", "Smoothness", "Concavity", "Perimeter"]]
d = {
    f"Irrelevant{i+1}": np.random.choice(
        [0, 1], size=len(cancer_irrelevant), replace=True
    )
    for i in range(40)  ## in R textbook, it is 500, but the downstream analysis only uses up to 40
}
cancer_irrelevant = pd.concat((cancer_irrelevant, pd.DataFrame(d)), axis=1)
```

```{code-cell} ipython3
cancer_irrelevant[
    ["Class", "Smoothness", "Concavity", "Perimeter", "Irrelevant1", "Irrelevant2"]
]
```

Next, we build a sequence of K-NN classifiers that include `Smoothness`,
`Concavity`, and `Perimeter` as predictor variables, but also increasingly many irrelevant
variables. In particular, we create 6 data sets with 0, 5, 10, 15, 20, and 40 irrelevant predictors.
Then we build a model, tuned via 5-fold cross-validation, for each data set.
{numref}`fig:06-performance-irrelevant-features` shows
the estimated cross-validation accuracy versus the number of irrelevant predictors.  As
we add more irrelevant predictor variables, the estimated accuracy of our
classifier decreases. This is because the irrelevant variables add a random
amount to the distance between each pair of observations; the more irrelevant
variables there are, the more (random) influence they have, and the more they
corrupt the set of nearest neighbors that vote on the class of the new
observation to predict.

```{code-cell} ipython3
:tags: [remove-cell]

# get accuracies after including k irrelevant features
ks = [0, 5, 10, 15, 20, 40]
fixedaccs = list()
accs = list()
nghbrs = list()

for i in range(len(ks)):
    cancer_irrelevant_subset = cancer_irrelevant.iloc[:, : (4 + ks[i])]
    cancer_preprocessor = make_column_transformer(
        (
            StandardScaler(),
            list(cancer_irrelevant_subset.drop(columns=["Class"]).columns),
        ),
    )
    cancer_tune_pipe = make_pipeline(cancer_preprocessor, KNeighborsClassifier())
    param_grid = {
        "kneighborsclassifier__n_neighbors": range(1, 21),
    }  
    cancer_tune_grid = GridSearchCV(
        estimator=cancer_tune_pipe,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        return_train_score=True,
    )

    X = cancer_irrelevant_subset.drop(columns=["Class"])
    y = cancer_irrelevant_subset["Class"]

    cancer_model_grid = cancer_tune_grid.fit(X, y)
    accuracies_grid = pd.DataFrame(cancer_model_grid.cv_results_)
    sorted_accuracies = accuracies_grid.sort_values(
        by="mean_test_score", ascending=False
    )

    res = sorted_accuracies.iloc[0, :]
    accs.append(res["mean_test_score"])
    nghbrs.append(res["param_kneighborsclassifier__n_neighbors"])

    ## Use fixed n_neighbors=3
    cancer_fixed_pipe = make_pipeline(
        cancer_preprocessor, KNeighborsClassifier(n_neighbors=3)
    )

    cv_5 = cross_validate(estimator=cancer_fixed_pipe, X=X, y=y, cv=5)
    cv_5_metrics = pd.DataFrame(cv_5).agg(["mean", "sem"])
    fixedaccs.append(cv_5_metrics.loc["mean", "test_score"])
```

```{code-cell} ipython3
:tags: [remove-cell]

summary_df = pd.DataFrame(
    {"ks": ks, "nghbrs": nghbrs, "accs": accs, "fixedaccs": fixedaccs}
)
plt_irrelevant_accuracies = (
    alt.Chart(summary_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "accs",
            title="Model Accuracy Estimate",
            scale=alt.Scale(zero=False),
        ),
    )
)
glue("fig:06-performance-irrelevant-features", plt_irrelevant_accuracies)
```

:::{glue:figure} fig:06-performance-irrelevant-features
:name: fig:06-performance-irrelevant-features

Effect of inclusion of irrelevant predictors.
:::

Although the accuracy decreases as expected, one surprising thing about
{numref}`fig:06-performance-irrelevant-features` is that it shows that the method
still outperforms the baseline majority classifier (with about {glue:text}`cancer_train_b_prop`% accuracy)
even with 40 irrelevant variables.
How could that be? {numref}`fig:06-neighbors-irrelevant-features` provides the answer:
the tuning procedure for the K-nearest neighbors classifier combats the extra randomness from the irrelevant variables
by increasing the number of neighbors. Of course, because of all the extra noise in the data from the irrelevant
variables, the number of neighbors does not increase smoothly; but the general trend is increasing. {numref}`fig:06-fixed-irrelevant-features` corroborates
this evidence; if we fix the number of neighbors to $K=3$, the accuracy falls off more quickly.

```{code-cell} ipython3
:tags: [remove-cell]

plt_irrelevant_nghbrs = (
    alt.Chart(summary_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "nghbrs",
            title="Tuned number of neighbors",
        ),
    )
)
glue("fig:06-neighbors-irrelevant-features", plt_irrelevant_nghbrs)
```

:::{glue:figure} fig:06-neighbors-irrelevant-features
:name: fig:06-neighbors-irrelevant-features

Tuned number of neighbors for varying number of irrelevant predictors.
:::

```{code-cell} ipython3
:tags: [remove-cell]

melted_summary_df = summary_df.melt(
            id_vars=["ks", "nghbrs"], var_name="Type", value_name="Accuracy"
        )
melted_summary_df["Type"] = melted_summary_df["Type"].apply(lambda x: "Tuned K" if x=="accs" else "K = 3")

plt_irrelevant_nghbrs_fixed = (
    alt.Chart(
        melted_summary_df
    )
    .mark_line(point=True)
    .encode(
        x=alt.X("ks", title="Number of Irrelevant Predictors"),
        y=alt.Y(
            "Accuracy",
            scale=alt.Scale(zero=False),
        ),
        color=alt.Color("Type"),
    )
)
glue("fig:06-fixed-irrelevant-features", plt_irrelevant_nghbrs_fixed)
```

:::{glue:figure} fig:06-fixed-irrelevant-features
:name: fig:06-fixed-irrelevant-features

Accuracy versus number of irrelevant predictors for tuned and untuned number of neighbors.
:::

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

