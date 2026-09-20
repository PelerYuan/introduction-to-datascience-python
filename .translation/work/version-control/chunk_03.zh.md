## 协作

### 为协作者授予项目访问权限

```{index} GitHub; 协作者访问权限
```

如前所述，GitHub 让你可以控制谁有权访问你的项目。无论公开项目还是私有项目，默认设置都是：只有创建该 GitHub 仓库的人才有创建、编辑和删除文件的权限（*写权限（write access）*）。要让协作者获得项目的写权限，请进入“设置（Settings）”选项卡（{numref}`add-collab-01`）。

```{figure} img/version-control/add_collab_01.png
---
name: add-collab-01
---
GitHub 网页界面上的“设置”选项卡。
```

然后点击“管理访问权限（Manage access）”（{numref}`add-collab-02`）。

```{figure} img/version-control/add_collab_02.png
---
name: add-collab-02
---
GitHub 网页界面上的“管理访问权限”选项卡。
```

然后点击绿色的“邀请协作者（Invite a collaborator）”按钮（{numref}`add-collab-03`）。

```{figure} img/version-control/add_collab_03.png
---
name: add-collab-03
---
GitHub 网页界面上的“邀请协作者”按钮。
```

输入协作者的 GitHub 用户名或邮箱，名字出现时选中它（{numref}`add-collab-04`）。

```{figure} img/version-control/add_collab_04.png
---
name: add-collab-04
---
用于输入协作者 GitHub 用户名或邮箱的文本框。
```

最后，点击绿色的“添加 <COLLABORATORS_GITHUB_USER_NAME> 到本仓库（Add <COLLABORATORS_GITHUB_USER_NAME> to this repository）”按钮（{numref}`add-collab-05`）。

```{figure} img/version-control/add_collab_05.png
---
name: add-collab-05
---
GitHub 网页界面上把协作者添加到仓库的确认按钮。
```

完成之后，你应该能在“管理访问权限”选项卡下看到刚添加的协作者。他们应该会收到一封电子邮件邀请，邀请他们作为协作者加入该 GitHub 仓库。他们需要接受邀请，写权限才会生效。

### 用 Jupyter 从 GitHub 拉取更改

下面我们来看看如何用 Jupyter Git 扩展，把协作者对我们的分析文件 `eda.ipynb` 所做的更改拉取过来（{numref}`git-pull-00`）。

```{figure} img/version-control/git_pull_00.png
---
name: git-pull-00
---
GitHub 界面会显示最后向远程仓库推送提交的人的名字、对应提交信息的预览、唯一的提交标识符，以及该提交是在多久之前做的快照。
```

```{index} git; 拉取
```

在 Jupyter 中点击带向下箭头的云朵图标，就能让 Git 执行拉取（{numref}`git-pull-01`）。

```{figure} img/version-control/git_pull_01.png
---
name: git-pull-01
---
Jupyter Git 扩展的克隆按钮。
```

文件成功地从 GitHub 拉取之后，你需要点击“关闭（Dismiss）”才能继续工作（{numref}`git-pull-02`）。

```{figure} img/version-control/git_pull_02.png
---
name: git-pull-02
---
更改成功地从远程仓库拉取后出现的提示。
```

之后，打开（或刷新）刚刚拉取了更改的文件，就能看到这些更改（{numref}`git-pull-03`）。

```{figure} img/version-control/git_pull_03.png
---
name: git-pull-03
---
协作者对 `eda.ipynb` 所做的更改（代码处用红色箭头标出）。
```

查看项目更改的历史记录往往很有用。在 Jupyter 里，点击 Git 面板中的“历史（History）”，就能直接查看（{numref}`git-pull-04`）。

```{figure} img/version-control/git_pull_04.png
---
name: git-pull-04
---
用 Jupyter Git 扩展查看版本控制仓库历史。
```


在*每次*开始工作、动手修改本地副本之前，都先拉取更改，这是良好实践。如果没有这样做，而协作者已经把一些更改推送到 GitHub 上的项目里，那么在你拉取之前，就无法把自己的更改推送到 GitHub。出现这种情况时，可以通过 {numref}`merge-conflict-01` 中所示的报错信息来判断。

```{figure} img/version-control/merge_conflict_01.png
---
name: merge-conflict-01
---
该报错信息表示远程仓库上存在你本地没有的更改。
```

一般来说，摆脱这种局面并不太麻烦。首先，你需要拉取 GitHub 上已经存在、而本地仓库中还没有的更改。通常出现这种情况时，Git 能自动帮你合并更改，即使你和协作者改动的是同一个文件的不同位置！

但是，如果你和协作者修改了同一个文件的同一行，Git 就无法自动合并这些更改——它不知道该保留你那一（几）行、协作者那一（几）行，还是两者的某种混合。这时 Git 会提示某些文件存在合并冲突（{numref}`merge-conflict-03`）。

```{figure} img/version-control/merge_conflict_03.png
---
name: merge-conflict-03
---
该报错信息表示你和协作者修改了同一个文件的同一行，Git 无法自动合并这些更改。
```

### 处理合并冲突

```{index} git; 合并冲突
```

要解决合并冲突，你需要用纯文本编辑器打开出问题的文件，找出 Git 写在文件中的特殊标记，这些标记会告诉你合并冲突发生在哪里（{numref}`merge-conflict-04`）。


```{figure} img/version-control/merge_conflict_04.png
---
name: merge-conflict-04
---
在 Jupyter 中把笔记本以纯文本文件视图打开的方法。
```

合并冲突的起始处前面有 `<<<<<<< HEAD`，结束处则由 `>>>>>>>` 标出。在这些标记之间，Git 还插入一个分隔符（`=======`）。分隔符之前的那个版本是你的更改，分隔符之后的版本则是 GitHub 上原有的更改。在 {numref}`merge-conflict-05` 中可以看到，你的本地仓库里有一行代码把坐标轴标度设为 `"sqrt"`。看来协作者也修改了这一行，只不过把坐标轴标度设成了 `"log"`！

```{figure} img/version-control/merge_conflict_05.png
---
name: merge-conflict-05
---
合并冲突标记（用红色标出）。
```

决定保留哪个版本的更改（或者怎样的组合！）之后，你需要用纯文本编辑器删掉 Git 添加的特殊标记（{numref}`merge-conflict-06`）。

```{figure} img/version-control/merge_conflict_06.png
---
name: merge-conflict-06
---
合并冲突已解决的文件。
```

必须先保存该文件、把它添加到暂存区并提交，然后才能把更改推送到 GitHub。

### 用 GitHub 议题沟通

在团队中做项目时，你想要的并不只是“谁在什么时候改了项目中的哪个文件”这样的历史记录——你还想要把做过的决定、提出过的想法、发现并解决的问题，以及围绕项目的其他所有沟通都记录下来。电子邮件和即时通讯应用在日常沟通中都很常用，但它们并不是为针对具体项目的沟通而设计的：两者通常都没有按项目子话题组织对话、搜索与某个缺陷或软件版本有关的对话等功能。

```{index} GitHub; 议题
```

GitHub 的*议题*（issue）是电子邮件和即时通讯应用之外的另一种书面沟通媒介，专门为方便项目内的沟通而设计。议题从项目 GitHub 页面上的“议题（Issues）”选项卡*发起*，即使对话结束、议题被*关闭*，它们也会留在那里（与电子邮件不同，议题通常不会被删除）。通常每个话题建一个议题讨论串，用 GitHub 的搜索工具很容易找到它们。所有议题对所有协作者都可见，因此没有人会被排除在对话之外。最后，议题还可以设置成让团队成员在有人创建新议题或在议题讨论串中发帖时收到电子邮件通知。也可以直接从电子邮件回复议题。既然有这么多好处，我们强烈建议在项目沟通中使用议题。

要发起 GitHub 议题，先点击“议题”选项卡（{numref}`issue-01`）。

```{figure} img/version-control/issue_01.png
---
name: issue-01
---
GitHub 网页界面上的“议题”选项卡。
```

接着点击“新建议题（New issue）”按钮（{numref}`issue-02`）。

```{figure} img/version-control/issue_02.png
---
name: issue-02
---
GitHub 网页界面上的“新建议题”按钮。
```

填写议题标题（作用类似电子邮件的主题行），然后在较大的文本框中填写正文。最后点击“提交新议题（Submit new issue）”发布议题，与其他人分享（{numref}`issue-03`）。

```{figure} img/version-control/issue_03.png
---
name: issue-03
---
创建 GitHub 议题的对话框与提交按钮。
```

要回复别人发起的议题，可以在大文本框中写下你的回应，然后点击“评论（Comment）”（{numref}`issue-04`）。

```{figure} img/version-control/issue_04.png
---
name: issue-04
---
回复 GitHub 议题的对话框。
```


对话结束后，可以点击“关闭议题（Close issue）”。已关闭的议题以后可以通过“议题”选项卡中的“已关闭（Closed）”标题链接查看（{numref}`issue-06`）。

```{figure} img/version-control/issue_06.png
---
name: issue-06
---
GitHub 网页界面上的“已关闭”议题选项卡。
```

## 习题

本章所讲内容的练习题，可以在配套的[练习册仓库](https://worksheets.python.datasciencebook.ca)中“用版本控制协作（Collaboration with version control）”一行找到。点击“查看练习册（view worksheet）”，可以预览本章练习册的非交互版本。要交互式地完成这些习题，请按照练习册仓库中的说明下载全部练习册，并按照 {numref}`第 %s 章 <move-to-your-own-machine>` 中给出的计算机配置说明操作。这样才能确保练习册提供的自动反馈和指导按预期工作。

## 拓展资源

现在你已经掌握了 Git 和 GitHub 版本控制的基础知识，可以借助下面列出的资源进一步拓展：

- GitHub 的[指南网站](https://docs.github.com/)是深入学习 Git 和 GitHub 的绝佳资源。
- [《Good enough practices in scientific computing》](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510#sec014) {cite:p}`wilson2014best` 就数据分析项目中有用的工作流和“够用就好”的实践给出了更多建议。
- 除了 [GitHub](https://github.com)，还有 [GitLab](https://gitlab.com) 和 [BitBucket](https://bitbucket.org) 等其他流行的 Git 仓库托管平台。比较这些选项超出了本书的范围；在你成为更进阶的用户之前，一直用 GitHub 就完全没问题。只要知道你有别的选择就好！
- GitHub 关于创建个人访问令牌（personal access token）的[文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)是很好的补充资源，如果你在生成和使用个人访问令牌时需要帮助，可以查阅它。

+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```
