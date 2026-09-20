So even with an accuracy of 89%, the precision and recall of the classifier
were both relatively low. For this data analysis context, recall is
particularly important: if someone has a malignant tumor, we certainly want to
identify it.  A recall of just 25% would likely be unacceptable!

```{note}
It is difficult to achieve both high precision and high recall at
the same time; models with high precision tend to have low recall and vice
versa.  As an example, we can easily make a classifier that has *perfect
recall*: just *always* guess positive! This classifier will of course find
every positive observation in the test set, but it will make lots of false
positive predictions along the way  and have low precision. Similarly, we can
easily make a classifier that has *perfect precision*: *never* guess
positive! This classifier will never incorrectly identify an obsevation as
positive, but it will make a lot of false negative predictions along the way.
In fact, this classifier will have 0% recall! Of course, most real
classifiers fall somewhere in between these two extremes. But these examples
serve to show that in settings where one of the classes is of interest (i.e.,
there is a *positive* label), there is a trade-off between precision and recall that one has to
make when designing a classifier.
```

+++

(randomseeds)=
