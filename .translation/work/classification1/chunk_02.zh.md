+++

:::{glue:figure} fig:05-knn-4
:name: fig:05-knn-4

凹度与周长的散点图。新观测用红色菱形表示，并有一条连线接向离它最近的那一个近邻，该近邻的标签为良性。
:::

```{code-cell} ipython3
:tags: [remove-cell]

# The index of 3 rows that has smallest distance to the new point
min_3_idx = np.argpartition(my_distances2, 3)[:3]
near_neighbor_df3 = pd.concat([
    cancer.loc[[min_3_idx[1]], attrs],
    perim_concav_with_new_point_df2.loc[[cancer.shape[0]], attrs],
])
near_neighbor_df4 = pd.concat([
    cancer.loc[[min_3_idx[2]], attrs],
    perim_concav_with_new_point_df2.loc[[cancer.shape[0]], attrs],
])
```


```{code-cell} ipython3
:tags: [remove-cell]

line3 = alt.Chart(near_neighbor_df3).mark_line().encode(
    x="Perimeter",
    y="Concavity",
    color=alt.value("black")
)
line4 = alt.Chart(near_neighbor_df4).mark_line().encode(
    x="Perimeter",
    y="Concavity",
    color=alt.value("black")
)
glue("fig:05-knn-5", (perim_concav_with_new_point2 + line2 + line3 + line4), display=True)
```


为了提高预测效果，我们可以考虑离新观测最近的若干个邻点，比如取 $K = 3$，用它们来预测新观测的诊断类别。在这 3 个最近的邻点中，我们取*多数类*作为新观测的预测结果。如 {numref}`fig:05-knn-5` 所示，新观测的 3 个最近邻中有 2 个的诊断结果是恶性。因此我们采用多数投票，把这个新的红色菱形观测判为恶性。

+++

:::{glue:figure} fig:05-knn-5
:name: fig:05-knn-5

带三个最近邻的凹度与周长散点图。
:::

+++

这里我们选的是最近的 $K=3$ 个观测，但 $K=3$ 并没有什么特别之处。我们也可以用 $K=4, 5$ 或更多（不过为了避免平局，最好选奇数）。关于如何选择 $K$，我们会在下一章进一步讨论。

+++

### 点与点之间的距离

```{index} 距离; k 近邻, 直线; 距离
```

我们依据*直线距离*（straight-line distance）判断哪些点是新观测的 $K$ 个“最近”邻点（后文常直接简称为*距离*）。假设有两个观测 $a$ 和 $b$，各自都有两个预测变量 $x$ 和 $y$。记 $a_x$ 和 $a_y$ 为观测 $a$ 在变量 $x$ 和 $y$ 上的取值；$b_x$ 和 $b_y$ 的含义与观测 $b$ 类似。那么观测 $a$ 与 $b$ 在 x-y 平面上的直线距离可以用下面的公式计算：

$$\mathrm{Distance} = \sqrt{(a_x -b_x)^2 + (a_y - b_y)^2}$$

+++

要找出新观测的 $K$ 个最近邻，我们先计算新观测到训练数据中每个观测的距离，再选出与 $K$ 个*最小*距离取值相对应的 $K$ 个观测。例如，假设我们要用 $K=5$ 个近邻来判断一个新观测的类别，它的周长为 {glue:text}`3-new_point_0`，凹度为 {glue:text}`3-new_point_1`，在图 {numref}`fig:05-multiknn-1` 中用红色菱形表示。下面我们计算新点与训练集中每个观测的距离，找出离新点最近的 $K=5$ 个近邻。在下面的代码中你会看到，我们按上面的公式计算直线距离：先把两个观测的周长之差与凹度之差分别平方，再把两个平方结果相加，最后开平方。为了找出 $K=5$ 个最近邻，我们使用 `pandas` 中的 `nsmallest` 函数。

```{index} nsmallest
```

```{code-cell} ipython3
:tags: [remove-cell]

new_point = [0, 3.5]
attrs = ["Perimeter", "Concavity"]
points_df3 = pd.DataFrame(
    {"Perimeter": new_point[0], "Concavity": new_point[1], "Class": ["Unknown"]}
)
perim_concav_with_new_point_df3 = pd.concat((cancer, points_df3), ignore_index=True)
perim_concav_with_new_point3 = (
    alt.Chart(
        perim_concav_with_new_point_df3,
    )
    .mark_point(opacity=0.6, filled=True, size=40)
    .encode(
        x=alt.X("Perimeter", title="Perimeter (standardized)"),
        y=alt.Y("Concavity", title="Concavity (standardized)"),
        color=alt.Color(
            "Class",
            title="Diagnosis",
        ),
        shape=alt.Shape(
            "Class", scale=alt.Scale(range=["circle", "circle", "diamond"])
        ),
        size=alt.condition("datum.Class == 'Unknown'", alt.value(80), alt.value(30)),
        stroke=alt.condition("datum.Class == 'Unknown'", alt.value("black"), alt.value(None)),
    )
)

glue("3-new_point_0", "{:.1f}".format(new_point[0]))
glue("3-new_point_1", "{:.1f}".format(new_point[1]))
glue("fig:05-multiknn-1", perim_concav_with_new_point3)
```


:::{glue:figure} fig:05-multiknn-1
:name: fig:05-multiknn-1

凹度与周长的散点图，其中新观测用红色菱形表示。
:::


```{code-cell} ipython3
new_obs_Perimeter = 0
new_obs_Concavity = 3.5
cancer["dist_from_new"] = (
       (cancer["Perimeter"] - new_obs_Perimeter) ** 2
     + (cancer["Concavity"] - new_obs_Concavity) ** 2
)**(1/2)
cancer.nsmallest(5, "dist_from_new")[[
    "Perimeter",
    "Concavity",
    "Class",
    "dist_from_new"
]]
```


```{code-cell} ipython3
:tags: [remove-cell]
# code needed to render the latex table with distance calculations
from IPython.display import Latex
five_neighbors = (
    cancer
   [["Perimeter", "Concavity", "Class"]]
   .assign(dist_from_new = (
       (cancer["Perimeter"] - new_obs_Perimeter) ** 2
     + (cancer["Concavity"] - new_obs_Concavity) ** 2
   )**(1/2))
   .nsmallest(5, "dist_from_new")
).reset_index()

for i in range(5):
    glue(f"gn{i}_perim", "{:0.2f}".format(five_neighbors["Perimeter"][i]))
    glue(f"gn{i}_concav", "{:0.2f}".format(five_neighbors["Concavity"][i]))
    glue(f"gn{i}_class", five_neighbors["Class"][i])

    # typeset perimeter,concavity with parentheses if negative for latex
    nperim = f"{five_neighbors['Perimeter'][i]:.2f}" if five_neighbors['Perimeter'][i] > 0 else f"({five_neighbors['Perimeter'][i]:.2f})"
    nconcav = f"{five_neighbors['Concavity'][i]:.2f}" if five_neighbors['Concavity'][i] > 0 else f"({five_neighbors['Concavity'][i]:.2f})"

    glue(f"gdisteqn{i}", Latex(f"\sqrt{{(0-{nperim})^2+(3.5-{nconcav})^2}}={five_neighbors['dist_from_new'][i]:.2f}"))
```


{numref}`tab:05-multiknn-mathtable` 用数学细节展示了我们如何为训练数据中 5 个最近邻逐一计算 `dist_from_new` 变量（即到新观测的距离）。

```{table} 评估新观测到其 5 个最近邻的距离
:name: tab:05-multiknn-mathtable
| Perimeter | Concavity | Distance            | Class |
|-----------|-----------|----------------------------------------|-------|
| {glue:text}`gn0_perim`  | {glue:text}`gn0_concav`  | {glue:}`gdisteqn0` | {glue:text}`gn0_class`     |
| {glue:text}`gn1_perim`  | {glue:text}`gn1_concav`  | {glue:}`gdisteqn1` | {glue:text}`gn1_class`     |
| {glue:text}`gn2_perim`  | {glue:text}`gn2_concav`  | {glue:}`gdisteqn2` | {glue:text}`gn2_class`     |
| {glue:text}`gn3_perim`  | {glue:text}`gn3_concav`  | {glue:}`gdisteqn3` | {glue:text}`gn3_class`     |
| {glue:text}`gn4_perim`  | {glue:text}`gn4_concav`  | {glue:}`gdisteqn4` | {glue:text}`gn4_class`     |
```

+++

计算结果表明，新观测的 5 个最近邻中有 3 个是恶性；既然恶性占多数，我们就把新观测判为恶性。这 5 个近邻在图 {numref}`fig:05-multiknn-3` 中用圆圈标出。

```{code-cell} ipython3
:tags: [remove-cell]

circle_path_df = pd.DataFrame(
    {
        "Perimeter": new_point[0] + 1.4 * np.cos(np.linspace(0, 2 * np.pi, 100)),
        "Concavity": new_point[1] + 1.4 * np.sin(np.linspace(0, 2 * np.pi, 100)),
    }
)
circle = alt.Chart(circle_path_df.reset_index()).mark_line(color="black").encode(
    x="Perimeter",
    y="Concavity",
    order="index"
)

glue("fig:05-multiknn-3", (perim_concav_with_new_point3 + circle))
```


:::{glue:figure} fig:05-multiknn-3
:name: fig:05-multiknn-3

凹度与周长的散点图，其中 5 个最近邻用圆圈标出。
:::

+++

### 多于两个解释变量

上面的介绍针对的是两个预测变量，但预测变量更多时，完全相同的 k 近邻算法同样适用。每个预测变量都可能提供新信息，帮助我们建立分类器。唯一的区别在于点与点之间的距离公式。假设两个观测 $a$ 和 $b$ 各有 $m$ 个预测变量，即 $a = (a_{1}, a_{2}, \dots, a_{m})$ 和 $b = (b_{1}, b_{2}, \dots, b_{m})$。

```{index} 距离; 多于两个变量
```

距离公式变为

$$\mathrm{Distance} = \sqrt{(a_{1} -b_{1})^2 + (a_{2} - b_{2})^2 + \dots + (a_{m} - b_{m})^2}.$$

这个公式仍然对应直线距离，只不过是在维数更多的空间里。假设我们要计算新观测与另一个观测之间的距离：新观测的周长为 0、凹度为 3.5、对称性为 1，另一个观测的周长、凹度和对称性分别为 0.417、2.31 和 0.837。这两个观测都有三个预测变量：周长、凹度和对称性。前面只有两个变量时，我们把（两个）变量各自之差的平方相加，再开平方。现在做法相同，只是变量换成了三个。距离的计算如下

$$\mathrm{Distance} =\sqrt{(0 - 0.417)^2 + (3.5 - 2.31)^2 + (1 - 0.837)^2} = 1.27.$$

下面我们计算新观测与训练集中每个观测的距离，找出在这三个预测变量下离新观测最近的 $K=5$ 个近邻。

```{code-cell} ipython3
new_obs_Perimeter = 0
new_obs_Concavity = 3.5
new_obs_Symmetry = 1
cancer["dist_from_new"] = (
      (cancer["Perimeter"] - new_obs_Perimeter) ** 2
    + (cancer["Concavity"] - new_obs_Concavity) ** 2
    + (cancer["Symmetry"] - new_obs_Symmetry) ** 2
)**(1/2)
cancer.nsmallest(5, "dist_from_new")[[
    "Perimeter",
    "Concavity",
    "Symmetry",
    "Class",
    "dist_from_new"
]]
```


在这三个预测变量下，$K=5$ 个最近邻中有 4 个属于恶性类别，因此我们会把新观测判为恶性。{numref}`fig:05-more` 展示了把这些数据画成三维散点图、并从新观测连向五个最近邻时的样子。

```{code-cell} ipython3
:tags: [remove-cell]

new_point = [0, 3.5, 1]
attrs = ["Perimeter", "Concavity", "Symmetry"]
points_df4 = pd.DataFrame(
    {
        "Perimeter": new_point[0],
        "Concavity": new_point[1],
        "Symmetry": new_point[2],
        "Class": ["Unknown"],
    }
)
perim_concav_with_new_point_df4 = pd.concat((cancer, points_df4), ignore_index=True)
# Find the euclidean distances from the new point to each of the points
# in the orginal data set
my_distances4 = euclidean_distances(perim_concav_with_new_point_df4[attrs])[
    len(cancer)
][:-1]
```


```{code-cell} ipython3
:tags: [remove-cell]

# The index of 5 rows that has smallest distance to the new point
min_5_idx = np.argpartition(my_distances4, 5)[:5]

neighbor_df_list = []
for idx in min_5_idx:
    neighbor_df = pd.concat(
        (
            cancer.loc[idx, attrs + ["Class"]],
            perim_concav_with_new_point_df4.loc[len(cancer), attrs + ["Class"]],
        ),
        axis=1,
    ).T
    neighbor_df_list.append(neighbor_df)
```


```{code-cell} ipython3
:tags: [remove-input]

fig = px.scatter_3d(
    perim_concav_with_new_point_df4,
    x="Perimeter",
    y="Concavity",
    z="Symmetry",
    color="Class",
    symbol="Class",
    opacity=0.5,
)
# specify trace names and symbols in a dict
symbols = {"Malignant": "circle", "Benign": "circle", "Unknown": "diamond"}

# set all symbols in fig
for i, d in enumerate(fig.data):
    fig.data[i].marker.symbol = symbols[fig.data[i].name]

# specify trace names and colors in a dict
colors = {"Malignant": "#ff7f0e", "Benign": "#1f77b4", "Unknown": "red"}

# set all colors in fig
for i, d in enumerate(fig.data):
    fig.data[i].marker.color = colors[fig.data[i].name]

# set a fixed custom marker size
fig.update_traces(marker={"size": 5})

# add lines
for neighbor_df in neighbor_df_list:
    fig.add_trace(
        go.Scatter3d(
            x=neighbor_df["Perimeter"],
            y=neighbor_df["Concavity"],
            z=neighbor_df["Symmetry"],
            line_color=colors[neighbor_df.iloc[0]["Class"]],
            name=neighbor_df.iloc[0]["Class"],
            mode="lines",
            line=dict(width=2),
            showlegend=False,
        )
    )


# tight layout
fig.update_layout(margin=dict(l=0, r=0, b=0, t=1), template="plotly_white")

# if HTML, use the plotly 3d image; if PDF, use static image
if "BOOK_BUILD_TYPE" in os.environ and os.environ["BOOK_BUILD_TYPE"] == "PDF":
    glue("fig:05-more", Image("img/classification1/plot3d_knn_classification.png"))
else:
    glue("fig:05-more", fig)
```


```{figure} data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
:name: fig:05-more
:figclass: caption-hack

标准化后的对称性、凹度和周长变量的三维散点图。请注意，一般情况下我们并不建议使用三维可视化；这里以三维方式展示数据，只是为了说明高维空间与最近邻是什么样子，供学习之用。
```

+++

### k 近邻算法小结

要用 k 近邻分类器判断一个新观测的类别，需要完成以下步骤：

1. 计算新观测与训练集中每个观测之间的距离。
2. 找出与 $K$ 个最小距离相对应的 $K$ 行。
3. 根据各近邻类别的多数投票，判定新观测的类别。

+++
<<TERM>>
perimeter = 周长
concavity = 凹度
symmetry = 对称性
diagnosis = 诊断
<<END>>
