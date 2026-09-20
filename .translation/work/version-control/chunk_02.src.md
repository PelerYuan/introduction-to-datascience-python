+++

### Editing files on GitHub with the pen tool

```{index} GitHub; pen tool
```

The pen tool can be used to edit existing plain text files. When you click on
the pen tool, the file will be opened in a text box where you can use your
keyboard to make changes ({numref}`pen-tool-01` and {numref}`pen-tool-02`).

```{figure} img/version-control/pen-tool_01.png
---
name: pen-tool-01
---
Clicking on the pen tool opens a text box for editing plain text files.
```


```{figure} img/version-control/pen-tool_02.png
---
name: pen-tool-02
---
The text box where edits can be made after clicking on the pen tool.
```

```{index} GitHub; commit
```

After you are done with your edits, they can be "saved" by *committing* your
changes. When you *commit a file* in a repository, the version control system
takes a snapshot of what the file looks like. As you continue working on the
project, over time you will possibly make many commits to a single file; this
generates a useful version history for that file. On GitHub, if you click the
green "Commit changes" button, it will save the file and then make a commit
({numref}`pen-tool-03`).

Recall from {numref}`commit-changes` that you normally have to add files
to the staging area before committing them. Why don't we have to do that when
we work directly on GitHub? Behind the scenes, when you click the green "Commit changes"
button, GitHub *is* adding that one file to the staging area prior to committing it.
But note that on GitHub you are limited to committing changes to only one file at a time.
When you work in your own local repository, you can commit
changes to multiple files simultaneously. This is especially useful when one
"improvement" to the project involves modifying multiple files.
You can also do things like run code when working in a local repository, which you cannot
do on GitHub. In general, editing on GitHub is reserved for small edits to plain text files.

```{figure} img/version-control/pen-tool_03.png
---
name: pen-tool-03
---
Saving changes using the pen tool requires committing those changes, and an associated commit message.
```

### Creating files on GitHub with the "Add file" menu

```{index} GitHub; add file
```

The "Add file" menu can be used to create new plain text files and upload files
from your computer. To create a new plain text file, click the "Add file"
drop-down menu and select the "Create new file" option
({numref}`create-new-file-01`).

```{figure} img/version-control/create-new-file_01.png
---
name: create-new-file-01
---
New plain text files can be created directly on GitHub.
```

```{index} markdown
```

A page will open with a small text box for the file name to be entered, and a
larger text box where the desired file content text can be entered. Note the two
tabs, "Edit new file" and "Preview". Toggling between them lets you enter and
edit text and view what the text will look like when rendered, respectively
({numref}`create-new-file-02`).
Note that GitHub understands and renders `.md` files using a
markdown syntax very similar to Jupyter notebooks, so the "Preview" tab is especially helpful
for checking markdown code correctness.

```{figure} img/version-control/create-new-file_02.png
---
name: create-new-file-02
---
New plain text files require a file name in the text box circled in red, and file content entered in the larger text box (red arrow).
```

Save and commit your changes by clicking the green "Commit changes" button at the
bottom of the page ({numref}`create-new-file-03`).

```{figure} img/version-control/create-new-file_03.png
---
name: create-new-file-03
---
To be saved, newly created files are required to be committed along with an associated commit message.
```

You can also upload files that you have created on your local machine by using
the "Add file" drop-down menu and selecting "Upload files"
({numref}`upload-files-01`).
To select the files from your local computer to upload, you can either drag and
drop them into the gray box area shown in {numref}`upload-files-02`, or click the "choose your files"
link to access a file browser dialog. Once the files you want to upload have
been selected, click the green "Commit changes" button at the bottom of the
page ({numref}`upload-files-02`).

```{figure} img/version-control/upload-files_01.png
---
name: upload-files-01
---
New files of any type can be uploaded to GitHub.
```

```{figure} img/version-control/upload-files_02.png
---
name: upload-files-02
---
Specify files to upload by dragging them into the GitHub website (red circle)
or by clicking on "choose your files." Uploaded files are also required to be
committed along with an associated commit message.
```


Note that Git and GitHub are designed to track changes in individual files.
**Do not** upload your whole project in an archive file (e.g., `.zip`). If you do,
then Git can only keep track of changes to the entire `.zip` file, which will not
be human-readable. Committing one big archive defeats the whole purpose of using
version control: you won't be able to see, interpret, or find changes in the history
of any of the actual content of your project!

(local-repo-jupyter)=
## Working with local repositories using Jupyter

```{index} git;Jupyter extension
```

Although there are several ways to create and edit files on GitHub, they are
not quite powerful enough for efficiently creating and editing complex files,
or files that need to be executed to assess whether they work (e.g., files
containing code).  For example, you wouldn't be able to run an analysis written
with Python code directly on GitHub.  Thus, it is useful to be able to connect the
remote repository that was created on GitHub to a local coding environment.  This
can be done by creating and working in a local copy of the repository.
In this chapter, we focus on interacting with Git via Jupyter using
the Jupyter Git extension. The Jupyter Git extension
can be run by Jupyter on your local computer, or on a JupyterHub server.
We recommend reading {numref}`Chapter %s <getting-started-with-jupyter>`
to learn how to use Jupyter before reading this chapter.

### Generating a GitHub personal access token

```{index} GitHub; personal access token
```

To send and retrieve work between your local repository
and the remote repository on GitHub,
you will frequently need to authenticate with GitHub
to prove you have the required permission.
There are several methods to do this,
but for beginners we recommend using the HTTPS method
because it is easier and requires less setup.
In order to use the HTTPS method,
GitHub requires you to provide a *personal access token*.
A personal access token is like a password&mdash;so keep it a secret!&mdash;but it gives
you more fine-grained control over what parts of your account
the token can be used to access, and lets you set an expiry date for the authentication.
To generate a personal access token,
you must first visit [https://github.com/settings/tokens](https://github.com/settings/tokens),
which will take you to the "Personal access tokens" page in your account settings.
Once there, click "Generate new token" ({numref}`generate-pat-01`).
Note that you may be asked to re-authenticate with your username
and password to proceed.


```{figure} img/version-control/generate-pat_01.png
---
name: generate-pat-01
---
The "Generate new token" button used to initiate the creation of a new personal
access token. It is found in the "Personal access tokens" section of the
"Developer settings" page in your account settings.
```


You will be asked to add a note to describe the purpose for your personal access token.
Next, you need to select permissions for the token; this is where
you can control what parts of your account the token can be used to access.
Make sure to choose only those permissions that you absolutely require. In
{numref}`generate-pat-02`, we tick only the "repo" box, which gives the
token access to our repositories (so that we can push and pull) but none of our other GitHub
account features. Finally, to generate the token, scroll to the bottom of that page
and click the green "Generate token" button ({numref}`generate-pat-02`).

```{figure} img/version-control/generate-pat_02.png
---
name: generate-pat-02
---
Webpage for creating a new personal access token.
```


Finally, you will be taken to a page where you will be able to see
and copy the personal access token you just generated ({numref}`generate-pat-03`).
Since it provides access to certain parts of your account, you should
treat this token like a password; for example, you should consider
securely storing it (and your other passwords and tokens, too!) using a password manager.
Note that this page will only display the token to you once,
so make sure you store it in a safe place right away. If you accidentally forget to
store it, though, do not fret&mdash;you can delete that token by clicking the
"Delete" button next to your token, and generate a new one from scratch.
To learn more about GitHub authentication,
see the additional resources section at the end of this chapter.

```{figure} img/version-control/generate-pat_03.png
---
name: generate-pat-03
---
Display of the newly generated personal access token.
```

### Cloning a repository using Jupyter

```{index} git;clone
```

*Cloning* a remote repository from GitHub
to create a local repository results in a
copy that knows where it was obtained from so that it knows where to send/receive
new committed edits. In order to do this, first copy the URL from the HTTPS tab
of the Code drop-down menu on GitHub ({numref}`clone-02`).

```{figure} img/version-control/clone_02.png
---
name: clone-02
---
The green "Code" drop-down menu contains the remote address (URL) corresponding to the location of the remote GitHub repository.
```

Open Jupyter, and click the Git+ icon on the file browser tab
({numref}`clone-01`).

```{figure} img/version-control/clone_01.png
---
name: clone-01
---
The Jupyter Git Clone icon (red circle).
```



Paste the URL of the GitHub project repository you
created and click the blue "CLONE" button ({numref}`clone-03`).

```{figure} img/version-control/clone_03.png
---
name: clone-03
---
Prompt where the remote address (URL) corresponding to the location of the GitHub repository needs to be input in Jupyter.
```

On the file browser tab, you will now see a folder for the repository.
Inside this folder  will be all the files that existed on GitHub ({numref}`clone-04`).

```{figure} img/version-control/clone_04.png
---
name: clone-04
---
Cloned GitHub repositories can been seen and accessed via the Jupyter file browser.
```


### Specifying files to commit
Now that you have cloned the remote repository from GitHub to create a local repository,
you can get to work editing, creating, and deleting files.
For example, suppose you created and saved a new file (named `eda.ipynb`) that you would
like to send back to the project repository on GitHub ({numref}`git-add-01`).
To "add" this modified file to the staging area (i.e., flag that this is a
file whose changes we would like to commit), click the Jupyter Git extension
icon on the far left-hand side of Jupyter ({numref}`git-add-01`).

```{figure} img/version-control/git_add_01.png
---
name: git-add-01
---
Jupyter Git extension icon (circled in red).
```

```{index} git;add
```


This opens the Jupyter Git graphical user interface pane. Next,
click the plus sign (+) beside the file(s) that you want to "add"
({numref}`git-add-02`). Note that because this is the
first change for this file, it falls under the "Untracked" heading.
However, next time you edit this file  and want to add the changes,
you will find it under the "Changed" heading.

You will also see an `eda-checkpoint.ipynb` file under the "Untracked" heading.
This is a temporary "checkpoint file" created by Jupyter when you work on `eda.ipynb`.
You generally do not want to add auto-generated files to Git repositories;
only add the files you directly create and edit.

```{figure} img/version-control/git_add_02.png
---
name: git-add-02
---
`eda.ipynb` is added to the staging area via the plus sign (+).
```

Clicking the plus sign (+) moves the file from the "Untracked" heading to the "Staged" heading,
so that Git knows you want a snapshot of its current state
as a commit ({numref}`git-add-03`). Now you are ready to "commit" the changes.
Make sure to include a (clear and helpful!) message about what was changed
so that your collaborators (and future you) know what happened in this commit.


```{figure} img/version-control/git_add_03.png
---
name: git-add-03
---
Adding `eda.ipynb` makes it visible in the staging area.
```


### Making the commit

```{index} git;commit
```

To snapshot the changes with an associated commit message,
you must put a message in the text box at the bottom of the Git pane
and click on the blue "Commit" button ({numref}`git-commit-01`).
It is highly recommended to write useful and meaningful messages about what
was changed. These commit messages, and the datetime stamp for a given
commit, are the primary means to navigate through the project's history in the
event that you need to view or retrieve a past version of a file, or
revert your project to an earlier state.
When you click the "Commit" button for the first time, you will be prompted to
enter your name and email. This only needs to be done once for each machine
you use Git on.

```{figure} img/version-control/git_commit_01.png
---
name: git-commit-01
---
A commit message must be added into the Jupyter Git extension commit text box before the blue Commit button can be used to record the commit.
```

After "committing" the file(s), you will see there are 0 "Staged" files.
You are now ready to push your changes
to the remote repository on GitHub ({numref}`git-commit-03`).

```{figure} img/version-control/git_commit_03.png
---
name: git-commit-03
---
After recording a commit, the staging area should be empty.
```

### Pushing the commits to GitHub

```{index} git;push
```

To send the committed changes back to the remote repository on
GitHub, you need to *push* them. To do this,
click on the cloud icon with the up arrow on the Jupyter Git tab
({numref}`git-push-01`).

```{figure} img/version-control/git_push_01.png
---
name: git-push-01
---
The Jupyter Git extension "push" button (circled in red).
```

You will then be prompted to enter your GitHub username
and the personal access token that you generated
earlier (not your account password!). Click
the blue "OK" button to initiate the push ({numref}`git-push-02`).

```{figure} img/version-control/git_push_02.png
---
name: git-push-02
---
Enter your Git credentials to authorize the push to the remote repository.
```

If the files were successfully pushed to the project repository on
GitHub, you will be shown a success message ({numref}`git-push-03`).
Click "Dismiss" to continue working in Jupyter.

```{figure} img/version-control/git_push_03.png
---
name: git-push-03
---
The prompt that the push was successful.
```

If you visit the remote repository on GitHub,
you will see that the changes now exist there too
({numref}`git-push-04`)!

```{figure} img/version-control/git_push_04.png
---
name: git-push-04
---
The GitHub web interface shows a preview of the commit message, and the time of the most recently pushed commit for each file.
```

