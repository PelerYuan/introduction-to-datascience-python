remember what each name in your code represents.  We recommend following the
**PEP 8** naming conventions outlined in the *[PEP 8](https://peps.python.org/pep-0008/)* {cite:p}`pep8-style-guide`.  Let's
now use the assignment symbol to give the name
`can_lang` to the 2016 Canadian census language data frame that we get from
`read_csv`.

```{code-cell} ipython3
can_lang = pd.read_csv("data/can_lang.csv")
```

Wait a minute, nothing happened this time! Where's our data?
Actually, something did happen: the data was loaded in
and now has the name `can_lang` associated with it.
And we can use that name to access the data frame and do things with it.
For example, we can type the name of the data frame to print both the first few rows
and the last few rows. The three dots (`...`) indicate that there are additional rows that are not printed.
You will also see that the number of observations (i.e., rows) and
variables (i.e., columns) are printed just underneath the data frame (214 rows and 6 columns in this case).
Printing a few rows from data frame like this is a handy way to get a quick sense for what is contained in it.

```{code-cell} ipython3
:tags: ["output_scroll"]
can_lang
```

