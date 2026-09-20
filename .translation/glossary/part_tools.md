# 术语表：统计推断、工具与环境、版本控制

## 一、统计推断
inferential question | 推断性问题 | 首见加注（inferential question）
interval estimation | 区间估计 | 与点估计 point estimate 相对
sample estimate | 样本估计值 | 与点估计同指，正文互见
proportion | 比例 |
population proportion | 总体比例 |
sample proportion | 样本比例 |
sampling variability | 抽样变异性 | 备选：抽样波动
sample size | 样本量 |
sample mean | 样本均值 |
population mean | 总体均值 |
sample distribution | 样本分布 | 与抽样分布 sampling distribution 严格区分
population distribution | 总体分布 |
sampling distribution of the mean | 均值的抽样分布 |
sampling distribution of the proportion | 比例的抽样分布 |
bell-shaped | 钟形的 | 首见加注（bell-shaped）
symmetric | 对称的 |
skewed | 偏斜的 | 首见加注（skewed）；备选：偏态的
long tail | 长尾 |
right tail | 右侧长尾 | 备选：右尾
one peak | 单峰 |
measure of center | 集中趋势度量 | 备选：位置的度量
spread | 离散程度 | 备选：波动程度
measure of spread | 离散程度度量 |
variability | 变异性 |
quantitative | 定量的 | 与 categorical 相对；备选：数值型
case | 研究个体 | 与核心表 case study（案例分析）区分
with replacement | 有放回 | 首见加注（with replacement）
without replacement | 无放回 |
bootstrap process | 自助过程 |
percentile bootstrap confidence interval | 百分位数自助置信区间 | 首见加注（percentile bootstrap confidence interval）
lower bound | 下限 |
upper bound | 上限 |
plausible range of values | 合理取值范围 | 置信区间定义用语
capture the population parameter | 覆盖总体参数 | 指区间包含参数真值
uncertainty | 不确定性 |
estimate accuracy | 估计的准确程度 | 与机器学习的准确率 accuracy 区分
finite population | 有限总体 |
rule of thumb | 经验法则 |
replicate | 重复 | 指第几次抽样，代码列名 `replicate` 保留英文

## 二、Jupyter 与开发环境
Jupyter | Jupyter | [保留英文]
JupyterHub | JupyterHub | [保留英文]
JupyterLab Desktop | JupyterLab Desktop | [保留英文]
Jupyter Git extension | Jupyter Git 扩展 | 扩展名保留英文
jupyterlab-git | jupyterlab-git | [保留英文]
Jupyter file browser | Jupyter 文件浏览器 |
Launcher | 启动器 | JupyterLab 界面标签页
Python session | Python 会话 |
restart | 重启 |
interrupt | 中断 |
idle | 空闲 | 内核状态
linear order | 线性顺序 | 指从上到下依次执行
nonlinear notebook | 非线性笔记本 | 指单元格执行顺序被打乱
out-of-order execution | 乱序执行 |
best practice | 最佳实践 | 与核心表 good practices（良好实践）并用
toolbar | 工具栏 |
autosave | 自动保存 | 首见加注（autosave）
rich text | 富文本 | 首见加注（rich text）
rendered | 已渲染 |
unrendered | 未渲染 | 首见加注（unrendered）
Markdown language | Markdown 语言 | [保留英文]
plain text file | 纯文本文件 |
separator | 分隔符 |
file extension | 文件扩展名 |
hidden dependency | 隐含依赖 | 备选：隐藏依赖
list comprehension | 列表推导式 | 首见加注（list comprehension）
web browser | 网页浏览器 | Firefox、Safari、Chrome、Edge 等名称保留英文
Run All Cells | 运行全部单元格 | 界面菜单项，首见加注（Run All Cells）
Restart Kernel and Run All Cells | 重启内核并运行全部单元格 | 界面菜单项
Interrupt Kernel | 中断内核 | 界面菜单项
Restart Kernel | 重启内核 | 界面菜单项
Save Notebook | 保存笔记本 | 界面菜单项
Docker | Docker | [保留英文]
Docker Desktop | Docker Desktop | [保留英文]
container | 容器 | 首见加注（container）
image | 镜像 | Docker 语境，勿与"图片"混淆
tag | 标签 | Docker 镜像版本标签
Dockerfile | Dockerfile | [保留英文]
conda | conda | [保留英文]
pip | pip | [保留英文]
environment.yml | environment.yml | [保留英文]
Python environment | Python 环境 |
autograder test | 自动评分测试 |
WSL-2 / Hyper-V | 保留英文 | [保留英文]
Ubuntu Linux | Ubuntu Linux | [保留英文]
MacOS | MacOS | [保留英文]
Windows | Windows | [保留英文]

## 三、版本控制与 GitHub
version control system | 版本控制系统 |
local repository | 本地仓库 | 与核心表 remote（远程仓库）配套
repository history | 仓库历史 |
version history | 版本历史 |
snapshot | 快照 | 首见加注（snapshot）
commit message | 提交信息 |
commit hash | 提交哈希值 |
revert | 回退 | 备选：还原
track changes | 跟踪更改 |
untracked | 未跟踪 | Jupyter Git 面板分组名
changed | 已修改 | Jupyter Git 面板分组名
staged | 已暂存 | Jupyter Git 面板分组名
add | 添加 | 指把文件加入暂存区，与 GitHub 的 Add file 菜单区分
checkpoint file | 检查点文件 | 首见加注（checkpoint file）
auto-generated file | 自动生成的文件 |
plain text editor | 纯文本编辑器 |
merge conflict marker | 合并冲突标记 | 指 `<<<<<<< HEAD` 一类标记
resolve a merge conflict | 解决合并冲突 |
write access | 写权限 | 首见加注（write access）
personal access token | 个人访问令牌 | 首见加注（personal access token）
PAT | PAT | [保留英文]
authentication | 身份验证 |
credentials | 凭据 |
public repository | 公开仓库 |
private repository | 私有仓库 |
README.md | README.md | [保留英文]
Git pane | Git 面板 | Jupyter Git 扩展界面
issue thread | 议题讨论串 |
collaborator access | 协作者访问权限 |
negative results | 负面结果 | 指未能成功的分析尝试
bug | 缺陷 | 首见加注（bug）
HTTPS method | HTTPS 方式 | [保留英文]
GitLab | GitLab | [保留英文]
pen tool | 铅笔工具 | GitHub 界面工具，首见加注（pen tool）
Commit changes | 提交更改 | GitHub 界面按钮
Add file | 添加文件 | GitHub 界面菜单
Upload files | 上传文件 | GitHub 界面菜单项
Manage access | 管理访问权限 | GitHub 界面
Invite a collaborator | 邀请协作者 | GitHub 界面按钮
New issue | 新建议题 | GitHub 界面按钮
Close issue | 关闭议题 | GitHub 界面按钮
Generate new token | 生成新令牌 | GitHub 界面按钮

## 四、课程组织与教学用语
worksheet | 练习册 | 指配套的 Jupyter 笔记本习题文件，首见加注（worksheet）
worksheets repository | 练习册仓库 |
view worksheet | 查看练习册 |
exercise | 习题 | 章节小节名 Exercises 译"习题"
non-interactive version | 非交互版本 |
automated feedback | 自动反馈 |
autograder | 自动评分程序 | 备选：自动评分器
course setup | 课程环境配置 |
introductory course | 入门课程 |
instructor | 授课教师 |
first-year student | 一年级学生 |
undergraduate student | 本科生 |
graduate course | 研究生课程 |
curriculum | 课程体系 |
open textbook | 开源教材 |
open educational resource | 开放教育资源 | 缩写 OER 保留英文
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License | 知识共享 署名—非商业性使用—相同方式共享 4.0 国际许可协议 | 首见加注（Creative Commons）
table of contents | 目录 |
Preface | 前言 | 与核心表 Front Matter（前言部分）区分
Foreword | 序言 |
Acknowledgments | 致谢 |
About the authors | 作者简介 |
reviewer | 审稿人 |
mentorship | 指导 |
Associate Professor of Teaching | 教学系列副教授 | UBC 教学岗；备选：教学副教授
Assistant Professor of Teaching | 教学系列助理教授 |
postdoctoral associate | 博士后研究员 |

## 五、机构、人名与专有名词（保留原文）
University of British Columbia | 不列颠哥伦比亚大学 | 简称 UBC 保留英文；备选：英属哥伦比亚大学；卑诗大学
British Columbia | 不列颠哥伦比亚省 | 备选：卑诗省
Department of Statistics | 统计系 | UBC 统计系
Department of Earth, Ocean, and Atmospheric Sciences | 地球、海洋与大气科学系 |
University of Toronto | 多伦多大学 |
MIT | 麻省理工学院 | 正文可写"麻省理工学院（MIT）"
Johns Hopkins Bloomberg School of Public Health | 约翰斯·霍普金斯大学布隆伯格公共卫生学院 | 备选：约翰霍普金斯大学
Statistics Canada | 加拿大统计局 |
Census of Population 2016 | 2016 年加拿大人口普查 |
mother tongue | 母语 | 加拿大人口普查用语
Indigenous peoples | 原住民 | 加拿大语境用"原住民"，不用"土著"
Indigenous languages | 原住民语言 |
First Nations | 第一民族 | 首见加注（First Nations）
Métis | 梅蒂人 | 备选：梅蒂斯人
Inuit | 因纽特人 |
Aboriginal | 原住民 | 加拿大统计局用语，与 Indigenous 同指
residential schools | 寄宿学校 | 指加拿大原住民寄宿学校，首见加注（residential schools）
colonization | 殖民化 |
endangered language | 濒危语言 |
Truth and Reconciliation Commission of Canada | 加拿大真相与和解委员会 | 首见加注（Truth and Reconciliation Commission）
Calls to Action | 《行动呼吁》 | 真相与和解委员会文件，保留英文原名
They Came for the Children | 《他们为孩子而来：加拿大、原住民与寄宿学校》 | 书名首见保留英文原名
Pulling Together: Foundations Guide | 《Pulling Together：基础指南》 | 保留英文书名
Canadian Geographic | 《Canadian Geographic》 | [保留英文]
Airbnb | Airbnb | [保留英文]
OpenIntro Statistics | 《OpenIntro Statistics》 | [保留英文] 书名
Data Science: A First Introduction with Python | 《Data Science: A First Introduction with Python》 | 书名保留英文原名
Tiffany Timbers | Tiffany Timbers | [保留原文]；如需音译可作"蒂法尼·廷伯斯"
Trevor Campbell | Trevor Campbell | [保留原文]
Melissa Lee | Melissa Lee | [保留原文]
Joel Ostblom | Joel Ostblom | [保留原文]
Lindsey Heagy | Lindsey Heagy | [保留原文]
Roger D. Peng | Roger D. Peng | [保留原文] 序言作者
Gabriela Cohen Freue | Gabriela Cohen Freue | [保留原文]
Hadley Wickham | Hadley Wickham | [保留原文]；备选音译：哈德利·威克姆
Mark T. Holder | Mark T. Holder | [保留原文] 章节题词作者
Navya Dahiya | Navya Dahiya | [保留原文]
Gloria Ye | Gloria Ye | [保留原文]
Philip Austin | Philip Austin | [保留原文]
Jim Zidek | Jim Zidek | [保留原文]
Kory Wilson | Kory Wilson | [保留原文]；《Pulling Together》作者
book reviewers | 审稿人 | Rohan Alexander、Isabella Ghement、Virgilio Gómez Rubio、Albert Kim、Adam Loy、Maria Prokofieva、Emily Riederer、Greg Wilson 均 [保留原文]