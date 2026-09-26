# 中译本生产流程（PROCESS）

> 本文件说明从英文原稿到可构建中文版书的完整流水线、角色分工与验收标准。
> 目标是**专业出版级译文**：准确、术语一致、无翻译腔/AI 味。
>
> 状态：**已完成**。18 章 / 52 块全部译出并通过机检；术语一致性扫描完成；构建通过。
> 2026-09-26：按外部评审报告完成一轮修订 —— 固定构建环境版本、扩展渲染层门禁、
> 调整 `source/_config.yml` 的 stderr 处理。实测数字待重建后补录，见 §9.5。

---

## 1. 总体架构

```
英文原稿 (git: main)
      │
      ├─(0) 保全 ──► .translation/source_en/   英文原文备份，供逐句比对与结构校验
      │
      ├─(1) 切块 ──► .translation/work/<chapter>/chunk_NN.src.md
      │              tools/segment.py 保证「拼接无损」（逐字节可还原）
      │
      ├─(2) 术语 ──► GLOSSARY_CORE.md（总协调人）+ glossary/part_*.md（领域 agent）
      │              tools/merge_glossary.py ──► GLOSSARY.md（冻结，884 条）
      │              tools/glossary_excerpt.py ──► 每章术语摘录（10–19KB，给译者与审校）
      │
      ├─(3) 翻译 ──► 每块一个译者 agent ──► chunk_NN.zh.md
      │              输入 = STYLE_GUIDE + 本章术语摘录 + 本块 + 上文只读上下文
      │
      ├─(4) 装配 ──► tools/assemble.py ──► source/<chapter>.md
      │              接缝精确还原 + 中文段落解折行 + 剥离 <<TERM>> 登记块
      │
      ├─(5) 机检 ──► tools/verify_structure.py（结构零改动，含 URL 允许表 URL_FIXES）
      │              tools/lint_zh.py（AI 味 / 标点 / 未译英文 / 空格）
      │              tools/check_emphasis.py（渲染散文块，找没闭合的 ** / _）
      │              tools/diff_paragraphs.py（段落数不符时定位到具体段落）
      │
      ├─(6) 审校 ──► 每章一个审校 agent（看整章 EN+ZH），直接改 source/<chapter>.md
      │              按 prompts/REVIEWER.md 的优先级：准确性 › 去 AI 味 › 一致性 › 排版
      │
      ├─(7) 全书终检 ► tools/term_audit.py（按段对齐的跨章术语审计）
      │              tools/term_fix.py（只改散文、不碰代码的定点统一）
      │              tools/fix_spacing.py（渲染级排版归一：中文间空格、{numref} 紧贴、缺的中西文空格）
      │              tools/status.py（全景状态看板）
      │
      └─(8) 构建 ──► tools/build_book.ps1 ──► source/_build/html
                     └─► tools/html_qa.py（渲染层终检：排版 + 依赖/告警/路径/强调 + 全书图表计数）
                         验证第 7 步真的生效，也验证图表**真的渲染出来了**
```

**为什么先切块再翻译**：切块在「结构安全点」进行（绝不切开代码块），
且 `segment.py` 自检拼接无损，因此译文可以机械拼回，结构完整性有保证。

**为什么要机检 + 审校两关**：机检能抓住「结构破坏、代码被改、术语漂移、AI 味词表」，
但抓不住「意思译反了」。审校 agent 负责语义与文风。

---

## 2. 角色分工（agent 编制）

| 角色 | 数量 | 输入 | 输出 | 上下文预算 |
|---|---|---|---|---|
| 术语抽取 agent | 3 | 规范 + 核心术语表 + 一组章节原文 | `glossary/part_*.md` | ~120k |
| 译者 agent | 1 / 块（52 块） | 规范 + 本章术语摘录 + 本块 + 前文上下文 | `chunk_NN.zh.md` | ~40k |
| 审校 agent | 1 / 章（18 个，前五章合并为 1） | 规范 + 本章术语摘录 + 整章 EN + 整章 ZH | 直接改 `source/<chapter>.md` | ~150k |
| 终检 | 总协调人 + `term_audit.py` | 全书 ZH + 术语表 | 一致性报告 + 定点修订 | — |

**上下文上限：每个 agent 不得超过 250k token。** 上表预算均按此留足余量；
切块大小（约 480 行 / 30KB 原文）保证「规范 + 术语摘录 + 语料」三者之和远低于上限。
审校 agent 需读整章，单章最大 92KB 原文 + 约 60KB 译文 ≈ 60k token，仍安全。
把 48KB 的完整术语表换成按章摘录（10–19KB）是刻意的：它把每个译者的固定开销压掉约 80%。

---

## 3. 验收标准（Definition of Done）

### 3.1 机检门禁（必须全绿）

| 检查 | 工具 | 通过条件 | 实测 |
|---|---|---|---|
| 拼接无损 | `segment.py` | 每章 `lossless=OK` | ✅ 全部 |
| 结构零改动 | `verify_structure.py` | 代码块哈希、指令名与选项、`(label)=`、角色、行内代码、公式、URL（只放过 `URL_FIXES` 里登记的上游 404 修正）、标题层级、`+++`、段落数全部一致 | ✅ 18/18 章（URL 项当时靠人工豁免，改用 `URL_FIXES` 后待重跑，见 §9.5） |
| 中文质量 | `lint_zh.py` | 0 项 | ✅ 18/18 章 |
| 术语一致 | `term_audit.py` | 无跨章漂移（51 条，允许的义项分歧已在 `ACCEPTED_POLYSEMY` 中登记） | ✅ 0 项待处理 |
| 排版（源层） | `fix_spacing.py` | 再次运行报告 `would tighten 0`（幂等） | ✅ 0 |
| 段落对齐 | `align_paragraphs.py` | 段落数一致，且按**角色目标**比较无缺失/无多余 | ✅ 0/18 不一致，`no content lost` |
| 排版（渲染层） | `html_qa.py` | 读 `source/_build/html`：无未解析 `{numref}`、无缺失中西文空格、无中文间多余空格、无泄漏的 `*`/`_`（`RENDERED_EMPHASIS`） | ✅ 旧版检查 `OK rendered book is clean`（初测 503 → 0）；本次新增项待录（见 §9.5） |
| 依赖与图表（渲染层） | `html_qa.py` | 页面里没有被贴进的 `ImportError`/`ModuleNotFoundError`；`vegaEmbed(` 计数 ≥ 80、Plotly 计数 ≥ 3（即 `MISSING_CHARTS` = 0） | ⏳ 待重建后录数（见 §9.5） |
| 告警与路径（渲染层） | `html_qa.py` | `RENDERED_WARNING` / `RENDERED_PATH` 均为 0：正文里不得出现 `…py:2: FutureWarning:` 这类泄漏形态，也不得出现构建机自己的临时路径 | ⏳ 待重建后录数（见 §9.5） |
| 强调标记闭合 | `check_emphasis.py` | 全书 0 处 `LEAK` / `SPAN`；**英文原稿 18 章必须同时为 0**（工具的假阳性基准） | 英文原稿 ✅ `total: 0 leaked marker(s), 0 over-long span(s) in 18 file(s)`；中文译文 ⏳（见 §9.5） |
| 构建 | `build_book.ps1` | 退出码 0，20 个 HTML 页面全部生成；stderr 不再进页面，构建日志里的警告条数按 `reports/build.log` 统计（评审前的「9 条」不再作为基线，见 §9.2） | 退出码 0 / 20 页 ✅；警告条数 ⏳ 重建后录数 |
| 发布 | `deploy_check.py` | 从已发布页面抓出全部本地引用并逐个请求，必须全部 200 | ✅ 20 页 / 187 个引用全部 200（`_images` 125、`_static` 23、`_sources` 18、页间链接 21） |

标 ⏳ 的行是本次评审回应新增的门禁，数字必须在**重建 + 重跑门禁**之后回填（记录位置见 §9.5）。
「发布」行的「20 页 / 187 个引用」是评审前那次构建的数字，重建后要重跑 `deploy_check.py`。

### 3.2 审校门禁（STYLE_GUIDE §8 八项）

R1 结构完整性 · R2 信息完整性 · R3 术语一致性 · R4 准确性 · R5 中文自然度 ·
R6 标点排版 · R7 可读性 · R8 代码零改动。

### 3.3 "无 AI 味"的可操作定义

见 `STYLE_GUIDE.md` 第 2 节黑名单（已固化为 `lint_zh.py` 的 `AI_FLAVOR` 规则）
+ 第 7 节高频句式对照样例。硬指标：

- 机检 `AI_FLAVOR` 命中数 = 0
- 中英混排空格 100% 规范（`CJK_LATIN_GAP` = 0）
- 未翻译英文散文 0 处（书名、专有名词、代码、UI 原文括注除外）
- 中文段落内无手工折行（否则渲染出多余空格，见 §4）

---

## 4. 关键决策记录

| 决策 | 选择 | 理由 |
|---|---|---|
| 译文放在哪里 | **原地翻译 `source/*.md`** | 保持 `img/`、`data/` 相对路径与构建脚本完全不变；英文原文由 git 历史与 `.translation/source_en/` 双重保全 |
| 切块粒度 | ~480 行 / 块 | 单块上下文充足、输出不易截断；跨块一致性由「章级审校」兜底 |
| 术语表来源 | 核心表人工确定 + 领域 agent 扩充 | 最高频术语由总协调人把关，长尾由 agent 覆盖 |
| 术语登记块 | 译者只在**回报**里列候选词，不写进译文文件 | 写进文件会让段落数 +1 并触发结构自检 FAIL（`assemble.py` 仍会防御性剥离 `<<TERM>>`） |
| 标点规范 | 中文全角 + 中西文间半角空格 | 大陆技术出版物通行规范 |
| **接缝精确装配** | `assemble.py` 从英文原稿重新推导分块间的**原始空白**并逐字还原 | 有的接缝原文没有空行（如 `(label)=` 紧跟 `## 标题`），盲目用空行拼接会凭空多出 1 个段落。已用 `diff_paragraphs.py` 定位并修复 2 处 |
| **中文段落解折行** | `unwrap_cjk.py` 把中文段落内的软换行接成一行 | CommonMark 把段落内换行渲染成空格，硬折行的中文段落会到处出现多余空格。规则：两侧都是汉字/中文标点时接成 `""`，中↔西文边界保留换行（正好渲染成一个空格） |
| 行尾符 | 沿用英文原稿的 CRLF | 与仓库工作区一致，减少无谓 diff |
| 构建方式 | Python venv + `jupyter-book`（替代 Docker） | 本机 Docker 守护进程未运行；venv 完全等价且更快 |
| 交叉引用前缀 | `_config.yml` 的 `numfig_format` → 图/表/代码块/第 N 节 | 一处配置全书生效，避免逐处改 `{numref}` |
| 构建环境缓存 | `MPLCONFIGDIR` / `JUPYTER_*` / `UV_CACHE_DIR` 全部指向仓库内 | 文件沙箱禁止写入工作区之外；不固定这些路径会让构建以「PermissionError」神秘失败 |
| **排版缺陷看渲染层，不看源文件** | 新增 `html_qa.py`，直接读 `source/_build/html` 里的 `<p>` | 源文件层看不出缺陷：Markdown 的软换行、`**加粗**`、`[链接](url)`、`{numref}` 都是「隐形字符」，渲染后才会以空格的形式暴露。分批修复 503 → 214 → 最终归零，全靠这个工具量化 |
| **指令围栏里是散文，不是代码** | `unwrap_cjk.py` / `fix_spacing.py` 用 `fence_kind()` 区分：`{code-cell}`/裸 ```` ``` ```` 视为代码不动，`{note}`/`{figure}`/`{list-table}` 体内按散文处理 | 起初把所有围栏一律跳过，于是 note 正文与图注里的折行、多余空格全部漏网（审校 agent 只能逐处手改）。这类围栏里的内容是译出来的句子 |
| **`{numref}` 两侧空格方向相反** | 先用 `label_kinds()` 从文档本身解析每个标签的类型（`:name:` 选项、指令参数、`(label)=` 目标），再据此决定 | 角色的渲染结果由目标类型决定：图表目标是「图 5.1」（数字结尾，**要**留空格），节目标是「第 5.8 节」（汉字结尾，**不要**空格），自定义文本则看文本首尾。标签名不一定带 `fig:`/`tab:` 前缀（`confusion-matrix-table` 是表、`canadamap` 是图），只看前缀会判错方向 |
| **段落数按「未剥离角色」的行统计** | `verify_structure.py` 的段落计数改用 `prose_all`，不再用剥掉角色的 `prose_wo_roles` | 只含角色的整行（`{numref}`fig:x``）剥离后会变成空行，被误当成段落分隔——但渲染时它在行内，并不分段。按原文行统计才对得上渲染结果，且两种语言用同一规则，比较依然有效 |
| **承接行合并的幂等性** | `fix_spacing.py` 的 `{numref}` 处理改为**从右向左**应用 | 循环里会改写 `line`，若按 `finditer` 的正序取原始 span，右侧匹配的偏移已失效，会静默删掉该位置的任意文本。倒序处理时未处理的 span 全在左侧，始终有效 |
| **保护掩码里的 URL 不能写 `\S+`** | `term_fix.py` 的 `PROTECTED` 中 URL 规则改为 `https?://[^\s<CJK>]+` | 中文没有空格，`\S+` 会从 URL 一路吞掉后面整句话直到下一个空格，把整段中文都标记为「受保护」——于是任何 URL 之后的排版修复都被**静默否决**。这一条是最后 13 处残留的主因，从 503 收敛到 2 就是靠它 |
| **列表项续行也要解折行** | `unwrap_cjk.py` 新增 `LIST_ITEM_RE`：`- ` 开头的项行虽然算 STRUCT，仍允许吸收其后缩进的散文续行 | 渲染器把项内换行也渲染成空格，于是 `- …属性，` + 换行 + `需要借助…` 会出现多余空格。此前只从 TEXT 行起才尝试合并，这类续行全部漏掉 |
| **只含角色的整行可以合并** | 取消 `ROLE_ONLY_RE` 的拦截，改由边界规则决定 | 原来拦截是为了配合旧的段落模型（剥掉角色后空行会被当成段落分隔）。模型已改为按原文行计数，段落是「连续非空行的游程」，合并其中两行不改变游程数，因此拦截已无必要——而它能修掉「……两个新列。」+ 换行 + `{numref}` 产生的多余空格 |
| **标签表要按整本书构建** | `book_label_kinds(source_dir)` 汇总全部章节 | 标签会跨章引用：`wrangling` 里的 `{numref}`ch1-adding-modifying`` 声明在 `intro`。只按单章解析会解析不到，判定方向就反了 |
| **stderr 一律 remove** | `source/_config.yml` 的 `stderr_output`：`show` → `remove` | 本书产生的每一条 stderr 都是「库比书新」导致的 pandas/numpy 弃用警告，而且每条都以构建机本地路径开头（`C:\Users\…\ipykernel_…\1234.py:2: FutureWarning:`），泄漏的正是构建机本身。错误不受影响：nbformat 把错误记成 `error` 输出而不是 stderr，而书里故意演示了若干错误。见 §9.2 |
| **依赖版本必须固定** | `altair 5.5.0` / `plotly 5.24.1` / `numpy 1.26.4` / `pyarrow 25.0.1` / `pyarrow-hotfix 0.7` | 本书的输出与渲染通道对版本敏感：新库换了序列化通道（Altair ≥5.5 走 narwhals→Arrow）、换了 mime bundle（Plotly 7 只发 `application/vnd.plotly.v1+json`）、换了标量 repr（NumPy 2 的 NEP 51）。换版本 = 换输出，因此版本是「等价于上游 Dockerfile」的一部分。见 §9.1 |
| **代码与英文原稿逐字节一致** | 即使代码里有弃用写法也不改 | `verify_structure.py` 对每个代码块做哈希来强制这条不变量。译文的本分是翻译，不是替上游修代码；上游的真缺陷另行回报（§9.4）。渲染层的告警由 `stderr_output: remove` 消除，不需要动代码 |
| **URL 允许表（`URL_FIXES`）** | 只放过**登记在案**的上游 404 链接 | 上游地址失效后，改正过的译文会被判成结构差异，于是只能人工豁免——而被豁免的检查就没人看了。比较时两侧都过 `canon_url()` 归一化，其他任何未登记的 URL 差异仍然 FAIL。见 §9.3 |

---

## 5. 排错记录（这些坑都真实踩过）

| 症状 | 真正原因 | 处理 |
|---|---|---|
| `pip install` 跑十几分钟却什么都没装上 | 沙箱禁止写工作区外，pip 回退到 `--user` 安装被拒 | 一律用**仓库内**的 `.venv-build\Scripts\python.exe -m pip`；再用 `uv` 装依赖 |
| `uv` 报 `Failed to initialize cache ... Access is denied` | uv 默认缓存在用户目录 | 设 `UV_CACHE_DIR` 到仓库内 |
| 每个 notebook 执行都在启动内核时 `PermissionError: [WinError 5]` | `jupyter_core` 调 `SetFileSecurityW`（WRITE_DAC）做连接文件 ACL 加固，沙箱拒绝 | `tools/build_runner.py` 用普通上下文管理器替换 `secure_write`，其余行为不变 |
| `classification2` 里 `GridSearchCV(n_jobs=-1)` 的单元格抛 `PermissionError`，图未生成、`{numref}` 渲染成原始文本 | joblib 走 loky 进程池，工作进程与父进程之间的 IPC 被沙箱拒绝 | 构建时设 `LOKY_MAX_CPU_COUNT=1`：loky 探测到的 CPU 数变 1，`n_jobs=-1` 退化为进程内串行，数值结果不变 |
| 大量分块报 `directives FAIL`（`{index}` 词条） | 工具把指令 info 行的可见文本当成不可变选项 | 新增 `TITLED_DIRECTIVES`：`{index}`/`note`/`table` 等只比对指令名与选项，info 行文本视为可译 |
| 含 `\$`（转义美元）的块报 `math missing=extra` 成对出现 | `MATH_RE` 把转义的 `\$` 当成定界符，跨句吞掉中间散文 | 匹配前用 `ESCAPED_DOLLAR` 中和 |
| 分块自检报 `paragraphs EN=n ZH=n+1` | 译者在文件末尾追加了 `<<TERM>>` 登记块 | 工具侧剥离该块；规范改为「只在回报里登记」 |
| 整章装配后段落数比原文多 1 | 拼接时插入的换行改变了「无空行的接缝」 | §4 的「接缝精确装配」 |
| 机器翻译腔「一个预测变量的模型」被误判为冗长定语 | `AI_FLAVOR` 规则过宽、且能跨越句号匹配 | 收窄为 10–30 字且排除句末标点 |
| 英文书名《Good enough practices in scientific computing》被报未翻译 | 这是 STYLE_GUIDE §5.7 允许的例外 | linter 对 `《…》` 内的西文豁免 |
| `pip install` 完全无输出、无限挂起（`-v` 也一样） | 沙箱里 pip 访问 index 会挂死，而裸 `urllib` 不到一秒就能到 pypi.org | 新增 `tools/fetch_wheel.py`：从 PyPI JSON API 取 wheel URL 直接下载，再 `pip install --no-index --no-deps` 离线安装 |
| 下到 32 位 wheel，装不上 | 平台标签按**子串**匹配，`win` 会命中 `win32`，于是给 64 位解释器下了 32 位 wheel | `fetch_wheel.py` 的 `score()` 改为**精确**比较平台标签 |
| 空白图表、泄漏的警告路径、字面量 `**` 在旧门禁下**全部为绿** | 旧门禁只检查散文文本与链接目标，从不渲染，看不到「图没渲染出来」这类缺陷 | 见 §9：固定依赖版本 + `stderr_output: remove` + 四类渲染层检查 + 图表计数断言 + 强调标记检查 |

---

## 6. 复现命令

```powershell
# 0. 备份英文原文
Copy-Item source\*.md .translation\source_en\

# 1. 切块（无损自检）
python .translation\tools\segment.py source\intro.md .translation\work\intro --target 480 --soft-max 780

# 2. 术语表 + 每章摘录
python .translation\tools\merge_glossary.py
python .translation\tools\glossary_excerpt.py

# 3. 翻译：由 agent 写入 .translation\work\<chapter>\chunk_NN.zh.md

# 4. 装配（接缝精确 + 中文解折行）+ 机检
python .translation\tools\assemble.py

# 5. 全景状态 / 术语审计 / 强调标记
python .translation\tools\status.py --verify
python .translation\tools\term_audit.py --all-chapters
python .translation\tools\check_emphasis.py                                  # 中文译文（默认 source/）
python .translation\tools\check_emphasis.py --dir .translation\source_en      # 英文基准，必须为 0

# 6. 构建（Docker 的本地等价物）
pwsh -NoProfile -File .translation\tools\build_book.ps1

# 7. 渲染层门禁（必须在构建之后；数字记进 reports/html_qa.json）
python .translation\tools\html_qa.py --json .translation\reports\html_qa.json
```

装依赖（只需一次，全部落在仓库内）：

```powershell
.\.venv-build\Scripts\python.exe -m pip install --no-cache-dir uv
$env:UV_CACHE_DIR="$PWD\.uv-cache"; $env:UV_LINK_MODE="copy"
.\.venv-build\Scripts\python.exe -m uv pip install --python .\.venv-build\Scripts\python.exe -r .translation\requirements-build.txt

# 版本固定（§9.1 的清单；requirements-build.txt 只给范围，光装它还会拉到过新的版本）
.\.venv-build\Scripts\python.exe .translation\tools\fetch_wheel.py --install `
    pyarrow==25.0.1 altair==5.5.0 plotly==5.24.1 numpy==1.26.4 pyarrow-hotfix==0.7 tenacity tzdata
```

---

## 7. 目录约定

```
.translation/
  STYLE_GUIDE.md            翻译规范（权威）
  GLOSSARY_CORE.md          核心术语（总协调人）
  GLOSSARY.md               合并后的完整术语表（冻结，884 条）
  PROCESS.md                本文件
  requirements-build.txt    构建依赖清单（部分是范围而非固定版本，见 §9.1）
  glossary/part_*.md        领域术语抽取结果
  source_en/                英文原文备份（结构校验与审校的英文基准）
  prompts/
      TRANSLATOR.md         译者手册
      REVIEWER.md           审校员手册
  work/<chapter>/
      front_matter.txt      YAML front matter（原样保留，不参与翻译）
      chunk_NN.src.md       待译原文
      chunk_NN.ctx.md       前文只读上下文（帮助跨块连贯）
      chunk_NN.zh.md        译文（译者 agent 输出）
      glossary_excerpt.md   本章术语摘录
      chunks.json           切块元数据
      term_requests.md      译者回报的候选术语汇总
  tools/
      segment.py            切块（无损自检）
      verify_structure.py   结构比对（代码块哈希、URL 允许表 URL_FIXES）
      lint_zh.py            中文质量 lint
      check_emphasis.py     强调标记闭合检查（markdown-it 渲染散文块，找残留 `*`/`_`；英文原稿须为 0）
      assemble.py           装配（接缝精确 + 解折行）+ 门禁
      unwrap_cjk.py         中文段落解折行（围栏分类、`{numref}` 渲染方向、列表续行）
      diff_paragraphs.py    段落级差异定位
      fix_spacing.py        排版归一：中文间空格、`{numref}`/链接两侧、缺失的中西文空格
      html_qa.py            渲染层终检（排版 + 依赖/告警/路径/强调 + 全书图表计数）
      align_paragraphs.py   内容零丢失证明（段落数 + 角色目标多重集，按整本书）
      blocked_joins.py      诊断：哪些该合并的散文行被 classify() 判成了结构行
      trace_findings.py     诊断：把 html_qa 的渲染层发现反查回源文件行
      deploy_check.py        发布校验：抓取已发布页面的全部本地引用并逐个请求
      status.py             全书状态看板
      term_audit.py         跨章术语审计（按段对齐）
      term_fix.py           定点术语统一（跳过代码/角色/公式）
      glossary_excerpt.py   生成每章术语摘录
      merge_glossary.py     术语表合并与冲突检测
      build_book.ps1        构建（含沙箱兼容的环境变量，含 PYTHONUTF8=1）
      build_runner.py       构建入口（绕过 Windows ACL 加固）
      install_build_env.ps1 安装构建依赖
      fetch_wheel.py        绕过 pip 的 index：按 PyPI JSON API 直接下 wheel，再离线安装（平台标签精确匹配）
  reports/                  状态、审计与构建日志
```

## 8. 发布（GitHub Pages）

在线地址：**https://page.peler.top/introduction-to-datascience-python/**

| 事项 | 现状与理由 |
|---|---|
| Pages 来源 | 分支 `gh-pages-zh` 的 `/`（`build_type: legacy`）。**故意不用 `gh-pages`**：这个 fork 从上游继承了原作者的 `gh-pages` 分支（英文版部署，含 `CNAME` 指向他们的自定义域名），那是别人的产物，不该覆盖 |
| 访问地址 | 仓库所属账号配置了 Pages 自定义域名 `page.peler.top`，项目站点因此挂在它的子路径下。`https://peleryuan.github.io/introduction-to-datascience-python/` 会自动跳转到该地址 |
| `.nojekyll` | **必需**。Pages 默认走 Jekyll，而 Jekyll 会忽略所有以 `_` 开头的目录 —— 正好是 `_static`（样式/脚本）、`_sources`（页面源文件）、`_images`（全部插图）。没有这个标记，样式和图片会全部 404。已由 `build_book.ps1` 自动生成 |
| canonical 链接 | `add_canonical_links.py` 原先**硬编码** `https://python.datasciencebook.ca/`。这对原作者是对的，对译本则有害：canonical 指向另一语言的页面，等于告诉搜索引擎「本文的权威版本在英文站」，中文页会被当成重复内容而不再收录（跨语言对应关系应该用 `hreflang` 表达）。现在基准 URL 由 `--base-url` / `$env:DOCS_BASE_URL` 显式给出，**不给就一律移除 canonical**，保证 fork 不会静默误声明 |
| 部署方式 | 发布的是**已验收的构建产物**，而不是让 CI 重新构建。理由：本书对版本敏感（jupyter-book 0.15.1 / sphinx 5.0.2 / myst-nb 0.17.2），且 `execute_notebooks: auto` 会在构建时执行部分代码；CI 里重建等于引入一套未经验证的环境。产物与本地验收的完全一致 |

重新发布的完整流程：

```powershell
$env:DOCS_BASE_URL = "https://page.peler.top/introduction-to-datascience-python"
pwsh -NoProfile -File .translation\tools\build_book.ps1     # 构建 + canonical + .nojekyll
# 然后把 source/_build/html 的内容推到 gh-pages-zh（见 PROCESS.md 的发布步骤）
```

**改动正文后必须重新发布**，否则线上仍是旧版：`source/*.md` 是唯一权威源，Pages 上的是它的产物。

---

## 9. 外部评审回应（2026-09-26）

外部评审对上一版**已发布**构建提出的缺陷如下。它们有一个共同点：**源文件层的检查全部通过**。
旧门禁只检查散文文本与链接目标，从不渲染，因此空白图表、被贴进页面的依赖报错、泄漏的
警告路径、以及字面量 `**`，一个都看不见。

| 评审发现 | 根因 | 处理 |
|---|---|---|
| 101 张 Altair 图空白 | 构建环境**缺 `pyarrow`** | 装 `pyarrow 25.0.1` + `tzdata`（§9.1） |
| 3 张 Plotly 3-D 散点图空白 | `plotly 7.1.0` 的 notebook renderer 不再发 `text/html` bundle | 固定 `plotly 5.24.1`（§9.1） |
| ibis 一节整体失败 | `ibis-framework 12.0.0` 的 sqlite 后端需要 `pyarrow_hotfix` | 装 `pyarrow_hotfix 0.7`（§9.1） |
| 7 条 pandas/numpy 警告把构建机临时路径印进正文 | `stderr_output: show` 把 stderr 流原样留在页面里 | 改为 `remove`（§9.2） |
| 约 76 处 Markdown 强调标记被当字面文本渲染 | CommonMark 的 right-flanking 规则使中文标点结尾的 `**` 无法闭合 | 新增 `check_emphasis.py` 量化并兜住，修法见 §9.3 |
| 若干术语与上游原文缺陷 | 原文自身的错误，以及旧译法不一致 | 见 §9.4 |

### 9.1 构建环境版本修正

上游权威构建走仓库的 `Dockerfile`；本机没有 Docker，`.venv-build` 是它的近似物。
评审后修正的版本如下（当前 venv 实测值，`pip list` 可核对）。每一条的理由都是
「更新的库改变了渲染通道或输出格式」，跟「新版本更好」无关。

| 库 | 修正前 | 现在 | 症状与原因 |
|---|---|---|---|
| `pyarrow` | **缺失** | `25.0.1`（+ `tzdata`） | 每个 Altair 单元格抛 `ImportError: Missing optional dependency 'pyarrow'`。Altair ≥5.5 通过 narwhals→Arrow 序列化图表数据，没有 pyarrow 时 `Chart._repr_mimebundle_()` 根本产不出 `text/html` bundle，myst-nb 也就没有东西可渲染。装上后 101 张空白图恢复；可视化那一章 `.save("img/...png")` 的失败是同一个 `ImportError`，一并解决 |
| `altair` | `6.2.2` | `5.5.0` | 6.2.2 比书本身新，渲染行为与书中的输出不一致；固定到书所用的系列 |
| `plotly` | `7.1.0` | `5.24.1`（需 `tenacity`） | myst-nb **没有** `application/vnd.plotly.v1+json` 的处理器：Plotly 只能通过 notebook renderer **另外**产出的 `text/html` bundle 进入 Jupyter Book 页面。Plotly 7 的 renderer 只发 vnd mime，于是 3 张 3-D 散点图渲染成空。5.24.1 的 renderer 会重新发出 `text/html` |
| `numpy` | `2.2.6` | `1.26.4` | NumPy 2 的 NEP 51 标量 repr 把 9 处输出印成 `np.float64(0.12)` 而不是 `0.12`，与英文书的输出对不上 |
| `ibis-framework` | `12.0.0`（保留） | `12.0.0` + `pyarrow_hotfix 0.7` | 12.0.0 仍有该章需要的 `.compile()`，但它的 sqlite 后端在 import 时需要 `pyarrow_hotfix`，缺了就整节失败 |

ibis 一节逐项复核（全部通过）：

- `ibis.sqlite.connect("source/data/can_lang.db")` 可连接；
- `list_tables() == ["can_lang"]`；
- 表的 repr 为 `DatabaseTable: can_lang`；
- `count().execute() == 214`，与正文叙述一致；
- `str(expr.compile())` 产出 SQL；
- `hasattr(table, "tail")` 为 `False` —— 这正是该章的讲解点。

沙箱里 `pip` 访问 index 会**无限挂起**（连 `-v` 都不产生任何输出），而裸 `urllib`
不到一秒就能到 pypi.org。因此新增 `tools/fetch_wheel.py`：按 PyPI JSON API 解析 wheel
URL、用 `urllib` 直接下载，再用 `pip install --no-index --no-deps` 离线安装。一个细节：
平台标签**精确**比较 —— 曾按子串匹配，于是给 64 位解释器下了一个 32 位 `win32` wheel
（`win` 命中 `win32`），pip 拒绝安装，下载白费。

遗留待办：`.translation/requirements-build.txt` 里 `altair>=5.1.2`、`plotly`、`numpy`、
`ibis-framework` 仍是范围而非固定版本，只按它安装会再次拉到过新的库。§9.1 的清单目前
只存在于已装好的 `.venv-build` 环境里，尚未写回该文件（见 §6 的固定版本命令）。

### 9.2 构建配置修正

| 改动 | 位置 | 理由 |
|---|---|---|
| `stderr_output`：`show` → `remove` | `source/_config.yml` | 本书产生的**每一条** stderr 都是「库比书新」导致的 pandas/numpy 弃用警告，而且每条都以构建机本地路径开头（`C:\Users\…\Temp\…\ipykernel_…\1234.py:2: FutureWarning: …`）。错误不受影响：nbformat 把错误记成 `error` 输出而不是 stderr，而书里故意演示了若干错误，必须保留 |
| 新增 `PYTHONUTF8=1` | `tools/build_book.ps1` | 有一个单元格打开 HTML 文件时没有指定编码：在 Linux（默认 UTF-8）下是对的，Windows cp1252 下抛 `UnicodeDecodeError: 'charmap' codec can't decode byte 0x8d`，并把回溯贴进页面。打开 UTF-8 模式后解释器的行为与作者机器一致，单元格正常执行 |

这两项只处理**泄漏进页面的文本**。构建日志里的警告条数需重建后按 `reports/build.log` 重新统计：
§3.1 原先记的「9 条警告」是评审前的数字，不再作为基线。

### 9.3 新增与扩展的门禁

**旧门禁看不见上面任何一条**，因为它们只检查散文文本与链接目标，从不渲染。

`html_qa.py`（渲染层，扩展）新增四类检查与一项断言：

| 代码 | 抓什么 |
|---|---|
| `RENDERED_IMPORTERROR` | 被贴进页面的 `ImportError` / `ModuleNotFoundError`。缺依赖就是这么藏起来的：图不渲染，取而代之的是一条错误输出 |
| `RENDERED_WARNING` | 库比书新导致的 pandas/numpy 告警 |
| `RENDERED_PATH` | 构建机自己的文件系统路径 |
| `RENDERED_EMPHASIS` | 渲染后仍留在散文里的 `*` / `_`（`*args` / `**kwargs` 是真正的 Python 语法，已排除） |
| `MISSING_CHARTS` | 断言全书渲染出的 Altair 图 **≥ 80**（`VEGA_MIN`；英文书为 84）、Plotly 图 **≥ 3**（`PLOTLY_MIN`）。图表计数同时写进 `--json` 报告（`vega_embed_total` / `plotly_total` / `vega_embed_pages`），可逐页核对 |

两条规则是**刻意收窄**的：`RENDERED_WARNING` 只匹配真正泄漏的形态 `…py:2: FutureWarning:`，
`RENDERED_PATH` 只匹配构建机自己的临时路径。因为书中正文本来就**点名**了
`SettingWithCopyWarning`，也本来就告诉读者去输入 `/home/jovyan/work` —— 第一版按裸名字匹配时，
这两处都成了假阳性，而且是永久告警。另外，报告在干净的运行里也会照常写盘：只在有发现时才写，
会让上一次的报告留在原地，把已经不存在的缺陷当成绿灯。

`check_emphasis.py`（**新增**）用 markdown-it-py 逐块渲染散文，报告 Markdown 强调**没能闭合**的情况。
规则是 CommonMark 的 right-flanking：收尾的 `**` 若前面是标点（`：`、`）` 等）、后面又紧跟汉字，
就不是合法的闭合，星号会原样印在正文里（`**汇总：**计算……`）。它同时报告 `SPAN`：
本意的开标记配到了更后面的收尾标记，于是**整段**被加粗（只报 `<strong>`；长 `<em>` 往往是有意
排成斜体的引文，报了反而淹没真问题）。

两处细节：数学公式在渲染**前**先挖掉 —— CommonMark 不解析 `$…$`，`CO$_{\text{2}}$` 的下划线
看起来和泄漏的 `_` 一模一样，英文原稿里那 15 处假阳性全出自这里；代码围栏整体跳过，
围栏里的 `*` 是数据不是标记。

校验方式是拿英文原稿当基准：必须报 0。实测 `.translation/source_en` 的 18 章为
`total: 0 leaked marker(s), 0 over-long span(s) in 18 file(s)`。

修法是把标点移到强调之外：`**X：**Y` → `**X**：Y`；或只加粗中文术语：
`**X（E）**Y` → `**X**（E）Y`。工具在报错末尾直接提示这两条。

`verify_structure.py`（扩展）新增 `URL_FIXES`，一份**登记在案**的 URL 允许表：只有上游地址
404、译文有意改用新地址时才登记。

| 上游地址（已 404） | 译文使用 |
|---|---|
| `https://scikit-learn.org/stable/tutorial/index.html` | `https://scikit-learn.org/stable/` |
| `https://altair-viz.github.io/user_guide/marks.html` | `https://altair-viz.github.io/user_guide/marks/index.html` |

比较时两侧都过 `canon_url()` 归一化，所以任何**其他**未登记的 URL 差异仍然 FAIL ——
否则改正过的译文会被判成结构差异，只能人工豁免，而「被豁免的检查就没人看了」。

### 9.4 有意保留的偏差

| 偏差 | 为什么不动 |
|---|---|
| `classification2.md` 的两处链式赋值（`cv_10_metrics["test_score"]["sem"] = …`，第 756 行；`cv_50_metrics[…]`，第 782 行）**没有**按评审建议改写成 `.loc[…]` | 代码必须与英文原稿逐字节一致，`verify_structure.py` 对每个代码块做哈希来强制这条不变量。它们产生的警告已在渲染层由 `stderr_output: remove` 消除，改写反而会破坏代码同一性。<br>另记：这两条在 pandas 3.0 下会**真正失效**（不再只是警告），这是上游的前向兼容问题，值得回报上游 |
| 上游作者的错误予以修正：`estimator` / `param_grid` 顺序写反、`range` 参数讲错、`CCS` 写成 CSS、`Craiglist`、`20,0000`、`MacOS`、重复的图题、重复的 PEP 8 句子等 | 这是原文的错误，照译等于把错误传给读者。**实质性**错误在正文里留一句简短译注 `（译注：…）`（如 `range` 参数、`estimator`/`param_grid` 顺序）；纯拼写与排版类错误静默修正，不加注 |
| 评审提出的术语问题按术语表收口，不逐处加注 | 术语一致性由 `GLOSSARY.md` 与 `term_audit.py` 统一约束（§3.1），逐个加译注会把一致性重新打散 |

### 9.5 本次修订的实测数字记在哪里

本次修订的最终数字要等**重建 + 重跑全部门禁**之后才有，这里不预先填写：

| 数字 | 记录位置 |
|---|---|
| 渲染图数（Altair / Plotly 总计与逐页分布）、全部渲染层发现 | `.translation/reports/html_qa.json`（`vega_embed_total` / `plotly_total` / `vega_embed_pages` / `findings`） |
| 中文译文的强调标记残留数 | `check_emphasis.py` 的输出（英文基准已实测为 0） |
| 结构比对结果（含 `URL_FIXES`） | `verify_structure.py --json` 的输出，归档到 `.translation/reports/` |
| 构建退出码与警告条数 | `.translation/reports/build.log` |
| 发布校验（页面数、引用数） | 重建后重跑 `deploy_check.py`；§3.1 里的「20 页 / 187 个引用」是评审前那次构建的数字 |