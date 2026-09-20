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

