+++

:::{glue:figure} fig:05-knn-4
:name: fig:05-knn-4

Scatter plot of concavity versus perimeter. The new observation is represented
as a red diamond with a line to the one nearest neighbor, which has a benign
label.
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

To improve the prediction we can consider several
neighboring points, say $K = 3$, that are closest to the new observation
to predict its diagnosis class. Among those 3 closest points, we use the
*majority class* as our prediction for the new observation. As shown in {numref}`fig:05-knn-5`, we
see that the diagnoses of 2 of the 3 nearest neighbors to our new observation
are malignant. Therefore we take majority vote and classify our new red, diamond
observation as malignant.

+++

:::{glue:figure} fig:05-knn-5
:name: fig:05-knn-5

Scatter plot of concavity versus perimeter with three nearest neighbors.
:::

+++

Here we chose the $K=3$ nearest observations, but there is nothing special
about $K=3$. We could have used $K=4, 5$ or more (though we may want to choose
an odd number to avoid ties). We will discuss more about choosing $K$ in the
next chapter.

+++

### Distance between points

```{index} distance; K-nearest neighbors, straight line; distance
```

We decide which points are the $K$ "nearest" to our new observation using the
*straight-line distance* (we will often just refer to this as *distance*).
Suppose we have two observations $a$ and $b$, each having two predictor
variables, $x$ and $y$.  Denote $a_x$ and $a_y$ to be the values of variables
$x$ and $y$ for observation $a$; $b_x$ and $b_y$ have similar definitions for
observation $b$.  Then the straight-line distance between observation $a$ and
$b$ on the x-y plane can be computed using the following formula:

$$\mathrm{Distance} = \sqrt{(a_x -b_x)^2 + (a_y - b_y)^2}$$

+++

To find the $K$ nearest neighbors to our new observation, we compute the distance
from that new observation to each observation in our training data, and select the $K$ observations corresponding to the
$K$ *smallest* distance values. For example, suppose we want to use $K=5$ neighbors to classify a new
observation with perimeter {glue:text}`3-new_point_0` and
concavity {glue:text}`3-new_point_1`, shown as a red diamond in {numref}`fig:05-multiknn-1`. Let's calculate the distances
between our new point and each of the observations in the training set to find
the $K=5$ neighbors that are nearest to our new point.
You will see in the code below, we compute the straight-line
distance using the formula above: we square the differences between the two observations' perimeter
and concavity coordinates, add the squared differences, and then take the square root.
In order to find the $K=5$ nearest neighbors, we will use the `nsmallest` function from `pandas`.

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

Scatter plot of concavity versus perimeter with new observation represented as a red diamond.
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

In {numref}`tab:05-multiknn-mathtable` we show in mathematical detail how
we computed the `dist_from_new` variable (the
distance to the new observation) for each of the 5 nearest neighbors in the
training data.

```{table} Evaluating the distances from the new observation to each of its 5 nearest neighbors
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

The result of this computation shows that 3 of the 5 nearest neighbors to our new observation are
malignant; since this is the majority, we classify our new observation as malignant.
These 5 neighbors are circled in {numref}`fig:05-multiknn-3`.

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

Scatter plot of concavity versus perimeter with 5 nearest neighbors circled.
:::

+++

### More than two explanatory variables

Although the above description is directed toward two predictor variables,
exactly the same K-nearest neighbors algorithm applies when you
have a higher number of predictor variables.  Each predictor variable may give us new
information to help create our classifier.  The only difference is the formula
for the distance between points. Suppose we have $m$ predictor
variables for two observations $a$ and $b$, i.e.,
$a = (a_{1}, a_{2}, \dots, a_{m})$ and
$b = (b_{1}, b_{2}, \dots, b_{m})$.

```{index} distance; more than two variables
```

The distance formula becomes

$$\mathrm{Distance} = \sqrt{(a_{1} -b_{1})^2 + (a_{2} - b_{2})^2 + \dots + (a_{m} - b_{m})^2}.$$

This formula still corresponds to a straight-line distance, just in a space
with more dimensions. Suppose we want to calculate the distance between a new
observation with a perimeter of 0, concavity of 3.5, and symmetry of 1, and
another observation with a perimeter, concavity, and symmetry of 0.417, 2.31, and
0.837 respectively. We have two observations with three predictor variables:
perimeter, concavity, and symmetry. Previously, when we had two variables, we
added up the squared difference between each of our (two) variables, and then
took the square root. Now we will do the same, except for our three variables.
We calculate the distance as follows

$$\mathrm{Distance} =\sqrt{(0 - 0.417)^2 + (3.5 - 2.31)^2 + (1 - 0.837)^2} = 1.27.$$

Let's calculate the distances between our new observation and each of the
observations in the training set to find the $K=5$ neighbors when we have these
three predictors.

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

Based on $K=5$ nearest neighbors with these three predictors we would classify
the new observation as malignant since 4 out of 5 of the nearest neighbors are malignant class.
{numref}`fig:05-more` shows what the data look like when we visualize them
as a 3-dimensional scatter with lines from the new observation to its five nearest neighbors.

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

3D scatter plot of the standardized symmetry, concavity, and perimeter
variables. Note that in general we recommend against using 3D visualizations;
here we show the data in 3D only to illustrate what higher dimensions and
nearest neighbors look like, for learning purposes.
```

+++

### Summary of K-nearest neighbors algorithm

In order to classify a new observation using a K-nearest neighbors classifier, we have to do the following:

1. Compute the distance between the new observation and each observation in the training set.
2. Find the $K$ rows corresponding to the $K$ smallest distances.
3. Classify the new observation based on a majority vote of the neighbor classes.

+++

