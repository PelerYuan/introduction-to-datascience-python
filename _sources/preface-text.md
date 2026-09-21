---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# 前言

```{index} 数据科学; 定义, 可审核, 可复现
```

本教材旨在成为一本平易近人的数据科学入门读物。在本书中，我们把**数据科学**定义为：借助**可复现**、**可审核**的流程，从数据中提炼洞见的过程。如果你分析了某些数据，并把分析交给朋友或同事，他们应当能够从头到尾重新运行这项分析，并得到与你相同的结果（*可复现性*）。他们还应当能够看到并理解分析中的每一个步骤，以及这项分析一步步发展成型的来龙去脉（*可审核性*）。做出可复现、可审核的分析，你和别人就都能轻松复查并验证你的工作。

概括而言，在本书中你将学会：

1. 识别数据科学中的常见问题，以及
2. 用可复现、可审核的工作流解决这些问题。

{numref}`preface-overview-fig` 概括了你在本书各章会学到的内容。贯穿全书，你将学会用 [Python 编程语言](https://www.python.org/)完成数据分析的各项任务。前四章，你将学习如何用 Python 读取、清洗、整理（即把数据重新组织成可用的格式）和可视化数据，同时回答描述性与探索性的数据分析问题。接下来的六章，你将学习如何用数据科学中的常见方法回答预测性、探索性和推断性的数据分析问题，这些方法包括分类、回归、聚类和估计。最后几章，你将学习如何用 Jupyter 把 Python 代码、带格式的文本和图片整合成一份连贯的文档，如何用版本控制开展协作，以及如何在自己的计算机上安装并配置数据科学所需的软件。如果你是在修读一门课程时使用本书，授课教师可能已经为你把这些工具都配置好了；这种情况下，你只要按顺序逐章读下去即可。但如果你是自学本书，不妨先跳到最后三章，确认自己的计算机已经配置妥当，能够运行我们在全书各处给出的示例代码，然后再继续往下读。

```{figure} img/frontmatter/chapter_overview.png
---
name: preface-overview-fig
---
我们将去向何方？
```


本书每一章都配有练习册（worksheet），其中的习题可以帮助你练习即将学到的概念。我们强烈建议你先把每一章的练习册做完，再进入下一章。所有练习册都可以在 [https://worksheets.python.datasciencebook.ca](https://worksheets.python.datasciencebook.ca) 获取；每章末尾的“习题”一节会指向该章对应的练习册。对每一份练习册，你都可以点击“查看练习册”预览它的非交互版本。如果想以交互方式做习题，请按照练习册仓库中的说明下载所有练习册，再按照{numref}`第 %s 章 <move-to-your-own-machine>`中的计算机配置说明操作。这样才能保证练习册提供的自动反馈和指导按预期正常工作。
