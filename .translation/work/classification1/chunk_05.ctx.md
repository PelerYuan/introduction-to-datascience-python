    (SimpleImputer(), ["Radius", "Texture", "Perimeter"]),
    verbose_feature_names_out=False
)
preprocessor
```

To visualize what mean imputation does, let's just apply the transformer directly to the `missing_cancer`
data frame using the `fit` and `transform` functions.  The imputation step fills in the missing
entries with the mean values of their corresponding variables.

```{code-cell} ipython3
preprocessor.fit(missing_cancer)
imputed_cancer = preprocessor.transform(missing_cancer)
imputed_cancer
```

Many other options for missing data imputation can be found in
[the `scikit-learn` documentation](https://scikit-learn.org/stable/modules/impute.html).  However
you decide to handle missing data in your data analysis, it is always crucial
to think critically about the setting, how the data were collected, and the
question you are answering.

+++

(08:puttingittogetherworkflow)=
