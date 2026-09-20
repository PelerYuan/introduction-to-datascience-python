
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


