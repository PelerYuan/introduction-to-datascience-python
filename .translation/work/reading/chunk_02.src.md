## Reading tabular data from a Microsoft Excel file

```{index} Excel spreadsheet
```

```{index} see: Microsoft Excel; Excel spreadsheet
```

```{index} see: xlsx; Excel spreadsheet
```

There are many other ways to store tabular data sets beyond plain text files,
and similarly, many ways to load those data sets into Python. For example, it is
very common to encounter, and need to load into Python, data stored as a Microsoft
Excel spreadsheet (with the file name
extension `.xlsx`).  To be able to do this, a key thing to know is that even
though `.csv` and `.xlsx` files look almost identical when loaded into Excel,
the data themselves are stored completely differently.  While `.csv` files are
plain text files, where the characters you see when you open the file in a text
editor are exactly the data they represent, this is not the case for `.xlsx`
files. Take a look at a snippet of what a `.xlsx` file would look like in a text editor:

+++

```text
,?'O
    _rels/.rels???J1??>E?{7?
<?V????w8?'J???'QrJ???Tf?d??d?o?wZ'???@>?4'?|??hlIo??F
t                                                       8f??3wn
????t??u"/
          %~Ed2??<?w??
                       ?Pd(??J-?E???7?'t(?-GZ?????y???c~N?g[^_r?4
                                                                  yG?O
                                                                      ?K??G?


     ]TUEe??O??c[???????6q??s??d?m???\???H?^????3} ?rZY? ?:L60?^?????XTP+?|?
X?a??4VT?,D?Jq
```

```{index} read function; read_excel
```

```{index} Excel spreadsheet; reading
```


This type of file representation allows Excel files to store additional things
that you cannot store in a `.csv` file, such as fonts, text formatting,
graphics, multiple sheets and more. And despite looking odd in a plain text
editor, we can read Excel spreadsheets into Python using the `pandas` package's `read_excel`
function developed specifically for this
purpose.

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_data = pd.read_excel("data/can_lang.xlsx")
canlang_data
```

If the `.xlsx` file has multiple sheets, you have to use the `sheet_name` argument
to specify the sheet number or name. This functionality is useful when a single sheet contains
multiple tables (a sad thing that happens to many Excel spreadsheets since this
makes reading in data more difficult). You can also specify cell ranges using the
`usecols` argument (e.g., `usecols="A:D"` for including columns from `A` to `D`).

As with plain text files, you should always explore the data file before
importing it into Python. Exploring the data beforehand helps you decide which
arguments you need to load the data into Python successfully. If you do not have
the Excel program on your computer, you can use other programs to preview the
file. Examples include Google Sheets and Libre Office.

In {numref}`read_func` we summarize the `read_csv` and `read_excel` functions we covered
in this chapter. We also include the arguments for data separated by
semicolons `;`, which you may run into with data sets where the decimal is
represented by a comma instead of a period (as with some data sets from
European countries).


```{list-table} Summary of read_csv and read_excel
:header-rows: 1
:name: read_func

* - Data File Type
  - Python Function
  - Arguments
* - Comma (`,`) separated files
  - `read_csv`
  - just the file path
* - Tab (`\t`) separated files
  - `read_csv`
  - `sep="\t"`
* - Missing header
  - `read_csv`
  - `header=None`
* - European-style numbers, semicolon (`;`) separators
  - `read_csv`
  - `sep=";"`, `thousands="."`, `decimal=","`
* - Excel files (`.xlsx`)
  - `read_excel`
  - `sheet_name`, `usecols`


```

## Reading data from a database

```{index} database
```

Another very common form of data storage is the relational database. Databases
are great when you have large data sets or multiple users
working on a project. There are many relational database management systems,
such as SQLite, MySQL, PostgreSQL, Oracle, and many more. These
different relational database management systems each have their own advantages
and limitations. Almost all employ SQL (*structured query language*) to obtain
data from the database. But you don't need to know SQL to analyze data from
a database; several packages have been written that allow you to connect to
relational databases and use the Python programming language
to obtain data. In this book, we will give examples of how to do this
using Python with SQLite and PostgreSQL databases.

### Reading data from a SQLite database

```{index} database; SQLite
```

SQLite is probably the simplest relational database system
that one can use in combination with Python. SQLite databases are self-contained, and are
usually stored and accessed locally on one computer from
a file with a `.db` extension (or sometimes a `.sqlite` extension).
Similar to Excel files, these are not plain text files and cannot be read in a plain text editor.

```{index} database; connection, ibis; connect
```

```{index} see: ibis; database
```

```{index} see: database; ibis
```

The first thing you need to do to read data into Python from a database is to
connect to the database. For an SQLite database, we will do that using
the `connect` function from the
`sqlite` backend in the
`ibis` package. This command does not read
in the data, but simply tells Python where the database is and opens up a
communication channel that Python can use to send SQL commands to the database.

```{note}
There is another database package in python called `sqlalchemy`.
That package is a bit more mature than `ibis`,
so if you want to dig deeper into working with databases in Python, that is a good next
package to learn about. We will work with `ibis` in this book, as it
provides a more modern and friendlier syntax that is more like `pandas` for data analysis code.
```

```{code-cell} ipython3
import ibis

conn = ibis.sqlite.connect("data/can_lang.db")
```

```{index} database; table, ibis; list_tables, ibis; sqlite
```

Often relational databases have many tables; thus, in order to retrieve
data from a database, you need to know the name of the table
in which the data is stored. You can get the names of
all the tables in the database using the `list_tables`
function:

```{code-cell} ipython3
tables = conn.list_tables()
tables
```

```{index} table, ibis; table
```

The `list_tables` function returned only one name---`"can_lang"`---which tells us
that there is only one table in this database. To reference a table in the
database (so that we can perform operations like selecting columns and filtering rows), we
use the `table` function from the `conn` object. The object returned
by the `table` function allows us to work with data
stored in databases as if they were just regular `pandas` data frames; but secretly, behind
the scenes, `ibis` will turn your commands into SQL queries!

```{code-cell} ipython3
canlang_table = conn.table("can_lang")
canlang_table
```

```{index} ibis; count
```

```{index} see: count; ibis
```

Although it looks like we might have obtained the whole data frame from the database, we didn't!
It's a *reference*; the data is still stored only in the SQLite database. The `canlang_table` object
is a `DatabaseTable`, which, when printed, tells
you which columns are available in the table. But unlike a usual `pandas` data frame,
we do not immediately know how many rows are in the table. In order to find out how many
rows there are, we have to send an SQL *query* (i.e., command) to the data base.
In `ibis`, we can do that using the `count` function from the table object.

```{code-cell} ipython3
canlang_table.count()
```

```{index} ibis; execute
```

Wait a second...this isn't the number of rows in the database. In fact, we haven't actually sent our
SQL query to the database yet! We need to explicitly tell `ibis` when we want to send the query.
The reason for this is that databases are often more efficient at working with (i.e., selecting, filtering,
joining, etc.) large data sets than Python. And typically, the database will not even
be stored on your computer, but rather a more powerful machine somewhere on the
web. So `ibis` is lazy and waits to bring this data into memory until you explicitly
tell it to using the `execute` function. The `execute` function actually sends the SQL query
to the database, and gives you the result. Let's look at the number of rows in the table by executing
the `count` command.

```{code-cell} ipython3
canlang_table.count().execute()
```
There we go! There are 214 rows in the `can_lang` table. If you are interested in seeing
the *actual* text of the SQL query that `ibis` sends to the database, you can use the `compile` function
instead of `execute`. But note that you have to pass the result of `compile` to the `str` function to turn it into
a human-readable string first.

```{index} see: compile;ibis
```
```{index} ibis; compile, str
```

```{code-cell} ipython3
str(canlang_table.count().compile())
```

The output above shows the SQL code that is sent to the database. When we
write `canlang_table.count().execute()` in Python, in the background, the `execute` function is
translating the Python code into SQL, sending that SQL to the database, and then translating the
response for us. So `ibis` does all the hard work of translating from Python to SQL and back for us;
we can just stick with Python!

The `ibis` package provides lots of `pandas`-like tools for working with database tables.
For example, we can look at the first few rows of the table by using the `head` function,
followed by `execute` to retrieve the response.

```{index} ibis; head
```

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_table.head(10).execute()
```

You can see that `ibis` actually returned a `pandas` data frame to us after we executed the query,
which is very convenient for working with the data after getting it from the database.
So now that we have the `canlang_table` table reference for the 2016 Canadian Census data in hand, we
can mostly continue onward as if it were a regular data frame. For example, let's do the same exercise
from {numref}`Chapter %s <intro>`: we will obtain only those rows corresponding to Aboriginal languages, and keep only
the `language` and `mother_tongue` columns.
We can use the `[]` operation with a logical statement
to obtain only certain rows. Below we filter the data to include only Aboriginal languages.

```{index} database; filter rows, ibis; []
```

```{code-cell} ipython3
canlang_table_filtered = canlang_table[canlang_table["category"] == "Aboriginal languages"]
canlang_table_filtered
```
Above you can see that we have not yet executed this command; `canlang_table_filtered` is just showing
the first part of our query (the part that starts with `Selection[r0]` above).
We didn't call `execute` because we are not ready to bring the data into Python yet.
We can still use the database to do some work to obtain *only* the small amount of data we want to work with locally
in Python. Let's add the second part of our SQL query: selecting only the `language` and `mother_tongue` columns.

```{index} database; select columns
```

```{code-cell} ipython3
canlang_table_selected = canlang_table_filtered[["language", "mother_tongue"]]
canlang_table_selected
```
Now you can see that the `ibis` query will have two steps: it will first find rows corresponding to
Aboriginal languages, then it will extract only the `language` and `mother_tongue` columns that we are interested in.
Let's actually execute the query now to bring the data into Python as a `pandas` data frame, and print the result.
```{code-cell} ipython3
aboriginal_lang_data = canlang_table_selected.execute()
aboriginal_lang_data
```

`ibis` provides many more functions (not just the `[]` operation)
that you can use to manipulate the data within the database before calling
`execute` to obtain the data in Python. But `ibis` does not provide *every* function
that we need for analysis; we do eventually need to call `execute`.
For example, `ibis` does not provide the `tail` function to look at the last
rows in a database, even though `pandas` does.

```{index} DataFrame; tail
```

```{code-cell} ipython3
:tags: ["output_scroll"]
canlang_table_selected.tail(6)
```

```{code-cell} ipython3
aboriginal_lang_data.tail(6)
```

So once you have finished your data wrangling of the database reference object, it is advisable to
bring it into Python as a `pandas` data frame using the `execute` function.
But be very careful using `execute`: databases are often *very* big,
and reading an entire table into Python might take a long time to run or even possibly
crash your machine. So make sure you select and filter the database table
to reduce the data to a reasonable size before using `execute` to read it into Python!

### Reading data from a PostgreSQL database

```{index} database; PostgreSQL
```

PostgreSQL (also called Postgres) is a very popular
and open-source option for relational database software.
Unlike SQLite,
PostgreSQL uses a client–server database engine, as it was designed to be used
and accessed on a network. This means that you have to provide more information
to Python when connecting to Postgres databases. The additional information that you
need to include when you call the `connect` function is listed below:

- `database`: the name of the database (a single PostgreSQL instance can host more than one database)
- `host`: the URL pointing to where the database is located (`localhost` if it is on your local machine)
- `port`: the communication endpoint between Python and the PostgreSQL database (usually `5432`)
- `user`: the username for accessing the database
- `password`: the password for accessing the database

Below we demonstrate how to connect to a version of
the `can_mov_db` database, which contains information about Canadian movies.
Note that the `host` (`fakeserver.stat.ubc.ca`), `user` (`user0001`), and
`password` (`abc123`) below are *not real*; you will not actually
be able to connect to a database using this information.

```{index} ibis; postgres, ibis; connect
```

```{code-cell} ipython3
:tags: ["remove-output"]
conn = ibis.postgres.connect(
    database="can_mov_db",
    host="fakeserver.stat.ubc.ca",
    port=5432,
    user="user0001",
    password="abc123"
)
```

Aside from needing to provide that additional information, `ibis` makes it so
that connecting to and working with a Postgres database is identical to
connecting to and working with an SQLite database. For example, we can again use
`list_tables` to find out what tables are in the `can_mov_db` database:

```{index} ibis; list_tables
```

```{code-cell} ipython3
:tags: ["remove-output"]
conn.list_tables()
```

```{code-cell} ipython3
:tags: ["remove-input"]
print('["themes", "medium", "titles", "title_aliases", "forms", "episodes", "names", "names_occupations", "occupation", "ratings"]')
```

We see that there are 10 tables in this database. Let's first look at the
`"ratings"` table to find the lowest rating that exists in the `can_mov_db`
database.

```{index} ibis; table
```

```{code-cell} ipython3
:tags: ["remove-output"]
ratings_table = conn.table("ratings")
ratings_table
```

```{code-cell} ipython3
:tags: ["remove-input"]
print("""
AlchemyTable: ratings
  title           string
  average_rating  float64
  num_votes       int64
""")
```

```{index} ibis; []
```

To find the lowest rating that exists in the data base, we first need to
select the `average_rating` column:

```{code-cell} ipython3
:tags: ["remove-output"]
avg_rating = ratings_table[["average_rating"]]
avg_rating
```

```{code-cell} ipython3
:tags: ["remove-input"]
print("""
r0 := AlchemyTable: ratings
  title           string
  average_rating  float64
  num_votes       int64

Selection[r0]
  selections:
    average_rating: r0.average_rating
""")
```

```{index} database; ordering, ibis; order_by, ibis; head
```

Next we use the `order_by` function from `ibis` order the table by `average_rating`,
and then the `head` function to select the first row (i.e., the lowest score).

```{code-cell} ipython3
:tags: ["remove-output"]
lowest = avg_rating.order_by("average_rating").head(1)
lowest.execute()
```

```{code-cell} ipython3
:tags: ["remove-input"]
lowest = pd.DataFrame({"average_rating" : [1.0]})
lowest
```

We see the lowest rating given to a movie is 1, indicating that it must have
been a really bad movie...

### Why should we bother with databases at all?

```{index} database; reasons to use
```

Opening a database involved a lot more effort than just opening a `.csv`, or any of the
other plain text or Excel formats. We had to open a connection to the database,
then use `ibis` to translate `pandas`-like
commands (the `[]` operation, `head`, etc.) into SQL queries that the database
understands, and then finally `execute` them. And not all `pandas` commands can currently be translated
via `ibis` into database queries. So you might be wondering: why should we use
databases at all?

Databases are beneficial in a large-scale setting:

- They enable storing large data sets across multiple computers with backups.
- They provide mechanisms for ensuring data integrity and validating input.
- They provide security and data access control.
- They allow multiple users to access data simultaneously
  and remotely without conflicts and errors.
  For example, there are billions of Google searches conducted daily in 2021 {cite:p}`googlesearches`.
  Can you imagine if Google stored all of the data
  from those searches in a single `.csv` file!? Chaos would ensue!

