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

