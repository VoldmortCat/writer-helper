#!/usr/bin/env python3
"""
AI 写作搭子 — 一致性检查脚本
v1.0

功能：检查长篇写作中前后不一致的问题
- 人物设定矛盾（外貌/性格/能力/关系）
- 情节逻辑漏洞（时间线/因果关系）
- 伏笔回收情况（前文埋的线后面收了没有）
- 细节前后照应（物件/地名/日期写错）

用法:
  python consistency_check.py --files "第1章.md,第2章.md,第3章.md"
  python consistency_check.py --dir 小说目录/
  python consistency_check.py --files ch1.md,ch2.md --detail
"""

import argparse
import json
import os
import re
import sys
import requests

API_KEY = os.environ.get("WRITING_BUDDY_API_KEY", "")
API_BASE = os.environ.get("WRITING_BUDDY_API_BASE", "https://api.deepseek.com")
MODEL = os.environ.get("WRITING_BUDDY_MODEL", "deepseek-chat")


def call_llm(system_prompt: str, user_prompt: str) -> str:
    if not API_KEY:
        return "[ERROR] 请先设置环境变量 WRITING_BUDDY_API_KEY"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 3000
    }
    try:
        resp = requests.post(
            f"{API_BASE.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR] API 调用失败: {e}"


SYSTEM_CONSISTENCY = """你是一个小说连续性编辑。你的任务是检查多章文本之间的前后一致性。

请检查以下四类问题：

1. 人物设定矛盾
   同一个角色在不同章节中外貌、性格、能力、人际关系有无不一致？
   比如：第一章说他有妹妹，第三章变成独生子。第一章说他是黑发，第五章变成棕发。

2. 情节逻辑漏洞
   时间线有无冲突？事件先后顺序合理吗？
   比如：第一天还是满月，第三天已经是下弦月。人物不可能在 10 分钟内从城东到城西。

3. 伏笔回收情况
   前文提到的线索、物品、人物后续有没有交代？
   注意识别"看起来像伏笔但实际没用上"的情节线。

4. 细节前后照应
   地名、人名、日期、物品描述在不同章节中写法是否一致？
   比如：第一章叫"张伟"，第五章变成"张玮"。第一章的伤在左臂，后面变成右臂。

输出格式：

## 一致性检查报告

### 🚨 严重问题（必须改）
- [章节A vs 章节B] 问题描述 | 原文引用

### ⚠️ 建议修正
- [章节A] 问题描述 | 原文引用

### 📌 伏笔跟踪
- 已回收：[线索] → 出现在[章节X]，回收在[章节Y]
- 未回收：[线索] → 出现在[章节X]，后续未提及

### ✅ 通过项
- 人物连贯、时间线合理、细节一致等方面

注意：没有问题时也要写"未发现问题"，不要强行找茬。
"""


def run_check(file_paths, detail=False):
    if not file_paths:
        return "[ERROR] 请提供至少一个文件"

    texts = []
    for fp in file_paths:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            name = os.path.basename(fp)
            texts.append(f"=== {name} ===\n{content}")
        except FileNotFoundError:
            return f"[ERROR] 文件不存在: {fp}"

    if len(texts) < 2:
        return "[ERROR] 一致性检查需要至少 2 个章节才能对比"

    user_prompt = "请检查以下文本的一致性：\n\n" + "\n\n".join(texts)

    result = call_llm(SYSTEM_CONSISTENCY, user_prompt)

    if detail:
        return result
    else:
        lines = result.split("\n")
        summary = []
        for line in lines:
            if line.startswith("###") or line.startswith("##"):
                summary.append(line)
            elif line.startswith("-") and any(
                kw in line for kw in ["严重", "建议", "未回收"]
            ):
                summary.append(line)
        if not summary:
            return result
        return "\n".join(summary)


def read_files_from_dir(dir_path):
    exts = (".md", ".txt", ".docx")
    files = []
    for f in sorted(os.listdir(dir_path)):
        if f.lower().endswith(exts):
            files.append(os.path.join(dir_path, f))
    return files


def main():
    parser = argparse.ArgumentParser(description="AI 写作搭子 — 一致性检查")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--files", type=str, help="章节文件列表，逗号分隔")
    group.add_argument("--dir", type=str, help="章节所在目录（自动按文件名排序）")

    parser.add_argument("--detail", action="store_true", help="输出完整报告而非摘要")

    args = parser.parse_args()

    if args.files:
        file_paths = [f.strip() for f in args.files.split(",")]
    elif args.dir:
        file_paths = read_files_from_dir(args.dir)
        if not file_paths:
            print(f"[ERROR] 目录 {args.dir} 中没有找到 .md/.txt 文件")
            return
        print(f"从目录加载了 {len(file_paths)} 个文件")

    print(run_check(file_paths, args.detail))


if __name__ == "__main__":
    main()
