
We can also use `read_csv` to read in data directly from a **U**niform **R**esource **L**ocator (URL) that
contains tabular data. Here, we provide the URL of a remote file
to `read_csv`, instead of a path to a local file on our
computer. We need to surround the URL with quotes similar to when we specify a
path on our local computer. All other arguments that we use are the same as
when using these functions with a local file on our computer.

```{code-cell} ipython3
:tags: ["output_scroll"]
url = "https://raw.githubusercontent.com/UBC-DSCI/introduction-to-datascience-python/reading/source/data/can_lang.csv"
pd.read_csv(url)
canlang_data = pd.read_csv(url)

canlang_data
```

### Previewing a data file before reading it into Python

In many of the examples above, we gave you previews of the data file before we read
it into Python. Previewing data is essential to see whether or not there are column
names, what the separators are, and if there are rows you need to skip. You
should do this yourself when trying to read in data files: open the file in whichever
text editor you prefer to inspect its contents prior to reading it into Python.

