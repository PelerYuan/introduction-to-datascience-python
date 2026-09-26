# -*- coding: utf-8 -*-
"""Apply the round-5 review batch. Every edit asserts its own occurrence count, so a
mismatch stops the run instead of half-applying changes."""
import pathlib

SRC = pathlib.Path("source")


def sub(fn, old, new, n=1):
    p = SRC / fn
    t = p.read_text(encoding="utf-8")
    c = t.count(old)
    assert c == n, "%s: expected %d of %r, found %d" % (fn, n, old[:40], c)
    p.write_text(t.replace(old, new), encoding="utf-8")
    print("OK  %-22s %dx %s" % (fn, c, old[:34]))


def note(fn, anchor, text):
    """Append a translator note right after the sentence the anchor ends."""
    sub(fn, anchor, anchor + text)


# A. mechanical replacements
sub("inference.md", "样本分布", "样本数据分布", 5)
sub("classification1.md", "### 多于两个解释变量", "### 多于两个预测变量")
sub("wrangling.md", "`string` 类型用来表示", "`str` 类型用来表示")
sub("regression1.md", "root mean square prediction error", "root mean squared prediction error")
sub("viz.md", "km/sec", "千米/秒", 2)

# B. sentence rewrites
sub("regression2.md",
    "在线性回归中，离群值指的是到最优拟合直线的纵向距离比根据其余数据所能预期的要大得多或小得多的点。",
    "在线性回归中，离群值指的是在纵向上比根据其余数据所预期的位置高出或低出很多的点。")
sub("inference.md", "所以不会再次抽到完全相同的样本取值。", "所以一般不会再次抽到完全相同的样本取值。")
sub("clustering.md",
    "我们开始 K 均值聚类算法，先选定 K，再把数量大致相等的观测随机分配到这 K 个簇中。",
    "运行 K 均值聚类算法时，先选定 K，再把数量大致相等的观测随机分配到这 K 个簇中。")
sub("clustering.md", "在本课程中，聚类只用于探索性分析", "在本书中，聚类只用于探索性分析")

# C. static output blocks: to_list() returns a list, not a numpy array
sub("classification2.md", "array([2, 9, 6, 4, 0, 3, 1, 7, 8, 5])", "[2, 9, 6, 4, 0, 3, 1, 7, 8, 5]")
sub("classification2.md", "array([9, 5, 3, 0, 8, 4, 2, 1, 6, 7])", "[9, 5, 3, 0, 8, 4, 2, 1, 6, 7]")

# D. translator notes (no backticks: the inline-code multiset is compared exactly)
note("wrangling.md", "这种写法总是行得通。",
     "（译注：原文对报错原因的解释并不准确。在 pandas 中，“df[\"a\":\"b\"]”这种写法是按行标签切片，"
     "而不是选取列范围；本例的行索引是整数 RangeIndex，所以会直接抛出 TypeError，"
     "与选出的列是否包含 region 无关。要按列名选取一段范围，应使用 “.loc[:, \"most_at_home\":\"lang_known\"]”。）")
note("viz.md", "当年迈克尔逊和莫雷的实验首次证明光速是有限的。",
     "（译注：此说有误。光速有限最早由罗默于 1676 年根据木卫食的观测推断得出；"
     "本节数据来自迈克尔逊 1879 年独自完成的光速精密测量，"
     "而迈克尔逊与莫雷合作的是 1887 年检验以太漂移的实验。）")
note("classification2.md", "我们再次得到相同的数字列表。",
     "（译注：to_list() 返回的是 Python 列表，原文此处把输出误写成了 array([...])，译文已改为列表形式。）")
note("inference.md", "高于或低于真实总体比例的可能性大致相同。",
     "（译注：严格来说，无偏只保证抽样分布的均值等于总体参数，并不保证高估和低估的概率各占一半；"
     "后者还要求抽样分布关于总体参数大致对称。本例中比例的抽样分布接近对称，因此这一说法近似成立。）")
print("ALL ROUND-5 EDITS APPLIED")