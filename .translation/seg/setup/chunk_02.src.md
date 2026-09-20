## Working with JupyterLab Desktop

You can also run the worksheets accompanying this book on your computer
using [JupyterLab Desktop](https://github.com/jupyterlab/jupyterlab-desktop).
The advantage of JupyterLab Desktop over Docker is that it can be easier to install;
Docker can sometimes run into some fairly technical issues (especially on Windows computers)
that require expert troubleshooting. The downside of JupyterLab Desktop is that there is a (very) small chance that
you may not end up with the right versions of all the Python packages needed for the worksheets. Docker, on the other hand,
*guarantees* that the worksheets will work exactly as intended.

In this section, we will cover how to install JupyterLab Desktop,
Git and the JupyterLab Git extension (for version control, as discussed in {numref}`Chapter %s <getting-started-with-version-control>`), and
all of the Python packages needed to run
the code in this book.
```{index} JupyterLab Desktop, git;installation
```

### Windows

**Installation** First, we will install Git for version control.
Go to [the Git download page](https://git-scm.com/download/win) and
download the Windows version of Git. Once the download has finished, run the installer and accept
the default configuration for all pages.
Next, visit the ["Installation" section of the JupyterLab Desktop homepage](https://github.com/jupyterlab/jupyterlab-desktop#installation).
Download the `JupyterLab-Setup-Windows.exe` installer file for Windows.
Double-click the installer to run it, use the default settings.
Run JupyterLab Desktop by clicking the icon on your desktop.


**Configuring JupyterLab Desktop**
Next, in the JupyterLab Desktop graphical interface that appears ({numref}`setup-jlab-gui`),
you will see text at the bottom saying "Python environment not found". Click "Install using the bundled installer"
to set up the environment.

```{figure} img/setup/jlab-1.png
---
height: 400px
name: setup-jlab-gui
---
The JupyterLab Desktop graphical user interface.
```

Next, we need to add the JupyterLab Git extension (so that
we can use version control directly from within JupyterLab Desktop),
the IPython kernel (to enable the Python programming language),
and various Python software packages. Click "New session..." in the JupyterLab Desktop
user interface, then scroll to the bottom, and click "Terminal" under the "Other" heading ({numref}`setup-jlab-gui-2`).

```{figure} img/setup/jlab-2.png
---
height: 400px
name: setup-jlab-gui-2
---
A JupyterLab Desktop session, showing the Terminal option at the bottom.
```


In this terminal, run the following commands:
```{code-cell}
:tags: ["remove-output"]
pip install --upgrade jupyterlab-git
conda env update --file https://raw.githubusercontent.com/UBC-DSCI/data-science-a-first-intro-python-worksheets/main/environment.yml
```
The second command installs the specific Python and package versions specified in
the `environment.yml` file found in
[the worksheets repository](https://worksheets.python.datasciencebook.ca).
We will always keep the versions in the `environment.yml` file updated
so that they are compatible with the exercise worksheets that accompany the book.
Once all of the software installation is complete, it is a good idea to restart
JupyterLab Desktop entirely before you proceed to doing your data analysis.
This will ensure all the software and settings you put in place are
correctly set up and ready for use.


### MacOS

**Installation** First, we will install Git for version control.
Open the terminal ([how-to video](https://youtu.be/5AJbWEWwnbY))
and type the following command:

```{code-cell}
:tags: ["remove-output"]
xcode-select --install
```
Next, visit the ["Installation" section of the JupyterLab Desktop homepage](https://github.com/jupyterlab/jupyterlab-desktop#installation).
Download the `JupyterLab-Setup-MacOS-x64.dmg` or `JupyterLab-Setup-MacOS-arm64.dmg` installer file.
To know which installer is right for your machine, you need to know
whether your computer has an Intel processor (older machines) or an
Apple processor (newer machines); the [Apple support page](https://support.apple.com/en-ca/HT211814) has
information to help you determine which processor you have.
Once downloaded, double-click the file to open the installer, then drag
the JupyterLab Desktop icon to the Applications folder.  Double-click
the icon in the Applications folder to start JupyterLab Desktop.

**Configuring JupyterLab Desktop** From this point onward, with JupyterLab Desktop running,
follow the instructions in the Windows section on *Configuring JupyterLab Desktop* to set up the
environment, install the JupyterLab Git extension, and install
the various Python software packages needed for the worksheets.

### Ubuntu

**Installation** First, we will install Git for version control.
Open the terminal and type the following commands:
```{code-cell}
:tags: ["remove-output"]
sudo apt update
sudo apt install git
```
Next, visit the ["Installation" section of the JupyterLab Desktop homepage](https://github.com/jupyterlab/jupyterlab-desktop#installation).
Download the `JupyterLab-Setup-Debian.deb` installer file for Ubuntu/Debian.
Open a terminal, navigate to where the installer file was downloaded, and run the command
```{code-cell}
:tags: ["remove-output"]
sudo dpkg -i JupyterLab-Setup-Debian.deb
```
Run JupyterLab Desktop using the command
```{code-cell}
:tags: ["remove-output"]
jlab
```

**Configuring JupyterLab Desktop** From this point onward, with JupyterLab Desktop running,
follow the instructions in the Windows section on *Configuring JupyterLab Desktop* to set up the
environment, install the JupyterLab Git extension, and install
the various Python software packages needed for the worksheets.
