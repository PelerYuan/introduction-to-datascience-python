## Writing data from Python to a `.csv` file

```{index} write function; to_csv, DataFrame; to_csv
```

At the middle and end of a data analysis, we often want to write a data frame
that has changed (through selecting columns, filtering rows, etc.)
to a file to share it with others or use it for another step in the analysis.
The most straightforward way to do this is to use the `to_csv` function
from the `pandas` package.  The default
arguments are to use a comma (`,`) as the separator, and to include column names
in the first row. We also specify `index = False` to tell `pandas` not to print
row numbers in the `.csv` file. Below we demonstrate creating a new version of the Canadian
languages data set without the "Official languages" category according to the
Canadian 2016 Census, and then writing this to a `.csv` file:

```{code-cell} ipython3
no_official_lang_data = canlang_data[canlang_data["category"] != "Official languages"]
no_official_lang_data.to_csv("data/no_official_languages.csv", index=False)
```

## Obtaining data from the web

```{note}
This section is not required reading for the remainder of the textbook. It
is included for those readers interested in learning a little bit more about
how to obtain different types of data from the web.
```

```{index} see: application programming interface; API
```

```{index} API
```

Data doesn't just magically appear on your computer; you need to get it from
somewhere. Earlier in the chapter we showed you how to access data stored in a
plain text, spreadsheet-like format (e.g., comma- or tab-separated) from a web
URL using the `read_csv` function from `pandas`. But as time goes on, it is
increasingly uncommon to find data (especially large amounts of data) in this
format available for download from a URL. Instead, websites now often offer
something known as an **a**pplication **p**rogramming **i**nterface (API),
which provides a programmatic way to ask for subsets of a data set. This allows
the website owner to control *who* has access to the data, *what portion* of
the data they have access to, and *how much* data they can access.  Typically,
the website owner will give you a *token* or *key* (a secret string of characters
somewhat like a password) that you have to provide when accessing the API.

```{index} web scraping, CSS, HTML
```

```{index} see: hypertext markup language; HTML
```

```{index} see: cascading style sheet; CSS
```

Another interesting thought: websites themselves *are* data! When you type a
URL into your browser window, your browser asks the *web server* (another
computer on the internet whose job it is to respond to requests for the
website) to give it the website's data, and then your browser translates that
data into something you can see. If the website shows you some information that
you're interested in, you could *create* a data set for yourself by copying and
pasting that information into a file. This process of taking information
directly from what a website displays is called
*web scraping* (or sometimes *screen scraping*). Now, of course, copying and pasting
information manually is a painstaking and error-prone process, especially when
there is a lot of information to gather. So instead of asking your browser to
translate the information that the web server provides into something you can
see, you can collect that data programmatically&mdash;in the form of
**h**yper**t**ext **m**arkup **l**anguage (HTML) and **c**ascading **s**tyle **s**heet (CSS)
code&mdash;and process it to extract useful information. HTML provides the
basic structure of a site and tells the webpage how to display the content
(e.g., titles, paragraphs, bullet lists etc.), whereas CSS helps style the
content and tells the webpage how the HTML elements should
be presented (e.g., colors, layouts, fonts etc.).

This subsection will show you the basics of both web scraping
with the [`BeautifulSoup` Python package](https://beautiful-soup-4.readthedocs.io/en/latest/) {cite:p}`beautifulsoup`
and accessing the NASA "Astronomy Picture of the Day" API
using the [`requests` Python package](https://requests.readthedocs.io/en/latest/) {cite:p}`requests`.

+++

### Web scraping

#### HTML and CSS selectors

```{index} web scraping, HTML; selector, CSS; selector, Craiglist
```

When you enter a URL into your browser, your browser connects to the
web server at that URL and asks for the *source code* for the website.
This is the data that the browser translates
into something you can see; so if we
are going to create our own data by scraping a website, we have to first understand
what that data looks like! For example, let's say we are interested
in knowing the average rental price (per square foot) of the most recently
available one-bedroom apartments in Vancouver
on [Craiglist](https://vancouver.craigslist.org). When we visit the Vancouver Craigslist
website and search for one-bedroom apartments,
we should see something similar to {numref}`fig:craigslist-human`.

+++

```{figure} img/reading/craigslist_human.png
:name: fig:craigslist-human

Craigslist webpage of advertisements for one-bedroom apartments.
```

+++

Based on what our browser shows us, it's pretty easy to find the size and price
for each apartment listed. But we would like to be able to obtain that information
using Python, without any manual human effort or copying and pasting. We do this by
examining the *source code* that the web server actually sent our browser to
display for us. We show a snippet of it below; the
entire source
is [included with the code for this book](https://github.com/UBC-DSCI/introduction-to-datascience-python/blob/main/source/data/website_source.txt):

```html
<span class="result-meta">
        <span class="result-price">$800</span>
        <span class="housing">
            1br -
        </span>
        <span class="result-hood"> (13768 108th Avenue)</span>
        <span class="result-tags">
            <span class="maptag" data-pid="6786042973">map</span>
        </span>
        <span class="banish icon icon-trash" role="button">
            <span class="screen-reader-text">hide this posting</span>
        </span>
    <span class="unbanish icon icon-trash red" role="button"></span>
    <a href="#" class="restore-link">
        <span class="restore-narrow-text">restore</span>
        <span class="restore-wide-text">restore this posting</span>
    </a>
    <span class="result-price">$2285</span>
</span>
```

Oof...you can tell that the source code for a web page is not really designed
for humans to understand easily. However, if you look through it closely, you
will find that the information we're interested in is hidden among the muck.
For example, near the top of the snippet
above you can see a line that looks like

```html
<span class="result-price">$800</span>
```

That snippet is definitely storing the price of a particular apartment. With some more
investigation, you should be able to find things like the date and time of the
listing, the address of the listing, and more. So this source code most likely
contains all the information we are interested in!

```{index} HTML; tag
```

Let's dig into that line above a bit more. You can see that
that bit of code has an *opening tag* (words between `<` and `>`, like
`<span>`) and a *closing tag* (the same with a slash, like `</span>`). HTML
source code generally stores its data between opening and closing tags like
these. Tags are keywords that tell the web browser how to display or format
the content. Above you can see that the information we want (`$800`) is stored
between an opening and closing tag (`<span>` and `</span>`). In the opening
tag, you can also see a very useful "class" (a special word that is sometimes
included with opening tags): `class="result-price"`. Since we want Python to
programmatically sort through all of the source code for the website to find
apartment prices, maybe we can look for all the tags with the `"result-price"`
class, and grab the information between the opening and closing tag. Indeed,
take a look at another line of the source snippet above:

```html
<span class="result-price">$2285</span>
```

It's yet another price for an apartment listing, and the tags surrounding it
have the `"result-price"` class. Wonderful! Now that we know what pattern we
are looking for&mdash;a dollar amount between opening and closing tags that have the
`"result-price"` class&mdash;we should be able to use code to pull out all of the
matching patterns from the source code to obtain our data. This sort of "pattern"
is known as a *CSS selector* (where CSS stands for **c**ascading **s**tyle **s**heet).

The above was a simple example of "finding the pattern to look for"; many
websites are quite a bit larger and more complex, and so is their website
source code. Fortunately, there are tools available to make this process
easier. For example,
[SelectorGadget](https://selectorgadget.com/) is
an open-source tool that simplifies identifying the generating
and finding of CSS selectors.
At the end of the chapter in the additional resources section, we include a link to
a short video on how to install and use the SelectorGadget tool to
obtain CSS selectors for use in web scraping.
After installing and enabling the tool, you can click the
website element for which you want an appropriate selector. For
example, if we click the price of an apartment listing, we
find that SelectorGadget shows us the selector `.result-price`
in its toolbar, and highlights all the other apartment
prices that would be obtained using that selector ({numref}`fig:sg1`).

```{figure} img/reading/sg1.png
:name: fig:sg1

Using the SelectorGadget on a Craigslist webpage to obtain the CCS selector useful for obtaining apartment prices.
```

If we then click the size of an apartment listing, SelectorGadget shows us
the `span` selector, and highlights many of the lines on the page; this indicates that the
`span` selector is not specific enough to capture only apartment sizes ({numref}`fig:sg3`).

```{figure} img/reading/sg3.png
:name: fig:sg3

Using the SelectorGadget on a Craigslist webpage to obtain a CCS selector useful for obtaining apartment sizes.
```

To narrow the selector, we can click one of the highlighted elements that
we *do not* want. For example, we can deselect the "pic/map" links,
resulting in only the data we want highlighted using the `.housing` selector ({numref}`fig:sg2`).

```{figure} img/reading/sg2.png
:name: fig:sg2

Using the SelectorGadget on a Craigslist webpage to refine the CCS selector to one that is most useful for obtaining apartment sizes.
```

So to scrape information about the square footage and rental price
of apartment listings, we need to use
the two CSS selectors `.housing` and `.result-price`, respectively.
The selector gadget returns them to us as a comma-separated list (here
`.housing , .result-price`), which is exactly the format we need to provide to
Python if we are using more than one CSS selector.

**Caution: are you allowed to scrape that website?**

```{index} web scraping; permission
```

+++

*Before* scraping data from the web, you should always check whether or not
you are *allowed* to scrape it! There are two documents that are important
for this: the `robots.txt` file and the Terms of Service
document. If we take a look at [Craigslist's Terms of Service document](https://www.craigslist.org/about/terms.of.use),
we find the following text: *"You agree not to copy/collect CL content
via robots, spiders, scripts, scrapers, crawlers, or any automated or manual equivalent (e.g., by hand)."*
So unfortunately, without explicit permission, we are not allowed to scrape the website.

```{index} Wikipedia
```

What to do now? Well, we *could* ask the owner of Craigslist for permission to scrape.
However, we are not likely to get a response, and even if we did they would not likely give us permission.
The more realistic answer is that we simply cannot scrape Craigslist. If we still want
to find data about rental prices in Vancouver, we must go elsewhere.
To continue learning how to scrape data from the web, let's instead
scrape data on the population of Canadian cities from Wikipedia.
We have checked the [Terms of Service document](https://foundation.wikimedia.org/wiki/Terms_of_Use/en),
and it does not mention that web scraping is disallowed.
We will use the SelectorGadget tool to pick elements that we are interested in
(city names and population counts) and deselect others to indicate that we are not
interested in them (province names), as shown in {numref}`fig:sg4`.

```{figure} img/reading/sg4.png
:name: fig:sg4

Using the SelectorGadget on a Wikipedia webpage.
```

We include a link to a short video tutorial on this process at the end of the chapter
in the additional resources section. SelectorGadget provides in its toolbar
the following list of CSS selectors to use:

```text
td:nth-child(8) ,
td:nth-child(4) ,
.largestCities-cell-background+ td a
```

Now that we have the CSS selectors that describe the properties of the elements
that we want to target, we can use them to find certain elements in web pages and extract data.


#### Scraping with `BeautifulSoup`

```{index} BeautifulSoup, requests
```

We will use the `requests` and `BeautifulSoup` Python packages to scrape data
from the Wikipedia page. After loading those packages, we tell Python which
page we want to scrape by providing its URL in quotations to the `requests.get`
function. This function obtains the raw HTML of the page, which we then
pass to the `BeautifulSoup` function for parsing:

```{code-cell} ipython3
:tags: ["remove-output"]
import requests
import bs4

wiki = requests.get("https://en.wikipedia.org/wiki/Canada")
page = bs4.BeautifulSoup(wiki.content, "html.parser")
```

```{code-cell} ipython3
:tags: [remove-cell]
import bs4

# the above cell doesn't actually run; this one does run
# and loads the html data from a local, static file

with open("data/canada_wiki.html", "r") as f:
    wiki_hidden = f.read()
page = bs4.BeautifulSoup(wiki_hidden, "html.parser")
```

The `requests.get` function downloads the HTML source code for the page at the
URL you specify, just like your browser would if you navigated to this site.
But instead of displaying the website to you, the `requests.get` function just
returns the HTML source code itself&mdash;stored in the `wiki.content`
variable&mdash;which we then parse using `BeautifulSoup` and store in the
`page` variable. Next, we pass the CSS selectors we obtained from
SelectorGadget to the `select` method of the `page` object.  Make sure to
surround the selectors with quotation marks; `select` expects that argument is
a string. We store the result of the `select` function in the `population_nodes`
variable. Note that `select` returns a list; below we slice the list to
print only the first 5 elements for clarity.

```{code-cell} ipython3
population_nodes = page.select(
    "td:nth-child(8) , td:nth-child(4) , .largestCities-cell-background+ td a"
)
population_nodes[:5]
```

Each of the items in the `population_nodes` list is a *node* from the HTML document that matches the CSS
selectors you specified. A *node* is an HTML tag pair (e.g., `<td>` and `</td>`
which defines the cell of a table) combined with the content stored between the
tags. For our CSS selector `td:nth-child(4)`, an example node that would be
selected would be:

```html
<td style="text-align:left;">
<a href="/wiki/London,_Ontario" title="London, Ontario">London</a>
</td>
```

Next, we extract the meaningful data&mdash;in other words, we get rid of the
HTML code syntax and tags&mdash;from the nodes using the `get_text` function.
In the case of the example node above, `get_text` function returns `"London"`.
Once again we show only the first 5 elements for clarity.

```{code-cell} ipython3
[row.get_text() for row in population_nodes[:5]]
```

Fantastic! We seem to have extracted the data of interest from the raw HTML
source code. But we are not quite done; the data is not yet in an optimal
format for data analysis. Both the city names and population are encoded as
characters in a single vector, instead of being in a data frame with one
character column for city and one numeric column for population (like a
spreadsheet).  Additionally, the populations contain commas (not useful for
programmatically dealing with numbers), and some even contain a line break
character at the end (`\n`). In {numref}`Chapter %s <wrangling>`, we will learn
more about how to *wrangle* data such as this into a more useful format for
data analysis using Python.

+++

#### Scraping with `read_html`

Using `requests` and `BeautifulSoup` to extract data based on CSS selectors is
a very general way to scrape data from the web, albeit perhaps a little bit
complicated.  Fortunately, `pandas` provides the
[`read_html`](https://pandas.pydata.org/docs/reference/api/pandas.read_html.html)
function, which is easier method to try when the data
appear on the webpage already in a tabular format.  The `read_html` function takes one
argument&mdash;the URL of the page to scrape&mdash;and will return a list of
data frames corresponding to all the tables it finds at that URL. We can see
below that `read_html` found 17 tables on the Wikipedia page for Canada.

```{index} read function; read_html
```

```{code-cell} ipython3
:tags: ["remove-output"]
canada_wiki_tables = pd.read_html("https://en.wikipedia.org/wiki/Canada")
len(canada_wiki_tables)
```

```{code-cell} ipython3
:tags: [remove-input]
canada_wiki_tables = pd.read_html("data/canada_wiki.html")
len(canada_wiki_tables)
```

After manually searching through these, we find that the table containing the
population counts of the largest metropolitan areas in Canada is contained in
index 1. We use the `droplevel` method to simplify the column names in the resulting
data frame:

```{code-cell} ipython3
canada_wiki_df = canada_wiki_tables[1]
canada_wiki_df.columns = canada_wiki_df.columns.droplevel()
canada_wiki_df
```

Once again, we have managed to extract the data of interest from the raw HTML
source code&mdash;but this time using the convenient `read_html` function,
without needing to explicitly use CSS selectors! However, once again, we still
need to do some cleaning of this result. Referring back to {numref}`fig:sg4`,
we can see that the table is formatted with two sets of columns (e.g., `Name`
and `Name.1`) that we will need to somehow merge. In {numref}`Chapter %s
<wrangling>`, we will learn more about how to *wrangle* data into a useful
format for data analysis.

### Using an API

```{index} API
```

Rather than posting a data file at a URL for you to download, many websites
these days provide an API that can be accessed through a programming language
like Python. The benefit of using an API is that data owners have much more control
over the data they provide to users. However, unlike web scraping, there is no
consistent way to access an API across websites. Every website typically has
its own API designed especially for its own use case. Therefore we will just
provide one example of accessing data through an API in this book, with the
hope that it gives you enough of a basic idea that you can learn how to use
another API if needed. In particular, in this book we will show you the basics
of how to use the `requests` package in Python to access data from the NASA "Astronomy Picture
of the Day" API (a great source of desktop backgrounds, by the way&mdash;take a look at the stunning
picture of the Rho-Ophiuchi cloud complex {cite:p}`rhoophiuchi` in {numref}`fig:NASA-API-Rho-Ophiuchi` from July 13, 2023!).

```{index} requests, NASA, API; token
```

```{figure} img/reading/NASA-API-Rho-Ophiuchi.png
:name: fig:NASA-API-Rho-Ophiuchi
:width: 400px

The James Webb Space Telescope's NIRCam image of the Rho Ophiuchi molecular cloud complex.
```

