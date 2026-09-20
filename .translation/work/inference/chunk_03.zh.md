+++

1. 从取自总体的原始样本中随机选取一个观测。
2. 记录这个观测的取值。
3. 把这个观测放回样本。
4. 重复第 1 至第 3 步（*有放回*地抽样），直到得到 $n$ 个观测，它们构成一个自助样本。
5. 计算自助样本中这 $n$ 个观测的自助点估计（例如均值、中位数、比例、斜率等）。
6. 重复第 1 至第 5 步很多次，得到点估计的分布（即自助分布）。
7. 计算观测到的点估计附近的合理取值范围。

+++

```{figure} img/inference/intro-bootstrap.jpeg
:name: fig:11-intro-bootstrap-image

自助法流程概览。
```

+++

### 用 Python 实现自助法

我们接着用 Airbnb 的例子，说明如何只靠从总体中抽出的一个样本，构造并使用自助分布。
仍然假设我们想估计加拿大温哥华所有 Airbnb 房源每晚价格的总体均值，而手头只有一个
样本量为 40 的样本。回想一下，我们的点估计是 \${glue:text}`estimate_mean`。样本中价格的
直方图见图 {numref}`fig:11-bootstrapping1`。

```{code-cell} ipython3
one_sample
```

```{code-cell} ipython3
:tags: ["remove-output"]
one_sample_dist = alt.Chart(one_sample).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()").title("Count"),
)

one_sample_dist
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping1", one_sample_dist)
```

:::{glue:figure} fig:11-bootstrapping1
:name: fig:11-bootstrapping1

样本量为 40 的一个样本中每晚价格（美元）的直方图。
:::

+++

该样本的直方图是偏斜的，有少数几个观测落在右侧较远处。样本均值为 \${glue:text}`estimate_mean`。
请记住，在实践中，我们通常只有从总体中抽到的这一个样本。所以这个样本和这个估计值
就是我们能使用的全部数据。

```{index} 自助法; 在 Python 中, 数据框; 样本（自助）
```

现在我们在 Python 中执行上面列出的第 1 至第 5 步，生成一个自助样本，并据此算出
点估计。我们继续使用数据框的 `sample` 函数。这里有一点很关键：我们把 `frac=1`
（即“fraction”，比例）设为 1，表示想抽取的条数与数据框的行数同样多（也可以设
`n=40`，但那样就得自己留意数据框里有多少行）。由于做自助法需要有放回抽样，
所以要把 `replace` 参数改成 `True`。

```{code-cell} ipython3
:tags: ["remove-output"]

boot1 = one_sample.sample(frac=1, replace=True)
boot1_dist = alt.Chart(boot1).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=30)
        .title("Price per night (dollars)"),
    y=alt.Y("count()", title="Count"),
)

boot1_dist
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping3", boot1_dist)
```

:::{glue:figure} fig:11-bootstrapping3
:name: fig:11-bootstrapping3

自助分布。
:::

```{code-cell} ipython3
boot1["price"].mean()
```

从 {numref}`fig:11-bootstrapping3` 中可以看到，自助样本的直方图与原始样本的直方图
形状相似。虽然两个分布的形状相近，但并不完全相同。你还会发现，原始样本的均值
与自助样本的均值不一样。这是怎么发生的呢？请记住，我们是从原始样本中有放回地
抽样，所以不会再次抽到完全相同的样本取值。我们是在*假装*这一个样本与总体很接近，
并通过从原始样本中再抽一个样本，来模拟从总体中再抽一个样本。

现在我们用原始样本（`one_sample`）生成 20,000 个自助样本，并计算每个重复的均值。
要记住，这样做的前提是 `one_sample` *看起来像*原始总体；但既然我们拿不到总体本身，
这通常已经是我们能做的最好的选择了。请注意，这里把列表推导式拆成了多行，
以便阅读。

```{code-cell} ipython3
boot20000 = pd.concat([
    one_sample.sample(frac=1, replace=True).assign(replicate=n)
    for n in range(20_000)
])
boot20000
```

我们来看看自助样本前六次重复的直方图。

```{code-cell} ipython3
:tags: ["remove-output"]

six_bootstrap_samples = boot20000.query("replicate < 6")
six_bootstrap_fig = alt.Chart(six_bootstrap_samples, height=150).mark_bar().encode(
    x=alt.X("price")
        .bin(maxbins=20)
        .title("Price per night (dollars)"),
    y=alt.Y("count()").title("Count")
).facet(
    "replicate:N",  # Recall that `:N` converts the variable to a categorical type
    columns=2
)
six_bootstrap_fig
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping-six-bootstrap-samples", six_bootstrap_fig)
```

:::{glue:figure} fig:11-bootstrapping-six-bootstrap-samples
:name: fig:11-bootstrapping-six-bootstrap-samples

自助样本前六次重复的直方图。
:::

+++

从 {numref}`fig:11-bootstrapping-six-bootstrap-samples` 中可以看到，各个自助样本的分布
有何不同。如果分别计算这六个样本的样本均值，会发现它们彼此也不相同。要计算每个
样本的均值，我们先按“replicate”分组，这一列记录的是样本/重复编号。然后计算
`price` 列的均值，并把它重命名为 `mean_price`，让名字更有描述性。最后用 `reset_index`
把 `replicate` 的取值变回数据框中的一列。

```{code-cell} ipython3
(
    six_bootstrap_samples
    .groupby("replicate")
    ["price"]
    .mean()
    .reset_index()
    .rename(columns={"price": "mean_price"})
)
```

自助样本之间的分布和均值之所以不同，是因为我们采用了*有放回*抽样。如果改成
*无放回*抽样，那么每次得到的样本取值都会完全一样。

接下来，我们为这 20,000 个自助样本分别计算均值的点估计，并由此得到这些点估计的
自助分布。自助分布（{numref}`fig:11-bootstrapping5`）可以提示我们，如果取多个样本，
点估计会有怎样的表现。

```{index} DataFrame;reset_index, DataFrame;rename, DataFrame;groupby, Series;mean
```

```{code-cell} ipython3
boot20000_means = (
    boot20000
    .groupby("replicate")
    ["price"]
    .mean()
    .reset_index()
    .rename(columns={"price": "mean_price"})
)

boot20000_means
```

```{code-cell} ipython3
:tags: ["remove-output"]

boot_est_dist = alt.Chart(boot20000_means).mark_bar().encode(
    x=alt.X("mean_price")
        .bin(maxbins=20)
        .title("Sample mean price per night (dollars)"),
    y=alt.Y("count()").title("Count"),
)

boot_est_dist
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping5", boot_est_dist)
```

:::{glue:figure} fig:11-bootstrapping5
:name: fig:11-bootstrapping5

自助样本均值的分布。
:::

+++

我们来比较自助分布——由大小为 40 的原始样本反复抽样构造而来——与真实的抽样
分布——相当于从总体中反复抽样。

```{code-cell} ipython3
:tags: [remove-cell]

sampling_distribution.encoding.x["bin"]["extent"] = (90, 250)
bootstr6fig = alt.vconcat(
    alt.layer(
        sampling_distribution,
        alt.Chart(sample_estimates).mark_rule(color="black", size=1.5, strokeDash=[6]).encode(x="mean(mean_price)"),
        alt.Chart(sample_estimates).mark_text(color="black", size=12, align="left", dx=16, fontWeight="bold").encode(
            x="mean(mean_price)",
            y=alt.value(7),
            text=alt.value(f"Mean = {sampling_distribution['data']['mean_price'].mean().round(1)}")
        )
    ).properties(title="Sampling distribution", height=150),
    alt.layer(
        boot_est_dist,
        alt.Chart(boot20000_means).mark_rule(color="black", size=1.5, strokeDash=[6]).encode(x="mean(mean_price)"),
        alt.Chart(boot20000_means).mark_text(color="black", size=12, align="left", dx=18, fontWeight="bold").encode(
            x="mean(mean_price)",
            y=alt.value(7),
            text=alt.value(f"Mean = {boot_est_dist['data']['mean_price'].mean().round(1)}")
        )
    ).properties(title="Bootstrap distribution", height=150)
)
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping6", bootstr6fig)
```

:::{glue:figure} fig:11-bootstrapping6
:name: fig:11-bootstrapping6

自助样本均值的分布与抽样分布的比较。
:::



```{code-cell} ipython3
:tags: [remove-cell]

glue("one_sample_mean", "{:.2f}".format(one_sample["price"].mean()))
```

```{index} 抽样分布; 与自助分布的比较
```

从 {numref}`fig:11-bootstrapping6` 中我们可以得到两个要点。第一，真实抽样分布与
自助分布的形状和离散程度相似；自助分布能帮助我们体会点估计的变异性。第二个要点
是：这两个分布的均值略有不同。抽样分布的中心是总体均值
\${glue:text}`population_mean`。而自助分布的中心是原始样本中每晚价格的平均值
\${glue:text}`one_sample_mean`。由于我们不断从原始样本中重抽样，可以看到自助分布
的中心落在原始样本的均值上（样本均值的抽样分布则不同，它的中心是总体参数的
取值）。

{numref}`fig:11-bootstrapping7` 总结了自助法的流程。这里的思路是：当我们只有
一个样本时，可以用自助样本均值的分布来近似样本均值的抽样分布。既然自助分布能
相当好地近似抽样分布的离散程度，我们就可以借助自助分布的离散程度，结合点估计
给出总体参数的合理取值范围！

```{figure} img/inference/11-bootstrapping7-1.png
:name: fig:11-bootstrapping7

自助法流程总结。
```

+++

### 用自助法计算合理取值范围

```{index} 置信区间
```

现在我们已经构造出自助分布，接下来用它来算出一个近似的 95\% 百分位数自助置信区间
（percentile bootstrap confidence interval）。**置信区间**是总体参数的合理取值范围。
我们要找出覆盖自助分布中间 95\% 的那一段取值，这样就得到了 95\% 置信区间。你也许
会问：“95\% 置信”是什么意思？如果我们抽取 100 个随机样本，算出 100 个 95\% 置信
区间，那么其中大约 95\% 的区间会覆盖总体参数的取值。请注意，95\% 这个数并没有什么
特别之处，我们也可以用其他水平，比如 90\% 或 99\%。置信水平与精度之间存在权衡：
置信水平越高，区间越宽；置信水平越低，区间越窄。因此，选择哪个水平取决于我们
愿意承担多大的出错概率，而这又取决于出错对我们的应用会有什么后果。一般来说，
我们选定的置信水平，既要让自己对不确定性感到安心，又不能严格到让区间失去用处。
例如，如果我们的决策会影响人的生命，一旦出错后果致命，那我们可能希望很有把握，
于是选择更高的置信水平。

要计算 95\% 百分位数自助置信区间，我们按下面的步骤来做：

1. 把自助分布中的观测按从小到大的顺序排列。
2. 找出这样的取值：有 2.5\% 的观测落在它以下（即第 2.5 百分位数）。把这个取值作为区间的下限。
3. 找出这样的取值：有 97.5\% 的观测落在它以下（即第 97.5 百分位数）。把这个取值作为区间的上限。

要在 Python 中完成这些步骤，我们可以用 DataFrame 的 `quantile` 函数。分位数用比例
而不是百分数表示，所以第 2.5 百分位数和第 97.5 百分位数分别对应 0.025 和 0.975
分位数。

```{index} DataFrame; [], DataFrame;quantile
```

```{index} 百分位数
```

```{code-cell} ipython3
ci_bounds = boot20000_means["mean_price"].quantile([0.025, 0.975])
ci_bounds
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("ci_lower", "{:.2f}".format(ci_bounds[0.025]))
glue("ci_upper", "{:.2f}".format(ci_bounds[0.975]))
```

我们的区间，从 \${glue:text}`ci_lower` 到 \${glue:text}`ci_upper`，覆盖了自助分布中
样本均值价格居中的 95\%。我们可以在 {numref}`fig:11-bootstrapping9` 中把这个
区间画在分布上。

```{code-cell} ipython3
:tags: [remove-cell]
# Create the annotation for for the 2.5th percentile
rule_025 = alt.Chart().mark_rule(color="black", size=1.5, strokeDash=[6]).encode(
    x=alt.datum(ci_bounds[0.025])
).properties(
    width=500
)
text_025 = rule_025.mark_text(
    color="black",
    size=12,
    fontWeight="bold",
    dy=-160
).encode(
    text=alt.datum(f"2.5th percentile ({ci_bounds[0.025].round(1)})")
)

# Create the annotation for for the 97.5th percentile
text_975 = text_025.encode(
    x=alt.datum(ci_bounds[0.975]),
    text=alt.datum(f"97.5th percentile ({ci_bounds[0.975].round(1)})")
)
rule_975 = rule_025.encode(x=alt.datum(ci_bounds[0.975]))

# Layer the annotations on top of the distribution plot
bootstr9fig = boot_est_dist + rule_025 + text_025 + rule_975 + text_975
```

```{code-cell} ipython3
:tags: ["remove-cell"]

glue("fig:11-bootstrapping9", bootstr9fig)
```

:::{glue:figure} fig:11-bootstrapping9
:name: fig:11-bootstrapping9

带百分位数上下限的自助样本均值分布。
:::



+++

要完成对总体参数的估计，我们需要报告点估计以及置信区间的下限和上限。这里 40 个
Airbnb 房源每晚价格的样本均值为 \${glue:text}`one_sample_mean`，而我们有 95\% 的
“把握”认为，温哥华所有 Airbnb 房源每晚价格的真实总体均值介于
\${glue:text}`ci_lower` 和 \${glue:text}`ci_upper` 之间。可以看到，我们的区间确实
覆盖了真实的总体均值 \${glue:text}`population_mean`\! 不过在实践中，我们并不知道
自己的区间有没有覆盖总体参数，因为我们通常只有一个样本，而不是整个总体。
只有一个样本时，这已经是我们能做到的最好结果了！

本章只是统计推断之旅的开端。我们可以把这里学到的概念推广出去，做远远不止于
报告点估计和置信区间的事情，比如检验总体之间是否存在真实差异、检验变量之间
是否有关联，等等。我们才刚刚触及统计推断的表面；不过，本章介绍的内容会成为
你今后学习更高级统计方法的基础！

+++

## 习题

本章内容的配套练习题见[练习册仓库](https://worksheets.python.datasciencebook.ca)中
“Statistical inference”（统计推断）那两行。点击“查看练习册”（view worksheet）
即可预览本章每份练习册的非交互版本。若要交互式地做这些习题，请按照练习册仓库中的
说明下载全部练习册，并按 {numref}`第 %s 章 <move-to-your-own-machine>` 中给出的
计算机环境配置说明操作。这样才能确保练习册提供的自动反馈与指导按预期正常工作。

+++

## 拓展资源

- 《OpenIntro Statistics》 {cite:p}`openintro` 的第 4 至第 7 章
  在进一步学习统计推断时，是一个不错的进阶选择。虽然它无疑仍是一部入门教材，
  但这里的内容会更偏数学一些。视你的基础而定，你也许反而应该先读第 1 至第 3 章，
  那里会讲到概率论的一些基本概念。概率论看似偏离主题，其实它正是*统计学的语言*；
  如果对概率有扎实的掌握，更高阶的统计学对你来说就会水到渠成！

+++

## 参考文献

```{bibliography}
:filter: docname in docnames
```

<<TERM>>
original sample = 原始样本
<<END>>