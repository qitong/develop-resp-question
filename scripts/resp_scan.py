#!/usr/bin/env python3
"""resp_scan.py — 呼吸科研究问题的“证据地形”快速扫描（仅用标准库）。

聚合 PubMed、Europe PMC 预印本和 ClinicalTrials.gov v2，输出 Markdown。
所有数字都是检索时点的粗略地形，不能替代系统检索或原文阅读。
"""
import argparse
import datetime as dt
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter

UA = {"User-Agent": "resp_scan/1.0 (research-question coaching)"}
THIS_YEAR = dt.date.today().year
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode())


def safe(section):
    def deco(fn):
        def wrap(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:
                return f"## {section}\n\n> 查询失败：{exc}\n"
        return wrap
    return deco


def pm_count(term):
    query = urllib.parse.urlencode({
        "db": "pubmed", "term": term, "retmode": "json", "retmax": 0
    })
    time.sleep(0.35)
    return int(_get(f"{EUTILS}/esearch.fcgi?{query}")["esearchresult"]["count"])


def pm_recent(term, n=8):
    query = urllib.parse.urlencode({
        "db": "pubmed", "term": term, "retmode": "json",
        "retmax": n, "sort": "pub_date"
    })
    time.sleep(0.35)
    ids = _get(f"{EUTILS}/esearch.fcgi?{query}")["esearchresult"]["idlist"]
    if not ids:
        return []
    time.sleep(0.35)
    summary = _get(
        f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(ids)}"
    )["result"]
    return [
        (pmid, summary[pmid].get("pubdate", ""),
         summary[pmid].get("source", ""), summary[pmid].get("title", ""))
        for pmid in ids
    ]


@safe("PubMed 文献地形")
def pubmed_section(base, years):
    first_year = THIS_YEAR - years + 1
    rows = [
        ("全部", base),
        (f"近 {years} 年", f"({base}) AND {first_year}:{THIS_YEAR}[dp]"),
        ("RCT", f"({base}) AND randomized controlled trial[pt]"),
        ("Meta 分析 / 系统评价", f"({base}) AND (meta-analysis[pt] OR systematic review[pt])"),
        ("综述", f"({base}) AND review[pt]"),
        ("指南 / 共识", f"({base}) AND (guideline[pt] OR practice guideline[pt] OR consensus[ti])"),
        ("队列 / 真实世界信号", f"({base}) AND (cohort OR registry OR real-world OR retrospective)"),
    ]
    out = [f"## PubMed 文献地形\n\n检索式：`{base}`\n", "| 类别 | 篇数 |", "|---|---|"]
    for name, term in rows:
        out.append(f"| {name} | {pm_count(term)} |")
    trend = []
    for year in range(THIS_YEAR - 4, THIS_YEAR + 1):
        trend.append(f"{year}: {pm_count(f'({base}) AND {year}[dp]')}")
    out.append("\n**年度趋势**：" + " · ".join(trend))
    out.append("\n**最新文献**：")
    for pmid, date, source, title in pm_recent(base):
        out.append(
            f"- {date} *{source}* — {title} "
            f"(PMID [{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/))"
        )
    out.append("\n**最新 RCT**：")
    for pmid, date, source, title in pm_recent(
        f"({base}) AND randomized controlled trial[pt]", 5
    ):
        out.append(
            f"- {date} *{source}* — {title} "
            f"(PMID [{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/))"
        )
    return "\n".join(out) + "\n"


@safe("预印本（Europe PMC）")
def preprint_section(query):
    params = urllib.parse.urlencode({
        "query": f"({query}) AND SRC:PPR", "format": "json",
        "pageSize": 6, "sort": "FIRST_PDATE_D desc"
    })
    data = _get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{params}")
    out = [
        f"## 预印本（Europe PMC）\n\n检索：`{query}`，"
        f"共 {data.get('hitCount', 0)} 篇，最新：\n"
    ]
    for item in data.get("resultList", {}).get("result", []):
        publisher = item.get("bookOrReportDetails", {}).get(
            "publisher", item.get("source", "")
        )
        out.append(
            f"- {item.get('firstPublicationDate', '')} *{publisher}* — "
            f"{item.get('title', '')} ({item.get('doi', item.get('id', ''))})"
        )
    out.append("\n> 预印本未经同行评议，只作为领域方向信号。")
    return "\n".join(out) + "\n"


@safe("在研 / 已注册试验（ClinicalTrials.gov）")
def ctgov_section(condition, intervention, other, max_fetch=300):
    params = {
        "pageSize": 100,
        "countTotal": "true",
        "fields": "NCTId,BriefTitle,OverallStatus,Phase,StartDate,EnrollmentCount,LeadSponsorName,LocationCountry",
    }
    if condition:
        params["query.cond"] = condition
    if intervention:
        params["query.intr"] = intervention
    if other:
        params["query.term"] = other
    studies, token, total = [], None, 0
    while True:
        page_params = dict(params)
        if token:
            page_params["pageToken"] = token
        data = _get(
            "https://clinicaltrials.gov/api/v2/studies?"
            + urllib.parse.urlencode(page_params)
        )
        total = data.get("totalCount", total)
        studies += data.get("studies", [])
        token = data.get("nextPageToken")
        if not token or len(studies) >= max_fetch:
            break

    def get(study, *path, default=""):
        current = study.get("protocolSection", {})
        for key in path:
            current = current.get(key, {}) if isinstance(current, dict) else {}
        return current or default

    status = Counter(get(s, "statusModule", "overallStatus") for s in studies)
    phase = Counter(
        "/".join(get(s, "designModule", "phases", default=["NA"]))
        for s in studies
    )
    countries = Counter()
    for study in studies:
        locations = get(study, "contactsLocationsModule", "locations", default=[])
        for country in {loc.get("country") for loc in locations if loc.get("country")}:
            countries[country] += 1
    active_statuses = {
        "RECRUITING", "NOT_YET_RECRUITING", "ACTIVE_NOT_RECRUITING",
        "ENROLLING_BY_INVITATION"
    }
    active = [
        s for s in studies
        if get(s, "statusModule", "overallStatus") in active_statuses
    ]
    active.sort(
        key=lambda s: get(s, "statusModule", "startDateStruct", "date"),
        reverse=True
    )

    query_label = " / ".join(
        label for label in [
            f"疾病={condition}" if condition else "",
            f"干预={intervention}" if intervention else "",
            f"其他={other}" if other else "",
        ] if label
    )
    out = [
        f"## 在研 / 已注册试验（ClinicalTrials.gov）\n\n检索：{query_label}；"
        f"共 **{total}** 项（统计基于前 {len(studies)} 项）\n",
        "**状态**：" + "，".join(f"{k} {v}" for k, v in status.most_common()),
        "\n**分期**：" + "，".join(f"{k} {v}" for k, v in phase.most_common()),
        "\n**主要国家**：" + "，".join(f"{k} {v}" for k, v in countries.most_common(8)),
        f"\n**正在进行 / 即将开始（{len(active)} 项，按开始日期倒序，列前 15）**：\n",
        "| NCT | 分期 | 状态 | 开始 | 样本量 | 申办方 | 标题 |",
        "|---|---|---|---|---|---|---|",
    ]
    for study in active[:15]:
        nct = get(study, "identificationModule", "nctId")
        out.append("| [{0}](https://clinicaltrials.gov/study/{0}) | {1} | {2} | {3} | {4} | {5} | {6} |".format(
            nct,
            "/".join(get(study, "designModule", "phases", default=["NA"])),
            get(study, "statusModule", "overallStatus"),
            get(study, "statusModule", "startDateStruct", "date"),
            get(study, "designModule", "enrollmentInfo", "count"),
            get(study, "sponsorCollaboratorsModule", "leadSponsor", "name"),
            get(study, "identificationModule", "briefTitle").replace("|", "/"),
        ))
    out.append(
        "\n> 中国研究者注意：另查 ChiCTR（https://www.chictr.org.cn/）和 "
        "WHO ICTRP（https://trialsearch.who.int/），并比较入排、背景治疗、T0 与终点。"
    )
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description="呼吸科研究问题证据地形扫描")
    parser.add_argument("--condition", help="疾病，英文，如 'progressive pulmonary fibrosis'")
    parser.add_argument("--intervention", help="干预/药物，如 'nintedanib'")
    parser.add_argument("--pubmed", help="自定义 PubMed 检索式（覆盖自动生成）")
    parser.add_argument("--pubmed-extra", help="追加到自动 PubMed 检索式的 AND 条件")
    parser.add_argument("--ct-term", help="ClinicalTrials.gov 额外关键词（query.term）")
    parser.add_argument("--years", type=int, default=5)
    parser.add_argument("--skip", default="", help="跳过数据源，逗号分隔：pubmed,preprint,ctgov")
    parser.add_argument("-o", "--output", help="输出 Markdown 文件路径")
    args = parser.parse_args()
    if args.years < 1:
        parser.error("--years 必须大于等于 1")
    skip = set(filter(None, args.skip.split(",")))
    unknown = skip - {"pubmed", "preprint", "ctgov"}
    if unknown:
        parser.error("未知 --skip 数据源：" + ",".join(sorted(unknown)))

    base = args.pubmed or " AND ".join(
        f"({value})" for value in [args.condition, args.intervention, args.pubmed_extra]
        if value
    )
    parts = [
        f"# 呼吸科证据地形扫描\n\n生成时间：{dt.datetime.now():%Y-%m-%d %H:%M}　|　"
        f"疾病：{args.condition or '-'}　|　干预：{args.intervention or '-'}\n"
    ]
    if base and "pubmed" not in skip:
        parts.append(pubmed_section(base, args.years))
    if base and "preprint" not in skip:
        parts.append(preprint_section(base))
    if (args.condition or args.intervention or args.ct_term) and "ctgov" not in skip:
        parts.append(ctgov_section(args.condition, args.intervention, args.ct_term))
    if len(parts) == 1:
        parser.error("没有可执行的数据源：请提供 --condition、--intervention、--pubmed 或 --ct-term")
    parts.append(
        "---\n*本报告为自动检索的粗略地形，仅供选题讨论；"
        "关键判断须回到原文、指南与系统检索。*\n"
    )
    markdown = "\n".join(parts)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(markdown)
        print(f"已写入 {args.output}", file=sys.stderr)
    print(markdown)


if __name__ == "__main__":
    main()
