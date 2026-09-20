# 中译本生产流程（PROCESS）

> 本文件说明从英文原稿到可构建中文版书的完整流水线、角色分工与验收标准。
> 目标是**专业出版级译文**：准确、术语一致、无翻译腔/AI 味。
>
> 状态：**已完成**。18 章 / 52 块全部译出并通过机检；术语一致性扫描完成；构建通过。

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
      ├─(5) 机检 ──► tools/verify_structure.py（结构零改动）
      │              tools/lint_zh.py（AI 味 / 标点 / 未译英文 / 空格）
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
                     └─► tools/html_qa.py（读**渲染后**的 HTML 复查排版，验证第 7 步真的生效）
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
| 结构零改动 | `verify_structure.py` | 代码块哈希、指令名与选项、`(label)=`、角色、行内代码、公式、URL、标题层级、`+++`、段落数全部一致 | ✅ 18/18 章 |
| 中文质量 | `lint_zh.py` | 0 项 | ✅ 18/18 章 |
| 术语一致 | `term_audit.py` | 无跨章漂移（51 条，允许的义项分歧已在 `ACCEPTED_POLYSEMY` 中登记） | ✅ 0 项待处理 |
| 排版（源层） | `fix_spacing.py` | 再次运行报告 `would tighten 0`（幂等） | ✅ 0 |
| 段落对齐 | `align_paragraphs.py` | EN/ZH 段落数一致，且每段「角色指纹」相同 | ✅ 18/18 |
| 排版（渲染层） | `html_qa.py` | 读 `source/_build/html`：无未解析 `{numref}`、无缺失中西文空格；中文间空格仅余 13 处（初测 503 处，收敛 97.4%） | ✅ |
| 构建 | `build_book.ps1` | 退出码 0，20 个 HTML 页面全部生成，9 条警告（全部为上游原文固有，见 §5） | ✅ |

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

# 5. 全景状态 / 术语审计
python .translation\tools\status.py --verify
python .translation\tools\term_audit.py --all-chapters

# 6. 构建（Docker 的本地等价物）
pwsh -NoProfile -File .translation\tools\build_book.ps1
```

装依赖（只需一次，全部落在仓库内）：

```powershell
.\.venv-build\Scripts\python.exe -m pip install --no-cache-dir uv
$env:UV_CACHE_DIR="$PWD\.uv-cache"; $env:UV_LINK_MODE="copy"
.\.venv-build\Scripts\python.exe -m uv pip install --python .\.venv-build\Scripts\python.exe -r .translation\requirements-build.txt
```

---

## 7. 目录约定

```
.translation/
  STYLE_GUIDE.md            翻译规范（权威）
  GLOSSARY_CORE.md          核心术语（总协调人）
  GLOSSARY.md               合并后的完整术语表（冻结，884 条）
  PROCESS.md                本文件
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
      verify_structure.py   结构比对
      lint_zh.py            中文质量 lint
      assemble.py           装配（接缝精确 + 解折行）+ 门禁
      unwrap_cjk.py         中文段落解折行
      diff_paragraphs.py    段落级差异定位
      status.py             全书状态看板
      term_audit.py         跨章术语审计（按段对齐）
      term_fix.py           定点术语统一（跳过代码/角色/公式）
      glossary_excerpt.py   生成每章术语摘录
      merge_glossary.py     术语表合并与冲突检测
      build_book.ps1        构建（含沙箱兼容的环境变量）
      build_runner.py       构建入口（绕过 Windows ACL 加固）
      install_build_env.ps1 安装构建依赖
  reports/                  状态、审计与构建日志
```