## Collaboration

### Giving collaborators access to your project

```{index} GitHub; collaborator access
```

As mentioned earlier, GitHub allows you to control who has access to your
project. The default of both public and private projects are that only the
person who created the GitHub repository has permissions to create, edit and
delete files (*write access*). To give your collaborators write access to the
projects, navigate to the "Settings" tab ({numref}`add-collab-01`).

```{figure} img/version-control/add_collab_01.png
---
name: add-collab-01
---
The "Settings" tab on the GitHub web interface.
```

Then click "Manage access" ({numref}`add-collab-02`).

```{figure} img/version-control/add_collab_02.png
---
name: add-collab-02
---
The "Manage access" tab on the GitHub web interface.
```

Then click the green "Invite a collaborator" button ({numref}`add-collab-03`).

```{figure} img/version-control/add_collab_03.png
---
name: add-collab-03
---
The "Invite a collaborator" button on the GitHub web interface.
```

Type in the collaborator's GitHub username or email,
and select their name when it appears ({numref}`add-collab-04`).

```{figure} img/version-control/add_collab_04.png
---
name: add-collab-04
---
The text box where a collaborator's GitHub username or email can be entered.
```

Finally, click the green "Add <COLLABORATORS_GITHUB_USER_NAME> to this repository" button ({numref}`add-collab-05`).

```{figure} img/version-control/add_collab_05.png
---
name: add-collab-05
---
The confirmation button for adding a collaborator to a repository on the GitHub web interface.
```

After this, you should see your newly added collaborator listed under the
"Manage access" tab. They should receive an email invitation to join the
GitHub repository as a collaborator. They need to accept this invitation
to enable write access.

### Pulling changes from GitHub using Jupyter

We will now walk through how to use the Jupyter Git extension tool to pull changes
to our `eda.ipynb` analysis file that were made by a collaborator
({numref}`git-pull-00`).

```{figure} img/version-control/git_pull_00.png
---
name: git-pull-00
---
The GitHub interface indicates the name of the last person to push a commit to the remote repository, a preview of the associated commit message, the unique commit identifier, and how long ago the commit was snapshotted.
```

```{index} git;pull
```

You can tell Git to "pull" by clicking on the cloud icon with
the down arrow in Jupyter ({numref}`git-pull-01`).

```{figure} img/version-control/git_pull_01.png
---
name: git-pull-01
---
The Jupyter Git extension clone button.
```

Once the files are successfully pulled from GitHub, you need to click "Dismiss"
to keep working ({numref}`git-pull-02`).

```{figure} img/version-control/git_pull_02.png
---
name: git-pull-02
---
The prompt after changes have been successfully pulled from a remote repository.
```

And then when you open (or refresh) the files whose changes you just pulled,
you should be able to see them ({numref}`git-pull-03`).

```{figure} img/version-control/git_pull_03.png
---
name: git-pull-03
---
Changes made by the collaborator to `eda.ipynb` (code highlighted by red arrows).
```

It can be very useful to review the history of the changes to your project. You
can do this directly in Jupyter by clicking "History" in the Git tab
({numref}`git-pull-04`).

```{figure} img/version-control/git_pull_04.png
---
name: git-pull-04
---
Version control repository history viewed using the Jupyter Git extension.
```


It is good practice to pull any changes at the start of *every* work session
before you start working on your local copy.
If you do not do this,
and your collaborators have pushed some changes to the project to GitHub,
then you will be unable to push your changes to GitHub until you pull.
This situation can be recognized by the error message
shown in {numref}`merge-conflict-01`.

```{figure} img/version-control/merge_conflict_01.png
---
name: merge-conflict-01
---
Error message that indicates that there are changes on the remote repository that you do not have locally.
```

Usually, getting out of this situation is not too troublesome. First you need
to pull the changes that exist on GitHub that you do not yet have in the local
repository.  Usually when this happens, Git can automatically merge the changes
for you, even if you and your collaborators were working on different parts of
the same file!

If, however, you and your collaborators made changes to the same line of the
same file, Git will not be able to automatically merge the changes&mdash;it will
not know whether to keep your version of the line(s), your collaborators
version of the line(s), or some blend of the two. When this happens, Git will
tell you that you have a merge conflict in certain file(s) ({numref}`merge-conflict-03`).

```{figure} img/version-control/merge_conflict_03.png
---
name: merge-conflict-03
---
Error message that indicates you and your collaborators made changes to the
same line of the same file and that Git will not be able to automatically merge
the changes.
```

### Handling merge conflicts

```{index} git;merge conflict
```

To fix the merge conflict, you need to open the offending file
in a plain text editor and look for special marks that Git puts in the file to
tell you where the merge conflict occurred ({numref}`merge-conflict-04`).


```{figure} img/version-control/merge_conflict_04.png
---
name: merge-conflict-04
---
How to open a Jupyter notebook as a plain text file view in Jupyter.
```

The beginning of the merge
conflict is preceded by `<<<<<<< HEAD` and the end of the merge conflict is
marked by `>>>>>>>`. Between these markings, Git also inserts a separator
(`=======`). The version of the change before the separator is your change, and
the version that follows the separator was the change that existed on GitHub.
In {numref}`merge-conflict-05`, you can see that in your local repository
there is a line of code that sets the axis scaling to `"sqrt"`.
It looks like your collaborator made an edit to that line too, except with axis scaling `"log"`!

```{figure} img/version-control/merge_conflict_05.png
---
name: merge-conflict-05
---
Merge conflict identifiers (highlighted in red).
```

Once you have decided which version of the change (or what combination!) to
keep, you need to use the plain text editor to remove the special marks that
Git added ({numref}`merge-conflict-06`).

```{figure} img/version-control/merge_conflict_06.png
---
name: merge-conflict-06
---
File where a merge conflict has been resolved.
```

The file must be saved, added to the staging area, and then committed before you will be able to
push your changes to GitHub.

### Communicating using GitHub issues

When working on a project in a team, you don't just want a historical record of who changed
what file and when in the project&mdash;you also want a record of decisions that were made,
ideas that were floated, problems that were identified and addressed, and all other
communication surrounding the project. Email and messaging apps are both very popular for general communication, but are not
designed for project-specific communication: they both generally do not have facilities for organizing conversations by project subtopics,
searching for conversations related to particular bugs or software versions, etc.

```{index} GitHub;issues
```

GitHub *issues* are an alternative written communication medium to email and
messaging apps, and were designed specifically to facilitate project-specific
communication. Issues are *opened* from the "Issues" tab on the project's
GitHub page, and they persist there even after the conversation is over and the issue is *closed* (in
contrast to email, issues are not usually deleted). One issue thread is usually created
per topic, and they are easily searchable using GitHub's search tools. All
issues are accessible to all project collaborators, so no one is left out of
the conversation. Finally, issues can be set up so that team members get email
notifications when a new issue is created or a new post is made in an issue
thread. Replying to issues from email is also possible. Given all of these advantages,
 we highly recommend the use of issues for project-related communication.

To open a GitHub issue,
first click on the "Issues" tab ({numref}`issue-01`).

```{figure} img/version-control/issue_01.png
---
name: issue-01
---
The "Issues" tab on the GitHub web interface.
```

Next click the "New issue" button ({numref}`issue-02`).

```{figure} img/version-control/issue_02.png
---
name: issue-02
---
The "New issues" button on the GitHub web interface.
```

Add an issue title (which acts like an email subject line), and then put the
body of the message in the larger text box. Finally, click "Submit new issue"
to post the issue to share with others ({numref}`issue-03`).

```{figure} img/version-control/issue_03.png
---
name: issue-03
---
Dialog boxes and submission button for creating new GitHub issues.
```

You can reply to an issue that someone opened by adding your written response to
the large text box and clicking comment ({numref}`issue-04`).

```{figure} img/version-control/issue_04.png
---
name: issue-04
---
Dialog box for replying to GitHub issues.
```


When a conversation is resolved, you can click "Close issue".
The closed issue can be later viewed by clicking the "Closed" header link
in the "Issue" tab ({numref}`issue-06`).

```{figure} img/version-control/issue_06.png
---
name: issue-06
---
The "Closed" issues tab on the GitHub web interface.
```

## Exercises

Practice exercises for the material covered in this chapter can be found in the
accompanying [worksheets repository](https://worksheets.python.datasciencebook.ca) in
the "Collaboration with version control" row. You can preview a
non-interactive version of the worksheet for this chapter by clicking "view
worksheet." To work on the exercises interactively, follow the instructions in
the worksheets repository to download all worksheets, and follow the
instructions for computer setup found in {numref}`Chapter %s <move-to-your-own-machine>`. This will ensure
that the automated feedback and guidance that the worksheets provide will
function as intended.

## Additional resources

Now that you've picked up the basics of version control with Git and GitHub,
you can expand your knowledge through the resources listed below:

- GitHub's [guides website](https://docs.github.com/) is a great resource for
  learning more about Git and GitHub.
- [Good enough practices in scientific
  computing](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510#sec014)
  {cite:p}`wilson2014best` provides more advice on useful workflows and "good enough"
  practices in data analysis projects.
- In addition to [GitHub](https://github.com), there are other popular Git
  repository hosting services such as [GitLab](https://gitlab.com) and
  [BitBucket](https://bitbucket.org). Comparing all of these options is beyond
  the scope of this book, and until you become a more advanced user, you are
  perfectly fine to just stick with GitHub. Just be aware that you have options!
- GitHub's [documentation on creating a personal access
  token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
  is an excellent additional resource to consult if you need help
  generating and using personal access tokens.

+++

## References

```{bibliography}
:filter: docname in docnames
```
