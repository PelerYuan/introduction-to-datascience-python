```

**Running JupyterLab** First, open the [`Dockerfile` in the worksheets repository](https://raw.githubusercontent.com/UBC-DSCI/data-science-a-first-intro-python-worksheets/main/Dockerfile),
and look for the line `FROM ubcdsci/py-dsci-100:` followed by a tag consisting of a sequence of numbers and letters.
Then in the terminal, navigate to the directory where you want to run JupyterLab, and run
the following command, replacing `TAG` with the *tag* you found earlier.
```{code-cell}
:tags: ["remove-output"]
docker run --rm -v $(pwd):/home/jovyan/work -p 8888:8888 ubcdsci/py-dsci-100:TAG jupyter lab
```
The terminal will then print some text as the Docker container starts. Once the text stops scrolling, find the
URL in your terminal that starts with `http://127.0.0.1:8888` (highlighted by the
red box in {numref}`ubuntu-docker-terminal`), and paste it into your browser to start JupyterLab.
More information on installing and running Docker on Ubuntu, as well as troubleshooting tips, can be found in
[the online Docker documentation](https://docs.docker.com/engine/install/ubuntu/).

```{figure} img/setup/ubuntu-docker.png
---
height: 400px
name: ubuntu-docker-terminal
---
The terminal text after running the Docker container in Ubuntu. The red box indicates the URL that you should paste into your browser to open JupyterLab.
```


