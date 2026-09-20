
(getting-started-with-version-control)=
# Collaboration with version control

> *You mostly collaborate with yourself,
> and me-from-two-months-ago never responds to email.*
>
> --Mark T. Holder

+++

## Overview

```{index} git, GitHub
```

This chapter will introduce the concept of using version control systems
to track changes to a project over its lifespan, to share
and edit code in a collaborative team,
and to distribute the finished project to its intended audience.
This chapter will also introduce how to use
the two most common version control tools: Git for local version control,
and GitHub for remote version control.
We will focus on the most common version control operations
used day-to-day in a standard data science project.
There are many user interfaces for Git; in this chapter
we will cover the Jupyter Git interface.

## Chapter learning objectives

By the end of the chapter, readers will be able to do the following:

- Describe what version control is and why data analysis projects can benefit from it.
- Create a remote version control repository on GitHub.
- Use Jupyter's Git version control tools for project versioning and collaboration:
  - Clone a remote version control repository to create a local repository.
  - Commit changes to a local version control repository.
  - Push local changes to a remote version control repository.
  - Pull changes from a remote version control repository to a local version control repository.
  - Resolve merge conflicts.
- Give collaborators access to a remote GitHub repository.
- Communicate with collaborators using GitHub issues.
- Use best practices when collaborating on a project with others.

## What is version control, and why should I use it?

Data analysis projects often require iteration
and revision to move from an initial idea to a finished product
ready for the intended audience.
Without deliberate and conscious effort towards tracking changes
made to the analysis, projects tend to become messy.
This mess can have serious, negative repercussions on an analysis project,
including results that your code cannot reproduce,
temporary files with snippets of ideas that are forgotten or
not easy to find, mind-boggling file names that make it unclear which is
the current working version of the file (e.g., `document_final_draft_final.txt`,
`to_hand_in_final_v2.txt`, etc.), and more.

Additionally, the iterative nature of data analysis projects
means that most of the time, the final version of the analysis that is
shared with the audience is only a fraction of what was explored during
the development of that analysis.
Changes in data visualizations and modeling approaches,
as well as some negative results, are often not observable from
reviewing only the final, polished analysis.
The lack of observability of these parts of the analysis development
can lead to others repeating things that did not work well,
instead of seeing what did not work well,
and using that as a springboard to new, more fruitful approaches.

Finally, data analyses are typically completed by a team of people
rather than a single person.
This means that files need to be shared across multiple computers,
and multiple people often end up editing the project simultaneously.
In such a situation, determining who has the latest version of the
project&mdash;and how to resolve conflicting edits&mdash;can be a real challenge.

```{index} version control
```

*Version control* helps solve these challenges. Version control is the process
of keeping a record of changes to documents, including when the changes were
made and who made them, throughout the history of their development.  It also
provides the means both to view earlier versions of the project and to revert
changes.  Version control is most commonly used in software development, but
can be used for any electronic files for any type of project, including data
analyses.  Being able to record and view the history of a data analysis project
is important for understanding how and why decisions to use one method or
another were made, among other things.  Version control also facilitates
collaboration via tools to share edits with others and resolve conflicting
edits.  But even if you're working on a project alone, you should still use
version control.  It helps you keep track of what you've done, when you did it,
and what you're planning to do next!

+++

```{index} version control;system, version control;repository hosting
```

To version control a project, you generally need two things:
a *version control system* and a *repository hosting service*.
The version control system is the software responsible
for tracking changes, sharing changes you make with others,
obtaining changes from others, and resolving conflicting edits.
The repository hosting service is responsible for storing a copy
of the version-controlled project online (a *repository*),
where you and your collaborators can access it remotely,
discuss issues and bugs, and distribute your final product.
For both of these items, there is a wide variety of choices.
In this textbook we'll use Git for version control,
and GitHub for repository hosting,
because both are currently the most widely used platforms.
In the
additional resources section at the end of the chapter,
we list many of the common version control systems
and repository hosting services in use today.

```{note}
Technically you don't *have to* use a repository hosting service.
You can, for example, version control a project
that is stored only in a folder on your computer&mdash;never
sharing it on a repository hosting service.
But using a repository hosting service provides a few big benefits,
including managing collaborator access permissions,
tools to discuss and track bugs,
and the ability to have external collaborators contribute work,
not to mention the safety of having your work backed up in the cloud.
Since most repository hosting services now offer free accounts,
there are not many situations in which you wouldn't
want to use one for your project.
```

## Version control repositories

```{index} repository, repository;local, repository;remote
```

```{index} see: repository; version control
```

Typically, when we put a data analysis project under version control,
we create two copies of the repository ({numref}`vc1-no-changes`).
One copy we use as our primary workspace where we create, edit, and delete files.
This copy is commonly referred to as the **local repository**. The local
repository most commonly exists on our computer or laptop, but can also exist within
a workspace on a server (e.g., JupyterHub).
The other copy is typically stored in a repository hosting service (e.g., GitHub), where
we can easily share it with our collaborators.
This copy is commonly referred to as the **remote repository**.

```{figure} img/version-control/vc1-no-changes.png
---
name: vc1-no-changes
---
Schematic of local and remote version control repositories.
```

```{index} working directory, git;commit
```

Both copies of the repository have a **working directory**
where you can create, store, edit, and delete
files (e.g., `analysis.ipynb` in {numref}`vc1-no-changes`).
Both copies of the repository also maintain a full project history
({numref}`vc1-no-changes`).  This history is a record of all versions of the
project files that have been created.  The repository history is not
automatically generated; Git must be explicitly told when to record
a version of the project.  These records are called **commits**. They
are a snapshot of the file contents as well
metadata about the repository at that time the record was created (who made the
commit, when it was made, etc.). In the local and remote repositories shown in
{numref}`vc1-no-changes`, there are two commits represented as rectangles
inside the "Repository History" sections. The white rectangle represents the most
recent commit, while faded rectangles represent previous commits.
Each commit can be identified by a
human-readable **message**, which you write when you make a commit, and a
**commit hash** that Git automatically adds for you.

The purpose of the message is to contain a brief, rich description
of what work was done since the last commit.
Messages act as a very useful narrative
of the changes to a project over its lifespan.
If you ever want to view or revert to an earlier version of the project,
the message can help you identify which commit to view or revert to.
In {numref}`vc1-no-changes`, you can see two such messages,
one for each commit: `Created README.md` and `Added analysis draft`.

```{index} hash
```

The hash is a string of characters consisting of about 40 letters and numbers.
The purpose of the hash is to serve as a unique identifier for the commit,
and is used by Git to index project history. Although hashes are quite long&mdash;imagine
having to type out 40 precise characters to view an old project version!&mdash;Git is able
to work with shorter versions of hashes. In {numref}`vc1-no-changes`, you can see
two of these shortened hashes, one for each commit: `Daa29d6` and `884c7ce`.

## Version control workflows

When you work in a local version-controlled repository, there are generally three additional
steps you must take as part of your regular workflow. In addition to
just working on files&mdash;creating,
editing, and deleting files as you normally would&mdash;you must:

1. Tell Git when to make a commit of your own changes in the local repository.
2. Tell Git when to send your new commits to the remote GitHub repository.
3. Tell Git when to retrieve any new changes (that others made) from the remote GitHub repository.

In this section we will discuss all three of these steps in detail.

(commit-changes)=
### Committing changes to a local repository

When working on files in your local version control
repository (e.g., using Jupyter) and saving your work, these changes will only initially exist in the
working directory of the local repository ({numref}`vc2-changes`).

```{figure} img/version-control/vc2-changes.png
---
name: vc2-changes
---
Local repository with changes to files.
```

```{index} git;add, staging area, git;commit
```

```{index} see: staging area; git
```

Once you reach a point that you want Git to keep a record
of the current version of your work, you need to **commit**
(i.e., snapshot) your changes. A prerequisite to this is telling Git which
files should be included in that snapshot. We call this step **adding** the
files to the **staging area**.
Note that the staging area is not a real physical location on your computer;
it is instead a conceptual placeholder for these files until they are committed.
The benefit of the Git version control system using a staging area is that you
can choose to commit changes in only certain files. For example,
in {numref}`vc-ba2-add`, we add only the two files
that are important to the analysis project (`analysis.ipynb` and `README.md`)
and not our personal scratch notes for the project (`notes.txt`).

```{figure} img/version-control/vc-ba2-add.png
---
name: vc-ba2-add
---
Adding modified files to the staging area in the local repository.
```

Once the files we wish to commit have been added
to the staging area, we can then commit those files to the repository history ({numref}`vc-ba3-commit`).
When we do this, we are required to include a helpful *commit message* to tell
collaborators (which often includes future you!) about the changes that were
made. In {numref}`vc-ba3-commit`, the message is `Message about changes...`; in
your work you should make sure to replace this with an
informative message about what changed. It is also important to note here that
these changes are only being committed to the local repository's history.  The
remote repository on GitHub has not changed, and collaborators would not yet be
able to see your new changes.

```{figure} img/version-control/vc-ba3-commit.png
---
name: vc-ba3-commit
---
Committing the modified files in the staging area to the local repository history, with an informative message about what changed.
```


### Pushing changes to a remote repository

```{index} git;push
```

Once you have made one or more commits that you want to share with your collaborators,
you need to **push** (i.e., send) those commits back to GitHub ({numref}`vc5-push`). This updates
the history in the remote repository (i.e., GitHub) to match what you have in your
local repository. Now when collaborators interact with the remote repository, they will be able
to see the changes you made. And you can also take comfort in the fact that your work is now backed
up in the cloud!

```{figure} img/version-control/vc5-push.png
---
name: vc5-push
---
Pushing the commit to send the changes to the remote repository on GitHub.
```

### Pulling changes from a remote repository

If you are working on a project with collaborators, they will also be making changes to files
(e.g., to the analysis code in a Jupyter notebook and the project's README file),
committing them to their own local repository, and pushing their commits to the remote GitHub repository
to share them with you. When they push their changes, those changes will only initially exist in
the remote GitHub repository and not in your local repository ({numref}`vc6-remote-changes`).

```{figure} img/version-control/vc6-remote-changes.png
---
name: vc6-remote-changes
---
Changes pushed by collaborators, or created directly on GitHub will not be automatically sent to your local repository.
```

```{index} git;pull
```

To obtain the new changes from the remote repository on GitHub, you will need
to **pull** those changes to your own local repository.  By pulling changes,
you synchronize your local repository to what is present on GitHub ({numref}`vc7-pull`).
Additionally, until you pull changes from the remote repository, you will not
be able to push any more changes yourself (though you will still be able to
work and make commits in your own local repository).

```{figure} img/version-control/vc7-pull.png
---
name: vc7-pull
---
Pulling changes from the remote GitHub repository to synchronize your local repository.
```

## Working with remote repositories using GitHub

```{index} repository;remote, GitHub, git;clone
```

Now that you have been introduced to some of the key general concepts
and workflows of Git version control, we will walk through the practical steps.
There are several different ways to start using version control
with a new project. For simplicity and ease of setup,
we recommend creating a remote repository first.
This section covers how to both create and edit a remote repository on GitHub.
Once you have a remote repository set up, we recommend **cloning** (or copying) that
repository to create a local repository in which you primarily work.
You can clone the repository either
on your own computer or in a workspace on a server (e.g., a JupyterHub server).
{numref}`local-repo-jupyter` below will cover this second step in detail.

### Creating a remote repository on GitHub

Before you can create remote repositories on GitHub,
you will need a GitHub account; you can sign up for a free account
at [github.com](https://github.com/).
Once you have logged into your account, you can create a new repository to host
your project by clicking on the "+" icon in the upper right-hand
corner, and then on "New Repository," as shown in
{numref}`new-repository-01`.

```{figure} img/version-control/new_repository_01.png
---
name: new-repository-01
---
New repositories on GitHub can be created by clicking on "New Repository" from the + menu.
```

```{index} repository;public, repository;private
```

Repositories can be set up with a variety of configurations, including a name,
optional description,  and the inclusion (or not) of several template files.
One of the most important configuration items to choose is the visibility to the outside world,
either public or private. *Public* repositories  can be viewed by anyone.
*Private* repositories can be viewed by only you. Both public and private repositories
are only editable by you, but you can change that by giving access to other collaborators.

To get started with a *public* repository having a template `README.md` file, take the
following steps shown in {numref}`new-repository-02`:

1. Enter the name of your project repository. In the example below, we use `canadian_languages`. Most repositories follow a similar naming convention involving only lowercase letter words separated by either underscores or hyphens.
2. Choose an option for the privacy of your repository.
3. Select "Add a README file." This creates a template `README.md` file in your repository's root folder.
4. When you are happy with your repository name and configuration, click on the green "Create Repository" button.

```{figure} img/version-control/new_repository_02.png
---
name: new-repository-02
---
Repository configuration for a project that is public and initialized with a README.md template file.
```

A newly created public repository with a `README.md` template file should look something
like what is shown in {numref}`new-repository-03`.

```{figure} img/version-control/new_repository_03.png
---
name: new-repository-03
---
Respository configuration for a project that is public and initialized with a README.md template file.
```

