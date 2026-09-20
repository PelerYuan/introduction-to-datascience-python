+++

### 用铅笔工具（pen tool）在 GitHub 上编辑文件

```{index} GitHub; 铅笔工具
```

铅笔工具可以用来编辑已有的纯文本文件。点击铅笔工具，文件会打开在一个文本框中，你可以用键盘修改其中的内容（{numref}`pen-tool-01` 和 {numref}`pen-tool-02`）。

```{figure} img/version-control/pen-tool_01.png
---
name: pen-tool-01
---
点击铅笔工具会打开一个文本框，用来编辑纯文本文件。
```


```{figure} img/version-control/pen-tool_02.png
---
name: pen-tool-02
---
点击铅笔工具后可以修改内容的文本框。
```

```{index} GitHub; 提交
```

修改完成后，可以通过*提交*更改把它们“保存”下来。在仓库中*提交文件*时，版本控制系统会为这个文件当时的样子拍一张快照（snapshot）。随着项目不断推进，你可能会对同一个文件做出许多次提交，这就为该文件生成了一份有用的版本历史。在 GitHub 上，点击绿色的“提交更改（Commit changes）”按钮，就会保存文件并完成一次提交（{numref}`pen-tool-03`）。

回想 {numref}`commit-changes` 讲过的内容：通常必须先把文件加入暂存区，然后才能提交。那么直接在 GitHub 上操作时，为什么不必这么做呢？因为在幕后，你点击绿色的“提交更改”按钮时，GitHub 确实在提交之前把这个文件加入了暂存区。不过请注意，在 GitHub 上一次只能提交一个文件的更改。而在自己的本地仓库中工作时，你可以同时提交多个文件的更改。如果项目的一次“改进”要改动多个文件，这一点尤其有用。在本地仓库中工作时，你还能运行代码，这在 GitHub 上是做不到的。一般来说，在 GitHub 上编辑只适合对纯文本文件做小幅修改。

```{figure} img/version-control/pen-tool_03.png
---
name: pen-tool-03
---
用铅笔工具保存更改时，必须提交这些更改并附上相应的提交信息。
```

### 用“添加文件（Add file）”菜单在 GitHub 上创建文件

```{index} GitHub; 添加文件
```

“添加文件”菜单可以用来创建新的纯文本文件，也可以从你的电脑上传文件。要新建纯文本文件，请点击“添加文件”下拉菜单，选择“新建文件（Create new file）”选项（{numref}`create-new-file-01`）。

```{figure} img/version-control/create-new-file_01.png
---
name: create-new-file-01
---
新的纯文本文件可以直接在 GitHub 上创建。
```

```{index} markdown
```

页面打开后，会有一个填写文件名的小文本框，还有一个填写文件内容的大文本框。注意“编辑新文件（Edit new file）”和“预览（Preview）”这两个标签页。在两者之间切换，就能分别输入、编辑文本，以及查看文本渲染后的样子（{numref}`create-new-file-02`）。GitHub 能够识别并渲染 `.md` 文件，它使用的 markdown 语法与 Jupyter 笔记本非常相似，所以“预览”标签页对检查 markdown 代码是否正确特别有帮助。

```{figure} img/version-control/create-new-file_02.png
---
name: create-new-file-02
---
新建纯文本文件时，需要在红圈标出的文本框中填写文件名，并在较大的文本框中填写文件内容（红色箭头）。
```

点击页面底部绿色的“提交更改”按钮，即可保存并提交你的更改（{numref}`create-new-file-03`）。

```{figure} img/version-control/create-new-file_03.png
---
name: create-new-file-03
---
新建的文件必须连同相应的提交信息一起提交，才能保存下来。
```

你也可以用“添加文件”下拉菜单，选择“上传文件（Upload files）”，把在本地电脑上创建的文件上传上去（{numref}`upload-files-01`）。要从本地电脑选择要上传的文件，你可以把它们拖放到 {numref}`upload-files-02` 所示的灰色方框区域，也可以点击“选择文件（choose your files）”链接，打开文件浏览对话框。选好要上传的文件后，点击页面底部绿色的“提交更改”按钮（{numref}`upload-files-02`）。

```{figure} img/version-control/upload-files_01.png
---
name: upload-files-01
---
任何类型的新文件都可以上传到 GitHub。
```

```{figure} img/version-control/upload-files_02.png
---
name: upload-files-02
---
将要上传的文件拖入 GitHub 网站（红圈处），或者点击“选择文件”，即可指定要上传的文件。上传的文件同样必须连同相应的提交信息一起提交。
```


请注意，Git 和 GitHub 的设计目标是跟踪单个文件的变化。**不要**把整个项目打包成一个归档文件（例如 `.zip`）上传。如果这样做，Git 就只能跟踪整个 `.zip` 文件的变化，而这样的变化是人无法阅读的。提交一个大归档文件，会让版本控制完全失去意义：你将无法查看、解读或找到项目任何实际内容在历史中的变化！

(local-repo-jupyter)=
## 使用 Jupyter 处理本地仓库

```{index} git;Jupyter 扩展
```

虽然在 GitHub 上有好几种创建和编辑文件的方式，但它们的能力都不足以高效地创建和编辑复杂文件，也不足以处理那些需要运行之后才能判断是否可用的文件（例如包含代码的文件）。比如，你没法直接在 GitHub 上运行用 Python 代码写的分析。因此，把在 GitHub 上创建的远程仓库连接到本地的编程环境会很有用。做法就是创建这份仓库的本地副本，并在其中工作。本章我们重点讲如何借助 Jupyter Git 扩展在 Jupyter 中使用 Git。这个扩展既可以由你本地电脑上的 Jupyter 运行，也可以在 JupyterHub 服务器上运行。建议你先阅读 {numref}`第 %s 章 <getting-started-with-jupyter>`，学会使用 Jupyter 之后再读本章。

### 生成 GitHub 个人访问令牌（personal access token）

```{index} GitHub; 个人访问令牌
```

要在本地仓库与 GitHub 上的远程仓库之间发送和取回工作内容，你需要经常向 GitHub 进行身份验证，以证明自己拥有所需权限。做法有好几种，但对初学者，我们推荐使用 HTTPS 方式，因为它更简单，需要做的配置也更少。要使用 HTTPS 方式，GitHub 要求你提供一个*个人访问令牌*。个人访问令牌就像密码一样——所以要保密！——不过它能让你更精细地控制令牌可以访问账户的哪些部分，还能为身份验证设置到期日期。要生成个人访问令牌，首先必须访问 [https://github.com/settings/tokens](https://github.com/settings/tokens)，它会带你进入账户设置中的“个人访问令牌（Personal access tokens）”页面。进入该页面后，点击“生成新令牌（Generate new token）”（{numref}`generate-pat-01`）。注意，接下来可能会要求你用用户名和密码重新进行身份验证，才能继续。


```{figure} img/version-control/generate-pat_01.png
---
name: generate-pat-01
---
用于发起创建新个人访问令牌的“生成新令牌”按钮。它位于账户设置的“开发者设置（Developer settings）”页面中的“个人访问令牌”部分。
```


系统会要求你添加一段说明，描述这个个人访问令牌的用途。接下来，你需要为令牌选择权限；在这里你可以控制令牌能访问账户的哪些部分。请务必只勾选你确实需要的权限。在 {numref}`generate-pat-02` 中，我们只勾选了“repo”方框，这样令牌就能访问我们的仓库（以便推送和拉取），而无法访问 GitHub 账户的其他任何功能。最后，把页面滚动到底部，点击绿色的“生成令牌（Generate token）”按钮，即可生成令牌（{numref}`generate-pat-02`）。

```{figure} img/version-control/generate-pat_02.png
---
name: generate-pat-02
---
创建新个人访问令牌的网页。
```


最后，你会进入一个页面，可以在这里查看并复制刚刚生成的个人访问令牌（{numref}`generate-pat-03`）。由于令牌能访问你账户的某些部分，你应该把它当作密码来对待；例如，可以考虑用密码管理器把它（以及你的其他密码和令牌！）安全地保存起来。请注意，这个页面只会向你显示一次令牌，所以务必马上把它存到安全的地方。万一你不小心忘了保存，也不用着急——点击令牌旁边的“删除（Delete）”按钮就能删掉它，然后重新生成一个。想进一步了解 GitHub 身份验证，请参阅本章末尾的拓展资源部分。

```{figure} img/version-control/generate-pat_03.png
---
name: generate-pat-03
---
刚刚生成的个人访问令牌的显示界面。
```

### 使用 Jupyter 克隆仓库

```{index} git;克隆
```

从 GitHub *克隆*远程仓库、建立本地副本之后，这份副本知道自己是从哪里来的，因此也知道该把新提交的修改发送到哪里、从哪里接收。为此，先在 GitHub 上打开“代码（Code）”下拉菜单，从 HTTPS 标签页复制 URL（{numref}`clone-02`）。

```{figure} img/version-control/clone_02.png
---
name: clone-02
---
绿色的“代码”下拉菜单中包含与 GitHub 远程仓库位置对应的远程地址（URL）。
```

打开 Jupyter，点击文件浏览器标签页上的 Git+ 图标（{numref}`clone-01`）。

```{figure} img/version-control/clone_01.png
---
name: clone-01
---
Jupyter Git 克隆图标（红圈处）。
```



粘贴你创建的 GitHub 项目仓库的 URL，然后点击蓝色的“克隆（CLONE）”按钮（{numref}`clone-03`）。

```{figure} img/version-control/clone_03.png
---
name: clone-03
---
Jupyter 中要求输入 GitHub 仓库远程地址（URL）的提示框。
```

现在，文件浏览器标签页上会出现该仓库的文件夹。文件夹里放着 GitHub 上原有的所有文件（{numref}`clone-04`）。

```{figure} img/version-control/clone_04.png
---
name: clone-04
---
克隆得到的 GitHub 仓库可以在 Jupyter 文件浏览器中查看和访问。
```


### 指定要提交的文件
现在你已经把 GitHub 上的远程仓库克隆成了本地仓库，接下来就可以编辑、创建和删除文件了。例如，假设你新建并保存了一个文件（名为 `eda.ipynb`），想把它送回 GitHub 上的项目仓库（{numref}`git-add-01`）。要把这个改动过的文件“添加”到暂存区（也就是标记这个文件是我们想要提交其更改的文件），请点击 Jupyter 最左侧的 Jupyter Git 扩展图标（{numref}`git-add-01`）。

```{figure} img/version-control/git_add_01.png
---
name: git-add-01
---
Jupyter Git 扩展图标（红圈标出）。
```

```{index} git;添加
```


这会打开 Jupyter Git 图形用户界面面板。接下来，点击想要“添加”的文件旁边的加号（+）（{numref}`git-add-02`）。注意，由于这是该文件的第一次改动，它出现在“未跟踪（Untracked）”分组下。不过下次你再编辑这个文件并想添加更改时，会在“已修改（Changed）”分组下找到它。

你还会在“未跟踪”分组下看到一个 `eda-checkpoint.ipynb` 文件。这是你在编辑 `eda.ipynb` 时由 Jupyter 创建的临时“检查点文件（checkpoint file）”。一般来说，不要把自动生成的文件添加到 Git 仓库中；只添加你自己直接创建和编辑的文件。

```{figure} img/version-control/git_add_02.png
---
name: git-add-02
---
用加号（+）把 `eda.ipynb` 加入暂存区。
```

点击加号（+）会把文件从“未跟踪”分组移到“已暂存（Staged）”分组，这样 Git 就知道你想把文件当前的状态拍成快照，作为一次提交（{numref}`git-add-03`）。现在你可以“提交”这些更改了。记得写一句（清楚、有用的！）说明，讲清改动了什么，好让你的协作者（以及未来的你）了解这次提交做了什么。


```{figure} img/version-control/git_add_03.png
---
name: git-add-03
---
把 `eda.ipynb` 添加进去之后，它就会出现在暂存区中。
```


### 完成提交

```{index} git;提交
```

要把更改连同相应的提交信息保存为快照，你必须在 Git 面板底部的文本框中填写一条信息，然后点击蓝色的“提交（Commit）”按钮（{numref}`git-commit-01`）。强烈建议写下有用、有意义的信息，说明改动了什么。今后如果需要查看或取回文件的某个历史版本，或者把项目回退到更早的状态，这些提交信息以及每次提交的日期时间戳就是浏览项目历史的主要依据。第一次点击“提交”按钮时，系统会提示你输入姓名和电子邮件。每台使用 Git 的机器只需设置一次。

```{figure} img/version-control/git_commit_01.png
---
name: git-commit-01
---
必须先在 Jupyter Git 扩展的提交文本框中填写提交信息，才能用蓝色的提交按钮记录这次提交。
```

“提交”文件之后，你会看到“已暂存”文件的数目是 0。现在你可以把更改推送到 GitHub 上的远程仓库了（{numref}`git-commit-03`）。

```{figure} img/version-control/git_commit_03.png
---
name: git-commit-03
---
记录一次提交之后，暂存区应该是空的。
```

### 把提交推送到 GitHub

```{index} git;推送
```

要把已提交的更改送回 GitHub 上的远程仓库，你需要*推送*它们。做法是点击 Jupyter Git 标签页上带向上箭头的云朵图标（{numref}`git-push-01`）。

```{figure} img/version-control/git_push_01.png
---
name: git-push-01
---
Jupyter Git 扩展的“推送”按钮（红圈处）。
```

然后系统会提示你输入 GitHub 用户名，以及你之前生成的个人访问令牌（不是你的账户密码！）。点击蓝色的“确定（OK）”按钮，开始推送（{numref}`git-push-02`）。

```{figure} img/version-control/git_push_02.png
---
name: git-push-02
---
输入你的 Git 凭据，以授权向远程仓库推送。
```

如果文件成功推送到了 GitHub 上的项目仓库，你会看到一条成功提示（{numref}`git-push-03`）。点击“忽略（Dismiss）”即可继续在 Jupyter 中工作。

```{figure} img/version-control/git_push_03.png
---
name: git-push-03
---
提示推送成功的信息。
```

如果你访问 GitHub 上的远程仓库，会看到这些更改现在也出现在那里了（{numref}`git-push-04`）！

```{figure} img/version-control/git_push_04.png
---
name: git-push-04
---
GitHub 网页界面会显示提交信息的预览，以及每个文件最近一次推送的提交时间。
```