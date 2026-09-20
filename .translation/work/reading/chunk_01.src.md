
(reading)=
# Reading in data locally and from the web


## Overview

```{index} see: loading; reading
```

```{index} reading; definition
```

In this chapter, you’ll learn to read tabular data of various formats into Python
from your local device (e.g., your laptop) and the web. “Reading” (or “loading”)
is the process of
converting data (stored as plain text, a database, HTML, etc.) into an object
(e.g., a data frame) that Python can easily access and manipulate. Thus reading data
is the gateway to any data analysis; you won’t be able to analyze data unless
you’ve loaded it first. And because there are many ways to store data, there
are similarly many ways to read data into Python. The more time you spend upfront
matching the data reading method to the type of data you have, the less time
you will have to devote to re-formatting, cleaning and wrangling your data (the
second step to all data analyses). It’s like making sure your shoelaces are
tied well before going for a run so that you don’t trip later on!

## Chapter learning objectives
By the end of the chapter, readers will be able to do the following:

- Define the types of path and use them to locate files:
    - absolute file path
    - relative file path
    - Uniform Resource Locator (URL)
- Read data into Python from various types of path using:
    - `read_csv`
    - `read_excel`
- Compare and contrast `read_csv` and `read_excel`.
- Describe when to use the following `read_csv` function arguments:
    - `skiprows`
    - `sep`
    - `header`
    - `names`
- Choose the appropriate `read_csv` function arguments to load a given plain text tabular data set into Python.
- Use the `rename` function to rename columns in a data frame.
- Use `pandas` package's `read_excel` function and arguments to load a sheet from an excel file into Python.
- Work with databases using functions from the `ibis` package:
    - Connect to a database with `connect`.
    - List tables in the database with `list_tables`.
    - Create a reference to a database table with `table`.
    - Bring data from a database into Python with `execute`.
- Use `to_csv` to save a data frame to a `.csv` file.
- (*Optional*) Obtain data from the web using scraping and application programming interfaces (APIs):
    - Read HTML source code from a URL using the `BeautifulSoup` package.
    - Read data from the NASA "Astronomy Picture of the Day" using the `requests` package.
    - Compare downloading tabular data from a plain text file (e.g., `.csv`), accessing data from an API, and scraping the HTML source code from a website.

## Absolute and relative file paths

```{index} see: location; path
```

```{index} path; local, path; remote, path; relative, path; absolute
```

This chapter will discuss the different functions we can use to import data
into Python, but before we can talk about *how* we read the data into Python with these
functions, we first need to talk about *where* the data lives. When you load a
data set into Python, you first need to tell Python where those files live. The file
could live on your computer (*local*) or somewhere on the internet (*remote*).

The place where the file lives on your computer is referred to as its "path". You can
think of the path as directions to the file. There are two kinds of paths:
*relative* paths and *absolute* paths. A relative path indicates where the file is
with respect to your *working directory* (i.e., "where you are currently") on the computer.
On the other hand, an absolute path indicates where the file is
with respect to the computer's filesystem base (or *root*) folder, regardless of where you are working.

Suppose our computer's filesystem looks like the picture in
{numref}`Filesystem`. We are working in a
file titled `project3.ipynb`, and our current working directory is `project3`;
typically, as is the case here, the working directory is the directory containing the file you are currently
working on.

```{figure} img/reading/filesystem.png
---
name: Filesystem
---
Example file system
```

Let's say we wanted to open the `happiness_report.csv` file. We have two options to indicate
where the file is: using a relative path, or using an absolute path.
The absolute path of the file always starts with a slash `/`&mdash;representing the root folder on the computer&mdash;and
proceeds by listing out the sequence of folders you would have to enter to reach the file, each separated by another slash `/`.
So in this case, `happiness_report.csv` would be reached by starting at the root, and entering the `home` folder,
then the `dsci-100` folder, then the `project3` folder, and then finally the `data` folder. So its absolute
path would be `/home/dsci-100/project3/data/happiness_report.csv`. We can load the file using its absolute path
as a string passed to the `read_csv` function from `pandas`.
```{code-cell} ipython3
:tags: ["remove-output"]
happy_data = pd.read_csv("/home/dsci-100/project3/data/happiness_report.csv")
```
If we instead wanted to use a relative path, we would need to list out the sequence of steps needed to get from our current
working directory to the file, with slashes `/` separating each step. Since we are currently in the `project3` folder,
we just need to enter the `data` folder to reach our desired file. Hence the relative path is `data/happiness_report.csv`,
and we can load the file using its relative path as a string passed to `read_csv`.
```{code-cell} ipython3
:tags: ["remove-output"]
happy_data = pd.read_csv("data/happiness_report.csv")
```
Note that there is no forward slash at the beginning of a relative path; if we accidentally typed `"/data/happiness_report.csv"`,
Python would look for a folder named `data` in the root folder of the computer&mdash;but that doesn't exist!

```{index} path; previous, path; current
```

```{index} see: ..; path
```

```{index} see: .; path
```

Aside from specifying places to go in a path using folder names (like `data` and `project3`), we can also specify two additional
special places: the *current directory* and the *previous directory*. We indicate the current working directory with a single dot `.`, and
the previous directory with two dots `..`. So for instance, if we wanted to reach the `bike_share.csv` file from the `project3` folder, we could
use the relative path `../project2/bike_share.csv`. We can even combine these two; for example, we could reach the `bike_share.csv` file using
the (very silly) path `../project2/../project2/./bike_share.csv` with quite a few redundant directions: it says to go back a folder, then open `project2`,
then go back a folder again, then open `project2` again, then stay in the current directory, then finally get to `bike_share.csv`. Whew, what a long trip!

So which kind of path should you use: relative, or absolute? Generally speaking, you should use relative paths.
Using a relative path helps ensure that your code can be run
on a different computer (and as an added bonus, relative paths are often shorter&mdash;easier to type!).
This is because a file's relative path is often the same across different computers, while a
file's absolute path (the names of
all of the folders between the computer's root, represented by `/`, and the file) isn't usually the same
across different computers. For example, suppose Fatima and Jayden are working on a
project together on the `happiness_report.csv` data. Fatima's file is stored at

```text
/home/Fatima/project3/data/happiness_report.csv
```

while Jayden's is stored at

```text
/home/Jayden/project3/data/happiness_report.csv
```

Even though Fatima and Jayden stored their files in the same place on their
computers (in their home folders), the absolute paths are different due to
their different usernames.  If Jayden has code that loads the
`happiness_report.csv` data using an absolute path, the code won't work on
Fatima's computer.  But the relative path from inside the `project3` folder
(`data/happiness_report.csv`) is the same on both computers; any code that uses
relative paths will work on both! In the additional resources section,
we include a link to a short video on the
difference between absolute and relative paths.

```{index} URL
```

Beyond files stored on your computer (i.e., locally), we also need a way to locate resources
stored elsewhere on the internet (i.e., remotely). For this purpose we use a
*Uniform Resource Locator (URL)*, i.e., a web address that looks something
like https://python.datasciencebook.ca/. URLs indicate the location of a resource on the internet, and
start with a web domain, followed by a forward slash `/`, and then a path
to where the resource is located on the remote machine.

## Reading tabular data from a plain text file into Python

(readcsv)=
### `read_csv` to read in comma-separated values files

```{index} csv, reading; separator, read function; read_csv
```

Now that we have learned about *where* data could be, we will learn about *how*
to import data into Python using various functions. Specifically, we will learn how
to *read* tabular data from a plain text file (a document containing only text)
*into* Python and *write* tabular data to a file *out of* Python. The function we use to do this
depends on the file's format. For example, in the last chapter, we learned about using
the `read_csv` function from `pandas` when reading `.csv` (**c**omma-**s**eparated **v**alues)
files. In that case, the *separator* that divided our columns was a
comma (`,`). We only learned the case where the data matched the expected defaults
of the `read_csv` function
(column names are present, and commas are used as the separator between columns).
In this section, we will learn how to read
files that do not satisfy the default expectations of `read_csv`.

```{index} Canadian languages; canlang data
```

Before we jump into the cases where the data aren't in the expected default format
for `pandas` and `read_csv`, let's revisit the more straightforward
case where the defaults hold, and the only argument we need to give to the function
is the path to the file, `data/can_lang.csv`. The `can_lang` data set contains
language data from the 2016 Canadian census.
We put `data/` before the file's
name when we are loading the data set because this data set is located in a
sub-folder, named `data`, relative to where we are running our Python code.
Here is what the text in the file `data/can_lang.csv` looks like.

```text
category,language,mother_tongue,most_at_home,most_at_work,lang_known
Aboriginal languages,"Aboriginal languages, n.o.s.",590,235,30,665
Non-Official & Non-Aboriginal languages,Afrikaans,10260,4785,85,23415
Non-Official & Non-Aboriginal languages,"Afro-Asiatic languages, n.i.e.",1150,44
Non-Official & Non-Aboriginal languages,Akan (Twi),13460,5985,25,22150
Non-Official & Non-Aboriginal languages,Albanian,26895,13135,345,31930
Aboriginal languages,"Algonquian languages, n.i.e.",45,10,0,120
Aboriginal languages,Algonquin,1260,370,40,2480
Non-Official & Non-Aboriginal languages,American Sign Language,2685,3020,1145,21
Non-Official & Non-Aboriginal languages,Amharic,22465,12785,200,33670
```

```{index} pandas
```

And here is a review of how we can use `read_csv` to load it into Python. First we
load the `pandas` package to gain access to useful
functions for reading the data.

```{code-cell} ipython3
import pandas as pd
```

Next we use `read_csv` to load the data into Python, and in that call we specify the
relative path to the file.

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv("data/can_lang.csv")
canlang_data
```

### Skipping rows when reading in data

Oftentimes, information about how data was collected, or other relevant
information, is included at the top of the data file. This information is
usually written in sentence and paragraph form, with no separator because it is
not organized into columns. An example of this is shown below. This information
gives the data scientist useful context and information about the data,
however, it is not well formatted or intended to be read into a data frame cell
along with the tabular data that follows later in the file.

```text
Data source: https://ttimbers.github.io/canlang/
Data originally published in: Statistics Canada Census of Population 2016.
Reproduced and distributed on an as-is basis with their permission.
category,language,mother_tongue,most_at_home,most_at_work,lang_known
Aboriginal languages,"Aboriginal languages, n.o.s.",590,235,30,665
Non-Official & Non-Aboriginal languages,Afrikaans,10260,4785,85,23415
Non-Official & Non-Aboriginal languages,"Afro-Asiatic languages, n.i.e.",1150,445,10,2775
Non-Official & Non-Aboriginal languages,Akan (Twi),13460,5985,25,22150
Non-Official & Non-Aboriginal languages,Albanian,26895,13135,345,31930
Aboriginal languages,"Algonquian languages, n.i.e.",45,10,0,120
Aboriginal languages,Algonquin,1260,370,40,2480
Non-Official & Non-Aboriginal languages,American Sign Language,2685,3020,1145,21930
Non-Official & Non-Aboriginal languages,Amharic,22465,12785,200,33670
```

With this extra information being present at the top of the file, using
`read_csv` as we did previously does not allow us to correctly load the data
into Python. In the case of this file, Python just prints a `ParserError`
message, indicating that it wasn't able to read the file.

```{code-cell} ipython3
:tags: ["remove-output"]
canlang_data = pd.read_csv("data/can_lang_meta-data.csv")
```
```{code-cell} ipython3
:tags: ["remove-input"]
print("ParserError: Error tokenizing data. C error: Expected 1 fields in line 4, saw 6")
```

```{index} ParserError
```

```{index} read function; skiprows argument
```

To successfully read data like this into Python, the `skiprows`
argument can be useful to tell Python
how many rows to skip before
it should start reading in the data. In the example above, we would set this
value to 3 to read and load the data correctly.

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv("data/can_lang_meta-data.csv", skiprows=3)
canlang_data
```

How did we know to skip three rows? We looked at the data! The first three rows
of the data had information we didn't need to import:

```text
Data source: https://ttimbers.github.io/canlang/
Data originally published in: Statistics Canada Census of Population 2016.
Reproduced and distributed on an as-is basis with their permission.
```

The column names began at row 4, so we skipped the first three rows.

### Using the `sep` argument for different separators

Another common way data is stored is with tabs as the separator. Notice the
data file, `can_lang.tsv`, has tabs in between the columns instead of
commas.

```text
category	language	mother_tongue	most_at_home	most_at_work	lang_known
Aboriginal languages	Aboriginal languages, n.o.s.	590	235	30	665
Non-Official & Non-Aboriginal languages	Afrikaans	10260	4785	85	23415
Non-Official & Non-Aboriginal languages	Afro-Asiatic languages, n.i.e.	1150	445	10	2775
Non-Official & Non-Aboriginal languages	Akan (Twi)	13460	5985	25	22150
Non-Official & Non-Aboriginal languages	Albanian	26895	13135	345	31930
Aboriginal languages	Algonquian languages, n.i.e.	45	10	0	120
Aboriginal languages	Algonquin	1260	370	40	2480
Non-Official & Non-Aboriginal languages	American Sign Language	2685	3020	1145	21930
Non-Official & Non-Aboriginal languages	Amharic	22465	12785	200	33670
```
```{index} read function; sep argument
```

```{index} see: tab-separated values; tsv
```

```{index} tsv
```

To read in `.tsv` (**t**ab **s**eparated **v**alues) files, we can set the `sep` argument
in the `read_csv` function to the *tab character* `\t`.

```{index} escape character
```

```{note}
`\t` is an example of an *escaped character*,
which always starts with a backslash (`\`).
Escaped characters are used to represent non-printing characters
(like the tab) or characters with special meanings (such as quotation marks).
```


```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv("data/can_lang.tsv", sep="\t")
canlang_data
```

If you compare the data frame here to the data frame we obtained in
{numref}`readcsv` using `read_csv`, you'll notice that they look identical: they have
the same number of columns and rows, the same column names, and the same entries!
So even though we needed to use different
arguments depending on the file format, our resulting data frame
(`canlang_data`) in both cases was the same.

### Using the `header` argument to handle missing column names

```{index} read function; header argument, reading; separator
```

The `can_lang_no_names.tsv` file contains a slightly different version
of this data set, except with no column names, and tabs for separators.
Here is how the file looks in a text editor:

```text
Aboriginal languages	Aboriginal languages, n.o.s.	590	235	30	665
Non-Official & Non-Aboriginal languages	Afrikaans	10260	4785	85	23415
Non-Official & Non-Aboriginal languages	Afro-Asiatic languages, n.i.e.	1150	445	10	2775
Non-Official & Non-Aboriginal languages	Akan (Twi)	13460	5985	25	22150
Non-Official & Non-Aboriginal languages	Albanian	26895	13135	345	31930
Aboriginal languages	Algonquian languages, n.i.e.	45	10	0	120
Aboriginal languages	Algonquin	1260	370	40	2480
Non-Official & Non-Aboriginal languages	American Sign Language	2685	3020	1145	21930
Non-Official & Non-Aboriginal languages	Amharic	22465	12785	200	33670

```

Data frames in Python need to have column names.  Thus if you read in data
without column names, Python will assign names automatically. In this example,
Python assigns the column names `0, 1, 2, 3, 4, 5`.
To read this data into Python, we specify the first
argument as the path to the file (as done with `read_csv`), and then provide
values to the `sep` argument (here a tab, which we represent by `"\t"`),
and finally set `header = None` to tell `pandas` that the data file does not
contain its own column names.

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv(
    "data/can_lang_no_names.tsv",
    sep="\t",
    header=None
)
canlang_data
```

```{index} DataFrame; rename, pandas
```

It is best to rename your columns manually in this scenario. The current column names
(`0, 1`, etc.) are problematic for two reasons: first, because they not very descriptive names, which will make your analysis
confusing; and second, because your column names should generally be *strings*, but are currently *integers*.
To rename your columns, you can use the `rename` function
from the [pandas package](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html#).
The argument of the `rename` function is `columns`, which takes a mapping between the old column names and the new column names.
In this case, we want to rename the old columns (`0, 1, ..., 5`) in the `canlang_data` data frame to more descriptive names.

To specify the mapping, we create a *dictionary*: a Python object that represents
a mapping from *keys* to *values*. We can create a dictionary by using a pair of curly
braces `{ }`, and inside the braces placing pairs of `key : value` separated by commas.
Below, we create a dictionary called `col_map` that maps the old column names in `canlang_data` to new column
names, and then pass it to the `rename` function.

```{code-cell} ipython3
:tags: ["output_scroll"]
col_map = {
    0 : "category",
    1 : "language",
    2 : "mother_tongue",
    3 : "most_at_home",
    4 : "most_at_work",
    5 : "lang_known"
}
canlang_data_renamed = canlang_data.rename(columns=col_map)
canlang_data_renamed
```

```{index} read function; names argument
```

The column names can also be assigned to the data frame immediately upon reading it from the file by passing a
list of column names to the `names` argument in `read_csv`.

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_csv(
    "data/can_lang_no_names.tsv",
    sep="\t",
    header=None,
    names=[
        "category",
        "language",
        "mother_tongue",
        "most_at_home",
        "most_at_work",
        "lang_known",
    ],
)
canlang_data
```

### Reading tabular data directly from a URL

```{index} URL; reading from
```

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

