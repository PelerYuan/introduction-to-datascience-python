#!/usr/bin/env python3
"""Cross-chapter terminology audit using paragraph alignment.

verify_structure.py guarantees that each chapter's English and Chinese versions have
the same number of paragraphs with the same structure, so paragraph *i* of the English
chapter corresponds to paragraph *i* of the Chinese one. That alignment lets us find,
for a given English term, which Chinese rendering the translator actually used — and
catch terms that drifted between chapters.

Usage:
    python term_audit.py                 # audit the built-in term list
    python term_audit.py --term "scale"  # focus on one term
    python term_audit.py --json out.json
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_structure as vs  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / ".translation"

CHAPTERS = [
    "index", "preface-text", "foreword-text", "acknowledgements", "authors",
    "intro", "reading", "wrangling", "viz", "classification1", "classification2",
    "regression1", "regression2", "clustering", "inference", "jupyter",
    "version-control", "setup",
]

# (English term, [acceptable Chinese renderings]; first entry is canonical)
AUDIT: list[tuple[str, list[str]]] = [
    ("k-nearest neighbour", ["k 近邻", "K-NN", "KNN", "k近邻"]),
    ("k-means", ["k 均值聚类", "k-means", "K-means", "k均值聚类"]),
    ("flipper length", ["鳍肢长", "翼长"]),
    ("bill length", ["喙长", "嘴长"]),
    ("concavity", ["凹度", "凹陷度"]),
    ("smoothness", ["光滑度", "平滑度"]),
    ("compactness", ["紧密度", "致密度"]),
    ("symmetry", ["对称性", "对称度"]),
    ("scale", ["标度", "尺度"]),
    ("standardize", ["标准化", "标准化处理"]),
    ("transformer", ["变换器", "转换器"]),
    ("summary", ["小结", "总结", "摘要"]),
    ("worksheet", ["练习册"]),
    ("primary language at home", ["在家主要使用的语言", "在家主要语言", "家中主要语言"]),
    ("accuracy", ["准确率", "精确度", "正确率"]),
    ("precision", ["精确率", "查准率"]),
    ("recall", ["召回率", "查全率"]),
    ("tuning parameter", ["调优参数", "调节参数"]),
    ("predictor", ["预测变量", "自变量"]),
    ("response variable", ["响应变量", "因变量"]),
    ("tidy data", ["整洁数据", "整齐数据"]),
    ("data frame", ["数据框", "数据帧"]),
    ("series", ["序列", "系列"]),
    ("wrangling", ["数据清洗", "数据整理"]),
    ("bootstrap", ["自助法", "自举"]),
    ("sampling distribution", ["抽样分布"]),
    ("sample distribution", ["样本分布"]),
    ("confidence interval", ["置信区间"]),
    ("centroid", ["质心", "簇中心", "聚类中心"]),
    ("elbow", ["肘部"]),
    ("overfitting", ["过拟合"]),
    ("underfitting", ["欠拟合"]),
    ("cross-validation", ["交叉验证"]),
    ("pipeline", ["流水线", "管道"]),
    ("random seed", ["随机种子", "随机数种子"]),
    ("point estimate", ["点估计"]),
    ("standard error", ["标准误"]),
    ("outlier", ["离群值", "异常值"]),
    ("multicollinearity", ["多重共线性", "共线性"]),
    ("domain", ["取值范围", "定义域"]),
    ("facet", ["分面", "小图"]),
    ("layer", ["图层"]),
    ("aesthetic", ["图形属性"]),
    ("tick", ["刻度"]),
    ("legend", ["图例"]),
    ("missing value", ["缺失值", "丢失值"]),
    ("distribution", ["分布"]),
    ("histogram", ["直方图"]),
    ("boxplot", ["箱线图", "盒须图"]),
    ("scatterplot", ["散点图"]),
    ("bar chart", ["条形图", "柱状图"]),
    ("classification", ["分类"]),
    ("regression", ["回归"]),
    ("cluster", ["簇", "聚类"]),
    ("version control", ["版本控制"]),
    ("repository", ["仓库"]),
    ("notebook", ["笔记本", "练习册"]),
]


def paras(path: Path) -> list[str]:
    return vs.structure(path.read_text(encoding="utf-8"))["paragraph_list"]


def audit(only: str | None) -> dict:
    cache: dict[str, tuple[list[str], list[str]]] = {}
    for ch in CHAPTERS:
        en = TR / "source_en" / f"{ch}.md"
        zh = ROOT / "source" / f"{ch}.md"
        if not (en.exists() and zh.exists()):
            continue
        a, b = paras(en), paras(zh)
        cache[ch] = (a, b)

    report: dict = {}
    for term, variants in AUDIT:
        if only and only.lower() not in term.lower():
            continue
        rx = re.compile(r"(?<![A-Za-z])" + re.escape(term).replace(r"\ ", r"\s+") + r"(?![A-Za-z])",
                        re.IGNORECASE)
        counts = collections.Counter()
        per_chapter: dict[str, collections.Counter] = {}
        for ch, (a, b) in cache.items():
            if len(a) != len(b):
                continue
            for i, en_p in enumerate(a):
                if not rx.search(en_p):
                    continue
                zh_p = b[i]
                for v in variants:
                    n = zh_p.count(v)
                    if n:
                        counts[v] += n
                        per_chapter.setdefault(ch, collections.Counter())[v] += n
        if counts:
            report[term] = {
                "totals": dict(counts),
                "chapters": {c: dict(v) for c, v in per_chapter.items()},
            }
    return report


# English words that legitimately map to more than one Chinese rendering because the
# source itself distinguishes the senses. Listing them here keeps the audit honest:
# anything NOT listed still reports as drift.
ACCEPTED_POLYSEMY = {
    # The book's own chapter title is "Cleaning and wrangling data": cleaning = 清洗,
    # wrangling = 整理, and the two are used contrastively throughout.
    "wrangling": {"数据清洗", "数据整理"},
    # "Summary" as a section heading vs. the verb "summarizes" vs. a data summary.
    "summary": {"小结", "总结", "摘要"},
    # The act of clustering vs. the resulting group.
    "cluster": {"聚类", "簇"},
    # Every chapter writes 「k 均值聚类」 and keeps the English term once, as the
    # first-occurrence gloss 「k 均值聚类（k-means clustering）」.
    "k-means": {"k 均值聚类", "k-means"},
    # Jupyter notebook vs. the book's worksheet (练习册) — distinct source words.
    "notebook": {"笔记本", "练习册"},
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--term", default=None)
    ap.add_argument("--json", type=Path, default=None)
    ap.add_argument("--all-chapters", action="store_true",
                    help="show per-chapter breakdown for every term")
    args = ap.parse_args()

    rep = audit(args.term)
    divergent = []
    for term, data in rep.items():
        # A rendering that is a substring of another one is the same word seen twice:
        # 共线性 inside 多重共线性 is not a second rendering, it is an artefact of
        # substring search. Drop those before judging.
        raw = list(data["totals"].keys())
        used = [u for u in raw if not any(u != o and u in o for o in raw)]
        canon = AUDIT and next(v for t, v in AUDIT if t == term)[0]
        allowed = {canon} | ACCEPTED_POLYSEMY.get(term, set())
        flag = ""
        if len(used) > 1:
            if set(used) <= allowed:
                flag = "  (accepted polysemy)"
            else:
                flag = "  <== DIVERGENT"
                divergent.append(term)
        elif used and used[0] != canon and used[0] not in allowed:
            flag = f"  <== canonical is {canon!r}"
            divergent.append(term)
        print(f"{term:<28} {data['totals']}{flag}")
        if args.all_chapters and len(used) > 1:
            for c, v in data["chapters"].items():
                print(f"      {c:<18} {v}")
    print(f"\n{len(rep)} terms audited, {len(divergent)} need attention: {divergent}")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())