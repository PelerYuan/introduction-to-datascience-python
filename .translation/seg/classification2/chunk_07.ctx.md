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

