
(intro)=
# Python and Pandas

```{code-cell} ipython3
:tags: [remove-cell]

from chapter_preamble import *
```

## Overview

This chapter provides an introduction to data science and the Python programming language.
The goal here is to get your hands dirty right from the start! We will walk through an entire data analysis,
and along the way introduce different types of data analysis question, some fundamental programming
concepts in Python, and the basics of loading, cleaning, and visualizing data. In the following chapters, we will
dig into each of these steps in much more detail; but for now, let's jump in to see how much we can do
with data science!

## Chapter learning objectives

By the end of the chapter, readers will be able to do the following:

- Identify the different types of data analysis question and categorize a question into the correct type.
- Load the `pandas` package into Python.
- Read tabular data with `read_csv`.
- Create new variables and objects in Python using the assignment symbol.
- Create and organize subsets of tabular data using `[]`, `loc[]`, `sort_values`, and `head`.
- Add and modify columns in tabular data using column assignment.
- Chain multiple operations in sequence.
- Visualize data with an `altair` bar plot.
- Use `help()` and `?` to access help and documentation tools in Python.



## Canadian languages data set

```{index} Canadian languages
```

In this chapter, we will walk through a full analysis of a data set relating to
languages spoken at home by Canadian residents ({numref}`canadamap`). Many Indigenous peoples exist in Canada
with their own cultures and languages; these languages are often unique to Canada and not spoken
anywhere else in the world {cite:p}`statcan2018mothertongue`. Sadly, colonization has
led to the loss of many of these languages. For instance, generations of
children were not allowed to speak their mother tongue (the first language an
individual learns in childhood) in Canadian residential schools. Colonizers
also renamed places they had "discovered" {cite:p}`wilson2018`.  Acts such as these
have significantly harmed the continuity of Indigenous languages in Canada, and
some languages are considered "endangered" as few people report speaking them.
To learn more, please see *Canadian Geographic*'s article, "Mapping Indigenous Languages in
Canada" {cite:p}`walker2017`,
*They Came for the Children: Canada, Aboriginal
peoples, and Residential Schools* {cite:p}`children2012`
and the *Truth and Reconciliation Commission of Canada's*
*Calls to Action* {cite:p}`calls2015`.

```{figure} img/intro/canada_map.png
---
name: canadamap
---
Map of Canada
```

The data set we will study in this chapter is taken from
[the `canlang` R data package](https://ttimbers.github.io/canlang/)
{cite:p}`timbers2020canlang`, which has
population language data collected during the 2016 Canadian census {cite:p}`cancensus2016`.
In this data, there are 214 languages recorded, each having six different properties:

1. `category`: Higher-level language category, describing whether the language is an Official Canadian language, an Aboriginal (i.e., Indigenous) language, or a Non-Official and Non-Aboriginal language.
2. `language`: The name of the language.
3. `mother_tongue`: Number of Canadian residents who reported the language as their mother tongue. Mother tongue is generally defined as the language someone was exposed to since birth.
4. `most_at_home`: Number of Canadian residents who reported the language as being spoken most often at home.
5. `most_at_work`: Number of Canadian residents who reported the language as being used most often at work.
6. `lang_known`: Number of Canadian residents who reported knowledge of the language.

According to the census, more than 60 Aboriginal languages were reported
as being spoken in Canada. Suppose we want to know which are the most common;
then we might ask the following question, which we wish to answer using our data:

*Which ten Aboriginal languages were most often reported in 2016 as mother
tongues in Canada, and how many people speak each of them?*

```{index} data science; good practices
```

```{note}
Data science cannot be done without
a deep understanding of the data and
problem domain. In this book, we have simplified the data sets used in our
examples to concentrate on methods and fundamental concepts. But in real
life, you cannot and should not do data science without a domain expert.
Alternatively, it is common to practice data science in your own domain of
expertise! Remember that when you work with data, it is essential to think
about *how* the data were collected, which affects the conclusions you can
draw. If your data are biased, then your results will be biased!
```

## Asking a question

Every good data analysis begins with a *question*&mdash;like the
above&mdash;that you aim to answer using data. As it turns out, there
are actually a number of different *types* of question regarding data:
descriptive, exploratory, predictive, inferential, causal, and mechanistic,
all of which are defined in {numref}`questions-table`. {cite:p}`leek2015question,peng2015art`
Carefully formulating a question as early as possible in your analysis&mdash;and
correctly identifying which type of question it is&mdash;will guide your overall approach to
the analysis as well as the selection of appropriate tools.

```{index} question; data analysis, descriptive question; definition, exploratory question; definition
```

```{index} predictive question; definition, inferential question; definition, causal question; definition, mechanistic question; definition
```

```{list-table} Types of data analysis question.
:header-rows: 1
:name: questions-table

* - Question type
  - Description
  - Example
* - Descriptive
  - A question that asks about summarized characteristics of a data set without interpretation (i.e., report a fact).
  - How many people live in each province and territory in Canada?
* - Exploratory
  - A question that asks if there are patterns, trends, or relationships within a single data set. Often used to propose hypotheses for future study.
  - Does political party voting change with indicators of wealth in a set of data collected on 2,000 people living in Canada?
* - Predictive
  - A question that asks about predicting measurements or labels for individuals (people or things). The focus is on what things predict some outcome, but not what causes the outcome.
  - What political party will someone vote for in the next Canadian election?
* - Inferential
  - A question that looks for patterns, trends, or relationships in a single data set **and** also asks for quantification of how applicable these findings are to the wider population.
  - Does political party voting change with indicators of wealth for all people living in Canada?
* - Causal
  - A question that asks about whether changing one factor will lead to a change in another factor, on average, in the wider population.
  - Does wealth lead to voting for a certain political party in Canadian elections?
* - Mechanistic
  - A question that asks about the underlying mechanism of the observed patterns, trends, or relationships (i.e., how does it happen?)
  - How does wealth lead to voting for a certain political party in Canadian elections?

```


In this book, you will learn techniques to answer the
first four types of question: descriptive, exploratory, predictive, and inferential;
causal and mechanistic questions are beyond the scope of this book.
In particular, you will learn how to apply the following analysis tools:

```{index} summarization; overview, visualization; overview, classification; overview, regression; overview
```

```{index} clustering; overview, estimation; overview
```

1. **Summarization:** computing and reporting aggregated values pertaining to a data set.
Summarization is most often used to answer descriptive questions,
and can occasionally help with answering exploratory questions.
For example, you might use summarization to answer the following question:
*What is the average race time for runners in this data set?*
Tools for summarization are covered in detail in {numref}`Chapters %s <reading>`
and {numref}`%s <wrangling>`, but appear regularly throughout the text.
1. **Visualization:** plotting data graphically.
Visualization is typically used to answer descriptive and exploratory questions,
but plays a critical supporting role in answering all of the types of question in {numref}`questions-table`.
For example, you might use visualization to answer the following question:
*Is there any relationship between race time and age for runners in this data set?*
This is covered in detail in {numref}`Chapter %s <viz>`, but again appears regularly throughout the book.
3. **Classification:** predicting a class or category for a new observation.
Classification is used to answer predictive questions.
For example, you might use classification to answer the following question:
*Given measurements of a tumor's average cell area and perimeter, is the tumor benign or malignant?*
Classification is covered in {numref}`Chapters %s <classification1>` and {numref}`%s <classification2>`.
4. **Regression:** predicting a quantitative value for a new observation.
Regression is also used to answer predictive questions.
For example, you might use regression to answer the following question:
*What will be the race time for a 20-year-old runner who weighs 50kg?*
Regression is covered in {numref}`Chapters %s <regression1>` and {numref}`%s <regression2>`.
5. **Clustering:** finding previously unknown/unlabeled subgroups in a
data set. Clustering is often used to answer exploratory questions.
For example, you might use clustering to answer the following question:
*What products are commonly bought together on Amazon?*
Clustering is covered in {numref}`Chapter %s <clustering>`.
6. **Estimation:** taking measurements for a small number of items from a large group
 and making a good guess for the average or proportion for the large group. Estimation
is used to answer inferential questions.
For example, you might use estimation to answer the following question:
*Given a survey of cellphone ownership of 100 Canadians, what proportion
of the entire Canadian population own Android phones?*
Estimation is covered in {numref}`Chapter %s <inference>`.

Referring to {numref}`questions-table`, our question about
Aboriginal languages is an example of a *descriptive question*: we are
summarizing the characteristics of a data set without further interpretation.
And referring to the list above, it looks like we should use visualization
and perhaps some summarization to answer the question. So in the remainder
of this chapter, we will work towards making a visualization that shows
us the ten most common Aboriginal languages in Canada and their associated counts,
according to the 2016 census.

## Loading a tabular data set

```{index} tabular data
```

A data set is, at its core essence, a structured collection of numbers and characters.
Aside from that, there are really no strict rules; data sets can come in
many different forms! Perhaps the most common form of data set that you will
find in the wild, however, is *tabular data*. Think spreadsheets in Microsoft Excel: tabular data are
rectangular-shaped and spreadsheet-like, as shown in {numref}`img-spreadsheet-vs-data frame`. In this book, we will focus primarily on tabular data.

```{index} data frame; overview, observation, variable
```

Since we are using Python for data analysis in this book, the first step for us is to
load the data into Python. When we load tabular data into
Python, it is represented as a *data frame* object. {numref}`img-spreadsheet-vs-data frame` shows that a Python data frame is very similar
to a spreadsheet. We refer to the rows as **observations**; these are the individual objects
for which we collect data. In {numref}`img-spreadsheet-vs-data frame`, the observations are
languages. We refer to the columns as **variables**; these are the characteristics of each
observation. In {numref}`img-spreadsheet-vs-data frame`, the variables are the the language's category, its name, the number of mother tongue speakers, etc.

```{figure} img/intro/spreadsheet_vs_df.png
---
height: 500px
name: img-spreadsheet-vs-data frame
---
A spreadsheet versus a data frame in Python
```

```{index} see: comma-separated values; csv
```

```{index} csv
```

The first kind of data file that we will learn how to load into Python as a data
frame is the *comma-separated values* format (`.csv` for short).  These files
have names ending in `.csv`, and can be opened and saved using common
spreadsheet programs like Microsoft Excel and Google Sheets.  For example, the
`.csv` file named `can_lang.csv`
is included with [the code for this book](https://github.com/UBC-DSCI/introduction-to-datascience-python/tree/main/source/data).
If we were to open this data in a plain text editor (a program like Notepad that just shows
text with no formatting), we would see each row on its own line, and each entry in the table separated by a comma:

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

```{index} function, argument, read function; read_csv
```

To load this data into Python so that we can do things with it (e.g., perform
analyses or create data visualizations), we will need to use a *function.* A
function is a special word in Python that takes instructions (we call these
*arguments*) and does something. The function we will use to load a `.csv` file
into Python is called `read_csv`. In its most basic
use-case, `read_csv` expects that the data file:

- has column names (or *headers*),
- uses a comma (`,`) to separate the columns, and
- does not have row names.

+++

```{index} package, import, pandas
```

Below you'll see the code used to load the data into Python using the `read_csv`
function. Note that the `read_csv` function is not included in the base
installation of Python, meaning that it is not one of the primary functions ready to
use when you install Python. Therefore, you need to load it from somewhere else
before you can use it. The place from which we will load it is called a Python *package*.
A Python package is a collection of functions that can be used in addition to the
built-in Python package functions once loaded. The `read_csv` function, in
particular, can be made accessible by loading
[the `pandas` Python package](https://pypi.org/project/pandas/) {cite:p}`reback2020pandas,mckinney-proc-scipy-2010`
using the `import` command. The `pandas` package contains many
functions that we will use throughout this book to load, clean, wrangle,
and visualize data.

+++

```{code-cell} ipython3
import pandas as pd
```

This command has two parts. The first is `import pandas`, which loads the `pandas` package.
The second is `as pd`, which give the `pandas` package the much shorter *alias* (another name) `pd`.
We can now use the `read_csv` function by writing `pd.read_csv`, i.e., the package name, then a dot, then the function name.
You can see why we gave `pandas` a shorter alias; if we had to type `pandas.` before every function we wanted to use,
our code would become much longer and harder to read!

Now that the `pandas` package is loaded, we can use the `read_csv` function by passing
it a single argument: the name of the file, `"can_lang.csv"`. We have to
put quotes around file names and other letters and words that we use in our
code to distinguish it from the special words (like functions!) that make up the Python programming
language.  The file's name is the only argument we need to provide because our
file satisfies everything else that the `read_csv` function expects in the default
use-case. {numref}`img-read-csv` describes how we use the `read_csv`
to read data into Python.

```{figure} img/intro/read_csv_function.png
---
name: img-read-csv
---
Syntax for the `read_csv` function
```


+++
```{code-cell} ipython3
:tags: ["output_scroll"]
pd.read_csv("data/can_lang.csv")

```



## Naming things in Python

When we loaded the 2016 Canadian census language data
using `read_csv`, we did not give this data frame a name.
Therefore the data was just printed on the screen,
and we cannot do anything else with it. That isn't very useful.
What would be more useful would be to give a name
to the data frame that `read_csv` outputs,
so that we can refer to it later for analysis and visualization.

```{index} see: =; assignment symbol
```

```{index} assignment symbol, string
```

The way to assign a name to a value in Python is via the *assignment symbol* `=`.
On the left side of the assignment symbol you put the name that you want
to use, and on the right side of the assignment symbol
you put the value that you want the name to refer to.
Names can be used to refer to almost anything in Python, such as numbers,
words (also known as *strings* of characters), and data frames!
Below, we set `my_number` to `3` (the result of `1+2`)
and we set `name` to the string `"Alice"`.

```{code-cell} ipython3
my_number = 1 + 2
name = "Alice"
```

Note that when
we name something in Python using the assignment symbol, `=`,
we do not need to surround the name we are creating  with quotes. This is
because we are formally telling Python that this special word denotes
the value of whatever is on the right-hand side.
Only characters and words that act as *values* on the right-hand side of the assignment
symbol&mdash;e.g., the file name `"data/can_lang.csv"` that we specified before, or `"Alice"` above&mdash;need
to be surrounded by quotes.

After making the assignment, we can use the special name words we have created in
place of their values. For example, if we want to do something with the value `3` later on,
we can just use `my_number` instead. Let's try adding 2 to `my_number`; you will see that
Python just interprets this as adding 2 and 3:

```{code-cell} ipython3
my_number + 2
```

```{index} object
```

Object names can consist of letters, numbers, and underscores (`_`).
Other symbols won't work since they have their own meanings in Python. For example,
`-` is the subtraction symbol; if we try to assign a name with
the `-` symbol, Python will complain and we will get an error!

```{code-cell} ipython3
:tags: ["remove-output"]
my-number = 1
```
```{code-cell} ipython3
:tags: ["remove-input"]
print("SyntaxError: cannot assign to expression here. Maybe you meant '==' instead of '='?")
```

```{index} object; naming convention
```

There are certain conventions for naming objects in Python.
When naming an object we
suggest using only lowercase letters, numbers and underscores `_` to separate
the words in a name.  Python is case sensitive, which means that `Letter` and
`letter` would be two different objects in Python.  You should also try to give your
objects meaningful names.  For instance, you *can* name a data frame `x`.
However, using more meaningful terms, such as `language_data`, will help you
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

