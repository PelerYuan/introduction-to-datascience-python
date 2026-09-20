+++

First, you will need to visit the [NASA APIs page](https://api.nasa.gov/) and generate an API key (i.e., a password used to identify you when accessing the API).
Note that a valid email address is required to
associate with the key. The signup form looks something like {numref}`fig:NASA-API-signup`.
After filling out the basic information, you will receive the token via email.
Make sure to store the key in a safe place, and keep it private.


```{figure} img/reading/NASA-API-signup.png
:name: fig:NASA-API-signup

Generating the API access token for the NASA API.
```

**Caution: think about your API usage carefully!**

When you access an API, you are initiating a transfer of data from a web server
to your computer. Web servers are expensive to run and do not have infinite resources.
If you try to ask for *too much data* at once, you can use up a huge amount of the server's bandwidth.
If you try to ask for data *too frequently*&mdash;e.g., if you
make many requests to the server in quick succession&mdash;you can also bog the server down and make
it unable to talk to anyone else. Most servers have mechanisms to revoke your access if you are not
careful, but you should try to prevent issues from happening in the first place by being extra careful
with how you write and run your code. You should also keep in mind that when a website owner
grants you API access, they also usually specify a limit (or *quota*) of how much data you can ask for.
Be careful not to overrun your quota! So *before* we try to use the API, we will first visit
[the NASA website](https://api.nasa.gov/) to see what limits we should abide by when using the API.
These limits are outlined in {numref}`fig:NASA-API-limits`.

```{figure} img/reading/NASA-API-limits.png
:name: fig:NASA-API-limits

The NASA website specifies an hourly limit of 1,000 requests.
```

After checking the NASA website, it seems like we can send at most 1,000 requests per hour.
That should be more than enough for our purposes in this section.

+++

#### Accessing the NASA API

```{index} API; HTTP, API; query parameters, API; endpoint
```

The NASA API is what is known as an *HTTP API*: this is a particularly common
kind of API, where you can obtain data simply by accessing a
particular URL as if it were a regular website.  To make a query to the NASA
API, we need to specify three things.  First, we specify the URL *endpoint* of
the API, which is simply a URL that helps the remote server understand which
API you are trying to access. NASA offers a variety of APIs, each with its own
endpoint; in the case of the NASA "Astronomy Picture of the Day" API, the URL
endpoint is `https://api.nasa.gov/planetary/apod`. Second, we write `?`, which denotes that a
list of *query parameters* will follow. And finally, we specify a list of
query parameters of the form `parameter=value`, separated by `&` characters.  The NASA
"Astronomy Picture of the Day" API accepts the parameters shown in
{numref}`fig:NASA-API-parameters`.

```{figure} img/reading/NASA-API-parameters.png
:name: fig:NASA-API-parameters

The set of parameters that you can specify when querying the NASA "Astronomy Picture of the Day" API,
along with syntax, default settings, and a description of each.
```

So for example, to obtain the image of the day
from July 13, 2023, the API query would have two parameters: `api_key=YOUR_API_KEY`
and `date=2023-07-13`. Remember to replace `YOUR_API_KEY` with the API key you
received from NASA in your email! Putting it all together, the query will look like the following:
```
https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY&date=2023-07-13
```
If you try putting this URL into your web browser, you'll actually find that the server
responds to your request with some text:

```json
{"date":"2023-07-13","explanation":"A mere 390 light-years away, Sun-like stars
and future planetary systems are forming in the Rho Ophiuchi molecular cloud
complex, the closest star-forming region to our fair planet. The James Webb
Space Telescope's NIRCam peered into the nearby natal chaos to capture this
infrared image at an inspiring scale. The spectacular cosmic snapshot was
released to celebrate the successful first year of Webb's exploration of the
Universe. The frame spans less than a light-year across the Rho Ophiuchi region
and contains about 50 young stars. Brighter stars clearly sport Webb's
characteristic pattern of diffraction spikes. Huge jets of shocked molecular
hydrogen blasting from newborn stars are red in the image, with the large,
yellowish dusty cavity carved out by the energetic young star near its center.
Near some stars in the stunning image are shadows cast by their protoplanetary
disks.","hdurl":"https://apod.nasa.gov/apod/image/2307/STScI-01_RhoOph.png",
"media_type":"image","service_version":"v1","title":"Webb's
Rho Ophiuchi","url":"https://apod.nasa.gov/apod/image/2307/STScI-01_RhoOph1024.png"}
```

```{index} see: JavaScript Object Notation; JSON
```

```{index} JSON, requests; get, requests; json
```

Neat! There is definitely some data there, but it's a bit hard to
see what it all is. As it turns out, this is a common format for data called
*JSON* (JavaScript Object Notation). We won't encounter this kind of data much in this book,
but for now you can interpret this data just like
you'd interpret a Python dictionary: these are `key : value` pairs separated by
commas. For example, if you look closely, you'll see that the first entry is
`"date":"2023-07-13"`, which indicates that we indeed successfully received
data corresponding to July 13, 2023.

So now our job is to do all of this programmatically in Python. We will load
the `requests` package, and make the query using the `get` function, which takes a single URL argument;
you will recognize the same query URL that we pasted into the browser earlier.
We will then obtain a JSON representation of the
response using the `json` method.

<!-- we have disabled the below code for reproducibility, with hidden setting
of the nasa_data object. But you can reproduce this using the DEMO_KEY key -->
```{code-cell} ipython3
:tags: ["remove-output"]
import requests

nasa_data_single = requests.get(
    "https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY&date=2023-07-13"
).json()
nasa_data_single
```

```{code-cell} ipython3
:tags: [remove-input]
import json
with open("data/nasa.json", "r") as f:
    nasa_data = json.load(f)
# the last entry in the stored data is July 13, 2023, so print that
nasa_data[-1]
```

We can obtain more records at once by using the `start_date` and `end_date` parameters, as
shown in the table of parameters in {numref}`fig:NASA-API-parameters`.
Let's obtain all the records between May 1, 2023, and July 13, 2023, and store the result
in an object called `nasa_data`; now the response
will take the form of a Python list. Each item in the list will correspond to a single day's record (just like the `nasa_data_single` object),
and there will be 74 items total, one for each day between the start and end dates:

```{code-cell} ipython3
:tags: ["remove-output"]
nasa_data = requests.get(
    "https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY&start_date=2023-05-01&end_date=2023-07-13"
    ).json()
len(nasa_data)
```

```{code-cell} ipython3
:tags: [remove-input]
# need to secretly re-load the nasa data again because the above running code destroys it
# see PR 341 for why we need to do things this way (essentially due to PDF build)
with open("data/nasa.json", "r") as f:
    nasa_data = json.load(f)
len(nasa_data)
```

For further data processing using the techniques in this book, you'll need to turn this list of dictionaries
into a `pandas` data frame. Here we will extract the `date`, `title`, `copyright`, and `url` variables
from the JSON data, and construct a `pandas` DataFrame using the extracted information.

```{note}
Understanding this code is not required for the remainder of the textbook. It is included for those
readers who would like to parse JSON data into a `pandas` data frame in their own data analyses.
```

```{code-cell} ipython3
data_dict = {
    "date":[],
    "title": [],
    "copyright" : [],
    "url": []
}

for item in nasa_data:
    if "copyright" not in item:
        item["copyright"] = None
    for entry in ["url", "title", "date", "copyright"]:
        data_dict[entry].append(item[entry])

nasa_df = pd.DataFrame(data_dict)
nasa_df
```

Success&mdash;we have created a small data set using the NASA
API! This data is also quite different from what we obtained from web scraping;
the extracted information is readily available in a JSON format, as opposed to raw
HTML code (although not *every* API will provide data in such a nice format).
From this point onward, the `nasa_df` data frame is stored on your
machine, and you can play with it to your heart's content. For example, you can use
`pandas.to_csv` to save it to a file and `pandas.read_csv` to read it into Python again later;
and after reading the next few chapters you will have the skills to
do even more interesting things! If you decide that you want
to ask any of the various NASA APIs for more data
(see [the list of awesome NASA APIS here](https://api.nasa.gov/)
for more examples of what is possible), just be mindful as usual about how much
data you are requesting and how frequently you are making requests.

+++

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Reading in data locally and from the web" row. You can preview a
non-interactive version of the worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.



## Additional resources

- The [`pandas` documentation](https://pandas.pydata.org/docs/getting_started/index.html)
  provides the documentation for the functions we cover in this chapter.
  It is where you should look if you want to learn more about these functions, the
  full set of arguments you can use, and other related functions.
- Sometimes you might run into data in such poor shape that the reading
  functions we cover in this chapter do not work. In that case, you can consult the
  [data loading chapter](https://wesmckinney.com/book/accessing-data.html#io_flat_files)
  from [*Python for Data Analysis*](https://wesmckinney.com/book/) {cite:p}`mckinney2012python`, which goes into a lot
  more detail about how Python parses text from files into data frames.
- A [video](https://www.youtube.com/embed/ephId3mYu9o) from the Udacity
  course *Linux Command Line Basics* provides a good explanation of absolute versus relative paths.
- If you read the subsection on obtaining data from the web via scraping and
  APIs, we provide two companion tutorial video links for how to use the
  SelectorGadget tool to obtain desired CSS selectors for:
    - [extracting the data for apartment listings on Craigslist](https://www.youtube.com/embed/YdIWI6K64zo), and
    - [extracting Canadian city names and populations from Wikipedia](https://www.youtube.com/embed/O9HKbdhqYzk).

+++

## References

```{bibliography}
:filter: docname in docnames
```
