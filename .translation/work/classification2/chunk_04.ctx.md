
Setting the number of
neighbors to $K =$ {glue:text}`best_k_unique`
provides the highest cross-validation accuracy estimate ({glue:text}`best_acc`%). But there is no exact or perfect answer here;
any selection from $K = 30$ to $80$ or so would be reasonably justified, as all
of these differ in classifier accuracy by a small amount. Remember: the
values you see on this plot are *estimates* of the true accuracy of our
classifier. Although the
$K =$ {glue:text}`best_k_unique` value is
higher than the others on this plot,
that doesn't mean the classifier is actually more accurate with this parameter
value! Generally, when selecting $K$ (and other parameters for other predictive
models), we are looking for a value where:

- we get roughly optimal accuracy, so that our model will likely be accurate;
- changing the value to a nearby one (e.g., adding or subtracting a small number) doesn't decrease accuracy too much, so that our choice is reliable in the presence of uncertainty;
- the cost of training the model is not prohibitive (e.g., in our situation, if $K$ is too large, predicting becomes expensive!).

We know that $K =$ {glue:text}`best_k_unique`
provides the highest estimated accuracy. Further, {numref}`fig:06-find-k` shows that the estimated accuracy
changes by only a small amount if we increase or decrease $K$ near $K =$ {glue:text}`best_k_unique`.
And finally, $K =$ {glue:text}`best_k_unique` does not create a prohibitively expensive
computational cost of training. Considering these three points, we would indeed select
$K =$ {glue:text}`best_k_unique` for the classifier.

