#!/usr/bin/env python3
"""
AI 写作搭子 — 核心脚本 v1.2
用法:
  python writing_buddy.py review --file <路径>
  python writing_buddy.py review --compare old.md new.md
  python writing_buddy.py brainstorm --context "卡壳内容"
"""

import argparse
import os
import re
import requests

API_KEY = os.environ.get("WRITING_BUDDY_API_KEY", "")
API_BASE = os.environ.get("WRITING_BUDDY_API_BASE", "https://api.deepseek.com")
MODEL = os.environ.get("WRITING_BUDDY_MODEL", "deepseek-chat")
MAX_TOKENS = 6000


def call_llm(system_prompt, user_prompt):
    if not API_KEY:
        return "[ERROR] 请先设置环境变量 WRITING_BUDDY_API_KEY"
    headers = {"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    try:
        base = API_BASE.rstrip("/")
        resp = requests.post(base + "/v1/chat/completions", headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return "[ERROR] API 调用失败: " + str(e)


# === 痛点3：长度检查 ===

def check_text_length(text, label="文本"):
    est = len(text) * 1.5
    if est > MAX_TOKENS:
        segs = int(est / MAX_TOKENS) + 1
        size = len(text) // segs
        out = "[WARNING] " + label
        out += "较长（约" + str(int(est)) + " token，上限" + str(MAX_TOKENS) + " token）\n"
        out += "建议分为 " + str(segs) + " 段，每段约 " + str(size) + " 字分别检查。\n"
        return out
    return ""


# === 文本类型检测 ===

NARRATIVE_CLUES = [r"他说", r"她说", r"我想", r"我觉得", r"走了", r"来到", r"推开",
                   r"看见", r"这时", r"突然", r"然后", r"第[一二三四五六七八九十]章"]
ARGUE_CLUES = [r"我认为", r"我觉得", r"首先", r"其次", r"最后", r"因为", r"所以",
               r"因此", r"但是", r"然而", r"一方面", r"另一方面"]


def detect_text_type(text):
    if not text.strip():
        return "argumentative"
    n = sum(len(re.findall(c, text)) for c in NARRATIVE_CLUES)
    a = sum(len(re.findall(c, text)) for c in ARGUE_CLUES)
    d = len(re.findall(r'["""‘’]', text))
    if d > 2:
        n += d // 4
    total = n + a
    if total == 0:
        return "argumentative"
    r = n / total
    if r > 0.65:
        return "narrative"
    if r < 0.35:
        return "argumentative"
    return "mixed"


# === Prompts ===

SYS_REV_NARR = ("你是一个有文学素养的编辑伙伴。分析用户写的文字给出有洞察力的反馈。"
    "不要夸奖过头，不要只说好话。从以下五个维度分析，每个维度1-2句加一个例子："
    "1.结构：开头抓人吗？段落衔接自然吗？"
    "2.人物：人物立住了吗？对话符合性格吗？"
    "3.细节：好的细节描写？环境动作感官够不够？"
    "4.节奏：哪里闷了哪里太赶？"
    "5.语言：用词准吗？句式有变化吗？"
    "最后给1个最需要改的问题（别超过1个）。"
    "在最后加一段'建议修改方向'——针对最需要改的问题，给1-2句具体的改写思路。"
    "格式：直接、具体、不绕弯。")

SYS_REV_ARG = ("你是一个有文学素养的编辑伙伴。分析用户的议论文或经验分享，给出有洞察力的反馈。"
    "不要夸奖过头。从以下五个维度分析，每个维度1-2句加一个例子："
    "1.结构：开头抓人吗？段落衔接自然吗？逻辑递进吗？"
    "2.论点与论据：观点明确吗？有具体例子支撑吗？有没有只说了结论没给过程？"
    "3.细节：具体场景事例数据让观点活起来？还是全程抽象说理？"
    "4.节奏：信息密度合适吗？有没有一句话塞三个观点？"
    "5.语言：用词准吗？句式有变化吗？套话多不多？"
    "最后给1个最需要改的问题。"
    "在最后加一段'建议修改方向'——针对最需要改的问题，给1-2句具体的改写思路。"
    "格式：直接、具体、不绕弯。")

SYS_REV_MIX = ("你是一个有文学素养的编辑伙伴。分析用户写的文字，关注叙事和议论的结合是否自然。"
    "从以下五个维度分析："
    "1.结构：整体安排合理吗？叙事和议论穿插有节奏感吗？"
    "2.人物/观点：人物立住了吗？有观点的话论据够吗？"
    "3.细节：描写够具体吗？例子有没有让内容活起来？"
    "4.节奏：哪里太赶哪里太拖？"
    "5.语言：用词有特色吗？句式有变化吗？"
    "最后给1个最需要改的问题。"
    "在最后加一段'建议修改方向'——针对最需要改的问题，给1-2句具体的改写思路。")

SYS_COMPARE = ("你是一个编辑伙伴。用户给了同一篇文章的修改前和修改后两个版本。"
    "你的任务是对比分析用户的修改是否有效。"
    "从以下维度分析："
    "1.改动摘要：用户改了哪些地方？"
    "2.每条改动是否有效：改前是什么问题？改后解决了吗？"
    "3.是否引入新问题：新版本有没有旧版没有的问题？"
    "4.综合评价：这篇值得改吗？改完之后整体提升多少？"
    "最后给1句总评。格式：直接、具体。")

SYS_STORM = ("你是一个写作灵感伙伴。用户卡壳了，需要你帮忙梳理思路。"
    "你的任务："
    "1.先帮用户理清ta最想解决的核心问题是什么"
    "2.给3个不同的发展方向（不要只给一个）"
    "3.每个方向用2-3句话：怎么发展、效果、风险"
    "4.如果用户提供了已有角色/设定，必须基于已有内容发散"
    "最后加一段'下一步建议'："
    "针对用户最可能选的方向，给1-2句现在就可以开始写的具体句子或开头。"
    "让用户看完就能动手写。注意：不要替用户写全文，给个开头就够了。")


# === review 模式 ===

def review(text):
    if not text.strip():
        return "[ERROR] 没有输入内容"
    warn = check_text_length(text, "输入文本")
    t = detect_text_type(text)
    pm = {"narrative": SYS_REV_NARR, "argumentative": SYS_REV_ARG, "mixed": SYS_REV_MIX}
    sp = pm.get(t, SYS_REV_ARG)
    result = call_llm(sp, text)
    return warn + "\n" + result if warn else result


# === 对比模式（修复痛点2） ===

def compare(old_text, new_text):
    if not old_text.strip() or not new_text.strip():
        return "[ERROR] 两个版本都需要提供内容"
    w1 = check_text_length(old_text, "原版")
    w2 = check_text_length(new_text, "修改版")
    up = "【修改前】\n" + old_text + "\n\n【修改后】\n" + new_text
    result = call_llm(SYS_COMPARE, up)
    ws = w1 + w2
    return ws + "\n" + result if ws else result


# === brainstorm 模式 ===

def brainstorm(context):
    if not context.strip():
        return "[ERROR] 请提供当前写作上下文"
    warn = check_text_length(context, "上下文")
    result = call_llm(SYS_STORM, context)
    return warn + "\n" + result if warn else result


# === 主入口 ===

def read_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def main():
    parser = argparse.ArgumentParser(description="AI 写作搭子 - v1.2")
    sub = parser.add_subparsers(dest="mode")

    pv = sub.add_parser("review", help="给写作内容反馈")
    pv.add_argument("--file", type=str)
    pv.add_argument("--text", type=str)
    pv.add_argument("--compare", nargs=2, metavar=("旧版", "新版"),
                    help="对比修改前后两个版本")

    ps = sub.add_parser("brainstorm", help="卡壳时找方向")
    ps.add_argument("--context", type=str)
    ps.add_argument("--file", type=str)

    args = parser.parse_args()
    if not args.mode:
        parser.print_help()
        return

    if args.mode == "review":
        if args.compare:
            o, n = args.compare
            ot = read_file_content(o)
            nt = read_file_content(n)
            if ot is None or nt is None:
                print("[ERROR] 文件不存在")
                return
            print(compare(ot, nt))
            return
        if args.file:
            txt = read_file_content(args.file)
            if txt is None:
                print("[ERROR] 文件不存在: " + args.file)
                return
        elif args.text:
            txt = args.text
        else:
            print("[ERROR] 请提供 --file 或 --text 或 --compare")
            return
        print(review(txt))

    elif args.mode == "brainstorm":
        if args.file:
            ctx = read_file_content(args.file)
            if ctx is None:
                print("[ERROR] 文件不存在: " + args.file)
                return
        elif args.context:
            ctx = args.context
        else:
            print("[ERROR] 请提供 --context 或 --file")
            return
        print(brainstorm(ctx))


if __name__ == "__main__":
    main()
