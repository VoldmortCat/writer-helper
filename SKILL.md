---
name: ai-writing-buddy
description: "AI 写作搭子：写一段给反馈，卡壳时帮梳理思路。"
version: 1.1.0
author: Hermes Agent
license: MIT
tags: [writing, creative-writing, editing, argumentative]
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [writing, creative-writing, editing, argumentative]
    category: creative
---

# AI 写作搭子 Skill

## 概述

AI 写作搭子是一个**编辑伙伴 + 灵感催化剂**，不是代写工具。你写一段，AI 给反馈，卡壳时帮你梳理思路。

**AI 核心价值：**
- 代笔 -> 任何 AI 都能做
- ✅ **给有洞察力的反馈**（结构/论点/人物/逻辑）-> 只有能理解文本结构的 AI 才能做
- ✅ **卡壳时帮你梳理思路** -> 基于你已有的上下文给出方向
- ✅ **自动识别文本类型** -> 议论文用论点维度，叙事文用人物维度

## 迭代记录

当前版本 v1.1 — 迭代1：自动检测文本类型，按类型适配分析维度

## 何时使用

- 写完一段需要反馈 -> review 模式
- 写作卡壳写不下去了 -> brainstorm 模式
- 写议论文/经验分享/公众号文章 -> review 自动适配"论点与论据"维度
- 写小说/叙事/故事 -> review 自动使用"人物"维度

## 先决条件

- Python 3.8+
- DeepSeek API（免费额度即可）
- `pip install requests`

## 快速开始

### 1. 设置 API Key

```bash
set WRITING_BUDDY_API_KEY=your_deepseek_api_key
```

### 2. 使用

```bash
# 给写作内容反馈（自动判断议论文还是叙事文）
python scripts/writing_buddy.py review --file 我的文章.txt

# 卡壳时找方向
python scripts/writing_buddy.py brainstorm --context "我写到一个侦探发现..."
```

## 脚本说明

### style_learner.py — 风格学习（迭代2）

学习你的写作风格，新文章保持风格一致，不出 AI 腔。

```bash
# 学习风格：用一篇你满意的旧文训练
python scripts/style_learner.py learn --reference 你的旧作.md --name my_style

# 检查新文章是否像你写的
python scripts/style_learner.py check --name my_style --target 新文章.md

# 查看已学习的风格
python scripts/style_learner.py list
```

learn 模式分析维度：用词偏好、句式特征、语气态度、修辞习惯、标点习惯。
check 模式对比统计特征 + AI 风格一致性分析。

### consistency_check.py — 一致性检查

长篇写作后检查前后矛盾。扫描多章，输出 4 类问题：
- **人物设定矛盾**：外貌/性格/能力/关系前后不一致
- **情节逻辑漏洞**：时间线冲突、因果关系断裂
- **伏笔回收情况**：前文埋的线后面收没收
- **细节前后照应**：地名/人名/物品描述写错

```bash
python scripts/consistency_check.py --files “第1章.md,第2章.md,第3章.md”
python scripts/consistency_check.py --dir 小说目录/
```

### writing_buddy.py

**文本类型自动检测（v1.1 新增）：**
系统会扫描文本中的特征词判断写作类型：
- 有对话、人称、情节推进 -> 叙事类，使用"结构/人物/细节/节奏/语言"五维度
- 有观点词、论证结构、总结句 -> 议论文类，使用"结构/论点与论据/细节/节奏/语言"五维度
- 两者都有 -> 混合类，使用适配的分析维度

两个模式：

- **review**：传入写作内容，自动检测文本类型，按类型适配分析维度给出反馈
- **brainstorm**：传入当前写作上下文，给出 3 个可能的发展方向

## 操作步骤

1. 设置 API Key
2. 写一段文字（300-1000 字）
3. 运行 `review` 获取反馈（自动适配文本类型）
4. 卡壳时运行 `brainstorm` 获取方向灵感

## 陷阱

| 陷阱 | 说明 |
|------|------|
| API Key 泄露 | 不要硬编码在脚本里，用环境变量 |
| AI 反馈是建议不是圣旨 | 最终判断你做主 |
| 不要用于代写 | 本工具帮你写得更好，不是替你写 |
| 短文本误判 | 少于 100 字的文本类型判断可能不准，建议凑够 300 字再跑 review |
