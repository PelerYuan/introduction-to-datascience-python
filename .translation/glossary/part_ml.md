# 术语表：机器学习（分类、回归、聚类、模型评估）

## 一、通用机器学习概念
data set | 数据集 |
data point | 数据点 |
measurement | 测量值 | 指对观测某个特征的量测结果
predictive question | 预测性问题 | 首见加注（predictive question）；与描述性、探索性问题相对
prediction error | 预测误差 |
model object | 模型对象 | 首见加注（model object）
model training | 模型训练 |
train | 训练 | 动词；与测试、验证三个阶段对应
training data | 训练数据 |
test data | 测试数据 |
retrain | 重新训练 |
algorithm | 算法 |
assumption | 假设 | 指模型前提；与假设检验中的"原假设"不是一回事
candidate model | 候选模型 |
generalization | 泛化 | 首见加注（generalization）；动词形式 generalize 译"泛化到"
interpretability | 可解释性 |
trade-off | 权衡取舍 |
reproducible | 可复现的 | 修饰 analysis 时译"可复现的分析"
randomness | 随机性 |
random number generator | 随机数生成器 | 缩写 RNG 保留英文
default random number generator | 默认随机数生成器 |
noise | 噪声 |
underlying structure | 潜在结构 | 指数据中未被标注出来的分组结构
subgroup | 子组 |
pattern | 模式 |
labeled data | 有标签数据 |
unlabeled data | 无标签数据 |
irrelevant predictor | 无关预测变量 |
informative predictor | 有信息量的预测变量 |
predictor variable selection | 预测变量选择 | 本书小节标题；亦称 variable selection
variable selection | 变量选择 |
best subset selection | 最优子集选择 | 首见加注（best subset selection）
forward selection | 前向选择 | 首见加注（forward selection）
feature engineering | 特征工程 | 首见加注（feature engineering）；特征与预测变量指同一对象，按语境择一
predictor design | 预测变量设计 | 本书中与 feature engineering 同义
preprocessor | 预处理器 | 首见加注（preprocessor）
centering | 中心化 |
center | 中心 | 名词，指变量的中心位置
unstandardized data | 未标准化数据 |
standardized data | 标准化数据 |
unscaled data | 未缩放数据 |
impute | 插补 |
mean imputation | 均值插补 |
missing entries | 缺失项 |
randomly missing | 随机缺失 | 原文指缺失与观测的其它方面无关
informative missingness | 有信息量的缺失 | 原文指缺失本身可能与其它变量取值相关
synthetic values | 合成取值 |
numerical variable | 数值变量 |
quantitative variable | 定量变量 |
categorical variable | 分类变量 | 与 categorical（类别型）同义，正文两词都出现
K-NN | K-NN | [保留英文]
supervised task | 有监督任务 |
unsupervised task | 无监督任务 |

## 二、分类
classification problem | 分类问题 |
binary classification | 二分类 | 首见加注（binary classification）
multiclass classification | 多分类 | 首见加注（multiclass classification）
class label | 类别标签 | 与 label（标签）同义，正文两词混用
predicted label | 预测标签 |
actual label | 实际标签 | 正文亦称 true label（真实标签）
positive label | 正类标签 | 与 negative label 相对；是理解精确率与召回率的关键
negative label | 负类标签 |
positive observation | 正类观测 |
misclassification | 误分类 | 动词 misclassify 同译
majority vote | 多数投票 |
majority classifier | 多数类分类器 | 备选：多数投票分类器；与 majority class（多数类）区分，前者是模型，后者是类别
ties | 平局 | 原文指投票票数相同的平局情形
distance | 距离 |
straight-line distance | 直线距离 | 首见加注（straight-line distance）
Euclidean distance | 欧氏距离 | 首见加注（Euclidean distance）
nearest neighbour | 最近邻 | 本书用英式拼写；美式写作 nearest neighbor
number of neighbors | 近邻个数 | 即 K 近邻算法中的参数 K
new observation | 新观测 |
decision | 判别 | 指分类器对新观测给出的类别判定
boundary | 边界 | 指分类判别边界；K 过小时呈锯齿状
class proportions | 类别比例 |
class imbalance | 类别不平衡 | 首见加注（class imbalance）
imbalanced data | 不平衡数据 |
rare class | 稀有类 |
rebalance | 重新平衡 |
balanced data | 平衡数据 |
oversampling | 过采样 | 首见加注（oversampling）
upsampled data | 上采样后的数据 | 本书用 sample 方法复制稀有类观测实现
voting power | 表决权 |
precision and recall | 精确率与召回率 | 与 accuracy 区分：accuracy 看整体正确比例，precision 只看预测为正的观测中真正为正的比例
decision tree | 决策树 | 拓展资源中提及，本书未展开
support vector machine | 支持向量机 | 拓展资源中提及，缩写 SVM 保留英文
logistic regression | 逻辑回归 | 用于分类而非回归，原文特别提醒名称容易混淆
neural network | 神经网络 |
linear discriminant analysis | 线性判别分析 |
naive Bayes | 朴素贝叶斯 |
benign | 良性的 | 乳腺癌案例的类别名；数据列取值 Benign 保留英文，搭配译"良性肿瘤"
malignant | 恶性的 | 乳腺癌案例的类别名；数据列取值 Malignant 保留英文，搭配译"恶性肿瘤"

## 三、回归
regression problem | 回归问题 |
K-NN regression | k 近邻回归 |
linear regression | 线性回归 |
simple linear regression | 简单线性回归 |
multivariable linear regression | 多变量线性回归 | 首见加注（multivariable linear regression）；指含多个预测变量的情形，备选：多元线性回归
regression equation | 回归方程 |
line of best fit | 最优拟合直线 | 备选：最佳拟合线
plane of best fit | 最优拟合平面 |
vertical intercept | 纵截距 |
intercept | 截距 |
slope | 斜率 |
coefficient | 系数 |
linear relationship | 线性关系 |
non-linear relationship | 非线性关系 |
flexible | 灵活的 | 形容 k 近邻拟合线可随数据起伏；原文亦用 wiggly
extrapolation | 外推 | 首见加注（extrapolation）
average squared vertical distance | 纵向距离平方的平均值 | 原文对最小二乘拟合的直观解释
RMSPE | 均方根预测误差 | 首见加注（root mean squared prediction error）；缩写 RMSPE 保留英文，备选：根均方预测误差
RMSE | 均方根误差 | 缩写 RMSE 保留英文；计算式与 RMSPE 完全相同，区别只在用于训练数据还是测试数据
mean squared error | 均方误差 | 首见加注（mean squared error）
training error | 训练误差 | 样本内误差；与 test error 区分
test error | 测试误差 | 样本外误差
in-sample prediction | 样本内预测 |
multicollinearity | 多重共线性 | 首见加注（multicollinearity）；指预测变量之间高度线性相关，此类变量译"共线预测变量"
goodness of fit | 拟合优度 | 本书亦写 model goodness of fit，同译
influence | 影响 | 指单个数据点对拟合直线的拉动程度
transformed predictor | 变换后的预测变量 |
regression tree | 回归树 | 拓展资源中提及，本书未展开
spline | 样条 | 拓展资源中提及，本书未展开
local regression | 局部回归 | 拓展资源中提及，本书未展开

## 四、聚类
cluster | 簇 | 首见加注（cluster）；与 clustering（聚类）区分，前者指一个分组，后者指方法或结果
clustering algorithm | 聚类算法 |
cluster center | 簇中心 | 代码中的变量名写作 centroid
centroid | 质心 | 与 cluster center 同义；代码变量名 centroid 保留英文
cluster label | 簇标签 |
cluster assignment | 簇归属 | 正文亦称 assignment，指数据点被分到哪个簇
initial centers | 初始中心 |
random initialization | 随机初始化 |
random restart | 随机重启 | 本书小节标题 Random restarts
bad solution | 劣质解 | 原文指 k 均值因初始化不佳而"卡住"的较差结果
center update | 中心更新 | k 均值算法两步之一
label update | 标签更新 | k 均值算法两步之一
WSSD | 簇内平方距离和 | 缩写 WSSD 保留英文；全称 within-cluster sum-of-squared-distances
within-cluster sum-of-squared-distances | 簇内平方距离和 | 首见加注（within-cluster sum-of-squared-distances）
total WSSD | 总 WSSD | 所有簇的 WSSD 之和，k 均值的目标即最小化该量；图中亦称 total within-cluster sum of squares
inertia | 惯性 | scikit-learn 中 inertia_ 属性即总 WSSD；属性名保留英文
cluster quality | 聚类质量 |
elbow method | 肘部法则 | 首见加注（elbow method）
elbow | 肘部 | 指总 WSSD 曲线由陡降转为平缓的拐弯处
number of clusters | 簇数 |
subdivide | 细分 | 与合并相对；K 过大时子组被细分
semisupervised | 半监督 | 首见加注（semisupervised）
hierarchical clustering | 层次聚类 | 本书仅在拓展资源中提及
principal component analysis | 主成分分析 | 缩写 PCA 保留英文
multidimensional scaling | 多维标度法 | 本书仅在拓展资源中提及
silhouette | 轮廓系数 | 本书正文未出现，作为聚类质量评估的通用指标收录

## 五、模型评估与调优
evaluating performance | 评估性能 |
performance | 性能 |
estimated accuracy | 估计准确率 | 交叉验证给出的准确率估计亦称 accuracy estimate（准确率估计值）
prediction accuracy | 预测准确率 | 与 precision（精确率）区分：前者是整体正确比例
estimated cross-validation accuracy | 交叉验证准确率估计值 |
validation accuracy | 验证准确率 |
perfect classifier | 完美分类器 |
trade-off between precision and recall | 精确率与召回率之间的权衡 |
baseline | 基准 | 指便于比较的简单方法，如多数类分类器
standard error | 标准误 | 首见加注（standard error）；与 standard deviation（标准差）区分
folds | 折 | 交叉验证中的等份；单数 fold 同译
number of folds | 折数 |
5-fold cross-validation | 5 折交叉验证 |
chunks | 等份 | 原文指把训练数据均分成的若干等份
train/test split | 训练/测试划分 |
train/validation split | 训练/验证划分 |
split the data | 划分数据 |
shuffle | 打乱 |
stratification | 分层 | 首见加注（stratification）；动词 stratify 同译
stratified split | 分层划分 |
held out | 留出 | 指调优期间不使用、最后才评估的数据
lock box | 保险箱 | 原文比喻，指把测试集暂时封存起来
golden rule of machine learning | 机器学习黄金法则 | 原文强调绝不能用测试数据来建模
tuning | 调优 | 动词 tune 与分词 tuning 同译
tuning process | 调优过程 |
parameter tuning | 参数调优 |
model selection | 模型选择 | 本书表述为调优与评估的整体流程
parameter value | 参数取值 |
parameter grid | 参数网格 |
grid search | 网格搜索 |
model simplicity | 模型简洁性 |
number of predictors | 预测变量个数 |
computational cost | 计算成本 |
critical analysis | 批判性分析 |
downstream application | 下游应用 |

## 六、scikit-learn API
scikit-learn | scikit-learn | [保留英文]；在 Python 中导入名为 sklearn
KNeighborsClassifier | KNeighborsClassifier | [保留英文]
KNeighborsRegressor | KNeighborsRegressor | [保留英文]
LinearRegression | LinearRegression | [保留英文]
Ridge | Ridge | [保留英文]；本书未直接使用，与 LinearRegression 同属回归模型名
KMeans | KMeans | [保留英文]
GridSearchCV | GridSearchCV | [保留英文]
RandomizedSearchCV | RandomizedSearchCV | [保留英文]；本书仅在索引中出现
SequentialFeatureSelector | SequentialFeatureSelector | [保留英文]
train_test_split | train_test_split | [保留英文]
cross_validate | cross_validate | [保留英文]
make_pipeline | make_pipeline | [保留英文]
make_column_transformer | make_column_transformer | [保留英文]
ColumnTransformer | ColumnTransformer | [保留英文]
make_column_selector | make_column_selector | [保留英文]
StandardScaler | StandardScaler | [保留英文]
SimpleImputer | SimpleImputer | [保留英文]
set_config | set_config | [保留英文]；其参数 transform_output 亦保留英文
transform | 变换 | 方法名 transform 保留英文；与 fit 配对使用
score | 得分 | 方法名 score 保留英文；分类器默认给出准确率
get_params | 获取参数 | 方法名 get_params 保留英文
labels_ | labels_ | [保留英文]
inertia_ | inertia_ | [保留英文]
n_clusters | n_clusters | [保留英文]
n_init | n_init | [保留英文]
n_neighbors | n_neighbors | [保留英文]
random_state | random_state | [保留英文]
cv | cv | [保留英文]；交叉验证折数参数
cv_results_ | cv_results_ | [保留英文]
best_params_ | best_params_ | [保留英文]
coef_ | coef_ | [保留英文]
intercept_ | intercept_ | [保留英文]
estimator argument | estimator 参数 | scikit-learn 中指传入的模型对象；与统计学的"估计量"estimator 区分
param_grid | param_grid | [保留英文]
scoring | scoring | [保留英文]
neg_root_mean_squared_error | neg_root_mean_squared_error | [保留英文]；scikit-learn 用负 RMSPE 以便统一按最大化处理
pos_label | pos_label | [保留英文]
y_true | y_true | [保留英文]
y_pred | y_pred | [保留英文]
crosstab | crosstab | [保留英文]
precision_score | precision_score | [保留英文]
recall_score | recall_score | [保留英文]
mean_squared_error | mean_squared_error | [保留英文]
euclidean_distances | euclidean_distances | [保留英文]
train_size | train_size | [保留英文]
test_size | test_size | [保留英文]
shuffle argument | shuffle 参数 | 参数名保留英文；控制划分前是否打乱数据
stratify argument | stratify 参数 | 参数名保留英文；按类别标签分层划分
remainder | remainder | [保留英文]
passthrough | passthrough | [保留英文]
verbose_feature_names_out | verbose_feature_names_out | [保留英文]
dtype_include | dtype_include | [保留英文]
weights | weights | [保留英文]