
(move-to-your-own-machine)=
# Setting up your computer

## Overview

In this chapter, you'll learn how to set up the software needed to follow along
with this book on your own computer.  Given that installation instructions can
vary based on computer setup, we provide instructions for
multiple operating systems (Ubuntu Linux, MacOS, and Windows).
Although the instructions in this chapter will likely work on many systems,
we have specifically verified that they work on a computer that:

- runs Windows 10 Home, MacOS 13 Ventura, or Ubuntu 22.04,
- uses a 64-bit CPU,
- has a connection to the internet,
- uses English as the default language.


## Chapter learning objectives

By the end of the chapter, readers will be able to do the following:

- Download the worksheets that accompany this book.
- Install the Docker virtualization engine.
- Edit and run the worksheets using JupyterLab running inside a Docker container.
- Install Git, JupyterLab Desktop, and Python packages.
- Edit and run the worksheets using JupyterLab Desktop.

## Obtaining the worksheets for this book

The worksheets containing exercises for this book
are online at [https://worksheets.python.datasciencebook.ca](https://worksheets.python.datasciencebook.ca).
You can download the worksheets as a compressed zip file
using [the link at the top of the page](https://github.com/UBC-DSCI/data-science-a-first-intro-python-worksheets/archive/refs/heads/main.zip).
Once you unzip the downloaded file, you will have a folder containing all of the Jupyter notebook worksheets
accompanying this book. See {numref}`Chapter %s <getting-started-with-jupyter>` for
instructions on working with Jupyter notebooks.

## Working with Docker

Once you have downloaded the worksheets, you will next need to install and run
the software required to work on Jupyter notebooks on your own computer. Doing
this setup manually can be quite tricky, as it involves quite a few different
software packages, not to mention getting the right versions of
everything&mdash;the worksheets and autograder tests may not work unless all the versions are
exactly right! To keep things simple, we instead recommend that you install
[Docker](https://docker.com). Docker lets you run your Jupyter notebooks inside
a pre-built *container* that comes with precisely the right versions of
all software packages needed run the worksheets that come with this book.
```{index} Docker, container
```

```{note}
A *container* is a virtual user space within your computer.
Within the container, you can run software in isolation without interfering with the
other software that already exists on your machine. In this book, we use
a container to run a specific version of the Python programming
language, as well as other necessary packages. The container ensures that
the worksheets function correctly, even if you have a different version of Python
installed on your computer&mdash;or even if you haven't installed Python at all!
```

### Windows

**Installation** To install Docker on Windows,
visit [the online Docker documentation](https://docs.docker.com/desktop/install/windows-install/),
and download the `Docker Desktop Installer.exe` file. Double-click the file to open the installer
and follow the instructions on the installation wizard, choosing **WSL-2** instead of **Hyper-V** when prompted.
```{index} Docker;installation
```

```{note}
Occasionally, when you first run Docker on Windows, you will encounter an error message. Some common errors you may see:

- If you need to update WSL, you can enter `cmd.exe` in the Start menu to run the command line. Type `wsl --update` to update WSL.
- If the admin account on your computer is different to your user account, you must add the user to the "docker-users" group.
  Run Computer Management as an administrator and navigate to `Local Users` and `Groups -> Groups -> docker-users`. Right-click to
  add the user to the group. Log out and log back in for the changes to take effect.
- If you need to enable virtualization, you will need to edit your BIOS. Restart your computer, and enter the BIOS using the hotkey
  (usually Delete, Esc, and/or one of the F# keys). Look for an "Advanced" menu, and under your CPU settings, set the "Virtualization" option
  to "enabled". Then save the changes and reboot your machine. If you are not familiar with BIOS editing, you may want to find an expert
  to help you with this, as editing the BIOS can be dangerous. Detailed instructions for doing this are beyond the scope of this book.
```

```{index} Docker;image, Docker;tag
```
**Running JupyterLab** Run Docker Desktop. Once it is running, you need to download and run the
Docker *image* that we have made available for the worksheets (an *image* is like a "snapshot" of a
computer with all the right packages pre-installed). You only need to do this step one time; the image will remain
the next time you run Docker Desktop.
In the Docker Desktop search bar, enter `ubcdsci/py-dsci-100`, as this is
the name of the image. You will see the `ubcdsci/py-dsci-100` image in the list ({numref}`docker-desktop-search`),
and "latest" in the Tag drop down menu. We need to change "latest" to the right image version before proceeding.
To find the right tag, open
the [`Dockerfile` in the worksheets repository](https://raw.githubusercontent.com/UBC-DSCI/data-science-a-first-intro-python-worksheets/main/Dockerfile),
and look for the line `FROM ubcdsci/py-dsci-100:` followed by the tag consisting of a sequence of numbers and letters.
Back in Docker Desktop, in the "Tag" drop down menu, click that tag to select the correct image version. Then click
the "Pull" button to download the image.

```{figure} img/setup/docker-1.png
---
height: 400px
name: docker-desktop-search
---
The Docker Desktop search window. Make sure to click the Tag drop down menu and find the right version of the image before clicking the Pull button to download it.
```

Once the image is done downloading, click the "Images" button on the left side
of the Docker Desktop window ({numref}`docker-desktop-images`). You
will see the recently downloaded image listed there under the "Local" tab.

```{figure} img/setup/docker-2.png
---
height: 400px
name: docker-desktop-images
---
The Docker Desktop images tab.
```

To start up a *container* using that image, click the play button beside the
image. This will open the run configuration menu ({numref}`docker-desktop-runconfig`).
Expand the "Optional settings" drop down menu. In the "Host port" textbox, enter
`8888`. In the "Volumes" section, click the "Host path" box and navigate to the
folder where your Jupyter worksheets are stored. In the "Container path" text
box, enter `/home/jovyan/work`. Then click the "Run" button to start the
container.

```{figure} img/setup/docker-3.png
---
height: 400px
name: docker-desktop-runconfig
---
The Docker Desktop container run configuration menu.
```

After clicking the "Run" button, you will see a terminal. The terminal will then print
some text as the Docker container starts. Once the text stops scrolling, find the
URL in the terminal that starts
with `http://127.0.0.1:8888` (highlighted by the red box in {numref}`docker-desktop-url`), and paste it
into your browser to start JupyterLab.

```{figure} img/setup/docker-4.png
---
height: 400px
name: docker-desktop-url
---
The terminal text after running the Docker container. The red box indicates the URL that you should paste into your browser to open JupyterLab.
```

When you are done working, make sure to shut down and remove the container by
clicking the red trash can symbol (in the top right corner of {numref}`docker-desktop-url`).
You will not be able to start the container again until you do so.
More information on installing and running
Docker on Windows, as well as troubleshooting tips, can
be found in [the online Docker documentation](https://docs.docker.com/desktop/install/windows-install/).

### MacOS

**Installation** To install Docker on MacOS,
visit [the online Docker documentation](https://docs.docker.com/desktop/install/mac-install/), and
download the `Docker.dmg` installation file that is appropriate for your
computer. To know which installer is right for your machine, you need to know
whether your computer has an Intel processor (older machines) or an
Apple processor (newer machines); the [Apple support page](https://support.apple.com/en-ca/HT211814) has
information to help you determine which processor you have. Once downloaded, double-click
the file to open the installer, then drag the Docker icon to the Applications folder.
Double-click the icon in the Applications folder to start Docker. In the installation
window, use the recommended settings.

**Running JupyterLab** Run Docker Desktop. Once it is running, follow the
instructions above in the Windows section on *Running JupyterLab* (the user
interface is the same). More information on installing and running Docker on
MacOS, as well as troubleshooting tips, can be
found in [the online Docker documentation](https://docs.docker.com/desktop/install/mac-install/).

### Ubuntu

**Installation** To install Docker on Ubuntu, open the terminal and enter the following five commands.
```{code-cell}
:tags: ["remove-output"]
sudo apt update
sudo apt install ca-certificates curl gnupg
curl -fsSL https://get.docker.com -o get-docker.sh
sudo chmod u+x get-docker.sh
sudo sh get-docker.sh
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


