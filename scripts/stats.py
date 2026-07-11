#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 文章统计 - 字数/句数/段落/句长等

import re, sys

def stats(text):
    chars = len(text.replace("\n", "").replace(" ", "").replace("\r", ""))
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    para_count = len(paras)
    sents = [s.strip() for s in re.split("[\u3002\uff01\uff1f\uff1b\u2026]+", text) if s.strip()]
    sent_count = len(sents)
    sent_lens = [len(s) for s in sents]
    avg_len = round(sum(sent_lens) / sent_count, 1) if sent_count else 0
    max_len = max(sent_lens) if sent_lens else 0
    parens = text.count("(") + text.count("\uff08") + text.count(")") + text.count("\uff09")
    punct = len(re.findall("[\u3001\uff0c\u3002\uff01\uff1f\uff1b\uff1a\u2026\u2014\u2018\u2019\u201c\u201d]", text))

    print(f"\u603b\u5b57\u6570: {chars}")
    print(f"\u6bb5\u843d\u6570: {para_count}")
    print(f"\u603b\u53e5\u6570: {sent_count}")
    print(f"\u5e73\u5747\u53e5\u957f: {avg_len} \u5b57")
    print(f"\u6700\u957f\u53e5: {max_len} \u5b57")
    print(f"\u62ec\u53f7\u4f7f\u7528: {parens} \u6b21")
    print(f"\u6807\u70b9\u603b\u6570: {punct} \u6b21")

    long_sents = [(i+1, l, s[:60]) for i, (l, s) in enumerate(zip(sent_lens, sents)) if l > 100]
    if long_sents:
        print()
        print("\u26a0\ufe0f \u8d85\u957f\u53e5\u5b50\uff08>100 \u5b57\uff09:")
        for idx, l, s in long_sents[:5]:
            print(f"  \u7b2c{idx}\u53e5 ({l}\u5b57): {s}...")

if __name__ == "__main__":
    stats(sys.stdin.read())
