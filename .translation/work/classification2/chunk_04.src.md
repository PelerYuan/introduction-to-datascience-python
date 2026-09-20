+++

### Under/Overfitting

To build a bit more intuition, what happens if we keep increasing the number of
neighbors $K$? In fact, the cross-validation accuracy estimate actually starts to decrease!
Let's specify a much larger range of values of $K$ to try in the `param_grid`
argument of `GridSearchCV`. {numref}`fig:06-lots-of-ks` shows a plot of estimated accuracy as
we vary $K$ from 1 to almost the number of observations in the data set.

```{code-cell} ipython3
:tags: [remove-output]

large_param_grid = {
    "kneighborsclassifier__n_neighbors": range(1, 385, 10),
}

large_cancer_tune_grid = GridSearchCV(
    estimator=cancer_tune_pipe,
    param_grid=large_param_grid,
    cv=10
)

large_cancer_tune_grid.fit(
    cancer_train[["Smoothness", "Concavity"]],
    cancer_train["Class"]
)

large_accuracies_grid = pd.DataFrame(large_cancer_tune_grid.cv_results_)

large_accuracy_vs_k = alt.Chart(large_accuracies_grid).mark_line(point=True).encode(
    x=alt.X("param_kneighborsclassifier__n_neighbors").title("Neighbors"),
    y=alt.Y("mean_test_score")
        .scale(zero=False)
        .title("Accuracy estimate")
)

large_accuracy_vs_k
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("fig:06-lots-of-ks", large_accuracy_vs_k)
```

:::{glue:figure} fig:06-lots-of-ks
:name: fig:06-lots-of-ks

Plot of accuracy estimate versus number of neighbors for many K values.
:::

+++

```{index} underfitting; classification
```

**Underfitting:** What is actually happening to our classifier that causes
this? As we increase the number of neighbors, more and more of the training
observations (and those that are farther and farther away from the point) get a
"say" in what the class of a new observation is. This causes a sort of
"averaging effect" to take place, making the boundary between where our
classifier would predict a tumor to be malignant versus benign to smooth out
and become *simpler.* If you take this to the extreme, setting $K$ to the total
training data set size, then the classifier will always predict the same label
regardless of what the new observation looks like. In general, if the model
*isn't influenced enough* by the training data, it is said to **underfit** the
data.

```{index} overfitting; classification
```

**Overfitting:** In contrast, when we decrease the number of neighbors, each
individual data point has a stronger and stronger vote regarding nearby points.
Since the data themselves are noisy, this causes a more "jagged" boundary
corresponding to a *less simple* model.  If you take this case to the extreme,
setting $K = 1$, then the classifier is essentially just matching each new
observation to its closest neighbor in the training data set. This is just as
problematic as the large $K$ case, because the classifier becomes unreliable on
new data: if we had a different training set, the predictions would be
completely different.  In general, if the model *is influenced too much* by the
training data, it is said to **overfit** the data.

```{code-cell} ipython3
:tags: [remove-cell]
alt.data_transformers.disable_max_rows()

cancer_plot = (
    alt.Chart(
        cancer_train,
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X(
            "Smoothness",
            scale=alt.Scale(
                domain=(
                    cancer_train["Smoothness"].min() * 0.95,
                    cancer_train["Smoothness"].max() * 1.05,
                )
            ),
        ),
        y=alt.Y(
            "Concavity",
            scale=alt.Scale(
                domain=(
                    cancer_train["Concavity"].min() -0.025,
                    cancer_train["Concavity"].max() * 1.05,
                )
            ),
        ),
        color=alt.Color("Class", title="Diagnosis"),
    )
)

X = cancer_train[["Smoothness", "Concavity"]]
y = cancer_train["Class"]

# create a prediction pt grid
smo_grid = np.linspace(
    cancer_train["Smoothness"].min() * 0.95, cancer_train["Smoothness"].max() * 1.05, 100
)
con_grid = np.linspace(
    cancer_train["Concavity"].min() - 0.025, cancer_train["Concavity"].max() * 1.05, 100
)
scgrid = np.array(np.meshgrid(smo_grid, con_grid)).reshape(2, -1).T
scgrid = pd.DataFrame(scgrid, columns=["Smoothness", "Concavity"])

plot_list = []
for k in [1, 7, 20, 300]:
    cancer_pipe = make_pipeline(cancer_preprocessor, KNeighborsClassifier(n_neighbors=k))
    cancer_pipe.fit(X, y)

    knnPredGrid = cancer_pipe.predict(scgrid)
    prediction_table = scgrid.copy()
    prediction_table["Class"] = knnPredGrid

    # add a prediction layer
    prediction_plot = (
        alt.Chart(
            prediction_table,
            title=f"K = {k}"
        )
        .mark_point(opacity=0.2, filled=True, size=20)
        .encode(
            x=alt.X(
                "Smoothness",
                scale=alt.Scale(
                    domain=(
                        cancer_train["Smoothness"].min() * 0.95,
                        cancer_train["Smoothness"].max() * 1.05
                    ),
                    nice=False
                )
            ),
            y=alt.Y(
                "Concavity",
                scale=alt.Scale(
                    domain=(
                        cancer_train["Concavity"].min() -0.025,
                        cancer_train["Concavity"].max() * 1.05
                    ),
                    nice=False
                )
            ),
            color=alt.Color("Class", title="Diagnosis"),
        )
    )
    plot_list.append(cancer_plot + prediction_plot)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue(
    "fig:06-decision-grid-K",
    ((plot_list[0] | plot_list[1])
    & (plot_list[2] | plot_list[3])).configure_legend(
        orient="bottom", titleAnchor="middle"
    ),
)
```

:::{glue:figure} fig:06-decision-grid-K
:name: fig:06-decision-grid-K

Effect of K in overfitting and underfitting.
:::

+++

Both overfitting and underfitting are problematic and will lead to a model that
does not generalize well to new data. When fitting a model, we need to strike a
balance between the two. You can see these two effects in
{numref}`fig:06-decision-grid-K`, which shows how the classifier changes as we
set the number of neighbors $K$ to 1, 7, 20, and 300.

+++

### Evaluating on the test set

Now that we have tuned the K-NN classifier and set $K =$ {glue:text}`best_k_unique`,
we are done building the model and it is time to evaluate the quality of its predictions on the held out 
test data, as we did earlier in {numref}`eval-performance-clasfcn2`.
We first need to retrain the K-NN classifier
on the entire training data set using the selected number of neighbors.
Fortunately we do not have to do this ourselves manually; `scikit-learn` does it for
us automatically. To make predictions and assess the estimated accuracy of the best model on the test data, we can use the
`score` and `predict` methods of the fit `GridSearchCV` object. We can then pass those predictions to
the `precision`, `recall`, and `crosstab` functions to assess the estimated precision and recall, and print a confusion matrix.

```{index} scikit-learn;predict, scikit-learn;score, scikit-learn;precision_score, scikit-learn;recall_score, crosstab
```

```{code-cell} ipython3
cancer_test["predicted"] = cancer_tune_grid.predict(
    cancer_test[["Smoothness", "Concavity"]]
)

cancer_tune_grid.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
```

```{code-cell} ipython3
precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
```

```{code-cell} ipython3
recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
```

```{code-cell} ipython3
pd.crosstab(
    cancer_test["Class"],
    cancer_test["predicted"]
)
```
```{code-cell} ipython3
:tags: [remove-cell]
cancer_prec_tuned = precision_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
cancer_rec_tuned = recall_score(
    y_true=cancer_test["Class"],
    y_pred=cancer_test["predicted"],
    pos_label='Malignant'
)
cancer_acc_tuned = cancer_tune_grid.score(
    cancer_test[["Smoothness", "Concavity"]],
    cancer_test["Class"]
)
glue("cancer_acc_tuned", "{:0.0f}".format(100*cancer_acc_tuned))
glue("cancer_prec_tuned", "{:0.0f}".format(100*cancer_prec_tuned))
glue("cancer_rec_tuned", "{:0.0f}".format(100*cancer_rec_tuned))
glue("mean_acc_ks", "{:0.0f}".format(100*accuracies_grid["mean_test_score"].mean()))
glue("std3_acc_ks", "{:0.0f}".format(3*100*accuracies_grid["mean_test_score"].std()))
glue("mean_sem_acc_ks", "{:0.0f}".format(100*accuracies_grid["sem_test_score"].mean()))
glue("n_neighbors_max", "{:0.0f}".format(accuracies_grid["n_neighbors"].max()))
glue("n_neighbors_min", "{:0.0f}".format(accuracies_grid["n_neighbors"].min()))
```

At first glance, this is a bit surprising: the accuracy of the classifier
has not changed much despite tuning the number of neighbors! Our first model
with $K =$ 3 (before we knew how to tune) had an estimated accuracy of {glue:text}`cancer_acc_1`%, 
while the tuned model with $K =$ {glue:text}`best_k_unique` had an estimated accuracy
of {glue:text}`cancer_acc_tuned`%. Upon examining {numref}`fig:06-find-k` again to see the
cross validation accuracy estimates for a range of neighbors, this result
becomes much less surprising. From {glue:text}`n_neighbors_min` to around {glue:text}`n_neighbors_max` neighbors, the cross
validation accuracy estimate varies only by around {glue:text}`std3_acc_ks`%, with
each estimate having a standard error around {glue:text}`mean_sem_acc_ks`%.
Since the cross-validation accuracy estimates the test set accuracy,
the fact that the test set accuracy also doesn't change much is expected.
Also note that the $K =$ 3 model had a precision 
of {glue:text}`cancer_prec_1`% and recall of {glue:text}`cancer_rec_1`%,
while the tuned model had
a precision of {glue:text}`cancer_prec_tuned`% and recall of {glue:text}`cancer_rec_tuned`%.
Given that the recall decreased&mdash;remember, in this application, recall
is critical to making sure we find all the patients with malignant tumors&mdash;the tuned model may actually be *less* preferred
in this setting. In any case, it is important to think critically about the result of tuning. Models tuned to
maximize accuracy are not necessarily better for a given application.

## Summary

Classification algorithms use one or more quantitative variables to predict the
value of another categorical variable. In particular, the K-nearest neighbors
algorithm does this by first finding the $K$ points in the training data
nearest to the new observation, and then returning the majority class vote from
those training observations. We can tune and evaluate a classifier by splitting
the data randomly into a training and test data set. The training set is used
to build the classifier, and we can tune the classifier (e.g., select the number
of neighbors in K-nearest neighbors) by maximizing estimated accuracy via
cross-validation. After we have tuned the model, we can use the test set to
estimate its accuracy.  The overall process is summarized in
{numref}`fig:06-overview`.

+++

```{figure} img/classification2/train-test-overview.png
:name: fig:06-overview

Overview of K-NN classification.
```

+++

```{index} scikit-learn;Pipeline, cross-validation, K-nearest neighbors; classification, classification
```

The overall workflow for performing K-nearest neighbors classification using `scikit-learn` is as follows:

1. Use the `train_test_split` function to split the data into a training and test set. Set the `stratify` argument to the class label column of the dataframe. Put the test set aside for now.
2. Create a `Pipeline` that specifies the preprocessing steps and the classifier.
3. Define the parameter grid by passing the set of $K$ values that you would like to tune.
4. Use `GridSearchCV` to estimate the classifier accuracy for a range of $K$ values. Pass the pipeline and parameter grid defined in steps 2. and 3. as the `param_grid` argument and the `estimator` argument, respectively.
5. Execute the grid search by passing the training data to the `fit` method on the `GridSearchCV` instance created in step 4.
6. Pick a value of $K$ that yields a high cross-validation accuracy estimate that doesn't change much if you change $K$ to a nearby value.
7. Create a new model object for the best parameter value (i.e., $K$), and retrain the classifier by calling the `fit` method.
8. Evaluate the estimated accuracy of the classifier on the test set using the `score` method.

In these last two chapters, we focused on the K-nearest neighbors algorithm,
but there are many other methods we could have used to predict a categorical label.
All algorithms have their strengths and weaknesses, and we summarize these for
the K-NN here.

**Strengths:** K-nearest neighbors classification

1. is a simple, intuitive algorithm,
2. requires few assumptions about what the data must look like, and
3. works for binary (two-class) and multi-class (more than 2 classes) classification problems.

**Weaknesses:** K-nearest neighbors classification

1. becomes very slow as the training data gets larger,
2. may not perform well with a large number of predictors, and
3. may not perform well when classes are imbalanced.

+++

